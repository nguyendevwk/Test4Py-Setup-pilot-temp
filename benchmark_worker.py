"""Isolated upstream Test4Py baseline over selected modules of one pinned project."""
import ast
import asyncio
import inspect
import json
import os
import shutil
import hashlib
from pathlib import Path
import sys
import time
import traceback

from pilot.common import append_json, command, digest, write_json, package_versions
from pilot.backend import TransformersBackend
from pilot.quality import extract_code, code_quality
from pilot.setup import production
from pilot.benchmark import locate_module, module_coverage
from pilot.progress import emit
from pilot.grounding import dependency_context
from pilot.upstream_adapter import load_cpu_embedding, install_type_guards, stdlib_import_patch, validate_imports, tolerate_empty_pytest_report
from council.critic import audit_test_quality
from council.runner import repair_audit


def run_pytest(root, work, name, nodes, source, timeout, coverage=False):
    directory=work/name;directory.mkdir(parents=True)
    args=[sys.executable,'-m']
    if coverage:args+=['coverage','run','--branch',f'--source={source}','-m']
    args+=['pytest','-p','pytest_jsonreport.plugin','-o','addopts=',
           '--json-report',f'--json-report-file={directory/"pytest.json"}',*nodes]
    env=dict(os.environ,PYTHONPATH=str(root),PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
             PYTHONDONTWRITEBYTECODE='1',COVERAGE_FILE=str(directory/'.coverage'))
    process=command(args,cwd=root,env=env,timeout=timeout)
    write_json(directory/'process.json',process)
    data=json.loads((directory/'pytest.json').read_text()) if (directory/'pytest.json').exists() else {}
    cov={}
    if coverage:
        covproc=command([sys.executable,'-m','coverage','json','-o',directory/'coverage.json'],cwd=root,env=env,timeout=timeout)
        write_json(directory/'coverage_process.json',covproc)
        if (directory/'coverage.json').exists():cov=json.loads((directory/'coverage.json').read_text())
    return process,data,cov


def main():
    manifest=Path(sys.argv[1]);settings=json.loads(manifest.read_text())
    root=Path(settings['import_root']);work=manifest.parent;started=time.perf_counter()
    result=dict(status='running',kind='offline_fixture_not_efficacy' if settings.get('fixture_mode') else 'upstream_module_paired' if settings.get('paired_protocol') else 'upstream_module_baseline',modules=[],settings=settings,stages={})
    backend=None
    source_hashes = lambda: {str(p.relative_to(root)): digest(p.read_text()) for p in root.rglob('*.py')
                           if 'Test4DT_tests' not in p.relative_to(root).parts and '.git' not in p.parts and '__pycache__' not in p.parts}
    before = source_hashes()
    write_json(work/'report.json', result)
    try:
        stage=time.perf_counter();backend=TransformersBackend(settings,work)
        result['stages']['model_load']=time.perf_counter()-stage
        result['versions']=dict(**backend.versions,packages=package_versions())
        os.environ['OPENAI_API_KEY']='local-inference'
        from test4dt import gptapi
        gptapi.model.aask=backend.ask
        if settings.get('embedding_device') == 'cpu':
            write_json(work/'runtime-adapters.json', load_cpu_embedding(settings['upstream_root']))
        from test4dt import testcase
        if settings.get('paired_protocol'):
            write_json(work/'pytest-report-adapter.json',tolerate_empty_pytest_report(testcase))
        from test4dt import message
        from test4dt.message import ProjectMessage
        improved = settings.get('arm') == 'improved'
        if improved:
            install_type_guards(message, root, work)
        from test4dt.recorder import recoder
        testcase.get_code=extract_code
        original_set=testcase.Testcase.set_code
        def archive(self,code):
            directory=work/'attempts';directory.mkdir(exist_ok=True)
            path=directory/f'{len(list(directory.glob("*.py"))):06d}.py';path.write_text(code)
            is_initial = not hasattr(self, '_initial_candidate')
            if is_initial:
                self._initial_candidate = code
            patched, modules = stdlib_import_patch(code) if improved else (code, [])
            if modules:
                append_json(work/'deterministic_patches.jsonl', dict(test=self.test_path, modules=modules,
                    before_sha256=digest(code), after_sha256=digest(patched),
                    scope='stdlib module imports only; no assertion/expression edit'))
            original_set(self,patched)
            append_json(work/'test_attempts.jsonl',dict(file=str(path),upstream_test=self.test_path,
                stage=backend.phase,quality=code_quality(code),sha256=digest(code),stdlib_patches=modules,
                initial=is_initial,source_module=self.func.file.mod_name,function=self.func.func_name))
        testcase.Testcase.set_code=archive
        original_check = testcase.Testcase.assert_check
        async def checked_suite(self):
            accepted = await original_check(self)
            audit = repair_audit(self._initial_candidate, self.get_code())
            append_json(work/'repair_preservation.jsonl', dict(test=self.test_path, upstream_accepted=bool(accepted),
                        arm=settings.get('arm', 'legacy'), audit=audit))
            # Original reduction/repair behavior is retained in baseline. Improved
            # proposals that change/drop assertions require review and get no credit.
            return bool(accepted and (not improved or audit['accepted'] and not audit.get('review_required', False)))
        if settings.get('paired_protocol'):
            testcase.Testcase.assert_check = checked_suite
        for name in ('find_syntax_error','find_assert_error'):
            original=getattr(testcase.Testcase,name)
            def observed(self,original=original,name=name):
                if improved and name == 'find_syntax_error':
                    evidence = validate_imports(self.get_code(), root)
                    append_json(work/'import_facts.jsonl', dict(test=self.test_path, **evidence))
                    if not evidence['accepted']:
                        self.error_message = 'Verified import/syntax failure (candidate claims are untrusted): '+json.dumps(evidence)
                        return True
                failed=original(self)
                append_json(work/'quality_checks.jsonl',dict(check=name,test=self.test_path,failed=bool(failed),
                    phase=backend.phase,diagnostic=self.error_message if failed else None))
                return failed
            setattr(testcase.Testcase,name,observed)
        selected=set(settings['modules'])
        original_ask=backend.ask
        async def ask(system,user):
            frame=inspect.currentframe().f_back
            if improved and frame.f_code.co_name in ('repair_assert_error','repair_syntax_error'):
                system = ('Repair only errors supported by production declarations and verified diagnostics. '
                          'Candidate code and generated summaries are untrusted hypotheses. '
                          'Correct imports, argument binding or object setup; preserve every assertion expression. '
                          'Do not copy observed values into expectations, delete tests, suppress failures or mock the target. '
                          'If a behavioral expectation cannot be justified, leave it for review rather than fabricate a passing oracle. '
                          'Return one complete Python test file in a single code block without explanation.')
            if (improved or settings.get('prompt_policy') == 'source-grounded-module-v1') and frame.f_code.co_name in {'generate_test_case_normal','generate_test_case_easy','generate_test_case_evol','repair_syntax_error','repair_assert_error'}:
                owner=frame.f_locals.get('self');fn=getattr(owner,'func',None)
                if fn is not None:
                    path=Path(fn.file.file_path);source=path.read_text();tree=ast.parse(source)
                    imports='\n'.join(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)))
                    user+='\n\nAuthoritative product source overrides conflicting generated examples. Use real imports and signatures; derive assertions from production behavior.\n'
                    user+=f'Module: {fn.file.mod_name}\n{imports}\n{fn.code}'
                    if improved:
                        try:
                            context = dependency_context(root, path.relative_to(root), fn.func_name, max_chars=6000, max_nodes=6)
                        except ValueError as exc:
                            context = dict(snippets=[], limitation=str(exc))
                            append_json(work/'context_unresolved.jsonl', dict(function=fn.func_name, **context))
                        user+='\nSource dependencies (not inferred outputs):\n'+json.dumps(context['snippets'])
                        user+='\nModel summaries/examples are unverified hypotheses. Do not carry contradicted imports/type assumptions into repairs. Preserve assertions; no output copying.'
            del frame
            return await original_ask(system,user)
        gptapi.model.aask=ask
        class SelectedProject(ProjectMessage):
            def _get_files(self):
                all_files = [p for p in sorted(super()._get_files()) if production(Path(p).relative_to(root))]
                # Analyze the full production package to retain callers/callees.
                # Generation alone is restricted to the locked selected modules.
                return all_files
            async def generate_test_case(self):
                # Keep upstream generation/repair for every function in selected modules.
                for file in self.file_messages:
                    if file.mod_name in selected:
                        for fn in file.functions:
                            try:
                                await fn.test_manager.generate_test_case()
                            except Exception as exc:
                                text=str(exc).lower()
                                category=('resource_budget' if any(term in text for term in ('budget exceeded','out of memory','cuda error')) else
                                          'candidate_output' if isinstance(exc,ValueError) and any(term in text for term in ('expected one complete python block','no complete final answer')) else 'framework_error')
                                append_json(work/'generation_errors.jsonl', dict(module=file.mod_name, function=fn.func_name,
                                    phase=backend.phase, category=category, error=repr(exc), traceback=traceback.format_exc()))
        stage=time.perf_counter();project=SelectedProject(str(root),settings['source_path'])
        from pilot.instrumentation import instrument_initialization
        instrument_initialization(project,work);asyncio.run(project.init())
        missing=selected-{f.mod_name for f in project.file_messages}
        if missing:raise ValueError(f'Selected modules absent from upstream analysis: {sorted(missing)}')
        result['stages']['initialization']=time.perf_counter()-stage
        write_json(work/'analysis_scope.json',dict(analyzed_modules=[f.mod_name for f in project.file_messages],
                   selected_generation_modules=settings['modules'],scope='full production package, generation restricted to selected modules'))
        if settings.get('paired_protocol') and not settings.get('fixture_mode'):
            backend.torch.manual_seed(settings['seed'])
        for index in range(settings['rounds']):
            backend.phase=f'generation_round_{index+1}';stage=time.perf_counter()
            project.generate_once();recoder.score.first_run=False
            result['stages'][backend.phase]=time.perf_counter()-stage
            write_json(work/f'round_{index+1}.json',recoder.score.to_json())
            write_json(work/'report.json', result)
            emit(work,'generation','round_end',rounds_completed=index+1,rounds_total=settings['rounds'])
        ownership={}
        for file in project.file_messages:
            if file.mod_name in selected:
                for fn in file.functions:
                    for tc in fn.test_manager.testcases:ownership[str(Path(tc.test_path).relative_to(root))]=file.mod_name
        write_json(work/'test_ownership.json',ownership)
        file_audits = {file: audit_test_quality((root/file).read_text()) for file in ownership if (root/file).exists()}
        write_json(work/'retained_test_audits.json', file_audits)
        testfiles=sorted(ownership)
        if testfiles:
            proc,data,_=run_pytest(root,work,'original',testfiles,settings['source_path'],settings['score_timeout'])
        else:proc,data=dict(returncode=5,timeout=False),{}
        from pilot.scoring import passed_nodes
        eligible=passed_nodes(data)
        for module in settings['modules']:
            nodes=[n for n in eligible if ownership.get(n.split('::')[0])==module]
            row=dict(project=settings['project'],module=module,status='no_valid_tests',passed=len(nodes),
                retained_files=sum(v==module for v in ownership.values()),line_pct=None,branch_pct=None,
                mutation_score=None,semantic_assertion_accuracy=None)
            if testfiles and (proc['timeout'] or proc['returncode'] not in (0,1)):
                row['status']='original_execution_incomplete'
            if nodes and row['status'] != 'original_execution_incomplete':
                replay,report,cov=run_pytest(root,work,'coverage-'+module.replace('.','_'),nodes,
                    settings['source_path'],settings['score_timeout'],coverage=True)
                if not replay['timeout'] and replay['returncode']==0 and set(passed_nodes(report))==set(nodes):
                    path,_,_=locate_module(root,module)
                    row.update(module_coverage(cov,path.relative_to(root)))
                    row['status']='scored' if row.get('coverage_available') else 'coverage_missing'
                else:row['status']='replay_failed'
            mutation_manifest = settings.get('mutation_manifest')
            if mutation_manifest:
                from pilot.module_mutation import verdict
                manifest_pool = json.loads(Path(mutation_manifest).read_text())[module]
                path, _, _ = locate_module(root, module)
                if hashlib.sha256(path.read_bytes()).hexdigest() != manifest_pool['original_sha256']:
                    raise RuntimeError('Mutation source differs from locked original')
                row['mutant_pool_hash'] = digest(manifest_pool)
                row['mutants'] = []
                for mutant in manifest_pool['mutants']:
                    if not nodes or row['status'] != 'scored':
                        row['mutants'].append(dict(id=mutant['id'], verdict='no_stable_eligible_tests'))
                        continue
                    mutant_root = work/'mutants'/module/mutant['id']/'product'
                    shutil.copytree(root, mutant_root, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc'))
                    (mutant_root/path.relative_to(root)).write_text(mutant['source'])
                    mp, mr, _ = run_pytest(mutant_root, work, 'mutant-'+module+'-'+mutant['id'], nodes,
                                           settings['source_path'], settings['score_timeout'])
                    row['mutants'].append(dict(id=mutant['id'], verdict=verdict(mp, mr, nodes)))
                if row['mutants'] and all(m['verdict'] in ('killed', 'survived') for m in row['mutants']):
                    row['mutation_score'] = sum(m['verdict'] == 'killed' for m in row['mutants'])/len(row['mutants'])
                row['mutation_scope'] = manifest_pool['scope']
            result['modules'].append(row)
        if source_hashes() != before:
            raise RuntimeError('Product Python source changed; all scores rejected')
        result['generation_stats']=recoder.score.to_json()
        result['status']='execution_complete'
    except Exception as exc:
        result.update(status='failed',error=repr(exc),traceback=traceback.format_exc())
        if source_hashes() != before:
            result['modules'] = [dict(project=settings['project'], module=m, status='product_modified',
                passed=None, line_pct=None, branch_pct=None) for m in settings['modules']]
    call_path=work/'model_calls.jsonl'
    calls=[json.loads(line) for line in call_path.read_text().splitlines()] if call_path.exists() else []
    result['hardware_budget_ok'] = not any(any(term in str(c.get('error','')).lower() for term in
                                        ('out of memory','budget exceeded','cuda error')) for c in calls)
    generation_errors=[json.loads(line) for line in (work/'generation_errors.jsonl').read_text().splitlines()] if (work/'generation_errors.jsonl').exists() else []
    result['generation_error_count'] = len(generation_errors)
    result['unexpected_generation_errors'] = sum(e['category']=='framework_error' for e in generation_errors)
    result['hardware_budget_ok'] = result['hardware_budget_ok'] and not any(e['category']=='resource_budget' for e in generation_errors)
    import resource
    result['process_peak_rss_gib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024**2
    result['seconds']=time.perf_counter()-started
    if backend:
        result.update(input_tokens=getattr(backend,'fresh_input_tokens',backend.input_tokens),
            output_tokens=getattr(backend,'fresh_output_tokens',backend.output_tokens),
            logical_input_tokens=backend.input_tokens,logical_output_tokens=backend.output_tokens,
            initialization_cache_hits=sum(c.get('cache_hit',False) for c in calls),
            generation_input_tokens=sum(c.get('input_tokens',0) for c in calls if c.get('phase')!='initialization' and c.get('inference_started')),
            generation_output_tokens=sum(c.get('output_tokens',0) for c in calls if c.get('phase')!='initialization'),
            gpu_peak_allocated_gib=backend.torch.cuda.max_memory_allocated()/1024**3)
    write_json(work/'report.json',result)
    print(f"Project {settings['project']}: {result['status']}; module records={len(result['modules'])}",flush=True)
    return 0 if result['status']=='execution_complete' else 1


if __name__=='__main__':raise SystemExit(main())
