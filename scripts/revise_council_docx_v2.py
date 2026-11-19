#!/usr/bin/env python3
"""Rebuild a corrected, auditable DOCX copy using only the Python standard library.

Always starts from the immutable original. No source experiment data are edited.
Run again with --summary research/groq_study_20261118_v2/summary.json.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = Path('/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx')
EXPECTED = '9a90877d5fe8c78b56c307042bffd59243e0a90884eec813ef295f13078310d9'
AUDIT = ROOT / 'research/reviews/council_sota_20261118'
RESTORED = AUDIT / 'restored/rebuild_q3x04keb/summary.json'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def q(name): return '{' + W + '}' + name
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def text_of(e): return ''.join(t.text or '' for t in e.iter(q('t')))
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def rewrite(p, value):
    """Retain paragraph and first text-run properties; replace only paragraph content."""
    rp = next((copy.deepcopy(r.find(q('rPr'))) for r in p.iter(q('r')) if r.find(q('rPr')) is not None), None)
    for child in list(p):
        if child.tag != q('pPr'): p.remove(child)
    r = ET.SubElement(p, q('r'))
    if rp is not None: r.append(rp)
    for i, line in enumerate(value.split('\n')):
        if i: ET.SubElement(r, q('br'))
        t = ET.SubElement(r, q('t')); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = line

def replacements():
    # IDs refer to the audit's immutable extraction, not Word page numbers.
    return {
7:'SINH VÀ SỬA LỖI KIỂM THỬ PYTHON BẰNG NGỮ CẢNH MÃ NGUỒN VÀ PHẢN HỒI THỰC THI: NGHIÊN CỨU THĂM DÒ COUNCIL TRÊN TEST4PY',
21:'SINH VÀ SỬA LỖI KIỂM THỬ PYTHON BẰNG NGỮ CẢNH MÃ NGUỒN VÀ PHẢN HỒI THỰC THI: NGHIÊN CỨU THĂM DÒ COUNCIL TRÊN TEST4PY',
142:'Sinh kiểm thử Python bằng LLM gặp lỗi import, chữ ký, thuộc tính và oracle. Tiểu luận khảo sát một pipeline kết hợp mã nguồn được trích bằng AST, hướng dẫn thủ công theo package và tối đa hai lượt phản hồi pytest. Các kết quả legacy thuộc tập phát triển tuyển chọn; thử nghiệm API-facts và chạy upstream cục bộ là các cohort riêng. Vì mô hình, hạ tầng và protocol khác nhau, nghiên cứu không dùng chúng để suy ra ưu thế nhân quả của AST hoặc ưu thế so với Test4Py upstream.',
145:'• RQ1: Các bảng phát triển tuyển chọn ghi nhận tỷ lệ suite pass và độ phủ mô-đun thay đổi thế nào giữa baseline nội bộ, Council Standard và pipeline có curated hints?',
146:'• RQ2: Bao nhiêu lượt pass đầu tiên và bao nhiêu lượt được phục hồi ở từng vòng repair, trước và sau refinement?',
147:'• RQ3: Artifact ablation còn hỗ trợ kết luận nào sau khi khôi phục hàng thất bại bị đổi nhãn?',
148:'• RQ4: Mutation trên golden tuyển chọn cho biết điều gì, và dữ liệu hiện có giới hạn thế nào về oracle, độ ổn định, latency và chi phí?',
150:'Phạm vi legacy gồm 21 target thuộc 8 dự án Python, ba nhánh nội bộ và năm lần gọi mỗi target/nhánh. Bảng cuối có 315 hàng; số thực thi thực tế còn gồm rerun/refinement. Nhãn 42–46 không phải seed inference đã kiểm soát. Mutation gồm 187 mutant chạy trên 21 golden suite được tuyển chọn từ nhiều nhánh. Chưa có manifest xác nhận 105 lượt flaky; không đưa số này vào quy mô thực nghiệm đã chứng minh.',
152:'Phương pháp gồm đọc source, đối chiếu evaluation và phục hồi provenance. Bảng mô tả được tách theo cohort gốc, refined-only và sau thay thế hai target. Thống kê trên 21 trung bình target là thăm dò; target nằm trong 8 project có cấu trúc cụm. Không sử dụng phân bố 384 traceback vì chưa có tập nhãn kiểm chứng.',
154:'Chương 1 phân biệt các nhánh nghiên cứu; Chương 2 trình bày khái niệm; Chương 3 mô tả implementation legacy; Chương 4 báo kết quả phục hồi và giới hạn; Chương 5 kết luận theo phạm vi bằng chứng. Phần thí nghiệm mới chỉ có kết quả khi summary thực tế được cung cấp.',
160:'Chen và cộng sự [3] giới thiệu ChatUniTest, framework sinh và sửa kiểm thử Java có phản hồi thực thi/biên dịch; ở đây không giả định giới hạn đúng một vòng. Juan Altmayer Pizzorno và Emery D. Berger [4] phát triển CoverUp cho Python. Ryan và cộng sự [5] nghiên cứu prompting theo ngữ cảnh mã; Foster, Gulati, Harman và cộng sự [6] nghiên cứu mutation-guided generation tại Meta. Các công trình dùng protocol riêng, không phải các đối chứng đã chạy trong nghiên cứu này.',
163:'Các thử nghiệm tiền trạm được giữ thành các nhánh độc lập: upstream 14B NF4 cục bộ có vấn đề cold-start/timeout; API source held-out so sánh source-only với source + API facts; R16 Groq 20B là nghiên cứu phát triển tuyển chọn. Không nối các chỉ số của ba nhánh thành một pipeline đối chứng.',
164:'Nhật ký upstream cục bộ ghi 95 lượt chuẩn bị và 2.627 giây cold-start trong cấu hình đó. Đây là quan sát vận hành, không phải thời gian của nhánh API-facts và không là phép đo matched với Groq.',
165:'Nhật ký VRAM/timeout của mô hình 14B NF4 chỉ mô tả môi trường GPU cục bộ. Cloud không dùng VRAM trên máy khách không có nghĩa tài nguyên suy luận hoặc chi phí bằng không.',
166:'Thử nghiệm API_SOURCE_HELDOUT_V2 ngày 17/11 dùng 12 target/4 project, 36 lượt mỗi nhánh, không repair/pruning: source-only pass 2/36, source + API facts pass 4/36. Tổng input token 23.865 → 35.187 (+47,44%). Đây không phải full Call-Graph RAG/Test4Py và không đối sánh trực tiếp với 98/105 của cohort Groq sau refinement.',
169:'Bảng 1.2. Các cohort tiền trạm độc lập và giới hạn so sánh',
170:'Cohort | Bằng chứng ghi nhận | Giới hạn diễn giải',
171:'Upstream 14B NF4 cục bộ | Cold-start, VRAM, timeout theo nhật ký riêng | Không gộp với API held-out hoặc Groq 20B',
172:'API held-out source-only | 2/36 suite pass; 23.865 input tokens | 12 target/4 project; không repair/pruning',
173:'API held-out source + API facts | 4/36 suite pass; 35.187 input tokens | Không phải Call-Graph RAG đầy đủ',
174:'R16 Groq 20B gốc | 96/105 suite pass | Tập phát triển tuyển chọn; curated hints',
175:'R16 sau refinement | 98/105 suite pass | Thay hai target bằng rerun; cohort hỗn hợp',
176:'So sánh giữa cohort | Không ước lượng hiệu ứng riêng của AST | Khác model, target, hạ tầng và protocol',
179:'Bảng 1.1 đặt các hướng tiếp cận trong bối cảnh nghiên cứu. Chỉ các nhánh nội bộ có artifact được báo kết quả; không dùng bảng related work để khẳng định ưu thế thực nghiệm.',
183:'ChatUniTest (Chen và cs., 2024) [3] | Ngữ cảnh lớp/phụ thuộc cho Java | Framework generation–validation–repair; không gán cứng một vòng | Không chạy đối chứng trong nghiên cứu này',
184:'CoverUp (Altmayer Pizzorno & Berger) [4] | Python và phản hồi coverage | Coverage-guided generation | Không chạy đối chứng trong nghiên cứu này',
187:'Council legacy (nghiên cứu này) | Source/import qua helper AST + SYMBOL_GROUNDING_MAP và setup hints thủ công | Tối đa 2 vòng cùng loại prompt; không tách chuyên môn cố định | repair_audit được ghi nhưng accepted không điều khiển nhận bản sửa; mutation trên golden hỗn hợp',
189:'Đóng góp được khảo sát là tổ hợp source context, curated hints và phản hồi thực thi trên tập phát triển. Kết quả chưa tách riêng hiệu ứng AST, chưa chứng minh trích xuất bảng định danh liên tệp tự động, và chưa xác lập ưu thế so với upstream.',
205:'AST biểu diễn cấu trúc cú pháp và hỗ trợ đọc source/import mà không thực thi chương trình. Phân giải re-export, thuộc tính động và quy tắc decorator đầy đủ là các bài toán bổ sung. Trong runner legacy, quy tắc package được viết sẵn; không mô tả chúng như kết quả suy tự động từ AST.',
207:'Traceback giúp định hướng sửa lỗi nhưng loại lỗi không nhất thiết xuất hiện theo hai pha cố định. Runner legacy cho phép sửa import, tham số, assertion và thuộc tính ở cả hai vòng. Không có bằng chứng một bộ trích riêng cặp giá trị actual/expected hoặc phân vai vòng 1/vòng 2 như thiết kế ban đầu.',
221:'Lặp nhiều lần gọi API cho phép quan sát biến thiên nhưng không tạo bảo đảm tái lập nếu seed không được truyền. Thống kê bắt cặp trên target cần đi kèm cấu trúc cụm project, chọn mẫu và tuning; Mann–Whitney/A12 không thay cho phân tích ghép cặp hoặc cụm. Rà soát oracle theo đặc tả vẫn cần thiết.',
225:'Implementation legacy gồm helper AST đọc source/import, SYMBOL_GROUNDING_MAP viết sẵn theo package, setup hints có assertion, Coder, chuẩn hóa và tối đa hai lượt repair theo pytest trong subprocess. repair_audit ghi nhận thay đổi nhưng accepted không được dùng làm cổng nhận bản sửa. Subprocess là cô lập tiến trình, chưa là security sandbox. Hình 3.1 giữ làm sơ đồ ý tưởng; các nhãn tự động hóa/gate/ngắt mạch trong hình không phải bằng chứng đã được thi hành.',
228:'3.2. Ngữ cảnh source/import và curated hints theo package',
229:'Runner dùng helper AST lấy mã nguồn/import, đồng thời nhúng SYMBOL_GROUNDING_MAP và setup hints do con người cung cấp. Một số quy tắc được bổ sung sau khi quan sát lỗi trên target đánh giá. Do đó đây là development tuning, không phải repository-independent AST synthesis.',
230:'Thuật toán 3.1. Luồng chuẩn bị ngữ cảnh của implementation legacy',
231:'Đầu vào: target và package đã chọn.\n1. Đọc source/import bằng helper hiện có.\n2. Tra SYMBOL_GROUNDING_MAP theo package; lấy đường dẫn, thuộc tính và quy tắc đã viết sẵn.\n3. Ghép source, map và setup hints (có thể chứa assertion) vào prompt.\n4. Gửi prompt cho Coder.\nGiới hạn: chưa chứng minh luồng tự suy toàn bộ re-export, thuộc tính và C_rules. Cần khóa quy tắc trước đánh giá held-out.',
234:'Runner legacy gọi tối đa hai vòng repair khi suite còn lỗi. Hai prompt cùng cho sửa import/parameter/assertion/attribute và khác chỉ số vòng; không phải hai chuyên môn cố định. Thành công được quy theo evaluation đầu tiên pass, không chứng minh assertion giữ nguyên ý nghĩa.',
235:'Thuật toán 3.2. Luồng repair legacy theo source đã audit',
236:'1. Sinh và chuẩn hóa T_curr; chạy pytest/coverage trong subprocess.\n2. Nếu suite_pass thì kết thúc.\n3. Với r = 1..2 khi còn lỗi: gửi code và phản hồi thực thi để sinh T_cand; chuẩn hóa; gọi repair_audit để ghi nhận; chạy evaluation trên T_cand. Nếu suite_pass thì nhận T_cand và kết thúc; nếu chưa pass, dùng candidate/phản hồi của vòng đó cho lượt kế tiếp theo runner.\n4. Ghi trạng thái cuối cùng.\nĐiểm quan trọng: nhánh nhận bản sửa kiểm tra suite_pass, không kiểm tra audit.accepted. Không có ngưỡng bảo toàn 75% trong gate nhận bản sửa.',
239:'Các kiểm soát legacy cần phân biệt giữa thao tác đã chạy và bảo đảm chưa được chứng minh:',
240:'• Preflight thực hiện biến đổi theo quy tắc package. Cần lưu phiên bản trước/sau để đánh giá tác động; không tự coi mọi biến đổi là bảo toàn ngữ nghĩa.',
241:'• repair_audit kiểm tra số lượng/thay đổi assertion nhưng kết quả accepted không điều khiển nhận repair trong runner legacy. Đếm assertion không chứng minh bảo toàn oracle.',
242:'Không áp dụng công thức ngưỡng 75% như một bảo đảm của kết quả legacy. Gate bắt buộc là yêu cầu cho revision tương lai, cần đánh giá riêng.',
243:'• Token usage và đơn giá cấu hình chỉ cho ước tính. Chưa có ledger đủ để xác nhận tổng chi phí hoặc chứng minh mọi request, kể cả gọi lại khi cạn output token, đều được cộng.',
244:'C_est = tổng usage từng request × đơn giá tương ứng. Chỉ tính được khi ledger đầy đủ; không xác nhận ngưỡng 1 USD đã được tuân thủ trong legacy.',
246:'Bảng legacy bố trí ba nhánh × 21 target × năm lần gọi, gắn nhãn 42–46. Payload Groq legacy không truyền seed; đây là nhãn lượt lặp, không phải năm inference seed độc lập đã kiểm soát. Rerun/refinement làm tổng số thực thi vượt số hàng cuối.',
247:'N_bảng = 3 × 21 × 5 = 315 hàng; cohort gốc và refined-only được lưu riêng.',
251:'Phương pháp | Baseline nội bộ; Council Standard; pipeline curated hints + preflight + tối đa hai vòng repair; không phải đối chứng Test4Py upstream',
253:'Lượt lặp | 21 target × 5 lần gọi/nhánh, nhãn 42–46; seed legacy không được gửi tới API',
254:'Biến kết quả | Suite pass; module coverage (phân biệt đo thực và failure penalty); repair theo evaluation; mutation trên golden riêng. FR chưa có manifest xác minh',
255:'Điều kiện | Cùng model trong bảng nội bộ; target và quy tắc có development tuning; pytest chạy subprocess, không gọi là security sandbox',
285:'1. Chuẩn bị context | Helper AST source/import và map/hints thủ công | Prompt có tri thức curated, không phải bảng định danh suy hoàn toàn tự động',
287:'3. Chuẩn hóa và audit | Preflight và ghi repair_audit | accepted chưa là gate nhận repair trong legacy',
288:'4. Thực thi và repair | Pytest subprocess; tối đa 2 vòng cùng loại chỉ dẫn | Evaluation/code từng phiên bản; không suy bảo toàn oracle',
289:'5. Tổng hợp | Tách cohort và missingness; mutation trên golden riêng | FR/taxonomy/chi phí chỉ báo nếu có ledger; không suy số còn thiếu',
293:'PR dùng số suite pass trên số lượt của cohort. SC/BC đo trên mô-đun; khi tính trung bình phạt failure bằng 0 phải nói rõ, khác với coverage đo thật bằng 0. Giá trị đo bị thiếu giữ null và công bố mẫu số; không đổi thành zero.',
295:'Mutation runner sinh bốn loại ROR/AOR/BVR/SIR; CRP không có trong luồng này. Bộ 187 mutants được đánh giá với golden tuyển chọn, không phải 105 đầu ra SOTA.',
301:'CRP | Không triển khai trong runner mutation này | Không đưa vào tập toán tử đã đo | Không có kết quả CRP',
302:'SIR | Return-expression replacement | return expr → return None | Không phải đảo if/else hoặc xóa gán trạng thái',
309:'Kết quả legacy báo riêng các cohort được phục hồi offline từ evaluation và CSV. Mỗi target có năm lần gọi gắn nhãn 42–46; không có inference seed được kiểm soát. Bảng sau refinement thay kết quả hai target, không phải 105 lượt theo protocol đã khóa. Nguồn kiểm tra: restored/rebuild_q3x04keb/summary.json và validation.md; missingness được giữ trong nguồn.',
312:'Mô hình/hạ tầng | Groq openai/gpt-oss-20b cho bảng nội bộ; upstream Qwen 14B NF4 là nhánh riêng, không ghép chỉ số',
313:'Nhánh nội bộ | Baseline 105 hàng; Standard 105 hàng; SOTA gốc 105 hàng; refined-only tách riêng trước khi lập cohort sau thay thế',
314:'Tập và nhóm | 21 target/8 project tuyển chọn; nhóm 18 target là thăm dò sau xem kết quả, không gọi nhóm không rẽ nhánh',
316:'Mutation/ổn định | 187 mutant/4 loại toán tử trên golden hỗn hợp; chưa có manifest 105 lượt flaky để xác nhận FR',
320:'Bảng 4.2 giữ chỉ số pass/SC phát triển sau refinement; cột repair được phục hồi theo evaluation. Mutation thuộc golden tuyển chọn khác nhánh, không dùng làm chất lượng của mỗi lượt SOTA. Các mẫu số và thiếu dữ liệu phải đọc cùng hồ sơ phục hồi.',
321:'Bảng 4.2. Mô tả tập phát triển sau refinement (5 lần gọi/target); mutation trên golden riêng',
346:'Baseline nội bộ pass 51/105 (48,57%), Standard 73/105 (69,52%). SOTA gốc 96/105 (91,43%); sau thay kết quả hai target bằng rerun đạt 98/105 (93,33%). SC failure-penalized lần lượt xấp xỉ 24,13%, 37,75%, 46,50% và 47,70%. Đây là mô tả các artifact phát triển có tuyển chọn và tuning; không phải bằng chứng nhân quả riêng cho AST. Độ phủ đo trên module và penalty cần phân biệt với missingness trong summary phục hồi.',
351:'Bảng 4.3. Thống kê thăm dò trên 21 trung bình target đã xuất; không suy khái quát sang project mới',
355:'Paired t | Không tái xác minh p trước refinement | t = 4,2074705; p không báo | Target có cụm project | Chỉ mô tả trên bảng đã xuất',
356:'Wilcoxon | Không báo suy luận trước refinement | W = 6; p exact hai phía = 0,00001335144 | Chênh lệch target đã xuất | Không sửa sai cohort hoặc tuning',
357:'Mann–Whitney U | Không báo p | U = 359; p không báo | Không thay phân tích ghép cặp/cụm | Không diễn giải như hiệu ứng nhân quả',
358:'Paired Cohen dz | Không báo trước refinement | dz = 0,9181453 | SD của chênh lệch ghép cặp | Không phải Cohen d độc lập',
359:'Vargha–Delaney A12 | Không báo trước refinement | A12 = 0,8140590 | Thống kê hai phân bố target | Không là xác suất thắng trên project mới',
361:'Các thống kê trong Bảng 4.3 chỉ mô tả 21 trung bình target đã xuất. Không báo p của t/U vì audit chưa xác minh; Wilcoxon exact được tái tính nhưng không khắc phục chọn mẫu, tuning hoặc cấu trúc cụm. Nhóm 18 target dưới đây dùng đúng danh sách loại trong văn bản: string_utils_slugify, docstring_parser_google, docstring_parser_numpydoc. Kết quả được tính lại từ đúng membership; đây là phân tích thăm dò, không phải tiêu chí nhóm định trước.',
362:'Bảng 4.4. Nhóm thăm dò 18 target theo danh sách loại đã công bố',
369:'Cohort gốc: 67 pass lần đầu + 29 phục hồi (24 vòng 1, 5 vòng 2) = 96/105. Cohort sau refinement: 70 pass lần đầu + 28 phục hồi (22 vòng 1, 6 vòng 2) = 98/105. Bảng 4.5 báo cohort sau refinement; không trộn phân bổ gốc. Hai vòng không có chuyên môn cố định và so sánh OneOf giữa hai nhánh không tách riêng hiệu ứng vòng 2. Mutation golden không cho điểm mutation riêng cho từng vòng repair.',
371:'Mốc thành công (sau refinement) | Số lượt | Tỷ trọng trong repair | Diễn giải | Mutation theo vòng',
372:'Vòng 1 | 22 | 78,57% | Evaluation pass đầu tiên tại vòng 1; không gán loại lỗi cố định | Chưa có bằng chứng',
373:'Vòng 2 | 6 | 21,43% | Evaluation pass đầu tiên tại vòng 2; không tách hiệu ứng nhân quả | Chưa có bằng chứng',
374:'Tổng repair | 28 | 100,00% | 70 pass lần đầu + 28 repair = 98/105 | Không suy từ golden',
379:'Artifact gốc xác nhận full_method chỉ pass 5/6 (83,33%); pycg_classes thất bại vì assertion MRO. SC phạt failure bằng 0 là 49,20%, thay cho 57,90% đã xuất sai. Không có artifact pass thay thế cho hàng này. Các biến thể được phục hồi riêng ở Bảng 4.6. Với sáu target, kết quả là thăm dò và không hỗ trợ kết luận AST là điều kiện tiên quyết; đặc biệt không giữ diễn giải preflight không tác động dựa trên hai mức coverage gần nhau đã sai.',
388:'Golden mutation được chọn theo pass, coverage cao và latency thấp từ nhiều nhánh: 19 council_enhanced (Standard), 2 baseline. Nhãn JSON ghi 71/187 killed (37,97%); trung bình target 43,10%. Đây không phải score của 105 đầu ra SOTA. Có 20/21 file khớp nguồn manifest; pycg_scopes đổi kiểm tra tập khóa bằng nhau thành chứa tập con, làm yếu điều kiện; chưa có giải trình tác động. Runner coi return code khác 0 hoặc timeout là kill, nhưng chi tiết thiếu log/return code để phân biệt assertion, collection/import và hạ tầng. JSON không ghi timeout nên không quy các kill quan sát là timeout. Chưa có manifest xác minh FR 105/105; không báo FR = 0.',
389:'Bảng 4.7. Nhãn mutation trên golden tuyển chọn (19 Standard + 2 Baseline), attribution kill chưa đầy đủ',
391:'SIR | return expr → return None | 23 | 19 | 82,61% | Nhãn kill legacy, chưa tách lỗi assertion và lỗi hạ tầng',
401:'Bảng 4.8 dùng bốn nhóm lỗi làm khung mô tả định tính, không báo tần suất. Chưa có 384 traceback cùng nhãn để tái lập; tautology thường không tạo traceback nên cần kiểm toán source riêng.',
402:'Bảng 4.8. Khung phân loại định tính, chưa có corpus gán nhãn để ước lượng tỷ trọng',
410:'Hai case study so sánh SOTA trước và sau tinh chỉnh, không phải Baseline: numpydoc pass 40% → 60%, SC 21,94% → khoảng 32,50%; genty_dataset pass 40% → 60%, SC 24,39% → khoảng 39,00%. Baseline trong Bảng 4.2 lần lượt pass 0% và 20%. Quy tắc theo lỗi quan sát là curated development hints, không chứng minh lược đồ AST tự động. Khung mã 4.1 chỉ là minh họa, không là artifact thực thi để suy chỉ số.',
411:'Khung mã 4.1. Minh họa lỗi giao diện và quy tắc curated; không đại diện so sánh Baseline–SOTA',
412:'Minh họa numpydoc: dùng short_description/long_description thay vì summary theo API thực. Minh họa genty_dataset: dùng quy tắc decorator và đối số phù hợp với source. Để tái lập cần dùng file trước/sau và evaluation trong manifest phục hồi; không dùng ví dụ mã rút gọn này để tính pass hoặc coverage.',
417:'Golden suite minh họa assertion kiểm tra giao diện và bất biến nhưng nguồn là tuyển chọn Standard/Baseline. Không quy thay đổi OneOf cho vòng 2 SOTA khi chưa có chuỗi phiên bản tương ứng. Monkeypatch đồng hồ có thể giảm phụ thuộc thời gian; tự nó không chứng minh FR bằng 0. pycg_scopes có assertion được sửa yếu hơn và phải giữ trong giới hạn provenance.',
418:'Khung mã 4.2. Cách đọc golden suite và yêu cầu kiểm chứng oracle',
419:'Khi đọc golden typesystem_oneof, đối chiếu truy cập err.messages() với production API. Với pycg_callgraph, đối chiếu kiểm tra bất biến và từng log mutant trước khi quy kill. Với codetiming_timer, kiểm tra patch đúng clock và replay trong môi trường khóa. Các ví dụ không chứng minh bảo toàn oracle hay không flaky tuyệt đối.',
421:'4.4. Thời gian xử lý và giới hạn ước tính chi phí',
422:'Latency CSV trung bình: Baseline 3,5321 s, Standard 4,0426 s, SOTA gốc 6,6479 s/lượt. Timer gồm generation, pytest/coverage và repair, không chỉ inference; latency refined có thể còn metadata cũ. Không có bằng chứng matched rằng SOTA nhanh hơn Standard hoặc nằm trên Pareto frontier. Chưa có ledger xác nhận 0,5166 USD tổng hay 0,1340 USD SOTA, nên không báo các khoản này như chi thực tế. Kiểm tra số học bảng kinh tế cho 1.390.650 + 491.202 = 1.881.852 token; theo đơn giá cấu hình là 0,5033187 USD, chỉ là tái tính từ bảng, không hóa đơn/ledger. Không suy chi phí đơn vị khi phạm vi tổng chưa khớp.',
423:'Bảng 4.9. Latency legacy theo CSV và mức độ sẵn có của bằng chứng chi phí',
424:'Cohort | Latency CSV TB | Suite pass | SC failure-penalized | Mutation cùng cohort | Chi phí | Giới hạn',
425:'Baseline nội bộ | 3,5321 s | 51/105 | 24,13% | Chưa đo cùng cohort | Chưa có ledger xác minh | Không phải Test4Py upstream',
426:'Council Standard | 4,0426 s | 73/105 | 37,75% | Chưa đo cùng cohort | Chưa có ledger xác minh | Cùng bảng phát triển tuyển chọn',
427:'API-facts held-out | Không ghép cold-start upstream | 4/36 | Không so với SC Groq | Không có matched mutation | Không có matched ledger | Nhánh riêng; không phải full RAG',
428:'SOTA gốc / sau refinement | 6,6479 s (gốc, CSV) | 96/105 / 98/105 | 46,50% / 47,70% | 37,97% thuộc golden hỗn hợp riêng | Chưa có ledger xác minh | Không suy nhanh hơn Standard hoặc Pareto',
434:'Mutation dùng bốn toán tử, trong đó SIR thay return expression bằng None. Kill legacy thiếu log phân loại; cần original-pass check và lưu stdout/stderr/return code, tách killed/survived/invalid/timeout/inconclusive. Chưa có hồ sơ rà soát 42/187 mutants hoặc hai equivalent mutants để xác nhận tỷ lệ. FR và taxonomy chưa có ledger tương ứng. Độ phủ cao không chứng minh oracle đúng.',
436:'Năm nhãn 42–46 chỉ là lượt gọi legacy: Groq payload không có seed. Thống kê trên 21 target trong 8 project cần điều chỉnh hoặc ít nhất trình bày cấu trúc cụm; số p trên bảng đã xuất không chứng minh tính khái quát. Tăng số lặp cần đi kèm protocol khóa, source/config snapshot và dữ liệu request đầy đủ.',
438:'Các thư viện công khai có thể đã xuất hiện trong tiền huấn luyện. Curated hints, lựa chọn theo hiệu năng và tuning trên target đã quan sát gây nhiễu; dùng cùng model không loại bỏ các nhiễu này. repair_audit chưa là gate và có golden assertion bị làm yếu. Cần đánh giá revision mới trên target chưa dùng cục bộ, giữ source/prompt/code/evaluation và tách rõ khỏi legacy.',
440:'21 target thuộc 8 project được tuyển chọn; pipeline còn có bước giữ target hiệu năng cao rồi thêm target mới. Nhóm 18 target là hậu nghiệm, không là bằng chứng đại diện cho lớp phần mềm có nhánh/trạng thái. Kết quả không tự khái quát tới project mới, hệ thống mạng/cơ sở dữ liệu hoặc ngôn ngữ khác.',
444:'Kết quả phục hồi cho thấy bảng phát triển có suite pass cao hơn baseline nội bộ, nhưng curated hints, refinement, chọn mẫu và giới hạn provenance ngăn suy ưu thế nhân quả hoặc vượt Test4Py upstream. Bảng 5.1 trả lời câu hỏi theo đúng cohort và bằng chứng hiện có. Không xác nhận FR, corpus 384 mẫu hoặc tổng chi phí legacy chưa có hồ sơ.',
447:'RQ1 | Mô tả tập phát triển, chưa tách hiệu ứng AST | Baseline 51/105; Standard 73/105; SOTA gốc 96/105; sau refinement 98/105. SC xấp xỉ 24,13%; 37,75%; 46,50%; 47,70%. Nhóm 18 target tính theo membership công bố là thăm dò.',
448:'RQ2 | Phục hồi theo evaluation đầu tiên pass, không chứng minh oracle được giữ | Gốc: 67 + 29 (24/5) = 96; sau refinement: 70 + 28 (22/6) = 98. Không tách chuyên môn hai vòng hoặc suy hiệu ứng riêng từ OneOf.',
449:'RQ3 | Khôi phục ablation, rút kết luận dựa trên ô bị sửa sai | Full_method 5/6 = 83,33%; SC phạt failure bằng 0 = 49,20%; pycg_classes vẫn FAIL. Sáu target chỉ hỗ trợ phân tích thăm dò.',
450:'RQ4 | Mutation trên golden hỗn hợp; chưa đủ hồ sơ về FR và chi phí | 71/187 nhãn killed = 37,97%, trung bình target 43,10%; 19 Standard + 2 Baseline; một assertion pycg_scopes yếu hơn. Không báo FR hoặc Pareto/chi phí đã xác minh.',
453:'Hướng phát triển: khóa source/config và tiêu chí chọn mẫu trước inference; tách original/rerun/refined; tự động trích dependency mà không nhúng oracle; thực thi gate chống làm yếu assertion; giữ ledger mọi request và log từng mutant; đánh giá held-out matched với cùng model, repair cap và môi trường. Một thí nghiệm mới chỉ chứng minh phạm vi nó đo được, không hợp thức hóa hồi tố legacy.',
456:'[1] R. Liu, Z. Zhang, Y. Hu, Y. Lin, X. Gao và H. Sun, “Type-aware LLM-based Regression Test Generation for Python Programs,” arXiv:2503.14000, v2 ngày 22/10/2025. https://arxiv.org/abs/2503.14000',
458:'[3] Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng và Jianwei Yin, “ChatUniTest: A Framework for LLM-Based Test Generation,” FSE Companion, 2024. https://arxiv.org/abs/2305.04764',
459:'[4] Juan Altmayer Pizzorno và Emery D. Berger, “CoverUp: Coverage-Guided LLM-Based Test Generation,” DOI: 10.1145/3729398; preprint arXiv:2403.16218. https://doi.org/10.1145/3729398',
461:'[6] Christopher Foster, Abhishek Gulati, Mark Harman và cộng sự, “Mutation-Guided LLM-based Test Generation at Meta,” arXiv:2501.12862, 2025. https://arxiv.org/abs/2501.12862',
473:'[18] Z. Yuan, Y. Lou, M. Liu, S. Ding, K. Wang, Y. Chen và X. Peng, “No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation,” arXiv:2305.04207, 2023. https://arxiv.org/abs/2305.04207',
477:'[22] J. Walczak, P. Tomalak và A. Laskowski, “Impact of Code Context and Prompting Strategies on Automated Unit Test Generation with Modern General-Purpose Large Language Models,” arXiv:2507.14256, 2025. Chưa xác minh DOI cho nhãn Journal of Systems and Software. https://arxiv.org/abs/2507.14256',
478:'[23] Mục tham khảo cũ chưa xác minh được tổ hợp tiêu đề/tác giả/ấn phẩm. Tạm rút khỏi nguồn hỗ trợ lập luận; cần DOI hoặc PDF gốc trước khi khôi phục.',
479:'[24] Mục tham khảo cũ chưa xác minh được tổ hợp tiêu đề/tác giả/ấn phẩm. Tạm rút khỏi nguồn hỗ trợ lập luận; cần DOI hoặc PDF gốc trước khi khôi phục.',
    }

def pct(x): return 'NA' if x is None else f'{x:.2f}'.replace('.', ',') + '%'
def derived_replacements(d):
    c = d['cohorts']; out = {}
    # Rebuild all six pass/coverage cells and repair attribution from restored evidence.
    extracted = read_extraction()
    for i in range(323, 344):
        cells = extracted[i].split(' | '); target = cells[0]
        for offset, key in [(1, 'control_baseline'), (3, 'control_council_enhanced'), (5, 'sota_after_refinement')]:
            t = c[key]['per_target'][target]
            cells[offset] = pct(t['pass_rate_pct'])
            cells[offset + 1] = pct(t['coverage']['line_pct']['penalized_mean_pct'])
        cells[7] = str(c['sota_after_refinement']['per_target'][target]['repairs'])
        cells[8] += ' [golden hỗn hợp]'
        out[i] = ' | '.join(cells)
    out[322] = 'Target | Base pass | Base SC (penalty) | Std pass | Std SC (penalty) | Sau tinh chỉnh pass | SC (penalty) | Repair sau tinh chỉnh | MS golden khác cohort'
    out[344] = 'Toàn tập (21 target) | 48,57% | 24,13% | 69,52% | 37,75% | 93,33% | 47,70% | 28 | 37,97% global; 43,10% TB target [golden riêng]'
    exclude = {'string_utils_slugify', 'docstring_parser_google', 'docstring_parser_numpydoc'}
    vals = []
    for key in ['control_baseline', 'control_council_enhanced', 'sota_after_refinement']:
        ts = [v for k,v in c[key]['per_target'].items() if k not in exclude]
        assert len(ts) == 18
        n = sum(t['n'] for t in ts); passed = sum(t['passed'] for t in ts)
        sc = sum(t['coverage']['line_pct']['penalized_mean_pct'] for t in ts)/18
        vals.append((passed, n, sum(t['passed']==t['n'] for t in ts), sc))
    out[363] = 'Chỉ số nhóm hậu nghiệm (18 target) | Baseline | Standard | Sau tinh chỉnh | Chênh lệch so Base'
    out[364] = ' | '.join(['Suite pass'] + [f'{p}/{n} ({pct(100*p/n)})' for p,n,_,_ in vals] + [f'{100*(vals[2][0]-vals[0][0])/90:+.2f} điểm %'])
    out[365] = ' | '.join(['Target pass đủ 5/5']+[f'{v[2]}/18' for v in vals]+[str(vals[2][2]-vals[0][2])+' target'])
    out[366] = ' | '.join(['SC penalty trung bình']+[pct(v[3]) for v in vals]+[f'{vals[2][3]-vals[0][3]:+.2f} điểm %'])
    for i,key,label in [(382,'ablation_full_method','Đầy đủ'),(383,'ablation_wo_auto_import','Không preflight'),(384,'ablation_wo_critic','Không critic'),(385,'ablation_wo_grounding','Không curated grounding')]:
        s = c[key]['summary']; out[i] = ' | '.join([label,f"{s['passed']}/{s['n']} ({pct(s['pass_rate_pct'])})",pct(s['coverage']['line_pct']['penalized_mean_pct']),pct(s['coverage']['branch_pct']['penalized_mean_pct']),f"{s['latency_mean_sec_csv']:.4f} s (CSV)"])
    for i in range(404,408):
        cells=extracted[i].split(' | '); cells[2]='Không ước lượng'
        if i==404: cells[5]='Source/import + curated hints; cần kiểm tra riêng tự động hóa'
        if i==407: cells[5]='Kiểm toán source riêng; đếm assertion không chứng minh ngữ nghĩa; gate nhận repair chưa bắt buộc trong giai đoạn phát triển'
        out[i]=' | '.join(cells)
    return out

def read_extraction():
    return {int(m[1]):m[2] for line in (AUDIT/'paper_extracted.txt').read_text().splitlines() if (m:=re.match(r'^(\d+): (.*)$',line))}

def polished(value):
    for old,new in [('legacy','giai đoạn phát triển'),('implementation','hiện thực'),('Implementation','Hiện thực'),('Legacy','Giai đoạn phát triển'),('source đã audit','mã nguồn đã đối chiếu'),('bị đổi nhãn','được hiệu chỉnh'),('hàng thất bại bị đổi nhãn','hiệu chỉnh kết quả'),('ô bị sửa sai','kết quả được hiệu chỉnh')]:
        value=value.replace(old,new)
    value=re.sub(r'\s*\[(?:23|24)\]', '', value)
    return value

def add_paragraph(value, template=None):
    p=ET.Element(q('p'))
    if template is not None and template.find(q('pPr')) is not None: p.append(copy.deepcopy(template.find(q('pPr'))))
    rewrite(p,value); return p

def simple_table(rows, template):
    t=copy.deepcopy(template)
    original_rows=t.findall(q('tr'))
    prototype=copy.deepcopy(original_rows[1] if len(original_rows)>1 else original_rows[0])
    for r in original_rows:t.remove(r)
    for values in rows:
        r=copy.deepcopy(prototype); cells=r.findall(q('tc'))
        while len(cells)<len(values):
            r.append(copy.deepcopy(cells[-1])); cells=r.findall(q('tc'))
        for cell in cells[len(values):]:r.remove(cell)
        for cell,value in zip(cells,values):
            ps=cell.findall(q('p'))
            for p in ps[1:]:cell.remove(p)
            p=ps[0] if ps else ET.SubElement(cell,q('p')); rewrite(p,str(value))
        t.append(r)
    # Grid definitions must agree with column count, including newly created tables.
    grid=t.find(q('tblGrid'))
    if grid is not None:
        for child in list(grid):grid.remove(child)
        for _ in rows[0]: ET.SubElement(grid,q('gridCol'),{q('w'):str(9000//len(rows[0]))})
    return t

def load_record(path, provenance):
    if not path.exists():return None
    raw=path.read_bytes(); obj=json.loads(raw)
    provenance[str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)]={'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
    return obj

def compact_aggregates(obj, prefix='', depth=0):
    """Render only aggregates, never completions, source code, row lists, or secrets."""
    if not isinstance(obj,dict):return []
    out=[]
    for k,v in obj.items():
        if k.lower() in {'rows','attempts','results','targets','manifest','source','prompt','completion','requests','ledger','api_key','token','authorization','details','per_target','pairs'}:continue
        label=prefix+k
        if isinstance(v,dict) and depth<3:out+=compact_aggregates(v,label+'.',depth+1)
        elif isinstance(v,(str,int,float,bool)) or v is None:
            out.append((label,'NA' if v is None else str(v)))
    return out

def experiment_section(args, table_template, provenance):
    nodes=[]
    def p(s):
        node=add_paragraph(s)
        if re.match(r'^4\.\d+\. ',s):
            pr=ET.SubElement(node,q('pPr'));ET.SubElement(pr,q('pStyle'),{q('val'):'Heading2'})
        nodes.append(node)
    def table(rows):nodes.append(simple_table(rows,table_template))
    study=load_record(args.summary,provenance)
    p('4.6. Nghiên cứu thăm dò mới trên các dự án chưa dùng trong giai đoạn phát triển')
    if study is None:
        p('Chưa có summary kết quả của chiến dịch mới tại thời điểm dựng bản thảo. Không bổ sung số đo mới hoặc suy diễn hiệu quả từ kế hoạch.');return nodes
    manifest_path=args.summary.parent/'manifest.json'
    if not manifest_path.exists(): manifest_path=ROOT/'research/groq_study_20261118/manifest.json'
    manifest=load_record(manifest_path,provenance)
    arms=study.get('arms',{})
    if not isinstance(arms,dict) or not {'source_only','ast_dependencies'}<=set(arms):
        raise ValueError('Primary summary must contain source_only and ast_dependencies arms')
    rows=study.get('rows',[])
    # Infrastructure-only summaries are never converted into efficacy rates.
    infrastructure=bool(rows) and all(str(r.get('status','')).startswith(('http','api_error','infrastructure','gateway')) or r.get('status')=='error:HTTPError' for r in rows)
    if infrastructure:
        p('Chiến dịch này chỉ ghi nhận lỗi hạ tầng/API, không có đầu ra mô hình hợp lệ để ước lượng hiệu quả. Không diễn giải như tỷ lệ sinh thành công bằng 0.');return nodes
    if not rows:raise ValueError('Primary summary lacks attempt-level rows; refuse unsupported efficacy summary')
    planned=study['planned']; completed=study['completed']
    assert len(rows)==completed
    p(f'Thiết kế ghép cặp gồm 9 target, 7 mô-đun thuộc 3 dự án sty, pyMonet và pytutils; 2 nhánh và 3 lượt lặp, tổng {planned} lượt dự kiến; summary ghi {completed} lượt hoàn tất. Các dự án chưa được dùng cục bộ ở giai đoạn trước, nhưng được chọn vì tính khả thi Python thuần, không phải mẫu ngẫu nhiên đại diện. So sánh source-only với source cộng dependency trích tĩnh; cùng model, hai vòng repair tối đa và cấu hình sinh. Seed gửi API theo best effort không bảo đảm tính tất định hoặc tạo đơn vị thống kê độc lập.')
    if manifest:
        targets=manifest.get('targets',[])
        if targets:
            projects={t['project']:t.get('commit','NA') for t in targets}
            table([['Dự án','Commit đã khóa']]+[[k,v] for k,v in sorted(projects.items())])
        p('Nguồn thiết kế: '+str(manifest_path.relative_to(ROOT))+f'; SHA256 {digest(manifest_path)}. Mục tiêu chính yêu cầu suite pass, coverage mô-đun dương, replay và static assertion gate; không đồng nhất với đúng oracle theo đặc tả.')
    result=[['Nhánh','Hoàn tất / kế hoạch','Đạt tiêu chí chính','Pass lần đầu','SC module có penalty']]
    rates={}
    for arm in ['source_only','ast_dependencies']:
        a=arms[arm]; rr=[r for r in rows if r['arm']==arm]
        assert len(rr)==a['completed']
        assert sum(bool(r.get('accepted')) for r in rr)==a['passed']
        n=a['planned']; rates[arm]=100*a['passed']/n
        result.append([arm,f"{a['completed']}/{n}",f"{a['passed']}/{n} ({pct(rates[arm])})",str(a['first_pass']),pct(a.get('end_to_end_line_pct'))])
    table(result)
    diff=rates['ast_dependencies']-rates['source_only']
    p(f'Chênh lệch AST-dependencies − source-only là {diff:+.2f} điểm phần trăm theo mẫu số kế hoạch của mỗi nhánh. Kết quả này không chứng minh cải thiện hoặc ưu thế suy luận. Coverage end-to-end có penalty dùng toàn bộ lượt; không thay kết quả bị gate từ chối bằng kết quả của tập con được tuyển lại. Các lỗi và trường hợp cần semantic review vẫn được giữ trong mẫu số. Chưa có đối chứng full Test4Py upstream để khẳng định vượt công cụ đó.')
    from collections import Counter
    counts=Counter((r['arm'],r.get('status','NA')) for r in rows)
    table([['Nhánh','Trạng thái kết thúc','Số lượt']]+[[arm,status,str(n)] for (arm,status),n in sorted(counts.items())])
    p('Lần chạy trước gặp HTTP gateway 1010 và không có đầu ra mô hình: được lưu riêng như sự cố hạ tầng, không gộp thành thất bại hiệu quả. Các khoản đặt trước trong ledger dùng quản lý ngân sách, không phải hóa đơn suy luận. Chi phí chỉ công bố theo ledger đầy đủ và phân biệt đặt trước với usage thực.')
    p('Giới hạn thống kê: 27 cặp lượt gọi vẫn chỉ thuộc 9 target và 3 project. Lượt lặp/seed không là 27 project độc lập; ba cụm quá ít để khái quát sang project mới. Khoảng tin cậy nếu có chỉ mang tính mô tả. Với 3 cụm, p hai phía nhỏ nhất của sign-flip đầy đủ là 0,25; nghiên cứu không có khả năng xác lập ưu thế suy luận bằng phép thử này. Phân tích công suất/sensitivity là kế hoạch quy mô tương lai, không chứng minh đã đạt cỡ mẫu.')
    statistics_path=args.statistics or args.summary.parent/'statistics.json'
    stats=load_record(statistics_path,provenance)
    if stats:
        p('Phụ lục thống kê bổ sung được lưu trong statistics.json và STATISTICS.md cùng cohort; các giả định và sensitivity cần đọc theo đúng định nghĩa chỉ số. Các giá trị sau trích nguyên trường tổng hợp, không dùng để kết luận superiority.')
        args._statistics_appendix = [add_paragraph('PHỤ LỤC THỐNG KÊ. ĐỘ NHẠY CỠ MẪU VÀ PHÂN TÍCH CỤM')]
        statrows=[['Chỉ số','Giá trị'],['Số cặp lượt gọi',str(stats.get('paired_repetitions','NA'))],['Project độc lập',str(stats.get('independent_projects','NA'))],['Chênh lệch cân bằng project',pct(100*stats['equal_project_weighted_difference'])],['Sign-flip cụm, p hai phía',str(stats.get('cluster_sign_flip_two_sided_p','NA'))]]
        args._statistics_appendix.append(simple_table(statrows,table_template))
        sensitivity=stats.get('sensitivity',[])
        if sensitivity:
            sr=[['Chênh lệch mục tiêu','Giả định discordance','Cặp độc lập (xấp xỉ)','Cặp sau design effect']]
            for row in sensitivity:sr.append([pct(100*row['minimum_difference']),str(row['discordance_assumption']),str(row['independent_pairs_normal_approx']),str(row['clustered_pairs_assuming_3_targets_per_project_ICC_0_1'])])
            args._statistics_appendix.append(simple_table(sr,table_template))
        args._statistics_appendix.append(add_paragraph('Sensitivity dùng xấp xỉ chuẩn cho outcome nhị phân ghép cặp, alpha hai phía 0,05, power mục tiêu 0,80. Discordance 0,25/0,50 và ICC 0,10 là giả định; design effect 1,20 khi ba target/project. Đây là yêu cầu kế hoạch, không phải cỡ mẫu đã đạt hoặc observed power. Bootstrap ba cụm có khoảng percentile kém hiệu chỉnh, chỉ mô tả; không dùng khoảng suy biến để khẳng định độ chắc chắn. Nguồn: '+str(statistics_path.relative_to(ROOT))+f'; SHA256 {digest(statistics_path)}.'))
    for title,path,explanation in [
        ('4.7. Phục hồi các node pass không sửa đổi',args.recovery_summary or args.summary.parent/'recovery_summary.json','Phân tích thứ cấp chọn các node đã pass trong v0, giữ nguyên nội dung kiểm thử và replay độc lập hai lần. Báo số suite không rỗng được phục hồi, retention và target-body reach riêng; đây không phải suite pass của tiêu chí chính và không thay đổi mẫu số 54 lượt.'),
        ('4.8. Mutation screen trên tập con được chọn',args.mutation_summary or args.summary.parent/'mutation_screen/summary.json','Mutation screen giới hạn ở target có suite thành công được chọn và matched giữa hai nhánh. Mẫu số mutant và suite của screen là tập con; không suy thành mutation score của toàn bộ 54 lượt hoặc của dự án mới nói chung.'),
        ('4.9. Thử nghiệm phát triển sau pilot',args.development_summary,'Các target đã được quan sát qua pilot nên đây là development, không là held-out xác nhận. Hai nhánh atomic_source và atomic_verified_setup dùng hai nhãn 45/46, không repair, giới hạn 2.048 output token và yêu cầu đúng ba hàm test. Probe runtime chỉ kiểm tra signature/kwargs/setup chung, không cung cấp giá trị kỳ vọng; probe pass không bảo đảm oracle đúng. Mọi lượt vẫn giữ trong mẫu số riêng của thử nghiệm này.')]:
        obj=load_record(path,provenance)
        if obj is None:continue
        p(title);p(explanation)
        if title.startswith('4.7'):
            rs=[['Nhánh','Đã phân tích / kế hoạch','Suite ổn định không rỗng','Node giữ / node gốc','Suite ổn định đạt target']]
            for arm,a in sorted(obj['arms'].items()):
                rs.append([arm,f"{a['completed_recovery_attempts']}/{a['planned_attempts']}",f"{a['recovery_has_stable_nonempty_tests']}/{a['planned_attempts']}",f"{a['stable_nodes']}/{a['original_generated_nodes']}",f"{a['stable_suite_target_reached']}/{a['planned_attempts']}"])
            table(rs)
            p('Các node chưa có evaluation hoặc chưa được replay không được coi là đã phục hồi. Mẫu số node retention phụ thuộc số node thực sự có sẵn; số suite dùng mẫu số kế hoạch 27/nhánh. Target-body reach được báo riêng vì suite pass/coverage mô-đun không tự chứng minh chạy thân target.')
        elif title.startswith('4.8'):
            ms=[['Nhánh','Scheduled mutants','Killed','Survived','Inconclusive']]
            for arm,a in sorted(obj['per_arm'].items()):ms.append([arm,str(a['denominator_including_inconclusive']),str(a['counts'].get('killed',0)),str(a['counts'].get('survived',0)),str(a['counts'].get('inconclusive',0))])
            table(ms)
            p('Mẫu số gồm toàn bộ scheduled mutant kể cả inconclusive. Chỉ lỗi assertion phù hợp mới quy killed; lỗi collection/import/setup/teardown, timeout hoặc thiếu node được giữ inconclusive. Không đồng nhất survived với equivalent. Screen dùng các node phục hồi không sửa đổi được chọn, không đại diện toàn bộ đầu ra generation.')
        elif title.startswith('4.9'):
            ds=[['Nhánh phát triển','Hoàn tất / kế hoạch','Đạt tiêu chí','SC module có penalty']]
            for arm,a in sorted(obj['arms'].items()):ds.append([arm,f"{a['completed']}/{a['planned']}",f"{a['passed']}/{a['planned']} ({pct(100*a['passed']/a['planned'])})",pct(a['penalized_module_line_pct'])])
            table(ds)
            da=obj['arms']['atomic_source'];db=obj['arms']['atomic_verified_setup']
            p(f"Chênh lệch verified-setup − source: {100*(db['passed']/db['planned']-da['passed']/da['planned']):+.2f} điểm phần trăm về tiêu chí chính và {db['penalized_module_line_pct']-da['penalized_module_line_pct']:+.2f} điểm phần trăm SC. Đây là tín hiệu phát triển sau quan sát pilot; không chứng minh hiệu quả trên target/project mới.")
        else:
            agg=compact_aggregates(obj)
            if agg:table([['Trường tổng hợp (nguồn JSON)','Giá trị']]+agg)
        p('Nguồn: '+str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)+f'; SHA256 {digest(path)}. Kết quả thăm dò không được diễn giải thành ưu thế xác nhận; không gộp với cohort chính.')
    confirmation=load_record(args.confirmation,provenance)
    if confirmation is not None:
        p('4.10. Đánh giá mở rộng sau khóa cấu hình')
        p('Đánh giá mở rộng được giữ như cohort riêng. Không gộp mẫu số với pilot hoặc development; tên nhánh, tiêu chí đạt và số hoàn tất dưới đây lấy từ summary thực tế. Target thuộc cùng project và lượt seed lặp vẫn có cấu trúc phụ thuộc, cần phân tích ở mức project; không tự coi số request là số đơn vị độc lập.')
        ca=confirmation.get('arms',{})
        if not isinstance(ca,dict) or not ca:raise ValueError('Confirmation summary must contain arms')
        cr=[['Nhánh','Kế hoạch','Hoàn tất','Đạt tiêu chí','SC có penalty']]
        for arm,a in sorted(ca.items()):
            n=a.get('planned'); done=a.get('completed'); passed=a.get('passed')
            if not isinstance(n,int) or n<=0 or not isinstance(done,int) or not isinstance(passed,int):raise ValueError('Confirmation missing denominators/counts')
            cr.append([arm,str(n),str(done),f'{passed}/{n} ({pct(100*passed/n)})',pct(a.get('penalized_module_line_pct',a.get('end_to_end_line_pct')))])
        table(cr)
        p('Các outcome chưa hoàn tất hoặc lỗi hạ tầng phải được phân biệt trong summary và giữ mẫu số kế hoạch; không chuyển sự cố không có đầu ra mô hình thành kết luận efficacy bằng 0. Không có đối chứng full upstream nên chưa khẳng định ưu thế so với Test4Py. Nguồn: '+str(args.confirmation.relative_to(ROOT) if args.confirmation.is_relative_to(ROOT) else args.confirmation)+f'; SHA256 {digest(args.confirmation)}.')
    return nodes


def main():
    global ORIGINAL
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original',type=Path,default=ORIGINAL)
    parser.add_argument('--summary',type=Path,default=ROOT/'research/groq_study_20261118_v2/summary.json')
    parser.add_argument('--recovery-summary',type=Path)
    parser.add_argument('--mutation-summary',type=Path)
    parser.add_argument('--statistics',type=Path)
    parser.add_argument('--confirmation',type=Path,default=ROOT/'research/groq_confirmation_20261118/summary.json')
    parser.add_argument('--development-summary',type=Path,default=ROOT/'research/groq_development_20261118/summary.json')
    parser.add_argument('--output',type=Path,default=ROOT/'reports/Tieu_Luan_CNPMTT_Council_SOTA_v2.docx')
    args=parser.parse_args()
    ORIGINAL=args.original.resolve()
    args.output=args.output.resolve()
    if not args.output.is_relative_to((ROOT/'reports').resolve()) or args.output==ORIGINAL.resolve():
        raise ValueError('Output must be a NEW file inside workspace reports/')
    if args.output.suffix!='.docx':raise ValueError('Output must have .docx suffix')
    before=digest(ORIGINAL)
    if before!=EXPECTED:raise ValueError('Original SHA256 differs from audited original; refusing edits')
    provenance={}
    for path in [AUDIT/'REVIEW.md',AUDIT/'paper_extracted.txt',AUDIT/'restored/rebuild_q3x04keb/validation.md']:
        provenance[str(path.relative_to(ROOT))]={'sha256':digest(path),'bytes':path.stat().st_size}
    restored=load_record(RESTORED,provenance)
    if not restored:raise ValueError('Restored summary required for evidence-derived tables')
    extracted=read_extraction(); edits=replacements(); edits.update(derived_replacements(restored))
    # Polished academic wording; detailed correction history belongs to the appendix/log.
    edits[379]='Trên sáu target đại diện, cấu hình đầy đủ pass 5/6 (83,33%) với SC phạt failure bằng 0 là 49,20%; pycg_classes chưa vượt qua kiểm tra MRO. Bảng 4.6 trình bày các cấu hình được tổng hợp từ evaluation gốc. Quy mô nhỏ và tuning trên tập phát triển không cho phép kết luận thành phần nào là điều kiện tiên quyết. Khi không preflight, SC đạt 57,88%; đây là quan sát mô tả trên sáu target, chưa tách được hiệu ứng nhân quả.'
    edits[434]='Mutation dùng bốn toán tử; SIR thay return expression bằng None. Nhãn kill chưa tách assertion failure khỏi collection/import/hạ tầng; cần original-pass check và log từng tiến trình để phân loại killed/survived/invalid/timeout/inconclusive. Chưa có hồ sơ đủ để định lượng equivalent mutants, FR hoặc tần suất taxonomy. Độ phủ cao không bảo đảm oracle đúng.'
    edits[449]='RQ3 | Ablation thăm dò trên sáu target | Full method pass 5/6 (83,33%); SC phạt failure bằng 0 = 49,20%. Kết quả chưa xác lập tác động nhân quả riêng cho từng thành phần.'
    edits[444]='Trên tập phát triển tuyển chọn, bảng sau tinh chỉnh cho thấy suite pass và coverage cao hơn baseline nội bộ. Tri thức thủ công, tuning và giới hạn provenance làm kết quả chưa xác lập ưu thế so với Test4Py upstream hoặc hiệu ứng riêng của AST. Nghiên cứu mới trên các dự án chưa dùng cục bộ được báo độc lập, giữ các kết quả bất lợi và không gộp vào bảng phát triển. Độ ổn định và chi phí chỉ được kết luận trong phạm vi ledger thực tế.'
    edits[460]='[5] G. Ryan, S. Jain, M. Shang, S. Wang, X. Ma, M. K. Ramanathan và B. Ray, “Code-Aware Prompting: A Study of Coverage-Guided Test Generation in Regression Setting Using LLM,” arXiv:2402.00097, 2024. https://arxiv.org/abs/2402.00097'
    edits[476]='[21] M. Tufano, D. Drain, A. Svyatkovskiy, Shao Kun Deng và N. Sundaresan, “Unit Test Case Generation with Transformers and Focal Context,” arXiv:2009.05617, 2020. https://arxiv.org/abs/2009.05617'
    edits[480]='[25] Wenhan Wang, Chenyuan Yang, Zhijie Wang, Yuheng Huang, Zhaoyang Chu, Da Song, Lingming Zhang, An Ran Chen và Lei Ma, “TestEval: Benchmarking Large Language Models for Test Case Generation,” Findings of NAACL 2025, tr. 3547–3562. https://aclanthology.org/2025.findings-naacl.197/'
    # Replace empirical image captions and their list entries consistently.
    for i in [168,348,350,377,398,415,431]:
        label=extracted[i].split('. ',1)[0]
        edits[i]=label+'. Hình cũ được thay bằng bảng và phân tích văn bản đã hiệu chỉnh'
    edits[227]='Hình 3.1. Kiến trúc ý tưởng; source context có curated hints, audit chưa là gate bắt buộc'
    edits[292]='Hình 3.2. Luồng ý tưởng; xem Thuật toán 3.2 cho repair thực tế trong giai đoạn phát triển'
    edits[97]=edits[321]; edits[98]=edits[351]; edits[99]=edits[362]; edits[103]=edits[402]; edits[104]=edits[423]
    edits[89]=edits[169]; edits[60]=edits[228]; edits[76]=edits[421]
    for list_id,body_id in [(107,168),(108,227),(109,292),(110,348),(111,350),(112,377),(113,398),(114,415),(115,431)]:edits[list_id]=edits[body_id]
    # Static TOC page numbers become invalid after substantive edits: keep text navigation, omit stale pages.
    for i in range(35,86):
        if extracted.get(i):edits.setdefault(i,re.sub(r'\d+$','',extracted[i]))
    mapping={norm(extracted[i]):(i,polished(v)) for i,v in edits.items()}
    changes=[];matched=set();removed_images=[]
    with zipfile.ZipFile(ORIGINAL) as z:
        raw=z.read('word/document.xml')
        # Preserve original prefixes, including ignorable extension namespaces.
        import io
        namespaces={}
        for _,pair in ET.iterparse(io.BytesIO(raw),events=['start-ns']):
            prefix,uri=pair;namespaces[prefix]=uri
            try:ET.register_namespace(prefix,uri)
            except ValueError:pass
        root=ET.fromstring(raw);body=root.find(q('body'));assert body is not None
        original_children=list(body)
        # Remove only charts identified by following captions; retain cover logos and conceptual diagrams.
        for idx,child in enumerate(original_children):
            if child.tag!=q('p') or not any(e.tag in {q('drawing'),q('pict')} for e in child.iter()):continue
            following=text_of(original_children[idx+1]) if idx+1<len(original_children) else ''
            if re.match(r'Hình (1\.1|4\.[1-6])\.',following):
                removed_images.append(following)
                rewrite(child,'Hình định lượng của phiên bản trước được rút để tránh lặp lại dữ liệu hoặc phép so sánh không cùng cohort. Kết quả hiện hành nằm ở bảng và đoạn phân tích tương ứng.')
        # Exact paragraph/table-row matching prevents accidental replacement inside unrelated text.
        for child in list(body):
            if child.tag==q('p'):
                old=text_of(child);key=norm(old)
                if key in {norm(extracted[478]),norm(extracted[479])}:
                    body.remove(child);changes.append({'extracted_line':478 if key==norm(extracted[478]) else 479,'kind':'removed_unverified_reference','before':old,'after':None});continue
                if key in mapping:
                    line,new=mapping[key];rewrite(child,new);matched.add(key)
                    changes.append({'extracted_line':line,'kind':'paragraph','before':old,'after':new})
            elif child.tag==q('tbl'):
                for row in child.findall(q('tr')):
                    cells=row.findall(q('tc'));old=' | '.join(text_of(c) for c in cells);key=norm(old)
                    if key not in mapping:continue
                    line,new=mapping[key];values=new.split(' | ')
                    if len(values)!=len(cells):raise ValueError(f'Table column mismatch line {line}: {len(values)} vs {len(cells)}')
                    for cell,value in zip(cells,values):
                        ps=cell.findall(q('p'))
                        for p in ps[1:]:cell.remove(p)
                        rewrite(ps[0] if ps else ET.SubElement(cell,q('p')),value)
                    matched.add(key);changes.append({'extracted_line':line,'kind':'table_row','before':old,'after':new})
        missing=[i for i in edits if norm(extracted[i]) not in matched and i not in [478,479]]
        if missing:raise ValueError(f'Unmatched mandatory replacements: {missing}')
        # Clean citations to removed, unverified entries in otherwise untouched paragraphs.
        for p in body.iter(q('p')):
            value=text_of(p)
            if re.search(r'\[(?:23|24)\]',value):
                new=re.sub(r'\s*\[(?:23|24)\]','',value);rewrite(p,new);changes.append({'kind':'removed_unverified_citation','before':value,'after':new})
        template=body.find(q('tbl'))
        section=experiment_section(args,template,provenance)
        ch5=next(c for c in reversed(list(body)) if c.tag==q('p') and text_of(c).startswith('CHƯƠNG 5.'))
        position=list(body).index(ch5)
        for node in section:body.insert(position,node);position+=1
        appendix=[add_paragraph('PHỤ LỤC. NGUỒN DỮ LIỆU VÀ KHẢ NĂNG TÁI LẬP'),add_paragraph('Bản v2 được tạo từ bản gốc bất biến bằng scripts/revise_council_docx_v2.py. Thay đổi học thuật gồm tách cohort, mô tả đúng curated hints và repair, phục hồi ablation, định danh nguồn golden và sửa metadata tài liệu tham khảo. Nhật ký JSON/Markdown đi kèm ghi từng đoạn/hàng trước và sau; không chỉnh source thực nghiệm hoặc bản gốc. Các hình định lượng cũ được rút; sơ đồ kiến trúc giữ như ý tưởng với giới hạn được chú thích.')]
        appendix.append(add_paragraph('Giới hạn dữ liệu phục hồi: SOTA gốc có 103/105 evaluation được đối chiếu, sau tinh chỉnh 104/105; các hàng còn lại chỉ có outcome CSV. Baseline đối chiếu 99/105, Standard 104/105. Summary giữ missingness theo trường; line coverage có thể lấy từ CSV fallback và không đồng nhất với đầy đủ log đo. Repair attribution có trường hợp thiếu evaluation ban đầu. Không coi thiếu hồ sơ là đã xác nhận thất bại hoặc thành công độc lập.'))
        appendix.extend(getattr(args,'_statistics_appendix',[]))
        for path,meta in provenance.items():appendix.append(add_paragraph(path+' — SHA256 '+meta['sha256']))
        appendix.append(add_paragraph('SHA256 bản gốc: '+before+'. Bản gốc được kiểm tra trước và sau khi dựng; không ghi vào Downloads. Trang mục lục cũ được bỏ để tránh số trang không còn đúng; cần cập nhật mục lục và kiểm tra bố cục bằng Word/LibreOffice trước khi nộp.'))
        sec=body.find(q('sectPr'));pos=list(body).index(sec) if sec is not None else len(body)
        for node in appendix:body.insert(pos,node);pos+=1
        xml=ET.tostring(root,encoding='utf-8',xml_declaration=True)
        # ElementTree may drop xmlns declarations used only in mc:Ignorable, not element names.
        for prefix,uri in namespaces.items():
            if prefix and f'xmlns:{prefix}='.encode() not in xml:
                xml=xml.replace(b'<w:document ',f'<w:document xmlns:{prefix}="{uri}" '.encode(),1)
        ET.fromstring(xml)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        # Copy ORIGINAL first, then edit the copy only. Stage atomically inside reports/.
        with tempfile.TemporaryDirectory(prefix='council-v2-',dir=args.output.parent) as td:
            copied=Path(td)/'original-copy.docx';shutil.copy2(ORIGINAL,copied)
            if digest(copied)!=before:raise ValueError('Copy hash verification failed')
            built=Path(td)/'revised.docx'
            with zipfile.ZipFile(copied) as source,zipfile.ZipFile(built,'w') as dest:
                for info in source.infolist():dest.writestr(info,xml if info.filename=='word/document.xml' else source.read(info.filename))
            with zipfile.ZipFile(built) as check:
                assert check.testzip() is None
                for name in check.namelist():
                    if name.endswith('.xml'):ET.fromstring(check.read(name))
                for name in z.namelist():
                    if name!='word/document.xml':assert check.read(name)==z.read(name),name
            if digest(ORIGINAL)!=before:raise ValueError('Original changed during build')
            built.replace(args.output)
    log={'status':'draft_requires_layout_review','source':str(ORIGINAL),'source_sha256_before':before,'source_sha256_after':digest(ORIGINAL),'original_unchanged':digest(ORIGINAL)==before,'output':str(args.output),'output_sha256':digest(args.output),'script_sha256':digest(Path(__file__)),'inputs':provenance,'changes':changes,'removed_chart_captions':removed_images,'new_section_paragraphs':len(section),'notes':['All package parts except word/document.xml preserved byte-for-byte.','Paragraph/run style and table/cell properties retained where feasible; replaced paragraphs use first run formatting.','Removed chart media remain unreferenced package assets; visible drawings removed.','No PDF/layout validation performed by this script.','References 23/24 and their citations removed; other numbers kept stable.']}
    logpath=args.output.with_suffix('.changes.json');logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
    md=['# Nhật ký hiệu chỉnh bản v2','',f'Bản gốc không đổi: `{before}`.',f'Đầu ra: `{args.output.name}`.',f'{len(changes)} thay đổi đoạn/hàng; {len(removed_images)} hình định lượng được rút.','', '## Nguồn bằng chứng','']
    md += [f'- `{k}`: SHA256 `{v["sha256"]}`' for k,v in provenance.items()]
    md+=['','## Thay đổi chi tiết','']
    for item in changes:md += [f'### Dòng trích {item.get("extracted_line", "—")} — {item["kind"]}','','Trước: '+item['before'],'','Sau: '+(item['after'] or '(rút mục chưa đủ nguồn)'), '']
    md+=['## Giới hạn trình bày','','Chưa kiểm tra PDF. Font, page breaks và mục lục cần kiểm tra bằng trình soạn thảo Word. Nội dung gói ngoài document.xml được giữ nguyên; style run đầu được giữ cho đoạn thay thế.']
    args.output.with_suffix('.changes.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({k:log[k] for k in ['status','output','output_sha256','original_unchanged']},ensure_ascii=False))
    print(f'Changes: {len(changes)}; removed charts: {len(removed_images)}; supplemental nodes: {len(section)}')

if __name__=='__main__':main()
