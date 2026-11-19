# Checkpoint tiếp tục nghiên cứu — 17/11/2026

## Kết luận phải giữ nguyên

Đã hoàn tất72/72lượt14B trên12module/bốn project, ba seed mỗi target.
Source-only2/36suitepass/replay; source+APIfacts4/36. Tiêu chí khóa có
positivePython targetcoverage:1/36vs3/36; có giới hạn đo vớiNumbaJIT.
Hai lượt thắng thêm đều thuộc cùng một targetKafka ởhai seed. Chưa chứng
minh tổng quát hóa, tương đương7B, hoặc ngang/vượt Test4Py/paper.
Inputtokens tăng47,44%, inference tăng1,58%; chưa có speedup held-out.
Không mở full campaign từ kết quả này. Đây là componentablation trên
source thật, không phải toàn pipeline Test4Py gốc.

## Những thứ đã hoàn tất

- API-contract-v1 development:10lượt, baseline0/5vsfacts1/5.
- Source-first-v2 development:15lượt, upstream-prompt0/5,source-only2/5,
  source+facts3/5; không pool với cohortv1.
- Held-out componentv2:72lượt, mọi productionintegrity check đúng.
- Local engineering regression:180tests pass. Đây không phải efficacy.
- Bộứngdụng14test giữ nguyên12testcũ và thêm2test nguyên văn; replay14/14
  trongba process. genty_args18/20→20/20line. Hai faultiterator pháttriển
  sống sót với bộcũ và bị bộmới phát hiện. Không suy rộng curatedbundle
  thành kết quả nghiên cứu; hai fault này được chọn sau review.

## Đọc trước khi tiếp tục

1. [Báo cáo72lượt](analysis/API_SOURCE_HELDOUT_V2_20261117.md).
2. [Đối chiếuđónggóp/priorart](analysis/API_CONTRACT_CONTRIBUTION_20261117.md).
3. [Thiếtkếvàprotocol](../docs/API_CONTRACT_MECHANISM.md).
4. [NhậtkýR14–R15](NHAT_KY_NGHIEN_CUU.md) và [sổtay](SO_TAY_HIEN_HANH.md).
5. [Accountingtarget/seed/project](artifacts/api_source_heldout_v2_analysis_20261117.json).
6. [Bộtestứngdụng](application/14b_genty_extended_20261117.zip).

## Bằng chứng đã tải về workspace

Trong `kaggle-output/remote-20261117/`:

- API_CONTRACT_DEV_20261117T020312879124Z.zip
  SHA2566dfc29d3c83fc1d13ec77bfc64ba68fa1636c6baf7c86ed0e8bfff4b242c221d.
- API_SOURCE_FIRST_DEV_20261117T023613600950Z.zip
  SHA25633a54ca54b9fe200934fec4be70d89f972a84ddc61f05f2093d824132e709a6d.
- API_HELDOUT_COMPONENT_20261117T025213627216Z.zip
  SHA25699eb3c3d117424c64984441b20d51e317600070e86c6d18657279b7ec479b1be.
  Đã kiểmCRC. Đây là bằng chứng gốc; không ghi đè.

Audit socketCPUlocal ở `research/artifacts/api_socket_sequential_local_audit_20261117.zip`.
Bốnfile nguyên văn vẫnfail khi chạy tuần tự local; hai replay bị quyền bind
port thấp khácKaggle, nên không gọi đó là replay cùng môi trường. Ba candidate
gốc có missingimportsocket, mộtcase doublebind. Không sửa điểm72lượt.

## Mã nguồn và điều cần lưu ý

`pilot/api_contract.py`, `pilot/source_prompt.py`,
`scripts/api_contract_probe.py`, `scripts/prepare_api_contract_heldout.py`,
`scripts/run_api_heldout_component.py`, `pilot/api_probe_analysis.py`.
Manifest đã khóa trong `research/benchmark/api_*json`.

Runtime/checkout trong `/tmp` và đường dẫn Kaggle cũ không phải tài nguyên
đảm bảo còn tồn tại khi resume. Kết nối Kaggle cũ hiện không truy cập được;
không cần kết nối để đọc bằng chứng đã lưu. Nếu chạyGPUtiếp, cần phiên
hoạt động và preflight/calibration phù hợp. Không lưu credential vào repo.

Workspace có nhiều thay đổi/untracked từ trước; chưa commit/push. Không
reset/clean hoặc xóa các file đó. Source của từng cohort đang chạy đã được
freeze riêng; code local mới không đổi nội dung archive cũ.

## Việc tiếp theo

Phân tích dependency context, setup/cache state và outputbịcắt để chọn một
cơ chế đủ rõ; kiểm chứng fixture phải gọi đúng target và xác nhận trạng thái
phù hợp, không chỉ import/constructor. Kiểm soát nguồn và oracle; không
xóa test/sửa yếuassertion để nâng điểm. Sau thay đổi, chạy engineeringprobe
nhỏ trước. Nếu dùng outcomesheldoutv2 để điều chỉnh cơ chế, các target này
trở thành development cho phiên bản mới; cần tập xác nhận mới.

Không coi chênh lệch chưa rõ là tương đương. Chưa chạy7B, chưa có phép so
sánh wholepipeline matched đủ để tuyên bố vượt paper.
