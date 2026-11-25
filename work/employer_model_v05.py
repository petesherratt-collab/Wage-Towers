"""v0.5 employer-choice model: v0.4 generalised for literature-grounded tests.

Additions (all default to v0.4 behaviour):
- `adopt`, `quarters`: adoption quarter and horizon (v0.4: 3 and 13);
- an arbitrary per-quarter demand multiplier path (cycles, shocks, spillovers);
- `ai_efficiency`: share of core human effort removed by AI (v0.4: 0.4);
- `shared_new_work`: the new-work opportunity also exists without AI
  (Acemoglu & Restrepo: new tasks need not depend on automation);
- `pre_review`: staffing reviews also happen before adoption (v0.4: never).
At adopt=3, quarters=13 with v0.4 parameters this reproduces employer_model_v04
exactly (see test_literature_v05.py). Earlier model files are untouched.
"""
from math import isclose

from employer_model_v03 import CASES, DEFAULTS

V05_DEFAULTS = dict(DEFAULTS, size=10, ai_efficiency=.4, shared_new_work=False, pre_review=False)


def environment(p, q, intervention, demand_path, adopt):
    size = p['size']
    adopted = intervention and p['ai'] and q >= adopt
    after = q >= adopt
    external = p['external_efficiency'] if after else 0
    demand = (p['demand'] if after else 1)*(p['rebound'] if adopted else 1)*demand_path[q]
    efficiency = max(p['ai_efficiency'] if adopted else 0, external)
    new_automated = adopted and p['pursue'] and q >= adopt+4
    new_open = adopted or (p['shared_new_work'] and after)
    new_hours = p['new_hours']*size/10
    return dict(core_hours=500*size*demand*(1-efficiency), core_revenue=25000*size*demand,
                new_hours=new_hours*(.25 if new_automated else 1) if new_open else 0,
                new_revenue=new_hours*p['new_value'] if new_open else 0,
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


def simulate(parameters, intervention=True, demand_path=None, adopt=3, quarters=13):
    p = {**V05_DEFAULTS, **parameters}
    demand_path = demand_path or [1.0]*quarters
    assert len(demand_path) >= quarters
    size = p['size']
    path, prior = [], size
    for q in range(quarters):
        e = environment(p, q, intervention, demand_path, adopt)
        departures = min(prior, size//10) if q else 0
        survivors = prior-departures
        # v0.3/v0.4 never review staffing before adoption; pre_review lets demand
        # changes move staffing in the pre-period so comparison methods can learn.
        review = (q >= adopt or (p['pre_review'] and q >= 1)) and q % p['review'] == 0
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


def potential_paths(parameters, demand_path=None, adopt=3, quarters=13):
    """With-AI and no-AI paths of one organisation under one shared demand path."""
    return (simulate(parameters, True, demand_path, adopt, quarters),
            simulate(parameters, False, demand_path, adopt, quarters))


# ---------------------------------------------------------------------------
# Two-cohort accounting model (Canaries pattern). Requirements-driven staffing,
# NOT an employer optimisation: it demonstrates what aggregate measures can hide.
# ---------------------------------------------------------------------------
COHORT_DEFAULTS = dict(junior=10, experienced=10, junior_saving=.5, experienced_expansion=.5,
                       junior_quit=1, experienced_quit=1, adopt=3, quarters=13)


def cohort_simulate(parameters=None, intervention=True):
    """Internal ladder: each quarter one junior and one experienced worker quit;
    experienced vacancies are filled by promoting juniors (then by outside
    experienced hires if no juniors remain); junior vacancies are filled by
    entry-level hiring. AI (from `adopt`) cuts junior-task requirements and
    expands experienced-supervised work. No layoffs. Without AI the stock is
    stationary at 10 + 10 with two junior hires a quarter.
    """
    p = {**COHORT_DEFAULTS, **(parameters or {})}
    adopted = lambda q: intervention and q >= p['adopt']
    junior, experienced = p['junior'], p['experienced']
    path = []
    for q in range(p['quarters']):
        promoted = hires_j = hires_e = 0
        if q:
            junior -= min(p['junior_quit'], junior)
            experienced -= min(p['experienced_quit'], experienced)
            need_e = round(p['experienced']*(1+p['experienced_expansion'])) if adopted(q) else p['experienced']
            need_j = round(p['junior']*(1-p['junior_saving'])) if adopted(q) else p['junior']
            if experienced < need_e:
                promoted = min(junior, need_e-experienced)
                junior -= promoted
                experienced += promoted
                hires_e = need_e-experienced
                experienced += hires_e
            if junior < need_j:
                hires_j = need_j-junior
                junior += hires_j
        path.append(dict(q=q, junior=junior, experienced=experienced, headcount=junior+experienced,
                         junior_hires=hires_j, experienced_hires=hires_e, promotions=promoted,
                         task_minutes=6 if adopted(q) else 10))
    return path
