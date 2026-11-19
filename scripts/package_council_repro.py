#!/usr/bin/env python3
"""Append-only, credential-free Council evidence packaging and offline relocation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1]
CONF = 'research/groq_confirmation_20261118'
STUDIES = ('groq_study_20261118', 'groq_study_20261118_v2',
           'groq_development_20261118', 'groq_confirmation_20261118',
           'groq_efficiency_20261119','14b_application_replay_20261119',
           'kaggle_execution_evidence_20261119','groq_codamosa_extension_20261119','14b_extended_replay_20261119','groq_context_development_20261119')
EXTENSIONS = {'.json', '.jsonl', '.py', '.md', '.txt', '.csv', '.stdout', '.stderr', '.tar', '.log'}
PUBLIC_SOURCE_EXCEPTIONS = {'repro/environments/youtube-dl/site/youtube_dl/extractor/twitter.py': 'fdb073aa401195c03b74262af8eba2ab90c995fafe2f4df5a71b36ac7933ad67'}
BLOCKED = {'venv', '.venv', '__pycache__', '.git', 'node_modules'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def allowed(path):
    return not any(p in BLOCKED or p.startswith('.env') for p in path.parts) and path.suffix != '.pyc'


def load(path):
    return json.loads(path.read_text())


def verify(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or z.testzip():
            raise ValueError('Duplicate member or CRC failure')
        entries = dict(line.split('  ', 1)[::-1] for line in z.read('MANIFEST.sha256').decode().splitlines())
        if set(entries) != set(names) - {'MANIFEST.sha256'}:
            raise ValueError('Checksum manifest membership mismatch')
        for name, expected in entries.items():
            if Path(name).is_absolute() or '..' in Path(name).parts or digest(z.read(name)) != expected:
                raise ValueError('Unsafe member or checksum mismatch: ' + name)
    return len(names)


def completeness(root):
    manifest = load(root / CONF / 'manifest.json')
    summary = load(root / CONF / 'summary.json')
    expected = {(t['id'], s, a) for t in manifest['targets']
                for s in manifest['seed_values'] for a in manifest['arms']}
    rows = [load(p) for p in sorted((root / CONF / 'attempts').glob('*/outcome.json'))]
    keys = [(r['target_id'], r['seed'], r['arm']) for r in rows]
    fatal = {'started', 'rate_limited', 'budget_exhausted', 'provider_error'}
    complete = (len(expected) == manifest['planned'] == summary['planned'] == summary['completed']
                == len(rows) == len(set(keys)) and set(keys) == expected
                and not any(r['status'] in fatal for r in rows)
                and sorted(summary['rows'], key=lambda r: (r['target_id'], r['seed'], r['arm']))
                == sorted(rows, key=lambda r: (r['target_id'], r['seed'], r['arm'])))
    result=dict(complete=complete, planned=manifest['planned'], outcomes=len(rows),
                summary_completed=summary['completed'], missing=len(expected-set(keys)))
    efficiency=root/'research/groq_efficiency_20261119'
    if (efficiency/'manifest.json').exists():
        em=load(efficiency/'manifest.json');es=load(efficiency/'summary.json')
        er=[load(p) for p in (efficiency/'attempts').glob('*/outcome.json')]
        expected_e={(t['id'],a,c) for t in em['targets'] for a in em['arms'] for c in em['output_caps']}
        actual_e=[(r['target_id'],r['arm'],r['output_cap']) for r in er]
        ready=len(set(actual_e))==len(actual_e)==em['planned']==es['completed']==len(expected_e) and set(actual_e)==expected_e
        result['efficiency']=dict(complete=ready,planned=em['planned'],outcomes=len(er))
        result['complete']=result['complete'] and ready
    extension=root/'research/groq_codamosa_extension_20261119'
    if (extension/'manifest.json').exists():
        xm=load(extension/'manifest.json');xs=load(extension/'summary.json')
        xr=[load(p) for p in (extension/'attempts').glob('*/outcome.json')]
        expected_x={(t['id'],seed,a) for t in xm['targets'] for seed in xm['seed_values'] for a in xm['arms']}
        actual_x=[(r['target_id'],r['seed'],r['arm']) for r in xr]
        ready=len(set(actual_x))==len(actual_x)==xm['planned']==xs['completed']==len(expected_x) and set(actual_x)==expected_x and not any(r['status'] in fatal for r in xr)
        result['external_extension']=dict(complete=ready,planned=xm['planned'],outcomes=len(xr))
        result['complete']=result['complete'] and ready
    development=root/'research/groq_context_development_20261119'
    if (development/'manifest.json').exists():
        dm=load(development/'manifest.json');ds=load(development/'summary.json')
        dr=[load(p) for p in (development/'attempts').glob('*/outcome.json')]
        expected_d={(t['id'],seed,a) for t in dm['targets'] for seed in dm['seed_values'] for a in dm['arms']}
        actual_d=[(r['target_id'],r['seed'],r['arm']) for r in dr]
        ready=len(set(actual_d))==len(actual_d)==dm['planned']==ds['completed']==len(expected_d) and set(actual_d)==expected_d and not any(r['status'] in fatal for r in dr)
        result['context_development']=dict(complete=ready,planned=dm['planned'],outcomes=len(dr))
        result['complete']=result['complete'] and ready
    return result


def package(args):
    root = args.root.resolve()
    state = completeness(root)
    if not state['complete'] and not args.allow_incomplete:
        raise SystemExit('Campaign incomplete; final bundle refused: ' + json.dumps(state))
    output = args.output or root / 'deliverables' / ('council_repro_20261119.zip' if state['complete']
                                                   else 'council_repro_20261119_provisional.zip')
    if output.exists():
        raise SystemExit('Refusing to overwrite: ' + str(output))
    members = {}
    def add(path, name=None):
        if path.is_symlink() or not path.is_file() or not allowed(Path(name) if name else path):
            return
        name = name or path.relative_to(root).as_posix()
        data = path.read_bytes()
        # Fail closed; never rewrite historical evidence to hide a credential.
        if re.search(rb'(?:gsk_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9_.-]{20,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY)', data):
            if PUBLIC_SOURCE_EXCEPTIONS.get(name) != digest(data):
                raise ValueError('Possible credential in whitelisted member: ' + name)
        members[name] = data
    for directory in ('pilot', 'council'):
        for p in (root / directory).rglob('*.py'):
            add(p)
    script_names = {'package_council_repro.py', 'rebuild_council_evidence.py', 'mutate_groq_recovery.py',
                    'revise_council_docx_v2.py', 'polish_council_report.py',
                    'finalize_council_report.py','update_council_toc.py',
                    'revise_kaggle_groq_narrative.py','collect_kaggle_execution_evidence.py','replay_14b_application.py','replay_14b_extended_application.py','extend_council_benchmark_report.py'}
    for p in (root / 'scripts').glob('*.py'):
        if 'groq' in p.name or p.name in script_names:
            add(p)
    for p in root.glob('requirements*.txt'):
        add(p)
    add(root / 'research/REPRODUCIBILITY_GROQ.md')
    for filename in ('REVIEW.md','paper_extracted.txt'):
        add(root/'research/reviews/council_sota_20261118'/filename)
    original=Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx')
    if original.exists():add(original,'repro/original_report.docx')
    for p in (root/'reports').glob('*'):
        if p.is_file() and p.suffix in {'.docx','.json','.md'}:add(p)
    for p in (root/'reports/rendered').glob('*.pdf'):add(p)
    for p in (root/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v4_assets').glob('*'):
        if p.suffix in {'.png','.svg','.json'}:add(p)
    for p in (root/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v9_assets').glob('*'):
        if p.suffix in {'.png','.svg','.json'}:add(p)
    for p in (root/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v10_assets').glob('*'):
        if p.suffix in {'.png','.svg','.json'}:add(p)
    for p in (root/'research/application/14b_genty_extended_20261117').rglob('*'):
        if p.suffix in {'.py','.md','.json','.zip'}:add(p)
    for name in ('UPSTREAM_14B_SMALL_TIMEOUT_20261116.md','NF4_SMALL_REMOTE_20261117.md'):
        add(root/'research/analysis'/name)
    for p in (root/'research/artifacts').glob('*.json'):add(p)
    for p in (root/'research/application/14b_genty_curated_20261117').rglob('*'):add(p)
    for p in (root/'local_benchmark_repos/genty/genty').rglob('*.py'):add(p)
    for study in STUDIES:
        for p in (root / 'research' / study).rglob('*'):
            if p.suffix in EXTENSIONS:
                add(p)
    for name in ('projects-upstream.json', 'groq_candidates_20261118.json', 'GROQ_NEXT_STUDY.md'):
        add(root / 'research/benchmark' / name)
    historical = []
    for p in sorted((root / 'research/reviews/council_sota_20261118/restored').glob('*/summary.json')):
        add(p); add(p.with_name('validation.md'))
        for item in load(p).get('manifest', []):
            rel = Path(item['path'])
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('Unsafe historical reference')
            candidate = root / rel
            if candidate.suffix in {'.csv', '.json', '.py', '.txt'}:
                add(candidate)
                historical.append(dict(path=str(rel), included=rel.as_posix() in members,
                                       recorded_sha256=item.get('sha256'),
                                       matches_recorded=(digest(candidate.read_bytes()) == item.get('sha256'))
                                       if candidate.is_file() else None))
    environments = {}
    environment_inputs=[]
    for study in (CONF,'research/groq_codamosa_extension_20261119'):
        directory=root/study
        if (directory/'manifest.json').exists():
            manifest=load(directory/'manifest.json')
            environment_inputs.extend((env,manifest) for env in sorted((directory/'environments').iterdir()))
    for env,manifest in environment_inputs:
        invpath = env / 'inventory.json'
        if not invpath.exists():
            continue
        inv = load(invpath)
        # Inventory site is authoritative; never derive import roots from distribution spelling.
        site = Path(inv['site'])
        roots = sorted({t['module'].split('.')[0] for t in manifest['targets'] if t['project'] == env.name})
        prefix = 'repro/environments/' + env.name
        files = {}
        for module in roots:
            source = site / module
            if not source.exists():
                source = site / (module + '.py')
            if not source.exists():
                raise ValueError('Missing subject source: ' + str(source))
            for p in ([source] if source.is_file() else source.rglob('*')):
                if p.is_file() and allowed(p.relative_to(site)) and not any(part in {'test','tests'} for part in p.relative_to(site).parts):
                    name = prefix + '/site/' + p.relative_to(site).as_posix()
                    add(p, name)
                    if name in members:
                        files[name] = digest(members[name])
        for p in site.glob('*.dist-info/*'):
            if p.name in {'METADATA', 'WHEEL', 'RECORD', 'top_level.txt', 'entry_points.txt'}:
                add(p, prefix + '/metadata/' + p.relative_to(site).as_posix())
        packages = inv['packages']
        for name, version in packages.items():
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or not re.fullmatch(r'[A-Za-z0-9_.+!-]+', version):
                raise ValueError('Unsafe requirement')
        members[prefix + '/requirements.txt'] = ('\n'.join(f'{n}=={v}' for n, v in sorted(packages.items(), key=lambda x:x[0].lower()))+'\n').encode()
        python = env / 'venv/bin/python'
        runtime = json.loads(subprocess.check_output([str(python), '-c',
            'import sys,platform,json;print(json.dumps(dict(version=sys.version,implementation=platform.python_implementation(),platform=platform.platform())))'], text=True))
        environments[env.name] = dict(python=runtime, root_package_version=inv['version'],
            import_roots=roots, original_site=str(site), packages=packages, source_files=files,
            source_tree_sha256=digest(encoded(files)))
        members[prefix + '/versions.json'] = encoded(environments[env.name])
    events = [json.loads(line) for line in members['research/groq_study_20261118/api/ledger.jsonl'].decode().splitlines()]
    balances = {}; settled = {}; labels = {}
    for e in events:
        balances[e['id']] = Decimal(e['charge_usd'])
        if e['event'] == 'reserve': labels[e['id']] = e['label']
        if e['event'] == 'settle': settled[e['id']] = Decimal(e['charge_usd'])
    budget = dict(currency='USD', pricing='configured estimates, not provider invoice',
        settled_usage_estimate=str(sum(settled.values(), Decimal(0))),
        outstanding_reservations=str(sum((v for k,v in balances.items() if k not in settled), Decimal(0))),
        accounted_total=str(sum(balances.values(), Decimal(0))),
        confirmation_requests=sum(v.startswith('confirmation__') for v in labels.values()),
        total_reserved_requests=len(labels),
        allocation_source='research/groq_confirmation_20261118/execution_manifest.json',
        locked_cumulative_allocation=load(root / CONF / 'execution_manifest.json')['budget_cumulative_usd'],
        caveat='Earlier manifests record 2 USD; execution lock records cumulative 3 USD. Allocation is not expenditure.')
    members['repro/BUDGET.json'] = encoded(budget)
    members['repro/HISTORICAL_REFERENCES.json'] = encoded(historical)
    members['repro/BUILD.json'] = encoded(dict(campaign=state, provisional=not state['complete'],
        original_root=str(root), packager_python=sys.version, platform=platform.platform(),
        environment_projects=sorted(environments), subject_packaging='Production package files; upstream test/test fixtures omitted, including example TLS private keys. All generated evaluation tests and outcomes retained.', checksum_policy='All members except MANIFEST.sha256 itself; self-hashing is impossible'))
    # Detect a moving campaign rather than silently producing a final archive mid-write.
    if completeness(root) != state:
        raise RuntimeError('Campaign changed during snapshot; retry after runner stops')
    members['MANIFEST.sha256'] = ''.join(f'{digest(data)}  {name}\n' for name,data in sorted(members.items())).encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, suffix='.zip', delete=False) as f:
        temporary = Path(f.name)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as z:
            for name,data in sorted(members.items()): z.writestr(name, data)
        count = verify(temporary)
        os.link(temporary, output)  # Atomic no-clobber publication, including concurrent builders.
    finally:
        temporary.unlink(missing_ok=True)
    print(json.dumps(dict(output=str(output), members=count, bytes=output.stat().st_size, campaign=state, budget=budget), indent=2))


def restore(args):
    """Derive relocated manifests; original evidence remains byte-for-byte untouched."""
    source = args.root.resolve(); dest = args.restore_root.resolve()
    if dest.exists(): raise SystemExit('Restore destination must not exist')
    import shutil
    shutil.copytree(source, dest, ignore=shutil.ignore_patterns('deliverables', '.git', 'venv', '.venv', '__pycache__'))
    build = load(source / 'repro/BUILD.json')
    old = build['original_root']
    replacements = {old: str(dest)}
    for p in (dest / 'repro/environments').glob('*/versions.json'):
        info = load(p); replacements[info['original_site']] = str(p.parent / 'site')
    for archive in (dest / 'research/groq_study_20261118/source_archives').glob('*.tar'):
        target = dest / 'repro/source_projects' / archive.stem
        target.mkdir(parents=True)
        with tarfile.open(archive) as tf:
            tf.extractall(target, filter='data')
        replacements['/tmp/council-study-sources/' + archive.stem] = str(target)
    def remap(value):
        if isinstance(value, str):
            for a,b in sorted(replacements.items(), key=lambda x:-len(x[0])): value=value.replace(a,b)
            return value
        if isinstance(value, list): return [remap(v) for v in value]
        if isinstance(value, dict): return {k:remap(v) for k,v in value.items()}
        return value
    for study in STUDIES:
        folder = dest / 'research' / study
        for name in ('manifest.json', 'summary.json'):
            p=folder/name
            if p.exists(): p.write_bytes(encoded(remap(load(p))))
    (dest/'RELOCATION.json').write_bytes(encoded(dict(original_root=old, replacements=replacements,
        note='Derived replay workspace. Original archive checksums do not apply to relocated JSON.')))
    print(dest)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--verify', type=Path)
    parser.add_argument('--restore-root', type=Path)
    args=parser.parse_args()
    if args.verify: print('Verified members:', verify(args.verify))
    elif args.restore_root: restore(args)
    else: package(args)


if __name__ == '__main__': main()
