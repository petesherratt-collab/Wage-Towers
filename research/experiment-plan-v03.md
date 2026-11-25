# v0.3 pre-execution plan: employer decisions and delayed evidence

25 November 2026. Development cases only; no holdout or empirical calibration.

Question: with identical observed task savings, do alternative employer objectives and adjustment rules produce different paid-work outcomes, and which outcome channels remain detectable under uneven reporting?

Proposition: a staffing reduction should emerge from a specified decision problem, not an imposed cut. Valuable new work and sufficiently valuable retained capacity may prevent a reduction. Attrition should produce suppressed replacement hiring without layoffs. Automating new work later may undo initial absorption. These outcomes would weaken an unconditional automation-to-displacement claim.

## Economic design

- Paired with-AI and no-AI paths, same employer rule and exogenous conditions; separate comparator. Quarters 0–12, adoption q3, ten starting workers, 500 paid hours/worker/quarter, fixed real hourly pay 25 currency units. Core full-service revenue 250,000/quarter requires 5,000 human hours before automation. Core automation reduces required human effort by 40%; it is imposed technology, not an imposed staffing outcome.
- Enumerate integer staffing 0–20; maximise four quarters of current operating surplus less immediate hiring/layoff costs. Core service receives priority. New work is divisible and has explicit revenue and human requirements. Option value is an explicit monetary payoff for up to 2,000 retained idle hours, with sensitivity at 0, 15 and 30 per hour. It is a stipulated benefit, not observed revenue or validated valuation. True realised and decision values are equal in this first extension.
- Compare immediate review, four-quarter review, high adjustment cost, retention value, useful versus uneconomic new work, new work later automated, natural attrition/no-layoff adjustment, demand expansion and contraction, and no adoption. Wage bargaining remains outside this experiment; retain the v0.2 pay tests as regression evidence only.
- Default one natural departure per quarter when staff exist, matched in the two potential paths; hires and involuntary layoffs are separate. Attrition policy forbids layoffs. Between reviews replace natural departures to retain the previously selected headcount. Review decisions are endogenous within the stipulated objective; review timing and policy are not endogenous.
- Preserve an indistinguishable pair and a deceptive comparator: external non-AI efficiency can produce the same staffing reduction; do not give the indicator the hidden mechanism or no-AI path. Technology/non-AI efficiency effects overlap via the maximum reduction, a deliberately strong substitution assumption.

## Observation and indicator comparison

Separate economic model, publication ledger, indicator and evaluation. Field-specific releases contain only measured values, audit facts and publication dates. Missing evidence is absent, not a flag attached to otherwise usable numbers. Compare immediate publication, staggered field lags, five-quarter workforce lag, no contractor coverage and adverse-outcome-selective withholding of workforce/pay records. This selection is imposed for stress testing, not a reporting model.

Use 5%, 10%, 20% thresholds. Compare cumulative flow gaps (normalised by cumulative comparator turnover) with a fixed q3–q6 event window (normalised by baseline headcount). Their units/windows/denominators differ: do not claim a pure causal improvement from accuracy differences. Fixed-window results describe a historical event, never current staffing. Record later events outside that window as misses of its scope. Also report hours/headcount/pay stocks and use observed involuntary layoffs rather than inferring them from net headcount.

Stale stock evidence can support a dated historical assessment but cannot certify the current period. Output latest observed period, current-period status and attribution separately. Alternatives and task evidence must have been published by the assessment date and refer to periods no later than the assessed outcome; no future evidence may justify an earlier outcome. Freeze assessment histories.

Implementation clarification before the grid run: option payoff is capped both at 2,000 hours and at released legacy core capacity `max(0, 5000 − required core hours)`. This prevents unlimited hiring solely to earn option payoff; its boundary remains contestable. Parameter-only cases additionally test layoff cost 0/50,000, review every two quarters, retention value 24/26 and new-work value 26. Layoff gaps use baseline headcount in both flow rules because comparator layoffs are often zero. Current-horizon evaluation requires the published period/window to match the target for cumulative flows as well as stocks; fixed-event q3–q6 evidence remains a valid historical result when published later.

## Evaluation and checks declared before running

Report outcome-specific false alerts, positives, negatives, non-alert misses, positive abstentions, measurement/attribution/freshness coverage and first-detection delays with censoring. Compare current truth to current-period stock assessments; compare historical stock assessments to truth in their evidence period. Flow truth uses exactly the candidate's declared window. Separately report detection by the horizon for ever-occurring loss events so a fixed early window cannot appear to cover later layoffs. No statistical confidence intervals over this deterministic designed grid.

Check stock–flow reconciliation, paid versus used hours, finite nonnegative quantities, profit accounting, optimiser choice under its stated constraints, no-AI equivalence, same-input/same-output, future-evidence exclusion, missing scope, zero flow denominators, and preservation of v0.1/v0.2 hashes. Run old checks without rerunning their generators. Save the model/plan/test hashes, all parameters, scenario definitions, raw publication ledgers, truth, assessments and metrics in a new numbered output directory. Record failed checks and changes before interpreting results.

## Repository status

Read-only GitHub inspection of `petesherratt-collab/Wage-Towers` found a public, empty repository (contents endpoint: “This repository is empty”). Local work has no Git metadata; use file hashes. No remote publication is part of this experiment.
