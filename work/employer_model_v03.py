"""Deterministic employer-choice model; no empirical calibration or collection."""
from math import isclose

DEFAULTS = dict(review=1, layoff_cost=15000, hire_cost=500, option_value=0,
                new_value=0, new_hours=2000, pursue=False, attrition_only=False,
                demand=1, rebound=1, external_efficiency=0, ai=True)
CASES = [
    ('no_adoption', dict(ai=False)),
    ('immediate_review', {}),
    ('quarterly_budget_cycle', dict(review=4)),
    ('costly_adjustment', dict(layoff_cost=1000000)),
    ('low_retention_value', dict(option_value=15)),
    ('high_retention_value', dict(option_value=30)),
    ('uneconomic_new_work', dict(new_value=15)),
    ('valuable_new_work', dict(new_value=40)),
    ('new_work_later_automated', dict(new_value=40, pursue=True)),
    ('attrition_no_layoffs', dict(attrition_only=True)),
    ('demand_absorption', dict(rebound=5/3)),
    ('demand_expansion', dict(rebound=2)),
    ('external_demand_slump', dict(demand=.7, option_value=30)),
    ('known_external_efficiency', dict(external_efficiency=.4, blocker='external efficiency programme')),
    ('hidden_external_efficiency', dict(external_efficiency=.4)),
    ('ambiguous_ai', dict(no_comparison=True)),
    ('ambiguous_external', dict(external_efficiency=.4, no_comparison=True)),
]


def environment(parameters, q, intervention):
    p = {**DEFAULTS, **parameters}
    adopted = intervention and p['ai'] and q >= 3
    external = p['external_efficiency'] if q >= 3 else 0
    demand = (p['demand'] if q >= 3 else 1) * (p['rebound'] if adopted else 1)
    efficiency = max(.4 if adopted else 0, external)
    new_automated = adopted and p['pursue'] and q >= 7
    return dict(core_hours=5000*demand*(1-efficiency), core_revenue=250000*demand,
                new_hours=p['new_hours']*(.25 if new_automated else 1) if adopted else 0,
                new_revenue=p['new_hours']*p['new_value'] if adopted else 0,
                ai_cost=5000*demand*efficiency*5 if adopted else 0,
                new_ai_cost=7500 if new_automated else 0,
                demand=demand, task_minutes=6 if adopted else 10)


def production(n, e, p):
    capacity = n*500
    core_used = min(capacity, e['core_hours'])
    core_fraction = core_used/e['core_hours'] if e['core_hours'] else 1
    remaining = capacity-core_used
    # Unprofitable work is not allocated merely to count occupied hours.
    valuable = e['new_revenue'] > e['new_ai_cost']
    new_used = min(remaining, e['new_hours']) if valuable else 0
    new_fraction = new_used/e['new_hours'] if e['new_hours'] else 0
    idle = remaining-new_used
    # Retention benefit applies to released legacy capacity, not unlimited
    # speculative hiring; this boundary is itself a sensitivity assumption.
    option_capacity = min(2000, max(0, 5000-e['core_hours']))
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
    options = range(survivors if p['attrition_only'] else 0, 21) if review else [prior]
    choices = []
    for n in options:
        hires, layoffs = max(0, n-survivors), max(0, survivors-n)
        cost = hires*p['hire_cost']+layoffs*p['layoff_cost']
        score = 4*production(n, e, p)['operating_surplus']-cost
        choices.append((score, -abs(n-prior), -n, n, hires, layoffs, cost))
    return max(choices)


def simulate(parameters, intervention=True):
    p = {**DEFAULTS, **parameters}
    path, prior = [], 10
    for q in range(13):
        e = environment(p, q, intervention)
        departures = int(prior > 0) if q else 0
        survivors = prior-departures
        review = q >= 3 and q % p['review'] == 0
        if q == 0:
            score, n, hires, layoffs, cost = 4*production(10,e,p)['operating_surplus'], 10, 0, 0, 0
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


def paired(parameters):
    actual = simulate(parameters, True)
    no_ai = simulate(parameters, False)
    # Comparator shares demand but misses the organisation-specific hidden shock.
    comparator = simulate({**parameters, 'external_efficiency': 0}, False)
    return actual, no_ai, comparator
