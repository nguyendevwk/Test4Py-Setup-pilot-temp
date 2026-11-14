> Báo cáo này mô tả source **trước sửa**. Các lỗi metric và luồng Council đã được
> xử lý trong phiên bản v2; xem [hướng dẫn chạy lại](../docs/COUNCIL_V2.md).
> `audit_reproduce.py` hiện chạy regression tests cho hành vi sau sửa, không còn
> yêu cầu các lỗi cũ phải tái xuất hiện. Giới hạn một target, adapter riêng và hai
> mutant vẫn tồn tại và phải được công khai.

# Kiểm định tính liêm chính và công bằng thực nghiệm

Phạm vi: source Python, cấu hình, tests và tài liệu trong checkout hiện tại. Đây là audit source, không phải tái lập kết quả GPU. Không có artifact Kaggle gốc của các lượt được sổ tay mô tả trong cây file đã kiểm tra; vì vậy không xác nhận được các số 5/5, 10/10, 0/7 hay thời gian chạy. Không xác minh độc lập các phát biểu về paper bên ngoài. Không sửa logic thực nghiệm.

## Nhận định reviewer

Có lỗi code xác định được làm sai ý nghĩa metric và có các phát biểu nghiên cứu vượt bằng chứng. Chưa có cơ sở kết luận tác giả cố tình gian lận hoặc bịa số. Tuy nhiên, bảng Council/ablation hiện chưa đủ tin cậy để dùng làm bằng chứng phương pháp vượt Test4Py hoặc có khả năng tổng quát. Cần phân biệt lỗi đo lường, thiết kế thiên lệch và hành vi gian lận có chủ ý.

Các phát hiện dưới đây có phạm vi khác nhau: lỗi Council không tự động áp dụng cho pipeline `worker.py`; `analyze.py` và protocol cũ đã có nhiều biện pháp thận trọng hơn.

## Phát hiện ưu tiên

### F1 — Cao: “Suite Pass Rate” thực tế là có ít nhất một test pass

Bằng chứng: `council/runner.py:153-173` gán `status='passed'` và tăng `passed_samples` chỉ dựa vào `score_res['passed'] > 0`. `pilot/scoring.py:136-141` định nghĩa `passed` là số node pass, không phải toàn suite thành công. `ablation_runner.py:74-85` đặt tên tỷ lệ này là Suite Pass Rate.

Một suite có 1 pass và 99 fail vẫn có thể được tính là sample thành công. Runner cũng không kiểm tra `score_res['status']`: score bị `unstable_original` vẫn có thể hiện passed. Đây là lỗi xác nhận được bằng harness tổng hợp, không phải kết quả LLM thực.

Khắc phục: tách `any_passing_tests`, `suite_all_pass`, `scoring_complete`, first-pass và final-pass; suite pass phải xét process hoàn tất, lỗi collection/setup/teardown và toàn bộ kết quả cần thiết. Giữ outcome chất lượng tách biệt lỗi hạ tầng.

### F2 — Cao: 0% coverage bị biến thành thiếu dữ liệu, sau đó bị loại khỏi trung bình

Bằng chứng: `council/runner.py:151` có điều kiện `if tot_branches and branch_cov else None`. Khi covered=0 và total=10, kết quả đúng là 0%, code trả `None`. `ablation_runner.py:97-98` bỏ `None` khỏi trung bình.

Hệ quả định lượng: nếu hai sample thực sự có 0% và 80%, bảng có thể hiện 80% thay vì trung bình 40%. Chỉ thay 0 thành NA là lỗi; NA do môi trường thật không nên tự động thay thành 0.

Khắc phục: kiểm tra `covered is not None` và `total > 0`, giữ 0 hợp lệ; báo mẫu số metric, số NA và lý do.

### F3 — Cao: mock có thể đi vào cùng hệ thống báo cáo với chạy thật

Bằng chứng: `council/engine.py:99-103,129-133` trả test `assert True` ở mock. `council/runner.py:167-178` không lưu `mock` trong summary. `ablation_runner.py:58-66` đọc đệ quy mọi `summary.json`, không phân loại mock/real hoặc kiểm tra schema/cohort.

Một lượt mock có thể báo sample passed dù không kiểm tra target; bảng tổng hợp không có cột nhận biết. Đây là khả năng trộn dữ liệu do thiết kế, chưa phải bằng chứng dữ liệu đã bị trộn.

Khắc phục: bắt buộc `run_kind`, `mock`, cấu hình và schema; tách mock artifacts, từ chối tổng hợp chúng vào bảng efficacy. Giữ mock cho kiểm tra hạ tầng.

### F4 — Cao: baseline Council không phải thực thi source gốc Test4Py

Bằng chứng: `council/runner.py:82-99` ở baseline chỉ bỏ setup rồi vẫn gọi generator Council. Cả baseline vẫn dùng nguồn `source_context`, prompt Council và có thể Critic. Không có bước upstream `ProjectMessage.init`, inference/retrieval và generation upstream trong runner này. Pipeline upstream có ở `worker.py` và `benchmark_worker.py`.

`SO_TAY_NGHIEN_CUU.md` phần 7.1 gắn nhãn “SOURCE GỐC (TEST4PY) VS CẢI TIẾN”. Nếu lấy baseline từ Council để điền cột đó thì sai nhận diện đối chứng. Nếu các số đến từ lượt upstream riêng, cần artifact và cấu hình chứng minh; source hiện không cung cấp chúng.

Khắc phục: đặt tên đúng “Council không setup”; chạy đối chứng Test4Py upstream riêng với cùng model/revision và công khai prompt, repair, budget, source scope. Cùng model và GPU chưa đủ tạo so sánh công bằng.

### F5 — Cao: kiến thức thủ công về target trùng trực tiếp hành vi mutant cần phát hiện

Bằng chứng: `council/generator.py:17-23`, `council/critic.py:89-94` cung cấp sẵn cách gọi closure, chuyển absolute path, điều kiện chỉ set filepath khi destination chưa có. Hai mutant trong `pilot/scoring.py:25-71` chính là sai filepath mới và ghi đè filepath cũ. `pilot/setup.py:47-65` và `pilot/probe.py` dùng API/literal/tiền điều kiện viết riêng cho PyCG.

Đọc implementation để sinh assertion là hợp lệ trong white-box testing. Vấn đề ở đây là người thiết kế đã mã hóa thủ công đúng hành vi chấm điểm, trên đúng target dùng đánh giá. Sổ tay phần 4 cũng mô tả sửa prompt sau khi thấy lỗi path. Đây là target tuning cần công khai; không tự chứng minh extraction tự động hoặc generalization. Không phát hiện đường đọc trực tiếp probe observation/oracle nội bộ vào prompt ở các đường code đã kiểm tra.

Khắc phục: gọi đây là development case study; khóa prompt/adapter/mutant pool trước đánh giá tiếp; dùng held-out projects và mutation operators đa dạng, tránh thêm rule theo kết quả test set. Công bố cả kết quả trước và sau tuning, không gộp thành cohort đồng nhất.

### F6 — Cao: lặp greedy một hàm bị diễn giải là các thực nghiệm độc lập

Bằng chứng: `council/runner.py:68-99` lặp cùng target và prompt; `council/engine.py:112-117,142-147` dùng `do_sample=False`. Sổ tay phần 5 gọi nhiều lần chạy là độc lập/quy mô lớn và suy từ sigma=0 ra ổn định tuyệt đối; phần 6 kết luận Fixture Architect không thể thay thế.

Lặp cùng hàm có thể đánh giá một phần độ lặp lại trong môi trường đó. Nó không tăng số target độc lập, không chứng minh ổn định tuyệt đối, và không xác lập tính cần thiết trên các project khác. Không có suy luận thống kê phù hợp từ số lượng sample này sang quần thể hàm Python.

Khắc phục: báo `independent_targets=1`; mô tả số lượt lặp và điều kiện; lấy target/project độc lập cho xác nhận. Protocol cũ `research/protocol.json` đã ghi rõ giới hạn này.

### F7 — Vừa: repair bỏ qua suite thất bại một phần và không thực thi bảo toàn assertion

Bằng chứng: `council/runner.py:123` chỉ gọi Critic khi không có node nào pass và AST hợp lệ. Suite mixed pass/fail không được repair. `:138` gọi repair thành công ngay khi có một node pass. Sau repair, không audit lại assertion/target reach; summary vẫn giữ audit của bản v1. Prompt “PRESERVE INTENT” trong critic chỉ là chỉ dẫn, không phải bộ kiểm tra.

Hệ quả: kết quả có thể che mất assertion bị bỏ/yếu đi; thí nghiệm cũng chưa đo lợi ích Critic đầy đủ. Sổ tay nói zero Critic calls không chứng minh thành phần Critic tạo ra cải thiện.

Khắc phục: định nghĩa eligibility và budget repair trước; ghi lỗi từng node, audit diff assertion và bản cuối, báo original/final riêng. Thêm đối chứng cùng coder tự repair với budget tương đương để tách lợi ích model thứ hai khỏi thêm lượt inference.

### F8 — Vừa: “semantic assertion” thực tế chỉ đếm cú pháp

Bằng chứng: `council/critic.py:48-74` đếm mọi AST Assert trong file. `assert True` được coi `is_hollow=False`, được tests hiện tại chấp nhận (`tests/test_council.py`). Runner chỉ in audit, không dùng nó để yêu cầu target reach hoặc tính hữu ích.

Khắc phục: đặt tên syntactic assertion count; audit nonvacuity, reach target/nested loader và observable behavior riêng. Không loại mọi test không dùng AST Assert: `pytest.raises`/unittest assertion cũng có thể hợp lệ.

### F9 — Vừa: báo trung bình có điều kiện mà không nêu mẫu số metric

Bằng chứng: `ablation_runner.py:97-104` bỏ thiếu cả coverage và mutation, không ghi n có điểm; chỉ có tổng sample. Compiler còn bỏ qua JSON lỗi hoàn toàn (`:65-66`) và không kiểm tra target/revision/mutant pool/config compatibility.

Ví dụ tổng hợp đã tái hiện: 2 sample, chỉ 1 có điểm 80%/1.0, bảng ghi Avg Branch=80% và Avg Mutation=1.00 mà không ghi n=1 cho metric. Trung bình complete-case có thể dùng nếu nêu rõ; không được hiểu là end-to-end quality của mọi lượt. Bất lợi/thuận lợi phụ thuộc cơ chế missingness.

Khắc phục: báo planned/started/finished/scored, phân loại lỗi, mẫu số từng metric và outcome end-to-end; kiểm tra cohort/schema/hash trước pooling. Tệp lỗi phải tạo audit warning, không biến mất.

### F10 — Vừa: coverage toàn module và hai mutant không đo chất lượng tổng quát của target

Bằng chứng: `council/runner.py:148` chỉ lấy `branch_coverage['module']`. `pilot/scoring.py` lưu functions riêng nhưng bảng Council không dùng. Mutation score có đúng hai mutant filepath nên chỉ có 0, 0.5, 1 khi chấm đầy đủ.

Khắc phục: ghi rõ “module branch coverage”, thêm target+nested coverage với mẫu số cụ thể; báo killed/total=2/2 và nguồn pool. Không diễn giải 1.0 thành 100% khả năng phát hiện lỗi nói chung. Hai scenario và hai mutant không phải các project độc lập.

### F11 — Vừa: Council thiếu provenance và dữ liệu chi phí cần cho tuyên bố tái lập/công bằng

Bằng chứng: `council/engine.py` gọi from_pretrained không ghim revision; summary không lưu resolved revisions, seed, source hashes, môi trường, prompt/output thô hay input tokens. Telemetry chỉ đếm output tokens và thời gian inference. `ablation_runner.py` luôn chạy variants theo cùng thứ tự. Các lỗi ngoài dự kiến có thể dừng loop trước khi ghi summary cuối vì runner không có try/finally cho từng sample.

Khắc phục: manifest bất biến, snapshot prompt/raw completion, stage costs gồm probe và model load, input/output tokens, trạng thái từng attempt ngay khi bắt đầu và kết thúc; counterbalance thứ tự nếu so tốc độ. Đánh giá no-critic cần ghi rõ vẫn nạp Critic trong engine, nên tổng thời gian/VRAM hiện không phản ánh một triển khai coder-only tối ưu.

### F12 — Vừa: extracted control yếu, chưa tách đầy đủ lợi ích verification

Bằng chứng: `pilot/setup.py:56` đặt constructor-only đầu danh sách; `:112-114` extracted lấy ứng viên đầu mỗi scenario. Verified tìm đến chuỗi phù hợp. Hai bên giữ pool/order là điểm tốt, nhưng đối chứng không dùng ranking cấu trúc mạnh và nhận lượng setup khác nhau. Council ablation còn không chạy extracted/caller.

Khắc phục: giữ control này để mô tả, thêm static ranking không thực thi và đối chứng có cùng setup được chọn khi phù hợp; báo prompt tokens và chi phí search. Không suy mọi lợi ích của thêm setup thành riêng lợi ích runtime verification.

## Các biện pháp tốt đã có

- `pilot/common.py` ghim target/upstream commit và tạo output mới, giữ lượt chạy cũ.
- `pilot/scoring.py` chỉ chấm mutant bằng node pass trên original, replay chúng trước, lưu source/hash pool; mutant inconclusive không tự biến mất khỏi mẫu số điểm của từng lượt.
- Bộ chấm tách lỗi import/setup/timeout ở mutant; vẫn là attribution heuristic, cần audit raw traceback cho claim fault detection mạnh.
- `pilot/validate.py` chứa oracle hạ tầng riêng; các worker đã kiểm tra không import oracle đó làm generated tests.
- `pilot/setup.py` có lọc file test theo tên/đường dẫn và công khai adapter PyCG. Đây không phải chứng nhận không có mọi dạng retrieval leakage hay pretraining contamination.
- `research/protocol.json`, `research/REVIEW.md`, `research/QUALITY_FIRST.md` và `analyze.py` đã ghi nhiều giới hạn đúng; Council và sổ tay chưa tuân theo đầy đủ.

## Tái hiện và giới hạn

Chạy `python3 -m research.audit_reproduce`: đã hoàn tất thành công. Harness dùng input tổng hợp và mock I/O có chủ đích, không tải repo/model và không tạo số thực nghiệm efficacy. Nó xác nhận mixed suite bị gọi passed, score unstable không ngăn passed, partial failure không được Critic sửa, 0 coverage thành null, thiếu mock flag, trung bình bỏ missing, và tautology không bị audit nhận là hollow.

Không chạy full GPU/Kaggle benchmark hoặc integration test cần network; không có raw artifact để xác nhận bảng sổ tay. Các phát hiện về metric là lỗi code có thể tái hiện; các khả năng trộn mock, chọn kết quả đẹp hoặc rò rỉ chưa quan sát được không được nâng thành cáo buộc đã xảy ra.

Ưu tiên xử lý: F1–F3 trước khi xuất bảng mới; sửa nhãn đối chứng và hạ mức kết luận F4–F6; sau đó khóa protocol, provenance và đối chứng mạnh trước chạy xác nhận. Giữ nguyên artifact cũ, tái tính report với phiên bản scorer mới và ghi rõ thay đổi.
