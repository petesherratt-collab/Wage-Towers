"""Decompose v0.4 paid-hours false alerts into the planted confounder vs noise.

Read-only analysis; prints a Markdown table and writes nothing. Uses the same
seeds, labels and rules as run_noise_v04.py.
"""
from collections import Counter

from employer_model_v04 import CASES, paired
from employer_measurement_v03 import causal_truth
from employer_measurement_v04 import assess, observe_noisy

PLANTED = 'hidden_external_efficiency'
SETTINGS = [(.03, 0, .10), (.06, 0, .10), (.06, 0, .05), (0, .03, .05)]


def main():
    print('| Size | Demand σ | Hours σ | Cutoff | Planted false alerts | Noise-driven false alerts / other nulls | Cases involved |')
    print('|---|---|---|---|---|---|---|')
    for size in (10, 100):
        for sd, sm, threshold in SETTINGS:
            alerts, negatives = Counter(), Counter()
            for seed in range(40):
                for name, p in CASES:
                    a, n, c = paired(p, size=size, sigma_demand=sd, seed=0 if sd == 0 else seed, case=name)
                    records = observe_noisy(a, c, p, sm, seed=seed, label=f'{name}-{size}')
                    o = assess(records, 12, threshold)['outcomes']['hours']
                    if not causal_truth(a, n, 'hours', 3, 12):
                        negatives[name] += 1
                        alerts[name] += o['alert']
            planted = alerts.pop(PLANTED, 0)
            others = sum(negatives.values())-negatives[PLANTED]
            involved = ', '.join(f'{k} {v}' for k, v in sorted(alerts.items()) if v) or 'none'
            print(f'| {size} | {sd} | {sm} | {threshold:.0%} | {planted} | {sum(alerts.values())} / {others} | {involved} |')


if __name__ == '__main__':
    main()
