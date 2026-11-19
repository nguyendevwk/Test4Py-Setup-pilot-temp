"""Paired descriptive accounting; no missing coverage imputation or efficacy claim."""
from collections import Counter


def analyze(manifest, summary):
    arms=manifest['arms']
    if len(arms)!=2:
        raise ValueError('This descriptive analysis requires two locked arms')
    targets={t['id']:t for t in manifest['targets']}
    if len(targets)!=len(manifest['targets']):
        raise ValueError('Duplicate planned case id')
    planned={(case,arm) for case in targets for arm in arms}
    observed={}
    for row in summary['rows']:
        key=(row['id'],row['arm'])
        if key not in planned or key in observed:
            raise ValueError('Unexpected or duplicated outcome: '+str(key))
        observed[key]=row
    rows=[]
    for case,target in targets.items():
        for arm in arms:
            row=dict(id=case,arm=arm,project=target['project'],module=target['module'],seed=target['seed'],
                     target_id=target.get('target_id',case),status='not_completed',meaningful_target_test=None)
            row.update(observed.get((case,arm),{}));rows.append(row)

    def counts(selected):
        values=[r.get('meaningful_target_test') for r in selected]
        return dict(planned=len(values),successful=sum(v is True for v in values),
                    known=sum(isinstance(v,bool) for v in values),unknown=sum(not isinstance(v,bool) for v in values),
                    statuses=dict(Counter(r['status'] for r in selected)))
    overall={a:counts([r for r in rows if r['arm']==a]) for a in arms}
    projects=[]
    for project in sorted({r['project'] for r in rows}):
        a,b=(counts([r for r in rows if r['project']==project and r['arm']==arm]) for arm in arms)
        # Bounds express incomplete outcomes, not statistical confidence intervals.
        low=b['successful']/b['planned']-(a['successful']+a['unknown'])/a['planned']
        high=(b['successful']+b['unknown'])/b['planned']-a['successful']/a['planned']
        projects.append(dict(project=project,control=a,treatment=b,
            paired_delta_pp=100*low if a['unknown']==b['unknown']==0 else None,
            missing_outcome_delta_bounds_pp=[100*low,100*high]))
    cases=[]
    for case,target in targets.items():
        a,b=(observed.get((case,arm),{}).get('meaningful_target_test') for arm in arms)
        cases.append(dict(id=case,project=target['project'],seed=target['seed'],target_id=target.get('target_id',case),
                          delta=int(b)-int(a) if isinstance(a,bool) and isinstance(b,bool) else None))
    paired_counts=dict(Counter(str(r['delta']) if r['delta'] is not None else 'unknown' for r in cases))
    return dict(arms=arms,planned=len(planned),summary_rows=len(observed),overall=overall,projects=projects,cases=cases,
        paired_counts=paired_counts,distinct_targets=len({t.get('target_id',t['id']) for t in targets.values()}),
        project_clusters=len(projects),full_pipeline_efficacy=False,semantic_review_required=True,
        interpretation='Success means a stable all-pass suite reaching the target, not proven assertion correctness. '
                       'Seeds repeat targets within project clusters; no significance or equivalence claim is inferred. '
                       'Unknown outcomes remain explicit. Missing-outcome bounds are not confidence intervals.')
