# Synthetic evidence experiment — version 0.1

**All organizations, histories and observations are artificial. No real-world evidence is represented.**

## Purpose

Test whether an indicator distinguishes task replacement, employment displacement and wage erosion, and whether it admits when the evidence is insufficient. This tests a measurement design; it does not validate an economic forecast.

The indicator sees only observable-evidence.json. Ground truth lives in ground-truth.json. It never receives scenario titles or causal labels. Its rules were fixed before these results were computed; nothing was fitted. These are designed tests, not a blinded or externally validated benchmark.

## The two levels

**Level 1 — task replacement supported:** operational evidence, separate from an announcement, shows AI executing a named task with lower human time per unit.

**Level 2 — a labor outcome is supported:** Level 1 plus correct timing, comparable output/quality/task mix, employee-and-contractor coverage, a credible unexposed comparison, and no recorded unresolved competing explanation. Employment quantity and real hourly pay are assessed separately.

An absent recorded competing explanation is NOT proof that none exists. Level 2 is conditional support, not verified causation.

## Quantitative rule used in this experiment

Every series starts at 100. Human hours include employees and contractors. The employment signal is:

    firm intensity change = (hours after / hours before) / (output after / output before)
    comparison intensity change = the corresponding ratio in an unexposed comparison group
    employment gap = 1 - firm intensity change / comparison intensity change

The wage signal is:

    wage gap = 1 - firm real-pay change / comparison real-pay change

The illustrative threshold is strictly greater than 10%. It is a design choice, not an empirically established cutoff or statistical significance test. Proportional output adjustment is also an assumption, not an economic law. Scale effects, different task mixes, quality changes or invalid controls can defeat it. If suitable measures are missing, the result stays unresolved.

This is not the earlier released-hours displacement ratio. It does not recover how many released task hours were reallocated; it measures relative labor outcomes when sufficient comparable observations are supplied.

## Results of 16 designed histories

| ID | Synthetic history | True AI employment displacement? | Indicator result |
|---|---|---|---|
| S01 | No AI intervention | No | Below Level 1: unknown; unknown |
| S02 | AI announcement only | No | Below Level 1: unknown; unknown |
| S03 | Successful reassignment | No | Level 1: not established at threshold; not established at threshold |
| S04 | Demand absorbs released capacity | No | Level 1: not established at threshold; not established at threshold |
| S05 | AI-linked layoffs | Yes | Level 2 support: displacement supported; not established at threshold |
| S06 | Attrition and non-replacement | Yes | Level 2 support: displacement supported; not established at threshold |
| S07 | Suppressed hiring during growth | Yes | Level 2 support: displacement supported; not established at threshold |
| S08 | Demand slump alongside AI | No | Level 1: not established at threshold; not established at threshold |
| S09 | Outsourcing disguises unchanged human work | No | Level 1: not established at threshold; not established at threshold |
| S10 | Retained spare capacity | No | Level 1: not established at threshold; not established at threshold |
| S11 | Expertise premium erodes | No | Level 2 support: not established at threshold; erosion supported |
| S12 | Hours and wages both contract | Yes | Level 2 support: displacement supported; erosion supported |
| S13 | Ambiguous history A: AI caused the reduction | Yes | Level 1: unresolved; unresolved |
| S14 | Ambiguous history B: another reorganization caused it | No | Level 1: unresolved; unresolved |
| S15 | Apparently convincing but invalid comparison | No | Level 2 support: displacement supported; not established at threshold |
| S16 | Known competing explanation | No | Level 1: unresolved; unresolved |

## Findings

1. **Task replacement and employment displacement are separable.** Successful reassignment and retained spare capacity have the same visible labor outcome here. Their internal economic support differs, but these observations cannot distinguish it.
2. **Rising headcount/hours can coexist with displaced hiring.** S07 rises from 100 to 110 hours against a stipulated comparison rising to 150. Its relative gap is 26.7%.
3. **Falling payroll headcount is insufficient.** S08's labor reduction follows demand; S09 moves work to contractors. Neither clears the employment criterion with full scope and comparison data.
4. **Wage erosion is a separate outcome.** S11 keeps hours unchanged while real hourly pay falls 25% relative to the comparator.
5. **Some causes are not identifiable from the observed record.** S13 and S14 have exactly identical observations and opposite employment-causation truths. The indicator correctly gives both an unresolved result; no method using only those same observations can distinguish them reliably.
6. **Apparently strong evidence can still mislead.** S15 produces Level 2 support even though a hidden reorganization caused the reduction. This deliberate false positive shows why a credible-looking comparator and correct chronology do not prove causation.
7. **Level 1 does not establish economic pressure by itself.** Additional evidence is needed about whether released capacity finds valuable work, is retained for flexibility, or is merely awaiting an adjustment.

## Evidence-loss stress test

Forty random evidence conditions per history produce 640 records. Seed: 42. The masks are chosen uniformly for testing, not to describe real reporting frequencies.

Results: {'Below Level 1': 154, 'Unassessable': 86, 'Level 1': 375, 'Level 2 support': 25}.

Removing a required evidence element prevents Level 2 support under this conservative rule. That reduces false confidence but necessarily misses true displacement when disclosure is incomplete. These counts are not real-world accuracy, prevalence or probability estimates.

## What to improve before collecting real evidence

- Define the unit tightly: organization, function, period, geography and workforce boundary.
- Establish what would count as a credible comparator and test its pre-intervention behavior.
- Specify alternative explanations before looking at cases, including outsourcing, demand, preplanned restructuring and quality deterioration.
- Distinguish reported company attribution from independently corroborated attribution.
- Preserve evidence availability as its own output. Unknown must not become zero displacement.
- Test thresholds and model structures using unseen scenarios later. No true holdout validation has been performed here.
- Add observation delays and repeated periods; this first set compares two periods and cannot estimate detection lead time.

## Files

- observable-evidence.json: evidence packets, without ground truth or scenario titles.
- ground-truth.json: causal labels and explanations, for evaluation only.
- indicator-results.json: rule-based assessments.
- evidence-loss-experiments.json: 640 evidence-masking records and their assessments.

The experiment has not changed Wage Towers, the published site, or any GitHub repository.
