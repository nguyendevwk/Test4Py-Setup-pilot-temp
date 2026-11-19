"""Build the research-depth v15 report from a preserved copy of v14."""
from __future__ import annotations
import copy,hashlib,json,re,shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from docx import Document
from docx.shared import Cm,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from polish_council_report import polish_tables
from revise_kaggle_groq_narrative import rebuild_lists

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v14.docx'
OUT=ROOT/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v15.docx'
CONTENT=ROOT/'research/editorial_v15/report_body.md'
ASSETS=OUT.parent/(OUT.stem+'_assets')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def num(x,d=2):
 if d==2 and x and abs(x)<.005:d=6
 return f'{x:.{d}f}'.replace('.',',')
def pvalue(v):return num(v,8 if 0<v<.00001 else 5)
def study(n):return load(ROOT/'research'/n/'summary.json')

CONTEXT='''Input: target f, module M, context budget B,
       dependency policy D, setup policy S
Output: bounded context C
1. Read the source of f and imports of M.
2. Initialize C with target source and imports.
3. If D is enabled:
   collect referenced declarations within its scope;
   add declarations while depth and size limits hold.
4. If S is enabled:
   inspect the callable signature;
   try setup arguments under the fixed probe policy;
   if the call completes, add signature and arguments.
5. Return C without probe return values as test oracles.'''
FEEDBACK='''Input: target f, context C, model L,
       repair limit R, evaluation policy Q
Output: test suite T and evaluation outcome E
1. Generate T from the task prompt and C.
2. For round r from 0 to R:
   extract a complete test module;
   check structure and execute tests on the real code;
   evaluate T under the fixed policy Q;
   record the outcome and the test version;
   if T is accepted, return T and its evidence;
   if r < R, revise T using execution diagnostics.
3. Return the unsuccessful outcome with its evidence.'''

def make_figures(cohorts,legacy,fullstat):
    ASSETS.mkdir(exist_ok=False)
    fig,ax=plt.subplots(figsize=(7,3.9));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
    boxes=[(.03,.70,.26,.18,'Mã nguồn và giao diện\nĐối tượng, import, khai báo'),(.37,.70,.26,.18,'Ngữ cảnh có giới hạn\nThiết lập đã thử nếu có'),(.71,.70,.26,.18,'Sinh kiểm thử\nYêu cầu hành vi cụ thể'),(.71,.30,.26,.18,'Thực thi và đánh giá\nKiểm tra, độ phủ, chạy lại'),(.37,.30,.26,.18,'Phản hồi sửa lỗi\nTheo ngân sách đã đặt'),(.03,.30,.26,.18,'Kết quả và bằng chứng\nGiữ cả lượt không đạt')]
    for i,(x,y,w,h,text) in enumerate(boxes):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.008',facecolor=['#E9F1F7','#E5F1EA','#E9EDF8','#E9EDF8','#FFF0DB','#E5F1EA'][i],edgecolor='#536D82'))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=8.5,linespacing=1.6)
    for a,b in [((.30,.79),(.36,.79)),((.64,.79),(.70,.79)),((.84,.69),(.84,.49)),((.70,.39),(.64,.39))]:
        ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='->',lw=1.3,color='#536D82'))
    ax.annotate('',xy=(.84,.70),xytext=(.50,.49),arrowprops=dict(arrowstyle='->',connectionstyle='angle,angleA=90,angleB=180,rad=6',color='#A06B30'))
    ax.plot([.84,.84,.16],[.30,.22,.22],color='#536D82',lw=1.1)
    ax.annotate('',xy=(.16,.30),xytext=(.16,.22),arrowprops=dict(arrowstyle='->',color='#536D82'))
    ax.text(.50,.16,'Ghi nhận khi đạt yêu cầu hoặc hết ngân sách sửa',fontsize=8,ha='center',color='#475569')
    ax.text(.50,.05,'Đánh giá thành phần: không sửa. Đánh giá quy trình: tối đa hai lần sửa.',fontsize=8,ha='center',color='#475569')
    fig.subplots_adjust(left=.01,right=.99,top=.98,bottom=.02);fig.savefig(ASSETS/'architecture.png',dpi=300,bbox_inches='tight');plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,3.2))
    names=['Ngữ cảnh kết hợp so với mã nguồn','Thiết lập so với mã nguồn','Khai báo phụ trợ bổ sung']
    for i,(name,c) in enumerate(fullstat['contrasts'].items()):
        e=c['difference']*100;lo,hi=[v*100 for v in c['percentile_95']]
        ax.errorbar(e,i,xerr=[[e-lo],[hi-e]],fmt='o',capsize=5,color=['#3E6585','#2F795B','#AD8337'][i]);ax.text(hi+.2,i,f'{e:+.2f}'.replace('.',','),va='center',fontsize=9)
    ax.axvline(0,ls='--',color='#777777');ax.set_yticks([0,1,2],names);ax.set_xlabel('Chênh lệch tỷ lệ đạt (điểm phần trăm)');ax.set_ylim(-.6,2.6);ax.grid(axis='x',alpha=.18);fig.tight_layout();fig.savefig(ASSETS/'effects.png',dpi=300);plt.close(fig)
    names=['Trước tinh chỉnh','Sau tinh chỉnh'];cols=['#3F6C8E','#5B9279','#DAAB4E','#BC7474'];series=[]
    for key in ['sota_original','sota_after_refinement']:
        s=legacy[key]['summary'];series.append([s['first_pass'],s['repairs_by_round']['1'],s['repairs_by_round']['2'],s['n']-s['passed']])
    fig,ax=plt.subplots(figsize=(6.8,3.1));left=[0,0]
    for i,label in enumerate(['Sinh đầu tiên','Sửa lần 1','Sửa lần 2','Chưa đạt']):
        values=[v[i] for v in series];ax.barh(names,values,left=left,color=cols[i],label=label,height=.42)
        for y,(start,v) in enumerate(zip(left,values)):
            if v:ax.text(start+v/2,y,str(v),ha='center',va='center',color='white' if i in [0,3] else '#263238',fontsize=10)
        left=[a+b for a,b in zip(left,values)]
    ax.set_xlim(0,105);ax.set_xlabel('Số lượt trong cùng quy mô 105');ax.legend(ncol=4,loc='lower center',bbox_to_anchor=(.5,1.03),fontsize=9,frameon=False);fig.tight_layout();fig.savefig(ASSETS/'repair.png',dpi=300);plt.close(fig)


def main():
    if OUT.exists():raise FileExistsError('Preserve existing versions; choose a new output.')
    input_hash=sha(SRC);original=Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx');original_hash=sha(original)
    old=Document(ROOT/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v11.docx');legacy=load(next((ROOT/'research/reviews/council_sota_20261118/restored').glob('*/summary.json')))['cohorts']
    ca=study('groq_confirmation_20261118');cb=study('groq_codamosa_extension_20261119')
    stats=[load(ROOT/'research'/n/'statistics.json') for n in ['groq_confirmation_20261118','groq_codamosa_extension_20261119']]
    assert [(ca['arms'][a]['passed'],cb['arms'][a]['passed']) for a in ['atomic_source','atomic_verified_setup']]==[(28,32),(36,34)]
    full=study('groq_full_scope_20261119');fullstat=load(ROOT/'research/groq_full_scope_20261119/statistics.json')
    assert full['completed']==full['planned']==3870 and fullstat['final']
    joint=load(ROOT/'research/groq_full_scope_20261119/joint_packs/main/summary.json');assert joint['complete']
    make_figures(stats,legacy,fullstat)
    projects=list(fullstat['contrasts']['context_setup-source']['project_differences'])
    values=[100*fullstat['contrasts']['context_setup-source']['project_differences'][p] for p in projects]
    fig,ax=plt.subplots(figsize=(7,5.6));ax.barh(projects,values,color=['#2F795B' if v>0 else '#AD694F' if v<0 else '#888888' for v in values]);ax.axvline(0,color='#666666',lw=.8);ax.invert_yaxis();ax.set_xlabel('Chênh lệch tỷ lệ đạt (điểm phần trăm)');ax.tick_params(axis='y',labelsize=8);ax.grid(axis='x',alpha=.15);fig.tight_layout();fig.savefig(ASSETS/'project_effects.png',dpi=300);plt.close(fig)
    body=CONTENT.read_text();used=sorted({int(x) for x in re.findall(r'\[(\d+)\]',body)});refs={}
    for p in old.paragraphs:
        match=re.match(r'^\[(\d+)\]\s',p.text)
        if match:refs[int(match.group(1))]=p.text
    refs[24]='[24] soarsmu, “BugsInPy: A Database of Existing Bugs in Python Programs to Enable Controlled Testing and Debugging Studies”, kho mã và hướng dẫn benchmark. https://github.com/soarsmu/BugsInPy. Truy cập ngày 19/11/2026.'
    ids={n:i+1 for i,n in enumerate(used)}
    def cite(text):return re.sub(r'\[(\d+)\]',lambda m:'['+str(ids[int(m.group(1))])+']',text)
    shutil.copy2(SRC,OUT);doc=Document(OUT)
    start=max(i for i,p in enumerate(doc.paragraphs) if p.text.strip()=='MỞ ĐẦU')
    first=doc.paragraphs[start]._p;container=doc._element.body;cut=False
    for element in list(container):
        if element is first:cut=True
        if cut and element.tag!=qn('w:sectPr'):container.remove(element)
    def para(text,style=None):
        p=doc.add_paragraph(cite(text),style)
        if not style:
            p.paragraph_format.keep_with_next=False
        return p
    def heading(text,level):
        p=para(text,'Heading '+str(level));p.paragraph_format.keep_with_next=True
        if level==1:p.paragraph_format.page_break_before=True
        return p
    def caption(text):
        p=para(text,'Caption');p.paragraph_format.keep_with_next=True;p.paragraph_format.first_line_indent=0;return p
    def table(rows,cap=None):
        if cap:caption(cap)
        t=doc.add_table(rows=0,cols=len(rows[0]));t.style='Table Grid'
        for row in rows:
            for c,value in zip(t.add_row().cells,row):c.text=str(value)
        return t
    code_tables=[];main_tables={}
    def code(text,cap=None):
        if cap:caption(cap)
        t=table([[text]]);code_tables.append(t);return t
    def figure(key,cap):
        p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.first_line_indent=0;p.paragraph_format.keep_with_next=True
        width=min(s.page_width-s.left_margin-s.right_margin for s in doc.sections);p.add_run().add_picture(str(ASSETS/(key+'.png')),width=width)
        caption(cap).paragraph_format.keep_with_next=False
    armnames={'source':'Chỉ mã nguồn','verified_setup':'Thêm thiết lập','context_setup':'Ngữ cảnh kết hợp'}
    primary=[['Nhánh','Đạt / lượt','Tỷ lệ theo lượt (%)','Tỷ lệ cân bằng dự án (%)','Độ phủ cân bằng dự án (%)']]
    for arm in ['source','verified_setup','context_setup']:
        a=fullstat['arms'][arm];primary.append([armnames[arm],f"{a['successes']}/{a['denominator']}",num(100*a['successes']/a['denominator']),num(100*a['equal_project_acceptance_rate']),num(a['equal_project_penalized_module_line_pct'])])
    costs=load(ROOT/'research/groq_full_scope_20261119/arm_cost_metrics.json')
    costtable=[['Nhánh','Token đầu vào','Token đầu ra','Ước tính (USD)','USD / bộ đạt']]
    for arm,record in costs.items():costtable.append([armnames[arm],str(record['prompt_tokens']),str(record['completion_tokens']),num(record['estimated_usd'],6),num(record['per_accepted_usd'],6) if record['per_accepted_usd'] is not None else 'Không áp dụng'])
    contrasts=[['Tương phản','Vai trò','Chênh lệch (điểm %)','Khoảng 95% (điểm %)','p','p hiệu chỉnh']]
    for name,c in fullstat['contrasts'].items():
        lo,hi=[v*100 for v in c['percentile_95']];label={'context_setup-source':'Ngữ cảnh kết hợp so với mã nguồn','verified_setup-source':'Thiết lập so với mã nguồn','context_setup-verified_setup':'Khai báo phụ trợ bổ sung'}[name]
        contrasts.append([label,'Chính' if c['role']=='primary' else 'Phụ',num(c['difference']*100),num(lo)+' đến '+num(hi),pvalue(c['exact_signflip_two_sided_p']),pvalue(c['holm_adjusted_p']) if 'holm_adjusted_p' in c else 'Không thuộc nhóm phụ'])
    development=[['Cấu hình','Đạt / lượt','Tỷ lệ đạt (%)','Độ phủ có tính lượt không đạt (%)']]
    for name,k in [('Cơ sở nội bộ','control_baseline'),('Council Standard','control_council_enhanced'),('Ngữ cảnh và phản hồi, trước tinh chỉnh','sota_original'),('Sau tinh chỉnh hai đối tượng','sota_after_refinement')]:
        s=legacy[k]['summary'];development.append([name,f"{s['passed']}/{s['n']}",num(s['pass_rate_pct']),num(s['coverage']['line_pct']['penalized_mean_pct'])])
    TABLES={
      'related':[['Hướng tiếp cận','Cơ chế trọng tâm','Liên hệ với đề tài'],['Pynguin [2]','Tìm kiếm đầu vào và chuỗi lời gọi','Cơ sở về khó khăn tạo dữ liệu cho Python'],['ChatUniTest [3]','Sinh, kiểm tra và sửa theo phản hồi','Cơ sở của vòng phản hồi thực thi'],['CoverUp [4]','Sinh kiểm thử Python có định hướng độ phủ','Cơ sở đánh giá mức bao quát'],['Test4Py [1]','Đồ thị gọi hàm, suy luận kiểu theo hành vi, sửa lặp','Phương pháp tham chiếu cho bài toán'],['Council','Ngữ cảnh có giới hạn, thiết lập đã thử, phản hồi hữu hạn','Hướng tiếp cận và thành phần được khảo sát']],
      'design':[['Nhóm bằng chứng','Phạm vi','Quy mô','Vai trò'],['Đánh giá toàn phạm vi','645 đối tượng /169 mô-đun / 21 dự án','3 nhánh; 2 lượt lặp; 3.870 lượt; không sửa','Đối chứng chính và tách thành phần'],['Đối chứng trước mở rộng','27 đối tượng/9 dự án và34 đối tượng/12 dự án','162 và204 lượt;giữ thiết kế riêng','Bối cảnh phát triển'],['Phát triển quy trình','21 đối tượng/8 dự án','105 lượt mỗi cấu hình;có sửa,tinh chỉnh','Phân tích phản hồi'],['Khảo sát bổ trợ','Các đối tượng đã quan sát','54,36,68 và108 lượt theo từng thiết kế','Lựa chọn cấu hình và vận hành'],['Thành phần 14B','12 đối tượng/4 dự án','72 lượt; không sửa','Bằng chứng thành phần14B'],['Ứng dụng 14B','genty','Bộ 12 và 14 ca;chạy lại,hai đột biến hậu kiểm','Tái sử dụng kiểm thử']],
      'primary':primary,'contrasts':contrasts,'development':development,
      'mechanisms':[['Khảo sát','Đối chứng','Bổ sung','Vai trò'],['Phụ thuộc mã nguồn, 54 lượt','Mã nguồn: 8/27','Phụ thuộc: 5/27','Khảo sát ban đầu, có sửa'],['Thiết lập, 36 lượt','Mã nguồn: 5/18','Thiết lập: 7/18','Cùng đối tượng đã quan sát; ba hàm kiểm thử'],['Khai báo phụ trợ, 68 lượt','Mã nguồn: 11/34','Ngữ cảnh và thiết lập: 12/34','Phát triển sau đánh giá mở rộng']],
      'application':[['Chỉ số','Bộ 12 ca','Bộ 14 ca'],['Chạy lại mới','12/12','14/14 trong cả ba tiến trình'],['Độ phủ dòng genty_args','18/20 (90%)','20/20 (100%)'],['Độ phủ nhánh genty_args','Không áp dụng (0/0)','Không áp dụng (0/0)'],['Độ phủ genty_repeat','8/8 dòng; 2/2 nhánh','8/8 dòng; 2/2 nhánh'],['Hai đột biến iterator hậu kiểm','0/2 phát hiện; 2/2 không phát hiện','2/2 phát hiện']],
      'efficiency':costtable,
      'conclusions':[['Câu hỏi','Bằng chứng trọng tâm','Phạm vi'],['RQ1: hiệu quả phương pháp',num(fullstat['contrasts']['context_setup-source']['difference']*100)+' điểm phần trăm theo dự án','Toàn 645 đối tượng;21 dự án đã quan sát'],['RQ2: đóng góp thành phần','Thiết lập và khai báo phụ trợ được tách bằng tương phản;phản hồi có bằng chứng phát triển','Hai tương phản phụ có hiệu chỉnh Holm'],['RQ3: chất lượng','Chạy lại độc lập và ứng dụng 14B trên genty','Chạy lại không chứng minh mọi oracle đúng'],['RQ4: khả thi','Chi phí theo dõi trong trần 3 USD;artifact14B tái dùng','Không so suy luận bằng thời gian chạy lại']]

    }
    from v15_research_tables import additional_tables
    TABLES.update(additional_tables(ROOT, num))
    # Markdown content is deliberately limited to paragraphs, numbered headings and explicit research objects.
    paragraphs=[];buffer=[]
    def flush():
        if buffer:paragraphs.append(' '.join(buffer));buffer.clear()
    for line in body.splitlines():
        if line.startswith(('# ','## ','### ','@')):
            flush();paragraphs.append(line)
        elif not line.strip():flush()
        else:buffer.append(line)
    flush()
    for block in paragraphs:
        block=block.strip()
        if not block:continue
        if block.startswith('# '):heading(block[2:],1)
        elif block.startswith('### '):heading(block[4:],3)
        elif block.startswith('## '):heading(block[3:],2)
        elif block.startswith('@'):
            kind,rest=block.split(' ',1);key,cap=[x.strip() for x in rest.split('|',1)]
            if kind=='@table':main_tables[key]=table(TABLES[key],cap)
            elif kind=='@figure':figure(key,cap)
            elif kind=='@algorithm':code(CONTEXT if key=='context' else FEEDBACK,cap)
            else:raise ValueError(kind)
        else:para(' '.join(block.splitlines()))
    heading('TÀI LIỆU THAM KHẢO',1)
    for n in used:
        p=doc.add_paragraph(re.sub(r'^\[\d+\]',f'[{ids[n]}]',refs[n]));p.paragraph_format.first_line_indent=0
    heading('PHỤ LỤC 1. LỜI NHẮC VÀ QUY ƯỚC THUẬT NGỮ',1)
    para('Lời nhắc dưới đây là nội dung hệ thống bằng tiếng Anh được lưu trong cấu hình đối chứng nhiều dự án. Đây là lời nhắc đã dùng, không phải bản dịch thay thế cho dữ liệu suy luận cũ. Ba hàm kiểm thử độc lập trong lời nhắc là yêu cầu tổ chức mã, không phải ba đơn vị thống kê độc lập.')
    prompt=load(ROOT/'research/groq_full_scope_20261119/manifest.json')['rules'];code(prompt,'Mẫu 1. Lời nhắc hệ thống trong đối chứng chuẩn hóa')
    code('Module {module_name} target {symbol_name}\n{imports_and_target_source}\n\nRuntime signature and successfully executed setup arguments\n(NOT expected results):\n{accepted_setup_signature_and_arguments}','Mẫu 2. Cấu trúc lời nhắc đối tượng, minh họa với chỗ điền dữ liệu')
    para('Phần thông tin thiết lập chỉ có trong nhánh bổ sung khi lời gọi thử hoàn tất. Mẫu 2 là cấu trúc có chỗ điền, không phải một câu trả lời hay kết quả thực thi cụ thể.')
    table([['Thuật ngữ','Cách dùng trong báo cáo'],['Target','Đối tượng kiểm thử: hàm hoặc lớp'],['Test suite','Bộ kiểm thử'],['Assertion','Điều kiện khẳng định'],['Test oracle','Cơ sở xác định kết quả mong đợi'],['Setup probe','Thực thi thử thiết lập'],['Repair','Sửa kiểm thử theo phản hồi'],['Replay','Chạy lại kiểm thử đã lưu'],['Cluster bootstrap','Lấy mẫu lại theo cụm dự án'],['Mutation testing','Kiểm thử đột biến']],'Bảng PL1. Quy ước thuật ngữ')
    heading('PHỤ LỤC 2. KẾT QUẢ CHI TIẾT THEO DỰ ÁN VÀ CẤU HÌNH',1)
    para('Phụ lục cung cấp phân bố kết quả để đối chiếu với các bảng tổng hợp. Các số lượt thuộc hai tập đánh giá được giữ riêng. Không cộng các lượt lặp hoặc các phiên bản tinh chỉnh thành số dự án độc lập.')
    rows=[['Dự án','Đối tượng','Mã nguồn đạt/lượt','Thiết lập đạt/lượt','Kết hợp đạt/lượt','Chênh lệch chính (điểm %)']]
    for project,rec in fullstat['per_project'].items():
        a=rec['arms'];cells=[f"{a[arm]['successes']}/{a[arm]['denominator']}" for arm in ['source','verified_setup','context_setup']]
        rows.append([project,str(rec['targets']),*cells,num(100*fullstat['contrasts']['context_setup-source']['project_differences'][project])])
    table(rows,'Bảng PL2. Phân bố đầy đủ kết quả của 21 dự án ở đợt toàn phạm vi')
    rows=[['Nhánh','Gói vượt qua /21','Ca đã thu thập','SC gói hợp lệ TB21 (%)']]
    for arm in ['source','verified_setup','context_setup']:
        rec=joint['arms'][arm];rows.append([armnames[arm],str(rec['packs_pass'])+'/21',str(rec['collected_nodes']),num(rec['equal_project_validated_pack_coverage_pct'])])
    table(rows,'Bảng PL3. Khả năng tích hợp và độ phủ của toàn bộ gói kiểm thử được nhận')
    para('Khảo sát gói là phân tích bổ sung về khả năng sử dụng. Mã của mọi bộ được nhận đều được đưa vào, không lọc ca thất bại hay sửa điều kiện khẳng định. Giá trị tổng hợp phạt gói không đạt bằng không; độ phủ đo thô của từng gói, lỗi thực thi và trường hợp không có dữ liệu được giữ riêng trong hồ sơ.')
    for index,st in enumerate(stats,1):
        rows=[['Dự án','Đối tượng','Mã nguồn đạt/lượt','Thiết lập đạt/lượt','Chênh lệch (điểm %)']]
        for project,r in st['per_project'].items():rows.append([project,str(r['targets']),f"{r['source_successes']}/{r['paired_attempts']}",f"{r['verified_successes']}/{r['paired_attempts']}",num(r['paired_difference']*100)])
        table(rows,f'Bảng PL{index+3}. Kết quả theo dự án của tập đánh giá {index}')
    rows=[['Cấu hình','Đạt/lượt','Tỷ lệ đạt (%)','Độ phủ (%)']]
    for title,key in [('Đầy đủ','ablation_full_method'),('Không tự động bổ sung lệnh nhập mô-đun','ablation_wo_auto_import'),('Không sửa lỗi','ablation_wo_critic'),('Không hướng dẫn giao diện','ablation_wo_grounding')]:
        s=legacy[key]['summary'];rows.append([title,f"{s['passed']}/{s['n']}",num(s['pass_rate_pct']),num(s['coverage']['line_pct']['penalized_mean_pct'])])
    table(rows,'Bảng PL6. Khảo sát loại bỏ thành phần trên sáu đối tượng phát triển')
    rows=[['Đối tượng phát triển','Cơ sở đạt/5','Standard đạt/5','Sau tinh chỉnh đạt/5','Độ phủ sau tinh chỉnh (%)']]
    for target,r in legacy['sota_after_refinement']['per_target'].items():rows.append([target,str(legacy['control_baseline']['per_target'][target]['passed']),str(legacy['control_council_enhanced']['per_target'][target]['passed']),str(r['passed']),num(r['coverage']['line_pct']['penalized_mean_pct'])])
    table(rows,'Bảng PL7. Phân bố kết quả trên 21 đối tượng phát triển')
    heading('PHỤ LỤC 3. PHẠM VI BẰNG CHỨNG VÀ TÁI LẬP',1)
    para('Các hồ sơ tái lập đi kèm lưu phiên bản môi trường, mã nguồn, lời nhắc, đầu ra mô hình và báo cáo thực thi. Danh mục chi tiết cùng mã kiểm tra toàn vẹn được cung cấp trong evidence_manifest_v15.json. Các đường dẫn tệp phục vụ truy vết được giới hạn ở phụ lục, không dùng thay cho mô tả phương pháp.')
    table([['Nguồn kết quả','Hồ sơ trong dự án'],['Đối chứng toàn phạm vi','research/groq_full_scope_20261119'],['Đối chứng 9 dự án','research/groq_confirmation_20261118'],['Đối chứng 12 dự án','research/groq_codamosa_extension_20261119'],['Khảo sát ngữ cảnh','research/groq_study_20261118_v2; groq_development_20261118; groq_context_development_20261119'],['Khảo sát token','research/groq_efficiency_20261119'],['Kết quả 14B và ứng dụng','research/kaggle_execution_evidence_20261119; research/14b_extended_replay_20261119'],['Số liệu phát triển','research/reviews/council_sota_20261118/restored'],['Hướng dẫn tái lập','research/REPRODUCIBILITY_GROQ.md']],'Bảng PL8. Danh mục nguồn dữ liệu và thực nghiệm')
    para('Ở tập phát triển, số bản đánh giá có thể đối chiếu lần lượt là 99/105 cho cấu hình cơ sở, 104/105 cho Standard, 103/105 cho cấu hình trước tinh chỉnh và 104/105 cho bảng sau tinh chỉnh. Một số trường hợp còn dựa trên bảng tổng hợp gốc. Các kết quả phát triển vì vậy được dùng để mô tả quá trình, không có cùng mức đầy đủ bằng chứng với hai đối chứng chuẩn hóa.')
    para('Bộ đột biến lịch sử có 187 trường hợp trên 21 bộ kiểm thử chuẩn tuyển chọn, gồm 19 bộ từ Standard và 2 bộ từ cấu hình cơ sở; nhãn lịch sử ghi 71 trường hợp thất bại trên phiên bản biến đổi. Cách phân loại cũ chưa đủ chi tiết để tách mọi lỗi khẳng định khỏi lỗi thực thi khác, và có một điều kiện khẳng định trong bộ tuyển chọn bị thay đổi theo hướng ít chặt chẽ hơn. Do đó tỷ lệ này không được sử dụng làm hiệu quả phát hiện lỗi của các bộ kiểm thử thuộc đối chứng chính.')
    para('Trong đợt 12 dự án, một câu trả lời có khối mã chưa đóng được giữ là lượt không đạt. Phân tích dùng phân loại lỗi định dạng được đối chiếu từ phản hồi gốc; giá trị chấp nhận và độ phủ không thay đổi. Việc chuẩn hóa quy ước kiểm tra mã nguồn do khác biệt xuống dòng cũng được ghi riêng. Các chi tiết này thuộc kiểm soát dữ liệu, không phải cơ chế tạo ra cải thiện nghiên cứu.')
    para('Khả năng tái lập đã kiểm tra gồm tính lại thống kê từ dữ liệu đã lưu, chạy lại các bộ kiểm thử được nhận và thử chạy sau khi di chuyển thư mục. Mô hình qua API được định danh bằng tên dịch vụ; đầu ra suy luận mới không được bảo đảm giống từng byte. Ngân sách được theo dõi theo request và usage ước tính, không thay thế hóa đơn nhà cung cấp.')
    heading('PHỤ LỤC 4. KHẢO SÁT PHÁT TRIỂN VÀ PHÂN TÍCH HẬU KIỂM',1)
    para('Phụ lục giữ toàn bộ các khảo sát phát triển đã rút gọn khỏi phần thân. Kết quả thuận lợi và bất lợi được giữ cùng nhau; các thiết kế không được cộng gộp vào đối chứng chính. Phân tích phân nhóm sau đợt lớn có tính thăm dò, không thay đổi kế hoạch kiểm định đã khóa.')
    hist=(ROOT/'research/editorial_v15/historical_appendix.md').read_text()
    for i,line in enumerate(hist.splitlines()):
        if not line.strip():continue
        if line.startswith('@table development'):table(TABLES['development'],'Bảng PL9. Kết quả phát triển quy trình trước và sau tinh chỉnh')
        elif line.startswith('@table mechanisms'):table(TABLES['mechanisms'],'Bảng PL10. Toàn bộ khảo sát lựa chọn cấu hình ngữ cảnh')
        elif line.startswith('@figure repair'):figure('repair','Hình PL1. Kết quả theo vòng sửa lỗi trong giai đoạn phát triển')
        elif line.startswith('#'):para(line.lstrip('# ').strip())
        elif not line.startswith('@'):para(line.replace('Bảng 4.3','Bảng PL9').replace('Bảng 4.4','Bảng PL10'))
    extra=additional_tables(ROOT,num)
    table(extra['subgroups'],'Bảng PL11. Toàn bộ phân nhóm mô tả theo thuộc tính nguồn mã và thiết lập')
    para('Phân nhóm được xác định từ thuộc tính nguồn đã lưu, nhưng phân tích hiệu quả theo nhóm được bổ sung sau thực nghiệm. Mỗi hàng giữ mọi lượt của nhóm; số dự án hiện diện khác nhau giữa các hàng. Không dùng bảng để lựa chọn lại mẫu hoặc tuyên bố tương tác nhân quả.')
    table(extra['versions'],'Bảng PL12. Phiên bản 21 gói sản phẩm và quy mô đối tượng')
    table(extra['nf4_settings'],'Bảng PL13. Cấu hình đã lưu của lượt khảo sát genty trên Kaggle 14B NF4')
    para('Cấu hình ở Bảng PL13 áp dụng cho lượt genty có hồ sơ worker-settings được dẫn trong danh mục bằng chứng. Không gán các tham số này cho mọi thực nghiệm 14B hoặc cho đợt GPT-OSS-20B. Thư viện suy luận, trình điều khiển và toàn bộ môi trường Kaggle chưa được tóm tắt đầy đủ trong bảng; thông tin không có bằng chứng riêng không được điền suy đoán.')
    # First table is the front-matter glossary inherited from v11; replace terms to match revised text.
    front=doc.tables[0]
    glossary=[['Ký hiệu','Ý nghĩa','Cách sử dụng'],['LLM','Large Language Model','Mô hình ngôn ngữ lớn'],['AST','Abstract Syntax Tree','Cây cú pháp trừu tượng'],['API','Application Programming Interface','Giao diện lập trình ứng dụng'],['NF4','NormalFloat 4-bit','Định dạng lượng tử hóa dùng ở giai đoạn 14B'],['PR','Pass rate','Tỷ lệ đạt yêu cầu theo tiêu chí của từng đợt'],['SC','Statement coverage','Độ phủ câu lệnh mô-đun'],['BC','Branch coverage','Độ phủ nhánh'],['RQ','Research question','Câu hỏi nghiên cứu']]
    # Remove obsolete glossary rows and refill using the same table object.
    for row in list(front.rows):front._tbl.remove(row._tr)
    for row in glossary:
        for c,text in zip(front.add_row().cells,row):c.text=text
    # Table presentation follows the existing page template, with zero paragraph indents in cells.
    polish_tables(doc)
    for t in doc.tables:
        for ri,row in enumerate(t.rows):
            for ci,c in enumerate(row.cells):
                for p in c.paragraphs:
                    p.paragraph_format.first_line_indent=0;p.paragraph_format.left_indent=0;p.paragraph_format.right_indent=0
                    p.alignment=WD_ALIGN_PARAGRAPH.LEFT if ci==0 and ri>0 else WD_ALIGN_PARAGRAPH.CENTER
    t=main_tables['primary'];available=doc.sections[0].page_width-doc.sections[0].left_margin-doc.sections[0].right_margin
    widths=[int(available*r) for r in [.28,.16,.18,.19,.19]]
    for column,width in zip(t.columns,widths):column.width=width
    for row in t.rows:
        for c,width in zip(row.cells,widths):c.width=width
    for grid,width in zip(t._tbl.tblGrid.gridCol_lst,widths):grid.set(qn('w:w'),str(int(width/635)))
    for t in code_tables:
        for p in t.cell(0,0).paragraphs:
            p.alignment=WD_ALIGN_PARAGRAPH.LEFT;p.paragraph_format.line_spacing=1.05
            for run in p.runs:run.font.name='Consolas';run.font.size=Pt(9);run.font.bold=False
    rebuild_lists(doc)
    for p in doc.paragraphs:
        if p.style.name=='Caption' and p.text.startswith(('Bảng','Thuật toán','Mẫu')):p.paragraph_format.keep_with_next=True
    doc.save(OUT)
    assert sha(SRC)==input_hash and sha(original)==original_hash
    inputs=[CONTENT,ROOT/'research/editorial_v15/full_benchmark_scope.json',ROOT/'research/editorial_v15/historical_appendix.md',ROOT/'research/editorial_v15/deep_analysis.json',ROOT/'research/groq_full_scope_20261119/environment_validation.json',ROOT/'research/groq_full_scope_20261119/external_project_origins.json',ROOT/'research/kaggle_execution_evidence_20261119/cold/small/genty-42-improved/worker-settings.json',ROOT/'scripts/v15_research_tables.py',ROOT/'scripts/analyze_v15_descriptive.py',ROOT/'research/groq_full_scope_20261119/dataset_description.json',ROOT/'research/groq_full_scope_20261119/arm_cost_metrics.json',ROOT/'research/groq_full_scope_20261119/joint_packs/main/summary.json']
    replay_report=load(ROOT/'research/editorial_v15/full_benchmark_scope.json')['independent_replay_report'];inputs.append(ROOT/replay_report)
    for name in ['groq_full_scope_20261119','groq_confirmation_20261118','groq_codamosa_extension_20261119','groq_context_development_20261119','groq_efficiency_20261119','14b_extended_replay_20261119']:
        for filename in ['manifest.json','summary.json','statistics.json','budget.json','independent_replay_summary.json']:
            p=ROOT/'research'/name/filename
            if p.exists():inputs.append(p)
    (ROOT/'research/editorial_v15/evidence_manifest_v15.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in inputs},indent=2))
    OUT.with_suffix('.revision.json').write_text(json.dumps(dict(input=str(SRC.relative_to(ROOT)),input_sha256=input_hash,output=str(OUT.relative_to(ROOT)),original_unchanged=True,input_unchanged=True,focus='Research problem, methodological mechanisms, matched evaluation and bounded conclusions; additional exploratory descriptive analyses on complete frozen outcomes; no new inference or model calls',main_chapter4_sections=7,prompts='English, copied from executed manifest; placeholders explicitly marked',references_renumbering=ids,changes=['Full3870case three-arm evaluation is now the central research evidence','Replaced implementation walkthrough with research-level algorithms','Unified experiments by research question; kept protocols separate','Preserved genuine14B work and bounded application benefit','Moved implementation and integrity details to appendix','Report complete645target,169module,21project assessment with prelocked primary and Holm-adjusted secondary comparisons']),ensure_ascii=False,indent=2))
    print(OUT)

if __name__=='__main__':main()
