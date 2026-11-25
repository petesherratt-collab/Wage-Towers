"""Run the v0.5 literature-grounded experiment into a new output directory."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import panel_v05 as P
from employer_model_v03 import CASES
from employer_model_v05 import V05_DEFAULTS, cohort_simulate, potential_paths, simulate
from employer_measurement_v03 import assess, observe

ROOT = Path(__file__).resolve().parents[1]
SEEDS = range(30)
PANEL_CASES = [(n, dict(CASES)[n]) for n in ('no_adoption', 'valuable_new_work', 'demand_absorption',
                                              'high_retention_value', 'immediate_review',
                                              'attrition_no_layoffs')]
PANEL_CASES += [('shared_new_work', dict(new_value=40, shared_new_work=True)),
                ('small_saving', dict(ai_efficiency=.05))]


def hashes(paths):
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if p.is_file()}


def preserved():
    out = []
    for d in ('outputs/synthetic-indicator', 'outputs/longitudinal-v02', 'outputs/employer-v03', 'outputs/noise-v04'):
        out += [p for p in (ROOT/d).rglob('*') if p.is_file()]
    return out


def v03_hours(actual, comparator, spec=None):
    """v0.3 rule, immediate publication, 10% cutoff, assessed at the last quarter."""
    o = assess(observe(actual, comparator, spec or {}, 'immediate'), len(actual)-1)['outcomes']
    return o


def part_a():
    rows = []
    for name, p in [('uneconomic_new_work', dict(new_value=15)), ('valuable_new_work', dict(new_value=40)),
                    ('new_work_later_automated', dict(new_value=40, pursue=True))]:
        for shared in (False, True):
            q = {**p, 'shared_new_work': shared}
            actual, no_ai = potential_paths(q)
            for comp_label, comp in (('peer without the opportunity', simulate({'ai': False}, False)),
                                     ('peer with the opportunity', simulate({**q, 'ai': False}, False))):
                o = v03_hours(actual, comp)['hours']
                rows.append(dict(part='A', case=name, shared_new_work=shared, comparator=comp_label,
                                 actual_q12=actual[-1]['headcount'], no_ai_q12=no_ai[-1]['headcount'],
                                 true_effect=actual[-1]['hours'] < no_ai[-1]['hours'],
                                 measured_gap=None if o['gap'] is None else round(o['gap'], 4),
                                 alert=o['alert'], attribution=o['attribution']))
    return rows


def part_b():
    rows = []
    for size in (10, 100):
        actual, no_ai = potential_paths(dict(ai_efficiency=.05, size=size))
        comp = simulate({'ai': False, 'size': size}, False)
        o = v03_hours(actual, comp)['hours']
        rows.append(dict(part='B1 small saving (Humlum-Vestergaard pattern)', case=f'size {size}',
                         actual_q12=actual[-1]['headcount'], no_ai_q12=no_ai[-1]['headcount'],
                         true_effect=actual[-1]['hours'] < no_ai[-1]['hours'],
                         measured_gap=round(o['gap'], 4), alert=o['alert'], attribution=o['attribution']))
    ai, base = cohort_simulate(), cohort_simulate(intervention=False)
    for view, key, hires in (('aggregate', 'headcount', ('junior_hires', 'experienced_hires')),
                             ('junior cohort', 'junior', ('junior_hires',))):
        def as_path(path):
            return [dict(q=s['q'], headcount=s[key], hours=500*s[key], hiring=sum(s[h] for h in hires),
                         layoffs=0, pay=25, task_minutes=s['task_minutes']) for s in path]
        a, c = as_path(ai), as_path(base)
        o = v03_hours(a, c)
        rows.append(dict(part='B2 cohorts (Canaries pattern)', case=view,
                         actual_q12=a[-1]['headcount'], no_ai_q12=c[-1]['headcount'],
                         true_effect=a[-1]['headcount'] < c[-1]['headcount'],
                         measured_gap=round(o['headcount']['gap'], 4), alert=o['headcount']['alert'],
                         attribution=o['headcount']['attribution'],
                         hiring_gap=round(o['hiring']['gap'], 4), hiring_alert=o['hiring']['alert']))
    return rows


def part_c(threshold=.10):
    records = []
    for condition in P.CONDITIONS:
        for seed in SEEDS:
            donors = P.donor_panel(condition, seed)
            for name, p in PANEL_CASES:
                actual, no_ai = P.treated_paths(p, condition, seed, name)
                hours = [s['hours'] for s in actual]
                est, _ = P.estimates(hours, donors)
                true_gap = 1-actual[-1]['hours']/no_ai[-1]['hours']
                gate = P.task_gate(actual)
                for method, gap in est.items():
                    records.append(dict(condition=condition, seed=seed, case=name, method=method,
                                        true_gap=true_gap, estimate=gap, gate=gate,
                                        positive=true_gap > 1e-9, alert=gate and gap > threshold+1e-12))
    return records


def summarise(records):
    rows = []
    for condition in P.CONDITIONS:
        for method in P.ESTIMATORS:
            sel = [r for r in records if r['condition'] == condition and r['method'] == method]
            pos = [r for r in sel if r['positive']]
            neg = [r for r in sel if not r['positive']]
            adopting_neg = [r for r in neg if r['gate']]
            errors = [r['estimate']-r['true_gap'] for r in sel]
            rows.append(dict(condition=condition, method=method, histories=len(sel),
                             positives=len(pos), negatives=len(neg), adopting_negatives=len(adopting_neg),
                             true_alerts=sum(r['alert'] for r in pos),
                             false_alerts=sum(r['alert'] for r in neg),
                             recall=round(sum(r['alert'] for r in pos)/len(pos), 4) if pos else None,
                             false_alarm_rate_adopting=round(sum(r['alert'] for r in adopting_neg)/len(adopting_neg), 4)
                             if adopting_neg else None,
                             mean_error=round(sum(errors)/len(errors), 4),
                             rmse=round((sum(e*e for e in errors)/len(errors))**.5, 4)))
    return rows


def write_csv(path, rows):
    fields = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='outputs/literature-v05/run-001')
    args = parser.parse_args()
    dest = (ROOT/args.out).resolve()
    if not dest.is_relative_to((ROOT/'outputs/literature-v05').resolve()):
        raise SystemExit('Destination must be within outputs/literature-v05.')
    if dest.exists():
        raise SystemExit('Destination exists; choose another numbered directory.')
    before = hashes(preserved())
    cases = part_a()+part_b()
    records = part_c()
    metrics = summarise(records)
    by_case = []
    for condition in P.CONDITIONS:
        for name, _ in PANEL_CASES:
            for method in P.ESTIMATORS:
                sel = [r for r in records if (r['condition'], r['case'], r['method']) == (condition, name, method)]
                by_case.append(dict(condition=condition, case=name, method=method,
                                    mean_true_gap=round(sum(r['true_gap'] for r in sel)/len(sel), 4),
                                    mean_estimate=round(sum(r['estimate'] for r in sel)/len(sel), 4),
                                    alert_share=round(sum(r['alert'] for r in sel)/len(sel), 4),
                                    positive_share=round(sum(r['positive'] for r in sel)/len(sel), 4)))
    assert before == hashes(preserved()), 'Preserved outputs changed during the run.'
    sources = [ROOT/'work'/n for n in ('employer_model_v03.py', 'employer_measurement_v03.py',
                                      'employer_model_v04.py', 'employer_model_v05.py', 'panel_v05.py',
                                      'run_literature_v05.py', 'test_literature_v05.py')]
    sources += [ROOT/'research/experiment-plan-v05.md', ROOT/'research/reference/spillover_paths_v05.csv']
    manifest = dict(command=f'python -B work/run_literature_v05.py --out {args.out}', date='2026-11-25',
                    defaults=V05_DEFAULTS, panel=dict(adopt=P.ADOPT, quarters=P.QUARTERS, donors=P.DONORS,
                                                      treated_loading=P.TREATED_LOADING,
                                                      donor_loadings=P.DONOR_LOADINGS, sigma=P.SIGMA,
                                                      conditions=P.CONDITIONS, size=100),
                    panel_cases=[n for n, _ in PANEL_CASES], seeds=list(SEEDS), threshold=.10,
                    estimators=P.ESTIMATORS, split='development only; no holdout',
                    borrowed=dict(spillover='Hoces de la Guardia (2026) reimplementation of Korinek et al., '
                                            'commit 2f7b1454d85e5ee88c407725e01b781af23e8706, MIT'),
                    source_hashes=hashes(sources), preserved_output_hashes=before,
                    raw_data='not saved; regenerate deterministically from this manifest',
                    repository='https://github.com/petesherratt-collab/Wage-Towers')
    dest.mkdir(parents=True)
    (dest/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    write_csv(dest/'cases.csv', cases)
    write_csv(dest/'metrics.csv', metrics)
    write_csv(dest/'panel_by_case.csv', by_case)
    print(f'{len(cases)} deterministic rows, {len(records)} panel estimates, {len(metrics)} metric rows')


if __name__ == '__main__':
    main()
