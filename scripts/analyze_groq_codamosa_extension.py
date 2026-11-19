"""Pre-specified external-project extension analysis; never pool prior cohorts."""
import json
from pathlib import Path
import hashlib
from analyze_groq_confirmation_statistics import analyze_group,validate

W=Path(__file__).resolve().parents[1]/'research/groq_codamosa_extension_20261119'
def main():
 m=json.loads((W/'manifest.json').read_text());s=json.loads((W/'summary.json').read_text())
 validate(m,s)
 out=analyze_group(m,s)
 out['scope']='Prospectively specified external-project extension on adapted published CodaMOSA module frame; no pooling with development or prior confirmation.'
 out['limitations'][0]='Analysis specified in PROVENANCE.json before model inference; not an externally registered trial.'
 out['limitations'][1]=f"{out['independent_projects']} project clusters give limited precision; percentile bootstrap may be poorly calibrated."
 out['project_selection']=json.loads((W/'PROVENANCE.json').read_text())
 out['input_sha256']={n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in ['manifest.json','summary.json','PROVENANCE.json']}
 out['strata']={}
 for accepted in [True,False]:
  targets=[t for t in m['targets'] if t['setup_probe']['accepted'] is accepted];ids={t['id'] for t in targets}
  rows=[r for r in s['rows'] if r['target_id'] in ids]
  if rows:
   sm=dict(m,targets=targets,planned=len(rows));ss=dict(s,rows=rows,planned=len(rows),completed=len(rows))
   result=analyze_group(sm,ss)
   out['strata'][str(accepted)]=dict(projects=result['independent_projects'],targets=len(targets),difference=result['difference'],ci=result['difference_percentile_95'],p=result['exact_cluster_signflip_two_sided_p'],scope='Exploratory pre-inference probe availability stratum; no-hint prompts identical when probe false')
 (W/'statistics.json').write_text(json.dumps(out,indent=2,allow_nan=False))
 lines=['# External-project extension',out['scope'],f"Projects {out['independent_projects']}; targets {out['target_count']}; paired attempts {out['paired_attempts']}.",f"Difference {out['difference']*100:.3f} pp; project bootstrap95% {[v*100 for v in out['difference_percentile_95']]}; sign flip p={out['exact_cluster_signflip_two_sided_p']}.",'|Project|Source|Setup|Difference pp|','|---|---:|---:|---:|']
 for p,r in out['per_project'].items():lines.append(f"|{p}|{r['source_successes']}/{r['paired_attempts']}|{r['verified_successes']}/{r['paired_attempts']}|{r['paired_difference']*100:.2f}|")
 lines+=['','Versions pinned by resolved inventory; original Docker benchmark commits not reproduced.','Passing and target reach are operational endpoints, not proof of oracle correctness or real-fault detection.','All outcomes retained; independent project counts, not API calls, govern inference.']
 (W/'STATISTICS.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines[:4]))
if __name__=='__main__':main()
