"""One-target development case study; baseline = Council without setup, not Test4Py."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import shutil
import time
import traceback
from types import SimpleNamespace

from pilot.common import BASE, PYCG, checkout, digest, package_versions, reserve_output, write_json
from pilot.setup import extract, select
from pilot.quality import source_context
from pilot.scoring import score, pytest_run, passed_nodes
from council.engine import CouncilEngine
from council.generator import generate_test_with_coder
from council.critic import audit_test_quality, repair_with_critic

SCHEMA_VERSION = 2


def suite_all_pass(process, report):
    tests = report.get('tests', [])
    return bool(tests and not process.get('timeout', False) and process.get('returncode') == 0
        and not report.get('summary', {}).get('errors', 0)
        and not any(c.get('outcome') == 'failed' for c in report.get('collectors', []))
        and all(r.get('outcome') == 'passed' and all(r.get(phase, {}).get('outcome') == 'passed'
                for phase in ('setup', 'call', 'teardown')) for r in tests))


def branch_percentage(record):
    covered, total = record.get('covered_branches'), record.get('num_branches')
    return round(100 * covered / total, 2) if covered is not None and total is not None and total > 0 else None


def repair_audit(before, after):
    """Conservative count/name gate; expression changes require human review."""
    def signatures(code):
        tree = ast.parse(code)
        tests = Counter(n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_'))
        checks = Counter(ast.dump(n, include_attributes=False) for n in ast.walk(tree)
            if isinstance(n, ast.Assert) or isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and (n.func.attr.startswith('assert') or n.func.attr in {'raises', 'warns'}))
        return tests, checks
    try:
        old_tests, old_checks = signatures(before)
        new_tests, new_checks = signatures(after)
        removed = list((old_tests-new_tests).elements())
        changed = list((old_checks-new_checks).elements())
        no_extra_tautologies = audit_test_quality(after)['tautological_assertions'] <= audit_test_quality(before)['tautological_assertions']
        return dict(accepted=not removed and no_extra_tautologies and sum(new_checks.values()) >= sum(old_checks.values()),
                    removed_tests=removed, removed_or_changed_checks=changed,
                    review_required=bool(changed), semantic_preservation=None)
    except SyntaxError:
        # There is no valid assertion AST to compare when the initial candidate
        # is malformed. Keep both files and require explicit semantic review.
        try:
            signatures(before)
        except SyntaxError:
            try:
                new_tests, new_checks = signatures(after)
                return dict(accepted=bool(new_tests and new_checks) and
                            audit_test_quality(after)['tautological_assertions'] == 0,
                            review_required=True, semantic_preservation=None,
                            reason='original AST invalid; preservation cannot be established')
            except SyntaxError:
                pass
        return dict(accepted=False, review_required=True, reason='invalid repair AST')


def source_hashes():
    paths = [*sorted((BASE/'council').glob('*.py')), BASE/'pilot.json', BASE/'pilot/setup.py',
             BASE/'pilot/probe.py', BASE/'analyze.py', BASE/'pilot/scoring.py', BASE/'pilot/quality.py', BASE/'pilot/screen_trace.py']
    return {str(p.relative_to(BASE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def run_sample(args, engine, product, sample_dir, settings):
    started = time.perf_counter()
    row = dict(sample_id=sample_dir.name, status='running', suite_all_pass=False, first_pass=False,
        passed_tests=0, branch_pct=None, mutation_score=None, repaired_by_critic=False,
        repair_attempted=False, stages={})
    write_json(sample_dir/'result.json', row)
    try:
        engine.sample_id = sample_dir.name
        root = sample_dir/'PyCG'
        shutil.copytree(product, root, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', 'Test4DT_tests'))
        baseline_hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (root/'pycg').rglob('*.py')}
        def unchanged_product():
            current = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in (root/'pycg').rglob('*.py')}
            if current != baseline_hashes:
                raise RuntimeError('Product source changed during test execution; scores rejected')
        stage = time.perf_counter()
        context = ''
        mode = 'verified' if args.mode == 'council' else args.mode
        if mode != 'baseline':
            extraction = extract(root)
            write_json(sample_dir/'candidates.json', extraction)
            context, selection = select(root, extraction, mode, sample_dir, settings)
            row['selection'] = selection
            row['stages']['setup'] = time.perf_counter()-stage
            if not selection['complete']:
                row['status'] = 'setup_incomplete'
                return row
        row['stages']['setup'] = time.perf_counter()-stage
        source = source_context(root)
        stage = time.perf_counter()
        initial = generate_test_with_coder(engine, settings['target_module'], settings['target_function'],
                                           source, context, settings['scenario_prompt'])
        (sample_dir/'test_candidate_v1.py').write_text(initial)
        row['initial_audit'] = audit_test_quality(initial)
        row['stages']['generation'] = time.perf_counter()-stage
        tests = root/'Test4DT_tests'
        tests.mkdir(exist_ok=True)
        test_file = tests/'test_generated.py'
        test_file.write_text(initial)
        shutil.copyfile(BASE/'pilot/screen_trace.py', tests/'conftest.py')
        timeout = settings['score_timeout']
        process, report, _ = pytest_run(root, sample_dir, 'v1_eval', ['Test4DT_tests'], timeout)
        row['first_pass'] = suite_all_pass(process, report)
        row['initial_passed_tests'] = len(passed_nodes(report))
        final = initial
        if not row['first_pass'] and not args.no_repair and not process.get('timeout'):
            row['repair_attempted'] = True
            stage = time.perf_counter()
            diagnostics = '\n'.join([process.get('stdout') or '', process.get('stderr') or '', json.dumps(report)])
            repair_engine = engine if getattr(args, 'repair_with', 'critic') == 'critic' else SimpleNamespace(call_critic=engine.call_coder)
            candidate = repair_with_critic(repair_engine, initial, diagnostics[-12000:], source, context)
            (sample_dir/'test_candidate_v2_repaired.py').write_text(candidate)
            row['repair_audit'] = repair_audit(initial, candidate)
            if row['repair_audit']['accepted']:
                test_file.write_text(candidate)
                process, report, _ = pytest_run(root, sample_dir, 'v2_repair_eval', ['Test4DT_tests'], timeout)
                final = candidate
                row['repaired_by_critic'] = suite_all_pass(process, report) and getattr(args, 'repair_with', 'critic') == 'critic'
                row['repair_suite_pass'] = suite_all_pass(process, report)
            row['stages']['repair'] = time.perf_counter()-stage
        row['audit'] = audit_test_quality(final)
        (sample_dir/'test_final.py').write_text(final)
        row['final_execution_all_pass'] = suite_all_pass(process, report)
        stage = time.perf_counter()
        unchanged_product()
        scored = score(root, sample_dir, settings)
        unchanged_product()
        row['stages']['scoring'] = time.perf_counter()-stage
        row['score_status'] = scored['status']
        row['passed_tests'] = scored.get('passed', 0)
        row['any_passing_tests'] = row['passed_tests'] > 0
        row['mutant_pool_hash'] = scored.get('mutant_pool_hash')
        row['mutants'] = [dict(name=m['name'], verdict=m['verdict']) for m in scored.get('mutants', [])]
        resolved = len(row['mutants']) == 2 and all(m['verdict'] in {'killed', 'survived'} for m in row['mutants'])
        row['scoring_complete'] = scored['status'] == 'scored' and resolved
        original_path = sample_dir/'original/pytest.json'
        original = json.loads(original_path.read_text()) if original_path.exists() else {}
        row['suite_all_pass'] = bool(row['scoring_complete'] and row['final_execution_all_pass']
            and suite_all_pass(scored.get('original_process', {}), original))
        row['status'] = 'passed' if row['suite_all_pass'] else ('failed' if scored['status'] in {'scored', 'no_generated_tests'} else 'scoring_error')
        if row['scoring_complete']:
            coverage = scored.get('branch_coverage') or {}
            row['branch_pct'] = branch_percentage(coverage.get('module') or {})
            row['function_coverage'] = coverage.get('functions')
            from analyze import scoped_coverage
            row.update(scoped_coverage(scored, settings['target_function']))
            row['mutation_score'] = scored.get('mutation_score')
        trace_path = sample_dir/'eligible_original/receiver_trace.json'
        row['loader_trace'] = json.loads(trace_path.read_text()) if trace_path.exists() else None
        row['quality_gate'] = 'review_required: suite pass, reach, and mutation do not establish oracle correctness'
    except Exception as exc:
        row.update(status='execution_error', suite_all_pass=False, scoring_complete=False,
                   branch_pct=None, mutation_score=None, error=repr(exc), traceback=traceback.format_exc())
    finally:
        row['seconds'] = time.perf_counter()-started
        write_json(sample_dir/'result.json', row)
    return row


def run_council_pipeline(args):
    if args.samples < 1 or args.max_new_tokens < 1:
        raise ValueError('samples and max_new_tokens must be positive')
    output = reserve_output(args.output)
    started = time.perf_counter()
    settings = json.loads((BASE/'pilot.json').read_text())
    policy = dict(protocol='council-case-study-v2', target_commit=PYCG, settings=settings,
        source_hashes=source_hashes(), max_new_tokens=args.max_new_tokens,
        generation=dict(do_sample=getattr(args, 'temperature', 0.0) > 0.0,
                        temperature=getattr(args, 'temperature', 0.0),
                        seed=getattr(args, 'seed', 42)),
        load_in_4bit=bool(getattr(args, 'load_in_4bit', False)))
    summary = dict(schema_version=SCHEMA_VERSION, run_kind='mock' if args.mock else 'real', mock=args.mock,
        output=str(output), protocol=policy['protocol'], cohort=digest(policy), policy=policy,
        independent_targets=1, inference='development case study; greedy repetitions are not independent targets',
        baseline_definition='Council without setup; not upstream Test4Py', mode=args.mode,
        coder_model=args.coder_model, critic_model=args.critic_model, no_repair=args.no_repair,
        repair_with=getattr(args, 'repair_with', 'critic'), planned_samples=args.samples,
        samples=0, passed_samples=0, first_pass_samples=0, critic_repairs=0, results=[], status='running',
        requested_revisions=dict(coder=getattr(args, 'coder_revision', 'main'), critic=getattr(args, 'critic_revision', 'main')))
    write_json(output/'manifest.json', summary)
    engine = None
    def save():
        summary['samples'] = len(summary['results'])
        summary['passed_samples'] = sum(r.get('suite_all_pass') is True for r in summary['results'])
        summary['first_pass_samples'] = sum(r.get('first_pass') is True for r in summary['results'])
        summary['critic_repairs'] = sum(r.get('repaired_by_critic') is True for r in summary['results'])
        summary['total_seconds'] = time.perf_counter()-started
        if engine:
            summary.update(telemetry=engine.telemetry, engine=engine.snapshot())
        write_json(output/'summary.json', summary)
    save()
    try:
        if not args.mock:
            # Install dependencies before the run, never mutate an experimental environment.
            import pytest_jsonreport  # noqa: F401
            import coverage  # noqa: F401
            summary['environment'] = dict(python=platform.python_version(), packages=package_versions())
        stage = time.perf_counter()
        engine = CouncilEngine(coder_model=args.coder_model, critic_model=args.critic_model,
            mock=args.mock, max_new_tokens=args.max_new_tokens, load_in_4bit=getattr(args, 'load_in_4bit', False),
            coder_revision=getattr(args, 'coder_revision', 'main'), critic_revision=getattr(args, 'critic_revision', 'main'),
            seed=getattr(args, 'seed', 42), enable_critic=not args.no_repair and getattr(args, 'repair_with', 'critic') == 'critic',
            work=output, temperature=getattr(args, 'temperature', 0.0))
        summary['model_load_seconds'] = time.perf_counter()-stage
        save()
        if not args.mock:
            product = output/'target_repo'
            checkout('https://github.com/vitsalis/PyCG.git', PYCG, product)
        for idx in range(args.samples):
            if not args.mock and getattr(args, 'temperature', 0.0) > 0.0:
                import torch
                torch.manual_seed(args.seed + idx)
            directory = output/'samples'/f'sample_{idx+1:02d}'
            directory.mkdir(parents=True)
            print(f'[Council] {args.mode}: {idx+1}/{args.samples} -> {directory}', flush=True)
            if args.mock:
                raw = engine.call_coder('Infrastructure smoke only', 'No experimental scoring')
                (directory/'mock_completion.txt').write_text(raw)
                row = dict(sample_id=directory.name, status='mock_only', suite_all_pass=None,
                    first_pass=None, passed_tests=None, branch_pct=None, mutation_score=None)
                write_json(directory/'result.json', row)
            else:
                row = run_sample(args, engine, product, directory, settings)
            summary['results'].append(row)
            save()
        summary['status'] = ('mock_complete' if args.mock else
            'complete_with_errors' if any(r['status'] in {'execution_error', 'scoring_error'} for r in summary['results']) else 'complete')
    except Exception as exc:
        summary.update(status='failed', error=repr(exc), traceback=traceback.format_exc())
    finally:
        save()
        lines = ['# Council one-target development case study', '',
            f"Run kind: {summary['run_kind']}; status: {summary['status']}; independent targets: 1.",
            'Baseline = Council without setup, not upstream Test4Py. Repetitions are greedy replays.',
            'Coverage: module and target+nested scopes are separate, conditional on complete scoring. Mutation: two illustrative mutants.',
            'Semantic assertion correctness requires review. Missing scores remain NA.', '',
            f"Completed attempts: {summary['samples']}/{args.samples}. " + ('Mock output has no efficacy scores.' if args.mock else
             f"All-pass suites: {summary['passed_samples']}/{args.samples}; first-pass suites: {summary['first_pass_samples']}/{args.samples}."), '',
            '| Sample | Status | Initial suite pass | Final suite pass | Passing nodes | Module branch % | Target+nested branch % | Mutation |',
            '|---|---|---|---|---:|---:|---:|---:|']
        for r in summary['results']:
            lines.append('| '+' | '.join('NA' if r.get(k) is None else str(r[k]) for k in
                ('sample_id', 'status', 'first_pass', 'suite_all_pass', 'passed_tests', 'branch_pct', 'target_branch_pct', 'mutation_score'))+' |')
        if summary.get('error'):
            lines += ['', 'Run failure: '+summary['error']]
        (output/'report.md').write_text('\n'.join(lines)+'\n')
    print(f"[Council] {summary['status']}; report: {output/'report.md'}", flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=2, help='Repeated generations of ONE target')
    parser.add_argument('--mode', choices=('council', 'baseline', 'verified', 'extracted', 'ranked', 'caller'), default='council')
    parser.add_argument('--fast', action='store_true')
    parser.add_argument('--coder-model')
    parser.add_argument('--critic-model')
    parser.add_argument('--coder-revision', default='main', help='Resolved to an immutable SHA and recorded')
    parser.add_argument('--critic-revision', default='main')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--temperature', type=float, default=0.0, help='Sampling temperature (0.0 for deterministic greedy)')
    parser.add_argument('--no-repair', action='store_true')
    parser.add_argument('--repair-with', choices=('critic', 'coder'), default='critic')
    parser.add_argument('--max-new-tokens', type=int, default=2048)
    parser.add_argument('--load-in-4bit', dest='load_in_4bit', action='store_true', default=None)
    parser.add_argument('--no-4bit', dest='load_in_4bit', action='store_false')
    parser.add_argument('--mock', action='store_true', help='Offline infrastructure only; no efficacy metrics')
    parser.add_argument('--output', type=Path, default=BASE/'runs/council_v2')
    args = parser.parse_args()
    if args.samples < 1 or args.max_new_tokens < 1:
        parser.error('positive samples and token limit required')
    args.coder_model = args.coder_model or ('Qwen/Qwen3-4B-Instruct-2507' if args.fast else 'Qwen/Qwen2.5-Coder-7B-Instruct')
    args.critic_model = args.critic_model or 'Qwen/Qwen3-4B-Instruct-2507'
    if args.load_in_4bit is None:
        args.load_in_4bit = any(s in args.coder_model.lower() for s in ('7b', '8b', '14b', '32b'))
    result = run_council_pipeline(args)
    return 1 if result['status'] in {'failed', 'complete_with_errors'} else 0


if __name__ == '__main__':
    raise SystemExit(main())
