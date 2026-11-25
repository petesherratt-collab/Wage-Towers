# v0.4 pre-execution plan: noise, imperfect comparators and firm size

25 November 2026. Development cases only; no holdout or empirical calibration. Written before any v0.4 code was run.

Question: do the v0.3 indicator rules still separate AI-caused staffing losses from null histories when (a) the comparator is a different organisation with its own demand fluctuations, (b) published paid hours carry reporting error, and (c) the organisation has 100 rather than 10 workers?

Why: v0.3 is fully deterministic and its comparator is an exact twin apart from deliberately planted flaws. Every v0.3 false alert therefore comes from a designed confounder; none comes from ordinary variation. The 5%, 10% and 20% cutoffs have never been tested against noise. With ten workers, one person is 10% of headcount, so integer granularity and the 10% cutoff coincide.

## Changed assumptions (structural departures from v0.3)

1. **Scale.** A `size` parameter scales initial workers, hours, revenue, new-work hours, option-value cap, AI running costs and natural departures (10% of the initial workforce per quarter, capped at the current stock). Per-person hiring and layoff costs, hourly pay and the 0–2×size staffing range are unchanged in form. At size 10 with no shocks the model must reproduce v0.3 exactly.
2. **Demand shocks.** Each organisation receives independent multiplicative demand shocks from q1: `demand_q = 1 + ε_q`, ε i.i.d. Normal(0, σ_d), truncated at ±3σ_d. The with-AI and no-AI potential paths of the treated organisation share the same shock series, so causal truth remains well defined. The comparator receives an independent series. This is the "imperfect comparator".
3. **Reporting error.** Published paid hours (treated and comparator) are multiplied by `1 + η`, η i.i.d. Normal(0, σ_m), independently per record. Headcount, hires and layoffs are published exactly. Hours and headcount observations are therefore no longer mechanically identical.

The economic employer rule, indicator (`assess`) and evaluator (`evaluate`) are imported unchanged from v0.3. No indicator rule is retuned.

## Grid

- 17 v0.3 structural cases; sizes {10, 100}; σ_d ∈ {0, 0.03, 0.06}; σ_m ∈ {0, 0.03}; cutoffs {5%, 10%, 20%}; immediate publication; cumulative flows; assessments q0–q12, evaluated at q12.
- 40 seeds per noisy cell (seed list 0–39; the shock series is a deterministic function of seed, case, organisation and size). Noise-free cells use one seed only, as extra seeds would repeat identical results.
- Primary comparison: false-alert rate on causal negatives and recall on causal positives, per outcome, by size and noise level.

## Predictions (recorded before running)

P1. Size 10, σ_d = σ_m = 0 reproduces the v0.3 primary table exactly (same positives, alerts, abstentions).
P2. Size 100, σ_d = σ_m = 0 gives the same table as size 10, because every quantity scales linearly. *If true, my earlier suggestion that the q12 hiring decay is "partly a firm-size artefact" is wrong without noise: the shortfall ratio 10/100 equals 1/10.*
P3. With σ_d > 0 the hours false-alert rate on nulls rises above the v0.3 rate (1/8), most at the 5% cutoff and least at 20%.
P4. Reporting error σ_m affects the hours indicator but not headcount, so hours and headcount metrics diverge for the first time.
P5. Under noise, size 100 has a lower false-alert rate than size 10 at the same σ_d, because a 10-worker firm cannot adjust in steps smaller than 10%, so shocks either do nothing or move headcount by a full 10%.

What would weaken the v0.3 candidates: hours false alerts above roughly 20% of nulls at the 10% cutoff with σ_d = 0.03 (a modest fluctuation), or recall collapsing below half. Either would mean single-comparator gap rules need a noise model (for example several comparators or a pre-period variance estimate) before further development.

## Limitations stated in advance

Shocks are i.i.d., not persistent; real demand is autocorrelated, which would make comparators drift further. One comparator only. Pay remains fixed at 25/hour, so wage erosion is still untested. Seeds measure within-model randomness, not model validity. No holdout.

## Development note (pre-run tests, before the grid was generated)

P2 partly failed during structural testing. All cases and paths scale exactly from size 10 to 100 except `external_demand_slump` with AI: core work needs 4.2 workers' hours at size 10, so whole-worker staffing gives 8, whereas size 100 matches 42 core + 40 retained = 82. Firm size therefore matters even without noise when requirements are not whole-worker multiples. The test now pins this exception. No model or indicator rule was changed in response.

## Outputs

`outputs/noise-v04/run-001/`: `manifest.json`, `results.md` and `metrics.csv` (one row per cell and outcome). Raw per-seed histories are not saved; they are regenerated deterministically from the manifest's seeds and source hashes. Preserved v0.1–v0.3 outputs are hashed before and after the run.
