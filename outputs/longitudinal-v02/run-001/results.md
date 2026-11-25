# v0.2 synthetic results

All cases are artificial development histories. No validation claim.

| ID | Mechanism | Task | Hours | Excess separations | Hiring gap | Pay |
|---|---|---|---|---|---|---|
| 0 | No adoption | not established | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 1 | Announcement without execution | not established | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 2 | AI staffing cuts | supported | alert | alert | below cutoff | below cutoff |
| 3 | Reduced paid schedules | supported | alert | below cutoff | below cutoff | below cutoff |
| 4 | Suppressed hiring during growth | supported | alert | below cutoff | alert | below cutoff |
| 5 | Demand absorbs savings | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 6 | Valuable reassignment | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 7 | Retained option capacity | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 8 | Delayed staffing review | supported | alert | alert | below cutoff | below cutoff |
| 9 | Expertise premium loss | supported | below cutoff | below cutoff | below cutoff | alert |
| 10 | Combined hours and pay | supported | alert | alert | below cutoff | alert |
| 11 | External demand contraction | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 12 | Outsourcing with stable paid work | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 13 | Workforce composition changes | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 14 | Quality deterioration | unknown | positive / unresolved | positive / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 15 | Preplanned restructuring disclosed | supported | positive / unresolved | positive / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 16 | Hidden restructuring fools comparator | supported | alert | alert | below cutoff | below cutoff |
| 17 | Adoption selection on declining demand | supported | positive / unresolved | positive / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 18 | Contaminated comparator | supported | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved | below cutoff / unresolved |
| 19 | AI demand expansion exceeds savings | supported | below cutoff | below cutoff | below cutoff | below cutoff |
| 20 | Ambiguous AI cause | supported | unknown / unresolved | unknown / unresolved | unknown / unresolved | unknown / unresolved |
| 21 | Ambiguous non-AI cause | supported | unknown / unresolved | unknown / unresolved | unknown / unresolved | unknown / unresolved |
| 22 | Small real effect below default cutoff | supported | below cutoff | below cutoff | below cutoff | below cutoff |

## Primary evaluation: complete records, zero delay, 10% cutoff

| Outcome | True positives in design | True negatives in design | Correct alerts | False alerts | Definitive misses | Positive abstentions | Coverage |
|---|---|---|---|---|---|---|---|
| hours | 8 | 15 | 5 | 1 | 1 | 2 | 65.2% |
| separations | 6 | 17 | 3 | 1 | 1 | 2 | 65.2% |
| hiring | 1 | 22 | 1 | 0 | 0 | 0 | 65.2% |
| pay | 2 | 21 | 2 | 0 | 0 | 0 | 65.2% |

Evaluation JSON contains all 54 parameter/evidence settings, denominators, false-alert rates, recall, precision, censoring and detected-delay lists. Grid totals repeat the same histories and are not independent samples. Truth counts every strictly adverse causal effect, including below-cutoff effects. Cumulative flow signals can dilute over time: first detection and endpoint detection differ.
