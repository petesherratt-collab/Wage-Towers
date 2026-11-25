"""Designed synthetic experiment; standard library only. No collection or live data.

Separate functions implement economics, observation publication, assessment and
evaluation. Run once per destination: python work/longitudinal_indicator_v02.py
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTCOMES = ('hours', 'separations', 'hiring', 'pay')
MASKS = ('complete', 'contractors', 'task', 'comparison', 'pay_panel', 'extraction')
CASES = [
    dict(name='No adoption', ai=False),
    dict(name='Announcement without execution', ai=False, claim=True),
    dict(name='AI staffing cuts', cut=.30),
    dict(name='Reduced paid schedules', cut=.30, schedules=True),
    dict(name='Suppressed hiring during growth', cut=.30, growth=.60),
    dict(name='Demand absorbs savings', cut=.30, rebound=1/.70-1),
    dict(name='Valuable reassignment', cut=0),
    dict(name='Retained option capacity', cut=0),
    dict(name='Delayed staffing review', cut=.30, onset=7),
    dict(name='Expertise premium loss', wage=.25),
    dict(name='Combined hours and pay', cut=.30, wage=.20),
    dict(name='External demand contraction', demand=-.30),
    dict(name='Outsourcing with stable paid work', outsourcing=True),
    dict(name='Workforce composition changes', composition=True),
    dict(name='Quality deterioration', external=.30, blocker='quality deterioration'),
    dict(name='Preplanned restructuring disclosed', external=.30, blocker='preplanned restructuring'),
    dict(name='Hidden restructuring fools comparator', external=.30),
    dict(name='Adoption selection on declining demand', external=.30, blocker='differential pre-trend', pretrend=True),
    dict(name='Contaminated comparator', cut=.30, contam=.30, blocker='comparator AI exposure'),
    dict(name='AI demand expansion exceeds savings', cut=.30, rebound=.70),
    dict(name='Ambiguous AI cause', cut=.30, no_comparison=True),
    dict(name='Ambiguous non-AI cause', external=.30, no_comparison=True),
    dict(name='Small real effect below default cutoff', cut=.08),
]


def economics(spec):
    """Paired potential outcomes; fixed-price real pay, no market equilibrium."""
    actual, counterfactual, comparison = [], [], []
    for q in range(11):
        post = q >= 3
        active = q >= spec.get('onset', 3)
        base = 100 * (1 + (spec.get('demand', 0) + spec.get('growth', 0)) * post)
        # External restructuring affects both potential outcomes, but not the
        # comparator: this deliberately violates parallel untreated changes.
        external = spec.get('external', 0) * post
        if spec.get('pretrend') and q < 3:
            external = .05 * q
        h0 = base * (1-external)
        h1 = h0 * (1+spec.get('rebound', 0)*post) * (1-spec.get('cut', 0)*active)
        n0 = h0
        n1 = h0 if spec.get('schedules') else h1
        p1 = 100 * (1-spec.get('wage', 0)*active)
        for series, h, n, pay in ((actual, h1, n1, p1), (counterfactual, h0, n0, 100),
                                  (comparison, base*(1-spec.get('contam', 0)*post),
                                   base*(1-spec.get('contam', 0)*post), 100)):
            prior = series[-1]['headcount'] if series else n
            # Ten routine hires and separations, plus expansion/contraction.
            series.append(dict(q=q, hours=h, headcount=n, pay=pay,
                               hiring=10+max(0, n-prior), separations=10+max(0, prior-n)))
        actual[-1].update(output=base*(1+spec.get('rebound', 0)*post),
                          employee_hours=h1*(.70 if spec.get('outsourcing') and post else 1),
                          mean_pay=80 if spec.get('composition') and post else p1)
    return actual, counterfactual, comparison


def observations(spec, actual, comparison, delay, mask):
    """Publication ledger: payloads contain no family, title or causal truth."""
    records = []
    for a, c in zip(actual, comparison):
        q = a['q']
        records.append(dict(period=q, available=q+delay, source=f'synthetic-record-q{q}',
                            payload=dict(actual=a, comparator=c,
                            task_minutes=4 if q >= 3 and spec.get('ai', True) else 10,
                            task_verified=mask != 'task',
                            quality_ok=spec.get('blocker') != 'quality deterioration',
                            scope_ok=mask != 'contractors', panel_ok=mask != 'pay_panel',
                            extraction_ok=mask != 'extraction',
                            comparison_ok=not spec.get('no_comparison') and mask != 'comparison',
                            blockers=[spec['blocker']] if spec.get('blocker') else [],
                            adoption_reported=spec.get('ai', True) or spec.get('claim', False))))
    return records


def assess(records, date, threshold):
    """Only published evidence is admitted. Nothing here reads CASES or truth."""
    available = [r for r in records if r['available'] <= date]
    result = dict(assessment_date=date, latest_period=None, task='unknown', intensity_gap=None,
                  outcomes={k: dict(signal='unknown', adequacy='insufficient', attribution='unresolved',
                                    gap=None, observed_change=None, alert=False) for k in OUTCOMES})
    if not available:
        return result
    available.sort(key=lambda r: r['period'])
    b, end = available[0]['payload'], available[-1]['payload']
    result['latest_period'] = available[-1]['period']
    valid = all(r['payload']['extraction_ok'] for r in available)
    task_ok = valid and b['task_verified'] and end['task_verified'] and end['quality_ok']
    if task_ok:
        result['task'] = 'supported' if end['task_minutes'] < b['task_minutes'] else 'not established'
    a, c = end['actual'], end['comparator']
    if valid and end['scope_ok']:
        result['intensity_gap'] = 1-(a['hours']/b['actual']['hours'])/(a['output']/b['actual']['output'])
    # Assess cumulative post-baseline flows; a flow threshold uses comparator
    # cumulative flows as denominator. Stocks use endpoint ratios of changes.
    for key in OUTCOMES:
        o = result['outcomes'][key]
        scope = end['scope_ok'] if key != 'pay' else end['panel_ok']
        if valid and scope:
            o['observed_change'] = a[key]-b['actual'][key]
        if not (valid and scope and end['comparison_ok'] and len(available) >= 2):
            continue
        if key in ('hiring', 'separations'):
            aa = sum(r['payload']['actual'][key] for r in available[1:])
            cc = sum(r['payload']['comparator'][key] for r in available[1:])
            gap = (aa-cc)/cc if key == 'separations' else (cc-aa)/cc
            o['observed_change'] = aa  # cumulative flow, explicitly labelled in specification
        else:
            gap = 1-(a[key]/b['actual'][key])/(c[key]/b['comparator'][key])
        o.update(gap=gap, signal='positive' if gap > threshold+1e-12 else 'below cutoff', adequacy='adequate')
        if end['blockers']:
            o['attribution'] = 'unresolved: ' + '; '.join(end['blockers'])
        elif result['task'] == 'supported' and result['latest_period'] >= 3:
            o['attribution'] = 'conditional support' if o['signal'] == 'positive' else 'not established'
        o['alert'] = o['signal'] == 'positive' and o['attribution'] == 'conditional support'
    return result


def truth_at(actual, cf, q):
    return dict(hours=actual[q]['hours'] < cf[q]['hours']-1e-9,
                pay=actual[q]['pay'] < cf[q]['pay']-1e-9,
                hiring=sum(x['hiring'] for x in actual[1:q+1]) < sum(x['hiring'] for x in cf[1:q+1])-1e-9,
                separations=sum(x['separations'] for x in actual[1:q+1]) > sum(x['separations'] for x in cf[1:q+1])+1e-9)


def evaluate(runs):
    metrics = {}
    for key in OUTCOMES:
        m = dict(n=len(runs), positives=0, negatives=0, true_alerts=0, false_alerts=0,
                 definitive_misses=0, positive_abstentions=0, abstentions=0,
                 detected_delays=[], censored=0)
        for run in runs:
            t = run['truth'][-1][key]
            o = run['assessments'][-1]['outcomes'][key]
            abstain = o['signal'] == 'unknown' or o['attribution'].startswith('unresolved')
            m['positives' if t else 'negatives'] += 1
            m['abstentions'] += abstain
            m['true_alerts'] += t and o['alert']
            m['false_alerts'] += not t and o['alert']
            m['positive_abstentions'] += t and abstain
            m['definitive_misses'] += t and not o['alert'] and not abstain
            if t:
                onset = next(q for q, truth in enumerate(run['truth']) if truth[key])
                first = next((a['assessment_date'] for a in run['assessments']
                              if a['assessment_date'] >= onset and a['outcomes'][key]['alert']), None)
                if first is None:
                    m['censored'] += 1
                else:
                    m['detected_delays'].append(first-onset)
        def ratio(n, d):
            return n/d if d else None
        m.update(false_alarm_rate=ratio(m['false_alerts'], m['negatives']),
                 recall=ratio(m['true_alerts'], m['positives']),
                 coverage=1-m['abstentions']/m['n'],
                 precision=ratio(m['true_alerts'], m['true_alerts']+m['false_alerts']),
                 missed_including_abstention=m['positives']-m['true_alerts'])
        metrics[key] = m
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='outputs/longitudinal-v02/run-001')
    args = parser.parse_args()
    dest = ROOT / args.out
    if dest.exists():
        raise SystemExit('Destination exists; choose a new --out to preserve prior runs.')
    baseline_files = list((ROOT/'outputs/synthetic-indicator').glob('*'))
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    baseline_before = {str(p.relative_to(ROOT)): digest(p) for p in baseline_files}
    runs, packets, truths = [], [], []
    for i, spec in enumerate(CASES):
        actual, cf, comp = economics(spec)
        truth = [truth_at(actual, cf, q) for q in range(11)]
        truths.append(dict(id=i, specification=spec, actual=actual, no_ai=cf, truth=truth))
        for delay in (0, 2, 5):
            for mask in MASKS:
                records = observations(spec, actual, comp, delay, mask)
                packets.append(dict(id=i, delay=delay, mask=mask, records=records))
                for threshold in (.05, .10, .20):
                    assessments = [assess(records, q, threshold) for q in range(11)]
                    # Unpublished content cannot affect an assessment.
                    for q in range(11):
                        assert assessments[q] == assess([r for r in records if r['available'] <= q], q, threshold)
                    runs.append(dict(id=i, delay=delay, mask=mask, threshold=threshold,
                                     truth=truth, assessments=assessments))
    def selected(i, delay=0, mask='complete', threshold=.10):
        return next(r for r in runs if (r['id'], r['delay'], r['mask'], r['threshold']) == (i, delay, mask, threshold))
    for delay in (0, 2, 5):
        for mask in MASKS:
            assert selected(20, delay, mask)['assessments'] == selected(21, delay, mask)['assessments']
    end = lambda i: selected(i)['assessments'][-1]
    assert end(16)['outcomes']['hours']['alert'] and not selected(16)['truth'][-1]['hours']
    assert end(4)['outcomes']['hiring']['alert']
    assert not end(13)['outcomes']['pay']['alert']
    assert not end(5)['outcomes']['hours']['alert'] and end(5)['intensity_gap'] > .1
    assert selected(8, 5)['assessments'][-1]['outcomes']['hours']['alert'] is False
    assert all(not r['assessments'][-1]['outcomes']['hours']['alert'] for r in runs if r['mask']=='contractors')
    assert baseline_before == {str(p.relative_to(ROOT)): digest(p) for p in baseline_files}
    main_runs = [r for r in runs if r['delay']==0 and r['mask']=='complete' and r['threshold']==.10]
    summary = dict(primary=evaluate(main_runs), grid=evaluate(runs),
                   by_setting=[dict(delay=d, mask=m, threshold=t, metrics=evaluate([
                       r for r in runs if (r['delay'],r['mask'],r['threshold'])==(d,m,t)]))
                       for d in (0,2,5) for m in MASKS for t in (.05,.10,.20)])
    files = [Path(__file__), ROOT/'research/experiment-plan-v02.md', ROOT/'work/wage-towers/dist/model.js',
             ROOT/'work/wage-towers/test.cjs', ROOT/'work/synthetic_indicator.py']
    manifest = dict(command=f'python work/longitudinal_indicator_v02.py --out {args.out}',
                    seed=None, randomness='none; exhaustive designed grid', periods=list(range(11)),
                    scenarios=len(CASES), runs=len(runs), assessments=len(runs)*11,
                    hashes={str(p.relative_to(ROOT)):digest(p) for p in files}, baseline_hashes=baseline_before,
                    split='development only; no holdout', assertions='passed')
    dest.mkdir(parents=True)
    for filename, obj in [('manifest.json',manifest), ('truth.json',truths), ('observations.json',packets),
                          ('assessments.json',[{k:v for k,v in r.items() if k!='truth'} for r in runs]),
                          ('evaluation.json',summary)]:
        (dest/filename).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    rows=[]
    for i,spec in enumerate(CASES):
        a=end(i)
        rows.append('| '+ ' | '.join([str(i),spec['name'],a['task']]+[
            ('alert' if a['outcomes'][k]['alert'] else a['outcomes'][k]['signal'])+
            (' / unresolved' if a['outcomes'][k]['attribution'].startswith('unresolved') else '') for k in OUTCOMES])+' |')
    report = '# v0.2 synthetic results\n\nAll cases are artificial development histories. No validation claim.\n\n'
    report += '| ID | Mechanism | Task | Hours | Excess separations | Hiring gap | Pay |\n|---|---|---|---|---|---|---|\n'+'\n'.join(rows)
    report += '\n\n## Primary evaluation: complete records, zero delay, 10% cutoff\n\n'
    report += '| Outcome | True positives in design | True negatives in design | Correct alerts | False alerts | Definitive misses | Positive abstentions | Coverage |\n|---|---|---|---|---|---|---|---|\n'
    for k,m in summary['primary'].items():
        report += f"| {k} | {m['positives']} | {m['negatives']} | {m['true_alerts']} | {m['false_alerts']} | {m['definitive_misses']} | {m['positive_abstentions']} | {m['coverage']:.1%} |\n"
    report += '\nEvaluation JSON contains all 54 parameter/evidence settings, denominators, false-alert rates, recall, precision, censoring and detected-delay lists. Grid totals repeat the same histories and are not independent samples. Truth counts every strictly adverse causal effect, including below-cutoff effects. Cumulative flow signals can dilute over time: first detection and endpoint detection differ.\n'
    (dest/'results.md').write_text(report,encoding='utf-8')
    print(json.dumps(dict(manifest=manifest,primary=summary['primary']),indent=2))


if __name__ == '__main__':
    main()
