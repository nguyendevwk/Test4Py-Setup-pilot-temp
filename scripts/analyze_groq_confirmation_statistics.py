#!/usr/bin/env python3
"""Post-hoc project-cluster statistics for the completed confirmation only.

No API calls, runner imports, pilot pooling, or interim inference. Differences
are verified setup minus source, averaged within project over target/seed pairs,
then equally across projects. Project independence is an assumption.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from statistics import NormalDist

import numpy as np

DEFAULT = Path(__file__).resolve().parents[1] / 'research/groq_confirmation_20261118'
SOURCE, VERIFIED = 'atomic_source', 'atomic_verified_setup'
BOOTSTRAPS, RANDOM_SEED = 20000, 20261118


def validate(manifest, summary):
    """Require the exact planned Cartesian product, not merely matching counts."""
    if set(manifest['arms']) != {SOURCE, VERIFIED} or len(manifest['arms']) != 2:
        raise ValueError('Expected atomic_source versus atomic_verified_setup')
    targets = {t['id']: t for t in manifest['targets']}
    if len(targets) != len(manifest['targets']) or not targets:
        raise ValueError('Empty or duplicate targets')
    seeds = manifest['seed_values']
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError('Empty or duplicate seeds')
    expected = {(tid, seed, arm) for tid in targets for seed in seeds for arm in (SOURCE, VERIFIED)}
    if manifest['planned'] != len(expected):
        raise ValueError('Manifest planned count mismatch')
    rows = summary['rows']
    indexed = {}
    for row in rows:
        key = (row['target_id'], row['seed'], row['arm'])
        if key not in expected or key in indexed:
            raise ValueError('Unexpected or duplicate attempt')
        if row['project'] != targets[row['target_id']]['project']:
            raise ValueError('Project identity mismatch')
        if type(row.get('accepted')) is not bool:
            raise ValueError('Missing/nonboolean acceptance')
        status = row.get('status', '')
        if status not in {'completed', 'quality_gate_failed', 'test_failure', 'target_not_reached'}:
            raise ValueError('Unresolved/infrastructure attempt: ' + status)
        if row['accepted'] and status != 'completed':
            raise ValueError('Accepted attempt lacks completed status')
        indexed[key] = row
    if (set(indexed) != expected or summary.get('completed') != len(expected)
            or summary.get('planned') != len(expected)):
        raise ValueError(f'Incomplete confirmation: {len(indexed)}/{len(expected)} rows; no interim inference')
    return targets, seeds, indexed


def wilson(successes, n):
    z = NormalDist().inv_cdf(.975)
    p = successes / n
    center = (p + z*z/(2*n))/(1 + z*z/n)
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))/(1 + z*z/n)
    return [center-half, center+half]


def ratio(a, b):
    return float(a / b) if b > 0 else None


def sensitivity(pairs_per_project):
    z = NormalDist().inv_cdf(.975) + NormalDist().inv_cdf(.8)
    out = []
    for effect in (.05, .10, .15):
        for discordance in (.25, .50):
            n = math.ceil(z*z*(discordance-effect*effect)/(effect*effect))
            for icc in (0, .10, .30):
                de = 1 + (pairs_per_project-1)*icc
                out.append(dict(difference=effect, discordance=discordance, ICC=icc,
                                pairs_per_project=pairs_per_project, design_effect=de,
                                independent_pairs_normal_approx=n,
                                projects_design_effect_approx=math.ceil(n*de/pairs_per_project)))
    return out


def analyze_group(manifest, summary):
    targets, seeds, rows = validate(manifest, summary)
    projects = sorted({t['project'] for t in targets.values()})
    if not 1 <= len(projects) <= 20:
        raise ValueError('Exact enumeration requires 1 to 20 project clusters')
    per_project = {}
    for project in projects:
        tids = sorted(tid for tid, t in targets.items() if t['project'] == project)
        pairs = [(rows[tid, seed, SOURCE], rows[tid, seed, VERIFIED]) for tid in tids for seed in seeds]
        source = np.array([a['accepted'] for a, b in pairs], dtype=float)
        verified = np.array([b['accepted'] for a, b in pairs], dtype=float)
        statuses = {arm: {} for arm in (SOURCE, VERIFIED)}
        for pair in pairs:
            for row in pair:
                counts = statuses[row['arm']]
                counts[row['status']] = counts.get(row['status'], 0) + 1
        per_project[project] = dict(targets=len(tids), paired_attempts=len(pairs),
            source_successes=int(source.sum()), verified_successes=int(verified.sum()),
            source_rate=float(source.mean()), verified_rate=float(verified.mean()),
            paired_difference=float((verified-source).mean()),
            relative_risk=ratio(verified.mean(), source.mean()),
            discordant_verified_only=int(((verified == 1) & (source == 0)).sum()),
            discordant_source_only=int(((verified == 0) & (source == 1)).sum()),
            both_accepted=int(((verified == 1) & (source == 1)).sum()),
            neither_accepted=int(((verified == 0) & (source == 0)).sum()),
            missing_attempts=0, status_counts=statuses)
    a = np.array([per_project[p]['source_rate'] for p in projects])
    b = np.array([per_project[p]['verified_rate'] for p in projects])
    effects = b-a
    observed = float(effects.mean())
    rng = np.random.default_rng(RANDOM_SEED)
    indices = rng.integers(0, len(projects), size=(BOOTSTRAPS, len(projects)))
    boot_a, boot_b = a[indices].mean(axis=1), b[indices].mean(axis=1)
    interval = np.quantile(boot_b-boot_a, [.025, .975]).tolist()
    # Preserve undefined RR draws rather than conditioning an interval on positive baselines.
    undefined = int((boot_a == 0).sum())
    rr_ci = None if undefined else np.quantile(boot_b/boot_a, [.025, .975]).tolist()
    exceed = sum(abs(float(np.mean(effects*np.array(signs)))) >= abs(observed)-1e-12
                 for signs in itertools.product((-1, 1), repeat=len(projects)))
    arms = {}
    for arm in (SOURCE, VERIFIED):
        arm_rows = [r for r in rows.values() if r['arm'] == arm]
        n, k = len(arm_rows), sum(r['accepted'] for r in arm_rows)
        arms[arm] = dict(successes=k, attempts=n, rate=k/n, wilson_95_descriptive=wilson(k, n),
                         limitation='Attempt-level Wilson interval ignores within-project dependence; not inferential.')
    return dict(scope='Post-hoc analysis of completed confirmation only; no pilot/development pooling.',
        endpoint='Runner accepted boolean, unchanged; not full Test4Py efficacy or oracle correctness.',
        contrast='atomic_verified_setup minus atomic_source',
        estimand='Equal-project mean of within-project target/seed paired acceptance differences.',
        independent_unit='project (assumed independent); seeds and targets are not independent projects',
        independent_projects=len(projects), target_count=len(targets), paired_attempts=len(rows)//2,
        bootstrap=dict(method='Paired project-cluster resampling, percentile 95%, numpy linear quantiles',
                       replicates=BOOTSTRAPS, seed=RANDOM_SEED, numpy_version=np.__version__),
        equal_project_source_rate=float(a.mean()), equal_project_verified_rate=float(b.mean()),
        difference=observed, difference_percentile_95=interval,
        relative_risk=ratio(b.mean(), a.mean()), relative_risk_percentile_95=rr_ci,
        relative_risk_undefined_bootstrap_draws=undefined,
        relative_risk_NA_rule='NA when source rate is zero; CI NA if any bootstrap denominator is zero.',
        exact_cluster_signflip_two_sided_p=exceed/(2**len(projects)),
        exact_cluster_signflip_assignments=2**len(projects),
        nonzero_effect_clusters=int((effects != 0).sum()),
        minimum_attainable_two_sided_p_bound= min(1., 2/(2**int((effects != 0).sum()))),
        signflip_assumption='Exact enumeration under independent project-effect sign exchangeability/symmetry under null; not guaranteed by pairing alone.',
        missingness=dict(planned_attempts=manifest['planned'], observed_attempts=len(rows), missing_attempts=0,
                         expected_target_slots=manifest.get('expected_target_slots'),
                         pre_inference_missing_target_slots=manifest.get('missing_target_slots'),
                         scope='Excluded project/target slots are not model failures; inference covers eligible projects only.'),
        arms=arms, per_project=per_project,
        discordant_pairs={k: sum(p[k] for p in per_project.values()) for k in
                          ('discordant_verified_only', 'discordant_source_only', 'both_accepted', 'neither_accepted')},
        sample_size_sensitivity=sensitivity(len(rows)/2/len(projects)),
        limitations=['Post-hoc statistical analysis, not a prospectively registered inference plan.',
                    'Nine project clusters give limited precision; percentile bootstrap may be poorly calibrated.',
                    'Project selection and shared ecosystem dependencies limit generalization and independence.',
                    'Wilson intervals and raw discordance counts are descriptive; no independent-pair p-value.',
                    'Sensitivity uses paired binary normal approximation, alpha .05 two-sided, power .80, assumed discordance and exchangeable within-project ICC.',
                    'Design-effect project counts are approximate, with balanced cluster size assumed; not a small-cluster power calculation.',
                    'No guaranteed significance, observed-power claim, or proof that this sample is sufficient.'])



def analyze(manifest, summary):
    # Validate the full ITT set before examining any stratum; never salvage interim data.
    targets, seeds, rows = validate(manifest, summary)
    for target in targets.values():
        if type(target.get('setup_probe', {}).get('accepted')) is not bool:
            raise ValueError('Missing pre-inference boolean setup_probe.accepted')
    out = analyze_group(manifest, summary)
    out['analysis_role'] = 'Primary comparison: ITT-style assignment contrast across all eligible targets, regardless of probe acceptance; post-hoc statistical plan.'
    out['stratification'] = dict(
        basis='Manifest setup_probe.accepted, measured before model inference; never selected from model outcomes.',
        interpretation='Probe acceptance measures intervention deliverability. When false, no setup hint is appended: treatment and control prompt content are identical; generation seed/order do not constitute a hint intervention.',
        weighting='Within each stratum, target/seed pairs are averaged within project, then projects weighted equally. Stratum effects need not average to the full ITT effect.',
        strata={})
    for delivered, name in ((True, 'probe_accepted_delivered'), (False, 'probe_failed_no_hint')):
        selected = [t for t in targets.values() if t['setup_probe']['accepted'] is delivered]
        ids = {t['id'] for t in selected}
        selected_rows = [r for r in rows.values() if r['target_id'] in ids]
        if not selected:
            result = dict(target_count=0, independent_projects=0, paired_attempts=0,
                          status='empty stratum; no effect or inference', difference=None,
                          difference_percentile_95=None, relative_risk=None,
                          relative_risk_percentile_95=None, exact_cluster_signflip_two_sided_p=None)
        else:
            submanifest = dict(manifest, targets=selected, planned=len(selected_rows))
            submanifest.pop('expected_target_slots', None)
            submanifest.pop('missing_target_slots', None)
            result = analyze_group(submanifest, dict(summary, rows=selected_rows,
                                   planned=len(selected_rows), completed=len(selected_rows)))
            if result['independent_projects'] < 2:
                for field in ('difference_percentile_95', 'relative_risk_percentile_95',
                              'exact_cluster_signflip_two_sided_p'):
                    result[field] = None
                result['inference_note'] = 'One project: descriptive effect only; cluster inference unavailable.'
        result['analysis_role'] = 'Exploratory pre-inference deliverability stratum; not a replacement primary or full-paper claim.'
        result['target_ids'] = sorted(ids)
        out['stratification']['strata'][name] = result
    eligible = sorted({t['project'] for t in targets.values()})
    candidates = sorted({p['project'] for p in manifest.get('projects', [])})
    out['project_selection'] = dict(
        sampled_projects=candidates, sampled_project_count=len(candidates),
        eligible_projects=eligible, eligible_project_count=len(eligible),
        excluded_before_model_inference=sorted(set(candidates)-set(eligible)),
        missing_target_slots=manifest.get('missing_target_slots'),
        explanation='Ten fixed candidate projects, nine eligible under the recorded import-origin criterion. black contributes three pre-inference target slots: loader origins resolve to compiled .so modules, although adjacent .py source files exist. The preparer accepted only .py import origins; it did not force source loading or measure compiled-code coverage. Exclusion preceded model outcomes; do not describe this as absence of source. The original manifest wording is clarified by SOURCE_ELIGIBILITY_CORRECTION.json.',
        scope='Component evaluation using resolved PyPI releases, not the complete Test4Py method or original pinned-paper replication; no full-paper efficacy claim.')
    out['budget_context'] = dict(cumulative_authorized_budget_usd=3,
        user_reported_opening_balance_usd=0.5,
        interpretation='Budget authorization and user-reported opening balance are reconciliation context, not measured API usage, spend, or remaining credit. No usage inferred from these amounts.')
    out['limitations'].append('Delivered-stratum analyses are exploratory, without multiplicity adjustment; no full-paper efficacy claim.')
    return out


def markdown(out):
    def fmt(x):
        return 'NA' if x is None else f'{x:.4f}'
    def ci(x):
        return 'NA' if x is None else '[' + ', '.join(fmt(v) for v in x) + ']'
    lines = ['# Confirmation statistics', '', out['scope'], '',
             f"{out['independent_projects']} project clusters; {out['target_count']} targets; {out['paired_attempts']} paired target/seed repetitions.",
             out['analysis_role'],
             'Independent unit: project. Contrast: verified setup minus source. Acceptance is the unchanged runner endpoint.', '',
             f"Equal-project acceptance difference: {fmt(out['difference'])}; 95% percentile cluster bootstrap CI {ci(out['difference_percentile_95'])}.",
             f"Equal-project relative risk: {fmt(out['relative_risk'])}; 95% cluster bootstrap CI {ci(out['relative_risk_percentile_95'])}.",
             f"Undefined RR bootstrap draws: {out['relative_risk_undefined_bootstrap_draws']}/20000. {out['relative_risk_NA_rule']}",
             f"Exact two-sided project sign-flip p: {fmt(out['exact_cluster_signflip_two_sided_p'])} ({out['exact_cluster_signflip_assignments']} sign assignments).",
             out['signflip_assumption'],
             'Bootstrap: 20,000 paired project resamples; deterministic seed 20261118. Effects are proportions (multiply differences by 100 for percentage points).', '',
             '## Arms (descriptive)', '', '| Arm | Accepted / attempts | Rate | Wilson 95% |', '|---|---:|---:|---|']
    for arm, a in out['arms'].items():
        lines.append(f"| {arm} | {a['successes']} / {a['attempts']} | {fmt(a['rate'])} | {ci(a['wilson_95_descriptive'])} |")
    lines += ['', 'Wilson intervals ignore clustering and must not be used as cluster-aware inference.', '',
              '## Project results', '', '| Project | Pairs | Source | Verified | Difference | RR | Verified only | Source only | Missing |',
              '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p, r in out['per_project'].items():
        lines.append(f"| {p} | {r['paired_attempts']} | {fmt(r['source_rate'])} | {fmt(r['verified_rate'])} | {fmt(r['paired_difference'])} | {fmt(r['relative_risk'])} | {r['discordant_verified_only']} | {r['discordant_source_only']} | 0 |")
    lines += ['', 'Discordant/concordant counts: ' + json.dumps(out['discordant_pairs']), '',
              'Missingness and pre-inference exclusions: ' + json.dumps(out['missingness']), '',
              'Per-project terminal status counts are included in statistics.json.', '',
              '## Prospective sample-size sensitivity (assumptions only)', '',
              '| Difference | Discordance | ICC | Pairs/project | Independent pairs approx. | Projects with design effect approx. |',
              '|---|---:|---:|---:|---:|---:|']
    for r in out['sample_size_sensitivity']:
        lines.append(f"| {r['difference']:.2f} | {r['discordance']:.2f} | {r['ICC']:.2f} | {r['pairs_per_project']:.1f} | {r['independent_pairs_normal_approx']} | {r['projects_design_effect_approx']} |")
    lines += ['', '## Pre-inference intervention deliverability (exploratory)', '',
              out['stratification']['basis'], out['stratification']['interpretation'],
              out['stratification']['weighting'], '',
              '| Probe stratum | Targets | Projects | Pairs | Difference | Cluster 95% CI | RR | RR 95% CI | Sign-flip p |',
              '|---|---:|---:|---:|---:|---|---:|---|---:|']
    for name, r in out['stratification']['strata'].items():
        lines.append(f"| {name} | {r['target_count']} | {r['independent_projects']} | {r['paired_attempts']} | {fmt(r['difference'])} | {ci(r['difference_percentile_95'])} | {fmt(r['relative_risk'])} | {ci(r['relative_risk_percentile_95'])} | {fmt(r['exact_cluster_signflip_two_sided_p'])} |")
    lines += ['', 'Full stratum arms, discordance, per-project results and status counts are in statistics.json. Empty or single-project strata do not support cluster inference.', '',
              '## Project selection and scope', '', out['project_selection']['explanation'],
              out['project_selection']['scope'], '',
              '## Budget reconciliation context', '',
              'Cumulative authorized budget: USD 3. User-reported opening balance: USD 0.50. These are reconciliation context, not API usage or measured spend.', '',
              '## Limitations', ''] + ['- ' + s for s in out['limitations']]
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, default=DEFAULT)
    args = parser.parse_args()
    study = args.study.resolve()
    try:
        manifest_bytes = (study/'manifest.json').read_bytes()
        summary_bytes = (study/'summary.json').read_bytes()
        out = analyze(json.loads(manifest_bytes), json.loads(summary_bytes))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Refusing final inference; no statistics written: {exc}\n')
    out['input_sha256'] = {name: hashlib.sha256(data).hexdigest() for name, data in
                           [('manifest.json', manifest_bytes), ('summary.json', summary_bytes)]}
    report = markdown(out)
    (study/'statistics.json').write_text(json.dumps(out, indent=2, allow_nan=False) + '\n')
    (study/'STATISTICS.md').write_text(report)
    print(f"Wrote statistics.json and STATISTICS.md in {study}")


if __name__ == '__main__':
    main()
