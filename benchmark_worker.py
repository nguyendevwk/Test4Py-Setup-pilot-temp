"""Isolated upstream Test4Py baseline over selected modules of one pinned project."""
import ast
import asyncio
import inspect
import json
import os
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
    result=dict(status='running',kind='upstream_module_baseline',modules=[],settings=settings,stages={})
    backend=None
    try:
        stage=time.perf_counter();backend=TransformersBackend(settings,work)
        result['stages']['model_load']=time.perf_counter()-stage
        result['versions']=dict(**backend.versions,packages=package_versions())
        os.environ['OPENAI_API_KEY']='local-inference'
        from test4dt import gptapi
        gptapi.model.aask=backend.ask
        from test4dt import testcase
        from test4dt.message import ProjectMessage
        from test4dt.recorder import recoder
        testcase.get_code=extract_code
        original_set=testcase.Testcase.set_code
        def archive(self,code):
            original_set(self,code)
            directory=work/'attempts';directory.mkdir(exist_ok=True)
            path=directory/f'{len(list(directory.glob("*.py"))):06d}.py';path.write_text(code)
            append_json(work/'test_attempts.jsonl',dict(file=str(path),upstream_test=self.test_path,
                stage=backend.phase,quality=code_quality(code),sha256=digest(code)))
        testcase.Testcase.set_code=archive
        for name in ('find_syntax_error','find_assert_error'):
            original=getattr(testcase.Testcase,name)
            def observed(self,original=original,name=name):
                failed=original(self)
                append_json(work/'quality_checks.jsonl',dict(check=name,test=self.test_path,failed=bool(failed),
                    phase=backend.phase,diagnostic=self.error_message if failed else None))
                return failed
            setattr(testcase.Testcase,name,observed)
        selected=set(settings['modules'])
        original_ask=backend.ask
        async def ask(system,user):
            frame=inspect.currentframe().f_back
            if frame.f_code.co_name in {'generate_test_case_normal','generate_test_case_easy','generate_test_case_evol','repair_syntax_error','repair_assert_error'}:
                owner=frame.f_locals.get('self');fn=getattr(owner,'func',None)
                if fn is not None:
                    path=Path(fn.file.file_path);source=path.read_text();tree=ast.parse(source)
                    imports='\n'.join(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)))
                    user+='\n\nAuthoritative product source overrides conflicting generated examples. Use real imports and signatures; derive assertions from production behavior.\n'
                    user+=f'Module: {fn.file.mod_name}\n{imports}\n{fn.code}'
            return await original_ask(system,user)
        gptapi.model.aask=ask
        class SelectedProject(ProjectMessage):
            def _get_files(self):
                return [p for p in sorted(super()._get_files()) if production(Path(p).relative_to(root))]
            async def generate_test_case(self):
                # Keep upstream generation/repair for every function in selected modules.
                for file in self.file_messages:
                    if file.mod_name in selected:
                        for fn in file.functions:await fn.test_manager.generate_test_case()
        stage=time.perf_counter();project=SelectedProject(str(root),settings['source_path'])
        from pilot.instrumentation import instrument_initialization
        instrument_initialization(project,work);asyncio.run(project.init())
        missing=selected-{f.mod_name for f in project.file_messages}
        if missing:raise ValueError(f'Selected modules absent from upstream analysis: {sorted(missing)}')
        result['stages']['initialization']=time.perf_counter()-stage
        for index in range(settings['rounds']):
            backend.phase=f'generation_round_{index+1}';stage=time.perf_counter()
            project.generate_once();recoder.score.first_run=False
            result['stages'][backend.phase]=time.perf_counter()-stage
            write_json(work/f'round_{index+1}.json',recoder.score.to_json())
            emit(work,'generation','round_end',rounds_completed=index+1,rounds_total=settings['rounds'])
        ownership={}
        for file in project.file_messages:
            if file.mod_name in selected:
                for fn in file.functions:
                    for tc in fn.test_manager.testcases:ownership[str(Path(tc.test_path).relative_to(root))]=file.mod_name
        write_json(work/'test_ownership.json',ownership)
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
            if nodes:
                replay,report,cov=run_pytest(root,work,'coverage-'+module.replace('.','_'),nodes,
                    settings['source_path'],settings['score_timeout'],coverage=True)
                if not replay['timeout'] and replay['returncode']==0 and set(passed_nodes(report))==set(nodes):
                    path,_,_=locate_module(root,module)
                    row.update(module_coverage(cov,path.relative_to(root)))
                    row['status']='scored' if row.get('coverage_available') else 'coverage_missing'
                else:row['status']='replay_failed'
            result['modules'].append(row)
        result['generation_stats']=recoder.score.to_json()
        result['status']='execution_complete'
    except Exception as exc:
        result.update(status='failed',error=repr(exc),traceback=traceback.format_exc())
    result['seconds']=time.perf_counter()-started
    if backend:
        result.update(input_tokens=backend.input_tokens,output_tokens=backend.output_tokens,
            gpu_peak_allocated_gib=backend.torch.cuda.max_memory_allocated()/1024**3)
    write_json(work/'report.json',result)
    print(f"Project {settings['project']}: {result['status']}; module records={len(result['modules'])}",flush=True)
    return 0 if result['status']=='execution_complete' else 1


if __name__=='__main__':raise SystemExit(main())
