# v0.3 findings: task savings, employer choice and delayed evidence

25 November 2026. Synthetic development experiment; no empirical validation or live collection.

## What changed

The v0.2 benchmark imposed cuts to hours and pay. The new model chooses integer staffing from a stated employer objective, holding initial task savings constant across competing mechanisms. It distinguishes natural departures, replacement hires and involuntary layoffs. New work has explicit human requirements and returns; retained idle capacity has an explicit, contestable monetary value. A separate publication ledger releases task, workforce, pay and audit evidence at different dates, or omits records entirely.

This is a new structural model alongside the original tower simulator and v0.2 benchmark. Neither was overwritten. It is not a calibrated upgrade to the tower interface and was not deployed. The linked GitHub repository was inspected using the connector: metadata showed a public repository and the contents endpoint reported that it was empty. No remote code or instructions existed to reconcile. All changes remain local.

## Question and result

Question: does the same verified task saving imply the same employment outcome when employer choices are represented explicitly?

No, within this model. A 40% reduction in core task effort can lead to fewer jobs, suppressed replacement hiring without layoffs, unchanged staffing supported by new work or retained capacity, or more staff following increased demand. These are counterexamples to automatic progression from Level 1 to Level 2, not estimates of which mechanism is most prevalent.

| Employer mechanism | Result with AI | No-AI result | What this discriminates |
|---|---|---|---|
| Immediate adjustment | 10 → 6 workers at q3 | 10 retained | Three layoffs plus one unreplaced natural departure; four missing jobs are not four layoffs |
| Four-quarter review cycle | 10 at q3, 6 from q4 | 10 retained | Delay between task replacement and staffing response |
| High layoff cost | 9 at q3, 6 by q6 | 10 retained | Employer chooses attrition without an explicit no-layoff constraint |
| No-layoff policy | Same gradual 10 → 6 path | 10 retained | Four suppressed replacement hires, zero layoffs |
| Retention value 15/hour | 6 workers | 10 retained | Retention payoff does not cover the wage cost |
| Retention value 30/hour | 10 workers, 2,000 idle paid hours/quarter | 10 retained | Unused hours need not imply imminent cuts if their option value is sufficient |
| New work worth 15 per original task-hour | 6 workers | 10 retained | A positive task count/value is insufficient to support extra paid labour |
| New work worth 40 per original task-hour | 10 workers | 10 retained | Valuable work absorbs 2,000 released human hours |
| Same new work later automated | 10 through q6, 7 from q7 | 10 retained | Initial absorption does not guarantee lasting human demand |
| Demand expands by 5/3 | 10 workers | 10 retained | Output expansion offsets core effort saving |
| Demand doubles | 12 workers | 10 retained | Positive total employment effect despite automation |

Each worker supplies 500 paid hours per quarter. Headcount and paid hours are therefore mechanically proportional in this experiment: their identical detection rates are not independent corroboration. Real hourly pay stays at 25 currency units; wage sensitivity is not tested by this run.

## Decision rule, units and counterfactual

For each candidate headcount n, the employer calculates quarterly operating surplus:

`core revenue delivered + new-work revenue delivered + option payoff − payroll − AI running costs`.

The decision score is four times this surplus minus immediate hiring and layoff costs. Four quarters is a fixed planning horizon, not a discount-rate estimate or a solution to a dynamic programme. Staffing is chosen among integers 0–20; ties favour the prior headcount, then the smaller workforce. The employer uses current conditions for all four quarters and does not anticipate later automation. Review schedules and the no-layoff policy are imposed, not optimised.

Ten initial workers provide 5,000 hours per quarter. Completing core output generates 250,000 currency units; delivery falls proportionally if there is insufficient human capacity. AI reduces core human requirement by 40%; AI running cost is five per removed core hour. Human pay is 25/hour. One natural departure occurs each quarter while anyone remains; this departure process does not respond to pay or adoption. Default hiring cost is 500/person and layoff cost 15,000/person. Outside review quarters, natural departures are replaced to preserve the previously selected stock.

Core tasks are allocated first. Extra work has up to 2,000 original human hours per quarter and explicit revenue; after new-work automation at q7 it needs 500 hours for the same revenue and costs 7,500 to automate each quarter. Unallocated work earns no revenue. Wage costs matter in the staffing decision even when work has positive gross revenue. All expected returns equal realised returns: forecast mistakes, learning and project failure are absent.

Option payoff applies to idle paid hours, capped at both 2,000 hours and released legacy capacity `max(0, 5000 − current required core hours)`. This prevents unlimited hiring to earn an artificial option benefit. The payoff is hypothetical monetary value, not cash receipts or an empirically measured benefit. Revenue, option payoff and realised surplus are separate fields so no one needs to mistake it for sales. At 24/hour, staffing falls gradually through attrition; at 26/hour it stays at ten. This is a consequence of the assumed wage/benefit comparison, not evidence that either valuation is realistic.

The paired no-AI path uses the same employer rule, demand and non-AI changes. It removes local AI and AI-enabled new work/rebound. The observable comparator shares the stated demand conditions but lacks the organisation-specific non-AI efficiency shock. This deliberately invalid comparison preserves a false-positive test. Overlapping AI and non-AI efficiency enter through their maximum rather than their sum, permitting identical observed histories with different hidden AI effects. This strong substitution assumption is a constructed identification test, not a claim about real production.

**An important maintained assumption:** new work is AI-enabled, so it is absent from the no-AI path. If the same opportunity would exist without AI, retaining ten people could still represent displacement relative to expansion without AI. The next paired counterfactual test should vary this assumption explicitly. Revenue and task requirements are distinct for core and new work, but the reported core-output field is not a quality-adjusted aggregate of both outputs.

## Observation and assessment design

The indicator imports no economic model and receives no hidden no-AI path, mechanism names, employer objective, option values or scenario title. A publication packet contains task samples, measured workforce quantities, pay and audit facts. Truth and titles are saved separately. Missing scope is an absent field. Selectively withheld workforce and pay records are absent rather than usable values accompanied by a warning flag.

Five observation profiles are compared:

| Profile | Task lag | Workforce lag | Pay lag | Audit lag | Additional restriction |
|---|---|---|---|---|---|
| Immediate | 0 | 0 | 0 | 0 | Complete records |
| Staggered | 0 | 2 | 3 | 1 | Field-specific dates |
| Long workforce lag | 0 | 5 | 3 | 1 | Longer staffing-report delay |
| Missing scope | 0 | 0 | 0 | 0 | No verified employee/contractor boundary |
| Selective withholding | 0 | 0 | 0 | 0 | No workforce/pay record when paid hours fall below q2 |

Lags are quarters. Selective withholding is an intentionally adverse disclosure rule; its incidence is not estimated. The simulator does not model a contractor sector, but the indicator still requires boundary assurance; scope tests are measurement tests, not an outsourcing simulation. Comparator credibility and source verification remain simplified audit inputs.

Hours, headcount and comparable-pay gaps use `1 − treated change / comparator change` from q2 to the latest published period. There is no output normalisation. Evidence must include the baseline and outcome, a scoped comparison, and published task evidence no later in event time than the outcome. A recorded alternative prevents attribution even when the measured signal is positive. Strict cutoffs are 5%, 10% and 20%, with a numerical tolerance of 1e-12. These remain arbitrary materiality tests, not statistical significance.

Current-period results require the observed period to equal the assessment period. Older data may support a historical signal but cannot certify current absence or current presence without an explicit persistence assumption. Consequently continuously lagged data always abstain on this strict current-period estimand. This is a deliberate refusal to nowcast, not a claim that historical evidence is useless. Historical detection is reported alongside current detection.

### Flow-window experiment

The cumulative rule sums q3 through the latest published period. Suppressed hiring is the shortfall divided by cumulative comparator hires. Layoffs are excess involuntary layoffs divided by baseline comparator headcount, since a comparator often has zero layoffs.

The fixed-event rule assesses q3–q6 once every required period is published, with both hiring and layoff gaps divided by baseline comparator headcount. Its result remains an assessment of that historical window. It can neither certify current staffing nor detect a first event at q7. A zero denominator returns unknown rather than a fabricated zero or an exception.

The comparison varies window **and** hiring denominator, so it is not a controlled test of window alone. A later experiment must cross these choices independently. The fixed rule successfully preserves an early event definition; it does not dominate cumulative monitoring.

## Results and denominators

The grid has 17 structural histories and six parameter-only variants. Each is assessed under five reporting profiles, three cutoffs and two flow rules: **690 variants and 8,970 assessment dates**. No random draws, seeds, independent population samples or holdout are involved. Structural and parameter-only metrics are reported separately in the evaluation JSON.

Primary setting: 17 structural histories, immediate records, 10% strict cutoff, cumulative flows, evaluated at q12.

| Outcome | True adverse effects | Correct alerts | False alerts / causal negatives | Positive abstentions | Other misses |
|---|---|---|---|---|---|
| Paid hours | 9 | 8 | 1 / 8 | 1 | 0 |
| Headcount | 9 | 8 | 1 / 8 | 1 | 0 |
| Suppressed hiring | 9 | 2 | 0 / 8 | 1 | 6 |
| Layoffs | 7 | 5 | 1 / 10 | 1 | 1 |
| Comparable hourly pay | 0 | Not estimable | 0 / 17 | 0 | 0 |

Measurement adequacy is 15/17 and attribution decision coverage 13/17 in this setting. Adequacy here includes an available comparison, so it is stricter than availability of a raw workforce number. “Other misses” are effects that fail the rule without an abstention, not proofs of no displacement. Any strictly adverse causal effect counts as truth, including an effect exactly equal to the materiality threshold.

The hours false alert is hidden non-AI efficiency: actual and hidden no-AI staffing both fall to six, while the observable comparator remains at ten. Known external efficiency blocks attribution. The opposite-cause ambiguous pair has identical observation packets and identical unresolved assessments. The preserved failure demonstrates why chronology, task execution and an apparently adequate comparison do not establish causality.

Hiring reveals a substantial timing problem: eight true cases alert at some point with immediate cumulative records, but only two still alert at q12. A one-hire shortfall is initially a large share of comparator recruitment; by q12 it is 1/10, exactly the cutoff and therefore below the strict alert rule. A persistent historical alert record should preserve the earlier result without pretending it is the current cumulative percentage.

The fixed event rule alerts on two of eight true hiring effects in q3–q6, and four of six true layoff effects in that window. Across the wider q3–q12 horizon there are nine histories with hiring effects and seven with layoffs; the fixed rule detects only two and four respectively. Its omission of later new-work automation is visible in the ever-effect denominators. Fixed-window detection waits until the window is complete, adding three quarters for q3 hiring effects even with immediate publication.

With staggered publication, eight of nine true hours-loss histories are eventually recognised historically by q12, with delays of two quarters in six cases and three quarters in two cases; the latter include an extra period to clear the threshold. One remains censored because the comparison is unavailable. None has a current-q12 hours alert because q12 workforce evidence is not yet published. Five-quarter workforce delays give the corresponding historical detection delays of five and six quarters. Missing scope and selective withholding leave all nine true hours effects undetected by q12. Zero alerts under those profiles must not be called successful avoidance of false alarms.

The external-demand-slump/retention case is intentionally an interaction, not a pure non-AI null: actual staffing is eight while the no-AI employer retains ten under its option-value rule. An outcome cannot be dismissed as “just demand” without examining the counterfactual interaction. The separate v0.2 matched-slump null remains preserved.

These rates cannot be compared directly with v0.2 as evidence of improved accuracy: the economic mechanisms, sample mixture, channels, timing rules and measurement definitions changed. All scenario labels and parameters were available during development. Synthetic success establishes neither real-world prevalence nor predictive validity.

## Verification, audit and reproduction

Pre-execution plan: `experiment-plan-v03.md`. Code is split between `work/employer_model_v03.py`, `work/employer_measurement_v03.py` and `work/run_employer_v03.py`.

Commands:

```text
python -B work/test_employer_v03.py
python -B work/run_employer_v03.py --out outputs/employer-v03/run-001
python -B work/verify_employer_v03.py
python -B work/test_longitudinal_v02.py
node work/wage-towers/test.cjs
```

The runner refuses an existing destination; use a new numbered directory inside `outputs/employer-v03` to reproduce the grid. The replay checker targets saved run-001. The manifest records source/plan/test SHA-256 hashes, all previous output hashes, parameters, observation profiles and counts. Raw observations, hidden potential outcomes, assessments and evaluation are separate JSON artefacts. No Git commit is claimed because the local project has no Git metadata.

Nine v0.3 tests passed before the grid run: capacity and financial/stock-flow accounting, maximisation under the stated constraints, no-AI equivalence, mechanism distinctions, identical observations/opposite truths, future-evidence exclusion, lagged/missing evidence, fixed windows/zero denominators and the retained hidden-confounding false alert. The six v0.2 checks and original 3,780-state simulator checks also passed. A supplementary post-run checker replays every saved assessment and evaluation setting and checks preservation hashes; its result is recorded in `verification-v03.md`.

No failed test run occurred. During pre-run inspection the implementation was clarified so that option payoff cannot subsidise unlimited speculative hiring, and stale cumulative flows cannot be judged against a later unpublished total. Those clarifications were recorded in the plan before generating run-001. No rules were retuned after seeing the grid results.

## Judgement and next experiment

Keep total paid hours as the primary quantity candidate, with separately reported hiring and layoffs. Keep real comparable pay separate, but make no new claim about wage sensitivity from this all-constant-pay model. Retain both dated historical evidence and an explicit current-period unknown. Do not collapse them into one confidence score.

The next discriminating experiment should vary whether new-work opportunities also exist in the no-AI world, introduce forecast errors about their value, and cross flow-window choice with denominator choice independently. Add a shock that later reverses staffing loss to test stale historical signals against recovery. These tests would challenge the current absorption result and the strict freshness policy more directly than another batch of random seeds.

The feasibility pilot remains a design, not an operational service. This experiment resolves the imposed-cut limitation partly: choices now follow costs and payoffs, but those objectives, beliefs, labour supply, option values and counterfactual opportunities remain assumptions.
