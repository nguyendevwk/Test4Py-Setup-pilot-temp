#!/usr/bin/env python3
"""Council development screen, NOT upstream Test4Py or an efficacy benchmark.

ranked uses a curated setup hint; verified witnesses target function or
constructor entry in the checkout. Neither is automatic setup mining or proof of target preconditions.
Protocol v4 must not be pooled with historical results.
Grounded adds bounded source dependencies; verified witnesses callable entry only.
"""
import argparse
import ast
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback

os.environ.setdefault('USE_TF', '0')
os.environ.setdefault('USE_FLAX', '0')

from council.engine import CouncilEngine
from council.critic import audit_test_quality
from council.runner import repair_audit
from pilot.common import (command, checked, reserve_output, write_json, append_json,
                          package_versions)
from pilot.grounding import dependency_context, verify_target_invocation, load_target_spec
from pilot.multitarget import (clean_code_block, passing_subset_measurement, execute_pytest_and_coverage,
                              probe_setup_candidate, inspect_api, readiness)

BASE_DIR = Path(__file__).resolve().parent
CURATED_TARGETS = [
    # =========================================================================
    # TẬP A: TYPE-ANNOTATED & DOCSTRING-RICH SUBJECTS (TEST4PY TABLE 1)
    # =========================================================================
    {
        "id": "docstring_parser_parse",
        "category": "Typed_A",
        "project": "docstring_parser",
        "repo_url": "https://github.com/rr-/docstring_parser.git",
        "commit": "a8e2a3ba5a4cdd906830735cb41a6a22c9346bf4",
        "module": "docstring_parser.parser",
        "file": "docstring_parser/parser.py",
        "symbol": "parse",
        "class_name": None,
        "setup_hint": "sample_doc = \"\"\"Summary line.\n\n:param name: parameter description\n:type name: str\n:returns: return description\n\"\"\""
    },
    {
        "id": "codetiming_timer",
        "category": "Typed_A",
        "project": "codetiming",
        "repo_url": "https://github.com/realpython/codetiming.git",
        "commit": "e51e4c3a50a395e301c33013cd048182f961f369",
        "module": "codetiming._timer",
        "file": "codetiming/_timer.py",
        "symbol": "Timer",
        "class_name": "Timer",
        "setup_hint": "from codetiming import Timer\nt = Timer(name='perf_timer', text='Elapsed: {:0.4f}s')\nt.start()"
    },
    {
        "id": "typesystem_schema",
        "category": "Typed_A",
        "project": "typesystem",
        "repo_url": "https://github.com/encode/typesystem.git",
        "commit": None,
        "module": "typesystem.schemas",
        "file": "typesystem/schemas.py",
        "symbol": "Schema",
        "class_name": "Schema",
        "setup_hint": "from typesystem import Schema, String, Integer\nclass UserSchema(Schema):\n    username = String(max_length=50)\n    age = Integer()\nuser = UserSchema(username='alice', age=30)"
    },
    # =========================================================================
    # TẬP NA: STATEFUL OBJECT GRAPH BASELINES (TEST4PY TABLE 1)
    # =========================================================================
    {
        "id": "pycg_imports",
        "category": "NA_Baseline",
        "project": "PyCG",
        "repo_url": "https://github.com/vitsalis/PyCG.git",
        "commit": "8d5dc40837803beef1d8d379fbf2cdad6cd94641",
        "module": "pycg.machinery.imports",
        "file": "pycg/machinery/imports.py",
        "symbol": "get_custom_loader",
        "class_name": "ImportManager",
        "setup_hint": "from pycg.machinery.imports import ImportManager\nmod = ImportManager()\nmod.create_node('pkg.main')\nmod.set_current_mod('pkg.main', 'main.py')"
    },
    {
        "id": "woa_whale_opt",
        "category": "NA_Baseline",
        "project": "woa",
        "repo_url": "https://github.com/docwza/woa.git",
        "commit": "4747379",
        "module": "src.whale_optimization",
        "file": "src/whale_optimization.py",
        "symbol": "WhaleOptimization",
        "class_name": "WhaleOptimization",
        "setup_hint": "from src.whale_optimization import WhaleOptimization\nwoa = WhaleOptimization(opt_func=lambda x: sum(i**2 for i in x), constraints=[(-5, 5), (-5, 5)], nsols=5, b=1, a=2, a_step=0.1)"
    },
    {
        "id": "superstring",
        "category": "NA_Baseline",
        "project": "superstring.py",
        "repo_url": "https://github.com/btwael/superstring.py.git",
        "commit": "f47ef78",
        "module": "superstring.superstring",
        "file": "superstring/superstring.py",
        "symbol": "SuperString",
        "class_name": "SuperString",
        "setup_hint": "from superstring.superstring import SuperString\ns = SuperString('Test String For Python Testing')"
    }
]

def extract_target_source(file_path: Path, symbol_name: str) -> dict:
    source = file_path.read_text(encoding='utf-8')
    tree = ast.parse(source)
    target_node, parent_class = None, None
    body = tree.body
    for part in symbol_name.split('.'):
        matches = [n for n in body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.name == part]
        if len(matches) != 1:
            raise ValueError(f'Target {symbol_name} missing or ambiguous in {file_path}; use qualified Class.method')
        if isinstance(target_node, ast.ClassDef):
            parent_class = target_node
        target_node = matches[0]
        body = getattr(target_node, 'body', [])

    # Extract type hints via AST
    type_hints = {}
    if isinstance(target_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for arg in target_node.args.args:
            if arg.annotation:
                type_hints[arg.arg] = ast.unparse(arg.annotation)
        if target_node.returns:
            type_hints['return'] = ast.unparse(target_node.returns)
    elif isinstance(target_node, ast.ClassDef):
        for item in target_node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                type_hints[item.target.id] = ast.unparse(item.annotation)
            elif isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == '__init__':
                for arg in item.args.args:
                    if arg.annotation and arg.arg != 'self':
                        type_hints[arg.arg] = ast.unparse(arg.annotation)

    docstring = ast.get_docstring(target_node) or ''

    return {
        'source': ast.get_source_segment(source, target_node) or '',
        'parent_class': parent_class.name if parent_class else None,
        'docstring': docstring,
        'has_docstrings': bool(docstring.strip()),
        'type_hints': type_hints,
        'has_type_hints': bool(type_hints)
    }



class DualGPUBenchmarkEngine(CouncilEngine):
    """Reuse the logged NF4 Council backend; raw calls also saved per sample."""
    def __init__(self, *args, max_input_tokens=8192, **kwargs):
        self.max_input_tokens = max_input_tokens
        super().__init__(*args, **kwargs)

    def generate(self, role, system_prompt, user_prompt, seed=42):
        if not self.mock:
            import torch
            torch.manual_seed(seed)
            tokenizer = getattr(self, role+'_tokenizer')
            tokens = tokenizer.apply_chat_template([dict(role='system', content=system_prompt),
                      dict(role='user', content=user_prompt)], tokenize=True, add_generation_prompt=True)
            if len(tokens) > self.max_input_tokens:
                raise ValueError(f'Input budget exceeded: {len(tokens)} > {self.max_input_tokens}; no silent truncation')
        return self._call(role, system_prompt, user_prompt)


def product_hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(root).rglob('*.py')) if '.git' not in p.parts}


def clone_if_needed(target, repos_dir):
    dest = Path(repos_dir).resolve()/target['project']
    if not dest.exists():
        checked(['git', 'clone', '--depth', '1', target['repo_url'], dest], timeout=180)
    commit = target.get('commit')
    if commit:
        actual = checked(['git', '-C', dest, 'rev-parse', 'HEAD'])
        if not actual.startswith(commit):
            if checked(['git', '-C', dest, 'status', '--porcelain']):
                raise ValueError('Refusing to change dirty target checkout: '+str(dest))
            checked(['git', '-C', dest, 'fetch', '--depth', '1', 'origin', commit], timeout=180)
            checked(['git', '-C', dest, 'checkout', '--detach', 'FETCH_HEAD'])
    if checked(['git', '-C', dest, 'status', '--porcelain']):
        raise ValueError('Target checkout is dirty: '+str(dest))
    return dest


OUTPUT_RULES = '''Return exactly one fenced Python block containing the COMPLETE pytest file.
CRITICAL: Write EXACTLY ONE focused test function for ONE behavior, with at most 50 lines of Python.
Do NOT write multiple test functions in the file, because any single failing test causes the entire suite to fail.
Include meaningful assertions or pytest.raises checks, grounded in source.
Keep the response concise: no explanation, reasoning comments or multiple blocks.
For object state, trace which operation writes the field before asserting it.
Distinguish returned values from logger/callback outputs; capture callbacks through
public dependency injection when supported. Do not mock the implementation.
For structured input, derive its format from the chosen parser/consumer source.
If source evidence is insufficient, do not invent exception or output expectations.
Use the verified API inventory; do not invent imports, attributes or enum members.
Do not skip/xfail tests, mock the target, change product files, or suppress failures.
Derive expected behavior from production source/docstrings, not observed outputs.
'''


def run_single_evaluation(target, arm, sample_idx, engine, repo_root, out_dir, seed=42, repair_with='critic'):
    started = time.perf_counter()
    sample_dir = Path(out_dir)/f'sample_{sample_idx+1:02d}'
    sample_dir.mkdir(parents=True, exist_ok=False)
    row = dict(target_id=target['id'], category=target.get('category', 'Development'),
               project=target['project'], module=target['module'], symbol=target['symbol'],
               arm=arm, sample=sample_dir.name, seed=seed+sample_idx, mock=engine.mock,
               status='running', suite_pass=False, first_pass=False, stable=False, replay_status='not_run',
               pass_count=0, total_count=0, line_pct=None, branch_pct=None,
               repaired_by_critic=False, repair_attempted=False, probe_time_sec=0)
    write_json(sample_dir/'result.json', row)
    try:
        if engine.mock:
            row['status'] = 'mock_excluded'
            return row
        root = sample_dir/'product'
        shutil.copytree(repo_root, root, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
        before = product_hashes(root)
        info = extract_target_source(root/target['file'], target['symbol'])
        row.update(has_type_hints=info['has_type_hints'], has_docstrings=info['has_docstrings'])
        api = inspect_api(root, target['module'], target['symbol'])
        write_json(sample_dir/'api.json', api)
        setup = ''
        if arm in ('ranked', 'verified'):
            hint = target.get('setup_hint', '')
            if arm == 'verified':
                t0 = time.perf_counter()
                row['setup_probe'] = verify_target_invocation(hint, root, target['module'], target['symbol']) if hint else dict(accepted=False, reason='no hint')
                row['probe_time_sec'] = time.perf_counter()-t0
                write_json(sample_dir/'setup_probe.json', row['setup_probe'])
                if not row['setup_probe']['accepted']:
                    row['status'] = 'setup_unresolved'
                    return row
            setup = hint
        dependencies = dependency_context(root, target['file'], target['symbol']) if arm != 'baseline' else None
        if dependencies is not None:
            write_json(sample_dir/'dependencies.json', dependencies)
        prompt_api = dict(api, file=target['file'])
        context = (f"Target source:\n{info['source']}\nModule: {target['module']}\nSymbol: {target['symbol']}\n"
                   + 'Runtime API inventory (same for all arms):\n'+json.dumps(prompt_api, indent=2)
                   + ('\nProduction dependency source:\n'+json.dumps(dependencies['snippets'], indent=2) if dependencies else '')
                   + '\nCurated setup example (not assertion evidence):\n'+setup)
        if arm == 'verified' and row.get('setup_probe', {}).get('invocation'):
            context += '\nInvocation witness code (no return/output observations):\n'+row['setup_probe']['invocation']
        write_json(sample_dir/'context.json', dict(context=context, setup_origin='curated hint',
                   verification_scope=row.get('setup_probe', {}).get('scope', 'unverified'), api_policy='runtime-api-v1',
                   dependencies_policy='production-dependencies-v1' if dependencies else None))
        engine.sample_id = f"{target['id']}/{arm}/{sample_dir.name}"
        def call(role, system, user, stage=None):
            artifact_role = stage or role
            write_json(sample_dir/(artifact_role+'_prompt.json'), dict(system=system, user=user))
            raw = engine.generate(role, system, user, seed=row['seed'])
            (sample_dir/(artifact_role+'_raw.txt')).write_text(raw)
            return raw
        raw = call('coder', 'Generate rigorous Python unit tests.\n'+OUTPUT_RULES, context)
        extraction_error = None
        try:
            initial = clean_code_block(raw)
        except ValueError as exc:
            initial = None
            extraction_error = str(exc)
        row['initial_extraction_error'] = extraction_error
        first = None
        if initial is not None:
            (sample_dir/'test_candidate_v1.py').write_text(initial)
            row['initial_audit'] = audit_test_quality(initial)
            first = execute_pytest_and_coverage(initial, root, target['module'], sample_dir/'v1_raw')
            row['first_pass'] = first['suite_pass']
        final, evaluation = initial, first
        if not row['first_pass'] and not (first and first['timeout']):
            row['repair_attempted'] = True
            if first:
                pytest_report = json.loads((sample_dir/'v1_raw/pytest_report.json').read_text()) if (sample_dir/'v1_raw/pytest_report.json').exists() else {}
                failures = [dict(node=t['nodeid'], phases={p: t.get(p, {}).get('crash', {}) for p in ('setup','call','teardown') if t.get(p, {}).get('outcome') == 'failed'})
                            for t in pytest_report.get('tests', []) if t.get('outcome') != 'passed']
                diagnostics = json.dumps(dict(status=first['status'], failures=failures,
                    collection_errors=[c.get('longrepr', '')[:1500] for c in pytest_report.get('collectors', []) if c.get('outcome') == 'failed']))
            else:
                diagnostics = extraction_error
            repair_raw = call(repair_with, 'Repair imports, setup or syntax while preserving every test and assertion expression. Never change expected values to match observed outputs.\n'+OUTPUT_RULES,
                              context+'\nCandidate:\n'+(initial or raw)+'\nDiagnostics:\n'+diagnostics[-6000:], stage='repair')
            try:
                repaired = clean_code_block(repair_raw)
                (sample_dir/'test_candidate_v2_repaired.py').write_text(repaired)
                row['repair_audit'] = repair_audit(initial or raw, repaired)
                if row['repair_audit']['accepted'] and not row['repair_audit']['review_required']:
                    rep_eval = execute_pytest_and_coverage(repaired, root, target['module'], sample_dir/'v2_repaired')
                    final, evaluation = repaired, rep_eval
                    row['repaired_by_critic'] = bool(rep_eval['suite_pass'] and repair_with == 'critic')
                    row['repair_suite_pass'] = rep_eval['suite_pass']
                else:
                    row['repair_rejected'] = 'test/check preservation or changed assertion; proposal saved for review, no automatic credit'
            except ValueError as exc:
                row['repair_extraction_error'] = str(exc)
        if final is None or evaluation is None:
            row['status'] = 'extraction_error'
            return row
        (sample_dir/'test_final.py').write_text(final)
        row['audit'] = audit_test_quality(final)
        row['focus_contract_met'] = row['audit']['test_functions'] == 1
        row['final_evaluation'] = evaluation
        row.update(suite_pass=evaluation['suite_pass'], pass_count=evaluation['pass_count'],
                   total_count=evaluation['total_nodes'], line_pct=evaluation['line_pct'],
                   branch_pct=evaluation['branch_pct'])
        if row['suite_pass']:
            replay = execute_pytest_and_coverage(final, root, target['module'], sample_dir/'replay')
            # Nodeids contain absolute sample paths, so compare test suffixes.
            node_names = lambda e: sorted(n.split('::', 1)[-1] for n in e['passing_nodes'])
            row['stable'] = bool(replay['suite_pass'] and node_names(replay) == node_names(evaluation)
                                 and replay['line_pct'] == evaluation['line_pct'] and replay['branch_pct'] == evaluation['branch_pct'])
            row['replay'] = replay
            row['replay_status'] = 'stable' if row['stable'] else 'unstable'
        row['passing_subset'] = passing_subset_measurement(final, root, target['module'], sample_dir/'passing_subset', evaluation)
        if product_hashes(root) != before:
            row.update(status='product_modified', suite_pass=False, stable=False, line_pct=None, branch_pct=None,
                       passing_subset=dict(status='product_modified', line_pct=None, branch_pct=None))
        else:
            row['status'] = 'completed'
    except Exception as exc:
        row.update(status='execution_error', error=repr(exc), traceback=traceback.format_exc(),
                   suite_pass=False, stable=False, line_pct=None, branch_pct=None)
    finally:
        row['runtime_sec'] = round(time.perf_counter()-started, 3)
        write_json(sample_dir/'result.json', row)
    return row


def export_markdown_report(records, out_path, telemetry):
    pct = lambda v: 'NA' if v is None else f'{v:.2f}'
    lines = ['# Council development screen v4',
             'Baseline is Council without setup, not upstream Test4Py. No efficacy claim.',
             'No pruning. Main coverage: full all-pass suite. Secondary subset coverage: original-passing nodes replayed twice; NA is not zero.',
             'grounded = production dependencies; ranked = grounded + curated hint; verified adds callable-entry witness (constructor only for classes).',
             '', '| Target | Arm | Status | First pass | Final pass | Nodes | Line % | Branch % | Replay | Eligible/planned | Subset line % |',
             '|---|---|---|---|---|---|---|---|---|---|---|']
    for r in records:
        lines.append(f"| {r['target_id']} | {r['arm']} | {r['status']} | {r.get('first_pass', False)} | {r['suite_pass']} | {r['pass_count']}/{r['total_count']} | {pct(r['line_pct'])} | {pct(r['branch_pct'])} | {r.get('replay_status', 'not_run')} | {r.get('passing_subset', {}).get('eligible', 0)}/{r['total_count']} | {pct(r.get('passing_subset', {}).get('line_pct'))} |")
    lines += ['', 'Telemetry (measured calls only): '+json.dumps(telemetry),
              'Inspect readiness.json and raw artifacts before scheduling any full experiment.']
    text = '\n'.join(lines)+'\n'
    Path(out_path).write_text(text)
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repos-dir', type=Path, default=Path('/kaggle/working/BENCHMARK_REPOS'))
    parser.add_argument('--targets', default=None, help='Comma-separated ids or all; default two development targets')
    parser.add_argument('--target-spec', type=Path, help='Locked external benchmark JSON; no runtime target selection')
    parser.add_argument('--arms', default='baseline,grounded,ranked,verified')
    parser.add_argument('--samples', type=int, default=1)
    parser.add_argument('--temperature', type=float, default=0.7)
    parser.add_argument('--coder-model', default='Qwen/Qwen2.5-Coder-7B-Instruct')
    parser.add_argument('--critic-model', default='Qwen/Qwen3-4B-Instruct-2507')
    parser.add_argument('--coder-revision', default='main')
    parser.add_argument('--critic-revision', default='main')
    parser.add_argument('--repair-with', choices=['critic', 'coder'], default='critic')
    parser.add_argument('--max-input-tokens', type=int, default=8192)
    parser.add_argument('--max-new-tokens', type=int, default=2048)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--mock', action='store_true', help='Offline artifact check; never efficacy data')
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--prepared', type=Path, help='preflight.json from the prepare-only run; locks checkouts')
    parser.add_argument('--zip', action='store_true', default=True)
    args = parser.parse_args()
    try:
        frame = load_target_spec(args.target_spec) if args.target_spec else CURATED_TARGETS
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
    if args.targets is None:
        args.targets = 'all' if args.target_spec else 'docstring_parser_parse,codetiming_timer'
    ids = args.targets.split(',')
    valid = {t['id']: t for t in frame}
    if args.targets == 'all':
        ids = list(valid)
    arms = args.arms.split(',')
    if (not ids or len(set(ids)) != len(ids) or set(ids)-valid.keys()
        or not arms or len(set(arms)) != len(arms) or set(arms)-{'baseline', 'grounded', 'ranked', 'verified'}
        or args.samples < 1 or args.max_new_tokens < 1 or args.max_input_tokens < 1 or not 0 <= args.temperature <= 2):
        parser.error('Invalid targets, arms, samples, temperature or token budget')
    targets = [dict(valid[i]) for i in ids]
    args.output = reserve_output(args.output)
    print('Reports: '+str(args.output), flush=True)
    manifest = dict(protocol='council-development-screen-v4', mock=args.mock,
                    argv=sys.argv, config={k: str(v) if isinstance(v, Path) else v for k,v in vars(args).items()},
                    source_hashes={str(p.relative_to(BASE_DIR)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in [Path(__file__).resolve(), BASE_DIR/'pilot/multitarget.py', BASE_DIR/'pilot/grounding.py',
                                             BASE_DIR/'council/engine.py', BASE_DIR/'council/runner.py', BASE_DIR/'council/critic.py']},
                    python=sys.version, packages=package_versions())
    if args.target_spec:
        write_json(args.output/'input-target-spec.json', dict(targets=frame))
        manifest['target_spec_sha256'] = hashlib.sha256(args.target_spec.read_bytes()).hexdigest()
    write_json(args.output/'manifest.json', manifest)
    write_json(args.output/'plan.json', dict(protocol=manifest['protocol'],
        context_policy='baseline API-only; grounded dependencies; ranked adds curated hint; verified adds invocation witness',
        repair_policy='one attempt, assertion expressions frozen; changed proposals never credited',
        planned=[dict(target=t['id'], arm=a, seed=args.seed+i, sample=f'sample_{i+1:02d}')
                 for t in targets for a in arms for i in range(args.samples)]))
    preflight = {}
    if not args.mock:
        locked = json.loads(args.prepared.read_text()) if args.prepared else None
        for target in targets:
            try:
                root = clone_if_needed(target, args.repos_dir)
                commit = checked(['git', '-C', root, 'rev-parse', 'HEAD'])
                hashes = product_hashes(root)
                if locked is not None:
                    prev = locked[target['id']]
                    if prev['commit'] != commit or prev['hashes'] != hashes or not prev['ready']:
                        raise ValueError('Prepared checkout changed or failed; create a new plan explicitly')
                api = inspect_api(root, target['module'], target['symbol'])
                extract_target_source(root/target['file'], target['symbol'])
                probe = verify_target_invocation(target.get('setup_hint', ''), root, target['module'], target['symbol'])
                preflight[target['id']] = dict(ready=True, setup_ready=probe['accepted'], root=str(root), commit=commit,
                                                hashes=hashes, api=api, setup_probe=probe)
            except Exception as exc:
                preflight[target['id']] = dict(ready=False, error=repr(exc))
            write_json(args.output/'preflight.json', preflight)
    if args.prepare_only:
        print('Preflight: '+str(args.output/'preflight.json'), flush=True)
        return 0 if preflight and all(p['ready'] for p in preflight.values()) else 2
    records = []
    planned = len(targets)*len(arms)*args.samples
    engine, load_error = None, None
    # Resolve immutable model SHAs BEFORE loading. No silent revision fallback.
    try:
        if not args.mock:
            if not preflight or not all(p['ready'] for p in preflight.values()):
                raise RuntimeError('Preflight failed; inference skipped. Inspect preflight.json.')
            import torch
            if torch.cuda.device_count() < 2:
                raise RuntimeError('This GPU screen requires two visible CUDA devices')
            from huggingface_hub import HfApi
            args.coder_revision = HfApi().model_info(args.coder_model, revision=args.coder_revision).sha
            args.critic_revision = HfApi().model_info(args.critic_model, revision=args.critic_revision).sha
        write_json(args.output/'resolved_models.json', dict(coder=args.coder_revision, critic=args.critic_revision))
        engine = DualGPUBenchmarkEngine(coder_model=args.coder_model, critic_model=args.critic_model,
                 coder_revision=args.coder_revision, critic_revision=args.critic_revision,
                 temperature=args.temperature, seed=args.seed, max_new_tokens=args.max_new_tokens,
                 mock=args.mock, load_in_4bit=True, work=args.output, max_input_tokens=args.max_input_tokens,
                 enable_critic=args.repair_with == 'critic')
    except Exception as exc:
        load_error = repr(exc)
        write_json(args.output/'engine_failure.json', dict(error=load_error, traceback=traceback.format_exc()))
    for target in targets:
        for arm in arms:
            for i in range(args.samples):
                if engine is None:
                    row = dict(target_id=target['id'], arm=arm, sample=f'sample_{i+1:02d}',
                               status='preflight_or_engine_error', error=load_error,
                               suite_pass=False, stable=False, pass_count=0, total_count=0,
                               line_pct=None, branch_pct=None)
                    write_json(args.output/target['id']/arm/row['sample']/'result.json', row)
                else:
                    row = run_single_evaluation(target, arm, i, engine,
                            Path(preflight[target['id']]['root']) if not args.mock else BASE_DIR,
                            args.output/target['id']/arm, args.seed, args.repair_with)
                records.append(row)
                write_json(args.output/'summary.json', dict(schema_version=4, protocol=manifest['protocol'],
                           mock=args.mock, planned=planned, finished=len(records), records=records,
                           telemetry=engine.telemetry if engine else {}))
                print(f"{target['id']} {arm} {i+1}/{args.samples}: {row['status']} pass={row['suite_pass']}", flush=True)
    gate = readiness(records, planned, args.mock)
    write_json(args.output/'readiness.json', gate)
    if engine:
        write_json(args.output/'engine.json', engine.snapshot())
    export_markdown_report(records, args.output/'FINAL_REPORT.md', engine.telemetry if engine else {})
    for r in records:
        if isinstance(r.get('passing_subset'), dict):
            r['subset_line_pct'] = r['passing_subset'].get('line_pct')
            r['subset_branch_pct'] = r['passing_subset'].get('branch_pct')
    keys = ['target_id', 'category', 'arm', 'sample', 'seed', 'status', 'first_pass', 'suite_pass',
            'pass_count', 'total_count', 'line_pct', 'branch_pct', 'subset_line_pct', 'subset_branch_pct',
            'stable', 'replay_status', 'repair_attempted', 'repaired_by_critic', 'runtime_sec']
    with (args.output/'results.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)
    if args.zip:
        shutil.make_archive(str(args.output), 'zip', args.output)
    print('Harness ready: '+str(gate['harness_ready'])+'; strict generation-quality gate: '+str(gate['automated_ready'])+'; semantic review still required.')
    print('Reports: '+str(args.output), flush=True)
    return 0 if gate['automated_ready'] or (args.mock and engine is not None) else 2


if __name__ == '__main__':
    sys.exit(main())
