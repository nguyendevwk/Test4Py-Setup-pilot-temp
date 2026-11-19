"""Prepare ten fixed project candidates, selecting by source only, never outcomes."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

from run_groq_study import ROOT,write,sha
from run_groq_development import ATOMIC

WORK=ROOT/'research/groq_confirmation_20261118'
PROJECTS={'apimd':'apimd','black':'black','dataclasses-json':'dataclasses-json',
 'flutes':'flutes','httpie':'httpie','isort':'isort','mimesis':'mimesis',
 'py-backwards':'py-backwards','pypara':'pypara','python-semantic-release':'python-semantic-release'}


def main():
    WORK.mkdir(parents=True,exist_ok=True)
    frame=json.loads((ROOT/'research/benchmark/projects-upstream.json').read_text())
    targets=[]; projects=[]
    for project,package in PROJECTS.items():
        dest=WORK/'environments'/project;dest.mkdir(parents=True,exist_ok=True)
        env=dest/'venv';python=env/'bin/python'
        if not python.exists():
            subprocess.run(['uv','venv','--python','3.10',str(env)],check=True,capture_output=True)
        install=subprocess.run(['uv','pip','install','--python',str(python),package,
            'pytest==9.2.0','coverage==7.16.2','pytest-json-report==1.5.0'],capture_output=True,text=True,timeout=240)
        (dest/'install.stdout').write_text(install.stdout);(dest/'install.stderr').write_text(install.stderr)
        info=dict(project=project,package=package,install_returncode=install.returncode)
        projects.append(info)
        if install.returncode:
            write(dest/'project.json',info);print(project,'install_failed',flush=True);continue
        inspection='''import ast,importlib.util,importlib.metadata as md,json,hashlib,sys,site
modules=MODULES
out=[];errors=[]
for module in sorted(modules):
 try:
  spec=importlib.util.find_spec(module)
  if not spec or not spec.origin or not spec.origin.endswith('.py'):raise ValueError('no Python source')
  path=__import__('pathlib').Path(spec.origin);source=path.read_text();tree=ast.parse(source)
  imports='\\n'.join(ast.get_source_segment(source,n) for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom)))
  for node in tree.body:
   if not isinstance(node,(ast.FunctionDef,ast.ClassDef)) or node.name.startswith('_'):continue
   excerpt=ast.get_source_segment(source,node)
   size=node.end_lineno-node.lineno+1
   if size<5 or size>160 or len(excerpt)>6000:continue
   out.append(dict(module=module,symbol=node.name,file=str(path),source_sha256=hashlib.sha256(source.encode()).hexdigest(),source=imports+'\\n\\n'+excerpt,source_lines=size))
 except Exception as exc:errors.append(dict(module=module,error=type(exc).__name__))
print(json.dumps(dict(candidates=out,errors=errors,site=site.getsitepackages()[0],version=md.version(PACKAGE),packages={d.metadata['Name']:d.version for d in md.distributions()})))
'''.replace('MODULES',repr(frame.get(project,[]))).replace('PACKAGE',repr(package))
        proc=subprocess.run([str(python),'-c',inspection],capture_output=True,text=True,timeout=60)
        (dest/'inspection.stdout').write_text(proc.stdout);(dest/'inspection.stderr').write_text(proc.stderr)
        if proc.returncode:
            info['inspection_failed']=True;write(dest/'project.json',info);continue
        data=json.loads(proc.stdout);write(dest/'inventory.json',data)
        info.update(version=data['version'],candidate_count=len(data['candidates']))
        # Structural eligibility and deterministic hash ordering fixed before inference.
        ordered=sorted(data['candidates'],key=lambda t:sha((project+'|'+t['module']+'|'+t['symbol']).encode()))
        chosen=[];used=set()
        for target in ordered:
            if target['module'] in used:continue
            chosen.append(target);used.add(target['module'])
            if len(chosen)==3:break
        if len(chosen)<3:
            chosen.extend(t for t in ordered if t not in chosen)
            chosen=chosen[:3]
        for t in chosen:
            root=data['site'];t.update(project=project,root=root,
                id=project+'__'+t['module']+'__'+t['symbol'],source_file_absolute=t['file'])
            # Generic signature-derived required arguments, not expected outputs.
            probe='''import importlib,inspect,json
obj=getattr(importlib.import_module(MODULE),SYMBOL);sig=inspect.signature(obj);kw={}
for name,p in sig.parameters.items():
 if p.default is not inspect.Parameter.empty or p.kind in (p.VAR_POSITIONAL,p.VAR_KEYWORD):continue
 if p.kind==p.POSITIONAL_ONLY:raise ValueError('unsupported positional-only')
 if name in ('f','fn','func','function','callback','mapper'):v=lambda *args:1
 elif name.startswith('is_') or p.annotation is bool:v=False
 elif name in ('errors','items','values','rules'):v=[]
 else:v=1
 kw[name]=v
obj(**kw)
print(json.dumps({'signature':str(sig),'arguments':{k:('lambda *args: 1' if callable(v) else repr(v)) for k,v in kw.items()},'scope':'call completed; no method precondition or oracle guarantee'}))
'''.replace('MODULE',repr(t['module'])).replace('SYMBOL',repr(t['symbol']))
            try:
                pp=subprocess.run([str(python),'-c',probe],capture_output=True,text=True,timeout=10,cwd=dest)
                t['setup_probe']=dict(accepted=pp.returncode==0,stdout=pp.stdout,stderr=pp.stderr,returncode=pp.returncode)
            except subprocess.TimeoutExpired:
                t['setup_probe']=dict(accepted=False,stdout='',stderr='timeout',returncode=None)
            targets.append(t)
        write(dest/'project.json',info)
        print(project,'candidates',len(ordered),'selected',len(chosen),flush=True)
    manifest=dict(status='locked_multi_project_component_evaluation_not_full_Test4Py',
        design='ten projects fixed before installation; source-only eligibility and deterministic hash selection; no model outcome selection',
        model='openai/gpt-oss-20b',seed_values=[42,43,44],arms=['atomic_source','atomic_verified_setup'],
        rules=ATOMIC,repair_rounds=0,max_completion_tokens=2048,temperature=.2,
        budget_shared_usd=2,targets=targets,projects=projects,planned=len(targets)*6,
        expected_target_slots=30,missing_target_slots=30-len(targets),
        primary='all-pass + positive module coverage + replay + quality gate',
        source_versions='Current PyPI versions pinned by resolved metadata; not original paper commits',
        preparation_time=time.time())
    with (WORK/'manifest.json').open('x') as f:json.dump(manifest,f,indent=2)
    print(json.dumps({'targets':len(targets),'projects_with_targets':len({t['project'] for t in targets}),'planned':manifest['planned']}))


if __name__=='__main__':main()
