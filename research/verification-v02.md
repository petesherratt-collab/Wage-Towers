# Verification and decision log — 25 November 2026

## Completed commands

- `python work/longitudinal_indicator_v02.py`: exit 0; wrote only the new `outputs/longitudinal-v02/run-001` destination. 23 designed histories, 1,242 variants, 13,662 assessments. In-script invariants passed; preserved v0.1 output hashes matched before/after.
- `node work/wage-towers/test.cjs`: exit 0; PASS across 3,780 quarterly states. Original model and checks were not edited.
- `python -B work/test_longitudinal_v02.py`: exit 0; six tests passed. Covers stock–flow conservation/nonnegative quantities, literally identical observation packets with different causal truths, mutations to future evidence, missing comparable-pay evidence, the strict threshold boundary, and reproduction of every saved assessment from the stored packets.

These checks establish implementation consistency for this design, not economic or empirical validity. The supplementary test file was added after run-001 and is therefore outside that run's source manifest; the main benchmark code has not changed since the run.

## Decisions and limits

- Preserve baseline outputs; do not import or execute the original benchmark, which writes to its baseline directory at module level.
- No Git repository was found at the project root (`git status --short` failed). Use recorded SHA-256 hashes rather than inventing a commit identifier.
- Keep total hours and comparable pay separate, with hiring and separations as separate experimental channels. Keep output intensity diagnostic.
- Keep hidden-confounding false alerts and non-identifiable twins; do not alter rules to erase them.
- Record cumulative-flow dilution rather than tune the window after observing it. A fixed-window comparison is the next test.
- Treat synthetic reassignment and retention labels as alternative interpretations of the same imposed hours path. Their economic value has not been simulated.
- Comparator validity, task verification and some alternatives are supplied flags. Real-world appraisal of those facts is harder and unvalidated.
- Missing-evidence flags control assessment despite fixture numbers remaining in packets. Future collection must use genuine missing values and validate schema, denominators, units and dates.
- No collection, monitoring, external publication, deployment or edits to protected evidence directories occurred.

Current research narrative: `theory-and-indicators-v02.md`. Conditional pilot protocol: `pilot-design-v02.md`. Next action: test employer adjustment rules, attrition, fixed flow windows and field-specific publication delays before revisiting pilot readiness.
