# Development experiment plan v0.2

Recorded before the first v0.2 execution, 24 November 2026. All histories are designed development cases; there is no holdout and no empirical calibration.

Question: can separate task, total paid-work and comparable-worker pay signals avoid confusing productive automation with displacement, while retaining explicit uncertainty about causes?

Proposition: output-normalised effort can fall without a negative total paid-work effect. Demand response, useful reassignment and retention should break the proposed automatic progression from task replacement to displacement. Plausible-looking comparisons should still fail under hidden confounding.

## Frozen comparison for this development run

- Preserve v0.1 files and simulator; run existing simulator checks without modifying it.
- Add a separate, deliberately simple quarterly structural model: three pre-adoption quarters (0–2), adoption at 3, follow-up through 10. Units: paid hours, headcount and output indices, real comparable-worker hourly pay index, hires and separations per quarter. Index headcount represents a synthetic workforce of 100 people at baseline, with continuous expected stocks/flows, not individual workers.
- Compare task-effort reduction, total hours/counterfactual comparison, separate headcount flows and pay. Output intensity is diagnostic only.
- Parameters: strict effect cutoffs 5%, 10%, 20%; publication delays 0, 2, 5 quarters; complete records, missing contractors, missing task evidence, missing comparison, missing pay panel and extraction failure. No random draws; this is an exhaustive designed grid, not a population sample.
- Structural cases: null, announcements, cuts, reduced schedules, hiring suppression with growth, demand absorption, reassignment, retention followed by cuts, wage erosion, combined loss, external demand slump, outsourcing, composition, quality deterioration, known and hidden restructuring, adoption selection, contaminated comparator, AI expansion and ambiguous opposite-cause twins.
- Signal = positive, below cutoff or unknown. Adequacy and attribution are separate. A Level 2 alert requires positive outcome, Level 1, adequate records, plausible timing and no observed unresolved alternative. Validity remains conditional.
- Evaluate hours, excess separations, suppressed hiring and pay separately. Count false alerts over true negatives, detected cases over true positives, definitive misses and abstentions separately, coverage, and positive predictive value. Report first-alert delay from true effect onset, censor undetected cases at the assessment horizon; never average only detected delays without stating the denominator.
- Success criteria for implementation: identical available inputs produce identical assessments; unavailable records cannot change past assessments; scope loss prevents hours attribution; composition alone does not cause a comparable-worker pay alert; growth can coexist with a hiring gap; hidden confounding remains a documented failure; delay causes censoring or later detection. These are invariants, not target accuracy fitted to the scenarios.

## Departures from the baseline

This is a structural extension, not a rerun of v0.1 or a calibrated extension of the tower optimiser. The latter optimises homogeneous staffing with imposed wage compression, uses labour utilisation to label bricks as supported, and lacks contractor/person tracking. It cannot establish the value of idle capacity or infer causal displacement from its own accounting identities. v0.2 uses explicit paired potential histories and separately generated observations. Comparator paths are evidence proxies, never the hidden no-AI path passed directly into the indicator. No indicator receives scenario names or truth labels. Comparator checks are simplified supplied audit flags, not automated identification.

Next untouched evaluation families should include heterogeneous labour bargaining, network spillovers, imperfect task measurement and non-random disclosure. They are proposals only; none is a holdout result.
