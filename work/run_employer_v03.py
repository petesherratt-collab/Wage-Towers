"""Run the v0.3 development grid into a new output directory."""
import argparse
import hashlib
import json
from pathlib import Path

from employer_model_v03 import CASES, DEFAULTS, paired
from employer_measurement_v03 import PROFILES, OUTCOMES, assess, evaluate, observe

ROOT=Path(__file__).resolve().parents[1]
SENSITIVITIES=[('cost_zero',dict(layoff_cost=0)),('cost_50000',dict(layoff_cost=50000)),
               ('review_two',dict(review=2)),('retention_24',dict(option_value=24)),
               ('retention_26',dict(option_value=26)),('new_value_26',dict(new_value=26))]


def hashes(paths):
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='outputs/employer-v03/run-001')
    args=parser.parse_args()
    dest=(ROOT/args.out).resolve()
    if not dest.is_relative_to((ROOT/'outputs/employer-v03').resolve()):
        raise SystemExit('Destination must be within outputs/employer-v03.')
    if dest.exists():
        raise SystemExit('Destination exists; choose another numbered directory.')
    baseline_paths=list((ROOT/'outputs/synthetic-indicator').rglob('*'))+list((ROOT/'outputs/longitudinal-v02').rglob('*'))
    baseline_hashes=hashes(baseline_paths)
    runs, truths, packets=[],[],[]
    scenarios=CASES+SENSITIVITIES
    for i,(name,p) in enumerate(scenarios):
        actual,no_ai,comparison=paired(p)
        truths.append(dict(id=i,name=name,parameters={**DEFAULTS,**p},
                           actual=actual,no_ai=no_ai,comparison=comparison,
                           family='structural' if i<len(CASES) else 'parameter sensitivity'))
        for profile in PROFILES:
            records=observe(actual,comparison,p,profile)
            packets.append(dict(id=i,profile=profile,records=records))
            for threshold in (.05,.1,.2):
                for flow_rule in ('cumulative','fixed_event'):
                    assessments=[assess(records,q,threshold,flow_rule) for q in range(13)]
                    runs.append(dict(id=i,profile=profile,threshold=threshold,flow_rule=flow_rule,
                                     actual=actual,no_ai=no_ai,assessments=assessments))
    settings=[]
    for profile in PROFILES:
        for threshold in (.05,.1,.2):
            for flow_rule in ('cumulative','fixed_event'):
                for family in ('structural','parameter sensitivity'):
                    subset=[r for r in runs if r['profile']==profile and r['threshold']==threshold
                            and r['flow_rule']==flow_rule and (r['id']<len(CASES))==(family=='structural')]
                    settings.append(dict(profile=profile,threshold=threshold,flow_rule=flow_rule,
                                         family=family,metrics=evaluate(subset)))
    primary=next(s['metrics'] for s in settings if s['profile']=='immediate' and s['threshold']==.1
                 and s['flow_rule']=='cumulative' and s['family']=='structural')
    sources=[ROOT/'work'/n for n in ('employer_model_v03.py','employer_measurement_v03.py',
                                    'run_employer_v03.py','test_employer_v03.py')]
    sources.append(ROOT/'research/experiment-plan-v03.md')
    manifest=dict(command=f'python -B work/run_employer_v03.py --out {args.out}',
                  date='2026-11-25',scenarios=len(scenarios),structural_cases=len(CASES),
                  parameter_cases=len(SENSITIVITIES),variants=len(runs),assessments=len(runs)*13,
                  periods=list(range(13)),seed=None,randomness='none; deterministic designed grid',
                  split='development only; no holdout',source_hashes=hashes(sources),
                  preserved_output_hashes=baseline_hashes,profiles=PROFILES,
                  thresholds=[.05,.1,.2],flow_rules=['cumulative','fixed_event'],
                  repository='https://github.com/petesherratt-collab/Wage-Towers',
                  repository_status='empty at read-only inspection; no remote changes')
    assert baseline_hashes==hashes(baseline_paths)
    dest.mkdir(parents=True)
    for name,obj in [('manifest.json',manifest),('truth.json',truths),('observations.json',packets),
                     ('assessments.json',[{k:v for k,v in r.items() if k not in ('actual','no_ai')} for r in runs]),
                     ('evaluation.json',dict(primary=primary,settings=settings))]:
        (dest/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
    rows=[]
    for t in truths:
        a,c=t['actual'],t['no_ai']
        rows.append(f"| {t['id']} | {t['name']} | {a[3]['headcount']} | {a[6]['headcount']} | {a[12]['headcount']} / {c[12]['headcount']} | {sum(x['hiring'] for x in a[3:])} / {sum(x['hiring'] for x in c[3:])} | {sum(x['layoffs'] for x in a[3:])} / {sum(x['layoffs'] for x in c[3:])} |")
    report='# v0.3 generated results\n\nSynthetic development cases; no empirical validation. Actual / no-AI pairs where shown. All workers have 500 paid hours per quarter.\n\n'
    report+='| ID | Case | Staff q3 | Staff q6 | Staff q12 actual / no-AI | Hires q3–q12 | Layoffs q3–q12 |\n|---|---|---|---|---|---|---|\n'+'\n'.join(rows)
    report+='\n\nPrimary: 17 structural histories, immediate publication, 10% threshold, cumulative flows.\n\n| Outcome | Positives | Negatives | True alerts | False alerts | Positive abstentions | Non-alert misses | Attribution coverage |\n|---|---|---|---|---|---|---|---|\n'
    for k,m in primary.items():
        report+=f"| {k} | {m['positives']} | {m['negatives']} | {m['true_alerts']} | {m['false_alerts']} | {m['positive_abstentions']} | {m['non_alert_misses']} | {m['attribution_coverage']:.1%} |\n"
    report+='\nFull evaluation retains all settings, current versus historical evidence, coverage, delay lists and censoring. Pay is a null-only outcome here; its sensitivity cannot be estimated. Fixed-event flows target q3–q6 and have different denominators from cumulative hiring; do not compare raw accuracy as if the estimands were identical. See research/employer-experiment-v03.md for interpretation.\n'
    (dest/'results.md').write_text(report,encoding='utf-8')
    print(json.dumps(dict(variants=len(runs),assessments=len(runs)*13,primary=primary),indent=2))


if __name__=='__main__':
    main()
