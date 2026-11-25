"""Run the v0.4 noise and firm-size grid into a new output directory."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from employer_model_v04 import CASES, V04_DEFAULTS, paired
from employer_measurement_v04 import OUTCOMES, assess, evaluate, observe_noisy

ROOT = Path(__file__).resolve().parents[1]
SIZES = (10, 100)
SIGMA_DEMAND = (0, .03, .06)
SIGMA_HOURS = (0, .03)
THRESHOLDS = (.05, .10, .20)
SEEDS = range(40)


def hashes(paths):
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if p.is_file()}


def preserved_paths():
    paths = []
    for d in ('outputs/synthetic-indicator', 'outputs/longitudinal-v02', 'outputs/employer-v03'):
        paths += [p for p in (ROOT/d).rglob('*') if p.is_file()]
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='outputs/noise-v04/run-001')
    args = parser.parse_args()
    dest = (ROOT/args.out).resolve()
    if not dest.is_relative_to((ROOT/'outputs/noise-v04').resolve()):
        raise SystemExit('Destination must be within outputs/noise-v04.')
    if dest.exists():
        raise SystemExit('Destination exists; choose another numbered directory.')
    before = hashes(preserved_paths())

    histories = {}  # (case, size, sigma_d, seed) -> (actual, no_ai, comparator)
    rows, cells = [], []
    for size in SIZES:
        for sd in SIGMA_DEMAND:
            for sm in SIGMA_HOURS:
                seeds = [0] if sd == 0 and sm == 0 else list(SEEDS)
                for threshold in THRESHOLDS:
                    runs = []
                    for seed in seeds:
                        sim_seed = 0 if sd == 0 else seed
                        for name, p in CASES:
                            key = (name, size, sd, sim_seed)
                            if key not in histories:
                                histories[key] = paired(p, size=size, sigma_demand=sd,
                                                        seed=sim_seed, case=name)
                            actual, no_ai, comparator = histories[key]
                            records = observe_noisy(actual, comparator, p, sm, seed=seed,
                                                    label=f'{name}-{size}')
                            runs.append(dict(actual=actual, no_ai=no_ai, flow_rule='cumulative',
                                             assessments=[assess(records, q, threshold) for q in range(13)]))
                    metrics = evaluate(runs)
                    cells.append(dict(size=size, sigma_demand=sd, sigma_hours=sm,
                                      threshold=threshold, seeds=len(seeds)))
                    for outcome in OUTCOMES:
                        m = metrics[outcome]
                        rows.append(dict(size=size, sigma_demand=sd, sigma_hours=sm, threshold=threshold,
                                         seeds=len(seeds), outcome=outcome, histories=m['n'],
                                         positives=m['positives'], negatives=m['negatives'],
                                         true_alerts=m['true_alerts'], false_alerts=m['false_alerts'],
                                         positive_abstentions=m['positive_abstentions'],
                                         non_alert_misses=m['non_alert_misses'],
                                         recall=m['recall'], false_alarm_rate=m['false_alarm_rate'],
                                         attribution_coverage=m['attribution_coverage']))
    after = hashes(preserved_paths())
    assert before == after, 'Preserved outputs changed during the run.'

    sources = [ROOT/'work'/n for n in ('employer_model_v03.py', 'employer_measurement_v03.py',
                                      'employer_model_v04.py', 'employer_measurement_v04.py',
                                      'run_noise_v04.py', 'test_noise_v04.py')]
    sources.append(ROOT/'research/experiment-plan-v04.md')
    manifest = dict(command=f'python -B work/run_noise_v04.py --out {args.out}',
                    date='2026-11-25', cases=[n for n, _ in CASES], defaults=V04_DEFAULTS,
                    sizes=SIZES, sigma_demand=SIGMA_DEMAND, sigma_hours=SIGMA_HOURS,
                    thresholds=THRESHOLDS, seeds=list(SEEDS),
                    seed_rule='one seed when both sigmas are zero; otherwise seeds 0-39. '
                              'Simulation seed is 0 when sigma_demand is zero.',
                    publication='immediate', flow_rule='cumulative', evaluated_at='q12',
                    split='development only; no holdout', cells=cells,
                    source_hashes=hashes(sources), preserved_output_hashes=before,
                    raw_data='not saved; regenerate deterministically from this manifest',
                    repository='https://github.com/petesherratt-collab/Wage-Towers')
    dest.mkdir(parents=True)
    (dest/'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    with (dest/'metrics.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'{len(cells)} cells, {len(rows)} metric rows, {len(histories)} simulated histories')


if __name__ == '__main__':
    main()
