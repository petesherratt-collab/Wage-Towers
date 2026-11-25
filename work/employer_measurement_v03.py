"""Observation publication and indicator. Does not import economic model/truth."""
STOCKS = ('hours', 'headcount', 'pay')
FLOWS = ('hiring', 'layoffs')
OUTCOMES = STOCKS+FLOWS
PROFILES = {
    'immediate': dict(task=0, workforce=0, pay=0, audit=0),
    'staggered': dict(task=0, workforce=2, pay=3, audit=1),
    'long_workforce_lag': dict(task=0, workforce=5, pay=3, audit=1),
    'missing_scope': dict(task=0, workforce=0, pay=0, audit=0),
    'selective_withholding': dict(task=0, workforce=0, pay=0, audit=0),
}


def observe(actual, comparator, specification, profile):
    """Actual published values only; hidden potential path is not an argument."""
    lags = PROFILES[profile]
    records = []
    def add(kind, q, value):
        records.append(dict(kind=kind, period=q, available=q+lags[kind],
                            source=f'synthetic-{kind}-{q}', value=value))
    for a,c in zip(actual,comparator):
        q = a['q']
        add('task',q,dict(minutes=a['task_minutes'],verified=True,quality=True))
        audit = dict(blockers=[specification['blocker']] if specification.get('blocker') and q>=3 else [],
                     comparison=not specification.get('no_comparison',False))
        if profile != 'missing_scope':
            audit['scope'] = True
        add('audit',q,audit)
        withheld = profile == 'selective_withholding' and q>=3 and a['hours']<actual[2]['hours']
        if not withheld:
            add('workforce',q,dict(actual={k:a[k] for k in ('hours','headcount','hiring','layoffs')},
                                   comparator={k:c[k] for k in ('hours','headcount','hiring','layoffs')}))
            add('pay',q,dict(actual=a['pay'],comparator=c['pay'],panel=True))
    return records


def assess(records, date, threshold=.10, flow_rule='cumulative'):
    published = [r for r in records if r['available']<=date]
    lookup = {(r['kind'],r['period']):r['value'] for r in published}
    result = dict(date=date, flow_rule=flow_rule, outcomes={})
    for key in OUTCOMES:
        kind = 'pay' if key=='pay' else 'workforce'
        # Freeze q3..q6 event window only when complete, retaining event meaning.
        end = 6 if key in FLOWS and flow_rule=='fixed_event' else max(
            (q for k,q in lookup if k==kind), default=-1)
        o = dict(signal='unknown', adequacy='insufficient', attribution='unresolved',
                 gap=None, alert=False, current_alert=False, observed_period=None,
                 fresh=False, window=None, reasons=[])
        result['outcomes'][key] = o
        if end<3 or (kind,2) not in lookup or (kind,end) not in lookup:
            o['reasons'].append('baseline or outcome unavailable')
            continue
        start = 3
        o.update(observed_period=end, window=[start,end] if key in FLOWS else [end,end],
                 fresh=end==date)
        required = range(start,end+1) if key in FLOWS else [2,end]
        if any((kind,q) not in lookup for q in required):
            o['reasons'].append('incomplete flow window')
            continue
        audit_periods = sorted(set([2]+list(required)))
        audits = [lookup.get(('audit',q),{}) for q in audit_periods]
        if any(a.get('scope') is not True for a in audits):
            o['reasons'].append('workforce boundary unverified')
            continue
        if any(a.get('comparison') is not True for a in audits):
            o['reasons'].append('comparison unavailable')
            continue
        baseline, last = lookup[kind,2], lookup[kind,end]
        if key in STOCKS:
            if key=='pay':
                if not baseline.get('panel') or not last.get('panel'):
                    o['reasons'].append('comparable pay missing')
                    continue
                a0,c0,a1,c1=baseline['actual'],baseline['comparator'],last['actual'],last['comparator']
            else:
                a0,c0,a1,c1=baseline['actual'][key],baseline['comparator'][key],last['actual'][key],last['comparator'][key]
            if min(a0,c0,c1)<=0:
                o['reasons'].append('nonpositive ratio denominator')
                continue
            gap=1-(a1/a0)/(c1/c0)
        else:
            aa=sum(lookup[kind,q]['actual'][key] for q in required)
            cc=sum(lookup[kind,q]['comparator'][key] for q in required)
            # Layoffs have a zero comparator in many genuine displacement cases.
            # Use baseline headcount for both layoff rules; only hiring uses turnover.
            denominator=baseline['comparator']['headcount'] if flow_rule=='fixed_event' or key=='layoffs' else cc
            if denominator<=0:
                o['reasons'].append('zero flow denominator')
                continue
            gap=(cc-aa)/denominator if key=='hiring' else (aa-cc)/denominator
        o.update(gap=gap, signal='positive' if gap>threshold+1e-12 else 'below cutoff',adequacy='adequate')
        tasks=[(q,v) for (k,q),v in lookup.items() if k=='task' and 3<=q<=end]
        base_task=lookup.get(('task',2),{})
        task=base_task.get('verified') and base_task.get('quality') and any(
            v.get('verified') and v.get('quality') and v['minutes']<base_task['minutes'] for q,v in tasks)
        blockers=sorted({b for a in audits for b in a.get('blockers',[])})
        if blockers:
            o['reasons'].extend(blockers)
        elif task:
            o['attribution']='conditional support' if o['signal']=='positive' else 'not established'
        else:
            o['reasons'].append('task replacement unestablished')
        o['alert']=o['attribution']=='conditional support'
        o['current_alert']=o['alert'] and o['fresh'] and key in STOCKS
    return result


def causal_truth(actual, no_ai, key, start, end):
    if key in STOCKS:
        return actual[end][key] < no_ai[end][key]-1e-9
    aa=sum(a[key] for a in actual[start:end+1])
    cc=sum(a[key] for a in no_ai[start:end+1])
    return aa<cc-1e-9 if key=='hiring' else aa>cc+1e-9


def evaluate(runs):
    """Evaluator alone receives hidden no-AI histories. No model import needed."""
    output={}
    for key in OUTCOMES:
        m=dict(n=len(runs), positives=0,negatives=0,true_alerts=0,false_alerts=0,
               positive_abstentions=0,non_alert_misses=0,measurement_adequate=0,
               attribution_decisions=0,fresh=0,historical_assessed=0,historical_false_alerts=0,
               historical_negatives=0,ever_positive=0,detected_delays=[],censored=0,
               historical_detected_delays=[],historical_censored=0)
        for run in runs:
            a,cf=run['actual'],run['no_ai']
            o=run['assessments'][-1]['outcomes'][key]
            end=6 if key in FLOWS and run['flow_rule']=='fixed_event' else 12
            t=causal_truth(a,cf,key,3,end)
            # The evaluated window must match the published one. Fixed-event
            # evidence remains valid for q3..q6; lagged cumulative flows cannot
            # certify the cumulative total through q12.
            aligned=o['observed_period']==end
            abstain=o['attribution']=='unresolved' or not aligned
            alert=o['alert'] and aligned
            m['positives' if t else 'negatives']+=1
            m['true_alerts']+=t and alert
            m['false_alerts']+=not t and alert
            m['positive_abstentions']+=t and abstain
            m['non_alert_misses']+=t and not alert and not abstain
            m['measurement_adequate']+=o['adequacy']=='adequate'
            m['attribution_decisions']+=not abstain
            m['fresh']+=o['fresh']
            if o['observed_period'] is not None:
                ht=causal_truth(a,cf,key,3,o['observed_period'])
                m['historical_assessed']+=1
                m['historical_negatives']+=not ht
                m['historical_false_alerts']+=not ht and o['alert']
            # Ever-loss target covers later events even for a fixed early window.
            onset=next((q for q in range(3,13) if causal_truth(a,cf,key,3,q)),None)
            if onset is not None:
                m['ever_positive']+=1
                for historical in (False,True):
                    detections=[]
                    for assessment in run['assessments']:
                        z=assessment['outcomes'][key]
                        if not z['alert'] or z['observed_period'] is None:
                            continue
                        if not historical and not z['fresh'] and (key in STOCKS or run['flow_rule']=='cumulative'):
                            continue
                        if causal_truth(a,cf,key,3,z['observed_period']) and assessment['date']>=onset:
                            detections.append(assessment['date']-onset)
                    prefix='historical_' if historical else ''
                    if detections:
                        m[prefix+'detected_delays'].append(min(detections))
                    else:
                        m[prefix+'censored']+=1
        def rate(n,d):
            return n/d if d else None
        m.update(false_alarm_rate=rate(m['false_alerts'],m['negatives']),
                 recall=rate(m['true_alerts'],m['positives']),
                 attribution_coverage=rate(m['attribution_decisions'],m['n']),
                 measurement_coverage=rate(m['measurement_adequate'],m['n']),
                 freshness_coverage=rate(m['fresh'],m['n']))
        output[key]=m
    return output
