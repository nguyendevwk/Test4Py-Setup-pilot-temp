# Đối chiếu pipeline và giới hạn pilot

Nguồn đã đọc trực tuyến tại commit `3c8b45410545183a9a579a784ffefae722a158a6`:

- [message.py](https://github.com/Test4DT/Test4Py/blob/3c8b45410545183a9a579a784ffefae722a158a6/test4dt/message.py): `ProjectMessage.init` xây call graph, tổng hợp thông tin caller/callee, summary class/function, embedding và chỉ mục truy xuất. `FunctionMessage.judge_params` suy luận kiểu; `get_source_code` gắn kết quả vào ngữ cảnh.
- [testcase.py](https://github.com/Test4DT/Test4Py/blob/3c8b45410545183a9a579a784ffefae722a158a6/test4dt/testcase.py): `TestManager.generate_test_case` gọi suy luận kiểu rồi chọn nhánh normal/easy/evolution. `Testcase.assert_check` chạy pylint, pytest, repair và fallback cắt code. Giữ nguyên các nhánh này, kể cả giới hạn repair và fallback upstream có thể bỏ assertion.
- [gptapi.py](https://github.com/Test4DT/Test4Py/blob/3c8b45410545183a9a579a784ffefae722a158a6/test4dt/gptapi.py): một object `model` dùng chung; adapter thay `aask` trước khi import các module còn lại, nên cả phân tích, type inference, retrieval và repair đều dùng cùng SLM.
- [coverage_message.py](https://github.com/Test4DT/Test4Py/blob/3c8b45410545183a9a579a784ffefae722a158a6/test4dt/coverage_message.py): giữ nguyên coverage branch và phản hồi missing lines cho vòng sau. Bộ chấm bổ sung chạy riêng, không đưa kết quả mutant vào model.

[Paper arXiv v2, 22-10-2025](https://arxiv.org/html/2503.14000v2) mô tả call graph guided parameter summarization (§3.2), behavior guided type inference (§3.3), generation và adaptive repair (§3.4). Pilot giữ các bước đó và bổ sung setup ở prompt generation/repair. Đây là đối chiếu kiến trúc, không phải chứng minh tái lập số liệu bài báo. SLM, giới hạn một target và phạm vi phân tích `pycg/machinery` là những khác biệt được áp dụng chung cho bốn chế độ.

## Các thay đổi đồng nhất ở mọi chế độ

1. Thay backend chat bằng Transformers greedy generation. Embedding giữ implementation upstream, dùng snapshot BGE được ghim revision.
2. Phân tích các file sản phẩm trong `pycg/machinery`, chỉ sinh test cho `get_custom_loader`. Loại thư mục `test`, `tests` và tên file test khỏi danh sách truy xuất. Không xóa test có sẵn trong checkout, nhưng không dùng chúng làm nguồn retrieval hoặc chạy chúng khi chấm.
3. Thêm newline vào kết quả `get_code`: upstream ghép comment module và code nên code không có newline đầu có thể bị comment mất dòng import. Adapter áp dụng cùng một sửa đổi cho tất cả chế độ.
4. Thêm cùng mô tả hai tình huống vào prompt sinh test/repair. Giữ nguyên prompt phân tích và suy luận kiểu.
5. Quan sát `set_code` và các bước check để lưu mọi phiên bản, kể cả test bị upstream xóa. Không sửa kết quả trả về của checker.

Không sửa file upstream. `upstream/` là checkout commit độc lập; `experiment.json` và `comparison.json` lưu hash file và cấu hình. Không cung cấp tùy chọn thay số repair vì cần giữ chính sách upstream nguyên vẹn.

## Quy tắc riêng cho PyCG

`pilot/setup.py` duyệt AST của file sản phẩm trong `pycg/`, ghi đường dẫn, dòng, lời gọi và function chứa lời gọi qua `self.import_manager`. Hai thao tác được phép tìm chuỗi là `set_current_mod` và `create_node`. Thứ tự: constructor, từng thao tác theo tên tăng dần, rồi hoán vị hai thao tác. Đây là tìm kiếm hữu hạn có adapter theo miền, chưa phải thuật toán tổng quát.

Chuyển đối số thành literal `pkg.main`/`main.py` và biến nhận `manager` là quy tắc viết riêng. Fixture tình huống đích đã tồn tại thêm `create_node("pkg.dep")` và `set_filepath("pkg.dep", "old.py")`; đó cũng là quy tắc viết riêng, không tuyên bố được suy ra tự động hoàn toàn. Mã gọi sản phẩm chứng minh hai thao tác nguồn; mọi bằng chứng `set_filepath` tìm thấy cũng được lưu, nhưng fixture đích không phụ thuộc vào việc có caller cho nó.

`extracted` dùng ứng viên đầu của từng tình huống, không probe. `verified` duyệt đúng danh sách/thứ tự đó và chọn ứng viên đầu thỏa tiền điều kiện và gọi được loader. Mỗi probe chạy process mới, object mới; mặc định tối đa 10 probe tổng, 10 giây/probe. Timeout giết cả process group. Không tìm được thì báo `selection.complete=false`; không âm thầm dùng oracle thay thế. `caller` chỉ nhận đoạn mã sản phẩm chứa thao tác, không nhận kết quả probe.

Prompt chỉ nhận mô tả tình huống và code setup/caller. `probes.jsonl` chứa trạng thái quan sát để audit nội bộ. Nó không được đọc bởi backend hay retrieval. Oracle viết tay chỉ ở `pilot/validate.py`, không import từ worker và không dùng làm pytest do model sinh.

## Bộ chấm

Test chính thức là file pytest upstream giữ lại, không ghép test viết tay vào kết quả sinh. Chạy bản gốc, lọc nodeid pass, replay tập đó để phát hiện bất ổn rồi dùng đúng tập đó chấm branch coverage và hai mutant. Coverage gồm summary module và function/nested function của `imports.py` để reviewer xem phạm vi; không gộp module coverage thành coverage riêng của target.

Hai operator cố định nằm trong returned loader: đổi filepath cho node mới; ghi đè filepath node đã tồn tại. `mutant_pool.json` chứa source và hash, so sánh hash qua cấu hình. AST guard báo lỗi nếu source không đúng hình dạng kỳ vọng; không chọn mutant thay thế sau khi xem test.

Call-phase failure của test từng pass được tính killed; import, lỗi collection/setup/teardown, process error, timeout hoặc thiếu nodeid là lỗi môi trường/inconclusive. Các stderr/traceback và từng test được lưu để kiểm tra nguyên nhân. Nếu cả hai mutant có verdict killed/survived, mutation score pilot = killed/2. Không có test hợp lệ hoặc mutant chưa chấm được thì score là null, không thay bằng 0 hoặc bỏ khỏi mẫu số. Đây chỉ là mutation score của hai mutant minh họa, không phải benchmark mutation score.

Phân loại generation/import/setup/assertion là heuristic dựa diagnostic, không phải nhãn ground truth; log thô được giữ để kiểm tra lại. Chi phí báo theo giai đoạn và loại lời gọi, gồm phân tích, probe và repair. So sánh có cùng ngân sách mỗi lời gọi/số vòng, không cùng tổng token. Một lần greedy chạy không đủ kết luận thống kê; không mở rộng ngoài pilot này.
