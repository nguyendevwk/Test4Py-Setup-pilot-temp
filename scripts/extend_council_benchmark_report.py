"""Copy v9 into v10 and report every external-project benchmark outcome."""
import json,hashlib,shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from revise_kaggle_groq_narrative import before,table_before,rebuild_lists
from polish_council_report import polish_tables

R=Path(__file__).resolve().parents[1];W=R/'research/groq_codamosa_extension_20261119'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 src=R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v9.docx';out=R/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v10.docx'
 if out.exists():raise RuntimeError('New output required; existing versions preserved')
 m=json.loads((W/'manifest.json').read_text());s=json.loads((W/'summary.json').read_text());st=json.loads((W/'statistics.json').read_text());eb=json.loads((W/'budget.json').read_text());b=json.loads((R/'research/groq_context_development_20261119/budget.json').read_text());b.update(extension_responses=eb['extension_responses'],extension_estimate_usd=eb['extension_estimate_usd']);replay=json.loads((W/'independent_replay_summary.json').read_text())
 assert s['completed']==m['planned'];old=digest(src);shutil.copy2(src,out);doc=Document(out)
 def pfx(text):return next(p for p in doc.paragraphs if p.style.name!='CouncilTOC' and p.text.startswith(text))
 anchor=pfx('CHƯƠNG 5.')
 before(anchor,'4.12. Mở rộng trên các project độc lập từ khung benchmark CodaMOSA','Heading 2')
 before(anchor,'Để mở rộng phạm vi ngoài tập đã quan sát, đợt bổ sung khóa trước 12 project ngoài các cohort Groq trước theo danh sách module công bố trong artifact CodaMOSA [23]. Danh sách ứng viên, module frame, commit nguồn artifact, tiêu chí source-only, seed và kế hoạch phân tích được lưu trước inference. Không dùng kết quả mô hình để chọn project, target hoặc dừng khi đạt p-value thuận lợi. Các package được cài vào môi trường riêng, khóa phiên bản và source hashes. Đây là đánh giá thích nghi trên bản PyPI được ghi nhận, không phải tái lập container/commit nguyên gốc của CodaMOSA hoặc chạy thuật toán CodaMOSA.')
 before(anchor,f"Trong 36 slot target dự kiến, {len(m['targets'])} target đủ tiêu chí; codetiming chỉ có một target công khai đáp ứng quy tắc source đã khóa, nên hai slot thiếu không được xem là mô hình thất bại. Cả 12 project đều có target; không trùng project của các cohort Groq trước. Tuy nhiên codetiming, docstring_parser, python-string-utils và typesystem đã xuất hiện trong tập phát triển lịch sử 105 lượt; vì vậy không gọi cả 12 project là held-out toàn dự án. Tám project còn lại bổ sung phạm vi ngoài cả tập 105 và các cohort Groq đó; đối chiếu lịch sử được lưu riêng, không đổi mẫu sau khi chạy. Ba seed 42/43/44, hai nhánh source và setup xác minh, cap 2.048, đúng ba hàm test, không repair tạo {m['planned']} lượt. Tiêu chí nhận giữ nguyên: gate tĩnh, toàn bộ test pass, coverage module dương, witness chạy thân target và replay khớp coverage. Setup probe được chấp nhận ở {sum(t['setup_probe']['accepted'] for t in m['targets'])}/{len(m['targets'])} target; khi probe không qua, hai prompt không khác nội dung hint, nên tương phản chính đo hiệu ứng chính sách cung cấp hint khi có thể thực thi.")
 before(anchor,'Bảng 4.18. Toàn bộ kết quả trên 12 project bổ sung; không chọn theo tỷ lệ đạt','Caption')
 rows=[['Project / phiên bản','Target','Source đạt/lượt','Setup đạt/lượt','Chênh lệch (đpt)']]
 versions={p['project']:p['version'] for p in m['projects']}
 for p,r in st['per_project'].items():rows.append([p+' / '+versions[p],str(r['targets']),f"{r['source_successes']}/{r['paired_attempts']}",f"{r['verified_successes']}/{r['paired_attempts']}",f"{100*r['paired_difference']:+.2f}"])
 table_before(doc,anchor,rows)
 a=s['arms']['atomic_source'];v=s['arms']['atomic_verified_setup'];lo,hi=[100*x for x in st['difference_percentile_95']];effect=100*st['difference']
 before(anchor,f"Theo lượt, source đạt {a['passed']}/{a['planned']} ({a['pass_rate_pct']:.2f}%), setup đạt {v['passed']}/{v['planned']} ({v['pass_rate_pct']:.2f}%); SC module có penalty tương ứng {a['penalized_module_line_pct']:.2f}% và {v['penalized_module_line_pct']:.2f}%. Vì số target/project không hoàn toàn bằng nhau, suy luận chính lấy trung bình chênh lệch trong từng project rồi cân bằng 12 project: {effect:+.2f} điểm phần trăm, bootstrap project 95% [{lo:.2f}; {hi:.2f}], sign-flip hai phía p={st['exact_cluster_signflip_two_sided_p']:.5f}. Không dùng khoảng Wilson theo lượt làm suy luận độc lập; không cộng thêm seed để tăng số project.")
 interpretation=('Khoảng tin cậy còn chứa 0; đợt này chưa đủ bằng chứng xác lập ưu thế thống kê của chính sách setup.' if lo<=0<=hi else 'Khoảng bootstrap không chứa 0 trong đợt này; vẫn cần đối chiếu giả định sign-flip, sai lệch lựa chọn và chất lượng oracle trước khi khái quát.')
 before(anchor,interpretation+' Kết luận của đợt 9 project trước được giữ nguyên theo cohort; hai đợt không được gộp tùy tiện sau khi đã thấy kết quả. Phân tầng theo trạng thái probe là phân tích thăm dò về khả năng chuyển giao hint, không phải cách loại các ca thất bại khỏi mẫu số.')
 assets=out.parent/(out.stem+'_assets');assets.mkdir();prior=json.loads((R/'research/groq_confirmation_20261118/statistics.json').read_text())
 fig,ax=plt.subplots(figsize=(6.3,2.8));stats=[prior,st]
 for i,t in enumerate(stats):
  e=t['difference']*100;l,h=[x*100 for x in t['difference_percentile_95']];ax.errorbar(e,i,xerr=[[e-l],[h-e]],fmt='o',capsize=5,color=['#55758C','#276749'][i]);ax.text(h+.6,i,f'{e:+.2f}',va='center',fontsize=9)
 ax.axvline(0,color='gray',linestyle='--');ax.set_yticks([0,1],['Đợt trước: 9 project','Mở rộng: 12 project']);ax.set_xlabel('Setup − source (điểm phần trăm); CI 95% theo project');ax.grid(axis='x',alpha=.2);ax.set_ylim(-.6,1.6);fig.tight_layout();image=assets/'external_project_effects.png';fig.savefig(image,dpi=300);plt.close(fig)
 p=before(anchor,'');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=0;p.add_run().add_picture(str(image),width=Cm(15.5))
 before(anchor,'Hình 4.8. Hiệu ứng cân bằng project và bất định của hai cohort riêng biệt; không phải kết quả gộp.','Caption')
 before(anchor,f"Replay độc lập các artifact được nhận: {replay['passed']}/{replay['planned']} pass, {replay['exact_line_matches']}/{replay['planned']} khớp độ phủ. Đây là kiểm tra tái chạy artifact, không chứng minh oracle đúng 100% hoặc phát hiện lỗi thật. Quy trình lưu cả collection/test failures; không lọc node, sửa assertion hay repair để nâng tỷ lệ chính. Một sửa chữa hạ tầng đã ghi biên bản: hai file PySnooper dùng CRLF, trong khi preparer hash văn bản đã chuẩn hóa; runner được sửa để kiểm tra cùng quy ước, giữ nguyên sáu outcome có trước và không gọi lại thay kết quả. Raw bytes có hash riêng trong PREFLIGHT_VALIDATION.json.")
 before(anchor,'Nguồn: research/groq_codamosa_extension_20261119/{PROVENANCE,manifest,summary,statistics,independent_replay_summary,PREFLIGHT_VALIDATION}.json. Mô hình/API là alias GPT-OSS-20B, seed best effort; raw prompt/response và source đã khóa hỗ trợ audit và replay, không bảo đảm inference mới giống từng byte.')
 before(anchor,'4.13. Giá trị ứng dụng của kết quả 14B NF4 được giữ lại','Heading 2')
 ext=json.loads((R/'research/14b_extended_replay_20261119/summary.json').read_text())
 before(anchor,'Bên cạnh bộ 12 test baseline, lịch sử dự án có bản mở rộng ứng dụng genty: giữ nguyên hai file chứa 12 test, bổ sung nguyên văn hai test từ lần sinh Qwen2.5-Coder-14B NF4 source-first/API facts. Model revision và hash của candidate đã được ghi ở manifest cũ. Bản mở rộng được tuyển chọn sau quan sát development; nó chứng minh giá trị tái sử dụng artifact cụ thể, không thay thế tỷ lệ đạt toàn bộ benchmark hoặc xác nhận ưu thế thuật toán.')
 before(anchor,'Bảng 4.19. Kiểm chứng lại bộ ứng dụng 14B: giữ nguyên test cũ và bổ sung test thật','Caption')
 table_before(doc,anchor,[['Chỉ số cùng source genty đã khóa','Bộ 12 test cũ','Bộ 14 test mở rộng'],['Replay CPU mới','12/12','14/14, cả 3 process'],['Line coverage genty_args','18/20 (90%)','20/20 (100%)'],['Branch coverage genty_args','NA (0/0)','NA (0/0)'],['Line / branch genty_repeat','8/8 ; 2/2','8/8 ; 2/2'],['Hai mutant iterator lịch sử, chọn post-hoc','0/2 killed; 2 survived','2/2 killed; 0 survived']])
 before(anchor,'Lần kiểm chứng mới dùng Python 3.10, các byte test gốc và sáu source hashes không đổi. Ba process độc lập đều đạt 14/14; bộ cũ và bộ mới được chạy trên cùng source và cùng hai mutant đã có trong hồ sơ lịch sử. Một mutant bỏ format positional arguments, mutant kia đảo thứ tự keyword arguments; chỉ lỗi assertion sau khi collect/run đúng các node mới được credit killed. Đây là hai mutant được chọn sau review development, không phải lỗi thực BugsInPy, pool ngẫu nhiên hay fault benchmark held-out. Không quy kết 100% phát hiện lỗi từ mẫu 2 mutant này.')
 before(anchor,'Dữ liệu mới xác nhận đóng góp ứng dụng có thể đo của giai đoạn 14B: tăng phạm vi kiểm tra iterator và phát hiện hai thay đổi hành vi mà bộ cũ bỏ sót, đồng thời giữ nguyên các kiểm thử đã có. Thời gian replay loại trừ sinh mô hình; không dùng nó so tốc độ 14B và Groq. Nguồn: research/application/14b_genty_extended_20261117/{manifest,verification}.json và research/14b_extended_replay_20261119/summary.json; các kết quả bất lợi của pipeline và cohort 14B vẫn giữ riêng.')
 before(anchor,'4.14. Cải tiến ngữ cảnh helper: screen phát triển sau đánh giá mở rộng','Heading 2')
 dev=json.loads((R/'research/groq_context_development_20261119/summary.json').read_text());dm=json.loads((R/'research/groq_context_development_20261119/manifest.json').read_text());dr=json.loads((R/'research/groq_context_development_20261119/independent_replay_summary.json').read_text())
 before(anchor,'Sau khi quan sát mức cải thiện hạn chế của setup, screen phát triển bổ sung ngữ cảnh declaration thật: AST lần theo tên helper/global cùng module tối đa hai mức, tối đa 8.000 ký tự tổng và 4.000 ký tự mỗi declaration, kết hợp setup probe có sẵn. Không lấy expected output, test generated hoặc assertion làm ngữ cảnh. Toàn bộ 34 target được giữ, seed mới 46, hai nhánh source và context+setup, cap 2.048, zero-repair: 68 lượt. Chỉ 17/34 target có closure bổ sung. Hai cơ chế được thêm cùng nhau, nên screen không tách được hiệu ứng riêng của closure và setup; đây là phát triển trên tập đã quan sát, không phải xác nhận độc lập.')
 before(anchor,'Bảng 4.20. Screen phát triển ngữ cảnh helper trên toàn bộ tập đã quan sát','Caption')
 rr=[['Nhánh','Đạt / 34','SC penalty (%)','Phạm vi']]
 for arm in dm['arms']:
  g=dev['arms'][arm];rr.append(['Source' if arm=='atomic_source' else 'AST closure + setup',str(g['passed'])+'/34',f"{g['penalized_module_line_pct']:.2f}",'Development; seed 46'])
 table_before(doc,anchor,rr)
 before(anchor,f"Kết quả source 11/34 (32,35%) và context+setup 12/34 (35,29%); SC tăng từ 17,50% lên 19,52%. {dr['passed']}/{dr['planned']} artifact được nhận pass khi replay độc lập và khớp coverage. Chênh lệch một lượt chưa chứng minh cải tiến vững; không cộng screen vào cỡ mẫu xác nhận hoặc chọn riêng target thuận lợi. Đây là bước cải tiến có triển khai và có kết quả đo, nhưng vẫn cần nhiều project độc lập và đánh giá oracle/fault để kết luận tổng quát. Nguồn: research/groq_context_development_20261119/manifest.json và summary.json.")
 sensitivity=json.loads((W/'history_scope_sensitivity.json').read_text());sl,sh=[v*100 for v in sensitivity['difference_percentile_95']]
 before(anchor,f"Đối chiếu phạm vi lịch sử (hậu kiểm, không phải primary mới): khi chỉ mô tả tám project không nằm trong tập 105 và các cohort Groq trước, source đạt 19/72, setup 24/72; chênh lệch cân bằng project {sensitivity['difference']*100:+.2f} điểm, CI95% [{sl:.2f}; {sh:.2f}]. Phân tích này vẫn chứa 0 và không dùng để thay kết luận toàn bộ 12 project. Nguồn: history_scope_sensitivity.json và HISTORICAL_OVERLAP_DISCLOSURE.json.")
 conclusion=pfx('Đánh giá mở rộng hoàn tất')
 conclusion.text+=f" Đợt benchmark bổ sung hoàn tất {m['planned']} lượt trên {len(m['targets'])} target/12 project bổ sung, mở rộng độ phủ dự án; chênh lệch cân bằng project {effect:+.2f} điểm, CI95% [{lo:.2f}; {hi:.2f}]. {interpretation} Số lượt thực nghiệm tăng không tự bảo đảm ý nghĩa thống kê hoặc vượt full Test4Py."
 budget=pfx('Ngân sách toàn chiến dịch được giới hạn')
 budget.text=f"Ngân sách toàn chiến dịch được giới hạn 3 USD. Sau đợt benchmark và screen phát triển bổ sung, sổ request ghi {b['settled_responses']} response có usage; ước tính usage theo giá cấu hình {float(b['settled_api_estimate_usd']):.6f} USD. Phân bổ bảo thủ cộng các reserve chưa quyết toán và khoản đối soát mốc ban đầu là {float(b['accounted_total_usd']):.6f} USD, nằm trong trần. Đây không phải hóa đơn nhà cung cấp; không cộng hai con số thành chi phí. Riêng đợt CodaMOSA-frame {b['extension_responses']} response có ước tính {float(b['extension_estimate_usd']):.6f} USD. Nguồn: research/groq_codamosa_extension_20261119/budget.json; HTTP status, usage và ledger được lưu để kiểm tra hạn mức/rate limit."
 appendix=pfx('PHỤ LỤC. NGUỒN DỮ LIỆU')
 before(appendix,'[23] Microsoft, “CodaMOSA Artifact — ICSE 2023”, replication/README.md và replication/scripts/modules_base_and_name.csv, commit '+st['project_selection']['commit']+'. https://github.com/microsoft/codamosa/tree/'+st['project_selection']['commit']+'/replication ; raw test dataset: https://github.com/microsoft/codamosa-dataset. Truy cập 19/11/2026.')
 for p in doc.paragraphs:
  if 'cần cập nhật mục lục và kiểm tra bố cục' in p.text:p.text=p.text.replace('cần cập nhật mục lục và kiểm tra bố cục bằng Word/LibreOffice trước khi nộp.','mục lục và bố cục được kiểm tra lại trên PDF của bản hiện hành.')
 for name in ['PROVENANCE.json','summary.json','statistics.json','budget.json','independent_replay_summary.json']:
  before(appendix,'research/groq_codamosa_extension_20261119/'+name+' — SHA256 '+digest(W/name))
 before(appendix,'research/groq_context_development_20261119/summary.json — SHA256 '+digest(R/'research/groq_context_development_20261119/summary.json'))
 before(appendix,'research/14b_extended_replay_20261119/summary.json — SHA256 '+digest(R/'research/14b_extended_replay_20261119/summary.json'))
 polish_tables(doc);rebuild_lists(doc)
 for paragraph in doc.paragraphs:
  if paragraph.style.name=='Caption' and paragraph.text.startswith('Bảng'):paragraph.paragraph_format.keep_with_next=True
 for table in doc.tables:
  for ri,row in enumerate(table.rows):
   for ci,cell in enumerate(row.cells):
    for paragraph in cell.paragraphs:
     paragraph.paragraph_format.first_line_indent=0;paragraph.paragraph_format.left_indent=0;paragraph.paragraph_format.right_indent=0
     paragraph.alignment=WD_ALIGN_PARAGRAPH.LEFT if ci==0 and ri>0 else WD_ALIGN_PARAGRAPH.CENTER
 doc.save(out);assert digest(src)==old
 out.with_suffix('.revision.json').write_text(json.dumps(dict(input=str(src),input_sha256=old,output=str(out),changes=['Retain14B narrative and v9 unchanged','Add entire12project extension with historical overlap disclosure and all negative results','Paired project statistics and separate-cohort uncertainty figure','Updated cumulative budget and replay evidence']),indent=2));print(out)
if __name__=='__main__':main()
