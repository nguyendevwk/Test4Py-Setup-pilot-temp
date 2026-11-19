# Đánh giá cùng điều kiện và tiêu chí cải tiến thực sự

Cập nhật: 2026-11-17. Đây là đối chiếu artifact hiện có và protocol cho cohort
tiếp theo; **chưa khởi chạy một thực nghiệm GPU mới**.

## 1. Hai phép so sánh cần phân biệt

Phép so sánh phương pháp chính: Test4Py upstream và bản cải tiến chạy trên cùng
SLM, cùng source và cùng ngân sách. Bản gốc được ghim tại commit
`3c8b45410545183a9a579a784ffefae722a158a6`; runtime adapters chung phải được
công khai. Chỉ thay phần cải tiến đang kiểm chứng.

Đối chiếu paper là phép so sánh riêng. Paper dùng GPT-4o mặc định, ba vòng sinh
test và BGE-large/Chroma. Chạy Qwen14B một vòng trên hai module không tương đương
cấu hình đó. Temperature/top-p/token caps của nghiên cứu gốc chưa được xác minh
đầy đủ; không gán cấu hình local thành cấu hình paper. Nguồn:
[paper, experimental setup](https://arxiv.org/html/2503.14000v2#S4).

Code upstream yêu cầu sinh một **pytest test case file** và nhắc nhiều test
cases. Không có cơ sở từ đoạn code này để bắt buộc file chỉ được chứa đúng một
hàm `test_*`. Vì vậy `single-test-v1` là ràng buộc bổ sung của experiment đã
thất bại, không phải điều kiện chung được mặc định gán cho paper.

## 2. Tham số chạy phải giữ chung

| Nhóm | Điều kiện đối chứng |
|---|---|
| Model | Cùng model và immutable revision cho mọi role; 14B và 7B thành hai block riêng |
| Runtime | Cùng NF4, attention policy, Torch/Transformers, dtype và loại GPU |
| Source | Cùng project/module/function scope, commit, dependencies và production hashes |
| Sampling | Cùng seed ghép cặp, temperature, top-p và chính sách greedy initialization |
| Token | Cùng input/output caps và kiểm tra overflow; không cắt ngầm |
| Generation | Cùng số vòng, giới hạn repair và stopping rule; ghi actual test/node count |
| Retrieval | Cùng embedding/revision và nguồn production; phần grounding bổ sung là treatment được ghi riêng |
| Cache | Cùng điều kiện cold/warm; chỉ tái dùng initialization hợp lệ, không tái dùng generation/outcomes |
| Acceptance/scoring | Cùng định nghĩa collection, pass, source integrity, oracle review, retention và fault verdict |
| Cost | Cùng worker timeout và cách tính ngân sách; cân bằng thứ tự/GPU khi so timing |

Budget giống nhau không có nghĩa actual cost giống nhau: số call/token do repair
phải được đo như một kết quả. Input dài hơn do grounding cũng là chi phí cần báo.
Số vòng không phải số mẫu độc lập; nhiều seed cùng project vẫn là dữ liệu cụm.

Artifact hiện tại xác nhận **17 trường cấu hình tính toán giống nhau**:
Qwen2.5-Coder-14B cùng revision, NF4, attention policy, 4096 input/512 output,
seed42, temperature0.7, top-p0.95, một vòng, BGE cùng revision, source scope và
các giới hạn liên quan. Xem `artifacts/matched_parameter_evaluation_20261117.json`.

Điểm còn khác giữa hai arm gồm grounding, repair prompt/import handling và gate
bảo toàn assertion. Kết quả hiện tại là đối chiếu **toàn bộ hai pipeline**, chưa
tách được hiệu ứng riêng của grounding khỏi gate. Cohort đo grounding phải dùng
cùng acceptance policy; tác động của gate chặt hơn là contrast/ablation riêng.
Giữ nguyên cách chạy/reduction upstream để quan sát, nhưng chấm đầu ra cả hai
arm bằng cùng tiêu chuẩn ngoài. Báo riêng trước repair, sau repair và sau reduction.

## 3. Chỉ số chung và chỉ số bổ sung

| Chỉ số | Quy tắc chấm |
|---|---|
| Line/branch coverage | Báo tử/mẫu số theo cùng module, tool version và coverage scope; 0/0 là NA |
| Type inference | Exact/relaxed match chỉ khi có cùng ground truth được xác minh; hiện chưa có bộ nhãn phù hợp |
| First-pass/final pass | Tách candidate trước repair và suite cuối; collection error không phải một test thất bại |
| Assertion correctness | Review độc lập theo source/spec; báo số đúng/số đã review, chưa review để NA |
| API hallucination | Nhãn lỗi có định nghĩa và mẫu số; không suy trực tiếp từ AttributeError hay pytest fail |
| Fault detection | Cùng pool khóa trước; phân biệt killed/survived/inconclusive, review tương đương mutant |
| Stability | Replay cùng node set trong process mới; không gọi replay là lượt sinh model độc lập |
| Repair/retention | Số test/check bị đổi hoặc bỏ, lỗi được cứu, proposal bị từ chối và lý do |
| Latency | Tách load, cold/warm initialization, generation/repair, scoring và chạy lại test |
| Compute | Fresh/logical tokens, model calls, peak VRAM/RSS, timeout/OOM và download/setup |

Các tham số bổ sung để khảo sát sau readiness: model7B/14B, một/ba vòng,
output512/1024 và ngân sách context. Đổi từng yếu tố hoặc dùng thiết kế ablation
có mục tiêu; không mở tích Descartes mọi cấu hình. Thay model/budget thì cần
calibration tương ứng. Không tái dùng initialization14B để tuyên bố một pipeline7B.

## 4. Đối chiếu số liệu đã có

| Chỉ số | Upstream baseline14B | Improved14B |
|---|---:|---:|
| Module-trials hoàn tất/planned | 2/2 | 2/2 |
| Module có retained suite all-pass | 2/2 | 0/2 |
| Retained test nodes pass | 20 | 0 |
| Module đo được coverage | 2/2 | 0/2 |
| Line coverage mean, có điều kiện đo được | 95% | NA |
| Project worker time, warm initialization | 1655,64s | 2047,67s |
| Generation/repair phase | 1358,79s | 1752,96s |
| Fresh model calls | 37 | 47 |
| Generation/repair output tokens | 11069 | 13695 |
| Candidate-output failures | 4 | 3 |
| Upstream-accepted repair bị preservation gate loại | 0 | 3 |

Đây là số liệu của cohort một vòng đã hoàn tất, không trộn với screen định dạng
dừng sớm hoặc bộ12test tuyển chọn. Cost là số đo mô tả một project/hai GPU;
không phải ước lượng hiệu ứng timing suy rộng. Không lấy95% trừ NA thành95 điểm.
Một mutant bị baseline phát hiện chưa đủ đánh giá fault detection rộng.

## 5. Khi nào được kết luận thực sự tốt hơn?

Mục tiêu chất lượng chính cho cohort xác nhận là **phát hiện lỗi hợp lệ** trên
pool/lỗi thật được khóa và review trước inference; branch coverage là chỉ số hỗ
trợ. Assertion phải đúng theo source/spec và được chấm cùng tiêu chuẩn hai arm.
Nếu chưa có pool đủ chất lượng, kết luận này phải chờ; coverage không thay thế nó.

Chỉ kết luận cải tiến khi lợi ích ghép cặp còn tồn tại trên các module/project
được chọn trước, với cùng cấu hình/ngân sách và không đổi oracle hay bỏ failures.
Báo cả trường hợp giảm chất lượng, tỷ lệ hoàn tất, effect size và bất định theo
project. Pilot nhỏ chỉ cho tín hiệu mô tả; không cam kết p-value hay suy rộng
từ một project. Ngưỡng lợi ích thực tế và thiết kế xác nhận phải khóa trước khi
chạy cohort xác nhận, không chọn sau khi nhìn điểm.

- Chất lượng tăng nhưng assertion yếu/sai hoặc lỗi bị bỏ: không đạt.
- Coverage tăng nhưng chưa có fault evidence: chỉ kết luận đúng mức coverage.
- Chất lượng ngang và chi phí giảm: có thể là cải tiến hiệu suất, chưa phải chất lượng test tốt hơn.
- Subset được chọn vì kết quả đẹp: chỉ dùng cho demo ứng dụng, không chứng minh hơn paper.
- Kết quả không thuận lợi: giữ nguyên và sửa nguyên nhân; không chọn lại seed để thắng.

**Trạng thái hiện tại: chưa đạt bằng chứng cải tiến thực sự.** Chưa mở full.
Cần sửa vấn đề đã quan sát, qua smoke đúng cấu trúc đầu ra, rồi mới làm pilot
đối chứng chung. Ba vòng theo hướng paper chỉ chạy khi runtime đã khả thi;
thay một vòng thành ba vòng mà không kiểm tra chi phí có thể lại gây timeout.
