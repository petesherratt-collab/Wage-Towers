# v0.3 generated results

Synthetic development cases; no empirical validation. Actual / no-AI pairs where shown. All workers have 500 paid hours per quarter.

| ID | Case | Staff q3 | Staff q6 | Staff q12 actual / no-AI | Hires q3–q12 | Layoffs q3–q12 |
|---|---|---|---|---|---|---|
| 0 | no_adoption | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |
| 1 | immediate_review | 6 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 2 | quarterly_budget_cycle | 10 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 3 | costly_adjustment | 9 | 6 | 6 / 10 | 6 / 10 | 0 / 0 |
| 4 | low_retention_value | 6 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 5 | high_retention_value | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |
| 6 | uneconomic_new_work | 6 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 7 | valuable_new_work | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |
| 8 | new_work_later_automated | 10 | 10 | 7 / 10 | 9 / 10 | 2 / 0 |
| 9 | attrition_no_layoffs | 9 | 6 | 6 / 10 | 6 / 10 | 0 / 0 |
| 10 | demand_absorption | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |
| 11 | demand_expansion | 12 | 12 | 12 / 10 | 12 / 10 | 0 / 0 |
| 12 | external_demand_slump | 8 | 8 | 8 / 10 | 9 / 10 | 1 / 0 |
| 13 | known_external_efficiency | 6 | 6 | 6 / 6 | 9 / 9 | 3 / 3 |
| 14 | hidden_external_efficiency | 6 | 6 | 6 / 6 | 9 / 9 | 3 / 3 |
| 15 | ambiguous_ai | 6 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 16 | ambiguous_external | 6 | 6 | 6 / 6 | 9 / 9 | 3 / 3 |
| 17 | cost_zero | 6 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 18 | cost_50000 | 9 | 6 | 6 / 10 | 6 / 10 | 0 / 0 |
| 19 | review_two | 10 | 6 | 6 / 10 | 9 / 10 | 3 / 0 |
| 20 | retention_24 | 9 | 6 | 6 / 10 | 6 / 10 | 0 / 0 |
| 21 | retention_26 | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |
| 22 | new_value_26 | 10 | 10 | 10 / 10 | 10 / 10 | 0 / 0 |

Primary: 17 structural histories, immediate publication, 10% threshold, cumulative flows.

| Outcome | Positives | Negatives | True alerts | False alerts | Positive abstentions | Non-alert misses | Attribution coverage |
|---|---|---|---|---|---|---|---|
| hours | 9 | 8 | 8 | 1 | 1 | 0 | 76.5% |
| headcount | 9 | 8 | 8 | 1 | 1 | 0 | 76.5% |
| pay | 0 | 17 | 0 | 0 | 0 | 0 | 76.5% |
| hiring | 9 | 8 | 2 | 0 | 1 | 6 | 76.5% |
| layoffs | 7 | 10 | 5 | 1 | 1 | 1 | 76.5% |

Full evaluation retains all settings, current versus historical evidence, coverage, delay lists and censoring. Pay is a null-only outcome here; its sensitivity cannot be estimated. Fixed-event flows target q3–q6 and have different denominators from cumulative hiring; do not compare raw accuracy as if the estimands were identical. See research/employer-experiment-v03.md for interpretation.
