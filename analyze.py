"""Collect real pilot artifacts into auditable CSV/Markdown and optional figures."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone

from pilot.common import MODES, digest, reserve_output, write_json


def read(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {}


def records(path):
    try:
        with Path(path).open() as stream:
            for line in stream:
                try:
                    yield json.loads(line)
                except ValueError:
                    yield {'_invalid_record': True}
    except OSError:
        return


def csv_table(path, rows, fields):
    with Path(path).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({key: (json.dumps(row.get(key), ensure_ascii=False) if isinstance(row.get(key), (dict,list)) else row.get(key)) for key in fields})


def percentage(covered, total):
    return 100 * covered / total if covered is not None and total is not None and total > 0 else None


def scoped_coverage(score, target):
    coverage = score.get('branch_coverage') or {}
    module = coverage.get('module') or {}
    functions = coverage.get('functions') or {}
    matched = {name: value for name, value in functions.items()
               if name == target or name.startswith(target + '.')}
    result = dict(module_branch_pct=percentage(module.get('covered_branches'), module.get('num_branches')),
                  target_branch_pct=None, target_line_pct=None, loader_init_branch_pct=None,
                  target_scopes=list(matched))
    # Union concrete lines/arcs, never sum parent/nested summaries and double count.
    for label, executed, missing in [('target_branch_pct','executed_branches','missing_branches'),
                                     ('target_line_pct','executed_lines','missing_lines')]:
        if matched and all(executed in value and missing in value for value in matched.values()):
            covered, absent = set(), set()
            for value in matched.values():
                covered.update(tuple(x) if isinstance(x,list) else x for x in value[executed])
                absent.update(tuple(x) if isinstance(x,list) else x for x in value[missing])
            result[label] = percentage(len(covered), len(covered | absent))
    init = [value for name, value in matched.items() if name.endswith('.__init__')]
    if len(init) == 1:
        summary = init[0].get('summary', {})
        result['loader_init_branch_pct'] = percentage(summary.get('covered_branches'), summary.get('num_branches'))
    return result


def call_statistics(path):
    result = dict(calls=0, raw_generation_calls=0, input_tokens=0, output_tokens=0,
                  invalid_records=0, truncated_calls=0, model_seconds=0.)
    initialization = hashlib.sha256()
    phases = {}
    for row in records(path):
        if row.get('_invalid_record'):
            result['invalid_records'] += 1
            continue
        result['calls'] += 1
        for key in ('input_tokens','output_tokens'):
            result[key] += row.get(key,0)
        result['model_seconds'] += row.get('seconds',0)
        result['truncated_calls'] += int(bool(row.get('truncated')))
        if row.get('upstream_operation') in {'generate_test_case_normal','generate_test_case_easy','generate_test_case_evol'}:
            result['raw_generation_calls'] += 1
        phase = row.get('phase','unknown')
        totals = phases.setdefault(phase, dict(calls=0,input_tokens=0,output_tokens=0,seconds=0.))
        totals['calls'] += 1
        totals['input_tokens'] += row.get('input_tokens',0)
        totals['output_tokens'] += row.get('output_tokens',0)
        totals['seconds'] += row.get('seconds',0)
        if phase == 'initialization':
            initialization.update(json.dumps([row.get('messages'),row.get('output')],sort_keys=True).encode())
    result['initialization_trace_hash'] = initialization.hexdigest() if phases.get('initialization') else None
    result['phases'] = phases
    return result


def effectiveness_metrics(row, work):
    """Measured denominators only; event counts are not independent test outcomes."""
    calls = list(records(work / 'model_calls.jsonl'))
    probes = [p for p in records(work / 'probes.jsonl') if not p.get('_invalid_record')]
    errors = [e for e in records(work / 'errors.jsonl') if not e.get('_invalid_record')]
    tokens = None if row['input_tokens'] is None or row['output_tokens'] is None else row['input_tokens'] + row['output_tokens']
    passed = row.get('passed')
    row.update(total_tokens=tokens,
        test_outcome=('valid_tests' if passed and passed > 0 else 'no_valid_tests' if passed == 0 else 'unknown'),
        passing_tests_per_million_tokens=passed * 1e6 / tokens if tokens else None,
        tokens_per_passing_test=tokens / passed if tokens is not None and passed else None,
        seconds_per_passing_test=row['worker_seconds'] / passed if row.get('worker_seconds') is not None and passed else None,
        truncated_call_pct=percentage(row['truncated_calls'], row['calls']),
        probe_attempts=len(probes), probe_acceptances=sum(p.get('accepted') is True for p in probes),
        probe_acceptance_pct=percentage(sum(p.get('accepted') is True for p in probes),len(probes)),
        probe_seconds=sum(p.get('process',{}).get('seconds',0) or 0 for p in probes) if probes else None)
    row['error_categories'] = {category:sum(e.get('category') == category for e in errors)
        for category in ('generation','import','setup','assertion','other')}
    operations = {}
    for call in calls:
        if call.get('_invalid_record'): continue
        name = call.get('upstream_operation','unknown')
        item = operations.setdefault(name,dict(calls=0,input_tokens=0,output_tokens=0,seconds=0.,truncated_calls=0))
        item['calls'] += 1
        for key in ('input_tokens','output_tokens','seconds'): item[key] += call.get(key,0) or 0
        item['truncated_calls'] += int(bool(call.get('truncated')))
    row['operations'] = operations


def collect(root):
    rows, experiments, mutants, probes, stages, warnings = [], [], [], [], [], []
    manifests = sorted(Path(root).rglob('experiment.json'))
    for manifest in manifests:
        experiment = manifest.parent
        settings = read(manifest)
        comparison = read(experiment / 'comparison.json')
        validation_only = comparison.get('validation_only', False)
        experiments.append(dict(experiment=str(experiment), status=comparison.get('status','running_or_unknown'),
                                validation_only=validation_only, wall_seconds=comparison.get('total_seconds'),
                                jobs=comparison.get('execution',{}).get('jobs'),
                                generation_wall_seconds=comparison.get('comparison_wall_seconds')))
        if validation_only:
            continue
        modes = [mode for mode in MODES if (experiment / mode).exists()]
        if not modes:
            warnings.append(dict(experiment=str(experiment), mode=None, issue='No arm artifacts; preflight failures are not quality scores'))
            continue
        # All modes declared by the comparison are expected, including a missing/failed arm.
        modes = list(MODES) if settings.get('mode')=='compare' or len(modes) > 1 else modes
        for mode in modes:
            work = experiment / mode
            report = read(work / 'report.json')
            score = report.get('score') or read(work / 'score.json')
            original = read(work / 'original/pytest.json')
            call = call_statistics(work / 'model_calls.jsonl')
            versions = report.get('versions') or read(experiment / 'environment.json')
            effective = dict(settings, **report.get('settings', {}))
            cohort = dict(upstream=effective.get('upstream'), model=effective.get('model'),
                model_revision=effective.get('model_revision'), embedding=effective.get('embedding'),
                embedding_revision=effective.get('embedding_revision'), runtime=effective.get('runtime'),
                generation=effective.get('generation'), rounds=effective.get('rounds'),
                repair_policy=effective.get('repair_policy'), source_hashes=effective.get('source_hashes'),
                scenario_prompt=effective.get('scenario_prompt'), source_path=effective.get('source_path'),
                python=versions.get('python'), packages=versions.get('packages'), cpu_threads=effective.get('cpu_threads'))
            collected = original.get('summary',{}).get('collected', original.get('summary',{}).get('total'))
            if collected is None:
                collected = (score.get('original_summary') or {}).get('collected', (score.get('original_summary') or {}).get('total'))
            selection = read(work / 'selection.json')
            row = dict(experiment=str(experiment), mode=mode, status=report.get('status','missing_or_running'),
                score_status=score.get('status'), cohort=digest(cohort)[:16],
                target=f"{effective.get('target_commit')}:{effective.get('target_module')}.{effective.get('target_function')}",
                model=effective.get('model'), model_revision=effective.get('model_revision'),
                embedding_revision=effective.get('embedding_revision'), seed=effective.get('seed'),
                do_sample=(effective.get('generation') or {}).get('do_sample'), jobs=comparison.get('execution',{}).get('jobs'),
                passed=score.get('passed'), collected=collected, retained_files=report.get('retained_pytest_files'),
                retained_test_pass_pct=percentage(score.get('passed'), collected) if collected else None,
                mutation_score=score.get('mutation_score'), mutant_pool_hash=score.get('mutant_pool_hash'),
                selection=selection.get('selected'), candidate_hash=selection.get('candidate_hash'),
                probes_used=selection.get('probes'), setup_complete=selection.get('complete'),
                worker_seconds=report.get('worker_seconds'),
                arm_seconds=comparison.get('arms',{}).get(mode,{}).get('total_seconds'),
                peak_allocated_gib=report.get('gpu_peak_allocated_gib'), peak_reserved_gib=report.get('gpu_peak_reserved_gib'),
                calls=call['calls'], raw_generation_calls=call['raw_generation_calls'],
                input_tokens=(report.get('input_tokens',call['input_tokens']) if report.get('status')=='complete' else call['input_tokens']) if call['calls'] or 'input_tokens' in report else None,
                output_tokens=(report.get('output_tokens',call['output_tokens']) if report.get('status')=='complete' else call['output_tokens']) if call['calls'] or 'output_tokens' in report else None,
                model_seconds=call['model_seconds'] if call['calls'] else None,
                truncated_calls=call['truncated_calls'], initialization_trace_hash=call['initialization_trace_hash'],
                comparability_complete=all(effective.get(key) is not None for key in
                    ('model','model_revision','embedding_revision','upstream','target_commit','generation','rounds','source_hashes','seed'))
                    and bool(versions.get('python')) and bool(versions.get('packages')),
                complete_artifact=report.get('status')=='complete' and score.get('status') in {'scored','no_generated_tests'})
            row.update(scoped_coverage(score, effective.get('target_function','get_custom_loader')))
            errors = list(records(work / 'errors.jsonl'))
            row['error_events'] = len(errors)
            row['setup_error_events'] = sum(e.get('category')=='setup' for e in errors)
            row['code_versions_archived'] = sum(1 for _ in records(work / 'test_attempts.jsonl'))
            # Unique-branch denominator and first-pass/setup-success labels are not fabricated.
            row['first_pass_rate'] = None
            row['setup_failure_rate'] = None
            row['model_phase_statistics'] = call['phases']
            effectiveness_metrics(row, work)
            rows.append(row)
            if call['invalid_records']:
                warnings.append(dict(experiment=str(experiment),mode=mode,issue='Incomplete/malformed model log records'))
            for key in ('input_tokens','output_tokens'):
                if report.get('status')=='complete' and key in report and report[key] != call[key]:
                    warnings.append(dict(experiment=str(experiment),mode=mode,issue=f'{key}: report/model-log mismatch'))
            for mutant in score.get('mutants',[]):
                mutants.append(dict(experiment=str(experiment),mode=mode,name=mutant.get('name'),
                    verdict=mutant.get('verdict'),sha256=mutant.get('sha256'),pool_hash=score.get('mutant_pool_hash')))
            for probe in records(work / 'probes.jsonl'):
                probes.append(dict(experiment=str(experiment),mode=mode,candidate=probe.get('candidate_id'),
                    scenario=probe.get('scenario'),accepted=probe.get('accepted'),reason=probe.get('reason'),
                    seconds=probe.get('process',{}).get('seconds'),timeout=probe.get('process',{}).get('timeout')))
            for phase, value in report.get('stages',{}).items():
                stages.append(dict(experiment=str(experiment),mode=mode,phase=phase,seconds=value,
                    additive=phase in {'model_load','setup_total','initialization','generation_repair_coverage','scoring'}))
        arm_rows = [row for row in rows if row['experiment']==str(experiment)]
        for field in ('cohort','mutant_pool_hash','initialization_trace_hash'):
            values = {row[field] for row in arm_rows if row.get(field)}
            if len(values)>1:
                warnings.append(dict(experiment=str(experiment),mode=None,issue=f'Across-arm mismatch: {field}'))
    return rows, experiments, mutants, probes, stages, warnings


def paired_rows(rows):
    pairs = []
    for experiment in sorted({row['experiment'] for row in rows}):
        arms = {row['mode']: row for row in rows if row['experiment']==experiment}
        verified = arms.get('verified')
        if not verified:
            continue
        for comparator in ('baseline','caller','extracted'):
            other = arms.get(comparator)
            valid = bool(other and verified['complete_artifact'] and other['complete_artifact']
                         and verified['cohort']==other['cohort']
                         and verified.get('comparability_complete') and other.get('comparability_complete')
                         and verified['target']==other['target'] and verified['seed']==other['seed']
                         and (comparator!='extracted' or (verified.get('candidate_hash') and verified['candidate_hash']==other.get('candidate_hash'))))
            common_pool = bool(other and other.get('mutant_pool_hash') and other['mutant_pool_hash']==verified.get('mutant_pool_hash'))
            row = dict(experiment=experiment, comparator=comparator, valid_pair=valid,
                common_mutant_pool=common_pool, cohort=verified['cohort'], target=verified['target'],
                same_setup=(verified.get('selection')==other.get('selection')) if other and comparator=='extracted' and verified.get('selection') and other.get('selection') else None)
            for metric in ('target_branch_pct','target_line_pct','module_branch_pct','passed','input_tokens','output_tokens','worker_seconds','mutation_score'):
                a, b = verified.get(metric), (other or {}).get(metric)
                row['delta_'+metric] = a-b if valid and a is not None and b is not None and (metric!='mutation_score' or common_pool) else None
            pairs.append(row)
    return pairs


def make_plots(output, rows):
    measured = [row for row in rows if row['complete_artifact']]
    if not measured:
        return dict(status='no_completed_measurements', files=[])
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return dict(status='matplotlib_unavailable', files=[], install='python -m pip install -r requirements-analysis.txt')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.fonttype':'none','pdf.fonttype':42})
    destination = output / 'figures'
    destination.mkdir()
    files = []
    for index, cohort in enumerate(sorted({row['cohort'] for row in measured})):
        group = [row for row in measured if row['cohort']==cohort]
        fig, axes = plt.subplots(1,3,figsize=(12,3.8), constrained_layout=True)
        for ax, metric, label in zip(axes, ('target_branch_pct','mutation_score','worker_seconds'),
                                    ('Target + nested branch coverage (%)','Two-mutant pilot score (0–1)','Worker time (s; includes contention)')):
            for experiment in sorted({row['experiment'] for row in group}):
                values = {row['mode']: row.get(metric) for row in group if row['experiment']==experiment}
                points = [values.get(mode) if values.get(mode) is not None else float('nan') for mode in MODES]
                if any(values.get(mode) is not None for mode in MODES):
                    ax.plot(range(4),points,marker='o',alpha=.6)
            if not any(row.get(metric) is not None for row in group):
                ax.text(.5,.5,'No measured values',ha='center',va='center',transform=ax.transAxes)
            ax.set_xticks(range(4),MODES,rotation=25)
            ax.set_ylabel(label)
            ax.grid(alpha=.2)
            if metric=='mutation_score':
                ax.set_ylim(-.05,1.05)
                ax.set_yticks([0,.5,1])
            if metric=='target_branch_pct': ax.set_ylim(-5,105)
        fig.suptitle(f'Observed pilot arms · cohort {cohort} · no inferential CI')
        for ext in ('svg','pdf','png'):
            name=f'cohort_{index+1}_observed.{ext}'
            fig.savefig(destination/name,dpi=300)
            files.append('figures/'+name)
        plt.close(fig)
        fig, axes = plt.subplots(1,2,figsize=(9,3.8), constrained_layout=True)
        palette = dict(zip(MODES, ('#4C78A8','#F58518','#54A24B','#B279A2')))
        for mode in MODES:
            subset = [row for row in group if row['mode']==mode]
            values = [(row['input_tokens']+row['output_tokens'], row['target_branch_pct']) for row in subset
                      if row.get('input_tokens') is not None and row.get('output_tokens') is not None and row.get('target_branch_pct') is not None]
            if values: axes[0].scatter(*zip(*values),label=mode,color=palette[mode])
            values = [(row['worker_seconds'],row['mutation_score']) for row in subset
                      if row.get('worker_seconds') is not None and row.get('mutation_score') is not None]
            if values: axes[1].scatter(*zip(*values),label=mode,color=palette[mode])
        axes[0].set(xlabel='Total measured input + output tokens',ylabel='Target + nested branch coverage (%)',ylim=(-5,105))
        axes[1].set(xlabel='Worker time (s; includes contention)',ylabel='Two-mutant pilot score (0–1)',ylim=(-.05,1.05))
        axes[1].set_yticks([0,.5,1])
        for ax in axes:
            ax.grid(alpha=.2)
            handles, labels = ax.get_legend_handles_labels()
            if handles: ax.legend()
        fig.suptitle(f'Observed cost/quality tradeoffs · cohort {cohort}')
        for ext in ('svg','pdf','png'):
            name=f'cohort_{index+1}_cost_quality.{ext}'
            fig.savefig(destination/name,dpi=300)
            files.append('figures/'+name)
        plt.close(fig)
    return dict(status='created', files=files, matplotlib_version=matplotlib.__version__)


def gpu_records(experiments):
    rows = []
    for experiment in experiments:
        if experiment['validation_only']:
            continue
        for frame in records(Path(experiment['experiment'])/'gpu_usage.jsonl'):
            for gpu in frame.get('gpus',[]):
                rows.append(dict(experiment=experiment['experiment'], time=frame.get('time'), **gpu))
    return rows


def file_hash(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1_048_576), b''):
            value.update(block)
    return value.hexdigest()


def provenance(experiments):
    files=[]
    for experiment in experiments:
        base=Path(experiment['experiment'])
        paths=[base/'experiment.json',base/'comparison.json',base/'environment.json']
        for mode in MODES:
            paths += [base/mode/name for name in ('report.json','score.json','selection.json','model_calls.jsonl',
                'probes.jsonl','errors.jsonl','test_attempts.jsonl','mutant_pool.json')]
        for path in paths:
            if not path.exists():
                continue
            before=path.stat()
            sha=file_hash(path)
            after=path.stat()
            files.append(dict(path=str(path),bytes=after.st_size,sha256=sha,
                              stable_during_hash=before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns))
    return files


def discover_runs(roots, max_depth=10, max_directories=10000):
    """Bounded artifact search, pruning source checkouts and package/model caches."""
    found, visited, truncated = {}, 0, False
    prune={'.git','__pycache__','upstream','PyCG','mutants','node_modules','site-packages','.cache','research_reports'}
    for root in map(Path,roots):
        if not root.is_dir():
            continue
        for directory, names, files in os.walk(root, followlinks=False):
            visited += 1
            if visited > max_directories:
                truncated = True
                break
            directory=Path(directory)
            depth=len(directory.relative_to(root).parts)
            names[:]=sorted(name for name in names if name not in prune and not name.startswith('.venv')) if depth<max_depth else []
            if 'experiment.json' not in files:
                continue
            settings=read(directory/'experiment.json')
            if settings.get('target_function')!='get_custom_loader':
                continue
            comparison=read(directory/'comparison.json')
            arms=[read(directory/mode/'report.json') for mode in MODES]
            recorded=sum(bool(arm) for arm in arms)
            row=dict(path=str(directory.resolve()),status=comparison.get('status','running_or_unknown'),
                recorded=recorded,completed=sum(arm.get('status')=='complete' for arm in arms),
                validation_only=comparison.get('validation_only',False),
                modified=(directory/'experiment.json').stat().st_mtime)
            found[row['path']]=row
        if truncated:
            break
    # Most recent experiment, NOT best quality or highest completion count.
    return sorted(found.values(),key=lambda row:(row['modified'],row['path']),reverse=True),truncated


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('auto'),help='artifact folder, or auto to find the latest run')
    parser.add_argument('--list-runs',action='store_true',help='list discovered artifact folders without analyzing')
    parser.add_argument('--search-root',type=Path,action='append',help='search roots (default: /kaggle/working and /kaggle/input)')
    parser.add_argument('--output',type=Path,default=Path('research_reports/pilot'))
    parser.add_argument('--plots',action='store_true')
    args=parser.parse_args()
    if args.list_runs or str(args.input)=='auto':
        candidates,truncated=discover_runs(args.search_root or [Path('/kaggle/working'),Path('/kaggle/input')])
        for row in candidates[:20]:
            kind='validation' if row['validation_only'] else 'experiment'
            print(f"{row['path']} | {kind} | {row['status']} | completed={row['completed']} recorded={row['recorded']}")
        if truncated:
            print('Search limit reached; use --search-root to narrow the search.')
        if args.list_runs:
            if not candidates:
                print('No pilot artifacts found. Restore saved Notebook outputs using Add Input, or run an experiment first.')
            return 0
        usable=[row for row in candidates if row['recorded'] and not row['validation_only']]
        if not usable:
            parser.error('No experimental arm artifacts found. Source alone is not results. Restore saved Notebook outputs via Add Input, use --search-root for their location, or run a new experiment if results were not saved.')
        args.input=Path(usable[0]['path'])
        print(f'Auto-selected most recent artifact run: {args.input}; use --input PATH to select another run.')
    if not args.input.is_dir():
        parser.error(f'Input directory does not exist: {args.input}. Use --input auto or --list-runs to locate saved artifacts.')
    output=reserve_output(args.output)
    rows,experiments,mutants,probes,stages,warnings=collect(args.input)
    pairs=paired_rows(rows)
    gpus=gpu_records(experiments)
    csv_table(output/'gpu_trace.csv',gpus,['experiment','time','index','uuid','name','utilization_percent','used_mib','total_mib'])
    fields=['experiment','mode','status','score_status','cohort','target','model','model_revision','embedding_revision','seed','do_sample','jobs',
        'passed','collected','retained_test_pass_pct','retained_files','target_branch_pct','target_line_pct','loader_init_branch_pct','module_branch_pct',
        'mutation_score','input_tokens','output_tokens','calls','raw_generation_calls','code_versions_archived','model_seconds','worker_seconds','arm_seconds',
        'peak_allocated_gib','peak_reserved_gib','probes_used','setup_complete','selection','candidate_hash','mutant_pool_hash','initialization_trace_hash',
        'error_events','setup_error_events','truncated_calls','first_pass_rate','setup_failure_rate','target_scopes','comparability_complete','complete_artifact']
    fields += ['test_outcome','total_tokens','passing_tests_per_million_tokens','tokens_per_passing_test',
        'seconds_per_passing_test','truncated_call_pct','probe_attempts','probe_acceptances','probe_acceptance_pct','probe_seconds','error_categories']
    csv_table(output/'arms.csv',rows,fields)
    operation_rows = [dict(experiment=r['experiment'],mode=r['mode'],operation=k,**v) for r in rows for k,v in r['operations'].items()]
    csv_table(output/'model_operations.csv',operation_rows,['experiment','mode','operation','calls','input_tokens','output_tokens','seconds','truncated_calls'])
    diagnostics=[]
    for r in rows:
        work=Path(r['experiment'])/r['mode']
        diagnostics.append(dict(experiment=r['experiment'],mode=r['mode'],execution_status=r['status'],
            test_outcome=r['test_outcome'],error_event_categories=r['error_categories'],
            recent_errors=[dict(category=e.get('category'),check=e.get('check'),message=str(e.get('message',''))[:2000])
                for e in list(records(work/'errors.jsonl'))[-3:]],
            limitation='Heuristic error events may repeat per test; not first-pass or causal setup-failure rates.'))
    write_json(output/'diagnostics.json',diagnostics)
    csv_table(output/'experiments.csv',experiments,['experiment','status','validation_only','wall_seconds','jobs','generation_wall_seconds'])
    csv_table(output/'mutants.csv',mutants,['experiment','mode','name','verdict','sha256','pool_hash'])
    csv_table(output/'probes.csv',probes,['experiment','mode','candidate','scenario','accepted','reason','seconds','timeout'])
    csv_table(output/'stages.csv',stages,['experiment','mode','phase','seconds','additive'])
    phase_rows = [dict(experiment=row['experiment'],mode=row['mode'],phase=phase,**values)
                  for row in rows for phase,values in row['model_phase_statistics'].items()]
    csv_table(output/'model_phases.csv',phase_rows,['experiment','mode','phase','calls','input_tokens','output_tokens','seconds'])
    pair_fields=['experiment','comparator','valid_pair','common_mutant_pool','cohort','target','same_setup']
    pair_fields += ['delta_'+key for key in ('target_branch_pct','target_line_pct','module_branch_pct','passed','input_tokens','output_tokens','worker_seconds','mutation_score')]
    csv_table(output/'paired_differences.csv',pairs,pair_fields)
    unique_targets=len({row['target'] for row in rows if row['complete_artifact']})
    summary=dict(experiments=len(experiments),arm_records=len(rows),completed_arm_records=sum(row['complete_artifact'] for row in rows),
        unique_completed_targets=unique_targets,valid_pairs=sum(row['valid_pair'] for row in pairs),
        inference='descriptive_only: this pilot does not establish independent multi-target/project evidence',
        missing_values='blank/NA, never imputed as zero',warnings=warnings)
    summary['plots']=make_plots(output,rows) if args.plots else dict(status='not_requested',files=[])
    write_json(output/'summary.json',summary)
    write_json(output/'analysis_manifest.json',dict(captured_at=datetime.now(timezone.utc).isoformat(),
        input=str(args.input.resolve()),analysis_sha256=file_hash(Path(__file__)),
        inference_policy=summary['inference'],artifacts=provenance(experiments)))
    lines=['# Pilot evidence report','',f'Experiments: {len(experiments)}; completed arm records: {summary["completed_arm_records"]}; unique completed targets: {unique_targets}.','',
        '**Descriptive pilot only. No claim of superiority or statistical significance.**',
        'Missing results remain NA. Validation oracle scores are excluded from generated-test results.',
        'Rows may include failed/running arms; effect differences require compatible completed pairs.', '',
        '| Mode | Completed / recorded | Retained tests passed | Target branch % | Pilot mutation score |',
        '|---|---:|---:|---:|---:|']
    for mode in MODES:
        group=[row for row in rows if row['mode']==mode]
        complete=[row for row in group if row['complete_artifact']]
        # Do not pool differing cohorts. One value per observed arm is explicit.
        def values(key): return ', '.join(str(round(row[key],3)) for row in complete if row.get(key) is not None) or 'NA'
        lines.append(f'| {mode} | {len(complete)} / {len(group)} | {values("passed")} | {values("target_branch_pct")} | {values("mutation_score")} |')
    lines += ['', '## Effectiveness and cost', '',
        '| Mode | Outcome | Total tokens | Pass / million tokens | Truncated calls % | Probe accepted / attempted |',
        '|---|---|---:|---:|---:|---:|']
    for r in rows:
        def fmt(key): return str(round(r[key],3)) if isinstance(r.get(key),(int,float)) else 'NA'
        lines.append(f"| {r['mode']} | {r['test_outcome']} | {fmt('total_tokens')} | {fmt('passing_tests_per_million_tokens')} | {fmt('truncated_call_pct')} | {r['probe_acceptances']} / {r['probe_attempts']} |")
    if any(r['test_outcome']=='no_valid_tests' for r in rows):
        lines += ['', 'Execution completion does not imply successful test generation. Zero-pass arms provide no eligible mutation evidence. Cost per passing test is undefined, not zero. Diagnose errors and generation/repair operations before another full run.']
    lines += ['', 'Each listed value is an arm observation, not a pooled mean. Use cohort IDs in arms.csv.',
        'No first-pass or true setup-failure rates are reconstructed from retained passing suites or heuristic error events.',
        'No target coverage is substituted with module coverage. No mutation pool mismatch is silently pooled.',
        'No confidence interval is computed by treating repeated runs of the same target as independent functions.',
        '', '## Audit warnings','']
    lines += ['- '+row['experiment']+': '+row['issue'] for row in warnings] or ['- None detected in available artifacts. Missing final data is still missing evidence.']
    (output/'report.md').write_text('\n'.join(lines)+'\n')
    print(f'Research report: {output}\nCompleted arms: {summary["completed_arm_records"]}; targets: {unique_targets}\nCharts: {summary["plots"]["status"]}')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
