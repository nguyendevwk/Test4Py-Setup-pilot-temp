"""Actual project + pinned upstream initialization with SCRIPTED summaries/vectors.

Detects source/API/call-graph failures without model weights. Not an inference,
context-budget, semantic-summary or test-quality evaluation.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import types

BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE))
from pilot.common import write_json
from pilot.setup import production


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',type=Path,required=True);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--source-path',required=True);p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    sys.path[:0]=[str(args.upstream),str(args.source)]
    calls=[]
    async def ask(system,user):
        calls.append(dict(system=system,user=user,fixture=True))
        return 'Scripted initialization fixture; no model semantics claimed.'
    gpt=types.ModuleType('test4dt.gptapi');gpt.model=types.SimpleNamespace(aask=ask);sys.modules[gpt.__name__]=gpt
    embedding=types.ModuleType('test4dt.embedding')
    embedding.embedder=types.SimpleNamespace(embed_query=lambda s:[0.1,0.2])
    embedding.find_topK_message=lambda name,messages,query_vector,k=1:messages[:k]
    embedding.function_database=types.SimpleNamespace(init=lambda project:None,query=lambda *a,**k:[])
    sys.modules[embedding.__name__]=embedding
    from test4dt.message import ProjectMessage
    class Project(ProjectMessage):
        def _get_files(self):
            return [f for f in sorted(super()._get_files()) if production(Path(f).relative_to(args.source))]
    try:
        project=Project(str(args.source),args.source_path)
        asyncio.run(project.init())
        result=dict(status='initialization_complete',fixture=True,
                    modules={f.mod_name:len(f.functions) for f in project.file_messages},
                    scripted_calls=len(calls),cg_edges=len(project.cg_edges),
                    scope='real source/AST/upstream with scripted model and embedding; no efficacy evidence')
    except Exception as exc:
        import traceback
        result=dict(status='failed',fixture=True,error=repr(exc),traceback=traceback.format_exc())
    write_json(args.output/'initialization.json',result)
    write_json(args.output/'scripted_calls.json',calls)
    print(json.dumps({k:v for k,v in result.items() if k!='traceback'},indent=2))
    return 0 if result['status']=='initialization_complete' else 2


if __name__=='__main__':sys.exit(main())
