# Review of Gemini's related-work response

Reviewed 25 November 2026 against primary sources. This is a targeted source check, not a systematic literature review or a claim that every related project has been found. No experiments, collection service or remote publication were started. Existing model results and README wording are unchanged.

## Judgement

Gemini provides a useful reading list. The principal projects and most descriptions are real and relevant. Its strongest claim—that Wage Towers occupies a rare methodological niche—is not established by the evidence it gives. It also incorrectly equates exposure scoring with our Level 1 and observational tracking with our Level 2. Those errors should not become repository positioning.

Question: does existing work already cover Wage Towers' economic mechanisms or indicator-testing approach? Provisional answer: much of the economics and the general simulation-based evaluation method have clear precedents. A useful contribution remains possible in a reproducible, domain-specific suite that tests the inference from task evidence to separate paid-work outcomes under missingness, delays and competing causes. That is a proposed contribution, not demonstrated novelty.

## Source-by-source assessment

| Gemini item | Verification and necessary qualification | Relevance to Wage Towers |
|---|---|---|
| Anthropic observed exposure | Confirmed: Massenkoff and McCrory, 5 March 2026. Combines capability and usage evidence and reports no systematic unemployment increase in highly exposed occupations, with tentative younger-worker hiring effects. “Observed exposure” is still an occupational measure, not verified firm-specific human minutes saved. [Source](https://www.anthropic.com/research/labor-market-impacts) | Separate capability, usage and realised labour outcomes; test platform-selection and occupation-to-firm inference. |
| Stanford Canaries | Confirmed August 2026 version, with ADP data through June 2026. Authors explicitly describe the patterns as descriptive, not causal estimates. They acknowledge sensitivity to education controls, some pre-existing divergence and sample differences from national benchmarks. [Paper](https://digitaleconomy.stanford.edu/app/uploads/2026/08/Canaries_August2026.pdf) | Add age/tenure cohorts and distinguish hiring from separations. Do not convert its relative employment gap into a count of AI-caused layoffs. |
| Yale Budget Lab | Broad summary needs qualification. Its May 2026 work uses synthetic differences-in-differences to address group differences. Its October tracker finds no clear large-scale disruption, while noting elevated relative unemployment growth for exposed workers. This is more nuanced than a blanket absence of relationships. [Method](https://budgetlab.yale.edu/research/what-we-do-and-dont-know-about-how-ai-affecting-labor-market), [tracker](https://interactives.budgetlab.yale.edu/tools/ai-labor-market-tracker/) | Comparator construction and cyclical sensitivity deserve explicit tests. “Synthetic” here is an estimation method, not invented economic histories. |
| RBA monitor | Confirmed staff note dated 9 November 2026, covering flows/stocks and younger workers. It explicitly calls the analysis partial and descriptive. One monitoring note does not establish an ongoing scheduled service. [Source](https://www.rba.gov.au/publications/insights/australian-economy/2026/monitoring-early-effects-of-ai-on-the-labour-market.html) | Good template for displaying contradictory evidence and cyclical alternatives without causal certainty. |
| ILO exposure caution | Confirmed brief announcement dated 17 April 2026: exposure indicators alone should not be interpreted as forecasts of job losses or labour-market outcomes. [Source](https://www.ilo.org/resource/news/ilo-releases-new-brief-ai-exposure-measurement) | Supports the distinction Gemini's closing classification accidentally removes. |
| Project Iceberg | Core description confirmed by MIT: 151 million workers, 32,000 skills, technical exposure distinguished from realised displacement and adoption timing. Its wage-value exposure figures are not wages actually lost. Ancillary implementation/count details in Gemini's text were not independently audited here. [MIT overview](https://www.media.mit.edu/projects/iceberg/overview/) | Closest visible overlap with wage-denominated task/skill exposure. Our wage bricks must remain an accounting illustration, not an additive valuation of task contributions. |
| Anthropic economic scenarios | Confirmed September 2026 model and explorer. Its explicit limitations include omitted policy/business-cycle effects and coarse treatment of displaced workers. Scenarios are conditional possibilities. [Source](https://www.anthropic.com/institute/econ-scenarios) | Relevant macroeconomic context, but not an empirical validator of our microeconomic rules. |
| BCC/NiGEM | Confirmed article dated 19 November 2026. Important omission in Gemini: the UK application models AI as a productivity increase, rather than reproducing task takeover and worker reallocation. Its baseline also differs from the Anthropic no-AI baseline. [Source](https://www.britishchambers.org.uk/news/2026/11/what-the-anthropic-institutes-ai-scenarios-could-mean-for-the-uk-economy/) | A direct warning that apparently similar scenarios can answer different counterfactual questions. |
| BCG task model | Confirmed 3 April 2026 analysis of roughly 1,500 roles. Automation potential, substitution/augmentation and demand expandability are explicit; structural scalability is also considered. Its projected job effects are model outputs, not measured displacement. [Source](https://www.bcg.com/publications/2026/ai-will-reshape-more-jobs-than-it-replaces) | Considerable overlap with our demand-response mechanism. That mechanism cannot credibly be presented as new. |
| PolicyEngine | Confirmed research infrastructure for policy/distributional effects under AI shocks. The repository describes a US starting focus, UK expansion and partially developed Canadian capability—not three equally implemented AI analyses. [Repository README](https://github.com/PolicyEngine/ai-inequality/blob/main/README.md) | Downstream complement: employment/pay scenarios can feed distributional analysis; it does not identify whether a firm's lost work was caused by AI. |
| Indeed/Glassdoor | Confirmed recent joint report/methodology. Measures include postings mentioning AI, occupation-level exposure, worker surveys and reviews. These are distinct denominators and measurement processes, not one realised-displacement series. [Methodology](https://hiringlab.indeed.com/2026/11/18/indeed-glassdoors-2027-u-s-hiring-and-worklife-trends-report-consolidated-methodology/) | Test changing terminology, job-posting coverage and sentiment separately from actual hires. |
| Challenger and aggregators | Challenger's October 2026 report confirms employer-attributed announcement categories, including separate AI and technological-update categories. I did not establish Gemini's causal explanation that relabelling explains part of the rise. Relabelling is a plausible testable alternative, not a verified decomposition. The named aggregators were not individually audited. [Report](https://www.challengergray.com/wp-content/uploads/2026/11/Challenger-Report-October-2026.pdf) | Preserve announced, implemented and attributed outcomes separately; do not treat every company statement as either truth or deception. |

The source checks verify specific versions and descriptions, not the correctness of every underlying empirical model or forecast. A more recent publication date does not mean its observations extend to that date.

## Three important omissions

**Task-based economic theory.** Acemoglu and Restrepo's 2019 *Automation and New Tasks* explicitly models displacement, productivity and reinstatement from new human tasks. Wage Towers should acknowledge this lineage and map its simpler mechanisms onto it. Their technical use of “displacement effect” should not be silently equated with our empirical employment-displacement claim. [Primary source](https://www.nber.org/papers/w25684)

**Linked adoption and administrative outcomes.** Humlum and Vestergaard link Danish adoption surveys to administrative earnings/hours records. The September 2025 paper reports task restructuring alongside null average earnings/hours effects, ruling out effects larger than 2% in the studied early period. The authors' October 2026 account states that the administrative observations run through December 2024; this is not a November 2026 labour-market snapshot. It is a particularly relevant challenge to the inference from adoption or changed tasks to lost paid work. [Paper](https://bfi.uchicago.edu/wp-content/uploads/2025/04/BFI_WP_2025-56-4.pdf), [authors' account](https://www.brookings.edu/articles/still-waters-rapid-currents-early-labor-market-transformation-under-generative-ai/)

**Simulation-based causal-method evaluation.** The ACIC competitions and Dorie et al.'s *Automated versus Do-It-Yourself Methods for Causal Inference* compare methods across constructed data-generating processes. This directly challenges Gemini's contrast between ordinary econometric work and synthetic diagnostic benchmarking. A specific AI-employment benchmark may still be useful; simulation-based evaluation itself is established practice. [Paper](https://arxiv.org/abs/1707.02641), [ACIC challenge](https://sites.google.com/view/acic2019datachallenge/home)

## Correcting the levels and novelty claim

Use the following as separate evidence dimensions, not a forced progression:

1. Capability/exposure: AI might perform a task.
2. Adoption/usage: AI is used in a relevant workflow.
3. Level 1: evidence supports actual replacement of identifiable human task effort, on a defined quality and workforce boundary.
4. Labour outcome: hours, hiring, layoffs or pay changed, relative to a stated baseline or comparator.
5. Level 2: evidence supports AI plausibly contributing to that specific consequence, conditional on the identification assumptions.

A project is not permanently assigned a level: its individual findings have different evidential status. An occupation-wide exposure score does not establish firm-level task replacement. A descriptive employment divergence does not automatically establish AI attribution. Conversely, broad wage or bargaining effects may occur without demonstrated local task replacement; our conservative Level 1 prerequisite can miss those channels.

Identical observations with different hidden causes are a useful non-identifiability test. Passing it means we have not allowed the rule to exploit hidden labels; it does not mean the rule has solved causal identification. The current benchmark is a set of designed development tests, with cases and rules built together. “Independent”, “clean-room validated” or “unique” would overstate its status.

Proposed repository description:

> Wage Towers is an experimental framework for testing when evidence of AI task automation supports a claim about reduced paid human work. It uses reproducible synthetic histories to compare candidate indicators for paid hours, hiring, layoffs and wages, with explicit assumptions, missing evidence, alternative explanations and reporting delays. It does not estimate current displacement prevalence or provide a validated monitoring service.

The tower metaphor is an accessible explanation of the problem. It is not a causal model or a proof that wages can be allocated additively to tasks.

## Consequences for the next work

These are proposed experiments, not runs completed in this review:

| Evidence/challenge | Model or measurement variant | Prediction and result that would weaken the claim |
|---|---|---|
| Stanford cohort divergence | Separate junior/senior hiring and task bundles, plus a non-AI junior-hiring slump | Aggregate stability can conceal a cohort effect; an indicator attributing the non-AI slump to AI fails specificity |
| Yale comparator difficulty | Matched and mismatched pre-trends, different interest-rate/cyclical sensitivity | Comparator differences should create false attribution unless detected or bounded |
| Humlum–Vestergaard task change without earnings/hours change | Time savings, oversight/new tasks and stable paid hours, with noisy effort measurement | A positive adoption/efficiency signal must not force an employment consequence |
| Iceberg capability versus use | High technical exposure without adoption; intensive platform use unrepresentative of the workforce | Exposure/usage-only inputs should not generate Level 1 replacement or Level 2 attribution |
| Existing displacement/reinstatement theory | New-work opportunities both with and without AI, versus AI-enabled opportunities only | Stable actual staffing may become a counterfactual shortfall once the no-AI opportunity is included |
| Challenger attribution categories | Hold realised workforce history fixed while changing announcement terminology and publication dates | An outcome indicator that changes solely with promotional wording is vulnerable |

Preserve the already planned shared-opportunity experiment; this review strengthens its rationale rather than replacing it with a large collection project. Add cohort composition next, but do not attempt to reproduce Stanford's finding with a toy model and call that validation.

Before populating GitHub, include a modest related-work section, the operational definitions and a prominent development-only status. Keep the failure cases visible. Distinguish a failure-mode benchmark from an economic forecast, and mechanism demonstrations from calibration. No claim of firstness is necessary to make the repository useful.
