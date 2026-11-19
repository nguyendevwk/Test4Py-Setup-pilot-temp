"""Replay genuine14B curated extension and historical two posthoc mutants."""
import hashlib,json,shutil,zipfile,sys,os,subprocess,time,argparse
from pathlib import Path
from mutate_groq_recovery import classify
R=Path(__file__).resolve().parents[1]
def h(data):return hashlib.sha256(data).hexdigest()
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=R/'research/14b_extended_replay_20261119');args=parser.parse_args()
 source=R/'research/application/14b_genty_extended_20261117';m=json.loads((source/'manifest.json').read_text());old=m['preserved_original_manifest'];subject=R/'local_benchmark_repos/genty';out=args.output.resolve();out.mkdir(exist_ok=False)
 for name,sha in old['production_sha256'].items():assert h((subject/name).read_bytes())==sha
 tests={name:(source/name).read_bytes() for name in old['files_sha256']}
 for name,sha in old['files_sha256'].items():assert h(tests[name])==sha
 added=Path(m['added_file']).name;tests[added]=(source/m['added_file']).read_bytes();assert h(tests[added])==m['added_file_sha256']
 verification=json.loads((source/'verification.json').read_text());mutants={}
 with zipfile.ZipFile(source/'verification-evidence.zip') as z:
  for mutant in verification['rows'][0]['mutants']:
   data=z.read('old/'+mutant['id']+'/product/genty/genty_args.py');assert h(data)==mutant['mutated_source_sha256'];mutants[mutant['id']]=data
 def run(label,extended,mutation=None):
  dest=out/label;dest.mkdir();product=dest/'product';shutil.copytree(subject/'genty',product/'genty',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  if mutation is not None:(product/'genty/genty_args.py').write_bytes(mutation)
  suite=dest/'tests';suite.mkdir()
  for name,data in tests.items():
   if name==added and not extended:continue
   (suite/name).write_bytes(data)
  env={'PATH':os.environ['PATH'],'HOME':str(dest),'PYTHONPATH':str(product),'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONDONTWRITEBYTECODE':'1','COVERAGE_FILE':str(dest/'.coverage'),'LANG':'C.UTF-8'}
  cmd=[sys.executable,'-m','coverage','run','--branch','--source=genty.genty_args,genty.genty_repeat','-m','pytest','-q','-o','addopts=','--confcutdir='+str(suite),'-p','pytest_jsonreport.plugin','--json-report','--json-report-file='+str(dest/'pytest.json'),str(suite)]
  start=time.monotonic();p=subprocess.run(cmd,cwd=product,env=env,capture_output=True,text=True,timeout=20);seconds=time.monotonic()-start
  (dest/'stdout.txt').write_text(p.stdout);(dest/'stderr.txt').write_text(p.stderr);report=json.loads((dest/'pytest.json').read_text());nodes=[t['nodeid'] for t in report.get('tests',[])];result=dict(returncode=p.returncode,timeout=False,report=report)
  covproc=subprocess.run([sys.executable,'-m','coverage','json','-o',str(dest/'coverage.json')],cwd=product,env=env,capture_output=True,text=True,timeout=20);assert covproc.returncode==0
  coverage=json.loads((dest/'coverage.json').read_text());counts={Path(n).name:entry['summary'] for n,entry in coverage['files'].items()}
  record=dict(label=label,extended=extended,returncode=p.returncode,seconds=seconds,total=len(nodes),passed=sum(t['outcome']=='passed' for t in report.get('tests',[])),node_suffixes=sorted(n.split('::',1)[-1] for n in nodes),coverage=counts)
  if mutation is not None:
   assert record['total']==(14 if extended else 12);record['verdict']=classify(result,nodes)
  else:assert p.returncode==0 and record['passed']==record['total']==(14 if extended else 12)
  (dest/'result.json').write_text(json.dumps(record,indent=2));return record
 records=[run('old_replay',False)]+[run('extended_replay'+str(i),True) for i in range(1,4)]
 for name,mutation in mutants.items():
  for extended in [False,True]:records.append(run(('extended_' if extended else 'old_')+name,extended,mutation))
 for name,sha in old['production_sha256'].items():assert h((subject/name).read_bytes())==sha
 summary=dict(scope='Fresh CPU replay of curated real14B application extension; historical two posthoc development mutants, not held-out fault benchmark or algorithm efficacy.',origin_manifest_sha256=h((source/'manifest.json').read_bytes()),generation_model=m['generation_model'],generation_revision=m['generation_revision'],original12_tests_unchanged=True,added2_tests_unchanged=True,source_unchanged=True,model_inference=False,rows=records,mutant_hashes={n:h(v) for n,v in mutants.items()})
 (out/'summary.json').write_text(json.dumps(summary,indent=2));print([(r['label'],r['passed'],r.get('verdict')) for r in records])
if __name__=='__main__':main()
