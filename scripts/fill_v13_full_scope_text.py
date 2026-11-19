"""Materialize v13 narrative only after all outcomes and independent replay exist."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'research/groq_full_scope_20261119';D=R/'research/editorial_v13'
def load(p):return json.loads(p.read_text())
def vn(v,d=2):
 if d==2 and v and abs(v)<.005:d=6
 return f'{v:.{d}f}'.replace('.',',')
def pvalue(v):return vn(v,8 if 0<v<.00001 else 5)
def main():
 completion=load(W/'completion.json');assert completion['complete'] and completion['completed']==3870
 m=load(W/'manifest.json');s=load(W/'summary.json');f=load(W/'statistics.json');b=load(W/'budget.json');assert f['final'] and f['completed']==3870
 replays=sorted((W/'independent_replays').glob('*/replay_summary_*.json'),key=lambda p:p.stat().st_mtime)
 assert replays,'Independent replay has not completed';replay=next(load(p) for p in reversed(replays) if load(p)['scope']=='official all-study replay audit');assert replay['complete']
 primary=f['contrasts']['context_setup-source'];lo,hi=primary['percentile_95'];pv=primary['exact_signflip_two_sided_p']
 if lo>0 and pv<.05:interpretation='Trong phạm vi đánh giá đã khóa, dữ liệu cung cấp bằng chứng cải thiện tỷ lệ đạt của nhánh ngữ cảnh kết hợp, với các giả định thống kê đã nêu.'
 elif hi<0 and pv<.05:interpretation='Trong phạm vi đánh giá đã khóa, dữ liệu ghi nhận tỷ lệ đạt thấp hơn ở nhánh ngữ cảnh kết hợp; kết quả không ủng hộ giả thuyết cải tiến của cấu hình này.'
 else:interpretation='Khoảng bất định và kiểm định chưa đồng thời xác lập ưu thế của nhánh ngữ cảnh kết hợp; mức chênh lệch quan sát không được xem là cải tiến vững trên mọi dự án.'
 vals={'COMPLETED':str(s['completed']),'PRIMARY_DIFF':vn(primary['difference']*100),'PRIMARY_LO':vn(lo*100),'PRIMARY_HI':vn(hi*100),'PRIMARY_P':pvalue(pv),'PRIMARY_INTERPRETATION':interpretation,'ACCEPTED_TOTAL':str(sum(a['successes'] for a in f['arms'].values())),'REPLAY_COUNT':str(replay['replayed']),'REPLAY_PASSED':str(replay['pass_count']),'REPLAY_MATCHED':str(replay['exact_coverage_matches']),'REPLAY_INTERPRETATION':('Các bộ được nhận đều tái chạy trong điều kiện đã kiểm tra; kết quả này không bảo đảm tính đúng đắn của mọi điều kiện khẳng định.' if replay['pass_count']==replay['accepted_count'] and replay['exact_coverage_matches']==replay['accepted_count'] else 'Các trường hợp chạy lại không đạt hoặc không khớp độ phủ được giữ trong báo cáo phụ trợ; chúng giới hạn mức ổn định có thể kết luận và không bị xóa khỏi hồ sơ.'),'SETTLED_RESPONSES':str(b['settled_responses']),'SETTLED_COST':vn(float(b['settled_api_estimate_usd']),6),'ACCOUNTED_COST':vn(float(b['accounted_total_usd']),6),'FULL_COST':vn(float(b['cohort_estimate_usd']),6)}
 for label,arm in [('SOURCE','source'),('SETUP','verified_setup'),('CONTEXT','context_setup')]:
  a=f['arms'][arm];vals.update({label+'_K':str(a['successes']),label+'_PR':vn(100*a['successes']/a['denominator']),label+'_EQ':vn(a['equal_project_acceptance_rate']*100)})
 for label,name in [('SETUP','verified_setup-source'),('CLOSURE','context_setup-verified_setup')]:
  c=f['contrasts'][name];vals[label+'_DIFF']=vn(c['difference']*100);vals[label+'_HOLM']=pvalue(c['holm_adjusted_p'])
 joint=load(W/'joint_packs/main/summary.json');assert joint['complete'] and joint['completed_packs']==63
 for label,arm in [('SOURCE','source'),('SETUP','verified_setup'),('CONTEXT','context_setup')]:
  vals[label+'_PACKS']=str(joint['arms'][arm]['packs_pass']);vals[label+'_PACK_COVERAGE']=vn(joint['arms'][arm]['equal_project_validated_pack_coverage_pct'])
 template=(D/'report_body.template.md').read_text();text=re.sub(r'\{\{(\w+)\}\}',lambda match:vals[match.group(1)],template);assert '{{' not in text
 costs={}
 for arm in m['arms']:
  rows=[r for r in s['rows'] if r['arm']==arm];inputs=sum(r['usage']['prompt_tokens'] for r in rows);outputs=sum(r['usage']['completion_tokens'] for r in rows);cost=(inputs*.075+outputs*.30)/1000000;accepted=f['arms'][arm]['successes'];costs[arm]=dict(prompt_tokens=inputs,completion_tokens=outputs,estimated_usd=cost,per_accepted_usd=cost/accepted if accepted else None)
 (W/'arm_cost_metrics.json').write_text(json.dumps(costs,indent=2))
 (D/'report_body.md').write_text(text);(D/'resolved_values.json').write_text(json.dumps(vals,ensure_ascii=False,indent=2))
 (D/'full_benchmark_scope.json').write_text(json.dumps(dict(status='completed_full_eligibility_frame',eligible_symbols=645,eligible_modules=169,projects=21,arms=m['arms'],seed_values=m['seed_values'],completed=3870,project_scope=m['project_scope'],source_scope=m['source_scope'],independent_replay_report=str(next(p for p in reversed(replays) if load(p)['scope']=='official all-study replay audit').relative_to(R))),ensure_ascii=False,indent=2))
 print('Resolved v13 evidence and narrative from completed3870 cases')
if __name__=='__main__':main()
