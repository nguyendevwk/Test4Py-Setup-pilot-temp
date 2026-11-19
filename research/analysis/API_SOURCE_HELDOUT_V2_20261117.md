# Kết quả source/API contract: kiểm chứng thành phần trên project độc lập

**Kết luận:** có tín hiệu dương nhỏ nhưng chưa đạt mục tiêu cải tiến đáng tin
cậy hoặc ngang/vượt Test4Py/paper. Chưa mở full campaign; chưa có kết quả7B.

Hoàn tất72/72lượt trên12target ở12module/bốn project, ba seed42/43/44.
Hai arm cùngQwen2.5-Coder-14B-Instruct NF4, revision
`aedcc2d42b622764e023cf882b6652e646b95671`, cap4096/512, temperature0,7,
top_p0,95, một lần sinh, zero repair/pruning. Control dùng source thật;
treatment chỉ thêm API facts. Đây không phải toàn pipeline Test4Py với
initialization/type inference/RAG/iterative repair.

| Chỉ số | Source-only | Source + API facts |
|---|---:|---:|
| Lượt dự kiến/hoàn tất |36/36|36/36|
| Full suite pass và replay ổn định |2/36|4/36|
| Pass/replay và positive Python target coverage theo tiêu chí khóa |1/36|3/36|
| Pytest failure |24|21|
| Capped output, giữ là failure theo protocol |10|11|
| Input tokens |23.865|35.187|
| Output tokens |15.102|14.596|
| Tổng thời gian inference trên từng arm |1530,81s|1555,02s|

API facts tăng input47,44%, inference khoảng1,58%; chưa có lợi ích tốc độ
trên tập độc lập này. Các thời gian loại trừ model load và preparation. Hai
GPU chạy song song nên không cộng các thời gian arm thành walltime.

## Phân bố kết quả

| Project | Source-only pass/replay | API pass/replay | Source có positive target coverage | API có positive target coverage |
|---|---:|---:|---:|---:|
|dfsql|0/9|0/9|0|0|
|kafka-shell|0/9|2/9|0|2|
|pymssa|1/9|1/9|0 (JIT)|0 (JIT)|
|pypykatz_server|1/9|1/9|1|1|

Chênh lệch đến từ `KafkaCompleter.is_cluster_command`, seed43và44. Vì đây
là cùng một target trong cùng một project, không coi hai lượt thắng là hai
project độc lập. Cả hai candidate import/call implementation thật, không
mock target; assertions về tên lệnh và giới hạn số từ phù hợp source.
Seed43 kill mutantbiên `len(split_text) <= 2` thành`< 2`; seed44 không kill
mutant này. Tín hiệu fault detection có thật nhưng chưa ổn định theo seed.
Không có cơ sở kết luận tương đương từ các chênh lệch còn bất định.

## Giới hạn đo và review

`vtmat_ts_startidx` được Numba JIT biên dịch. Cả hai arm ởseed42pass/replay
với assertions gọi trực tiếp hàm thật và kiểm tra phép nhân với các giá trị
cụ thể. Python coverage ghi0bodyline do native execution; không diễn giải
đó là bằng chứng test không gọi target. Chỉ số khóa giữ nguyên, đồng thời
báo first-pass/replay riêng. Không đổi scoring giữa cohort để cộng điểm.

Các suite socket setup pass sử dụng loopback và port cố định. Review cho
thấy một số check chưa mạnh: gọi lại listen trong assertion không xác nhận
lệnh listen củasetup, và try/except không cóelsefail không chứng minh đầy
đủ negative behavior. Pass không đồng nghĩa mọi assertion đều đủ mạnh;
không có tỷ lệ semantic assertion accuracy đã được đo toàn bộ.

Các lỗi đáng chú ý là import thiếu trong test, setup/cache state sai,
expected output không phù hợp source, thiếu helper context và file bị cắt
ở512token. Không sửa assertion hoặc bỏ các test lỗi để làm đẹp kết quả.
Tất cả72production source integrity checks đều đúng; không có outcome bị
loại khỏi mẫu số. Scope pool mutant nhỏ và có mutant ở hàm khác target;
không suy ra khả năng phát hiện lỗi toàn diện từ các score này.

## Kết quả ứng dụng riêng

Bộ `14b_genty_extended_20261117.zip` giữ nguyên12test cũ và thêm2test
nguyên văn từ development. Ba processPy3.12pass14/14, genty_args coverage
18/20→20/20dòng; hai lỗi iterator bổ sung bị bộ mới phát hiện và sống sót
với bộ cũ. Hai fault này được chọn sau reviewdevelopment, không phải pool
confirmatory. Đây là cải thiện bộứngdụng cụ thể, không thay thế kết quả72
lượt trên project độc lập hoặc chứng minh thuật toán vượt paper.

## Bằng chứng

Raw archive: `API_HELDOUT_COMPONENT_20261117T025213627216Z.zip`, CRC verified,
SHA256`99eb3c3d117424c64984441b20d51e317600070e86c6d18657279b7ec479b1be`.
Manifest khóa SHA256
`e89de4086cf3ba2ab2d62fafe59709a792a5e129dd297c801002f404e78bf6e5`.
Accounting theo target/seed/project:
`research/artifacts/api_source_heldout_v2_analysis_20261117.json`.
Engineering regression:180tests pass; không dùng số đó làm efficacy.

Cần xử lý đúng dependency/setup state và kiểm soát output scope trước
khi tốn thêm full-run. Nếu dùng các lỗi held-out này để đổi cơ chế, tập này
sẽ trở thành development cho phiên bản mới và cần tập xác nhận mới.

### Audit bổ sung lỗi socket

Bốn report có `Address already in use`. Ba candidate đã có lỗi thiếu import
`socket`; một candidate gọi setup lại trên cùng địa chỉ khi socket trước còn
mở. Replay tuần tự bốn file nguyên văn ở môi trường local khóa dependency
vẫn không có suite all-pass. Hai replay local bị chặn thêm bởi quyền bind
port thấp, nên không gọi đây là xác nhận độc lập cùng môi trường Kaggle.
Các kết quả Kaggle72lượt không bị ghi đè hoặc đổi điểm; không kết luận mọi
lỗi port đều do tranh chấp worker. ZIP bổ sung nằm ở
`research/artifacts/api_socket_sequential_local_audit_20261117.zip`.
