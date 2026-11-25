"""v0.4 publication layer: v0.3 publication plus reporting error on paid hours.

Does not import the economic model or truth. The indicator (assess) and
evaluator (evaluate) are re-exported unchanged from v0.3: no rule is retuned.
"""
import random

from employer_measurement_v03 import OUTCOMES, assess, evaluate, observe


def observe_noisy(actual, comparator, specification, sigma_hours=0, seed=0, label='case'):
    """Immediate publication; published paid hours carry multiplicative error.

    Headcount, hiring and layoffs are published exactly. Error draws are
    independent per record and organisation, truncated at 3 sigma.
    """
    records = observe(actual, comparator, specification, 'immediate')
    if sigma_hours == 0:
        return records
    rng = random.Random(f'v04-report-{seed}-{label}')

    def draw():
        while True:
            e = rng.gauss(0, sigma_hours)
            if abs(e) <= 3*sigma_hours:
                return 1+e

    for record in records:
        if record['kind'] == 'workforce':
            for side in ('actual', 'comparator'):
                record['value'][side]['hours'] *= draw()
    return records


__all__ = ['OUTCOMES', 'assess', 'evaluate', 'observe_noisy']
