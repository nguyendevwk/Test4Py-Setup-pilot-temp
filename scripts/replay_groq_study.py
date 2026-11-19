"""Replay accepted primary artifacts offline; do not regenerate or select scores."""
import json
from pathlib import Path
import sys
import argparse
from run_groq_study import execute,sha,write

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study',type=Path)
    parser.add_argument('--project')
    parser.add_argument('--output-root',type=Path)
    args=parser.parse_args()
    study=args.study.resolve()
    replay_root=args.output_root.resolve() if args.output_root else study/'independent_replay'
    summary=json.loads((study/'summary.json').read_text())
    manifest=json.loads((study/'manifest.json').read_text())
    targets={t['id']:t for t in manifest['targets']}
    records=[]
    for row in summary['rows']:
        if not row['accepted'] or args.project and row['project']!=args.project:continue
        code_path=Path(row['final_code']);target=targets[row['target_id']]
        dest=replay_root/code_path.parent.name
        if (dest/'evaluation.json').exists():result=json.loads((dest/'evaluation.json').read_text())
        else:result=execute(code_path.read_text(),Path(target['root']),target['module'],dest)
        records.append(dict(target_id=row['target_id'],arm=row['arm'],seed=row['seed'],
            code_sha256=sha(code_path.read_bytes()),suite_pass=result['suite_pass'],
            module_line_pct=result['line_pct'],matches_saved_line=result['line_pct']==row['line_pct']))
    summary_path=replay_root/'replay_summary.json' if args.output_root else study/'independent_replay_summary.json'
    write(summary_path,dict(scope='Selected primary accepted artifacts only; offline replay, not regenerated inference or population flakiness.',
        planned=len(records),passed=sum(r['suite_pass'] for r in records),
        exact_line_matches=sum(r['matches_saved_line'] for r in records),records=records))
    print('Replay:',len(records),'planned;',sum(r['suite_pass'] for r in records),'passed')

if __name__=='__main__':main()
