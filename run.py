"""Reproducible one-function Test4Py setup pilot; --help needs only Python."""
import argparse
from datetime import datetime, timezone
import json
import importlib.metadata
import platform
import os
from pathlib import Path
import sys
import time
import traceback

from pilot.console import Console
from pilot.progress import emit
from pilot.scheduling import execute_modes, gpu_slots
from pilot.telemetry import GPUMonitor
from pilot.common import BASE, MODES, PYCG, UPSTREAM, checkout, command, digest, write_json, reserve_output, package_versions


def print_metrics(output, summary):
    if not summary['arms']:
        return
    print('mode        status    pass  module_branch%  mutation  tokens(in/out)  seconds', flush=True)
    for mode in MODES:
        path = output / mode / 'report.json'
        if not path.exists():
            continue
        report = json.loads(path.read_text())
        score = report.get('score', {})
        coverage = score.get('branch_coverage') or {}
        module = coverage.get('module') or {}
        branches = module.get('num_branches', 0)
        branch = round(100 * module.get('covered_branches', 0) / branches, 1) if branches else None
        tokens = f"{report.get('input_tokens', 0)}/{report.get('output_tokens', 0)}"
        print(f"{mode:<11} {report.get('status','?'):<9} {str(score.get('passed')):<5} "
              f"{str(branch):<15} {str(score.get('mutation_score')):<9} {tokens:<16} "
              f"{summary['arms'][mode].get('total_seconds', 0):.1f}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=(*MODES, 'compare'), default='compare')
    parser.add_argument('--runtime', choices=('legacy', 'modern'), default='legacy',
                        help='modern allows Python 3.13 and requires requirements-modern.txt')
    parser.add_argument('--console', choices=('compact', 'quiet', 'full'), default='compact')
    parser.add_argument('--jobs', type=int, default=1, help='concurrent independent arms, one per GPU')
    parser.add_argument('--gpus', default='auto', help='indices relative to parent-visible GPUs, e.g. 0,1')
    parser.add_argument('--cpu-threads', type=int, default=1, help='CPU threads per arm, identical for all modes')
    parser.add_argument('--rounds', type=int, default=1)
    parser.add_argument('--model', default='Qwen/Qwen2.5-Coder-1.5B-Instruct')
    parser.add_argument('--model-revision')
    parser.add_argument('--embedding-revision')
    parser.add_argument('--max-new-tokens', type=int, default=512)
    parser.add_argument('--config', type=Path, default=BASE / 'pilot.json')
    parser.add_argument('--output', type=Path, default=BASE / 'runs' /
                        datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    parser.add_argument('--validate-only', action='store_true',
                        help='real pinned checkouts, two states, probes and internal scorer; no model/GPU')
    args = parser.parse_args()
    console = Console(args.console)
    if min(args.rounds, args.max_new_tokens, args.jobs, args.cpu_threads) < 1:
        parser.error('rounds and max-new-tokens must be positive')
    config = json.loads(args.config.read_text())
    if min(config['probe_timeout'], config['score_timeout'], config['worker_timeout'], config['max_probes']) <= 0:
        parser.error('timeouts and max_probes must be positive')
    try:
        output = reserve_output(args.output)
    except ValueError as exc:
        parser.error(str(exc))
    if output != args.output.resolve():
        print(f'Output already exists; preserving it. New run: {output}', flush=True)
    started = time.perf_counter()
    write_json(output / 'environment.json', dict(python=platform.python_version(), executable=sys.executable,
        packages=package_versions()))
    settings = dict(config, mode=args.mode, requested_output=str(args.output.resolve()), actual_output=str(output), runtime=args.runtime, model=args.model, model_revision=args.model_revision,
                    embedding_revision=args.embedding_revision, upstream=UPSTREAM,
                    target_commit=PYCG, rounds=args.rounds, max_new_tokens=args.max_new_tokens,
                    generation=dict(do_sample=False, seed=config['seed']), cpu_threads=args.cpu_threads,
                    requested_jobs=args.jobs, requested_gpus=args.gpus,
                    source_hashes={str(p.relative_to(BASE)): digest(p.read_text())
                        for p in [BASE / 'run.py', BASE / 'worker.py', BASE / 'bootstrap_kaggle.py',
                                  BASE / 'check_environment.py', BASE / 'requirements-notebook.txt',
                                  BASE / 'bootstrap_modern.py', BASE / 'requirements-modern.txt',
                                  *sorted((BASE / 'pilot').glob('*.py'))]})
    manifest = output / 'experiment.json'
    write_json(manifest, settings)
    summary = dict(status='running', output=str(output), arms={}, validation_only=args.validate_only,
                   paper='https://arxiv.org/abs/2503.14000v2')
    try:
        lower, upper = ((3, 11), (3, 13)) if args.runtime == 'modern' else ((3, 10), (3, 12))
        if not lower <= sys.version_info[:2] <= upper:
            raise RuntimeError('Pilot requires Python 3.10–3.12. Run python bootstrap_kaggle.py --venv /tmp/test4py-venv, then /tmp/test4py-venv/bin/python run.py with the same arguments.')
        upstream = output / 'upstream'
        stage = time.perf_counter()
        emit(output, 'preflight', 'checkout_upstream')
        checkout('https://github.com/Test4DT/Test4Py.git', UPSTREAM, upstream)
        summary['upstream_checkout_seconds'] = time.perf_counter() - stage
        summary['upstream_files'] = {name: digest((upstream / 'test4dt' / name).read_text())
            for name in ('message.py', 'testcase.py', 'gptapi.py', 'coverage_message.py')}
        if args.validate_only:
            root = output / 'validation' / 'PyCG'
            checkout('https://github.com/vitsalis/PyCG.git', PYCG, root)
            env = dict(os.environ, PYTHONPATH=str(BASE), PYTHONDONTWRITEBYTECODE='1')
            result = command([sys.executable, '-m', 'pilot.validate', root],
                             cwd=root, env=env, timeout=config['worker_timeout'], stream=True, label='validation',
                             log_path=output / 'validation-worker.log', console=console)
            write_json(output / 'validation_process.json', result)
            summary['status'] = 'complete' if result['returncode'] == 0 else 'validation_failed'
            if result['returncode'] != 0 or result['timeout']:
                print('Validation worker failed:\n' + (result['stdout'] + result['stderr'])[-6000:], flush=True)
        else:
            stage = time.perf_counter()
            emit(output, 'preflight', 'resolve_and_download_models')
            from huggingface_hub import model_info, snapshot_download
            settings['model_revision'] = model_info(args.model, revision=args.model_revision).sha
            settings['embedding_revision'] = model_info(config['embedding'], revision=args.embedding_revision).sha
            embedding_path = snapshot_download(config['embedding'], revision=settings['embedding_revision'],
                                ignore_patterns=['*.onnx', 'onnx/*', '*.h5', '*.msgpack'])
            # Download once before parallel processes contend for the same cache.
            snapshot_download(args.model, revision=settings['model_revision'],
                              ignore_patterns=['*.onnx', 'onnx/*', '*.h5', '*.msgpack'])
            summary['model_resolution_download_seconds'] = time.perf_counter() - stage
            write_json(manifest, settings)
            modes = MODES if args.mode == 'compare' else (args.mode,)
            slots = gpu_slots(min(args.jobs, len(modes)), args.gpus)
            settings['parallel_jobs'] = len(slots)
            settings['gpu_slots'] = slots
            write_json(manifest, settings)
            summary['execution'] = dict(jobs=len(slots), gpu_slots=slots, cpu_threads=args.cpu_threads,
                timing_note='Parallel wall time includes shared CPU/IO contention; not a serial speed benchmark')
            emit(output, 'comparison', 'schedule', arms=len(modes), jobs=len(slots), gpus=slots)
            def run_arm(mode, gpu):
                work = output / mode
                work.mkdir()
                arm_started = time.perf_counter()
                arm = dict(status='running', gpu=gpu)
                emit(work, 'arm', 'start', gpu=gpu if gpu is not None else 'inherited:cuda:0')
                for name in ('model_calls.jsonl', 'probes.jsonl'):
                    (work / name).touch()
                try:
                    root = work / 'PyCG'
                    stage = time.perf_counter()
                    checkout('https://github.com/vitsalis/PyCG.git', PYCG, root)
                    arm['checkout_seconds'] = time.perf_counter() - stage
                    env = dict(os.environ, PYTHONUNBUFFERED='1',
                        OMP_NUM_THREADS=str(args.cpu_threads), MKL_NUM_THREADS=str(args.cpu_threads),
                        OPENBLAS_NUM_THREADS=str(args.cpu_threads), USE_TF='0', USE_FLAX='0', TRANSFORMER_PATH=embedding_path,
                        USER_PYTHON_PATH=sys.executable,
                        PYTHONPATH=os.pathsep.join(map(str, (upstream, root, BASE))),
                        ANONYMIZED_TELEMETRY='False', PYTHONDONTWRITEBYTECODE='1',
                        TOKENIZERS_PARALLELISM='false', PYTHONHASHSEED=str(config['seed']))
                    if gpu is not None:
                        env['CUDA_VISIBLE_DEVICES'] = str(gpu)
                    process = command([sys.executable, BASE / 'worker.py', root, mode, manifest],
                                      cwd=root, env=env, timeout=config['worker_timeout'], stream=True,
                                      log_path=work / 'worker.log', label=mode, console=console)
                    write_json(work / 'process.json', process)
                    path = work / 'report.json'
                    report = json.loads(path.read_text()) if path.exists() else {}
                    arm['status'] = report.get('status', 'failed')
                    score = report.get('score', {})
                    arm['metrics'] = dict(passed=score.get('passed'), mutation_score=score.get('mutation_score'),
                        input_tokens=report.get('input_tokens', 0), output_tokens=report.get('output_tokens', 0))
                    if process['timeout'] or process['returncode'] != 0:
                        arm['status'] = 'failed'
                        report.update(status='failed', process=process)
                        write_json(path, report)
                except Exception as exc:
                    arm.update(status='failed', error=repr(exc), traceback=traceback.format_exc())
                    write_json(work / 'report.json', arm)
                arm['total_seconds'] = time.perf_counter() - arm_started
                emit(work, 'arm', 'finished', status=arm['status'], seconds=round(arm['total_seconds'], 2),
                     **arm.get('metrics', {}))
                return arm
            parallel_started = time.perf_counter()
            with GPUMonitor(output, console=console):
                for mode, arm in execute_modes(modes, slots, run_arm):
                    summary['arms'][mode] = arm
                    write_json(output / 'comparison.json', summary)
                    emit(output, 'comparison', 'completed', mode_finished=mode,
                         completed=len(summary['arms']), total=len(modes), status=arm['status'])
            summary['comparison_wall_seconds'] = time.perf_counter() - parallel_started
            summary['sum_arm_seconds'] = sum(a.get('total_seconds', 0) for a in summary['arms'].values())
            selections = {}
            hashes = {}
            for mode in modes:
                p = output / mode / 'selection.json'
                if p.exists():
                    value = json.loads(p.read_text())
                    selections[mode] = value.get('selected', {})
                    if value.get('candidate_hash'):
                        hashes[mode] = value['candidate_hash']
            pool_hashes = {}
            for mode in modes:
                report_path = output / mode / 'report.json'
                if report_path.exists():
                    arm_report = json.loads(report_path.read_text())
                    score = arm_report.get('score', {})
                    if score.get('mutant_pool_hash'):
                        pool_hashes[mode] = score['mutant_pool_hash']
                    summary['arms'][mode]['metrics'] = dict(
                        passed=score.get('passed'), mutation_score=score.get('mutation_score'),
                        branch_coverage=score.get('branch_coverage'),
                        input_tokens=arm_report.get('input_tokens'), output_tokens=arm_report.get('output_tokens'),
                        stages=arm_report.get('stages'))
            summary['mutant_pool_hashes'] = pool_hashes
            summary['same_mutant_pool'] = len(set(pool_hashes.values())) == 1 if pool_hashes else None
            summary['candidate_hashes'] = hashes
            summary['same_candidate_list'] = len(set(hashes.values())) == 1 if hashes else None
            summary['extracted_equals_verified'] = (
                {scenario: selections['extracted'].get(scenario) == selections['verified'].get(scenario)
                 for scenario in ('new_target', 'existing_target')}
                if {'extracted', 'verified'} <= selections.keys() else None)
            summary['status'] = 'complete' if all(a['status'] == 'complete' for a in summary['arms'].values()) else 'partial_failure'
    except Exception as exc:
        summary.update(status='preflight_failed', error=repr(exc), traceback=traceback.format_exc())
    summary['total_seconds'] = time.perf_counter() - started
    write_json(output / 'comparison.json', summary)
    print_metrics(output, summary)
    print(f'Reports: {output}\nStatus: {summary["status"]}')
    return 0 if summary['status'] == 'complete' else 1


if __name__ == '__main__':
    sys.exit(main())
