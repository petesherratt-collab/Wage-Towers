"""v0.4 employer-choice model: v0.3 plus organisation size and demand shocks.

No empirical calibration or collection. At size=10 with no shocks this must
reproduce employer_model_v03 exactly (see test_noise_v04.py). The v0.3 file
is deliberately left untouched because its hash is part of preserved run-001.
"""
from math import isclose
import random

from employer_model_v03 import CASES, DEFAULTS  # same cases and parameters

V04_DEFAULTS = dict(DEFAULTS, size=10)
QUARTERS = 13


def shock_series(sigma, seed, label, quarters=QUARTERS):
    """Multiplicative demand shocks 1+e, e ~ Normal(0, sigma) truncated at 3 sigma.

    q0 is always 1 (the common starting point). Deterministic in (seed, label):
    random.Random seeded with a str is stable across runs and PYTHONHASHSEED.
    """
    if sigma == 0:
        return [1.0]*quarters
    rng = random.Random(f'v04-demand-{seed}-{label}')
    series = [1.0]
    while len(series) < quarters:
        e = rng.gauss(0, sigma)
        if abs(e) <= 3*sigma:  # resample rather than clip: true truncation
            series.append(1+e)
    return series


def environment(p, q, intervention, shock):
    size = p['size']
    adopted = intervention and p['ai'] and q >= 3
    external = p['external_efficiency'] if q >= 3 else 0
    demand = (p['demand'] if q >= 3 else 1)*(p['rebound'] if adopted else 1)*shock[q]
    efficiency = max(.4 if adopted else 0, external)
    new_automated = adopted and p['pursue'] and q >= 7
    new_hours = p['new_hours']*size/10
    return dict(core_hours=500*size*demand*(1-efficiency), core_revenue=25000*size*demand,
                new_hours=new_hours*(.25 if new_automated else 1) if adopted else 0,
                new_revenue=new_hours*p['new_value'] if adopted else 0,
                ai_cost=500*size*demand*efficiency*5 if adopted else 0,
                new_ai_cost=750*size if new_automated else 0,
                demand=demand, task_minutes=6 if adopted else 10)


def production(n, e, p):
    size = p['size']
    capacity = n*500
    core_used = min(capacity, e['core_hours'])
    core_fraction = core_used/e['core_hours'] if e['core_hours'] else 1
    remaining = capacity-core_used
    valuable = e['new_revenue'] > e['new_ai_cost']
    new_used = min(remaining, e['new_hours']) if valuable else 0
    new_fraction = new_used/e['new_hours'] if e['new_hours'] else 0
    idle = remaining-new_used
    option_capacity = min(200*size, max(0, 500*size-e['core_hours']))
    option = min(option_capacity, idle)*p['option_value']
    revenue = e['core_revenue']*core_fraction+e['new_revenue']*new_fraction
    ai_cost = e['ai_cost']*core_fraction+e['new_ai_cost']*new_fraction
    payroll = capacity*25
    return dict(hours=capacity, used_hours=core_used+new_used, idle_hours=idle,
                core_used=core_used, new_used=new_used, option_payoff=option,
                revenue=revenue, ai_cost=ai_cost, payroll=payroll,
                operating_surplus=revenue+option-payroll-ai_cost,
                output=100*e['demand']*core_fraction)


def choose(prior, survivors, e, p, review):
    top = 2*p['size']
    options = range(survivors if p['attrition_only'] else 0, top+1) if review else [prior]
    choices = []
    for n in options:
        hires, layoffs = max(0, n-survivors), max(0, survivors-n)
        cost = hires*p['hire_cost']+layoffs*p['layoff_cost']
        score = 4*production(n, e, p)['operating_surplus']-cost
        choices.append((score, -abs(n-prior), -n, n, hires, layoffs, cost))
    return max(choices)


def simulate(parameters, intervention=True, shock=None):
    p = {**V04_DEFAULTS, **parameters}
    shock = shock or [1.0]*QUARTERS
    size = p['size']
    path, prior = [], size
    for q in range(QUARTERS):
        e = environment(p, q, intervention, shock)
        departures = min(prior, size//10) if q else 0
        survivors = prior-departures
        review = q >= 3 and q % p['review'] == 0
        if q == 0:
            score, n, hires, layoffs, cost = 4*production(size, e, p)['operating_surplus'], size, 0, 0, 0
        else:
            score, _, _, n, hires, layoffs, cost = choose(prior, survivors, e, p, review)
        quantities = production(n, e, p)
        path.append(dict(q=q, headcount=n, hiring=hires, layoffs=layoffs,
                         natural_departures=departures, pay=25, task_minutes=e['task_minutes'],
                         review=review, decision_score=score, adjustment_cost=cost,
                         realised_surplus=quantities['operating_surplus']-cost, **quantities))
        assert n == prior+hires-departures-layoffs
        assert isclose(quantities['hours'], quantities['used_hours']+quantities['idle_hours'])
        prior = n
    return path


def paired(parameters, size=10, sigma_demand=0, seed=0, case='case'):
    """Actual and no-AI paths share the treated shock series; comparator has its own."""
    p = {**parameters, 'size': size}
    treated = shock_series(sigma_demand, seed, f'{case}-treated-{size}')
    peer = shock_series(sigma_demand, seed, f'{case}-comparator-{size}')
    actual = simulate(p, True, treated)
    no_ai = simulate(p, False, treated)
    comparator = simulate({**p, 'external_efficiency': 0}, False, peer)
    return actual, no_ai, comparator


__all__ = ['CASES', 'V04_DEFAULTS', 'shock_series', 'environment', 'production',
           'choose', 'simulate', 'paired']
