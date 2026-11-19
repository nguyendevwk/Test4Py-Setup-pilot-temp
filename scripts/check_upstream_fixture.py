"""Run REAL pinned ProjectMessage/type/RAG/test/coverage flow with scripted LLM.

Offline engineering fixture, never efficacy data. Embedding/model are doubles;
syntax checking uses compile instead of pylint. PyCG, pytest, coverage, upstream
initialization/generation/repair orchestration and module scoring are real.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import types

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--arm',choices=['baseline','improved','api_contract'],required=True)
    parser.add_argument('--mechanism',choices=['api-contract-v1'])
    args=parser.parse_args()
    root=args.output/'product';package=root/'fixturepkg';package.mkdir(parents=True,exist_ok=False)
    (package/'__init__.py').write_text('')
    (package/'helpers.py').write_text('class Box:\n    def __init__(self, value):\n        self.value = value\n    def doubled(self):\n        return self.value * 2\n')
    (package/'core.py').write_text('from fixturepkg.helpers import Box\ndef compute(box):\n    return box.doubled() + 1\n')
    os.environ.update(PYTHONPATH=os.pathsep.join([str(args.upstream),str(root),str(BASE)]),
                      USER_PYTHON_PATH=sys.executable,PYTHONDONTWRITEBYTECODE='1',
                      PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTEST_PLUGINS='pytest_jsonreport.plugin')
    sys.path[:0]=[str(args.upstream),str(root)]
    fake_gpt=types.ModuleType('test4dt.gptapi')
    fake_gpt.model=types.SimpleNamespace(aask=None)
    sys.modules['test4dt.gptapi']=fake_gpt
    fake_embedding=types.ModuleType('test4dt.embedding')
    fake_embedding.embedder=types.SimpleNamespace(embed_query=lambda text:[0.1,0.2],device='cpu')
    fake_embedding.find_topK_message=lambda name,messages,query_vector,k=1:messages[:k]
    fake_embedding.function_database=types.SimpleNamespace(init=lambda project:None,query=lambda query,k=3:[])
    sys.modules['test4dt.embedding']=fake_embedding
    import test4dt.testcase as testcase
    def syntax(self):
        try:
            compile(self.get_code(),self.test_path,'exec')
            return False
        except SyntaxError as exc:
            self.error_message=str(exc)
            return True
    testcase.Testcase.find_syntax_error=syntax
    class FixtureBackend:
        def __init__(self,settings,work):
            self.settings,self.work=settings,work
            self.phase='initialization';self.input_tokens=self.output_tokens=0
            self.versions=dict(fixture=True,model='SCRIPTED_FIXTURE_NOT_QWEN')
            self.torch=types.SimpleNamespace(cuda=types.SimpleNamespace(max_memory_allocated=lambda:0))
        async def ask(self,system,user):
            from pilot.common import append_json
            if '<1>' in system:
                answer='<3>'
            elif 'pytest' in system.lower():
                answer='```python\nfrom fixturepkg.core import compute\nfrom fixturepkg.helpers import Box\ndef test_compute():\n    assert compute(Box(2)) == 5\n```'
            else:
                answer='Scripted fixture summary, not model evidence.'
            append_json(self.work/'model_calls.jsonl',dict(fixture=True,phase=self.phase,system=system,user=user,output=answer))
            return answer
    import benchmark_worker
    benchmark_worker.TransformersBackend=FixtureBackend
    benchmark_worker.load_cpu_embedding=lambda upstream:dict(fixture=True,embedding_device='cpu',note='embedding double only')
    from pilot.module_mutation import pool
    from pilot.common import write_json
    write_json(args.output/'mutant-pools.json',{'fixturepkg.core':pool((package/'core.py').read_text())})
    settings=dict(fixture_mode=True,project='fixturepkg',arm=args.arm,paired_protocol=True,
                  import_root=str(root),source_path='fixturepkg',modules=['fixturepkg.core'],
                  rounds=1,embedding_device='cpu',upstream_root=str(args.upstream),
                  prompt_policy='upstream-original',score_timeout=20,
                  mutation_manifest=str(args.output/'mutant-pools.json'))
    if args.mechanism:
        settings.update(mechanism=args.mechanism,acceptance_policy='preserve-assertions-v1',api_contract_max_chars=2500)
    manifest=args.output/'worker-settings.json';write_json(manifest,settings)
    sys.argv=['benchmark_worker.py',str(manifest)]
    os.chdir(root)
    code=benchmark_worker.main()
    report=json.loads((args.output/'report.json').read_text())
    assert code==0,report.get('traceback',report)
    row,=report['modules']
    assert row['status']=='scored',row
    assert row['passed']>0,row
    assert row['mutation_score']==1.0,row
    # Non-selected helper must still be in the full project analysis/call context.
    calls=[json.loads(l) for l in (args.output/'model_calls.jsonl').read_text().splitlines()]
    assert any('doubled' in c['user'] for c in calls),calls
    scope=json.loads((args.output/'analysis_scope.json').read_text())
    assert set(scope['analyzed_modules']) >= {'fixturepkg.core','fixturepkg.helpers'},scope
    assert scope['selected_generation_modules']==['fixturepkg.core'],scope
    assert report['kind']=='offline_fixture_not_efficacy'
    if args.mechanism:
        contexts=[json.loads(l) for l in (args.output/'api_contract_context.jsonl').read_text().splitlines()]
        assert contexts and all(c['status']!='unknown' for c in contexts),contexts
        assert any(c['evidence'] is not None for c in contexts)==(args.arm=='api_contract'),contexts
        assert not (args.output/'type_filter.jsonl').exists(), 'Legacy improved treatment leaked into ablation'
    print('REAL upstream fixture '+args.arm+': PASS (not LLM efficacy)',flush=True)
    return 0


if __name__=='__main__':
    sys.exit(main())
