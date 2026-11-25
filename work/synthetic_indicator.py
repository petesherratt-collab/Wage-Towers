"""Synthetic evidence benchmark. No real firms, sources or observations.

The indicator only receives `observations`. Ground truth is generated and
stored separately. Rules are fixed; no parameters are fitted to the cases.
"""
import copy
import json
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'synthetic-indicator'
OUT.mkdir(parents=True, exist_ok=True)

def observations(hours=100, output=100, wage=100, comparator_hours=100,
                 comparator_output=100, comparator_wage=100, task=True,
                 verified=True, comparison=True, scope=True):
    # Indices use 100 as the common pre-intervention baseline. Numbers are
    # illustrative observations of synthetic firms, not inferred ground truth.
    return {
        'synthetic': True,
        'unit': 'same organization, function and observation period',
        'ai_adoption_reported': task,
        'task_execution_evidence': {
            'available': task and verified,
            'ai_performs_named_task': task and verified,
            'human_minutes_per_unit_before': 10 if task and verified else None,
            'human_minutes_per_unit_after': 4 if task and verified else None,
            'operational_record_independent_of_announcement': task and verified,
        },
        'workforce': {
            'paid_human_hours_before': 100,
            'paid_human_hours_after': hours,
            'covers_employees_and_contractors': scope,
            'real_hourly_pay_before': 100,
            'real_hourly_pay_after': wage,
        },
        'production': {'output_before': 100, 'output_after': output,
                       'quality_comparable': True, 'task_mix_comparable': True},
        'comparison': {
            'available': comparison,
            'unexposed_group': True,
            'similar_pre_intervention_trend': True,
            'same_work_and_period': True,
            'human_hours_before': 100, 'human_hours_after': comparator_hours,
            'output_before': 100, 'output_after': comparator_output,
            'real_hourly_pay_before': 100, 'real_hourly_pay_after': comparator_wage,
        },
        'timing': {'ai_precedes_workforce_change': True},
        'alternative_explanations': [],
        'coverage': {'before_and_after_observed': True, 'extraction_valid': True},
        'source_records': [
            {'id': 'A', 'kind': 'synthetic implementation disclosure'},
            {'id': 'B', 'kind': 'synthetic operational record'},
            {'id': 'C', 'kind': 'synthetic workforce and contractor record'},
            {'id': 'D', 'kind': 'synthetic comparison-series record'},
        ],
    }

def classify(o, threshold=.10):
    """A deliberately conservative rule, not a causal estimator or probability."""
    coverage = o['coverage']
    if not all(coverage.values()):
        return {'level': 'Unassessable', 'employment': 'unknown', 'wages': 'unknown',
                'reason': 'Observation or extraction coverage is inadequate.',
                'employment_gap': None, 'wage_gap': None}
    t = o['task_execution_evidence']
    task = (t['available'] and t['ai_performs_named_task']
            and t['operational_record_independent_of_announcement']
            and t['human_minutes_per_unit_after'] < t['human_minutes_per_unit_before'])
    if not task:
        return {'level': 'Below Level 1', 'employment': 'unknown', 'wages': 'unknown',
                'reason': 'An announcement alone does not establish task replacement.',
                'employment_gap': None, 'wage_gap': None}
    w, p, c = o['workforce'], o['production'], o['comparison']
    blockers = []
    if not w['covers_employees_and_contractors']: blockers.append('contractor scope missing')
    if not p['quality_comparable']: blockers.append('quality not comparable')
    if not p['task_mix_comparable']: blockers.append('task mix not comparable')
    if not all(c[k] for k in ['available','unexposed_group','similar_pre_intervention_trend','same_work_and_period']):
        blockers.append('credible comparison absent')
    if not o['timing']['ai_precedes_workforce_change']: blockers.append('timing does not support attribution')
    blockers.extend(o['alternative_explanations'])
    if blockers:
        return {'level': 'Level 1', 'employment': 'unresolved', 'wages': 'unresolved',
                'reason': 'Task replacement supported; attribution unresolved: ' + '; '.join(blockers) + '.',
                'employment_gap': None, 'wage_gap': None}
    firm_intensity = (w['paid_human_hours_after']/w['paid_human_hours_before'])/(p['output_after']/p['output_before'])
    control_intensity = (c['human_hours_after']/c['human_hours_before'])/(c['output_after']/c['output_before'])
    # This comparison requires proportional labor/output scaling within each
    # group and a usable comparator. Neither assumption is automatically true.
    employment_gap = 1-firm_intensity/control_intensity
    wage_gap = 1-(w['real_hourly_pay_after']/w['real_hourly_pay_before'])/(c['real_hourly_pay_after']/c['real_hourly_pay_before'])
    employment = employment_gap > threshold
    wages = wage_gap > threshold
    return {
        'level': 'Level 2 support' if employment or wages else 'Level 1',
        'employment': 'displacement supported' if employment else 'not established at threshold',
        'wages': 'erosion supported' if wages else 'not established at threshold',
        'employment_gap': round(employment_gap, 6), 'wage_gap': round(wage_gap, 6),
        'reason': ('Task evidence, timing and comparison support a labor outcome; causation remains conditional on comparison validity.'
                   if employment or wages else 'Task replacement is supported; no labor outcome clears the selected threshold. This is not proof of no effect.'),
    }

cases = []
def add(name, o, task, employment, wages, explanation, family):
    i = f'S{len(cases)+1:02d}'
    cases.append({'id': i, 'name': name, 'family': family,
                  'truth': {'task_replaced': task, 'employment_displaced_by_ai': employment,
                            'wages_eroded_by_ai': wages, 'mechanism': explanation},
                  'observations': o})

add('No AI intervention', observations(task=False), False, False, False,
    'Tasks, staffing, workload and wages stay unchanged.', 'baseline')
add('AI announcement only', observations(verified=False), False, False, False,
    'AI is announced but never used in the workflow.', 'announcement')
add('Successful reassignment', observations(), True, False, False,
    'AI releases task time; valuable new assignments absorb all released hours.', 'absorption')
add('Demand absorbs released capacity', observations(output=150, comparator_output=150), True, False, False,
    'Firm and comparator both expand output using spare capacity. No AI-attributable reduction versus the stipulated counterfactual.', 'absorption')
add('AI-linked layoffs', observations(hours=70), True, True, False,
    'AI reduces the human hours required for unchanged service output; payroll roles are cut.', 'direct displacement')
add('Attrition and non-replacement', observations(hours=80), True, True, False,
    'No dismissals occur. Departing employees are not replaced because AI performs their work.', 'attrition')
add('Suppressed hiring during growth', observations(hours=110, output=150, comparator_hours=150, comparator_output=150), True, True, False,
    'Hours grow 10%, but without AI they would have grown 50% for the stipulated workload.', 'hiring')
add('Demand slump alongside AI', observations(hours=70, output=70, comparator_hours=70, comparator_output=70), True, False, False,
    'AI changes tasks; remaining tasks absorb released time. A demand contraction causes the observed hours reduction.', 'demand')
o = observations(); o['workforce']['employee_hours_after'] = 70; o['workforce']['contractor_hours_after'] = 30
add('Outsourcing disguises unchanged human work', o, True, False, False,
    'Tasks change with AI, but 30 employee-hour units move to contractors. Total paid human hours remain 100.', 'outsourcing')
add('Retained spare capacity', observations(), True, False, False,
    'Management continues paying for released hours. Within the observation horizon no labor outcome has occurred.', 'lag')
add('Expertise premium erodes', observations(wage=75), True, False, True,
    'AI provides diagnosis. Humans still execute the work for the same hours but receive lower real hourly pay.', 'wages')
add('Hours and wages both contract', observations(hours=70, wage=80), True, True, True,
    'AI substitutes for some work and reduces the scarcity premium on the remainder.', 'combined')
ambiguous = observations(hours=80, comparison=False)
add('Ambiguous history A: AI caused the reduction', copy.deepcopy(ambiguous), True, True, False,
    'AI is the true cause, but no credible comparison is observable.', 'identification')
add('Ambiguous history B: another reorganization caused it', copy.deepcopy(ambiguous), True, False, False,
    'An undisclosed preplanned reorganization is the true cause. Visible records match history A exactly.', 'identification')
hidden = observations(hours=70)
add('Apparently convincing but invalid comparison', hidden, True, False, False,
    'A hidden firm-specific reorganization reduces hours. The comparator looks valid in available records, but its counterfactual is wrong. The indicator should be exposed as fallible.', 'hidden confounding')
o = observations(hours=80); o['alternative_explanations'] = ['independent reorganization not separated from AI']
add('Known competing explanation', o, True, False, False,
    'A documented reorganization explains the hours reduction; attribution is unresolved from the observations.', 'known confounding')

predictions = [{'id': c['id'], 'name': c['name'], **classify(c['observations'])} for c in cases]

# Evidence loss is not economic randomness. Random masks make no claim about
# how frequently these reporting defects occur in reality.
variants = []
mask_types = ['none', 'missing_comparison', 'missing_contractors', 'missing_task_record',
              'bad_extraction', 'unknown_quality', 'unknown_task_mix', 'bad_timing']
rng = random.Random(42)
for c in cases:
    for trial in range(40):
        o = copy.deepcopy(c['observations'])
        mask = rng.choice(mask_types)
        if mask == 'missing_comparison': o['comparison']['available'] = False
        elif mask == 'missing_contractors': o['workforce']['covers_employees_and_contractors'] = False
        elif mask == 'missing_task_record': o['task_execution_evidence']['available'] = False
        elif mask == 'bad_extraction': o['coverage']['extraction_valid'] = False
        elif mask == 'unknown_quality': o['production']['quality_comparable'] = False
        elif mask == 'unknown_task_mix': o['production']['task_mix_comparable'] = False
        elif mask == 'bad_timing': o['timing']['ai_precedes_workforce_change'] = False
        variants.append({'id': f"{c['id']}-V{trial+1:02d}", 'parent': c['id'],
                         'mask': mask, 'observations': o, 'indicator': classify(o)})

assert cases[12]['observations'] == cases[13]['observations']
assert classify(cases[12]['observations']) == classify(cases[13]['observations'])
assert predictions[6]['employment'] == 'displacement supported'  # Growth can conceal displacement.
assert predictions[7]['employment'] == 'not established at threshold'  # Demand contraction.
assert predictions[8]['employment'] == 'not established at threshold'  # Outsourcing.
assert predictions[10]['wages'] == 'erosion supported' and predictions[10]['employment'] == 'not established at threshold'
assert predictions[14]['employment'] == 'displacement supported' and not cases[14]['truth']['employment_displaced_by_ai']
assert all(v['indicator']['level'] != 'Level 2 support' for v in variants if v['mask'] != 'none')

def write(name, data):
    (OUT/name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
write('observable-evidence.json', [{'id':c['id'], 'observations':c['observations']} for c in cases])
write('ground-truth.json', [{'id':c['id'], 'name':c['name'], 'family':c['family'], **c['truth']} for c in cases])
write('indicator-results.json', predictions)
write('evidence-loss-experiments.json', variants)

from collections import Counter
counts = Counter(v['indicator']['level'] for v in variants)
rows = '\n'.join(f"| {c['id']} | {c['name']} | {'Yes' if c['truth']['employment_displaced_by_ai'] else 'No'} | {p['level']}: {p['employment']}; {p['wages']} |" for c,p in zip(cases,predictions))
report = f'''# Synthetic evidence experiment — version 0.1

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
{rows}

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

Results: {dict(counts)}.

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
'''
(OUT/'Findings-and-rules.md').write_text(report, encoding='utf-8')
print(json.dumps({'cases':len(cases), 'stress_records':len(variants), 'stress_results':dict(counts),
                  'designed_false_positive':predictions[14], 'report':str(OUT/'Findings-and-rules.md')}, indent=2))
