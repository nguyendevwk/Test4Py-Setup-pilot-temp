# Sổ Tay Khắc Phục Sự Cố Kaggle (Troubleshooting Guide)

Tài liệu này tổng hợp các cạm bẫy thực tế và cách giải quyết triệt để trên môi trường Kaggle GPU.

---

## 1. Cạm bẫy Subshell của Jupyter (`!` và biến môi trường)

* **Hiện tượng**: Gõ `!OUT_ROOT="/kaggle/working/..."` ở dòng trên, nhưng dòng dưới `!mkdir -p "$OUT_ROOT"` lại tạo thư mục rỗng, hoặc ghi file nhầm vào thư mục gốc `//stat_arm_...` gây lỗi `Permission denied`.
* **Bản chất**: Mỗi dòng bắt đầu bằng `!` trong Jupyter là một subshell độc lập. Sau khi dòng đó kết thúc, biến môi trường biến mất hoàn toàn.
* **Cách khắc phục chuẩn**:
  * Dùng biến Python và cú pháp nội suy của IPython:
    ```python
    out_root = "/kaggle/working/MASTER_EVALUATION"
    !mkdir -p {out_root}
    !python council_runner.py --output {out_root}/run_01
    ```
  * Hoặc dùng vòng lặp Python trực tiếp `for mode in [...]`.

---

## 2. Lỗi `fatal: not a git repository`

* **Hiện tượng**: `git pull origin main` báo lỗi:
  `fatal: not a git repository (or any parent up to mount point /kaggle)`
* **Bản chất**: Kaggle mặc định mở notebook tại `/kaggle/working`. Thư mục này chưa có `.git` vì repo được clone vào một thư mục con (ví dụ: `/kaggle/working/Test4Py-Setup-pilot-temp`).
* **Cách khắc phục**: Luôn kiểm tra và `cd` vào repo trước:
  ```python
  import os
  from pathlib import Path

  repo = list(Path("/kaggle/working").glob("**/council_runner.py"))
  if repo:
      os.chdir(repo[0].parent)
      print("Đã chuyển vào thư mục repo:", os.getcwd())
  else:
      !git clone https://github.com/nguyendevwk/Test4Py-Setup-pilot-temp.git /kaggle/working/Test4Py-Setup-pilot-temp
      os.chdir("/kaggle/working/Test4Py-Setup-pilot-temp")
  ```

---

## 3. Lỗi thiếu thư viện sau khi khởi động lại Session

* **Hiện tượng**: `ModuleNotFoundError: No module named 'pytest_jsonreport'`.
* **Bản chất**: Container của Kaggle là ephemeral (bộ nhớ tạm). Khi session hết hạn hoặc restart, các gói pip tự cài sẽ bị xóa sạch về trạng thái gốc.
* **Cách khắc phục**:
  * Luôn có cell cài đặt đầu notebook:
    ```python
    !pip install -q pytest-json-report coverage bitsandbytes
    ```
  * Mã nguồn Council từ commit `c0d99b0` đã tích hợp cơ chế tự động cài đặt `pytest-json-report` nếu phát hiện thiếu khi runtime.

---

## 4. CUDA Out-Of-Memory (OOM) trên Tesla T4 (15GB)

* **Hiện tượng**: `torch.cuda.OutOfMemoryError: CUDA out of memory`.
* **Bản chất**: Mô hình 14B (như `Qwen2.5-Coder-14B-Instruct`) ở chế độ FP16 ngốn > 28GB VRAM, vượt xa dung lượng 15GB của Tesla T4.
* **Cách khắc phục**:
  * Bắt buộc bật **4-bit NF4 Quantization** (`--load-in-4bit`).
  * Mức tiêu thụ VRAM thực tế sau 4-bit:
    * Coder 14B trên GPU 0: **~8.5 GB** (hoàn toàn an toàn trên 15GB).
    * Critic 4B trên GPU 1: **~3.2 GB** (hoàn toàn an toàn trên 15GB).

---

## 5. HuggingFace Hub Rate Limit (Unauthenticated Warnings)

* **Hiện tượng**: Lỗi kết nối hoặc cảnh báo `You are sending unauthenticated requests to the HF Hub`.
* **Cách khắc phục**:
  * Commit `c0d99b0` đã bổ sung khối `try...except` an toàn: nếu API kiểm tra SHA bị nghẽn mạng, engine sẽ tự động fallback về revision `main` hoặc revision local thay vì làm crash toàn bộ pipeline.
  * Nếu muốn tốc độ tải nhanh hơn, có thể truyền `HF_TOKEN` trong biến môi trường:
    ```python
    import os
    os.environ['HF_TOKEN'] = 'hf_your_token_here'
    ```
