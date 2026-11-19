"""Read-only Council-v4 artifact audit; never changes scores or source."""
import argparse
import ast
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path
from statistics import mean
import zipfile


def audit(path,output):
    output.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path) as z:
        names=set(z.namelist());summary=json.loads(z.read('summary.json'));records=summary['records']
        raw_csv=z.read('results.csv');csv_rows=list(csv.DictReader(io.StringIO(raw_csv.decode())))
        plan=json.loads(z.read('plan.json'));manifest=json.loads(z.read('manifest.json'))
        preflight=json.loads(z.read('preflight.json'));engine=json.loads(z.read('engine.json'))
        key=lambda r:(r['target_id'],r['arm'],r['sample'])
        index={key(r):r for r in records}
        assert len(index)==len(records)==len(csv_rows)==len(plan['planned'])
        assert set(index)=={(r['target'],r['arm'],r['sample']) for r in plan['planned']}
        for row in csv_rows:
            r=index[key(row)]
            for field in ('suite_pass','first_pass','stable','repair_attempted','repaired_by_critic'):
                assert (row[field]=='True')==r.get(field,False),(key(row),field)
            assert json.loads(z.read('/'.join(key(row))+'/result.json'))==r
        source_checks=0;pass_counts=[];rescues=[]
        for r in records:
            prefix='/'.join(key(r))
            for relative,sha in preflight[r['target_id']]['hashes'].items():
                member=prefix+'/product/'+relative
                assert member in names and hashlib.sha256(z.read(member)).hexdigest()==sha,member
                source_checks+=1
            if not r['suite_pass']:continue
            version='v2_repaired' if r['repaired_by_critic'] else 'v1_raw';base=prefix+'/'+version
            process=json.loads(z.read(base+'/process.json'));pytest=json.loads(z.read(base+'/pytest_report.json'))
            tests=pytest.get('tests',[])
            assert process['returncode']==0 and not process['timeout'] and tests
            assert all(t['outcome']=='passed' and all(t.get(p,{}).get('outcome')=='passed' for p in ('setup','call','teardown')) for t in tests)
            assert len(tests)==r['pass_count']==r['total_count']
            cov=json.loads(z.read(base+'/coverage.json'));relative=r['module'].replace('.','/')+'.py'
            matches=[d['summary'] for f,d in cov['files'].items() if f.replace('\\','/').endswith(relative)]
            assert len(matches)==1
            s=matches[0]
            assert math.isclose(100*s['covered_lines']/s['num_statements'],r['line_pct'],abs_tol=1e-9)
            branch=100*s['covered_branches']/s['num_branches'] if s['num_branches'] else None
            assert (branch is None and r['branch_pct'] is None) or math.isclose(branch,r['branch_pct'],abs_tol=1e-9)
            replay=json.loads(z.read(prefix+'/replay/pytest_report.json'));rp=json.loads(z.read(prefix+'/replay/process.json'))
            assert rp['returncode']==0 and not rp['timeout'] and replay.get('tests')
            assert all(t['outcome']=='passed' for t in replay['tests'])
            pass_counts.append(dict(target=r['target_id'],arm=r['arm'],sample=r['sample'],
                covered_lines=s['covered_lines'],total_lines=s['num_statements'],
                covered_branches=s['covered_branches'],total_branches=s['num_branches']))
            if r['repaired_by_critic']:
                before=ast.parse(z.read(prefix+'/v1_raw/test_run.py').decode())
                after=ast.parse(z.read(prefix+'/v2_repaired/test_run.py').decode())
                checks=lambda tree:Counter(ast.dump(n,include_attributes=False) for n in ast.walk(tree) if isinstance(n,ast.Assert))
                assert checks(before)==checks(after)
                rescues.append(dict(target=r['target_id'],arm=r['arm'],sample=r['sample'],assertion_ast_unchanged=True))
        groups=[]
        for target in dict.fromkeys(r['target_id'] for r in records):
            for arm in ('baseline','grounded','ranked','verified'):
                rows=[r for r in records if (r['target_id'],r['arm'])==(target,arm)];passing=[r for r in rows if r['suite_pass']]
                groups.append(dict(target=target,arm=arm,planned=len(rows),first_pass=sum(r['first_pass'] for r in rows),
                    final_pass=len(passing),repair_attempted=sum(r['repair_attempted'] for r in rows),
                    rescued=sum(r['repaired_by_critic'] for r in rows),
                    conditional_line_mean=mean(r['line_pct'] for r in passing) if passing else None,
                    conditional_branch_mean=mean(r['branch_pct'] for r in passing) if passing else None))
        arms={a:dict(planned=sum(g['planned'] for g in groups if g['arm']==a),
             first_pass=sum(g['first_pass'] for g in groups if g['arm']==a),
             final_pass=sum(g['final_pass'] for g in groups if g['arm']==a)) for a in ('baseline','grounded','ranked','verified')}
        result=dict(archive=path.name,archive_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            protocol=summary['protocol'],planned=summary['planned'],finished=summary['finished'],
            checks=dict(plan_csv_summary_result_agree=True,source_files_unchanged=source_checks,
                        raw_passing_suite_checks=len(pass_counts),raw_replay_checks=len(pass_counts),raw_coverage_ratios_match=True),
            arms=arms,groups=groups,first_pass=sum(r['first_pass'] for r in records),final_pass=sum(r['suite_pass'] for r in records),
            repair_attempts=sum(r['repair_attempted'] for r in records),rescues=rescues,
            repair_rejected_for_review=sum(bool(r.get('repair_rejected')) for r in records),
            statuses=dict(Counter(r['status'] for r in records)),
            final_execution_statuses=dict(Counter(r.get('final_evaluation',{}).get('status','missing') for r in records)),
            runtime_sec_sum=sum(r['runtime_sec'] for r in records),telemetry=summary['telemetry'],engine=engine,
            source_hashes=manifest['source_hashes'],
            interpretation='artifact consistency/execution audit, not independent execution reproduction or oracle validation; four target clusters; no superiority claim')
    (output/'council_160_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'council_160_rows.csv').write_bytes(raw_csv)
    for name,rows in [('council_160_groups.csv',groups),('council_160_pass_raw_counts.csv',pass_counts)]:
        with (output/name).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps(dict(planned=result['planned'],arms=arms,checks=result['checks']),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();audit(args.archive,args.output)
