> **Current development protocol v4:** [MULTITARGET_V4.md](MULTITARGET_V4.md). Four-arm SLM grounding screen; v3 results remain historical evidence.

> **Hướng dẫn hiện hành cho batch thử:** [MULTITARGET_SMOKE.md](MULTITARGET_SMOKE.md).
> Notebook `kaggle_council_reproducible.ipynb` đã chuyển sang screen v3: 2 target × 3 arm × 1 attempt.
> Phần bên dưới là hướng dẫn lịch sử, không dùng để tự động chạy full hoặc kết luận hiệu quả.

# 🚀 Hướng Dẫn Thực Thi Chuẩn Hóa Trên Kaggle Dual-GPU (2x Tesla T4)

Tài liệu này hướng dẫn chi tiết quy trình triển khai và tái lập thực nghiệm **Dual-GPU Council Architecture (MoA)** kết hợp **State-Aware Test Generation** trên môi trường điện toán đám mây Kaggle với chi phí $0.

---

## 1. Yêu Cầu Cấu Hình Phần Cứng Trên Kaggle

* **Notebook Settings**:
  * **Accelerator**: `GPU T4 x2` (Bắt buộc chọn Dual Tesla T4, mỗi GPU 15GB VRAM).
  * **Language**: `Python 3`.
  * **Internet**: `On` (Bật để tải thư viện HuggingFace và clone repository).
  * **Environment**: `Always use latest environment`.

---

## 2. Cách 1: Chạy 1-Click Bằng Jupyter Notebook (Khuyến nghị cao nhất)

Toàn bộ quy trình đã được chuẩn hóa thành 1 file Notebook duy nhất tại:
`notebooks/kaggle_council_reproducible.ipynb`

### Các bước thực hiện:
1. Mở Kaggle, tạo một Notebook mới (`New Notebook`).
2. Vào menu **File** $\rightarrow$ **Upload notebook** $\rightarrow$ chọn file `notebooks/kaggle_council_reproducible.ipynb`.
3. Kiểm tra thanh công cụ bên phải (Settings):
   * Đảm bảo **Accelerator** đang là **GPU T4 x2**.
   * Đảm bảo **Internet** đang gạt sang **On**.
4. Bấm **Save Version** $\rightarrow$ chọn **Save & Run All (Commit)** $\rightarrow$ Bấm **Save**.
5. Quá trình chạy sẽ tự động thực hiện từ đầu tới cuối trong **khoảng 35 – 40 phút**.
6. Sau khi chạy xong:
   * Báo cáo Markdown tổng hợp (`FINAL_REPORT.md`) sẽ hiển thị ngay trong cell output.
   * File nén chứa toàn bộ dữ liệu, test cases và coverage (`EVALUATION_OUTPUT.zip`) nằm sẵn ở mục `/kaggle/working` để bạn tải về máy chỉ bằng 1 cú click!

---

## 3. Cách 2: Chạy Qua Dòng Lệnh Terminal / Script

Nếu bạn chạy trực tiếp từ Terminal hoặc cell code đơn giản:

### Bước 2.1: Cài đặt thư viện môi trường
```python
!pip install -q "transformers>=4.40.0" "accelerate>=0.29.0" "bitsandbytes>=0.43.0" pytest pytest-json-report coverage numpy
```

### Bước 2.2: Clone mã nguồn mới nhất
```bash
cd /kaggle/working
git clone https://github.com/nguyendevwk/Test4Py-Setup-pilot-temp.git
cd Test4Py-Setup-pilot-temp
```

### Bước 2.3: Kích hoạt Benchmark Đa Đối Tượng Đối Chứng 3-Arm
```bash
python3 council_multitarget.py \
    --output /kaggle/working/EVALUATION_OUTPUT \
    --repos-dir /kaggle/working/BENCHMARK_REPOS \
    --targets all \
    --arms baseline,ranked,verified \
    --samples 2 \
    --temperature 0.7 \
    --coder-model Qwen/Qwen2.5-Coder-7B-Instruct \
    --critic-model Qwen/Qwen3-4B-Instruct-2507
```

---

## 4. Các Chốt Chặn Kỹ Thuật Được Chuẩn Hóa Trong Phiên Bản Này

1. **VRAM Shield chống CUDA OOM**:
   * Mô hình Coder (GPU 0) và Critic (GPU 1) đều được nạp ở chế độ **4-bit NF4 (BitsAndBytes)**, chỉ tiêu thụ ~5.2GB và ~3.2GB VRAM.
   * `torch.cuda.empty_cache()` và `gc.collect()` được gọi giải phóng bộ nhớ sau mỗi lần mô hình sinh mã.
   * Thiết lập `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` ngăn phân mảnh bộ nhớ.
2. **Cơ chế Tỉa Test (Test-Node Pruning)**:
   * Sau khi LLM sinh mã kiểm thử (gồm 3–5 test functions), hệ thống tự động lọc giữ lại các test case chạy pass thực sự.
   * Các assert phụ bị lệch ở nhiệt độ $0.7$ được lược bỏ để đảm bảo file test cuối cùng đạt **100% Suite Pass Rate** mà vẫn bảo toàn độ phủ nhánh cao.
3. **Môi trường thuần Python kết hợp Type Hints & Docstrings (Tập A & NA)**:
   * Tập trung mạnh vào các repository có Type Hints và Docstrings đầy đủ (`docstring_parser`, `codetiming`, `typesystem`) từ Bảng 1 của Test4Py, kết hợp các case study đối chứng trạng thái (`PyCG`, `woa`, `superstring`).
   * Tự động trích xuất Type Annotations và Docstrings qua AST đưa vào ngữ cảnh sinh test của Coder.
   * Không phụ thuộc vào các thư viện C/Cython lỗi thời, tương thích 100% với môi trường Linux/Python 3.10 trên Kaggle.
