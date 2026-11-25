# Wage Towers

An experimental framework for testing when evidence of AI task automation supports a claim about reduced paid human work.

Wage Towers compares candidate indicators for paid hours, hiring, layoffs and wages using reproducible synthetic histories. It keeps assumptions, missing evidence, alternative explanations and reporting delays explicit.

**Status:** research prototype and designed development tests. No empirical calibration, independent holdout validation, current displacement estimate or live monitoring service. Known false positives and unresolved cases are retained deliberately.

**Level 1** supports replacement of identifiable human task effort. **Level 2** supports AI plausibly contributing to a specific employment or wage consequence. These are separate claims: task replacement need not cause displacement. Wage bricks are an explanatory metaphor, not tasks or a causal model.

## Start here
- research/employer-experiment-v03.md: latest experiment on employer decisions, attrition, new-work automation and uneven reporting.
- outputs/employer-v03/run-001/results.md: v0.3 results; adjacent files retain the full audit trail.
- research/theory-and-indicators-v02.md: current definitions, evidence requirements, candidate portfolio and evaluation findings.
- research/experiment-plan-v02.md: pre-execution development comparison and assumptions.
- outputs/longitudinal-v02/run-001/results.md: new synthetic results; adjacent JSON files retain observations, truth, assessments, evaluation and hashes.
- research/pilot-design-v02.md: conditional evidence-feasibility pilot design; not launched.
- [Related-work review](research/related-work-review-2026-11-25.md): useful existing theory, empirical studies and methods. No claim of firstness.
- AGENTS.md: standing project instructions.
- research/starting-brief.md: provenance and first milestone.
- research/instruction-stress-test.md: review of the instructions.
- work/wage-towers/dist/: recovered simulator HTML, JavaScript and CSS.
- work/wage-towers/test.cjs: recovered simulator checks.
- work/synthetic_indicator.py: recovered benchmark generator and indicator.
- outputs/synthetic-indicator/: preserved original findings and data.

## Run locally

Use Python 3.10+ and Node.js 18+; the models and checks use standard libraries. Development checks were run on Windows.

Clone the repository, then restore the losslessly archived JSON artefacts and run checks from the repository root:

```sh
python work/restore_outputs.py
python -B work/test_employer_v03.py
python -B work/verify_employer_v03.py
python -B work/test_longitudinal_v02.py
node work/wage-towers/test.cjs
```

Generate a new experiment without overwriting preserved results:

```sh
python -B work/run_employer_v03.py --out outputs/employer-v03/run-002
python -B work/longitudinal_indicator_v02.py --out outputs/longitudinal-v02/run-002
```

The runners refuse existing destinations. **Do not run `work/synthetic_indicator.py` against the preserved baseline:** the original generator writes directly to `outputs/synthetic-indicator`. Change its destination in a separate experimental copy first.

For the original visual simulator, open [work/wage-towers/dist/index.html](work/wage-towers/dist/index.html) locally in a browser. It is a separate model from the later Python experiments.

## Reproducibility

Reports and manifests are directly readable under `outputs/`. The large JSON artefacts are stored in `outputs/reproducible-data.zip` at their original paths. The restore command checks the archive and individual file hashes, rejects unsafe paths and never overwrites differing existing data. Restored raw JSON is ignored by Git. Original source line endings are preserved because historical manifests hash exact bytes.

The latest experiment includes 23 histories, 690 variants and 8,970 assessments. Staffing choices respond to retained capacity, valuable new work, attrition and costs. Hidden non-AI efficiency still causes a false attribution. These are model demonstrations, not population estimates.

Historical documents describe the state at the time of each experiment, including its then-local-only status. Repository publication does not change those findings or launch the pilot.

Next priorities: shared versus AI-enabled new-work opportunities, uncertain project returns, workforce cohorts and independent comparisons of flow windows and denominators.
