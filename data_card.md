# DATA CARD: BỘ DỮ LIỆU TRÍCH XUẤT THỰC THỂ VÀ DỮ KIỆN KINH TẾ (ĐT02)

**Học phần:** CSC4007 – Xử lý ngôn ngữ tự nhiên  
**Nhóm thực hiện:** Nhóm 4 | **Trường:** Đại học Đại Nam  
**Nhiệm vụ:** Trích xuất bộ dữ kiện kinh tế: `(indicator, value, unit, period, evidence)` từ tin tức tiếng Việt  
**Phiên bản:** 1.0.0 (Ngày cập nhật: 2026-11-24)  

---

### 1. Dataset Summary & Intended Use
- **Mục đích:** Cung cấp ngữ liệu văn bản tiếng Việt từ các bản tin kinh tế - tài chính để huấn luyện, đánh giá và đối chứng các mô hình trích xuất thực thể và dữ kiện định lượng.
- **Phạm vi sử dụng:** Nhiệm vụ NLP Information Extraction / Relation Extraction. Đầu vào là một đoạn văn ngắn (2–4 câu) và đầu ra là danh sách các bộ dữ kiện cấu trúc `(chỉ tiêu, giá trị, đơn vị, mốc thời gian, câu chứng cứ)`.
- **Đối tượng không áp dụng:** Không sử dụng để tự động ra quyết định đầu tư chứng khoán, dự báo kinh tế lượng vĩ mô GDP/CPI tự động.

### 2. Dataset Sources & Versions
- **Nguồn gốc:** Tập con được trích chọn từ corpus `undertheseanlp/UVN-1` trên Hugging Face Hub (`https://huggingface.co/datasets/undertheseanlp/UVN-1`).
- **Tác giả nguồn:** Nhóm nghiên cứu Underthesea NLP.
- **Ngày truy xuất (Retrieved At):** 2026-11-24.
- **Version/Revision:** `UVN-1 commit snapshot 2024` (3.268 bài báo gốc).

### 3. License & Access
- **Giấy phép:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
- **Quyền sử dụng:** Phục vụ nghiên cứu và học tập phi thương mại.
- **Giới hạn tái phân phối:** Không bán lại dữ liệu, không phát tán toàn văn trái phép ngoài phạm vi nghiên cứu của học phần CSC4007.

### 4. Data Structure
Tập dữ liệu bao gồm các trường chính trong `data_manifest.csv` và các file annotation:
- `item_id` (string): Định danh duy nhất cho từng đoạn văn (ví dụ `UVN_BIZ_123_1`).
- `document_id` (string): ID bài báo gốc trong corpus UVN-1.
- `source_name` (string): Nguồn tin tức.
- `published_at` (string): Ngày phát hành thực của bài báo từ nguồn (nếu không có thì để `null`).
- `original_category` (string): Chuyên mục gốc (`Kinh doanh`).
- `task_label` (string): Tên nhiệm vụ (`fact_tuple_extraction`).
- `split` (string): Phân chia tập dữ liệu (`train`, `dev`, `test`).
- `tuples` (list of objects): Mỗi tuple gồm:
  - `indicator` (string): Tên chỉ tiêu kinh tế / doanh nghiệp (ví dụ: `doanh thu hợp nhất Vinamilk`).
  - `value` (string): Con số định lượng (ví dụ: `15637`, `15.6`, `4,5`).
  - `unit` (string): Đơn vị đo lường (ví dụ: `tỷ đồng`, `%`, `triệu USD`).
  - `period` (string): Mốc thời gian (ví dụ: `quý III/2023`, `năm 2022`, hoặc `unknown`).
  - `evidence` (string): Câu trích dẫn trực tiếp chứa sự kiện.

### 5. Composition & Distributions
- **Tổng số đoạn văn trích chọn:** 200 đoạn văn.
- **Phân bố theo split:**
  - `train`: 120 đoạn (60.0%)
  - `dev`: 30 đoạn (15.0%)
  - `test`: 50 đoạn (25.0% - Khóa độc lập cho đánh giá cuối kỳ)
- **Số lượng bài báo độc lập (Document IDs):** 116 bài báo khác nhau.
- **Phân bố chủ đề:** Tài chính doanh nghiệp (45%), Xuất nhập khẩu & Thương mại (25%), Thị trường năng lượng/xăng dầu (15%), Kinh tế vĩ mô & Lãi suất (15%).

### 6. Collection & Sampling
- **Chiến lược lọc:** Từ 1.113 bài báo thuộc nhãn `Kinh doanh` của UVN-1, áp dụng bộ lọc regex bắt buộc chứa đồng thời:
  1. Ít nhất một chỉ tiêu kinh tế (`doanh thu`, `lợi nhuận`, `GDP`, `xuất khẩu`...).
  2. Ít nhất một đơn vị tiền tệ / định lượng (`tỷ đồng`, `triệu USD`, `%`...).
  3. Ít nhất một con số cụ thể.
- **Hạn chế lấy mẫu:** Mỗi bài báo chỉ trích xuất tối đa 2 đoạn văn tiêu biểu để bảo đảm sự đa dạng văn phong và tác giả.

### 7. Preprocessing
- **Chuẩn hóa Unicode:** Chuẩn NFC bằng `unicodedata.normalize("NFC")`.
- **Làm sạch văn bản:** Loại bỏ thẻ HTML, chuẩn hóa ký tự xuống dòng và khoảng trắng liên tiếp.
- **Bảo toàn số liệu kinh tế:** Giữ nguyên vẹn dấu chấm/phẩy thập phân, dấu âm, tỷ lệ %, không làm tròn hay tự ý biến đổi số liệu gốc (tránh chuyển `3,2%` thành `32%`).

### 8. Annotation Process
- **Người gắn nhãn:** Nhóm nghiên cứu gồm 2 sinh viên (Annotator 1 & Annotator 2).
- **Công cụ:** Gắn nhãn thủ công có đối chiếu trực tiếp trên văn bản gốc theo `annotation_guideline.md`.
- **Chính sách xử lý Unclear:** Nếu câu chứa số liệu nhưng không thể xác định chủ thể/chỉ tiêu một cách chắc chắn, hoặc mốc thời gian không được nhắc tới $\rightarrow$ gán nhãn `period: "unknown"`, tuyệt đối không tự suy đoán ngoài văn bản.

### 9. Quality Checks
- **Hậu kiểm chéo (Cross-validation):** 50 đoạn văn (chiếm 25.0% tổng tập dữ liệu, vượt ngưỡng 20% tối thiểu của yêu cầu) được cả 2 thành viên gán nhãn độc lập.
- **Chỉ số bất đồng:** Đạt hệ số tương đồng Cohen's Kappa $\kappa = 0.88$ (mức đồng thuận rất cao).
- **Giải quyết bất đồng:** Các trường hợp xung đột ranh giới chuỗi thực thể (span boundary) được thảo luận và thống nhất theo quy tắc ưu tiên chuỗi dài nhất chứa đủ thông tin ngữ nghĩa.

### 10. Splits & Leakage Prevention
- **Chống rò rỉ dữ liệu (Data Leakage Prevention):** Phân chia tập `train`, `dev`, `test` hoàn toàn dựa trên `document_id`. Không có bất kỳ 2 đoạn văn nào thuộc cùng một bài báo gốc xuất hiện ở hai tập khác nhau.
- **Khóa tập Test:** Danh sách 50 `item_id` trong tập test được lưu cứng tại `data/splits/test_ids.txt` và bị khóa, không được dùng để điều chỉnh luật hay prompt trong quá trình phát triển mô hình.

### 11. Gold & Evaluation Protocol
- **Bộ Gold:** Toàn bộ tập `dev` và `test` được kiểm tra thủ công 100% để đảm bảo độ tin cậy tuyệt đối.
- **Giao thức đánh giá:**
  - `Span-level Precision / Recall / F1` cho việc định vị các thực thể.
  - `Fact Tuple Exact Match (EM)` và `Fact Tuple Normalized Match (NM)` cho bộ 5 dữ kiện.

### 12. Biases, Ethics & Risks
- **Thiên lệch nguồn:** Dữ liệu tập trung vào các sự kiện kinh tế lớn của Việt Nam được đăng tải trên các trang báo điện tử chính thống giai đoạn 2020–2024.
- **Bảo vệ PII & Đạo đức:** Văn bản chỉ chứa thông tin công khai về các doanh nghiệp, cơ quan nhà nước và chuyên gia, không chứa thông tin cá nhân nhạy cảm (PII) bất hợp pháp.

### 13. Limitations & Inappropriate Uses
- Dữ liệu phản ánh thông tin tại thời điểm bài báo được phát hành; không dùng làm căn cứ thời gian thực để giao dịch chứng khoán.
- Các quan hệ so sánh phức tạp kéo dài qua nhiều đoạn văn chưa được bao phủ trong giới hạn từng đoạn đơn lẻ.

### 14. Reproducibility & Access Instructions
- Tải lại và tạo toàn bộ dữ liệu chỉ bằng lệnh:
  ```bash
  python src/download_extract_uvn.py
  ```
- Toàn bộ tham số seed ngẫu nhiên, ID cố định và manifest được cam kết tái lập 100%.
