#!/usr/bin/env python3
"""Polish a corrected Council report into a NEW document, never edit its input.

uv run --no-project --with python-docx --with matplotlib scripts/polish_council_report.py \
  --input reports/Tieu_Luan_CNPMTT_Council_SOTA_v2.docx \
  --output reports/Tieu_Luan_CNPMTT_Council_SOTA_v3.docx \
  --confirmation research/groq_confirmation_20261118/summary.json

Only supplied/restored evidence feeds charts. Partial confirmation counts are not
shown as efficacy. Creates chart PNGs and an accountable polish log next to output.
No API calls or changes to experimental data, the builder, or older reports.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
# Keep package caches out of protected home/config folders.
os.environ.setdefault('MPLCONFIGDIR', '/tmp/council-polish-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph

BLUE='#245A81'; TEAL='#278478'; ORANGE='#C77732'; GREY='#78828D'
COLORS=[BLUE,TEAL,ORANGE]
CAPTIONS={
 '4.1':'Hình 4.1. Tỷ lệ suite pass trên tập phát triển tuyển chọn: baseline, Standard và sau tinh chỉnh (105 lượt/nhánh).',
 '4.2':'Hình 4.2. Độ phủ câu lệnh mô-đun theo target: baseline và sau tinh chỉnh; failure được tính penalty bằng 0.',
 '4.3':'Hình 4.3. Phân bổ 28 lượt repair thành công sau tinh chỉnh: 22 ở vòng 1 và 6 ở vòng 2.',
 '4.4':'Hình 4.4. Mutation screen mới trên tập node phục hồi được chọn: 18 lượt mutant/nhánh, gồm cả inconclusive.',
 '4.5':'Hình 4.5. Hai target phát triển trước và sau tinh chỉnh: suite pass và độ phủ mô-đun có penalty.',
 '4.6':'Hình 4.6. Thời gian xử lý trung bình theo CSV của ba cohort phát triển ban đầu; không phải thời gian inference riêng.',
 '4.7':'Hình 4.7. Kết quả đánh giá mở rộng sau khóa cấu hình; mẫu số kế hoạch và số hoàn tất theo summary đầy đủ.',
}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot(path):
    data=path.read_bytes()
    return json.loads(data), {'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
def number(x,places=2): return f'{x:.{places}f}'.replace('.',',')
def remove(p):
    e=p._element;e.getparent().remove(e)
def write(p,text):
    # python-docx paragraph.text discards runs; explicitly preserve paragraph and first run style.
    rp=copy.deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
    p.clear();r=p.add_run(text)
    if rp is not None:r._r.insert(0,rp)
def before(p,text='',style=None):
    node=OxmlElement('w:p');p._p.addprevious(node)
    out=Paragraph(node,p._parent)
    if style:out.style=style
    if text:out.add_run(text)
    return out

def setting():
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
        'axes.spines.right':False,'axes.titleweight':'bold','axes.titlesize':11,
        'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9,
        'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})
def save(fig,path,footnote):
    fig.text(.02,.015,footnote,ha='left',va='bottom',fontsize=8,color='#404852',wrap=True)
    fig.tight_layout(rect=(0,.09,1,.98))
    fig.savefig(path,dpi=220,bbox_inches='tight');plt.close(fig)

def make_charts(evidence, mutation, output_dir):
    c=evidence['cohorts'];paths={};chart_data={}
    def emit(key,fig,data,note):
        path=output_dir/f'figure_{key.replace(".","_")}.png';save(fig,path,note);paths[key]=path;chart_data[key]=data
    keys=['control_baseline','control_council_enhanced','sota_after_refinement']
    labels=['Baseline','Council Standard','Sau tinh chỉnh']
    ss=[c[k]['summary'] for k in keys]
    for s in ss:
        if not (s['n']>0 and 0<=s['passed']<=s['n']):raise ValueError('Invalid development denominator')
    rates=[100*s['passed']/s['n'] for s in ss]
    fig,ax=plt.subplots(figsize=(7,3.5));bars=ax.bar(labels,rates,color=COLORS,width=.58)
    ax.set(ylabel='Suite pass (%)',ylim=(0,110),title='Tập phát triển tuyển chọn — ba nhánh nội bộ')
    ax.set_yticks(range(0,101,20));ax.yaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    for b,s,v in zip(bars,ss,rates):ax.text(b.get_x()+b.get_width()/2,v+2,f"{s['passed']}/{s['n']}\n{number(v)}%",ha='center',fontsize=10)
    emit('4.1',fig,dict(zip(keys,[{'n':s['n'],'passed':s['passed']} for s in ss])),
         'Sau tinh chỉnh: thay kết quả hai target bằng rerun; cohort hỗn hợp, không là đánh giá held-out.\nNguồn: summary phục hồi, cohorts.*.summary. Không có đối chứng full Test4Py upstream.')
    base=c['control_baseline']['per_target'];ref=c['sota_after_refinement']['per_target']
    targets=sorted(base,key=lambda t:ref[t]['coverage']['line_pct']['penalized_mean_pct']-base[t]['coverage']['line_pct']['penalized_mean_pct'])
    b=[base[t]['coverage']['line_pct']['penalized_mean_pct'] for t in targets]
    a=[ref[t]['coverage']['line_pct']['penalized_mean_pct'] for t in targets]
    fig,ax=plt.subplots(figsize=(7.4,6.4));y=list(range(len(targets)))
    ax.hlines(y,b,a,color='#B5BDC4',linewidth=1.4)
    ax.scatter(b,y,s=25,color=BLUE,label='Baseline',zorder=3)
    ax.scatter(a,y,s=25,color=ORANGE,label='Sau tinh chỉnh',zorder=3)
    ax.set_yticks(y,targets,fontsize=8);ax.set(xlim=(-2,105),xlabel='SC mô-đun, failure penalty = 0 (%)',title='Độ phủ theo 21 target phát triển')
    ax.xaxis.grid(True,alpha=.18);ax.legend(loc='lower right',fontsize=9)
    emit('4.2',fig,{t:{'baseline':bv,'after_refinement':av} for t,bv,av in zip(targets,b,a)},
         '5 lượt/target/nhánh; SC lấy từ summary phục hồi (có CSV fallback).\nChênh lệch mô tả trên target đã quan sát; không tách riêng hiệu ứng AST.')
    s=c['sota_after_refinement']['summary'];rr=s['repairs_by_round'];values=[rr['1'],rr['2']]
    if sum(values)!=s['repairs']:raise ValueError('Repair counts do not sum')
    fig,ax=plt.subplots(figsize=(7,3.1));bars=ax.barh(['Vòng 1','Vòng 2'],values,color=[TEAL,ORANGE],height=.5);ax.invert_yaxis()
    ax.set(xlabel='Số lượt repair thành công',xlim=(0,max(values)*1.3),title='Cohort sau tinh chỉnh — thành công đầu tiên theo evaluation')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True));ax.xaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    for bar,v in zip(bars,values):ax.text(v+.4,bar.get_y()+bar.get_height()/2,f'{v} ({number(100*v/s["repairs"])}%)',va='center')
    emit('4.3',fig,{'repairs':s['repairs'],'by_round':rr,'first_pass':s['first_pass'],'passed':s['passed']},
         '70 pass lần đầu + 28 repair = 98/105. Giai đoạn ban đầu: 67 + 29 = 96/105.\nHai vòng không có chuyên môn cố định; thống kê repair không chứng minh bảo toàn oracle.')
    arm_keys=['source_only','ast_dependencies'];arm_labels=['Source-only','AST dependencies'];counts={}
    for arm in arm_keys:
        item=mutation['per_arm'][arm];counts[arm]=item['counts']
        if sum(item['counts'].values())!=item['denominator_including_inconclusive']:raise ValueError('Mutation denominator inconsistent')
    fig,ax=plt.subplots(figsize=(7,3.5));left=[0,0]
    for status,color,label in [('killed',TEAL,'Killed'),('survived',GREY,'Survived'),('inconclusive',ORANGE,'Inconclusive')]:
        vals=[counts[arm].get(status,0) for arm in arm_keys]
        ax.barh(arm_labels,vals,left=left,label=label,color=color,height=.52)
        for i,v in enumerate(vals):
            if v:ax.text(left[i]+v/2,i,str(v),va='center',ha='center',color='white',weight='bold')
        left=[l+v for l,v in zip(left,vals)]
    ax.set(xlabel='Số lượt mutant đã lên lịch (gồm inconclusive)',xlim=(0,max(left)+1),title='Screen thăm dò trên tập con node phục hồi được chọn')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True));ax.legend(loc='upper center',bbox_to_anchor=(.5,-.18),ncol=3,frameon=False)
    emit('4.4',fig,mutation['per_arm'],
         'Node v0 không sửa đổi; chọn theo kết quả thành công, tối đa 5 mutant cú pháp/target.\nKhông đại diện toàn bộ 54 đầu ra; lỗi không quy được cho assertion giữ inconclusive.')
    ts=['docstring_parser_numpydoc','genty_dataset'];original=c['sota_original']['per_target']
    data={t:{'before':original[t],'after':ref[t]} for t in ts};fig,axes=plt.subplots(1,2,figsize=(7.4,3.8))
    for ax,metric,title in [(axes[0],'pass','Suite pass'),(axes[1],'coverage','SC mô-đun (penalty)')]:
        bv=[original[t]['pass_rate_pct'] if metric=='pass' else original[t]['coverage']['line_pct']['penalized_mean_pct'] for t in ts]
        av=[ref[t]['pass_rate_pct'] if metric=='pass' else ref[t]['coverage']['line_pct']['penalized_mean_pct'] for t in ts]
        for offset,vals,label,color in [(-.18,bv,'Trước tinh chỉnh',BLUE),(.18,av,'Sau tinh chỉnh',ORANGE)]:
            bars=ax.bar([i+offset for i in range(2)],vals,width=.34,label=label,color=color)
            for bar,v in zip(bars,vals):ax.text(bar.get_x()+bar.get_width()/2,v+1.5,number(v,1),ha='center',fontsize=8)
        ax.set_xticks([0,1],['numpydoc','genty_dataset'],fontsize=9)
        ax.set(title=title,ylabel='Tỷ lệ (%)',ylim=(0,80));ax.yaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    axes[0].legend(loc='upper center',bbox_to_anchor=(1.1,1.22),ncol=2,frameon=False,fontsize=9)
    emit('4.5',fig,{t:{k:{'pass_rate_pct':v['pass_rate_pct'],'coverage':v['coverage']['line_pct']['penalized_mean_pct']} for k,v in d.items()} for t,d in data.items()},
         'Mỗi mốc 5 lượt/target. So sánh giai đoạn phát triển trước/sau refinement, không phải Baseline–SOTA.\nTuning theo lỗi đã quan sát; không diễn giải là hiệu ứng nhân quả của AST.')
    lk=['control_baseline','control_council_enhanced','sota_original'];lat=[c[k]['summary']['latency_mean_sec_csv'] for k in lk]
    fig,ax=plt.subplots(figsize=(7,3.4));bars=ax.bar(['Baseline','Council Standard','Cấu hình đề xuất\n(giai đoạn ban đầu)'],lat,color=COLORS,width=.58)
    ax.set(ylabel='Thời gian xử lý TB (giây/lượt)',ylim=(0,max(lat)*1.3),title='Latency trung bình ghi trong CSV — 105 lượt/cohort')
    for bar,v in zip(bars,lat):ax.text(bar.get_x()+bar.get_width()/2,v+.12,number(v,4)+' s',ha='center',fontsize=10)
    ax.yaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    emit('4.6',fig,dict(zip(lk,lat)),
         'Timer gồm generation, pytest/coverage và repair. Đây là metadata CSV, không là benchmark inference.\nKhông dùng latency refined còn metadata cũ; không kết luận Pareto hoặc nhanh hơn Standard.')
    return paths,chart_data

def confirmation_complete(d):
    if not isinstance(d,dict) or not isinstance(d.get('arms'),dict) or not d['arms']:return False
    if not isinstance(d.get('planned'),int) or d['planned']<=0 or d.get('completed')!=d['planned']:return False
    if sum(a.get('planned',0) for a in d['arms'].values())!=d['planned']:raise ValueError('Confirmation arm plans do not sum')
    if any(a.get('completed')!=a.get('planned') or a.get('planned',0)<=0 for a in d['arms'].values()):return False
    rows=d.get('rows')
    if not isinstance(rows,list) or len(rows)!=d['completed']:raise ValueError('Complete confirmation needs all attempt rows')
    for name,a in d['arms'].items():
        rr=[r for r in rows if r.get('arm')==name]
        if len(rr)!=a['completed'] or sum(bool(r.get('accepted')) for r in rr)!=a.get('passed'):raise ValueError('Confirmation row/count mismatch')
    return True

def confirmation_chart(d,path):
    arms=list(d['arms']);rates=[100*d['arms'][k]['passed']/d['arms'][k]['planned'] for k in arms]
    fig,ax=plt.subplots(figsize=(7,3.5));labels=[k.replace('atomic_','').replace('_',' ') for k in arms]
    bars=ax.bar(labels,rates,color=COLORS[:len(arms)],width=.55)
    ax.set(ylabel='Đạt tiêu chí chính (%)',ylim=(0,max(20,max(rates)+15)),title=f"Đánh giá mở rộng: {d.get('target_count','?')} target / {d.get('project_count','?')} project")
    for bar,k,v in zip(bars,arms,rates):
        a=d['arms'][k];ax.text(bar.get_x()+bar.get_width()/2,v+1,f"{a['passed']}/{a['planned']}\n{number(v)}%",ha='center')
    ax.yaxis.grid(True,alpha=.18);ax.set_axisbelow(True)
    save(fig,path,f"Hoàn tất {d['completed']}/{d['planned']} lượt; denominator theo kế hoạch, outcome theo summary.\nSo sánh thành phần, không phải full Test4Py upstream; target/seed có cấu trúc cụm project.")

def insert_figure(p,path,width,caption,note=None):
    # A compact keep-with-next picture/caption pair avoids empty pages.
    p.clear();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next=True;p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(2)
    p.add_run().add_picture(str(path),width=width)
    inline=p._p.xpath('.//wp:docPr')
    for element in inline:element.set('descr',caption)
    if note:
        node=OxmlElement('w:p');p._p.addnext(node);np=Paragraph(node,p._parent)
        np.add_run(note);np.paragraph_format.space_after=Pt(5)
        for r in np.runs:r.font.size=Pt(9)

def polish_tables(doc):
    changes=[]
    for index,t in enumerate(doc.tables):
        n=len(t.columns)
        if not n:continue
        # Wide quantitative tables receive a larger first column and compact numeric cells.
        section=doc.sections[0];available=section.page_width-section.left_margin-section.right_margin
        t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
        first=.24 if n>=7 else (.35 if n>=3 else .43)
        widths=[int(available*first)]+[int(available*(1-first)/(n-1))]*(n-1) if n>1 else [available]
        for col,w in zip(t.columns,widths):col.width=w
        for ri,row in enumerate(t.rows):
            row.height=None
            for ci,cell in enumerate(row.cells):
                cell.width=widths[min(ci,n-1)];cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                pr=cell._tc.get_or_add_tcPr()
                margins=pr.find(qn('w:tcMar'))
                if margins is None:margins=OxmlElement('w:tcMar');pr.append(margins)
                for edge in ['top','bottom','left','right']:
                    e=margins.find(qn('w:'+edge))
                    if e is None:e=OxmlElement('w:'+edge);margins.append(e)
                    e.set(qn('w:w'),'60' if edge in ['left','right'] else '40');e.set(qn('w:type'),'dxa')
                for p in cell.paragraphs:
                    p.paragraph_format.space_before=Pt(1);p.paragraph_format.space_after=Pt(2)
                    p.paragraph_format.line_spacing=1.05;p.paragraph_format.keep_with_next=False
                    for r in p.runs:
                        r.font.name='Times New Roman';r.font.size=Pt(9 if n>=7 else 10)
                        if ri==0:r.font.bold=True
                if ri==0:
                    shade=pr.find(qn('w:shd'))
                    if shade is None:shade=OxmlElement('w:shd');pr.append(shade)
                    shade.set(qn('w:fill'),'EAF0F5')
            rp=row._tr.get_or_add_trPr()
            if ri==0:
                repeat=rp.find(qn('w:tblHeader'))
                if repeat is None:rp.append(OxmlElement('w:tblHeader'))
            # Prevent short rows from breaking; allow exceptionally long cells to paginate.
            if sum(len(c.text) for c in row.cells)<1100 and rp.find(qn('w:cantSplit')) is None:rp.append(OxmlElement('w:cantSplit'))
        # Grid must use the same widths as cell definitions.
        for grid,w in zip(t._tbl.tblGrid.gridCol_lst,widths):grid.set(qn('w:w'),str(int(w/635)))
        changes.append({'table':index,'columns':n,'font_pt':9 if n>=7 else 10,'repeat_header':True})
    return changes

def clean_main(doc,log):
    appendix=False
    # Replace whole paragraphs when they read as editorial instructions rather than scholarship.
    starts={
      'Các thống kê trong Bảng 4.3':'Các thống kê trong Bảng 4.3 là phân tích thăm dò trên 21 trung bình target. Wilcoxon exact được tái tính; p của t và U không được sử dụng để suy luận. Chọn mẫu, tuning và cấu trúc cụm project giới hạn khả năng diễn giải. Nhóm 18 target loại string_utils_slugify, docstring_parser_google và docstring_parser_numpydoc; kết quả được tính theo đúng danh sách này và không xem là nhóm định trước.',
      'Bảng 4.8 dùng bốn nhóm lỗi':'Bảng 4.8 trình bày bốn nhóm lỗi như khung phân tích định tính. Nghiên cứu không ước lượng tần suất do chưa có corpus gán nhãn đầy đủ; khẳng định hằng đúng cần được nhận diện qua kiểm toán source, vì thường không tạo traceback.',
      'Latency CSV trung bình:':'Trong giai đoạn phát triển ban đầu, latency trung bình theo CSV là 3,5321 s/lượt ở Baseline, 4,0426 s/lượt ở Standard và 6,6479 s/lượt ở cấu hình đề xuất. Timer gồm generation, pytest/coverage và repair. Các số đo không hỗ trợ kết luận cấu hình đề xuất nhanh hơn Standard; metadata sau refinement không được dùng để lập đường biên Pareto. Chưa có ledger đầy đủ để định lượng tổng chi phí thực tế hoặc chi phí đơn vị. Chi tiết nguồn và hiệu chỉnh số học được trình bày trong phụ lục thay đổi.',
      'Nguồn kiểm tra:':'Nguồn dữ liệu và quy trình tái lập được trình bày ở phụ lục.',
    }
    for p in list(doc.paragraphs):
        old=p.text
        if old.startswith('PHỤ LỤC'):appendix=True
        if appendix:continue
        new=old
        for prefix,value in starts.items():
            if old.startswith(prefix):new=value;break
        new=new.replace('legacy','giai đoạn phát triển').replace('Implementation','Hiện thực')
        new=new.replace('source đã audit','mã nguồn đã đối chiếu').replace('theo source đã audit','theo mã nguồn đã đối chiếu')
        new=new.replace('vì audit chưa xác minh','do chưa có phép tái tính được kiểm chứng')
        if re.match(r'^Hình 3\.1\.',new):new='Hình 3.1. Kiến trúc khái niệm; ngữ cảnh kết hợp source và curated hints, kiểm toán repair chưa là cổng nhận bắt buộc.'
        if re.match(r'^Hình 3\.2\.',new):new='Hình 3.2. Luồng xử lý khái niệm; hai vòng repair thực tế không phân vai chuyên môn cố định (Thuật toán 3.2).'
        if new!=old:write(p,new);log.append({'kind':'main_prose','before':old,'after':new})

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--confirmation',type=Path,default=ROOT/'research/groq_confirmation_20261118/summary.json')
    ap.add_argument('--evidence',type=Path,default=ROOT/'research/reviews/council_sota_20261118/restored/rebuild_q3x04keb/summary.json')
    ap.add_argument('--mutation',type=Path,default=ROOT/'research/groq_study_20261118_v2/mutation_screen/summary.json')
    args=ap.parse_args();src=args.input.resolve();out=args.output.resolve()
    if src==out or out.exists():raise ValueError('Output must be a NEW path, distinct from input and not already present')
    if not out.is_relative_to(ROOT/'reports') or out.suffix.lower()!='.docx':raise ValueError('Output must be a new DOCX in workspace reports/')
    original=Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx')
    original_before=sha(original);input_before=sha(src)
    if original_before!='9a90877d5fe8c78b56c307042bffd59243e0a90884eec813ef295f13078310d9':raise ValueError('Original does not match audited hash')
    evidence,evmeta=snapshot(args.evidence);mutation,mmeta=snapshot(args.mutation);inputs=[evmeta,mmeta]
    confirmation=None;complete=False
    if args.confirmation.exists():
        confirmation,cmeta=snapshot(args.confirmation);inputs.append(cmeta);complete=confirmation_complete(confirmation)
    assets=out.parent/(out.stem+'_assets')
    if assets.exists():raise ValueError('Asset directory already exists; choose a new output name')
    assets.mkdir(parents=True);setting();charts,chart_data=make_charts(evidence,mutation,assets)
    if complete:
        charts['4.7']=assets/'figure_4_7.png';confirmation_chart(confirmation,charts['4.7']);chart_data['4.7']={k:v for k,v in confirmation.items() if k!='rows'}
    changes=[]
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='council-polish-',dir=out.parent) as td:
        copied=Path(td)/'copy.docx';shutil.copy2(src,copied)
        if sha(copied)!=input_before:raise ValueError('Input copy mismatch')
        doc=Document(copied)
        # Only the LAST occurrence of each caption is a body figure; preceding ones are lists.
        for key in ['4.1','4.2','4.3','4.4','4.5','4.6']:
            matches=[p for p in doc.paragraphs if re.match(r'^Hình '+re.escape(key)+r'\.',p.text)]
            if not matches:raise ValueError(f'Missing required figure anchor {key}')
            for p in matches:write(p,CAPTIONS[key])
            cap=matches[-1];prev=cap._p.getprevious()
            if prev is not None and prev.tag==qn('w:p') and Paragraph(prev,cap._parent).text.startswith('Hình định lượng'):
                pic=Paragraph(prev,cap._parent)
            else:pic=before(cap)
            width=min(Inches(6.3),doc.sections[0].page_width-doc.sections[0].left_margin-doc.sections[0].right_margin)
            insert_figure(pic,charts[key],width,CAPTIONS[key])
            cap.paragraph_format.keep_with_next=False;cap.paragraph_format.space_after=Pt(7)
            cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
            for r in cap.runs:r.font.size=Pt(10);r.font.italic=True
            changes.append({'kind':'verified_figure','figure':key,'path':str(charts[key]),'caption':CAPTIONS[key]})
            if key=='4.4':
                note=before(pic,'Hình 4.4 trình bày screen mới của nghiên cứu thăm dò ở mục 4.8. Mẫu này khác bộ golden giai đoạn phát triển tại Bảng 4.7; hai kết quả không được gộp hoặc dùng thay thế cho nhau.')
                note.paragraph_format.keep_with_next=True
        for p in list(doc.paragraphs):
            if re.match(r'^Hình 1\.1\.',p.text):
                prev=p._p.getprevious()
                if prev is not None and prev.tag==qn('w:p') and Paragraph(prev,p._parent).text.startswith('Hình định lượng'):prev.getparent().remove(prev)
                changes.append({'kind':'remove_obsolete_figure_1_1','before':p.text});remove(p)
        clean_main(doc,changes)
        # Refresh the confirmation section from one snapshot. Suppress ALL stale partial counts/tables.
        anchors=[p for p in doc.paragraphs if re.match(r'^4\.10\.',p.text)]
        if anchors:
            anchor=anchors[-1];cursor=anchor._p.getnext()
            while cursor is not None:
                nxt=cursor.getnext()
                if cursor.tag==qn('w:p') and ''.join(cursor.itertext()).startswith('CHƯƠNG 5.'):break
                cursor.getparent().remove(cursor);cursor=nxt
        else:
            ch5=[p for p in doc.paragraphs if p.text.startswith('CHƯƠNG 5.')][-1]
            anchor=before(ch5,'4.10. Đánh giá mở rộng sau khóa cấu hình',style='Heading 2')
        after_anchor=anchor._p.getnext()
        def add(text='',style=None):
            if after_anchor is not None:
                node=OxmlElement('w:p');after_anchor.addprevious(node);p=Paragraph(node,anchor._parent)
            else:
                node=OxmlElement('w:p');anchor._p.addnext(node);p=Paragraph(node,anchor._parent)
            if text:p.add_run(text)
            if style:p.style=style
            return p
        if complete:
            add(f"Đánh giá mở rộng đã hoàn tất {confirmation['completed']}/{confirmation['planned']} lượt, gồm {confirmation.get('target_count','không ghi')} target thuộc {confirmation.get('project_count','không ghi')} project. Đây là cohort độc lập sau khóa cấu hình; không gộp với pilot hoặc thử nghiệm phát triển. Kết quả đánh giá thành phần, không đối sánh full Test4Py upstream.")
            figp=add();insert_figure(figp,charts['4.7'],Inches(6.2),CAPTIONS['4.7']);add(CAPTIONS['4.7'],'Caption')
            for arm,a in confirmation['arms'].items():add(f"{arm}: {a['passed']}/{a['planned']} đạt tiêu chí chính ({number(100*a['passed']/a['planned'])}%); SC mô-đun có penalty {number(a['penalized_module_line_pct'])}%.")
            add('Tỷ lệ dùng toàn bộ mẫu số kế hoạch; lượt lặp không thay thế project độc lập. Coverage mô-đun không tự chứng minh thực thi thân target hoặc oracle đúng. Chênh lệch giữa hai nhánh cần phân tích theo project và protocol trước khi suy luận ưu thế.')
            # Add the new figure to the figure list immediately after its last existing list entry.
            lists=[p for p in doc.paragraphs if p.text.startswith('Hình 4.6.')]
            if len(lists)>1:
                pos=lists[0]._p;np=OxmlElement('w:p');pos.addnext(np);Paragraph(np,lists[0]._parent).add_run(CAPTIONS['4.7'])
        else:
            add('Đánh giá mở rộng đang được thực hiện. Bản này chưa trình bày tỷ lệ hiệu quả hoặc biểu đồ của cohort mở rộng; kết quả sẽ được tổng hợp sau khi toàn bộ lượt theo kế hoạch hoàn tất. Sự cố hạ tầng được phân biệt với đầu ra kiểm thử không đạt tiêu chí.')
        if complete:
            stats_path=args.confirmation.parent/'statistics.json'
            if stats_path.exists():
                st,meta=snapshot(stats_path);inputs.append(meta)
                lo,hi=st['difference_percentile_95']
                add(f"Chênh lệch cân bằng theo {st['independent_projects']} project: {number(100*st['difference'])} điểm phần trăm; khoảng percentile bootstrap cụm 95% [{number(100*lo)}; {number(100*hi)}] điểm phần trăm. Kiểm tra sign-flip theo project cho p hai phía = {number(st['exact_cluster_signflip_two_sided_p'],4)}. Khoảng còn chứa 0; chưa đủ bằng chứng xác nhận ưu thế suy luận.")
                add('Phân tích thống kê được thực hiện sau khi hoàn tất dữ liệu; bootstrap 20.000 mẫu cụm có seed cố định và chỉ chín project nên độ hiệu chỉnh còn hạn chế. Số lượt seed không thay thế số project độc lập. Ba vị trí target của black không đủ source tương ứng đã bị loại trước suy luận; không thay bằng target thuận lợi hơn.')
                # Include the complete project table; negative and zero effects remain visible.
                tab=doc.add_table(rows=1,cols=4)
                for cell,value in zip(tab.rows[0].cells,['Project','Source','Setup xác minh','Chênh lệch (điểm %)']):cell.text=value
                for project,item in st['per_project'].items():
                    cells=tab.add_row().cells
                    sr=item.get('source_rate',item.get('source',0));vr=item.get('verified_rate',item.get('verified',0))
                    for cell,value in zip(cells,[project,number(100*sr)+'%',number(100*vr)+'%',number(100*(vr-sr))]):cell.text=value
                anchor._p.addnext(tab._tbl);anchor=add('Bảng bổ sung: chênh lệch được giữ theo mọi project; không lọc chỉ các project có mức tăng dương.')
            add('Rà soát source-based trên 27 đại diện target–arm và quét cấu trúc 64 artifact đạt tiêu chí cho thấy cần lưu ý: một số kiểm tra TransportPlugin dựa trên lớp con giả lập; Fieldset có giả định uniqueness trên dữ liệu ngẫu nhiên; BaseProvider dùng private API. Đây là kiểm tra hồi quy theo source, không phải bằng chứng oracle đúng theo đặc tả độc lập. Toàn bộ 64 artifact được chấp nhận đã được replay offline thêm một lần; chỉ kết luận về các artifact được chọn này, không chứng minh không flaky tuyệt đối.')
        changes.append({'kind':'confirmation_section','status':'complete' if complete else 'withheld_incomplete_or_missing','planned':confirmation.get('planned') if confirmation else None,'completed':confirmation.get('completed') if confirmation else None})
        if complete:
            stats_path=args.confirmation.parent/'statistics.json'
            st=json.loads(stats_path.read_text()) if stats_path.exists() else None
            # Lead the conclusion with the strongest directly traceable new evidence.
            for paragraph in doc.paragraphs:
                if paragraph.text.startswith('Trên tập phát triển tuyển chọn, bảng sau tinh chỉnh'):
                    ca=confirmation['arms']['atomic_source'];va=confirmation['arms']['atomic_verified_setup']
                    value=(f"Đánh giá mở rộng hoàn tất {confirmation['completed']} lượt trên {confirmation['target_count']} target thuộc {confirmation['project_count']} project. Setup xác minh đạt {va['passed']}/{va['planned']} ({number(100*va['passed']/va['planned'])}%), đối chứng cùng cấu hình đạt {ca['passed']}/{ca['planned']} ({number(100*ca['passed']/ca['planned'])}%). Mức tăng quan sát là {number(100*(va['passed']/va['planned']-ca['passed']/ca['planned']))} điểm phần trăm; độ phủ mô-đun có penalty tăng {number(va['penalized_module_line_pct']-ca['penalized_module_line_pct'])} điểm. ")
                    if st:
                        lo,hi=st['difference_percentile_95']
                        value+=f"Khoảng bootstrap theo project 95% [{number(100*lo)}; {number(100*hi)}] điểm còn chứa 0; chưa xác nhận ưu thế suy luận. "
                    value+='Kết quả hỗ trợ hướng phát triển setup kiểm chứng trong phạm vi đánh giá thành phần; chưa chứng minh vượt Test4Py upstream. Các cohort phát triển trước đó và mọi kết quả bất lợi được báo riêng, không gộp để tăng cỡ mẫu.'
                    write(paragraph,value)
                    changes.append({'kind':'updated_conclusion_from_complete_confirmation'})
                    break
        table_changes=polish_tables(doc)
        # Add provenance/history to the appendix rather than repeat it in the main narrative.
        doc.add_heading('PHỤ LỤC TRÌNH BÀY. NGUỒN BIỂU ĐỒ VÀ LỊCH SỬ HIỆU CHỈNH',level=1)
        doc.add_paragraph('Bản trình bày này được tạo từ bản hiệu chỉnh trước đó, giữ nguyên dữ liệu thực nghiệm. Sáu hình định lượng được dựng lại từ summary phục hồi và mutation screen mới; hình cold-start không cùng cohort được bỏ. Hai sơ đồ khái niệm được giữ với giới hạn phương pháp. Phụ lục này cùng nhật ký JSON ghi nguồn và lịch sử thay đổi; các số đo chưa đủ hồ sơ không được dùng để suy luận hiệu quả.')
        for meta in inputs:doc.add_paragraph(f"{meta['path']} — SHA256 {meta['sha256']}")
        doc.add_paragraph('Nguồn hình 4.1–4.3, 4.5–4.6: cohorts.* trong summary phục hồi. Hình 4.4: per_arm của mutation screen trên tập con node v0 được chọn. Hình 4.7 chỉ có khi summary mở rộng đầy đủ và số accepted được kiểm tra với từng hàng.')
        if any('0,5033187' in item.get('before','') for item in changes):doc.add_paragraph('Hiệu chỉnh số học chi phí giai đoạn phát triển: input 1.390.650 + output 491.202 = 1.881.852 token; áp dụng đơn giá cấu hình cho 0,5033187 USD. Đây là tái tính từ bảng, không phải ledger đầy đủ hoặc hóa đơn. Các số tổng 0,5166/0,1340 USD không được sử dụng như chi phí đã xác nhận.')
        doc.add_paragraph(f'Bản đầu vào: {src.name}, SHA256 {input_before}. Bản gốc Downloads được giữ nguyên, SHA256 {original_before}.')
        built=Path(td)/'polished.docx';doc.save(built)
        with zipfile.ZipFile(built) as z:
            if z.testzip() is not None:raise ValueError('Corrupt output package')
        reread=Document(built)
        if any('Hình cũ' in p.text or p.text.startswith('Hình định lượng') for p in reread.paragraphs):raise ValueError('Unresolved chart placeholder')
        if any(p.text.startswith('Hình 1.1.') for p in reread.paragraphs):raise ValueError('Obsolete figure survives')
        if sha(src)!=input_before or sha(original)!=original_before:raise ValueError('Protected source changed')
        built.replace(out)
    record={'input':str(src),'input_sha256_before':input_before,'input_sha256_after':sha(src),
        'original_sha256_before':original_before,'original_sha256_after':sha(original),
        'output':str(out),'output_sha256':sha(out),'script_sha256':sha(Path(__file__)),
        'evidence':inputs,'confirmation_complete':complete,'charts':chart_data,'changes':changes,'tables':table_changes,
        'validation':{'package':True,'input_unchanged':sha(src)==input_before,'original_unchanged':sha(original)==original_before,
                      'no_obsolete_chart_placeholders':True,'pdf_review':'separate rendering step required'}}
    out.with_suffix('.polish.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    out.with_suffix('.polish.md').write_text('# Polish log\n\n'+f'Input: `{src.name}` (unchanged). Original Downloads SHA256 unchanged.\n\n'+
        f'{len(charts)} verified charts; {len(table_changes)} tables formatted with repeated headers. Confirmation: '+('complete.' if complete else 'incomplete; numerical results withheld.')+'\n\n'+
        '\n'.join('- '+item.get('caption',item['kind']) for item in changes)+'\n\nEvidence hashes and plotted values: accompanying `.polish.json`. PDF/layout review is separate.\n')
    print(json.dumps({'output':str(out),'charts':len(charts),'tables':len(table_changes),'confirmation_complete':complete,'protected_inputs_unchanged':True},ensure_ascii=False))

if __name__=='__main__':main()
