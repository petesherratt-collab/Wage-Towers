# v0.5 findings: literature-grounded cases and borrowed comparison methods

25 November 2026. Synthetic development experiment; no empirical validation, holdout or live collection. Pre-execution plan, with development notes recorded before the grid ran: `experiment-plan-v05.md`. Results: `outputs/literature-v05/run-001/` (`cases.csv`, `metrics.csv`, `panel_by_case.csv`, `manifest.json`).

This carries out the four steps proposed after the related-work review. A previous attempt in another session was not saved anywhere this session could reach; nothing from it is reused.

## Headline results

1. **Whether new work would exist without AI decides the verdict, and the treated firm's own data cannot tell you.** If the opportunity is shared, the v0.3 "valuable new work" case becomes 10 workers against a no-AI 14 (29% fewer) with no fall from baseline. The v0.3 rule alerts only if the comparator also took up the opportunity; against a comparator without it, the measured gap is 0.
2. **Better comparison methods do not fix a missing counterfactual opportunity.** In the donor panel, every method (single peer, difference-in-differences, synthetic control) estimates about 0% for that 29% effect, because no donor has the opportunity.
3. **Synthetic control clearly beats plain difference-in-differences when the treated firm is less cyclical than its peers** (Yale's concern). In a boom it cuts false alerts among firms that adopted AI harmlessly from 63% to 13%, and cuts average bias from +6.7 to +0.3 percentage points. In a bust it halves the bias (−28 to −13 points). It does not remove the bust bias entirely with nine noisy pre-period quarters.
4. **No method handles comparator contamination.** With the borrowed macro spillover (unexposed employment +12.6% over three years), all four methods are biased by about +6.5 points and false-alert in 60–78% of harmless adopters. Reweighting cannot help when every donor is contaminated.
5. **Aggregate measures hide composition shifts.** In a two-cohort firm, AI halves junior staff while total headcount is unchanged. The aggregate rule is silent; a junior-cohort rule alerts at 50%.
6. **Small task savings are invisible in small firms and sub-threshold in larger ones.** A 5% saving changes nothing at 10 workers and removes 5 of 100, below the 10% cutoff. This fits the Humlum–Vestergaard pattern of restructured tasks with little measured change, without settling which explanation applies there.

## What was borrowed, and how far

| Source | Used as | Not claimed |
|---|---|---|
| Acemoglu & Restrepo (2019) | Idea that new tasks need not depend on automation → `shared_new_work` | Not their model or their technical "displacement effect" |
| Humlum & Vestergaard (2025) | Pattern: task change, little measured change in hours → 5% saving case | Not a calibration to Danish data |
| Brynjolfsson, Chandar & Chen, *Canaries* (Aug 2026) | Pattern: entry-level channel hidden in aggregates → cohort case | Not an age model; requirements-driven staffing, not optimisation |
| Yale Budget Lab (2026) | Observation that exposed occupations are less cyclical; their use of synthetic difference-in-differences | **Not** a reproduction: unit weights on demeaned pre-period hours, no time weights, no inference, not the `synthdid` package. I could not confirm a public code link for their analysis |
| Hoces de la Guardia (2026), reimplementation of Korinek et al. | Exported unexposed-employment paths only (`research/reference/`) | Code not imported or run inside Wage Towers |

### Assessment of the public macro-scenarios repository

`fhoces/opa-ai-macro-econ-scenarios`, inspected at commit `2f7b145` (tag v1.0 plus later slides). MIT licence; standard-library Python; a monthly two-sector model to 2030 written from the paper's equations; its 129 tests passed here in 5 seconds; a self-audit against BITSS Open Policy Analysis guidelines is included. It reports reproducing the paper's Tables 3, 5 and 6 within tolerance.

Recommendation: **use it as an external scenario source, not as code to import.** It models economy-wide occupational groups and gaps against a no-AI path, which is the right estimand philosophy, but it has no firms, comparators or observation process, so it cannot replace any part of Wage Towers. Its most useful output for us is the spillover into unexposed employment, which directly challenges the comparator assumption. Pin the commit and cite it, as `research/reference/README.md` does. Its repository also contains a `.claude/settings.json` hook that runs a local script after edits; that only matters if someone opens the repository in Claude Code, and nothing here uses it.

## Part A: new work with and without AI (step 1)

v0.3 rule, immediate publication, 10% cutoff, size 10, q12.

| Case | Opportunity exists without AI? | Comparator | Actual / no-AI staff | True effect | Measured gap | Alert |
|---|---|---|---|---|---|---|
| valuable_new_work | No (v0.3 assumption) | either | 10 / 10 | none | 0% | no |
| valuable_new_work | **Yes** | peer without it | 10 / 14 | **−29%** | 0% | **no (miss)** |
| valuable_new_work | **Yes** | peer with it | 10 / 14 | −29% | 28.6% | yes |
| new_work_later_automated | Yes | peer with it | 7 / 14 | −50% | 50% | yes |
| uneconomic_new_work | either | either | 6 / 10 | −40% | 40% | yes |

Predictions A1 and A2 confirmed. Uneconomic new work is unaffected because the no-AI firm would not take it up either. Consequence: every "AI-enabled new work absorbs released hours" result in v0.3 is conditional on the opportunity being AI-specific. Evidence about whether competitors without AI expanded into the same work is a required observation, not an optional extra.

## Part B: contrasting cases from empirical studies (step 2)

| Case | Actual / no-AI | Measured gap | Alert |
|---|---|---|---|
| 5% saving, 10 workers | 10 / 10 | 0% | no (true null) |
| 5% saving, 100 workers | 95 / 100 | 5% | no (real effect below cutoff) |
| Cohorts, aggregate headcount | 20 / 20 | 0% | no (true null in aggregate) |
| Cohorts, junior headcount | 5 / 10 | 50% | yes |
| Cohorts, junior hiring | 2 a quarter either way | 0% | no |

B1 confirmed. B2 confirmed for headcount, and the junior-hiring part failed as flagged in the plan before running: under an internal promotion ladder, AI pulls juniors up into expanded experienced roles, so entry hiring holds steady while the junior stock halves. A hiring-flow indicator can miss an entry-level squeeze that a cohort-stock indicator sees. Real firms also hire experienced staff externally, so this is one mechanism, not a general result.

## Part C: comparison methods on a donor panel (step 3)

One treated firm and 20 donors, all 100 workers, 21 quarters, adoption at q9, 30 seeds × 8 cases × 4 conditions. The treated firm's cyclical loading is 0.5; donors span 0.25–1.75. Alerts need a gap above 10% plus published task replacement (the v0.3 gate). "Harmless adopters" are histories where AI was adopted but the true effect is zero or favourable; they are where false alerts matter (v0.4).

| Condition | Method | False alerts, harmless adopters | Recall, all positives | Mean error | RMSE |
|---|---|---|---|---|---|
| Flat | arbitrary peer | 1 / 57 | 42% | −3.1 pts | 0.111 |
| Flat | matched peer | 0 / 57 | 41% | −3.5 | 0.115 |
| Flat | DiD | 0 / 57 | 40% | −3.0 | 0.104 |
| Flat | synthetic control | 0 / 57 | 41% | −3.2 | 0.105 |
| Boom | arbitrary peer | 17 / 30 (57%) | 94% | +6.5 | 0.111 |
| Boom | matched peer | 3 / 30 (10%) | 67% | −1.1 | 0.109 |
| Boom | DiD | 19 / 30 (63%) | 100% | +6.7 | 0.106 |
| Boom | synthetic control | 4 / 30 (13%) | 72% | **+0.3** | **0.093** |
| Bust | arbitrary peer | 0 / 60 | 40% | −29.3 | 0.332 |
| Bust | matched peer | 1 / 60 | 42% | −11.7 | 0.211 |
| Bust | DiD | 0 / 60 | 40% | −28.0 | 0.315 |
| Bust | synthetic control | 0 / 60 | 40% | −13.3 | **0.195** |
| Spillover | arbitrary peer | 35 / 55 (64%) | 83% | +6.8 | 0.125 |
| Spillover | matched peer | 33 / 55 (60%) | 86% | +6.3 | 0.117 |
| Spillover | DiD | 43 / 55 (78%) | 92% | +6.4 | 0.115 |
| Spillover | synthetic control | 36 / 55 (65%) | 91% | +6.4 | 0.115 |

How to read recall: "all positives" counts any strictly adverse true effect, as in v0.3. Most misses in the flat condition are by design (true effects of 2–5%, below the 10% cutoff) or the shared-new-work case, which every method estimates at about 0% against a true 29%. Every method catches the two large-loss cases (≈40%) in every seed under flat conditions. In a boom, DiD's 100% recall is inflated by its upward bias: it also flags most harmless adopters.

Prediction check: C1 confirmed (DiD and arbitrary peer false-alert heavily in a boom; matched peer and synthetic control far less). C2 partly: bias mirrors as predicted, but recall is equally low for all methods, so the bust advantage shows only in error, not in alerts at this cutoff. C3 confirmed, with a bias of about +6.5 points rather than the 11% predicted, because staffing responds less than one-for-one to donor demand. C4 confirmed: little difference without a cycle.

A single best-fitting peer does nearly as well as synthetic control on false alerts but is noisier (higher RMSE in boom and bust). Synthetic control has the lowest RMSE in every cyclical condition.

## Judgement

- **Retire the arbitrary single-comparator rule** (v0.3) as the default in favour of a donor-pool method. Synthetic control is the best of the four here; DiD with equal weights inherits any cyclical mismatch between exposed and unexposed firms.
- **Add two required observations:** whether comparators had access to the same new-work opportunity, and whether comparators are themselves receiving displaced workers or AI-driven demand (contamination). Neither can be fixed by estimator choice.
- **Add a cohort indicator** (entry-level stock) alongside aggregate hours; do not rely on hiring flows alone for the entry-level channel.
- The weakening criterion in the plan was not met: synthetic control clearly beat DiD under boom and bust. That supports borrowing the method, within this model.

## Limitations

Loadings, cycle sizes, noise, panel size and the nine-quarter pre-period are illustrative, not calibrated. The cycle is large (±30% demand at its peak, scaled by loading) to make the bias visible. The synthetic control has no inference and no time weights. Pre-period staffing reviews were added (`pre_review`) because the inherited model froze staffing before adoption; this is recorded in the plan. The cohort model is accounting, not optimisation. The spillover path is an economy-wide occupational aggregate applied to every donor, an extreme case. Pay is still fixed: wage erosion remains untested. All cases and rules were visible during development; there is no holdout.

## Next experiments

1. **Time weights and inference:** add placebo-in-time and placebo-across-donor tests so the synthetic control reports uncertainty instead of a bare point estimate; check whether that repairs bust-period recall.
2. **Contamination diagnostics:** test whether pre-period donor fit or donor exposure measures can flag a contaminated pool before attribution.
3. **Opportunity evidence:** represent observable expansion by non-adopting competitors as evidence for or against a shared new-work opportunity.
4. **Wage setting:** still the largest untested channel.

## Reproduction

```text
python work/restore_outputs.py
python -B work/test_literature_v05.py
python -B work/run_literature_v05.py --out outputs/literature-v05/run-002
```

About two minutes on one core. The runner refuses existing destinations and checks that v0.1–v0.4 outputs are unchanged.
