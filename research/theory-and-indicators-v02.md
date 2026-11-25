# Task replacement and paid-work displacement: working theory v0.2

25 November 2026. Proposed operational definitions and designed synthetic tests, not empirical findings. Read with `experiment-plan-v02.md` and `../outputs/longitudinal-v02/run-001/results.md`.

## Question and provisional judgement

When does AI performing human tasks imply less paid human work, rather than a different allocation of effort?

The testable proposition is conditional: AI can reduce the human effort needed for a specified service, but its total employment effect depends on demand, useful new assignments, retention, outsourcing and employer adjustment. The synthetic demand-absorption and expansion cases refute an *inevitable* progression from automation to displacement within this model. They do not establish how often either mechanism operates outside it.

Keep a vector of candidate indicators. A single composite score would conceal both the outcome being measured and which missing observation prevents attribution.

## Definitions and estimands

Declare the unit before assessment: organisation × function × geography × workforce boundary × period. Record employee and relevant contractor work, including suppliers taking over the same function. A narrow employer boundary and a wider production boundary can legitimately yield different answers; label both. Do not generalise either to economy-wide employment or displaced people's later employment.

Use event time (when work changed), reporting time (when a record was published) and assessment time (what could then be known). Default research window: quarterly observations, at least three pre-adoption periods and eight post-adoption periods where obtainable. These lengths are design choices, not sufficient identification conditions. Record seasonality and changes of boundary.

**Task replacement** means AI executes an identifiable operation formerly performed by a human, reducing total human effort needed per comparable completed task. Include prompting, supervision, checking, correction, exceptions and shifted supplier effort. Let m0 and m1 be human minutes per quality-comparable task without and with the intervention. Replacement fraction is `1 − m1/m0`; released effort for a fixed volume V is `V × (m0 − m1)` minutes. A positive measured difference needs evidence that AI executes the operation and that changed task mix, quality or another process change does not explain it. A before/after reduction alone is descriptive evidence, not an identified causal effect. Distinguish partial from complete replacement. Mere adoption, assistance without measured effort reduction, and abandoned work of lower quality do not meet this operational definition. Complete replacement would require zero residual human effort throughout the declared boundary.

**Employment displacement** is a negative causal effect on paid human work relative to a specified credible no-AI path, within the unit and time window. If H1 is paid hours with AI and H0 is hours without it, displacement in hours is `H0 − H1` when positive. Relative displacement is `1 − H1/H0`. Report negative values too: they represent net expansion under this estimand. In real data H0 is unobserved and must be estimated; a company plan is evidence about it, not its truth.

Report these channels separately:

- Job losses: excess eliminated occupied jobs or involuntary separations attributable to AI, with dates, reasons and treatment of transfers. Headcount decline alone cannot identify this channel. The v0.2 excess-separations candidate is a proxy; it lacks separation reasons and does not establish dismissals.
- Suppressed hiring: fewer actual hires than the no-AI path, including non-replacement of leavers. A cancelled advert or vanished page is not a hire or a lost job. Headcount can grow while hiring is suppressed.
- Reduced paid hours: lower total hours, and separately lower hours per continuing worker. FTE is an hours conversion, not a count of people. Distinguish unpaid effort from paid hours.
- Headcount shortfall: fewer people than the counterfactual, measured independently of hours. It is a stock, whereas hires and separations are flows. `N_t = N_(t−1) + hires − separations + net transfers/boundary changes`. Do not add overlapping hours, hiring and headcount effects into a total loss.

**Wage erosion** is an AI-attributable reduction in comparable-worker real hourly remuneration relative to the no-AI path. Let W be a fixed-composition real hourly pay measure; relative erosion is `1 − W1/W0`. Include the chosen cash/benefit components consistently and state the deflator and base period. Lower real pay growth counts even if nominal pay rises. Lower average pay caused only by hiring more junior workers is a composition change, not established comparable-worker wage erosion. Matched-worker panels also risk survivor selection when the worst-affected workers leave; report exits and fixed role/grade weights alongside them.

Annual earnings, hourly pay, hours and payroll are distinct. A worker's earnings may fall because hours fall while hourly pay is unchanged. Aggregate payroll combines hours, pay and composition. The synthetic pay index is already real with constant prices; inflation, benefits and selective worker exits are not simulated.

The primary estimand is the **total effect**, allowing AI to change output and demand. A secondary question holds output, quality and task mix comparable: how much human input is required for that service? Normalising hours by output does not automatically identify this controlled effect, and may remove AI-induced demand expansion from the total effect. The diagnostic `1 − (H_t/H_b)/(Q_t/Q_b)` is an intensity change, never a displacement estimate by itself.

## From Level 1 to Level 2

Level 1 supports task replacement. Level 2 supports AI plausibly contributing to a specified employment or pay consequence. They are separate claims, not inevitable stages. No numerical magnitude by itself promotes a case to Level 2.

| Evidence layer | Minimum operational record | What would weaken the judgement |
|---|---|---|
| Task execution | Named workflow, deployment/use dates, before/after task samples, all human handling time, output and quality checks; operational evidence independent of promotional wording | Unused tool, task redesign rather than AI execution, correction effort omitted, quality deterioration |
| Realised outcome | Consistent payroll/hours records, employee and contractor scope, hires/exits/transfers, or comparable-worker pay; both reference periods and units | Boundary change, outsourcing, unpaid overtime, worker composition, revisions or extraction error |
| Temporal link | AI operation precedes the proposed consequence; distinguish decision date, notice date and implementation date | Restructuring approved before adoption, seasonal hiring cycle, anticipation predating the chosen baseline |
| Counterfactual | Pre-trend and exposure evidence for a comparison group, or a documented alternative design such as staggered operational rollout; baseline plans with their uncertainty | Differential demand, adoption selection, comparator automation/spillovers, conflicting trends or forecasts |
| Mechanism and alternatives | Evidence linking task change to hours, staffing or bargaining decisions; explicit checks of demand, reorganisation, outsourcing, quality and composition | A non-AI mechanism explains the outcome, or relevant causes cannot be separated |
| Provenance and availability | Source identifier, publisher, publication/event dates, retrieved version, exact supporting passage/table, extraction method, unit and revisions | Sole company assertion, incompatible reporting periods, missing documents mistaken for zero |

A contemporaneous management explanation helps specify a mechanism but cannot replace outcome and counterfactual evidence. Multiple sources repeating one announcement are one evidential origin. Absence of a recorded alternative is not evidence that none exists. An event study or unexposed comparator is only conditionally credible: pre-trend similarity does not prove future parallel counterfactual trends.

For every outcome emit three outputs: (1) measured signal and magnitude, including unknown/below cutoff; (2) evidence adequacy, identifying the missing fields; (3) attribution: conditional support, not established or unresolved with reasons. Retain observed declines even if attribution is unresolved. “Below cutoff” means the selected rule did not alert, not zero effect. Adequacy of measurement can coexist with inadequate causal identification.

The implemented Level 2 route requires Level 1. That is a conservative candidate rule, not a logical claim that all AI wage effects require measurable task replacement: AI may change outside options or bargaining before local automation. Such a wage-only route needs separate exposure and identification evidence and remains untested here.

## Candidate portfolio and operational rules

Common specification: assess a fixed unit at each quarterly assessment date using only published records. b is the initial pre-adoption baseline, t is the latest published period, c is the comparator. Publication delay must be shown beside each result. All v0.2 observations are explicitly synthetic records, not citations or reconstructed firm data. The code stores the complete publication ledger and filters by availability; evidence masks are explicit invalidity flags even where numerical values remain in the test packet. Do not apply this fixture format directly to a collector.

The 10% strict cutoff is an illustrative materiality choice inherited for comparability, not significance, probability or an established economic threshold. The grid also tests 5% and 20%. A numerical tolerance of 1e-12 prevents floating-point rounding from moving equality above a cutoff. Real measurement error would require uncertainty intervals and sensitivity bounds; those are absent from this run.

### T: verified task effort reduction — tested diagnostic

Claim: partial or complete task replacement, not economic pressure. Unit is human minutes per completed comparable task; compare the baseline and latest observation. Signal is positive when `m_t < m_b`, supported by verified execution and quality checks. In v0.2 any exact reduction qualifies because task times are noiseless; do not export that rule to noisy observations. Needs time/workflow logs, checking effort and quality samples with independent provenance. Missing execution, invalid extraction or quality uncertainty produces unknown. Counterfactual assumption: the comparison task represents what humans would otherwise do; simultaneous workflow changes can defeat it. False alarms arise from hidden rework or lower quality; misses from unmeasured intermittent adoption. It can appear before staffing adjustment. Test result: announcement-only gives no Level 1; quality deterioration gives unknown. Task mix and omitted supplier checking are not fully tested.

### H: total paid-hours comparison — tested consequence candidate

Claim: plausible total hours displacement. Rule: `g_H = 1 − (H_t/H_b)/(H_c,t/H_c,b)`. The comparison estimates the no-AI change; output is not a divisor. Required sources: payroll time records plus contractor hours on the same boundary, comparison hours and exposure/pre-trend audit. Signal positive if `g_H > cutoff`; unknown when scope, extraction or comparison is inadequate. Attribution additionally requires T, timing and no unresolved recorded alternative. Reassignment, retained hours and demand expansion need not alert. Outsourcing with full boundary coverage should not alert; missing contractors must abstain. Hidden differential shocks can falsely alert; spillover-contaminated comparisons and late reports can miss effects. Evidence that a comparison group itself automated or had different demand weakens attribution. This tests total hours, not numbers of people or identified individuals losing work.

### F: separate hiring and separation flows — tested consequence proxies

Claim: suppressed hiring or excess separations, shown separately, not a single score. Sum flows from the first post-baseline period through the latest published period. Let A and C be cumulative treated and comparison counts. Hiring gap is `(C_hires − A_hires)/C_hires`; excess separation gap is `(A_exits − C_exits)/C_exits`. These dimensionless fractions require comparable workforce size and baseline turnover; both are supplied in this synthetic design. Zero denominators require unknown or a separately specified absolute-count rule, not division by zero. Current fixtures have positive denominators and the implementation is not a general input validator.

Needs reconciled HR stocks/flows, reasons for exits, planned versus realised recruitment, contractor turnover and comparison-group size. Current implementation requires scope, extraction and comparison checks, then the common attribution gate. Same illustrative cutoffs. A hiring gap is not an unfilled vacancy count. False alarms include transfers or a preplanned freeze; misses include attrition and turnover dilution. The v0.2 model always supplies ten routine hires and exits per quarter and puts all net contraction into extra separations: it does **not** simulate non-replacement attrition or distinguish voluntary/involuntary exits. These are priority additions. The observed-change field stores cumulative counts for these flow candidates; for H and W it stores endpoint minus baseline index units.

### W: fixed-composition real hourly pay comparison — tested consequence candidate

Rule: `g_W = 1 − (W_t/W_b)/(W_c,t/W_c,b)`; positive above cutoff. Needs matched-worker or fixed-grade pay data, hours and pay components, price deflator, composition weights, and comparison pay/exposure evidence. Missing comparable-pay panel gives unknown even when aggregate mean pay is supplied. Common attribution gate applies. General labour-market shifts, selective exits, bonuses and deflator mismatch can produce false alarms; delayed bargaining, new-starter-only cuts and missing contractors can cause misses. Opposite movement in within-grade and aggregate pay weakens an aggregate-pay inference. Synthetic result: pure composition change does not alert; two imposed wage-loss cases do. Two positives do not meaningfully validate sensitivity.

### P: unabsorbed released capacity — untested pressure proposal

Claim: potential adjustment pressure, not realised displacement. For a quarter let R be verified task hours released at fixed comparable volume, V be released hours reassigned to demonstrably useful human work, and O be released hours deliberately retained for documented option/service value. Report the interval for `U = max(0, R − V − O)` in hours and as a share of baseline paid hours. Track cohort allocation to avoid counting the same hour twice. If assignment value or option value cannot be supported, report unknown rather than setting it to zero. Proposed pressure flag: lower bound of U exceeds 10% of baseline hours for two quarters; arbitrary and untested. Needs allocation records, service outcomes, trial costs/value and management retention decisions. False alarm: valuable idle capacity omitted. Miss: activity recorded as useful while failing to earn sufficient value. Task counts or labour utilisation alone cannot supply V or O. Two-quarter persistence adds at least a quarter of detection delay after first excess. Replenishment-versus-retention is observationally identical in the current model, so this candidate is not scored.

| Candidate | Distinguishes | Evidence burden | Main robustness limit | Timing | Interpretability/status |
|---|---|---|---|---|---|
| T | Execution from announcements | Workflow and quality samples | Rework/task mix omissions | Early operational evidence | Direct minutes; tested simplification |
| H | Total hours from productivity | High: boundary plus counterfactual | Hidden shocks and spillovers | Staffing and reporting lags | Clear hours gap; recommended primary |
| F | Hiring suppression from exit flows | Very high: reconciled HR flows | Turnover, transfers, window dilution | Can precede net headcount decline | Separate channels; retain, revise window |
| W | Pay erosion from composition | Very high: comparable pay panel | Selective exits and bargaining confounding | Contract/review cycles | Separate pay gap; recommended co-primary |
| P | Possible pressure from absorbed savings | Highest: allocation and value | Option value hard to observe | Intended leading signal | Untested; do not promote to Level 2 |

Recommendation: carry T, H and W into the next synthetic cycle, retain F as separate experimental channels, and defer a numerical P alert until effort allocation and value are represented. Do not average their scores.

## Experiments, outcomes and limits

Run command: `python work/longitudinal_indicator_v02.py --out outputs/longitudinal-v02/run-001`. Completed 25 November 2026. The script refuses an existing destination; use a new numbered directory for reproduction. This deterministic grid has 23 histories × 3 delays × 6 evidence states × 3 cutoffs = 1,242 variants and 13,662 assessment dates. These are repeated designed cases, not 1,242 independent economic samples. No seed is required. Model, benchmark and plan hashes are in the manifest. Baseline output hashes were unchanged before/after execution. The original benchmark was inspected but not rerun because it writes to the preserved baseline directory. Existing tower checks passed on 3,780 quarterly states; their accounting success is not causal validation.

The new model is separate from the tower optimiser. Its paid-hours equation is `H1 = H0 × (1 + AI demand rebound) × (1 − staffing cut)` after the relevant onset. H0 incorporates external demand and non-AI restructuring. Cuts and pay effects are imposed parameters, not decisions derived from profitability or bargaining. The task sample falls from ten to four minutes independently of the staffing-cut parameter: it represents a named task, not all work. The model tests whether assessments respect distinctions, not whether the macroeconomic mechanism is correct.

| Challenge / changed assumption | Predicted difference and weakening result | Actual development result |
|---|---|---|
| Demand response offsets a 30% cut | If output expands by 1/0.7, total hours recover; automatic task-to-loss inference fails | Hours stay at 100 while output reaches 142.9; intensity falls 30%, no hours alert |
| Demand response exceeds savings | Net total effect can be positive despite task replacement | Output 170 and hours 119 versus no-AI 100; no hours alert |
| Demand slump independent of AI | Treated and comparator hours fall together; no differential effect | No hours alert |
| Hiring during growth | Headcount/hours grow but below the no-AI path | Actual 112 versus counterfactual 160; H and hiring alert |
| Smaller schedules rather than staff cuts | Hours should alert without excess exits | Hours alert; separation channel below cutoff |
| Outsourcing | Employee hours fall but boundary-total hours do not | No H alert; scope mask forces unknown |
| Composition rather than within-worker pay | Mean pay falls while comparable pay is constant | W does not alert |
| Known restructuring, quality loss, adoption selection | Visible alternative should prevent attribution even with adverse signal | Conditional alerts withheld; pre-trend detection itself is supplied as a flag |
| Hidden restructuring | Apparently adequate comparison can still falsely attribute | One hours and one separations false alert preserved |
| Comparator also automates | Comparator difference understates true effect | True loss missed/abstained; exposure supplied as an audit flag |
| Same observed history, different hidden cause | No observation-only rule can discriminate | Opposite-cause twins have identical assessments; attribution unresolved |
| Staffing cut at q7, evidence delayed five quarters | At q10 the cut has not yet been published | No alert by q10; censored |
| Reassignment versus retained capacity | Same paid hours should not reveal economic support or option value | Identical histories; these are stipulated interpretations, not independently modelled mechanisms |

Primary setting (complete records, no reporting delay, 10% cutoff): hours detects 5/8 true cases, with 1/15 false alerts among true negatives; one below-cutoff miss and two positive abstentions. Separations detects 3/6 at the endpoint with 1/17 false alerts; hiring detects 1/1 and pay 2/2, each with zero false alerts. Attribution decision coverage is 15/23 for every channel. The tiny and designed denominators prevent real-world accuracy claims.

At 5% the hours indicator detects 6/8, still with the same hidden-confounding false alert. At 20% it detects 5/8. This does not identify an optimal threshold. A two-quarter reporting delay leaves hours endpoint detection at 5/8 but delays each of those detections by two quarters. A five-quarter delay reduces it to 4/8; the four detected cases each have five-quarter delay and four true cases remain censored. These simple uniform lags do not model selective reporting or revisions.

An unexpected limitation is cumulative-flow dilution: the 8% staffing contraction triggers an excess-separation alert early, then routine turnover increases the denominator until the endpoint signal falls below 10%. Four true separation cases were detected at some point, but only three alert at q10. A fixed post-adoption window and persistent event record should be compared next; do not silently change the rule after seeing this outcome.

## Evaluation contract

Evaluate each channel and each assessment horizon separately. Hidden potential outcomes supply synthetic truth; the indicator never receives them or scenario titles. The benchmark explicitly verifies identical assessments for opposite-cause twins and that removing unpublished records cannot change an assessment. Known alternatives are visible audit flags, whereas hidden restructuring is not. This separation is necessary but the audit flags are much easier than real evidence appraisal.

- False-alarm rate: alerts on causal negatives / all causal negatives. Report count and denominator.
- Recall: alerts on causal positives / all causal positives. Here any adverse effect counts as positive, even below the indicator cutoff; a material-effect target would require a separately declared denominator.
- Misses: all causal positives without an alert, split into abstentions and non-alert decisions. The implementation calls the latter `definitive_misses`; this means a non-abstaining rule output, **not** a definitive finding that no effect exists. It includes stale-evidence failures when the latest reported period precedes the true change.
- Attribution coverage: proportion not unknown/unresolved. Measurement coverage is different; the current summary reports attribution coverage only, while each assessment retains adequacy. A null without task evidence is conservatively attribution-unresolved even when the observed outcome is below cutoff.
- Precision: correct alerts / all alerts. It depends on the artificial mixture and is not a real posterior probability.
- Detection delay: first qualifying alert at/after effect onset minus onset, in quarters; report the detected count, delay list and number undetected by q10. Censored cases are not zero-delay successes. First-ever detection and endpoint alert status answer different questions.
- False certainty: never render conditional support as proven causation. The hidden-confounding alert is the explicit erroneous attribution test. The implementation has no probability or “certain” output, so it does not estimate probabilistic calibration.

The evaluator compares detection by the assessment horizon against truth at that horizon, even when evidence ends earlier. Every assessment records its latest observed period: a late report cannot certify current absence of displacement. Future evaluation should additionally publish performance for the latest observed period, freshness coverage, per-quarter false-alert exposure, stale-evidence misses and transient effects. Current delay tests use persistent adverse effects, so later recovery is not tested.

No holdout has been used. This portfolio and cases developed together. Before claiming generalisation, freeze rules and evaluate untouched mechanism families with independent labels. Candidate next families are heterogeneous bargaining, contractor networks/spillovers, endogenous reporting, selective exits and new work subsequently automated. Repeated seeds in the existing tower simulator only measure randomness within its assumptions.

## Next discriminating experiment

Replace the imposed staffing cut with alternative employer rules: retain option capacity; cut only after a budget review; reassign only to tasks whose realised value covers costs; automate those new tasks later. Match initial visible task savings across rules. Add distinct hires/exits for attrition, fixed flow windows, field-specific publication delays and selective disclosure. The claim that released effort predicts pressure would weaken if comparable task savings repeatedly coexist with sustained, valuable human work under plausible rules. A model with only imposed cuts cannot answer that question.

The conditional pilot design is in `pilot-design-v02.md`. No sources, archives or watchlists were collected or modified during this work.
