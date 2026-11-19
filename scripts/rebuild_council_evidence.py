#!/usr/bin/env python3
"""Offline, append-only Council evidence rebuild. JSON is the document-writer interface."""
import csv
import hashlib
import json
import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research/reviews/council_sota_20261118/restored'
SOTA = Path('curated_benchmark_results/sota_council_results')


def main():
    manifest = {}

    def artifact(path):
        path = Path(path)
        if not path.is_absolute():
            path = ROOT / path
        path = path.resolve()
        key = path.relative_to(ROOT).as_posix()
        if key not in manifest:
            manifest[key] = {'path': key, 'exists': path.is_file(),
                             'sha256': hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None}
        return key

    def read_csv(path):
        artifact(path)
        with (ROOT / path).open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def reconstruct(row, directory, stages, source, number):
        evidence = []
        for stage, name in enumerate(stages):
            p = directory / name / 'evaluation.json'
            if p.is_file():
                key = artifact(p)
                if (p.parent / 'test_run.py').is_file():
                    artifact(p.parent / 'test_run.py')
                value = json.loads(p.read_text())
                if not isinstance(value.get('suite_pass'), bool):
                    raise ValueError(f'Invalid suite_pass: {p}')
                evidence.append((stage, key, value))
        first = evidence[0][2]['suite_pass'] if evidence and evidence[0][0] == 0 else None
        winner = next((e for e in evidence if e[2]['suite_pass']), None)
        final = winner or (evidence[-1] if evidence else None)
        # Missing evaluation retains an explicitly labelled CSV outcome, never a verified outcome.
        passed = final[2]['suite_pass'] if final else row['final_pass'].lower() == 'true'
        measured = {k: final[2].get(k) if final else None for k in ('line_pct', 'branch_pct')}
        result = dict(target_id=row['target_id'], project=row['project'], seed=int(row['seed']),
                      arm=row.get('config') or row['arm'], source_csv=source, source_row=number,
                      source_final_code_path=row.get('final_code_path') or None,
                      final_pass=passed, first_pass=first,
                      repair_round=winner[0] if winner and first is False else None,
                      evaluation_verified=final is not None,
                      outcome_source='evaluation' if final else 'csv_only',
                      evaluations=[{'stage': e[0], 'path': e[1]} for e in evidence],
                      final_evaluation=final[1] if final else None,
                      measured_coverage=measured,
                      penalized_coverage={k: (v if passed else 0.0) for k, v in measured.items()},
                      latency_sec_csv=float(row['latency_sec']),
                      missingness=[])
        if not evidence:
            result['missingness'].append('no_evaluation; CSV-only outcome')
            artifact(directory / stages[0] / 'evaluation.json')
        if first is None:
            result['missingness'].append('first_evaluation_missing; repair attribution unknown')
        if not row.get('final_code_path'):
            result['missingness'].append('source_code_path_missing')
        elif not Path(row['final_code_path']).is_file():
            result['missingness'].append('source_code_file_missing')
        else:
            artifact(row['final_code_path'])
        if passed and any(v is None for v in measured.values()):
            result['missingness'].append('passing_coverage_missing')
        result['csv_disagreements'] = {}
        for key, actual in [('final_pass', passed), ('first_pass', first)]:
            if actual is not None and (row[key].lower() == 'true') != actual:
                result['csv_disagreements'][key] = {'csv': row[key], 'evaluation': actual}
        for key, value in measured.items():
            if passed and value is not None and abs(float(row[key]) - value) > .011:
                result['csv_disagreements'][key] = {'csv': float(row[key]), 'evaluation': value}
        return result

    def summarize(rows):
        n = len(rows)
        repairs = Counter(r['repair_round'] for r in rows if r['repair_round'])
        def mean(values):
            values = [v for v in values if v is not None]
            return sum(values) / len(values) if values else None
        return dict(n=n, passed=sum(r['final_pass'] for r in rows),
                    pass_rate_pct=100 * sum(r['final_pass'] for r in rows) / n,
                    first_pass=sum(r['first_pass'] is True for r in rows),
                    repairs=sum(repairs.values()), repairs_by_round=dict(sorted(repairs.items())),
                    evaluation_verified=sum(r['evaluation_verified'] for r in rows),
                    rows_with_missingness=sum(bool(r['missingness']) for r in rows),
                    missingness_counts=dict(Counter(m for r in rows for m in r['missingness'])),
                    rows_with_csv_disagreements=sum(bool(r['csv_disagreements']) for r in rows),
                    coverage={k: {'penalized_mean_pct': mean(r['penalized_coverage'][k] for r in rows),
                                  'penalized_known_n': sum(r['penalized_coverage'][k] is not None for r in rows),
                                  'measured_mean_pct': mean(r['measured_coverage'][k] for r in rows),
                                  'measured_n': sum(r['measured_coverage'][k] is not None for r in rows)}
                              for k in ('line_pct', 'branch_pct')},
                    latency_mean_sec_csv=mean(r['latency_sec_csv'] for r in rows))

    artifact('research/reviews/council_sota_20261118/REVIEW.md')
    artifact(Path(__file__))
    cohorts = {}
    source = (SOTA / 'trials_raw_sota_21targets.csv').as_posix()
    original_csv = read_csv(source)
    original = [reconstruct(r, ROOT / SOTA / 'runs' / r['target_id'] / f"seed_{r['seed']}",
                            ['eval_v1', 'eval_repair_r1', 'eval_repair_r2'], source, i)
                for i, r in enumerate(original_csv, 2)]
    cohorts['sota_original'] = original
    refined_source = 'monograph_final_deliverables/data/trials_raw_sota_21targets_refined.csv'
    refined_csv = read_csv(refined_source)
    refined = []
    for i, r in enumerate(refined_csv, 2):
        directory = ROOT / SOTA / 'runs_refined' / r['target_id'] / f"seed_{r['seed']}"
        if directory.is_dir():
            refined.append(reconstruct(r, directory, ['eval_v1', 'eval_r1', 'eval_r2'], refined_source, i))
    cohorts['sota_refined_only'] = refined
    replacements = {(r['target_id'], r['seed']): r for r in refined}
    cohorts['sota_after_refinement'] = [replacements.get((r['target_id'], r['seed']), r) for r in original]
    for source in ['curated_benchmark_results/trials_raw_curated_21targets.csv',
                   'standardized_research_artifacts/ablation_study_results.csv']:
        for i, r in enumerate(read_csv(source), 2):
            ablation = 'ablation' in source
            directory = (ROOT / 'standardized_research_artifacts/ablation_runs' / r['target_id'] / r['config']
                         if ablation else Path(r['final_code_path']).parent if r['final_code_path'] else ROOT / '__missing__')
            key = ('ablation_' if ablation else 'control_') + (r.get('config') or r['arm'])
            cohorts.setdefault(key, []).append(reconstruct(r, directory, ['v1_exec', 'v2_exec'], source, i))
    result = dict(schema_version=1, consumer='Parent document writer: consume cohorts.*.summary and per_target; cite manifest SHA256 and validation.md.',
                  policies=['Offline reconstruction; no API or benchmark execution.',
                            'Original and refined-only executions remain separate. After-refinement is a mixed development cohort, not a locked protocol.',
                            'Failure coverage penalty is zero; absent measured coverage remains null. Means include known values only; consult denominators.',
                            'Latency is CSV provenance only; refined rows may retain old latency/code metadata.',
                            'Seed is a repetition label, not verified inference seeding. Missing evidence is not verified failure.',
                            'Repair attribution follows first successful evaluation; no claim of oracle preservation.'],
                  cohorts={key: {'summary': summarize(rows),
                                 'per_target': {t: summarize([r for r in rows if r['target_id'] == t]) for t in sorted({r['target_id'] for r in rows})},
                                 'rows': rows} for key, rows in cohorts.items()})
    checks = []
    for key, expected in [('sota_original', (105, 96, 67, 29)), ('sota_after_refinement', (105, 98, 70, 28)),
                          ('ablation_full_method', (6, 5, None, None))]:
        s = result['cohorts'][key]['summary']
        actual = tuple(s[k] for k in ['n', 'passed', 'first_pass', 'repairs'])
        checks.append({'cohort': key, 'expected': expected, 'actual': actual,
                       'ok': all(e is None or e == a for e, a in zip(expected, actual))})
    for key, expected in [('sota_original', {1: 24, 2: 5}), ('sota_after_refinement', {1: 22, 2: 6})]:
        actual = result['cohorts'][key]['summary']['repairs_by_round']
        checks.append({'cohort': key, 'expected_rounds': expected, 'actual_rounds': actual, 'ok': actual == expected})
    for key, rows in cohorts.items():
        identities = [(r['target_id'], r['seed'], r['arm']) for r in rows]
        if len(identities) != len(set(identities)):
            raise ValueError(f'Duplicate trial identities: {key}')
    result['validation'] = checks
    result['manifest'] = [manifest[k] for k in sorted(manifest)]
    OUT.mkdir(parents=True, exist_ok=True)
    # Versioned directories keep every previous rebuild immutable, including repeated runs.
    import tempfile
    destination = Path(tempfile.mkdtemp(prefix='rebuild_', dir=OUT))
    summary = destination / 'summary.json'
    summary.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
    lines = ['# Council evidence validation', '',
             f'[Machine-readable summary](summary.json) — SHA256 `{hashlib.sha256(summary.read_bytes()).hexdigest()}`', '',
             '| Cohort | N | Pass | First pass | Repairs | Rounds | Verified | Missing rows |',
             '|---|---:|---:|---:|---:|---|---:|---:|']
    for key, cohort in result['cohorts'].items():
        s = cohort['summary']
        lines.append(f"| {key} | {s['n']} | {s['passed']} | {s['first_pass']} | {s['repairs']} | {s['repairs_by_round']} | {s['evaluation_verified']} | {s['rows_with_missingness']} |")
    lines += ['', '## Policies', ''] + ['- ' + p for p in result['policies']]
    lines += ['', '## Validation', ''] + [f"- {'PASS' if c['ok'] else 'FAIL'}: {c}" for c in checks]
    lines += ['', '## Missingness and CSV disagreements', '']
    for key, cohort in result['cohorts'].items():
        for r in cohort['rows']:
            if r['missingness'] or r['csv_disagreements']:
                lines.append(f"- {key}/{r['target_id']}/{r['seed']}: {r['missingness']}; disagreements: {r['csv_disagreements']}")
    lines += ['', '## Source artifact hashes', '']
    for item in result['manifest']:
        link = os.path.relpath(ROOT / item['path'], destination)
        lines.append(f"- [{item['path']}]({link}): `{item['sha256']}`")
    (destination / 'validation.md').write_text('\n'.join(lines) + '\n')
    for item in result['manifest']:
        if item['exists'] and hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise RuntimeError(f"Source changed during rebuild: {item['path']}")
    print(summary.relative_to(ROOT))
    if not all(c['ok'] for c in checks):
        raise SystemExit('Audit expectation mismatch; see validation.md')


if __name__ == '__main__':
    main()
