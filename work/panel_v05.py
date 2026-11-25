"""v0.5 donor panel and comparison estimators. Synthetic; no calibration.

Estimators see only published paid hours and task evidence, never the no-AI
path, loadings, condition names or case names. The synthetic control here is a
simplified, transparent stand-in for synthetic difference-in-differences
(Arkhangelsky et al.; used by the Yale Budget Lab): unit weights on demeaned
pre-period outcomes, no time weights, no inference. It is not the synthdid
package and results must not be described as reproducing Yale's analysis.
"""
import csv
import math
import random
from pathlib import Path

from employer_model_v05 import simulate

ROOT = Path(__file__).resolve().parents[1]
ADOPT, QUARTERS, DONORS = 9, 21, 20
TREATED_LOADING = .5
DONOR_LOADINGS = [.25+1.5*j/(DONORS-1) for j in range(DONORS)]
SIGMA = .03
CONDITIONS = ('flat', 'boom', 'bust', 'spillover')


def spillover_path():
    """Extreme scenario, 2027-2030 window, from research/reference (borrowed)."""
    with (ROOT/'research/reference/spillover_paths_v05.csv').open(encoding='utf-8') as f:
        ratios = {int(r['post_quarter']): float(r['unexposed_employment_ratio'])
                  for r in csv.DictReader(f) if r['scenario'] == 'extreme' and r['window'] == '2027-2030'}
    return [ratios[t-(ADOPT-1)] if t >= ADOPT-1 else 1.0 for t in range(QUARTERS)]


def cycle(condition):
    base = [.06*math.sin(2*math.pi*t/8) for t in range(QUARTERS)]
    ramp = [max(0, t-(ADOPT-1))/(QUARTERS-ADOPT) for t in range(QUARTERS)]
    sign = {'boom': .30, 'bust': -.30}.get(condition, 0)
    return [b+sign*r for b, r in zip(base, ramp)]


def noise(seed, label):
    rng = random.Random(f'v05-panel-{seed}-{label}')
    out = [1.0]
    while len(out) < QUARTERS:
        e = rng.gauss(0, SIGMA)
        if abs(e) <= 3*SIGMA:
            out.append(1+e)
    return out


def demand(condition, loading, seed, label, donor):
    c, eps = cycle(condition), noise(seed, label)
    spill = spillover_path() if condition == 'spillover' and donor else [1.0]*QUARTERS
    return [(1+loading*ct)*s*e for ct, s, e in zip(c, spill, eps)]


def donor_panel(condition, seed, size=100):
    return [[s['hours'] for s in simulate({'ai': False, 'size': size, 'pre_review': True}, False,
                                          demand(condition, b, seed, f'{condition}-donor-{j}', True),
                                          ADOPT, QUARTERS)]
            for j, b in enumerate(DONOR_LOADINGS)]


def treated_paths(parameters, condition, seed, case, size=100):
    d = demand(condition, TREATED_LOADING, seed, f'{condition}-treated-{case}', False)
    p = {**parameters, 'size': size, 'pre_review': True}
    return simulate(p, True, d, ADOPT, QUARTERS), simulate(p, False, d, ADOPT, QUARTERS)


# --------------------------- estimators -----------------------------------
def _log(xs):
    return [math.log(x) for x in xs]


def _change_from_mean(series):
    logs = _log(series)
    return logs[-1]-sum(logs[:ADOPT])/ADOPT


def _change_from_base(series):
    return math.log(series[-1])-math.log(series[ADOPT-1])


def _gap(treated_change, control_change):
    return 1-math.exp(treated_change-control_change)


def _demeaned_pre(series):
    logs = _log(series[:ADOPT])
    m = sum(logs)/len(logs)
    return [x-m for x in logs]


def project_simplex(v):
    """Euclidean projection onto {w >= 0, sum w = 1} (Duchi et al. 2008)."""
    u = sorted(v, reverse=True)
    css, rho, theta = 0.0, 0, 0.0
    for i, ui in enumerate(u, 1):
        css += ui
        t = (css-1)/i
        if ui-t > 0:
            rho, theta = i, t
    return [max(0.0, x-theta) for x in v]


def synthetic_weights(treated, donors, iterations=3000):
    y = _demeaned_pre(treated)
    X = [_demeaned_pre(d) for d in donors]
    n = len(X)
    lipschitz = 2*sum(v*v for d in X for v in d) or 1.0
    w = [1/n]*n
    for _ in range(iterations):
        fit = [sum(w[j]*X[j][t] for j in range(n)) for t in range(len(y))]
        resid = [f-yt for f, yt in zip(fit, y)]
        grad = [2*sum(resid[t]*X[j][t] for t in range(len(y))) for j in range(n)]
        w = project_simplex([wj-gj/lipschitz for wj, gj in zip(w, grad)])
    return w


def estimates(treated, donors):
    """All four paid-hours gap estimates at the final quarter (fraction lost)."""
    median = donors[len(donors)//2]  # loading closest to 1.0 by construction
    y = _demeaned_pre(treated)
    rmse = [sum((a-b)**2 for a, b in zip(y, _demeaned_pre(d))) for d in donors]
    matched = donors[rmse.index(min(rmse))]
    did_control = sum(_change_from_mean(d) for d in donors)/len(donors)
    w = synthetic_weights(treated, donors)
    sc_control = sum(wj*_change_from_mean(d) for wj, d in zip(w, donors))
    t_mean = _change_from_mean(treated)
    return dict(arbitrary_peer=_gap(_change_from_base(treated), _change_from_base(median)),
                matched_peer=_gap(_change_from_base(treated), _change_from_base(matched)),
                did=_gap(t_mean, did_control),
                synthetic_control=_gap(t_mean, sc_control)), w


ESTIMATORS = ('arbitrary_peer', 'matched_peer', 'did', 'synthetic_control')


def task_gate(path):
    """v0.3 attribution prerequisite: published, verified task-time reduction."""
    return path[-1]['task_minutes'] < path[ADOPT-1]['task_minutes']
