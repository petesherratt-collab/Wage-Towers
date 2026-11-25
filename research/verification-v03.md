# v0.3 verification and decisions

25 November 2026.

## Executed checks

| Command | Result |
|---|---|
| `python -B work/test_employer_v03.py` | Nine tests passed before generation; repeated after the pre-run evaluation alignment clarification, also passed |
| `python -B work/run_employer_v03.py` | Exit 0; 23 histories (17 structural, six parameter-only), 690 variants, 8,970 assessments saved to new run-001 |
| `python -B work/verify_employer_v03.py` | Exit 0; replayed all 690 variants/8,970 assessments and 60 evaluation settings; source and preserved-output hashes matched; stale cumulative window and late-event checks passed |
| `python -B work/test_longitudinal_v02.py` | Six regression tests passed; original assessments reproduced |
| `node work/wage-towers/test.cjs` | PASS for 3,780 quarterly states |

No failed test runs or failed experimental executions occurred. The GitHub contents read returned an expected 404 explanation that the repository is empty; repository metadata was accessible. That is not a local execution failure.

## Preservation and limitations

The v0.1 and v0.2 outputs are preserved byte-for-byte against the hashes captured before v0.3 execution. The generated manifest hashes the three v0.3 implementation files, pre-execution plan and pre-run test file. The supplementary replay checker and research interpretation were written after the run and are not falsely represented as part of its pre-run manifest.

No Git repository exists locally, and no remote commits, branches, pull requests or publication were created. The user-supplied repository URL is recorded for provenance. Existing simulator code, collection archives and monitoring state were not changed.

New-work availability is assumed to depend on AI; option value is a stipulated monetary benefit; employer forecasts are perfect for current conditions but ignore future changes; labour supply and wages are fixed; headcount and hours are proportional. The supplementary cases are parameter sensitivities, not independent mechanisms. The report preserves hidden-confounding false positives, unknown current outcomes under publication lags, and the fixed event window's failure to cover later losses.

The next useful experiment is shared versus AI-enabled opportunities in the no-AI counterfactual, uncertain project returns, reversals in staffing, and independently crossed flow windows/denominators. Monitoring remains unstarted.
