#!/usr/bin/env python3
"""Read-only evidence analysis; writes only the two authorized v15 editorial artifacts.
Run from any cwd with .venv/bin/python scripts/analyze_v15_descriptive.py.
All additional summaries are exploratory post hoc; no new subgroup hypothesis tests.
"""
import ast
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from statistics import mean
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'research/groq_full_scope_20261119'
OUT = ROOT / 'research/editorial_v15'
inputs = {}
def read(p):
    p = Path(p)
    data = p.read_bytes()
    inputs[str(p.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
    return json.loads(data)
def key(r): return r['target_id'], r['seed'], r['arm']
manifest = read(R/'manifest.json')
targets = {t['id']: t for t in manifest['targets']}
arms = manifest['arms']; seeds = manifest['seed_values']
projects = sorted({t['project'] for t in targets.values()})
rows = {}
for p in sorted((R/'attempts').glob('*/outcome.json')):
    row = read(p)
    assert key(row) not in rows
    rows[key(row)] = row
expected = {(tid, s, a) for tid in targets for s in seeds for a in arms}
assert set(rows) == expected and len(rows) == manifest['planned'] == 3870
for (tid, s, a), r in rows.items():
    assert type(r['accepted']) is bool and r['project'] == targets[tid]['project']
    assert r['module'] == targets[tid]['module']
    if r['accepted']: assert r['line_pct'] is not None and r['status'] == 'completed'
summary = read(R/'summary.json')
assert {key(r):r for r in summary['rows']} == rows
logpath = R/'outcomes.jsonl'
logdata = logpath.read_bytes(); inputs[str(logpath.relative_to(ROOT))] = hashlib.sha256(logdata).hexdigest()
logrows = [json.loads(s) for s in logdata.splitlines() if s.strip()]
assert len(logrows) == len(rows) and {key(r):r for r in logrows} == rows

features = {}
for tid,t in targets.items():
    nodes = [n for n in ast.parse(t['source']).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name == t['symbol']]
    assert len(nodes)==1
    features[tid] = dict(kind='class' if isinstance(nodes[0], ast.ClassDef) else 'function',
        setup_available=t['setup_probe']['accepted'], closure_available=bool(t['context_closure']))
contrasts = [('context_setup','source'),('verified_setup','source'),('context_setup','verified_setup')]

def describe(tids, chosen_seeds=seeds):
    tids = list(tids)
    ps = sorted({targets[t]['project'] for t in tids})
    byp = {p:[t for t in tids if targets[t]['project']==p] for p in ps}
    rates = {a:{p:mean(int(rows[t,s,a]['accepted']) for t in byp[p] for s in chosen_seeds) for p in ps} for a in arms}
    result = dict(targets=len(tids), pairs=len(tids)*len(chosen_seeds), projects=len(ps), arms={}, contrasts={})
    for a in arms:
        rr = [rows[t,s,a] for t in tids for s in chosen_seeds]
        result['arms'][a] = dict(accepted=sum(r['accepted'] for r in rr),denominator=len(rr),
            pooled_rate=mean(int(r['accepted']) for r in rr),equal_project_rate=mean(rates[a].values()),
            status_counts=dict(sorted(Counter(r['status'] for r in rr).items())),
            pooled_penalized_module_line_pct=mean(r['line_pct'] if r['accepted'] else 0 for r in rr),
            equal_project_penalized_module_line_pct=mean(mean(rows[t,s,a]['line_pct'] if rows[t,s,a]['accepted'] else 0 for t in byp[p] for s in chosen_seeds) for p in ps))
    for a,b in contrasts:
        counts=Counter()
        transition=Counter()
        for t in tids:
            for s in chosen_seeds:
                ra,rb=rows[t,s,a], rows[t,s,b]
                aa,bb=ra['accepted'],rb['accepted']
                counts['both_pass' if aa and bb else 'treatment_only' if aa else 'control_only' if bb else 'neither']+=1
                transition[rb['status']+' -> '+ra['status']]+=1
        diff={p:rates[a][p]-rates[b][p] for p in ps}
        result['contrasts'][a+'-'+b]=dict(treatment=a,control=b,
            paired_counts={k:counts[k] for k in ['both_pass','control_only','treatment_only','neither']},
            pooled_difference=(counts['treatment_only']-counts['control_only'])/result['pairs'],
            equal_project_difference=mean(diff.values()),project_differences=diff,
            project_wins=sum(d>1e-14 for d in diff.values()),project_ties=sum(abs(d)<=1e-14 for d in diff.values()),project_losses=sum(d< -1e-14 for d in diff.values()),
            terminal_status_transition_counts=dict(sorted(transition.items())))
    return result

full=describe(targets)
per_project={p:describe([t for t in targets if targets[t]['project']==p]) for p in projects}
subgroups={}
for dimension,values in [('setup_available',[False,True]),('kind',['class','function']),('closure_available',[False,True])]:
    subgroups[dimension]={str(v):describe([t for t in targets if features[t][dimension]==v]) for v in values}
subgroups['setup_by_kind']={f'setup={s};kind={k}':describe([t for t in targets if features[t]['setup_available']==s and features[t]['kind']==k]) for s in [False,True] for k in ['class','function']}
assert sum(x['targets'] for x in subgroups['setup_by_kind'].values())==645
by_seed={str(s):describe(targets,[s]) for s in seeds}
seed_stability={}
for a in arms:
    c=Counter(sum(rows[t,s,a]['accepted'] for s in seeds) for t in targets)
    seed_stability[a]=dict(accepted_both=c[2],accepted_exactly_one=c[1],accepted_neither=c[0])
delta_cross=Counter()
for t in targets:
    dd=tuple(int(rows[t,s,'context_setup']['accepted'])-int(rows[t,s,'source']['accepted']) for s in seeds)
    delta_cross[str(dd)]+=1

# Refine terminal test_failure only where actual pytest records support it.
# These categories partition every planned attempt, rather than filtering to runnable suites.
stage_counts = {a:Counter() for a in arms}
stage_records = []
for (tid, seed, arm), row in rows.items():
    category = row['status']
    evidence = None
    if category == 'test_failure':
        report_path = R/'attempts'/f'{tid}__{seed}__{arm}'/'eval0/pytest.json'
        if report_path.exists():
            report = read(report_path)
            evidence = str(report_path.relative_to(ROOT))
            collectors = report.get('collectors', [])
            tests = report.get('tests', [])
            if any(c.get('outcome') == 'failed' for c in collectors):
                category = 'test_failure:collection_failed'
            elif any(t.get(phase,{}).get('outcome') == 'failed' for t in tests for phase in ['setup','teardown']):
                category = 'test_failure:setup_or_teardown_failed'
            elif any(t.get('call',{}).get('outcome') == 'failed' for t in tests):
                category = 'test_failure:call_failed'
            else:
                category = 'test_failure:other_reported'
        else:
            category = 'test_failure:pytest_report_unavailable'
    stage_counts[arm][category] += 1
    stage_records.append(dict(target_id=tid,seed=seed,arm=arm,category=category,pytest_evidence=evidence))
assert all(sum(c.values()) == 1290 for c in stage_counts.values())

# Verify only the three existing inferential facts; no additional hypothesis tests.
# Exact rational subset-sum distribution gives independent integer arithmetic p-values.
frozen = read(R/'statistics.json')
bootstrap_indices=np.random.default_rng(20261119).integers(0,len(projects),(20000,len(projects)))
verification={}
for a,b in contrasts:
    name=a+'-'+b
    exact=[]
    for p in projects:
        tt=[t for t in targets if targets[t]['project']==p]
        exact.append(Fraction(sum(int(rows[t,s,a]['accepted'])-int(rows[t,s,b]['accepted']) for t in tt for s in seeds),len(tt)*len(seeds)))
    import math
    denominator=math.lcm(*(d.denominator for d in exact))
    weights=[int(d*denominator) for d in exact]
    distribution=Counter({0:1})
    for w in weights:
        nxt=Counter()
        for total,n in distribution.items(): nxt[total+w]+=n; nxt[total-w]+=n
        distribution=nxt
    observed=abs(sum(weights))
    numerator=sum(n for total,n in distribution.items() if abs(total)>=observed)
    pv=numerator/(2**len(weights))
    # Match original operation order for deterministic bootstrap reproduction.
    differences=np.array([full['contrasts'][name]['project_differences'][p] for p in projects])
    ci=np.quantile(differences[bootstrap_indices].mean(axis=1),[.025,.975]).tolist()
    old=frozen['contrasts'][name]
    assert abs(pv-old['exact_signflip_two_sided_p'])<1e-15
    assert np.allclose(ci,old['percentile_95'],rtol=0,atol=1e-14)
    assert abs(float(sum(exact)/len(exact))-old['difference'])<1e-14
    verification[name]=dict(equal_project_difference=float(sum(exact)/len(exact)),
        exact_p=pv,exact_exceeding_sign_assignments=numerator,total_sign_assignments=2**len(weights),
        rational_common_denominator=denominator,bootstrap_95=ci,matches_frozen=True)
p1=verification['verified_setup-source']['exact_p']; p2=verification['context_setup-verified_setup']['exact_p']
holm={'context_setup-verified_setup':min(1,2*p2),'verified_setup-source':min(1,max(p1,2*p2))}
assert all(abs(holm[k]-frozen['contrasts'][k]['holm_adjusted_p'])<1e-15 for k in holm)
for a in arms:
    assert full['arms'][a]['accepted']==frozen['arms'][a]['successes']
    assert abs(full['arms'][a]['equal_project_rate']-frozen['arms'][a]['equal_project_acceptance_rate'])<1e-14

# Raw joint pack records, independently matched to the aggregate and accepted suite identities.
js=read(R/'joint_packs/main/summary.json'); jm=read(R/'joint_packs/main/pack_manifest.json')
packrows=[]
for p in sorted((R/'joint_packs/main/packs').glob('*/pack_result.json')):
    q=read(p); packrows.append(q)
assert len(packrows)==63
assert {q['identity']['pack_id']:q for q in packrows}=={q['identity']['pack_id']:q for q in js['results']}
pack_summary={}
pack_details=[]
for q in packrows:
    i=q['identity']; p=i['project']; a=i['arm']
    actual={(s['target_id'],s['seed'],s['arm']) for s in i['suites']}
    wanted={k for k,r in rows.items() if r['project']==p and r['arm']==a and r['accepted']}
    assert actual==wanted and len(actual)==len(i['suites'])
    assert q['expected_nodes']==3*len(wanted)
    if q['measured_coverage_pct'] is not None:
        assert abs(q['measured_coverage_pct']-100*(q['statements']-q['missing'])/q['statements'])<1e-10
    assert q['validated_pack_coverage_pct']==(q['measured_coverage_pct'] if q['pack_pass'] else 0)
    pack_details.append(dict(project=p,arm=a,pack_id=i['pack_id'],status=q['status'],empty=q['empty'],
        accepted_suites=len(actual),expected_nodes=q['expected_nodes'],collected_nodes=q['collected_nodes'],
        pack_pass=q['pack_pass'],suite_pass=q['suite_pass'],returncode=q.get('returncode'),
        measured_coverage_pct=q['measured_coverage_pct'],validated_pack_coverage_pct=q['validated_pack_coverage_pct']))
for a in arms:
    qq=[q for q in packrows if q['identity']['arm']==a]
    available=[q['measured_coverage_pct'] for q in qq if q['measured_coverage_pct'] is not None]
    pack_summary[a]=dict(packs_pass=sum(q['pack_pass'] for q in qq),denominator=21,
        nonempty_packs=sum(not q['empty'] for q in qq),empty_projects=[q['identity']['project'] for q in qq if q['empty']],
        nonempty_failed_projects=[q['identity']['project'] for q in qq if not q['pack_pass'] and not q['empty']],
        expected_nodes=sum(q['expected_nodes'] for q in qq),collected_nodes=sum(q['collected_nodes'] for q in qq),
        available_measured_projects=len(available),available_case_measured_coverage_pct=mean(available),
        equal_project_validated_pack_coverage_pct=mean(q['validated_pack_coverage_pct'] for q in qq))
    assert pack_summary[a]['packs_pass']==js['arms'][a]['packs_pass']
    assert abs(pack_summary[a]['equal_project_validated_pack_coverage_pct']-js['arms'][a]['equal_project_validated_pack_coverage_pct'])<1e-12

# Exact decomposition of weighting, without excluding small or inconvenient projects.
weighting={}
for a,b in contrasts:
    name=a+'-'+b
    contributions={}
    for p in projects:
        d=full['contrasts'][name]['project_differences'][p]
        n=per_project[p]['pairs']
        contributions[p]=dict(pairs=n,pooled_weight=n/1290,equal_project_weight=1/21,
            project_difference=d,pooled_contribution=d*n/1290,equal_project_contribution=d/21,
            pooled_minus_equal_contribution=d*(n/1290-1/21))
    weighting[name]=dict(pooled_minus_equal_difference=full['contrasts'][name]['pooled_difference']-full['contrasts'][name]['equal_project_difference'],per_project=contributions)

result=dict(schema=1,scope='Exploratory post hoc descriptive analysis of the complete frozen full-scope experiment. Existing inference reproduced only; no new subgroup tests, exclusions, repairs, or case filtering.',
    evidence_sources='All trial metrics use attempts/*/outcome.json, cross-checked exactly against outcomes.jsonl and summary.json; target attributes use manifest.json; pack metrics use packs/*/pack_result.json matched to joint summary. input_sha256 maps every input used.',
    definitions=dict(acceptance='Runner accepted boolean; not semantic oracle correctness.',
        paired_counts='Treatment/control named explicitly. For context-source, treatment_only=context_only and control_only=source_only. Counts are target-seed pairs.',
        equal_project='Within each represented project average all selected target-seed pairs, then give each represented project equal weight.',
        subgroups='Exhaustive manifest-defined strata, retaining all arms, both seeds and failures. Each stratum balances its represented projects; project sets may differ across strata. Cross-stratum comparisons are descriptive and confounded, not interaction estimates.',
        status='Terminal runner categories, not independent causal mechanisms or cumulative gate probabilities. test_failure can include collection failures; no finer label inferred.',
        coverage='Trial line_pct is module coverage; acceptance-penalized mean includes every planned attempt. Pack coverage is union over locked eligible modules; its denominator and selected suite composition differ from standalone coverage.',
        seed='Two labels are repetitions within projects; descriptive sensitivity does not estimate broad seed uncertainty.'),
    completeness=dict(planned=3870,raw_outcomes=len(rows),targets=len(targets),projects=len(projects),modules=len({(t['project'],t['module']) for t in targets.values()}),summary_and_jsonl_exact_match=True),
    full=full,per_project=per_project,subgroups=subgroups,by_seed=by_seed,seed_stability=seed_stability,
    stage_failure_partition={a:dict(sorted(c.items())) for a,c in stage_counts.items()},stage_failure_records=stage_records,
    context_source_target_delta_seed71_seed72=dict(sorted(delta_cross.items())),weighting_decomposition=weighting,
    existing_statistics_independent_verification=verification,existing_secondary_holm_verified=holm,
    joint_pack_summary=pack_summary,joint_pack_details=sorted(pack_details,key=lambda q:(q['project'],q['arm'])),
    input_sha256=inputs)
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'deep_analysis.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

lines=['# Independent descriptive analysis for v15','',
'All additional summaries below are **exploratory post hoc**. All 645 targets, 21 projects, three arms and both seeds remain in the analysis (3,870/3,870 attempts). No new significance tests, outcome-based case filtering, repairs or changes to frozen evidence were performed. Existing three-contrast inference is reproduced solely as an audit. No applicable AGENTS.md was found in the repository or ancestor directories.','',
'## Evidence and reproducibility','',
'Run `.venv/bin/python scripts/analyze_v15_descriptive.py`. Raw trial inputs are `research/groq_full_scope_20261119/attempts/*/outcome.json`; every row matches `outcomes.jsonl` and `summary.json` exactly. Target features are parsed from `manifest.json` (AST class/function, setup probe acceptance, nonempty context closure). Raw pack inputs are `joint_packs/main/packs/*/pack_result.json`; every result matches the pack summary, and each pack contains exactly all accepted suites for that project and arm across both seeds. All input paths and SHA-256 digests are in `deep_analysis.json:input_sha256`. All tables below are generated from those raw inputs; JSON keys identify the corresponding calculations.','',
'## Primary contrast: context setup versus source','']
c=full['contrasts']['context_setup-source']; pc=c['paired_counts']
lines += [f"Among 1,290 target-seed pairs: both accepted **{pc['both_pass']}**, source only **{pc['control_only']}**, context only **{pc['treatment_only']}**, neither **{pc['neither']}**. The net gain is {pc['treatment_only']-pc['control_only']} accepted attempts; {pc['treatment_only']+pc['control_only']} pairs change acceptance. A net gain hides bidirectional turnover. Project outcomes: {c['project_wins']} wins, {c['project_ties']} ties, {c['project_losses']} losses. [JSON: full.contrasts.context_setup-source]",'',
'| Arm | Accepted / 1,290 | Pooled % | Equal-project % | Penalized module coverage, equal-project % |','|---|---:|---:|---:|---:|']
for a in arms:
    q=full['arms'][a]; lines.append(f"| {a} | {q['accepted']} | {100*q['pooled_rate']:.4f} | {100*q['equal_project_rate']:.4f} | {q['equal_project_penalized_module_line_pct']:.4f} |")
lines += ['', '## Weighting discrepancy','', '[JSON: full.contrasts; weighting_decomposition]', '']
for a,b in contrasts:
    name=a+'-'+b; q=full['contrasts'][name]
    lines.append(f"- {name}: pooled {100*q['pooled_difference']:+.4f} pp; equal-project {100*q['equal_project_difference']:+.4f} pp; {q['project_wins']}/{q['project_ties']}/{q['project_losses']} project wins/ties/losses.")
lines += ['', 'This is a change of estimand: pooled rates weight projects by target counts; the primary estimand weights every project equally. For codetiming, one target gives two pairs: verified setup loses one acceptance, a -50 pp project effect and a -2.3810 pp contribution to the 21-project mean, versus -0.0775 pp to the pooled mean. Keep that project in all analyses; explain the leverage rather than deleting it. The decomposition records every project contribution.','',
'## Complete project results','', '[JSON: per_project; differences in percentage points]','',
'| Project | Targets | Source accepted | Verified accepted | Context accepted | Context-source pp |','|---|---:|---:|---:|---:|---:|']
for p in projects:
    q=per_project[p]; lines.append(f"| {p} | {q['targets']} | {q['arms']['source']['accepted']} | {q['arms']['verified_setup']['accepted']} | {q['arms']['context_setup']['accepted']} | {100*q['contrasts']['context_setup-source']['equal_project_difference']:+.4f} |")
lines += ['', '## Terminal failure categories','',
'These are terminal runner labels, not causal diagnoses or conditional stage probabilities. Collection failures may be included in test_failure; no finer failure category is fabricated. [JSON: full.arms.*.status_counts and full.contrasts.*.terminal_status_transition_counts]','',
'| Status | Source | Verified | Context |','|---|---:|---:|---:|']
for status in sorted({r['status'] for r in rows.values()}):
    lines.append('| '+status+' | '+' | '.join(str(full['arms'][a]['status_counts'].get(status,0)) for a in arms)+' |')
lines += ['', 'The following mutually exclusive refinement retains the full planned denominator. For terminal test_failure, inspect eval0/pytest.json with precedence: failed collector, failed setup/teardown, failed test call, other reported, unavailable report. Mixed failures are assigned by this precedence, not counted twice. These describe where pytest failed, not the semantic root cause. [JSON: stage_failure_partition; stage_failure_records, including raw report paths]', '',
'| Stage partition | Source | Verified | Context |','|---|---:|---:|---:|']
for category in sorted(set().union(*(set(c) for c in stage_counts.values()))):
    lines.append('| '+category+' | '+' | '.join(str(stage_counts[a][category]) for a in arms)+' |')
lines += ['', '## Exhaustive subgroup summaries','',
'All strata retain both seeds and all arms, including failed attempts. Equal-project means balance only projects represented within that stratum; varying project composition and correlated target attributes prevent causal subgroup or interaction conclusions. Closure availability is supplementary descriptive context. The setup-by-kind cross-tab partitions all targets exactly. No subgroup p-values or confidence intervals are computed. [JSON: subgroups]','',
'| Stratum | Targets | Projects | Source accepted | Verified accepted | Context accepted | Context-source pooled pp | Context-source balanced pp | Verified-source balanced pp |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for dim,groups in subgroups.items():
    for label,q in groups.items():
        lines.append(f"| {dim}:{label} | {q['targets']} | {q['projects']} | {q['arms']['source']['accepted']} | {q['arms']['verified_setup']['accepted']} | {q['arms']['context_setup']['accepted']} | {100*q['contrasts']['context_setup-source']['pooled_difference']:+.4f} | {100*q['contrasts']['context_setup-source']['equal_project_difference']:+.4f} | {100*q['contrasts']['verified_setup-source']['equal_project_difference']:+.4f} |")
lines += ['', 'Unavailable setup does not imply a setup intervention was delivered. Residual arm differences in identical-prompt strata can arise from generation/execution variation; they do not establish a setup mechanism. Availability itself is not randomized.','',
'## Seed sensitivity','', '[JSON: by_seed; seed_stability; context_source_target_delta_seed71_seed72]','',
'| Seed | Source accepted | Verified accepted | Context accepted | Context-source pooled pp | Context-source balanced pp | Verified-source balanced pp |','|---|---:|---:|---:|---:|---:|---:|']
for s,q in by_seed.items():
    lines.append(f"| {s} | {q['arms']['source']['accepted']} | {q['arms']['verified_setup']['accepted']} | {q['arms']['context_setup']['accepted']} | {100*q['contrasts']['context_setup-source']['pooled_difference']:+.4f} | {100*q['contrasts']['context_setup-source']['equal_project_difference']:+.4f} | {100*q['contrasts']['verified_setup-source']['equal_project_difference']:+.4f} |")
lines.append('')
for a,q in seed_stability.items():
    lines.append(f"- {a}: {q['accepted_both']} targets accepted on both seeds; {q['accepted_exactly_one']} on exactly one; {q['accepted_neither']} on neither.")
lines += ['', 'The combined equal-project effect is the arithmetic mean of the two seed-specific effects because each project has the same target frame at both seeds. Two seeds do not establish robustness across generation settings, and are not independent projects.','',
'## Standalone acceptance versus joint-pack usability','',
'This audit was added after generation began and remains supplementary exploratory. It combines every accepted suite across both seeds without editing. Failure of one test can invalidate a whole pack; the selected test count differs by arm. Higher standalone acceptance therefore need not imply better integration. [JSON: joint_pack_summary; joint_pack_details]','',
'| Arm | Passing packs / 21 | Nonempty failed projects | Expected / collected nodes | Available measured projects | Measured available-case coverage % | Validated coverage, all 21 % |','|---|---:|---|---:|---:|---:|---:|']
for a,q in pack_summary.items():
    lines.append(f"| {a} | {q['packs_pass']} | {', '.join(q['nonempty_failed_projects']) or 'none'} | {q['expected_nodes']} / {q['collected_nodes']} | {q['available_measured_projects']} | {q['available_case_measured_coverage_pct']:.4f} | {q['equal_project_validated_pack_coverage_pct']:.4f} |")
lines += ['', 'An empty pack counts as nonpassing, not as an executed failure. Source and context each have an empty dataclasses-json pack; verified setup has no empty pack. All expected nodes were collected, which does not imply that all nodes passed. Validated pack coverage is zero for nonpassing/empty packs. Available-case measured coverage excludes missing measurements and can include coverage from failing packs; it must not replace the all-project validated measure. Standalone and pack coverage use different denominators and cannot be interpreted as a common treatment effect. The result supports an integration/usability limitation, not an identified cause or proof that more context intrinsically harms integration.','',
'## Independent check of the existing inference','',
'Project effects were recomputed from individual outcome booleans. Exact sign-flip probabilities were recomputed using rational effects scaled to a common integer denominator and an integer subset-sum distribution, independent of the frozen floating-point sign enumeration. The original 20,000 project bootstrap draws and two-secondary Holm adjustment were reproduced. This verifies arithmetic, not the inferential assumptions. [JSON: existing_statistics_independent_verification; existing_secondary_holm_verified]','',
'| Existing contrast | Balanced effect pp | Original bootstrap 95%, pp | Exact p | Secondary Holm p |','|---|---:|---|---:|---:|']
for name,q in verification.items():
    lo,hi=q['bootstrap_95']; hp=f"{holm[name]:.9f}" if name in holm else 'outside secondary family'
    lines.append(f"| {name} | {100*q['equal_project_difference']:+.6f} | [{100*lo:.6f}, {100*hi:.6f}] | {q['exact_p']:.9f} | {hp} |")
lines += ['',
'The primary interval includes zero and the exact primary p-value does not support a superiority claim. The context-versus-verified marginal bootstrap interval excludes zero while the exact p exceeds .05 and its Holm-adjusted p is about .111: different procedures can disagree. Do not promote that marginal interval to multiplicity-controlled evidence. Sign-flip inference needs independent project-effect sign exchangeability/symmetry; bootstrap calibration is limited with 21 heterogeneous, previously observed projects. Passing generated tests is not independent semantic oracle validation or full Test4Py efficacy.','',
'## Actionable editorial conclusions','',
'1. Lead with the prespecified equal-project primary effect and its uncertainty; show pooled counts as descriptive support, with the full paired turnover table.',
'2. Explain the verified-setup pooled/balanced sign reversal using unequal project weights and the complete contribution decomposition. Do not remove codetiming or redefine the primary estimand.',
'3. Present setup availability, class/function and their complete cross-tab as hypothesis-generating descriptions, with denominators and represented-project counts; avoid subgroup superiority claims.',
'4. Place standalone acceptance and joint-pack usability side by side, and distinguish empty packs, failing nonempty packs, measured coverage availability, and validated coverage over all projects.',
'5. State that all projects were previously observed and two seeds repeat targets within projects. Independent assertion review, mutation/real-fault validation and a prospective held-out-project evaluation remain necessary for stronger efficacy claims.','']
(OUT/'deep_analysis_notes.md').write_text('\n'.join(lines))
print(json.dumps(dict(written=[str(OUT/'deep_analysis.json'),str(OUT/'deep_analysis_notes.md')],primary=full['contrasts']['context_setup-source'],seed_effects={s:q['contrasts']['context_setup-source']['equal_project_difference'] for s,q in by_seed.items()},packs=pack_summary),indent=2))
