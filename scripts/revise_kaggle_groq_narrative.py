"""New DOCX copy: preserve the real Kaggle execution and explain backend migration."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

from polish_council_report import polish_tables

ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_budget(doc):
    b=json.loads((ROOT/'research/groq_efficiency_20261119/budget.json').read_text())
    for p in doc.paragraphs:
        if p.text.startswith('Ngân sách toàn chiến dịch được giới hạn'):
            p.text=(f"Ngân sách toàn chiến dịch được giới hạn 3 USD. Đến hết screen bổ sung, sổ request ghi {b['settled_responses']} response có usage, {b['prompt_tokens']:,} input token và {b['completion_tokens']:,} output token; ước tính theo đơn giá đã ghi là {float(b['settled_api_estimate_usd']):.6f} USD. Tổng phân bổ bảo thủ {b['accounted_total_usd']:.6f} USD gồm cả khoản đặt trước chưa quyết toán và đối soát mốc 0,50 USD do người vận hành cung cấp; đây không phải hai hóa đơn để cộng với nhau. Riêng screen 108 lượt bổ sung có ước tính usage {float(b['efficiency_estimate_usd']):.6f} USD. Nguồn cập nhật: research/groq_efficiency_20261119/budget.json; chưa có hóa đơn nhà cung cấp để khẳng định số thực trả.")
            break


def before(anchor,text,style=None):
    node=OxmlElement('w:p');anchor._p.addprevious(node);p=Paragraph(node,anchor._parent)
    if style:p.style=style
    p.add_run(text);return p


def table_before(doc,anchor,rows):
    t=doc.add_table(rows=1,cols=len(rows[0]))
    for c,value in zip(t.rows[0].cells,rows[0]):c.text=value
    for row in rows[1:]:
        for c,value in zip(t.add_row().cells,row):c.text=value
    anchor._p.addprevious(t._tbl);return t


def timeline(path):
    fig,ax=plt.subplots(figsize=(6,4.4));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    stages=[('14B NF4 / Kaggle: đã thực thi',
        'Qwen2.5-Coder-14B trên từng T4; stress 4K sau adapter: 4/4 qua.'),
        ('Cold run: giới hạn thời gian thực nghiệm',
        '95 calls khởi tạo/worker; sinh đầu tiên sau ~43m47; timeout ~3.587 s.'),
        ('Warm-prefix: có kết quả đo được',
        '4 module-trials hoàn tất; baseline 20 node pass; nhánh cải tiến bị gate loại.'),
        ('Groq / GPT-OSS-20B: tiếp tục nghiên cứu',
        'Đổi backend + model để bảo đảm tiến độ; khảo sát hướng ngữ cảnh/setup gọn.')]
    for i,(title,body) in enumerate(stages):
        y=.94-i*.24
        ax.add_patch(FancyBboxPatch((.025,y-.16),.95,.16,boxstyle='round,pad=.012',facecolor=['#E9F1F7','#FFF1DF','#E8F3EE','#ECEDF8'][i],edgecolor='#547286'))
        ax.text(.055,y-.035,title,fontsize=10,fontweight='bold',va='top')
        ax.text(.055,y-.10,body,fontsize=8.8,va='top',wrap=True)
        if i<3:ax.annotate('',xy=(.5,y-.228),xytext=(.5,y-.172),arrowprops={'arrowstyle':'->','color':'#547286'})
    fig.subplots_adjust(left=.01,right=.99,top=.99,bottom=.02);fig.savefig(path,dpi=300,bbox_inches='tight');plt.close(fig)


def rebuild_lists(doc):
    ps=list(doc.paragraphs);body=max(i for i,p in enumerate(ps) if p.text.strip()=='MỞ ĐẦU')
    start=next(i for i,p in enumerate(ps) if p.text.strip()=='MỤC LỤC')
    end=max(i for i,p in enumerate(ps[:body]) if p.text.strip()=='DANH MỤC BẢNG')
    heads=[]
    for p in ps[body:]:
        s=p.text.strip()
        if s in {'MỞ ĐẦU','TÀI LIỆU THAM KHẢO'} or re.match(r'^(CHƯƠNG \d+\.|\d+\.\d+(?:\.\d+)?\.\s|PHỤ LỤC)',s):
            if s not in heads:heads.append(s)
    for p in ps[start+1:end]:p._p.getparent().remove(p._p)
    anchor=ps[start]
    for s in heads:
        node=OxmlElement('w:p');anchor._p.addnext(node);p=Paragraph(node,anchor._parent);p.style='CouncilTOC';p.add_run(s+'\t—');anchor=p
    for title,nxt,prefix in [('DANH MỤC BẢNG','DANH MỤC HÌNH','Bảng'),('DANH MỤC HÌNH','DANH MỤC TỪ VIẾT TẮT','Hình')]:
        ps=list(doc.paragraphs);body=max(i for i,p in enumerate(ps) if p.text.strip()=='MỞ ĐẦU')
        a=max(i for i,p in enumerate(ps[:body]) if p.text.strip()==title);b=max(i for i,p in enumerate(ps[:body]) if p.text.strip()==nxt)
        captions=list(dict.fromkeys(p.text.strip() for p in ps[body:] if re.match(r'^'+prefix+r' \d+\.\d+\.',p.text.strip())))
        for p in ps[a+1:b]:p._p.getparent().remove(p._p)
        anchor=ps[a]
        for s in captions:
            node=OxmlElement('w:p');anchor._p.addnext(node);p=Paragraph(node,anchor._parent);p.style='CouncilTOC';p.add_run(s+'\t—');anchor=p


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists() or a.input.resolve()==a.output.resolve():raise ValueError('New output required')
    efficiency_path=ROOT/'research/groq_efficiency_20261119/summary.json';eff=json.loads(efficiency_path.read_text())
    if eff['completed']!=eff['planned']:raise RuntimeError('Wait for complete efficiency screen')
    original=Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx');old=sha(original);input_hash=sha(a.input)
    shutil.copy2(a.input,a.output);doc=Document(a.output)
    def mainp(prefix):return next(p for p in doc.paragraphs if p.style.name!='CouncilTOC' and p.text.startswith(prefix))
    replacements={
      '1.3. Vấn đề ngữ cảnh mã nguồn':'1.3. Triển khai 14B NF4 trên Kaggle và chuyển hạ tầng sang Groq',
      'Các thử nghiệm tiền trạm được giữ thành các nhánh độc lập:':'Dự án đã triển khai và thực thi Qwen2.5-Coder-14B-Instruct lượng tử hóa NF4 trên Kaggle Dual T4, gồm pipeline upstream, kiểm tra bộ nhớ, chạy cold-start, thử lại warm-prefix và đánh giá thành phần source/API facts. Đây là giai đoạn thực nghiệm có log và artifact, không phải cấu hình mới đề xuất hoặc chưa chạy. Khi chi phí khởi tạo và giới hạn phiên GPU cản trở tiến độ thu thập số liệu, nhóm chuyển backend suy luận sang Groq API với openai/gpt-oss-20b để tiếp tục cùng bài toán sinh/sửa kiểm thử.',
      'Nhật ký upstream cục bộ ghi 95 lượt chuẩn bị':'Ở lượt cold-start, mỗi worker xử lý 95 calls khởi tạo. Sự kiện sinh kiểm thử đầu tiên xuất hiện khoảng 2.627 giây (43 phút 47 giây); hai worker chạm deadline được đặt cho lượt thử ở khoảng 3.587 giây. Cả bốn module-trials chưa hoàn tất scoring nên coverage và chênh lệch hiệu quả giữ NA. Đây là giới hạn ngân sách thực thi trong môi trường Kaggle đã dùng, không phải tỷ lệ chất lượng bằng 0 hoặc khẳng định Kaggle luôn giới hạn mọi job ở 60 phút.',
      'Nhật ký VRAM/timeout của mô hình 14B':'OOM tại ngữ cảnh 4K được ghi ở runtime ban đầu. Sau khi thay adapter attention, bốn stress test 4.096 input + 512 output token (hai lần trên từng GPU) đều qua; peak reserved khoảng 10,76 GiB và conservative headroom khoảng 3,67 GiB. Hai T4 phục vụ các worker riêng, không ghép thành một vùng VRAM 32 GB. Stress pass chỉ hỗ trợ cấu hình đã đo; không bảo đảm mọi prompt thực đều vừa bộ nhớ.',
      'Kết quả giai đoạn phát triển báo riêng các cohort':'Nghiên cứu được triển khai theo tiến trình: (i) thực thi 14B NF4 trên Kaggle để đánh giá tính khả thi và pipeline upstream; (ii) chuyển sang Groq/GPT-OSS-20B để thu thập dữ liệu nhanh hơn trong giới hạn tiến độ; (iii) chuẩn hóa bằng chứng và đánh giá các thành phần ngữ cảnh/setup trên các project bổ sung. Bảng phát triển có 21 target, năm lượt gắn nhãn 42–46 và refinement trên hai target; seed legacy chưa được truyền vào API. Các cohort có model/runtime/protocol khác nhau được giữ riêng, dù cùng thuộc tiến trình của dự án.'}
    for prefix,new in replacements.items():mainp(prefix).text=new
    oldcaption=mainp('Bảng 1.1.')
    oldcaption.text='Bảng 1.1. Tiến trình thực thi dự án và chuyển đổi hạ tầng'
    old_table=oldcaption._p.getnext()
    while old_table is not None and not old_table.tag.endswith('}tbl'):old_table=old_table.getnext()
    if old_table is not None:old_table.getparent().remove(old_table)
    anchor=mainp('1.4.')
    warm=before(anchor,'Lượt warm-prefix tiếp theo đã hoàn tất bốn module-trials trong khoảng 2.053 giây wall time của launcher. Baseline giữ ba file/20 node pass, có replay ổn định; nhánh cải tiến không được credit test tự động do extraction và cổng bảo toàn assertion. Không đổi kết quả này thành thành công của cải tiến. Từ baseline, 12 node được tuyển chọn không sửa mã để làm gói ứng dụng; ba replay Kaggle đều pass 12/12. Giai đoạn Kaggle vì vậy vừa cho thấy giới hạn hạ tầng, vừa tạo ra kiểm thử thực có thể tái sử dụng.')
    cold=mainp('Ở lượt cold-start');memory=mainp('OOM tại ngữ cảnh');cold._p.addprevious(memory._p);cold._p.addnext(warm._p)
    rows=[['Giai đoạn','Cấu hình và bằng chứng','Kết quả/giới hạn'],
      ['Kaggle: bộ nhớ','14B NF4; 2 T4; adapter attention','4/4 stress 4K+512 qua; không là efficacy'],
      ['Kaggle: cold-start','95 calls init/worker; first generation ~2.627 s','Timeout ~3.587 s; 4 module-trials chưa chấm xong; NA'],
      ['Kaggle: warm-prefix','95 prefix đã xác minh được reuse; launcher ~2.053 s','Baseline 20 node pass; cải tiến 0 node được credit theo gate'],
      ['Gói ứng dụng 14B','12 node baseline không sửa đổi; source/test hashes khóa','3 replay cũ 12/12; phạm vi ứng dụng tuyển chọn'],
      ['Chuyển Groq','GPT-OSS-20B API thay backend/model vì tiến độ và tài nguyên','Tiếp tục khảo sát nguồn/setup gọn; không là đối chứng chéo model']]
    history_table=table_before(doc,anchor,rows)
    history_table._tbl.addprevious(oldcaption._p)
    assets=a.output.parent/(a.output.stem+'_assets');assets.mkdir(exist_ok=False);figure=assets/'research_timeline.png';timeline(figure)
    pp=before(anchor,'');pp.alignment=WD_ALIGN_PARAGRAPH.CENTER;pp.paragraph_format.first_line_indent=0
    usable=min(s.page_width-s.left_margin-s.right_margin for s in doc.sections);pp.add_run().add_picture(str(figure),width=usable)
    before(anchor,'Hình 1.1. Lộ trình thực nghiệm đã thực thi: từ 14B NF4/Kaggle đến Groq/GPT-OSS-20B; không biểu diễn so sánh chất lượng chéo model.','Caption')
    before(anchor,'Nguồn lịch sử: UPSTREAM_14B_SMALL_TIMEOUT_20261116.md, NF4_SMALL_REMOTE_20261117.md và các audit JSON tương ứng. Chuyển backend kèm đổi model là thay đổi điều kiện thực nghiệm; không quy mức tăng Groq cho riêng AST hoặc khẳng định GPT-OSS-20B tốt hơn 14B từ các cohort này.')
    ch4=mainp('CHƯƠNG 4.')
    before(ch4,'3.7. Hướng đề xuất so với Test4Py gốc và vai trò của backend','Heading 2')
    before(ch4,'Test4Py gốc kết hợp đồ thị gọi hàm, suy luận kiểu dựa trên hành vi và sinh/sửa lặp theo coverage [1]. Dự án đã thực thi nhánh bám pipeline đó bằng 14B NF4 để khảo sát giới hạn thực tế. Hướng Council về sau tập trung vào ngữ cảnh source/import có giới hạn, thiết lập receiver/trạng thái, phản hồi pytest và kiểm soát nhận kiểm thử trong ngân sách nhỏ. Đổi sang Groq là giải pháp triển khai, không tự tạo đóng góp phương pháp.')
    before(ch4,'Bảng 3.5. Phân biệt pipeline gốc, hướng triển khai Kaggle và hướng đề xuất gọn','Caption')
    table_before(doc,ch4,[['Khía cạnh','Test4Py gốc / nhánh bám upstream','Hướng Council/Groq đang khảo sát'],
      ['Chuẩn bị ngữ cảnh','Call graph, tóm tắt, suy luận kiểu/hành vi và truy xuất','Source/import qua AST; curated hints ở giai đoạn đầu; probe signature/setup chung ở bản đánh giá mới'],
      ['Thiết lập trạng thái','Thành phần xây input trong pipeline upstream','Cung cấp setup đã thực thi qua probe; không bảo đảm tiền điều kiện mọi method'],
      ['Vòng lặp','Generation/repair và phản hồi coverage trong full pipeline','Hai lượt repair ở bản phát triển; zero-repair ở đối chứng thành phần mới'],
      ['Hạ tầng đã chạy','14B NF4/Kaggle cho nhánh triển khai upstream của dự án','Groq/GPT-OSS-20B cho giai đoạn thu thập bổ sung'],
      ['Tuyên bố hợp lệ','Đối chiếu full pipeline chỉ khi có matched control','Kết quả hiện tại là đánh giá thành phần; chưa chứng minh vượt full Test4Py']])
    before(ch4,'Tri thức thủ công, probe thực thi và trích dependency là các can thiệp khác nhau nên phải ghi rõ trong từng cohort. Hướng đề xuất khác phạm vi full Test4Py; dùng chung benchmark frame không đồng nghĩa tái lập nguyên paper. Các kết quả âm của Kaggle và Groq được giữ để giải thích quyết định thiết kế, không bị loại khỏi lịch sử nghiên cứu.')
    replay=json.loads((ROOT/'research/14b_application_replay_20261119/summary.json').read_text())
    ch5=mainp('CHƯƠNG 5.')
    before(ch5,'4.11. Screen tối ưu vận hành và tái sử dụng kiểm thử 14B','Heading 2')
    before(ch5,'Để kiểm tra lựa chọn output budget gọn, screen khóa 27 target đã quan sát, hai nhánh ngữ cảnh và hai output cap 1.536/2.048, cùng yêu cầu đúng ba hàm test và seed API best effort 45. Tổng 108 lượt, không repair; thứ tự cap/nhánh được luân phiên. Đây là screen vận hành trên tập đã quan sát, không phải cohort xác nhận độc lập hoặc căn cứ tăng cỡ mẫu suy luận.')
    before(ch5,'Bảng 4.17. Đánh đổi output cap trên cùng tập target và cùng tiêu chí chấm','Caption')
    rows=[['Nhánh / cap','Đạt / 27','SC penalty (%)','Output token TB','Giây/lượt TB']]
    for _,g in sorted(eff['groups'].items()):
        rows.append([g['arm'].replace('atomic_','')+' / '+str(g['output_cap']),str(g['passed'])+'/27',f"{g['module_line_penalized']:.2f}",f"{g['completion_tokens']/g['planned']:.1f}",f"{g['total_seconds']/g['planned']:.3f}"])
    table_before(doc,ch5,rows)
    before(ch5,'Thời gian/lượt gồm pacing/network, API và pytest/replay; không phải latency kernel thuần. Token và finish_reason được ghi cho mọi request. Chọn cap cần xét đồng thời tỷ lệ đạt, coverage và output-limit; không coi cap thấp hoặc pass cao hơn trong một lượt là chứng minh chất lượng oracle. Source/model/backend của screen giữ nguyên nên không dùng nó để suy tốc độ 14B so với 20B.')
    aggregate={cap:{'passed':sum(g['passed'] for g in eff['groups'].values() if g['output_cap']==cap),'tokens':sum(g['completion_tokens'] for g in eff['groups'].values() if g['output_cap']==cap),'limit':sum(g['output_limit_responses'] for g in eff['groups'].values() if g['output_cap']==cap)} for cap in [1536,2048]}
    before(ch5,f"Ở screen này, cap 1.536 đạt {aggregate[1536]['passed']}/54 và dùng {aggregate[1536]['tokens']:,} output token; cap 2.048 đạt {aggregate[2048]['passed']}/54 và dùng {aggregate[2048]['tokens']:,} output token. Không response nào chạm output limit. Vì mô hình đã thường dừng trước cả hai cap, dữ liệu không ủng hộ tự động hạ cap để tiết kiệm. Giữ 2.048 làm cấu hình vận hành có dư địa, không diễn giải chênh lệch một lượt là lợi ích nhân quả. Nhánh setup cũng không thắng đều trong lượt seed 45 này; kết quả cho thấy độ nhạy theo lần sinh và phải giữ cùng kết quả có mức tăng trước đó.")
    seconds=[r['seconds'] for r in replay['replays']]
    before(ch5,'Bổ sung khả năng tái dùng: hai file kiểm thử thật do nhánh baseline 14B NF4 sinh trước đây được replay CPU trong ba process mới, giữ nguyên test bytes và kiểm tra sáu source hashes genty. Cả ba lần đều pass 12/12, node sets giống nhau; thời gian mới lần lượt '+', '.join(f'{x:.3f}' for x in seconds)+' giây. Đây là chạy lại artifact sinh trước đó, không phải ba lần sinh mô hình mới hoặc tốc độ inference 14B.')
    before(ch5,'Nguồn bổ sung: research/groq_efficiency_20261119/summary.json và research/14b_application_replay_20261119/summary.json. Các artifact gốc Kaggle, số liệu Groq và replay CPU được phân biệt theo nguồn, runtime và mẫu số.')
    conclusion=mainp('Đánh giá mở rộng hoàn tất')
    conclusion.text+=' Chuỗi 14B NF4/Kaggle đã được thực thi và tạo artifact tái dùng; việc chuyển gấp sang Groq phục vụ tiến độ và hạn chế tài nguyên, không phủ nhận giai đoạn này. Screen output-cap bổ sung không cho thấy lý do hạ mặc định từ 2.048 xuống 1.536; kết quả setup biến thiên theo lượt sinh, vì vậy kết luận cải thiện vẫn giới hạn theo cohort và khoảng bất định.'
    appendix=next(p for p in doc.paragraphs if p.text.startswith('PHỤ LỤC. NGUỒN DỮ LIỆU'))
    for name in ['research/artifacts/nf4_14b_efficient_attention_pass.json','research/artifacts/nf4_14b_warm_small_audit_20261117.json','research/analysis/UPSTREAM_14B_SMALL_TIMEOUT_20261116.md','research/analysis/NF4_SMALL_REMOTE_20261117.md','research/groq_efficiency_20261119/summary.json','research/14b_application_replay_20261119/summary.json']:
        before(appendix,name+' — SHA256 '+sha(ROOT/name))
    refresh_budget(doc);polish_tables(doc);rebuild_lists(doc);doc.save(a.output)
    if sha(a.input)!=input_hash or sha(original)!=old:raise RuntimeError('Protected input changed')
    a.output.with_suffix('.revision.json').write_text(json.dumps({'input':str(a.input),'input_sha256':input_hash,'output':str(a.output),'output_sha256_before_navigation':sha(a.output),'original_unchanged':True,'changes':['Explicit real14B execution timeline, cold/warm distinction and useful retained tests','Explained emergency backend/model migration as practical continuation, not invalidating earlier work','Compared methodological direction with full Test4Py, without paper superiority claim','Added complete108attempt cap screen and3fresh CPU application replays']},indent=2))
    print(a.output)


if __name__=='__main__':main()
