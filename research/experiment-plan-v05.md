# v0.5 pre-execution plan: literature-grounded cases and borrowed comparison methods

25 November 2026. Development cases only; no holdout or empirical calibration. Written before any v0.5 code was run. Picks up the four-step plan from the related-work review; an earlier attempt at this work in a separate session was not saved and is not reused.

## Sources and how each is used

| Source | What is borrowed | Status here |
|---|---|---|
| Acemoglu & Restrepo (2019), *Automation and New Tasks* | Displacement vs reinstatement through new tasks; new tasks need not depend on automation | Concept only. Tested by letting new work exist in the no-AI world too |
| Humlum & Vestergaard (2025) | Task restructuring with little measured change in earnings or hours; small reported time savings | Pattern only. A small-saving case (5% of core effort) |
| Brynjolfsson, Chandar & Chen, *Canaries* (Aug 2026) | Separate entry-level / younger-worker channel; aggregate can hide it | Pattern only. A two-cohort accounting case |
| Yale Budget Lab (2026) | Exposed occupations are less cyclical than unexposed ones; synthetic difference-in-differences to handle that | Method idea. A **simplified** synthetic control with a level shift is implemented; it is not the `synthdid` package and has no time weights or inference |
| Hoces de la Guardia (2026) reimplementation of Korinek et al. | Displaced workers raise employment in unexposed occupations | Exported paths only: `research/reference/spillover_paths_v05.csv` |

## Part A: does new work exist without AI? (Step 1)

Question: v0.3 assumed AI-enabled new work, so "valuable new work" keeps 10 workers and counts as no displacement. If the same opportunity would exist without AI, the no-AI firm grows instead.

Change: `shared_new_work=True` makes the new-work opportunity (2,000 original human hours, same value) available from adoption in the no-AI path as well.

Predictions:
- A1. With shared opportunities, `valuable_new_work` becomes a true positive: actual 10 workers vs no-AI 14 (29% fewer), with no fall from baseline.
- A2. A comparator that also gets the opportunity shows the gap (it grows to 14) and the v0.3 rule alerts. A comparator that does not shows no gap and the rule misses it. The result therefore depends entirely on comparator choice, not on the treated firm's data.

## Part B: contrasting cases from empirical studies (Step 2)

- B1, Humlum–Vestergaard pattern: AI saves 5% of core effort. Prediction: at size 10 no staffing change (whole-worker rounding absorbs it, consistent with v0.4); at size 100 about 5 fewer workers, a real effect below the 10% materiality cutoff, so a non-alert miss by design.
- B2, Canaries pattern: a separate two-cohort accounting model (junior and experienced). AI halves junior task hours; AI-enabled expansion raises experienced-staff requirements. Staffing follows requirements mechanically (not optimised). Prediction: total headcount unchanged vs no-AI, so the aggregate indicator does not alert; a junior-cohort indicator alerts; junior hiring is suppressed. If cohort data are unpublished, the aggregate rule silently misses rather than abstaining.
- B3, Yale cyclicality pattern: covered by Part C conditions.

## Part C: comparison methods on a donor panel (Step 3)

Panel: one treated organisation (size 100) and 20 donor organisations, 21 quarters, adoption at q9 (nine pre-period quarters). Each organisation runs the v0.4 employer rule with its own demand path:

`demand_t = (1 + β · cycle_t) × spillover_t × (1 + ε_t)`, ε ~ Normal(0, 0.03) truncated at ±3σ.

- Treated loading β = 0.5 (less cyclical, following Yale's observation); donor loadings evenly spaced 0.25–1.75 (mean 1.0).
- Pre-period cycle: 0.06·sin(2πt/8), so loadings are in principle identifiable from pre-period data.
- Post-period conditions: **flat** (cycle continues at the same amplitude); **boom** (cycle ramps linearly to +0.30 at q20); **bust** (ramps to −0.30); **spillover** (flat cycle, donors only multiplied by the extreme 2027–2030 path, +12.6% by q20).
- With-AI and no-AI treated paths share their shock series; truth is the q20 paid-hours gap against the no-AI path.

Cases (all size 100): `no_adoption`, `valuable_new_work`, `demand_absorption`, `high_retention_value` (adopting nulls), `immediate_review`, `attrition_no_layoffs`, `shared_new_work` (positives), and `small_saving` (true effect ~5%, below cutoff).

Estimators of the paid-hours gap at q20 (all expressed as `1 − exp(treated log change − control log change)`):
1. **Arbitrary peer** (v0.3 style): the donor with median loading (β = 1.0), base q8.
2. **Matched peer:** the single donor with the smallest pre-period RMSE in log hours, base q8.
3. **DiD:** treated change from pre-period mean minus the equal-weighted donor mean change.
4. **Synthetic control with level shift:** non-negative donor weights summing to one that minimise pre-period squared error after removing each unit's pre-period mean; the change is then compared as in DiD. Simplified SDID without time weights.

The v0.3 attribution gate is unchanged: alert only if the gap exceeds 10% **and** task replacement is published and there is no recorded blocker. 30 seeds per case × condition.

Predictions:
- C1. **Boom:** arbitrary peer and DiD produce false alerts in adopting nulls (donors average β ≈ 1 against the treated firm's 0.5; expected gap ≈ 1 − 1.15/1.30 ≈ 12%). Matched peer and synthetic control produce far fewer.
- C2. **Bust:** the mirror image, with recall falling for arbitrary peer and DiD.
- C3. **Spillover:** all four estimators are biased upward by about the spillover (~11%); synthetic control cannot fix it because every donor is contaminated. Expect false alerts in adopting nulls for all methods.
- C4. **Flat:** all methods similar; the synthetic control has slightly lower variance than the matched peer.

Weakening results: if synthetic control does not clearly beat DiD under boom or bust, the borrowed method is not worth its complexity at this panel size. If it does, the v0.3 single-comparator rule should be retired in favour of a donor-pool method.

## Development notes (smoke tests, before the grid was generated)

1. **Pre-period reviews.** The inherited employer rule never reviews staffing before adoption, so every panel unit had flat pre-period hours and the synthetic-control weights stayed equal. A `pre_review` option (default off, so v0.4 reproduces) now lets staffing respond to demand from q1 in all panel units. This is a structural departure required for any pre-period comparison method to work at all.
2. **Cohort model simplified** to an internal ladder (promotion fills experienced vacancies; entry hiring fills junior ones) after a tenure-bucket draft promoted every starting junior at q1. Observed before running anything else: under this ladder junior *hiring* does not fall with AI (two a quarter either way); only the junior stock falls. B2's prediction of suppressed junior hiring is therefore expected to fail.
3. One smoke panel suggested the synthetic control learns loadings poorly with nine noisy pre-period quarters (σ = 0.03 against a cycle of 0.06 × loading). Noise, cycle and pre-period length were **not** changed in response; they stay as planned.

## Outputs and limitations

`outputs/literature-v05/run-001/`: `manifest.json`, `metrics.csv`, `cases.csv`. The cohort model is a requirements-driven accounting demonstration, not an employer optimisation. Loadings, cycle amplitudes and donor counts are illustrative. The synthetic control has no inference, so it reports a point estimate against a materiality cutoff, as the v0.3 rule does. Pay remains fixed.
