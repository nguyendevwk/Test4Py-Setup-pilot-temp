"""Bounded same-module declaration closure, no oracle or generated-test inputs."""
import ast,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'research/groq_context_development_20261119'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 W.mkdir(exist_ok=False);source=R/'research/groq_codamosa_extension_20261119/manifest.json';m=json.loads(source.read_text())
 for t in m['targets']:
  raw=Path(t['source_file_absolute']).read_text();tree=ast.parse(raw);symbols={}
  for n in tree.body:
   names=[n.name] if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)) else [x.id for x in ast.walk(n) if isinstance(x,ast.Name) and isinstance(x.ctx,ast.Store)] if isinstance(n,(ast.Assign,ast.AnnAssign)) else []
   for name in names:symbols[name]=n
  selected=symbols[t['symbol']];pending={n.id for n in ast.walk(selected) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load)};used={t['symbol']};snippets=[];size=0
  for depth in range(2):
   nextnames=set()
   for name in sorted(pending):
    if name in used or name not in symbols:continue
    used.add(name);node=symbols[name];excerpt=ast.get_source_segment(raw,node)
    if len(excerpt)>4000 or size+len(excerpt)>8000:continue
    snippets.append(excerpt);size+=len(excerpt);nextnames.update(n.id for n in ast.walk(node) if isinstance(n,ast.Name) and isinstance(n.ctx,ast.Load))
   pending=nextnames
  t['context_closure']='\n\n'.join(snippets);t['context_closure_names']=sorted(used-{t['symbol']});t['context_closure_characters']=size
 m.update(status='post_extension_development_context_closure_screen_not_independent_confirmation',seed_values=[46],planned=len(m['targets'])*2,design='All34 previously observed targets; matched new generation two arms; two-level same-module AST declarations max8000chars/4000per declaration plus verified setup. No model outcome selection or expected-output hints.',source_manifest_sha256=h(source),preparer_sha256=h(Path(__file__)),rationale='Respond to limited setup-only transfer with bounded genuine helper/global production context; a development engineering comparison, not held-out proof.')
 (W/'manifest.json').write_text(json.dumps(m,indent=2));print('Prepared',m['planned'],'calls; context supplied',sum(bool(t['context_closure']) for t in m['targets']))
if __name__=='__main__':main()
