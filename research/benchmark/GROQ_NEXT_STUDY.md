**Kế hoạch phát triển và đánh giá tiếp theo — ngân sách Groq tối đa 2 USD**

Trạng thái: đã lập inventory offline; chưa gọi API, chưa khóa tập đánh giá,
chưa có kết quả cải tiến mới. Không cam kết hiệu quả trước khi đo.

Nguồn chính: [Test4Py upstream](https://github.com/Test4DT/Test4Py), frame
`projects-upstream.json` đang có trong dự án. Inventory được tạo bằng
`python3 scripts/plan_groq_benchmark.py --output PATH_MOI.json`.
Script không đọc outcome/coverage để chọn module, không import subject, không
cài dependency và không gọi mạng/API. File đầu ra mới được tạo độc quyền,
không ghi đè inventory cũ.

Kết quả inventory đầu tiên: 584 định danh public cấp module trong 10 repo local;
106 module thuộc 13 project upstream chưa bị đánh dấu phơi nhiễm bởi quy tắc
hiện tại. Đây là **ứng viên**, chưa phải 106 module chạy được hoặc held-out đã
xác nhận. Quy tắc bảo thủ: mọi repo local và project trong các manifest API cũ
được coi là development. Cần rà lịch sử các chiến dịch còn lại trước khi xác
nhận project mới; không suy chưa có checkout đồng nghĩa chưa từng dùng.

**Công việc trước Groq**

1. Khôi phục bảng ablation từ raw, dựng lại metadata original/refined và
   attribution repair; giữ nguyên các artifact cũ.
2. Sửa runner: audit là gate thực sự; raw prompt/completion/usage mọi request;
   không gọi tên seed inference nếu API không dùng seed; không thay đổi oracle
   chỉ để pass; lưu lý do fail, timeout và missingness.
3. Xác minh source SHA, license, thay đổi local; preflight import/dependency
   riêng theo project. Module lỗi vẫn nằm trong inventory, có lý do; mọi loại
   trừ phải dựa trên điều kiện kỹ thuật công khai trước khi xem điểm mô hình.
4. Chọn tập development đa dạng từ inventory; chỉ dùng tập này để sửa prompt
   và thử cấu hình. Nêu rõ đây là quá trình tìm kiếm theo kết quả, không dùng
   điểm thắng trên development làm bằng chứng xác nhận.

**Thiết kế chạy sau khi runner sẵn sàng**

- Phân bổ trần chi phí: development 0,50 USD; đánh giá khóa 1,20 USD;
  dự phòng request thất bại/retry 0,30 USD. Tổng không vượt 2,00 USD theo
  accounting bảo thủ. Xác minh biểu giá/model hiện hành trước chạy; lưu
  biểu giá và cả chi phí ước tính lẫn usage nhà cung cấp.
- Trước mỗi request, dự trù cận trên chi phí input + output cap, gồm repair
  và retry. Không đủ phần ngân sách còn lại thì dừng trước request; không
  chỉ kiểm tra sau khi đã phát sinh chi phí. Lưu usage cả response bị cắt.
- Hai arm chính: source-only và cải tiến đã khóa, cùng model, token budget,
  repair budget, timeout, điều kiện thực thi. Đảo thứ tự arm cân bằng.
  Nếu thêm Standard, chia lại số lượt trước chạy; không lấy ngân sách thêm
  ngầm. Baseline nội bộ không được ghi thành Test4Py upstream.
- Khóa project/target, SHA source/runner, prompt, số lần lặp, thứ tự,
  outcomes, exclusions và stopping rule trong manifest trước evaluation.
  Chọn số target/lượt dựa trên ước tính token development, không dựa trên
  p-value mong muốn. Không tự mở rộng hoặc thay target để đạt kết quả đẹp.
- Chia tập theo **project**; ưu tiên các project mới xác nhận chưa tuning.
  Chỉ mở kết quả tập đánh giá sau khóa cấu hình. Nếu dùng kết quả đó để sửa,
  tập ấy trở thành development cho vòng tiếp theo.
- Primary outcome: suite all-pass và replay ổn định trên tất cả planned
  attempts. Secondary: target/module line/branch counts, latency toàn lượt,
  token/cost, review assertion và mutation có kiểm tra original-pass.
  NA khác measured zero; báo rõ penalty end-to-end nếu dùng.
- Mutation trên đầu ra từng arm và cùng pool; không thay bằng golden chọn
  từ nhiều arm. Tách assertion kill, invalid/import, timeout, inconclusive.
- Giữ mọi thất bại và raw revision; báo effect ghép cặp, bất định và cụm
  project. Một chiến dịch nhỏ trong 2 USD có thể chỉ đủ pilot thăm dò.

**Benchmark bổ sung**

[EvalPlus](https://github.com/evalplus/evalplus) / HumanEval+ / MBPP+ có thể
làm kiểm tra phụ cho hàm thuần, nhưng là benchmark code generation gốc;
dùng cho test generation là adaptation phải mô tả riêng. Không thay thế
benchmark module thực tế khi luận điểm tập trung vào import, receiver state
và dependency. Không chọn dataset vì đã thấy điểm cao rồi trình bày như
đánh giá độc lập. Ưu tiên mở rộng đúng frame Test4Py trước để giữ liên hệ
với câu hỏi nghiên cứu hiện tại.

Tiêu chí hoàn tất: dữ liệu truy nguyên được và kết luận theo effect quan sát,
kể cả không cải thiện. Chỉ gọi “cải tiến được xác nhận” nếu đối chứng đã khóa
thực sự hỗ trợ; không bảo đảm kết quả dương bằng tuyển chọn đầu ra.
