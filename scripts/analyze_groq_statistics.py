"""Cluster-aware descriptive inference and prospective sensitivity, no API calls."""
import itertools
import json
import math
from pathlib import Path
from statistics import NormalDist, mean

ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'research/groq_study_20261118_v2'


def main():
    data=json.loads((STUDY/'summary.json').read_text())
    pairs={}
    for row in data['rows']:
        pairs.setdefault((row['project'],row['target_id'],row['seed']),{})[row['arm']]=row
    differences={}
    for (project,target,seed),arms in pairs.items():
        if len(arms)==2:
            d=int(arms['ast_dependencies']['accepted'])-int(arms['source_only']['accepted'])
            differences.setdefault(project,[]).append(d)
    effects={p:mean(ds) for p,ds in differences.items()}
    observed=mean(effects.values())
    permutation=[mean(s*x for s,x in zip(signs,effects.values()))
                 for signs in itertools.product((-1,1),repeat=len(effects))]
    p=sum(abs(x)>=abs(observed)-1e-12 for x in permutation)/len(permutation)
    bootstrap=[mean(effects[x] for x in sample)
               for sample in itertools.product(effects,repeat=len(effects))]
    bootstrap.sort()
    # Exact enumeration of the finite bootstrap distribution, not a claim of coverage calibration with 3 clusters.
    interval=[bootstrap[int((len(bootstrap)-1)*q)] for q in (.025,.975)]
    z=NormalDist().inv_cdf(.975)+NormalDist().inv_cdf(.8)
    sensitivity=[]
    for effect in (.05,.10,.15):
        for discordance in (.25,.5):
            n=math.ceil(z*z*(discordance-effect*effect)/(effect*effect))
            sensitivity.append(dict(minimum_difference=effect,discordance_assumption=discordance,
                independent_pairs_normal_approx=n,
                clustered_pairs_assuming_3_targets_per_project_ICC_0_1=math.ceil(n*1.2)))
    out=dict(scope='exploratory; three project clusters cannot establish general superiority',
        paired_repetitions=len(pairs),independent_projects=len(effects),project_effects=effects,
        equal_project_weighted_difference=observed,
        cluster_sign_flip_two_sided_p=p,
        minimum_attainable_two_sided_sign_flip_p=2/(2**len(effects)),
        cluster_bootstrap_percentile_95_interval=interval,
        interval_warning='Only three clusters; percentile interval poorly calibrated, descriptive only.',
        sensitivity=sensitivity,
        power_warning='Normal approximation assuming paired binary outcomes, two-sided alpha .05, power .80. '
                      'Discordance/ICC are assumptions, not established pilot estimates. Not a guarantee. '
                      'Repeated seeds do not substitute independent projects. No observed/post-hoc power claim.')
    (STUDY/'statistics.json').write_text(json.dumps(out,indent=2)+'\n')
    lines=['**Phân tích thống kê và cỡ mẫu**','',
        f'Có {len(pairs)} cặp lượt, nhưng chỉ {len(effects)} cụm project độc lập ở mức thiết kế.',
        f'Chênh lệch pass AST − source, trọng số đều theo project: {observed*100:.2f} điểm phần trăm.',
        f'Kiểm tra sign-flip theo project: p hai phía = {p:.3f}; với 3 cụm, p nhỏ nhất có thể là 0,25.',
        'Không thể dùng chiến dịch này để cam kết p < 0,05 hoặc khái quát vượt phương pháp gốc.',
        '', '| Mức tăng cần phát hiện | Giả định discordance | Cặp độc lập xấp xỉ | Có design effect 1,2 |',
        '|---|---:|---:|---:|']
    for r in sensitivity:
        lines.append(f"| {r['minimum_difference']*100:.0f} điểm % | {r['discordance_assumption']} | {r['independent_pairs_normal_approx']} | {r['clustered_pairs_assuming_3_targets_per_project_ICC_0_1']} |")
    lines+=['','Giả định: alpha hai phía 0,05; power 80%; xấp xỉ chuẩn cho binary paired; ICC 0,1, ba target/project chỉ là sensitivity. Không bảo đảm ý nghĩa thống kê. Cần chốt effect thực tiễn, lấy mẫu project và cập nhật variance trước confirmatory study. Không tăng seed để giả tăng số project.']
    (STUDY/'STATISTICS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:out[k] for k in ('independent_projects','equal_project_weighted_difference','cluster_sign_flip_two_sided_p')}))


if __name__=='__main__':main()
