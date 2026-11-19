**Đánh giá đối chiếu bài tiểu luận Council-SOTA — 18/11/2026**

**Kết luận: cần sửa lớn trước khi nộp.** Bài khớp một số bảng CSV bàn giao và nhật ký R16, nhưng chưa khớp đầy đủ với phương pháp đã triển khai, nguồn gốc dữ liệu và lịch sử các nhánh thực nghiệm. Có bằng chứng trực tiếp về gán sai phương pháp, tuyển chọn đầu ra khác nhánh và cập nhật CSV bằng số nhập sẵn. Chưa có cơ sở kết luận tác giả cố ý gian lận; cũng chưa đủ cơ sở xác nhận các kết luận hiệu quả và độ tin cậy như bài đang viết.

Phạm vi: đọc DOCX, source, CSV/JSON, Git local, nhật ký; ba subagent độc lập kiểm tra lịch sử, định lượng, mutation/oracle/chi phí. Agent chính kiểm tra thuật toán, seed, số học bảng và tài liệu tham khảo. Không chạy lại GPU/API, không sửa bài gốc hay kết quả cũ. Không phải kiểm tra đạo văn toàn văn hoặc xác minh hóa đơn API.

Bài gốc: `/home/heurix/Downloads/Tieu_Luan_CNPMTT_Council_SOTA.docx`.
SHA256: `9a90877d5fe8c78b56c307042bffd59243e0a90884eec813ef295f13078310d9`.
HEAD khi kiểm tra: `7a97eb0`, ngày 16/11/2026. Checkout có nhiều thay đổi và file untracked từ trước audit. Các runner/deliverables Council-SOTA chưa nằm trong snapshot Git HEAD. Bản trích [paper_extracted.txt](paper_extracted.txt) giữ thứ tự đoạn và hàng bảng; số dòng là vị trí trích, không phải trang Word. Không kiểm tra bố cục ảnh hay field mục lục.

**Các phần đã khớp về số học**

| Nội dung | Tính lại | Ý nghĩa giới hạn |
|---|---:|---|
| Baseline | 51/105 = 48,57%; SC 24,1276% | Khớp bảng 4.2 và CSV bàn giao |
| Council Standard | 73/105 = 69,52%; SC 37,7510% | Khớp bảng 4.2 và CSV bàn giao |
| SOTA sau cập nhật | 98/105 = 93,33%; SC 47,70% | Khớp bảng đã cập nhật, chưa chứng minh một cohort chạy thống nhất |
| Thống kê trên 21 trung bình target đã xuất | t = 4,2074705; dz = 0,9181453; U = 359; A12 = 0,8140590 | Tái tính bằng thư viện chuẩn; không xác minh p của t/U |
| Wilcoxon | W = 6; p exact hai phía = 0,00001335144 | Tái tính phân phối tổng hạng trên các chênh lệch đã xuất |
| Mutation | 71/187 = 37,97%; trung bình target 43,0952% | Khớp nhãn trong JSON/CSV, chưa xác nhận attribution của mọi kill |

Nguồn: [bảng tổng hợp](../../../monograph_final_deliverables/data/statistical_summary_sota_3way.csv), [mutation JSON](../../../curated_benchmark_results/mutation_results/mutation_details_21targets.json). Cohen d ở bảng thực chất khớp paired dz; nên ghi rõ định nghĩa. 21 target thuộc 8 project vẫn có cấu trúc cụm; p trên target không tự chứng minh khái quát sang project mới. Mann–Whitney/A12 không thay thế phân tích ghép cặp/cụm. Một p đúng số học không khắc phục được sai cohort hoặc tuning trên tập đánh giá.

**Các phát hiện cần xử lý**

| ID | Mức độ | Phát hiện | Vị trí trong bài |
|---|---|---|---|
| F01 | Nghiêm trọng | Gán thí nghiệm API-facts thành Call-Graph RAG | §1.3; bảng 1.2 và 4.9 |
| F02 | Nghiêm trọng | Mutation/golden khác nhánh nhưng quy cho Council-SOTA | §4.2.4, §4.3.3, kết luận RQ4 |
| F03 | Cao | Có script ghi đè số vào CSV được gọi là raw; cần phục hồi provenance | Bảng 4.2, 4.3, 4.6 |
| F04 | Cao | Grounding thủ công được mô tả như tự động trích bảng AST | Thuật toán 3.1, RQ1/RQ3 |
| F05 | Cao | Seed API bị bỏ qua | §3.5, §4.1, §4.5.2 |
| F06 | Cao | Cổng bảo toàn assertion không điều khiển nhận bản sửa | Thuật toán 3.2, §3.4 |
| F07 | Cao | Mutation operators và cách nhận kill khác mô tả | Bảng 3.4, §4.2.4 |
| F08 | Cao | Flaky, taxonomy và rà soát mutant chưa đủ hồ sơ để xác nhận | §4.2.4, bảng 4.8, §4.5.1 |
| F09 | Cao | Latency/Pareto và chi phí chưa cùng nguồn đo | Bảng 4.9, RQ4 |
| F10 | Vừa | Cộng repair và nhãn case study không nhất quán | Bảng 4.2/4.5, §4.3.2 |
| F11 | Cao | Trích dẫn sai metadata, mô tả related work cần kiểm tra lại | Chương 1, danh mục tham khảo |

**F01 — Sai phương pháp và ghép các cohort khác nhau.** Bài đoạn 166 ghi source-only 2/36 và Call-Graph 4/36, input 5.869 → 7.141. Báo cáo nguồn [API_SOURCE_HELDOUT_V2_20261117.md](../../analysis/API_SOURCE_HELDOUT_V2_20261117.md), dòng 6–24, xác định đây là source-only so với source + API facts, 12 target/4 project, zero repair/pruning; input 23.865 → 35.187 (+47,44%). Báo cáo nói rõ không phải toàn pipeline Test4Py/RAG. Không được ghép 4/36 với cold-start upstream 2.627 giây thành một phương pháp đối chứng duy nhất, hoặc so 11,11% đó với 93,33% Groq như hiệu ứng riêng của AST.

**F02 — Golden không phải mẫu thuần SOTA.** [curated_optimal_suites.csv](../../../curated_benchmark_results/curated_optimal_suites.csv) ghi 19 suite `council_enhanced` và 2 `baseline`. [run_curated_high_quality_benchmark.py](../../../run_curated_high_quality_benchmark.py), dòng 343–361, chọn suite pass có coverage cao, latency thấp từ nhiều nhánh. Hai thư mục golden dùng cho mutation và flaky giống nhau 21/21 file. 20/21 file khớp nguồn được manifest chọn; riêng `pycg_scopes` đổi assertion kiểm tra bằng tập khóa thành chứa tập con: so [nguồn baseline](../../../curated_benchmark_results/runs/pycg_scopes/baseline/seed_46/test_candidate_v1.py) dòng 11 với [golden](../../../curated_benchmark_results/golden_curated_suites/test_pycg_scopes_golden.py) dòng 11. Đây là điều kiện kiểm tra yếu hơn, chưa xác định lý do/người sửa hay tác động tới score. Cần ghi đúng “mutation trên golden tuyển chọn từ các nhánh”, công bố mọi chỉnh sửa; không dùng score này đại diện 105 đầu ra SOTA hoặc chứng minh Critic bảo toàn oracle.

**F03 — CSV sau xử lý không còn là raw bất biến.** [fix_data_and_ablation.py](../../../scripts/fix_data_and_ablation.py), dòng 18–29, gán trực tiếp `pycg_classes/full_method/seed42` thành pass, coverage 52,17%, latency 4,01. Dòng 84–138 tạo dictionary số refined cho hai target và ghi cả file refined lẫn file mang tên gốc. **Đã đối chiếu và xác nhận riêng ablation bị nâng sai:** `standardized_research_artifacts/ablation_runs/pycg_classes/full_method/v1_exec/evaluation.json` ghi exit_code=1, pass_count=0, suite_pass=false; pytest_debug.log ghi AssertionError MRO và 1 failed. CSV xuất bản ghi PASS nhưng còn pass_count=0. Chưa thấy artifact chạy thành công thay thế cho hàng này. Theo bảng gốc, full method là 5/6 = 83,33%, coverage theo quy ước phạt failure bằng 0 là 49,20%, không phải 6/6 và 57,90%. Ngược lại, 10 lượt refined SOTA có evaluation thực hỗ trợ pass/coverage; không được gọi toàn bộ số refined là synthetic. Đối chiếu 103/105 lượt SOTA gốc với evaluation không thấy lệch pass/coverage; hai lượt còn lại extraction failure được giữ là thất bại. Đối chứng kiểm tra được 203/210 hàng với evaluation, không thấy lệch; 7 hàng thiếu đường dẫn code. Sau refinement, một số metadata vẫn cũ: final_code_path trỏ runs thay vì runs_refined, numpydoc/44 có final_pass=True nhưng pass_count=0; genty/46 có final_pass=True nhưng total_nodes=pass_count=0 trong khi evaluation refined có 4/4 pass. 98/105 là tổng hợp sau thay kết quả hai target, không mặc nhiên là 105 lượt theo cùng protocol khóa trước. 315 là số hàng bảng cuối; tổng lượt thực thi còn có rerun/refinement. Cần giữ riêng original/rerun và sinh bảng bằng parser, có manifest nguồn/hash; không tiếp tục sửa số để khớp văn bản.

**F04 — Tự động hóa bị mô tả quá mức.** [run_sota_curated_benchmark.py](../../../run_sota_curated_benchmark.py), dòng 38–87, định nghĩa `SYMBOL_GROUNDING_MAP` viết sẵn theo package; dòng 273–275 đưa setup hint có assertion vào prompt. Có dùng helper AST lấy source/import, nhưng chưa thấy luồng tự suy toàn bộ re-export, thuộc tính và C_rules như Thuật toán 3.1. [resolve_council_critiques.py](../../../scripts/resolve_council_critiques.py), dòng 28–37, bổ sung quy tắc theo lỗi quan sát. Hợp lệ nếu công khai là curated hints và development tuning; không phải bằng chứng repository-independent AST synthesis. Viết lại đóng góp đúng phần tự động và phần con người cung cấp; đánh giá held-out sau khóa quy tắc.

**F05 — Seed là nhãn lượt, không phải seed inference đã kiểm soát.** [groq_engine.py](../../../council/groq_engine.py), dòng 88–96, payload không có seed; `generate(..., seed=42)` dòng 147–148 không dùng tham số. Runner SOTA nhận seed nhưng gọi `call_coder` không truyền seed. Nên ghi “5 lần gọi/lặp” và công khai giới hạn; không khẳng định 5 seed độc lập có thể tái tạo. Không suy ra các lần gọi là giả hoặc giống nhau.

**F06 — Audit chưa là gate.** [run_sota_curated_benchmark.py](../../../run_sota_curated_benchmark.py), dòng 396–407, gọi `repair_audit` rồi nhận bản sửa theo suite_pass, không xét accepted. [council/runner.py](../../../council/runner.py), dòng 39–71, helper có quy tắc đếm/so đổi assertion, không phải ngưỡng 75% như bài. Prompt hai vòng ở dòng 303–306 chỉ thay số round; cả hai cùng cho sửa import/parameter/assertion/attribute. Chưa thấy hai chuyên môn vòng cố định hoặc bộ trích `(v_actual,v_expected)` riêng như mô tả. Thuật toán 3.2 còn chạy lại `T_curr` sau khi tạo `T_cand` mà thiếu bước cập nhật. Đếm assertion cũng không chứng minh bảo toàn ngữ nghĩa. Subprocess là cô lập tiến trình, chưa phải security sandbox.

**F07 — Mutation implementation khác bảng.** [run_mutation_testing.py](../../../scripts/run_mutation_testing.py), dòng 185–248, chỉ sinh ROR/AOR/BVR/SIR; SIR là `return expr → return None`, không phải đảo if/else hoặc bỏ cập nhật trạng thái. CRP không có trong luồng này. Dòng 291–325 coi return code khác 0 và timeout là kill; bản ghi chi tiết thiếu log/return code để phân biệt assertion failure với collection/import/hạ tầng. JSON hiện không ghi timeout: chỉ kết luận hạn chế attribution, không quy rằng các kill đã quan sát đều là timeout. Cần kiểm tra original-pass trước mutation, lưu từng tiến trình, tách killed/survived/invalid/timeout/inconclusive.

**F08 — Chưa đủ hồ sơ xác nhận 105/105 và 384 mẫu.** [resolve_council_critiques.py](../../../scripts/resolve_council_critiques.py), dòng 121–156, có chạy 5 lần/suite nhưng chỉ in kết quả. [run_expert_council_defense.py](../../../scripts/run_expert_council_defense.py), dòng 9, 90, 116–121, ghi sẵn văn bản 105/105 rồi xuất Markdown; sự tồn tại báo cáo không chứng minh lệnh đã chạy. Chưa tìm được manifest 105 kết quả, 384 traceback cùng nhãn, hoặc hồ sơ 42/187 mutants được rà soát tương đương. Không tìm thấy hồ sơ không đồng nghĩa chưa từng thực hiện. Ngay cả 5/5 pass chỉ cho phép viết “không quan sát flaky trong 5 lượt ở môi trường này”, không “bảo đảm không flaky/đủ tiêu chuẩn doanh nghiệp”. Nhóm tautology thường không có traceback; cần định nghĩa lại mẫu taxonomy nếu gồm cả kiểm toán source.

**F09 — Tốc độ và chi phí.** CSV SOTA cho latency trung bình 6,6479 s/lượt; đối chứng curated cho baseline 3,5321 và Standard 4,0426 s/lượt. Bài dùng 3,2/7,4/5,8–6,6; [generate_all_master_figures.py](../../../scripts/generate_all_master_figures.py), dòng 286–290, ghi cứng tọa độ Pareto. Chưa có phép đo matched hỗ trợ SOTA nhanh hơn Standard. Timer runner gồm generation, pytest/coverage và repair, không chỉ inference. Ước tính tiền theo engine chưa phải hóa đơn. Chưa thấy ledger cộng lại 0,5166 USD hoặc 0,1340 USD. Bảng kinh tế [chapter_6_and_7_qualitative_economics.md](../../../monograph_final_deliverables/chapters/chapter_6_and_7_qualitative_economics.md), dòng 315–329, input 1.390.650 + output 491.202 = 1.881.852, không phải 1.461.752; theo giá cấu hình chi phí là 0,5033187 USD. Trong bài, 0,0246 USD/target = tổng toàn dự án/21, không phải 0,1340 USD SOTA/21 (= 0,00638). Engine dòng 117–139 có thể bỏ usage lần đầu khi gọi lại do hết output token; cần ledger mọi request. Cloud có VRAM cục bộ bằng 0 không có nghĩa chi phí/bộ nhớ suy luận tổng bằng 0.

**F10 — Bất nhất nội bộ.** Tổng cột “Số ca Critic sửa” 21 hàng bảng 4.2 là **30**, trong khi dòng tổng/bảng 4.5 ghi **29**. Evaluation/CSV gốc cho 67 first-pass + 29 repairs (24 vòng1, 5 vòng2) = 96 pass. Sau refinement là **70 first-pass + 28 repairs (22 vòng1, 6 vòng2) = 98 pass**; bài ghi 69+29 và giữ phân bổ cũ. Cần sinh lại attribution, không sửa một ô tổng đơn lẻ. §4.3.2 gọi mốc 40% của numpydoc/genty_dataset là Baseline, trái bảng 4.2 lần lượt 0% và 20%; mốc 40% đang là SOTA trước tinh chỉnh. Không dùng chênh lệch giữa Standard và SOTA trên OneOf để suy riêng tác động vòng 2 vì đồng thời đổi grounding/protocol. **Nhóm 18 target còn sai danh sách:** bài ghi loại slugify/google/numpydoc, nhưng `scripts/generate_curated_elite_charts.py:35` loại slugify/genty_dataset/numpydoc. Theo danh sách trong bài, pass rate là 95,56%, coverage 50,0111%; theo danh sách mã là 96,67%, coverage khoảng 49,87%, và chỉ 15/18 target đạt 100%, không phải 16/18. Pipeline tuyển chọn `run_curated_high_quality_benchmark.py:108,280` loại ba target rồi giữ “16 high-performing targets” và thêm năm target mới: cần công khai chọn lọc theo kết quả. Nhóm con cần tiêu chí định trước, báo như phân tích thăm dò nếu chọn sau xem kết quả; parser vẫn có nhánh nên nhãn “không rẽ nhánh” cần sửa. Nhật ký R16 ghi 7 project nhưng bài/CSV là 8.

**F11 — Tài liệu tham khảo và related work.** Đã kiểm tra trực tiếp một số nguồn gốc, chưa xác minh trọn bộ 25 mục:

- [1] tên và tác giả Test4Py khớp; arXiv v2 sửa ngày 22/10/2025, không phải phiên bản v2 tháng 3 như cách ghi hiện tại. Nguồn: [arXiv 2503.14000](https://arxiv.org/abs/2503.14000).
- [3] metadata ChatUniTest không khớp danh sách tác giả trong bài: bản framework FSE Companion 2024 ghi Yinghao Chen, Zehao Hu, Chen Zhi, Junxiao Han, Shuiguang Deng, Jianwei Yin. Nguồn: [bài gốc](https://arxiv.org/html/2305.04764v2). Không thu hẹp cơ chế repair thành đúng một vòng nếu chưa có bằng chứng cấu hình tương ứng.
- [4] “J. A. Pizzorno” khác tên Juan Altmayer Pizzorno; mục FSE 2024 cần sửa theo phiên bản thực dùng, bản xuất bản có [DOI 10.1145/3729398](https://doi.org/10.1145/3729398), cùng [preprint](https://arxiv.org/abs/2403.16218).
- [6] Mutation-Guided LLM-based Test Generation at Meta có tác giả Christopher Foster, Abhishek Gulati, Mark Harman và cộng sự, bản arXiv năm 2025; không khớp Garg/TOSEM 2024. Nguồn: [arXiv](https://arxiv.org/abs/2501.12862), [kho UCL và DOI xuất bản](https://discovery.ucl.ac.uk/id/eprint/10218052/).
- [18] thứ tự/tên viết tắt tác giả khác bản gốc: Yuan, Lou, Liu, Ding, Wang, Chen, Peng. Nguồn: [arXiv 2305.04207](https://arxiv.org/abs/2305.04207).
- [22] tên và tác giả khớp; nguồn gốc là [arXiv 2507.14256](https://arxiv.org/abs/2507.14256). Chưa xác minh được nhãn Journal of Systems and Software như bài đang ghi; cần DOI nhà xuất bản trước khi nhận là đã xuất bản ở đó.
- [23], [24]: chưa xác minh được đúng các tổ hợp tiêu đề/tác giả/ấn phẩm đang ghi. Đánh dấu chờ DOI/PDF gốc, không gọi chắc chắn là tài liệu bịa chỉ vì search không tìm thấy.

**Đối chiếu lịch sử cần đưa vào bài**

| Giai đoạn | Kết quả/phạm vi cần giữ riêng |
|---|---|
| Council v2, audit 15/11 | Sửa lỗi metric, baseline Council không phải upstream; audit cũ không tự áp dụng cho mọi runner mới |
| Council v4/160 lượt | Baseline 13/40, grounded 11/40, ranked/verified 10/40; không cho thấy thắng tổng thể |
| Upstream 14B NF4 cold/warm | Có timeout/không hoàn tất; không đổi NA thành zero để so headline |
| API source held-out 17/11 | Source-only 2/36, API-facts 4/36; khác full RAG |
| R16 Groq 20B 18/11 | Nhánh riêng, dữ liệu refined và curated cần manifest riêng |

Nguồn: [audit 15/11](../../AUDIT_INTEGRITY_2026-11-15.md), [Council160](../../analysis/COUNCIL_160_20261116.md), [upstream cold](../../analysis/UPSTREAM_14B_SMALL_TIMEOUT_20261116.md), [warm](../../analysis/NF4_SMALL_REMOTE_20261117.md), [nhật ký R16](../../NHAT_KY_NGHIEN_CUU.md). Không cần đưa mọi lịch sử vào phần kết quả chính, nhưng phải tránh ghép chúng thành một nghiên cứu đối chứng thống nhất và công khai tuning/negative results có liên quan.

**Thứ tự sửa đề nghị**

1. Sửa ngay F01/F02 và nhãn before/after; rút kết luận vượt upstream, Pareto, không flaky tuyệt đối.
2. Khóa và lưu snapshot source/config; dựng manifest nối từng hàng CSV tới raw evaluation, prompt, completion và phiên bản test. Giữ original/rerun riêng; giải trình mọi số nhập tay.
3. Khôi phục ablation theo artifact gốc: 5/6 full_method, không giữ hàng FAIL bị đổi PASS. Sinh lại toàn bộ bảng/hình từ cùng manifest, báo mẫu số/missingness, tách coverage zero do outcome penalty khỏi coverage thực sự đo được bằng 0; nêu rõ module coverage.
4. Viết lại thuật toán đúng implementation, công khai curated hints và giới hạn assertion audit. Nếu sửa code sau audit, kết quả mới phải mang revision/cohort mới.
5. Xác minh mutation/fault attribution, nguồn golden, flaky ledger, taxonomy và chi phí; chỉ giữ claim có bằng chứng hoặc hạ xuống thiết kế/chưa xác minh.
6. Đính chính bibliography bằng DOI/BibTeX nguồn gốc; thêm hạn chế tuning và cụm project; dùng đánh giá held-out khóa trước để xác nhận đóng góp.

Câu kết luận phù hợp hơn hiện tại: “Trên tập phát triển tuyển chọn, các bảng sau cập nhật cho thấy tỷ lệ suite pass và độ phủ cao hơn baseline nội bộ. Do có tri thức thủ công, tinh chỉnh trên target đã quan sát và giới hạn provenance/đối chứng, kết quả chưa xác lập ưu thế so với Test4Py upstream hoặc khả năng khái quát.”
