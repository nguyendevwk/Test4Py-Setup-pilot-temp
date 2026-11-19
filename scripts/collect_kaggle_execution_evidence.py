"""Hash-verify historical Kaggle ZIPs; copy only a structural evidence whitelist."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT=Path(__file__).resolve().parents[1]
SPECS=[('memory','NF4_14B_OOM_CHECK_20261116T172805400121Z.zip','e3980f3a8ef62bd2a0896ae72873ca0a926d7a2800626f8b55f38338800ffe8c'),
       ('cold','UPSTREAM_NF4_RESUME_20261116T174754946339Z.zip','603266e8f6360ae0fc86d93d2bed7edc131db23a81448017a80202518d566b3a'),
       ('warm','UPSTREAM_NF4_RETRY_20261116T190701623856Z.zip','604d75c7e03bca094984d51bf4421860b6772c589df69f6866b1fbed11a0dcf6')]
NAMES={'probe.json','provenance.json','process.json','report.json','model_calls.jsonl','events.jsonl',
       'worker-settings.json','summary.json','modules.csv','pytest_report.json','coverage.json',
       'repair_preservation.jsonl','retained_test_audits.json'}


def main():
    out=ROOT/'research/kaggle_execution_evidence_20261119';out.mkdir(exist_ok=False)
    records=[]
    for stage,name,expected in SPECS:
        path=Path('/home/heurix/Downloads')/name;data=path.read_bytes();actual=hashlib.sha256(data).hexdigest()
        if actual!=expected:raise RuntimeError('Historical archive hash mismatch: '+name)
        rec=dict(stage=stage,archive=name,archive_sha256=actual,members=[],skipped_sensitive=[])
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                rel=Path(info.filename)
                if info.is_dir() or rel.name not in NAMES:continue
                if rel.is_absolute() or '..' in rel.parts:raise ValueError('Unsafe archive path')
                payload=z.read(info)
                if re.search(rb'(gsk_[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9_.-]{20,}|[?&]token=[A-Za-z0-9_-]{20,})',payload):
                    rec['skipped_sensitive'].append(str(rel));continue
                dest=out/stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload)
                rec['members'].append({'member':str(rel),'sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)})
        records.append(rec)
    (out/'manifest.json').write_text(json.dumps({'purpose':'Preserve verifiable real 14B NF4 execution; structural whitelist not outcome selection','archives':records,'original_archives_unchanged':True},indent=2))
    print(json.dumps({r['stage']:{'files':len(r['members']),'sensitive_omitted':len(r['skipped_sensitive'])} for r in records}))


if __name__=='__main__':main()
