#!/usr/bin/env python3
"""Offline final-only analysis of the full eligibility sweep; no study pooling."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

DEFAULT = Path(__file__).resolve().parents[1] / 'research/groq_full_scope_20261119'
ARMS = ('source', 'verified_setup', 'context_setup')
TERMINAL = frozenset(('completed', 'quality_gate_failed', 'extraction_failure',
                      'test_failure', 'target_not_reached', 'replay_failure',
                      'execution_timeout', 'execution_error'))
BOOTSTRAPS, RANDOM_SEED = 20000, 20261119
CONTRASTS = (('context_setup', 'source'), ('verified_setup', 'source'),
             ('context_setup', 'verified_setup'))
ENDPOINT = ('Runner accepted boolean: exactly three tests, static gate, all tests pass, '
            'target-body witness, and successful same-line replay. The analyzer trusts '
            'the runner attestation; aggregate rows cannot independently audit these gates.')
LIMITATIONS = [
    'Projects are assumed independent; shared dependencies and fixed eligibility selection limit generalization.',
    'Sign-flip inference requires independent project-effect sign exchangeability/symmetry under the null; pairing alone does not establish it.',
    'Percentile project-cluster bootstrap intervals can have limited coverage with few clusters, discrete outcomes, or heterogeneous projects. They are marginal 95% intervals, not simultaneous intervals.',
    'Seeds and target symbols are repetitions within projects, not independent project samples. With one project inference is unavailable.',
    'Acceptance is conditional on the runner oracle and environment; passing generated assertions does not prove semantic correctness or full Test4Py efficacy.',
    'All 21 projects were already observed; 584 of 645 target symbols were not in the earlier 61 normalized trials. These are not new held-out projects. No older outcomes are pooled.',
    'No significance, power, or sample sufficiency is promised. Module-line coverage is descriptive, not target-body coverage.',
]


def validate(manifest, summary):
    """Reject incomplete products and infrastructure outcomes before any inference."""
    if len(manifest['arms']) != 3 or set(manifest['arms']) != set(ARMS):
        raise ValueError('Expected the three full-scope arms')
    seeds = manifest['seed_values']
    if seeds != [71, 72]:
        raise ValueError('Expected seed_values [71, 72]')
    targets = {}
    for target in manifest['targets']:
        if any(not isinstance(target[k], str) or not target[k] for k in ('id', 'project', 'module')):
            raise ValueError('Invalid target identity')
        if target['id'] in targets:
            raise ValueError('Duplicate target')
        targets[target['id']] = target
    if not targets:
        raise ValueError('Empty targets')
    expected = {(tid, seed, arm) for tid in targets for seed in seeds for arm in ARMS}
    n = len(expected)
    if type(manifest['planned']) is not int or manifest['planned'] != n:
        raise ValueError('Manifest planned count differs from Cartesian product')
    indexed = {}
    for row in summary['rows']:
        if type(row['seed']) is not int:
            raise ValueError('Invalid seed')
        key = row['target_id'], row['seed'], row['arm']
        if key not in expected or key in indexed:
            raise ValueError('Unexpected or duplicate attempt')
        target = targets[row['target_id']]
        if any(row[k] != target[k] for k in ('project', 'module')):
            raise ValueError('Project/module identity mismatch')
        if type(row.get('accepted')) is not bool:
            raise ValueError('Acceptance must be boolean')
        if row.get('status') not in TERMINAL:
            raise ValueError('Unresolved/infrastructure status: ' + str(row.get('status')))
        if row['accepted'] and row['status'] != 'completed':
            raise ValueError('Accepted outcome must be completed')
        line = row.get('line_pct')
        if line is not None and (type(line) not in (int, float) or not math.isfinite(line) or not 0 <= line <= 100):
            raise ValueError('Invalid module line percentage')
        if row['accepted'] and line is None:
            raise ValueError('Accepted outcome needs module line percentage')
        indexed[key] = row
    if (set(indexed) != expected or any(type(summary.get(k)) is not int or summary[k] != n
                                      for k in ('planned', 'completed'))):
        raise ValueError('Incomplete sweep; no final inference')
    return targets, indexed


def exact_signflip(effects, chunk_size=65536):
    """Two-sided exact project sign test of the mean, including ties and zeros."""
    effects = np.asarray(effects, dtype=float)
    if effects.ndim != 1 or not 1 <= effects.size <= 21 or not np.isfinite(effects).all():
        raise ValueError('Need 1 to 21 finite project effects')
    if chunk_size < 1:
        raise ValueError('Positive chunk size required')
    n = effects.size
    observed = abs(effects.sum())
    tolerance = 64 * np.finfo(float).eps * max(1., np.abs(effects).sum())
    exceed = 0
    shifts = np.arange(n, dtype=np.uint64)
    for start in range(0, 1 << n, chunk_size):
        assignments = np.arange(start, min(start + chunk_size, 1 << n), dtype=np.uint64)
        signs = ((assignments[:, None] >> shifts) & 1).astype(float) * 2 - 1
        sums = np.sum(signs * effects, axis=1)
        exceed += int(np.count_nonzero(np.abs(sums) >= observed - tolerance))
    return exceed / (1 << n)


def holm(pvalues):
    """Adjusted p-values in original order, for exactly the secondary family."""
    if len(pvalues) != 2 or any(not math.isfinite(p) or not 0 <= p <= 1 for p in pvalues):
        raise ValueError('Two secondary p-values required')
    order = sorted(range(2), key=lambda i: pvalues[i])
    result = [0., 0.]
    result[order[0]] = min(1., 2 * pvalues[order[0]])
    result[order[1]] = max(result[order[0]], pvalues[order[1]])
    return result


def analyze(manifest, summary):
    targets, rows = validate(manifest, summary)
    projects = sorted({t['project'] for t in targets.values()})
    if len(projects) > 21:
        raise ValueError('At most 21 project clusters supported')
    per_project = {}
    for project in projects:
        tids = [tid for tid, t in targets.items() if t['project'] == project]
        arms = {}
        for arm in ARMS:
            selected = [rows[tid, seed, arm] for tid in tids for seed in manifest['seed_values']]
            successes = sum(r['accepted'] for r in selected)
            arms[arm] = dict(successes=successes, denominator=len(selected),
                acceptance_rate=successes / len(selected),
                penalized_module_line_pct=sum(r['line_pct'] if r['accepted'] else 0 for r in selected) / len(selected),
                status_counts={s: sum(r['status'] == s for r in selected) for s in sorted(TERMINAL)})
        per_project[project] = dict(targets=len(tids), arms=arms)
    rates = np.array([[per_project[p]['arms'][a]['acceptance_rate'] for a in ARMS] for p in projects])
    indices = np.random.default_rng(RANDOM_SEED).integers(0, len(projects), (BOOTSTRAPS, len(projects)))
    contrasts = {}
    for i, (treatment, control) in enumerate(CONTRASTS):
        effects = rates[:, ARMS.index(treatment)] - rates[:, ARMS.index(control)]
        infer = len(projects) >= 2
        contrasts[treatment + '-' + control] = dict(role='primary' if i == 0 else 'secondary',
            difference=float(effects.mean()),
            project_differences=dict(zip(projects, effects.tolist())),
            percentile_95=np.quantile(effects[indices].mean(axis=1), [.025, .975]).tolist() if infer else None,
            exact_signflip_two_sided_p=exact_signflip(effects) if infer else None,
            sign_assignments=2 ** len(projects) if infer else None)
    secondary = list(contrasts.values())[1:]
    adjusted = holm([c['exact_signflip_two_sided_p'] for c in secondary]) if len(projects) >= 2 else [None, None]
    for c, p in zip(secondary, adjusted):
        c['holm_adjusted_p'] = p
    arms = {}
    for arm in ARMS:
        selected = [r for r in rows.values() if r['arm'] == arm]
        arms[arm] = dict(successes=sum(r['accepted'] for r in selected), denominator=len(selected),
            equal_project_acceptance_rate=float(rates[:, ARMS.index(arm)].mean()),
            equal_project_penalized_module_line_pct=float(np.mean([per_project[p]['arms'][arm]['penalized_module_line_pct'] for p in projects])),
            pooled_penalized_module_line_pct_descriptive=sum(r['line_pct'] if r['accepted'] else 0 for r in selected) / len(selected))
    return dict(scope='New full eligibility sweep only; no pooling of prior studies.',
        manifest_provenance=manifest.get('provenance'), manifest_scope=manifest.get('scope'),
        endpoint=ENDPOINT, final=True, planned=manifest['planned'], completed=len(rows),
        target_count=len(targets), project_count=len(projects), paired_target_seed_count=len(rows)//3,
        estimand='Equal-project mean of within-project paired target/seed acceptance differences.',
        coverage_definition='Module-line percentage times acceptance; rejected attempts contribute zero, denominator includes every planned attempt. Not target-body coverage.',
        bootstrap=dict(replicates=BOOTSTRAPS, seed=RANDOM_SEED, method='Paired project-cluster percentile 95%; common project resamples across arms and contrasts; linear quantiles', numpy_version=np.__version__),
        multiplicity='Primary context_setup-source is separate. Holm correction applies only to the two secondary acceptance p-values; coverage is descriptive.',
        arms=arms, contrasts=contrasts, per_project=per_project, limitations=LIMITATIONS)


def markdown(out):
    lines = ['# Full eligibility sweep statistics', '', out['scope'], '', out['endpoint'], '',
             f"Final complete Cartesian product: {out['completed']}/{out['planned']} attempts; {out['target_count']} targets; {out['project_count']} projects.",
             out['estimand'], out['coverage_definition'], out['multiplicity'], '',
             'Bootstrap: 20,000 paired project resamples, seed 20261119. Differences are proportions; line percentages are on a 0–100 scale.', '',
             '| Contrast | Role | Difference | Marginal 95% CI | Exact two-sided p | Holm p |',
             '|---|---|---:|---|---:|---:|']
    for name, c in out['contrasts'].items():
        lines.append(f"| {name} | {c['role']} | {c['difference']:.6f} | {c['percentile_95']} | {c['exact_signflip_two_sided_p']} | {c.get('holm_adjusted_p', 'not in family')} |")
    lines += ['', '| Arm | Accepted / denominator | Equal-project rate | Equal-project penalized module-line % |', '|---|---:|---:|---:|']
    for a, r in out['arms'].items():
        lines.append(f"| {a} | {r['successes']}/{r['denominator']} | {r['equal_project_acceptance_rate']:.6f} | {r['equal_project_penalized_module_line_pct']:.6f} |")
    lines += ['', '| Project | Arm | Accepted / denominator | Penalized module-line % |', '|---|---|---:|---:|']
    for p, record in out['per_project'].items():
        for a, r in record['arms'].items():
            lines.append(f"| {p} | {a} | {r['successes']}/{r['denominator']} | {r['penalized_module_line_pct']:.6f} |")
    lines += ['', 'Manifest scope: ' + json.dumps(out['manifest_scope']),
              'Manifest provenance: ' + json.dumps(out['manifest_provenance']), '',
              *['- ' + s for s in out['limitations']], '',
              'Input SHA-256: ' + json.dumps(out['input_sha256']), '']
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, default=DEFAULT)
    args = parser.parse_args(argv)
    try:
        inputs = {name: (args.study / name).read_bytes() for name in ('manifest.json', 'summary.json')}
        out = analyze(*(json.loads(inputs[name]) for name in ('manifest.json', 'summary.json')))
        out['input_sha256'] = {name: hashlib.sha256(data).hexdigest() for name, data in inputs.items()}
        serialized = json.dumps(out, indent=2, allow_nan=False) + '\n'
        report = markdown(out)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Refusing final inference; no output written: {exc}\n')
    # All validation and rendering precede writes. Never publish interim inference.
    for name in ('stats.json', 'statistics.json'):
        (args.study / name).write_text(serialized)
    (args.study / 'STATISTICS.md').write_text(report)
    print(f'Wrote final stats.json, statistics.json and STATISTICS.md in {args.study}')


if __name__ == '__main__':
    main()
