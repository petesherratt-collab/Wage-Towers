# Reference inputs borrowed from other work

## spillover_paths_v05.csv

Employment in **non-AI-sensitive** occupations relative to its value at the start of each window, sampled every three months. Derived from the exported monthly paths (`out/substantial.csv`, `out/extreme.csv`, column `l_N`) of:

> Hoces de la Guardia, F. (2026). *Reimplementation: "Economic Scenarios for Transformative AI"*, v1.0, MIT licence. https://github.com/fhoces/opa-ai-macro-econ-scenarios, commit `2f7b1454d85e5ee88c407725e01b781af23e8706`.

That repository independently reimplements Korinek, Jones, Sacher, Cotter and McCrory (2026), *Economic Scenarios for Transformative AI*, Anthropic Institute Working Paper 2026-02. Its 129 tests passed when inspected here on 25 November 2026. Wage Towers does not import or run its code; only these exported values are used.

Why it matters here: in that model, workers displaced from AI-sensitive occupations move into other occupations, so an "unexposed" comparator is itself changed by AI. That breaks the assumption that a comparator shows the no-AI path. v0.5 uses these paths as a contaminated-comparator condition. They are a macro scenario's spillover for an economy-wide occupational group, not an estimate for any firm's peers, and are used only as an illustrative magnitude.

| Scenario | 2024–2027 rise | 2027–2030 rise |
|---|---|---|
| Substantial | +0.8% | +4.3% |
| Extreme | +1.5% | +12.6% |
