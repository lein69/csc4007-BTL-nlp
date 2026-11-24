# BÁO CÁO PHÂN TÍCH LỖI (ERROR ANALYSIS)

**Mã đề tài:** ĐT02 – Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Tập dữ liệu:** 50 mẫu Test bị khóa (`data/splits/test_ids.txt`)  
**Số lượng mẫu phân tích:** 10 trường hợp cụ thể theo đúng mẫu Phụ lục B  

---

### Ca lỗi 1 (ID: UVN_BIZ_article-00011_2) - Lỗi gán nhầm đơn vị kép (Dual Currency)
- **item_id và loại lỗi:** `UVN_BIZ_article-00011_2` | Lỗi đơn vị kép (Unit / Currency Conversion)
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"EU cho biết thỏa thuận cũng sẽ giúp tiết kiệm 4 tỷ euro (4,75 tỷ USD) tiền thuế cho các doanh nghiệp châu Âu."*
- **Gold hoặc đáp án tham chiếu:**
  * Tuple 1: `indicator: "tiết kiệm tiền thuế EU", value: "4", unit: "tỷ euro", period: "unknown"`
  * Tuple 2: `indicator: "tiết kiệm tiền thuế EU", value: "4.75", unit: "tỷ USD", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** Bắt được cả 2 con số nhưng gán cùng một đơn vị `tỷ euro` cho cả hai do khoảng cách ký tự.
  * **E1:** Tách được 2 số nhưng không nhận biết dấu ngoặc đơn `(4,75 tỷ USD)` là giá trị quy đổi tương đương.
  * **E2:** Nhận diện đúng 2 đơn vị `EUR` và `USD` nhờ module chuẩn hóa tiền tệ.
- **Nguyên nhân khả dĩ:** Viết số liệu tương đương trong dấu ngoặc đơn gây nhiễu cấu trúc cú pháp của câu.
- **Ảnh hưởng đến người dùng:** Người dùng có thể hiểu nhầm là hai khoản tiền thuế khác nhau thay vì một khoản được quy đổi.
- **Đề xuất thay đổi:** Bổ sung luật phát hiện cụm số tương đương trong ngoặc đơn dạng `A (B)`.

---

### Ca lỗi 2 (ID: UVN_BIZ_article-00014_1) - Lỗi đảo dấu âm khi có từ "giảm"
- **item_id và loại lỗi:** `UVN_BIZ_article-00014_1` | Lỗi phân cực số liệu (Negative Sign Omission)
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Chỉ số giá tiêu dùng tháng 5 giảm 0,2% so với tháng trước."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "chỉ số giá tiêu dùng CPI", value: "-0.2", unit: "%", period: "tháng 5 so với tháng trước"`
- **Prediction E0 / E1 / E2:**
  * **E0:** `value: "0.2"` (Sai dấu, không có dấu âm `-`).
  * **E1:** `value: "-0.2"` (Đúng, nhờ module nhận biết động từ xu hướng `giảm`).
  * **E2:** `value: "-0.2"` (Đúng).
- **Nguyên nhân khả dĩ:** E0 chỉ dùng regex tìm số thuần túy nên không xét ngữ cảnh phân cực trước số.
- **Ảnh hưởng đến người dùng:** Đảo ngược bản chất kinh tế từ lạm phát giảm sang tăng giá.
- **Đề xuất thay đổi:** Luôn kích hoạt phân tích ngữ cảnh trước từ ngữ định lượng.

---

### Ca lỗi 3 (ID: UVN_BIZ_article-00018_2) - Lỗi nhầm lẫn mốc thời gian đa kỳ (Period Mismatch)
- **item_id và loại lỗi:** `UVN_BIZ_article-00018_2` | Lỗi gán nhầm mốc thời gian
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Năm 2023, doanh thu đạt 12.000 tỷ đồng, trong khi kế hoạch năm 2024 dự kiến đạt 15.000 tỷ đồng."*
- **Gold hoặc đáp án tham chiếu:**
  * Tuple 1: `indicator: "doanh thu", value: "12000", unit: "tỷ đồng", period: "Năm 2023"`
  * Tuple 2: `indicator: "kế hoạch doanh thu", value: "15000", unit: "tỷ đồng", period: "năm 2024"`
- **Prediction E0 / E1 / E2:**
  * **E0:** Gán cả hai số liệu về cùng mốc `Năm 2023` vì `Năm 2023` nằm ở đầu câu.
  * **E1:** Tách được theo liên từ `trong khi`, gán đúng mốc từng kỳ.
  * **E2:** Gán đúng và nhận diện `kế hoạch doanh thu` thay vì chỉ `doanh thu`.
- **Nguyên nhân khả dĩ:** Heuristic khoảng cách ký tự toàn câu của E0 bị nhiễu khi câu có nhiều mốc thời gian.
- **Ảnh hưởng đến người dùng:** Nhầm lẫn giữa số liệu thực tế đã đạt và số liệu kế hoạch tương lai.
- **Đề xuất thay đổi:** Phân rã câu thành các mệnh đề phụ trước khi liên kết thuộc tính.

---

### Ca lỗi 4 (ID: UVN_BIZ_article-00021_1) - Lỗi ranh giới chuỗi chỉ tiêu (Span Boundary Truncation)
- **item_id và loại lỗi:** `UVN_BIZ_article-00021_1` | Lỗi cắt cụt tên chỉ tiêu
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Tổng kim ngạch xuất nhập khẩu hàng hóa cả nước đạt 683 tỷ USD."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "tổng kim ngạch xuất nhập khẩu hàng hóa", value: "683", unit: "tỷ USD", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** `indicator: "xuất khẩu"` (Cắt cụt, mất chữ nhập khẩu và hàng hóa).
  * **E1:** `indicator: "kim ngạch"` (Thiếu thành phần bổ nghĩa).
  * **E2:** `indicator: "kim ngạch xuất khẩu"` (Khá đầy đủ).
- **Nguyên nhân khả dĩ:** Từ điển E0 ưu tiên từ khóa ngắn thay vì cụm danh từ dài nhất.
- **Ảnh hưởng đến người dùng:** Làm sai lệch phạm vi thống kê (từ cả xuất nhập khẩu thành chỉ xuất khẩu).
- **Đề xuất thay đổi:** Áp dụng NP-chunking hoặc POS tagging để lấy trọn vẹn cụm danh từ.

---

### Ca lỗi 5 (ID: UVN_BIZ_article-00025_1) - Lỗi số viết tắt với đơn vị (Unit Concatenation)
- **item_id và loại lỗi:** `UVN_BIZ_article-00025_1` | Lỗi tách từ số và đơn vị dính liền
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Giá dầu thô Brent giao dịch ở mức 85USD/thùng."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "giá dầu thô Brent", value: "85", unit: "USD/thùng", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** Bỏ sót mẫu vì `85USD` viết liền không có khoảng trắng.
  * **E1:** Bỏ sót mẫu.
  * **E2:** Trích xuất thành công do regex linh hoạt `\d+([A-Za-z%]+)`.
- **Nguyên nhân khả dĩ:** Regex cứng nhắc đòi hỏi khoảng trắng giữa số và chữ.
- **Ảnh hưởng đến người dùng:** Bỏ lọt các chỉ báo hàng hóa quan trọng.
- **Đề xuất thay đổi:** Chuẩn hóa tiền xử lý tách số và chữ cái dính nhau trước khi chạy mô hình.

---

### Ca lỗi 6 (ID: UVN_BIZ_article-00030_2) - Lỗi điểm phần trăm (Percentage vs Percentage Points)
- **item_id và loại lỗi:** `UVN_BIZ_article-00030_2` | Lỗi phân biệt % và điểm phần trăm
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Ngân hàng Nhà nước hạ trần lãi suất thêm 0,5 điểm phần trăm."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "hạ trần lãi suất", value: "-0.5", unit: "điểm phần trăm", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** `unit: "%"` (Nhầm lẫn giữa điểm phần trăm và tỷ lệ phần trăm).
  * **E1:** `unit: "điểm phần trăm"` (Đúng).
  * **E2:** `unit: "điểm phần trăm"` (Đúng).
- **Nguyên nhân khả dĩ:** Từ điển E0 đơn giản hóa tất cả biến thể về `%`.
- **Ảnh hưởng đến người dùng:** Sai lầm toán học trong phân tích chính sách tiền tệ.
- **Đề xuất thay đổi:** Giữ nguyên vẹn đơn vị kỹ thuật `điểm phần trăm` theo đúng văn bản nguồn.

---

### Ca lỗi 7 (ID: UVN_BIZ_article-00033_1) - Lỗi suy diễn mốc thời gian ngoài văn bản (Hallucination)
- **item_id và loại lỗi:** `UVN_BIZ_article-00033_1` | Lỗi ngoại suy thời gian ngoài câu
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Dư nợ tín dụng đối với nền kinh tế đạt trên 13,5 triệu tỷ đồng."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "dư nợ tín dụng nền kinh tế", value: "13.5", unit: "triệu tỷ đồng", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** `period: "unknown"` (Đúng nguyên tắc).
  * **E1:** `period: "unknown"` (Đúng nguyên tắc).
  * **E2:** `period: "unknown"` (Đúng nguyên tắc).
- **Nguyên nhân khả dĩ:** Không mắc lỗi vì tuân thủ nghiêm ngặt quy định không tự ý lấy `published_at` gán vào dữ kiện.
- **Ảnh hưởng đến người dùng:** Đảm bảo độ trung thực và tính kiểm chứng khoa học.
- **Đề xuất thay đổi:** Duy trì cờ `period: "unknown"` khi văn bản không nói rõ.

---

### Ca lỗi 8 (ID: UVN_BIZ_article-00037_2) - Lỗi trích xuất cụm số ước lượng (Range Values)
- **item_id và loại lỗi:** `UVN_BIZ_article-00037_2` | Lỗi khoảng giá trị (Range Number)
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Tăng trưởng GDP năm nay dự báo trong khoảng 6 - 6,5%."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "dự báo tăng trưởng GDP", value: "6 - 6.5", unit: "%", period: "năm nay"`
- **Prediction E0 / E1 / E2:**
  * **E0:** Chỉ lấy được số `6.5%`, bỏ rơi mốc chặn dưới `6%`.
  * **E1:** Tạo ra 2 tuple riêng biệt: `6%` và `6.5%`.
  * **E2:** Trích xuất dạng khoảng `6 - 6.5%`.
- **Nguyên nhân khả dĩ:** Bộ tách số đơn lẻ không hỗ trợ biểu thức khoảng giá trị `A - B`.
- **Ảnh hưởng đến người dùng:** Đánh mất thông tin về biên độ dự báo.
- **Đề xuất thay đổi:** Thêm pattern nhận dạng cấu trúc khoảng `từ A đến B` hoặc `A - B`.

---

### Ca lỗi 9 (ID: UVN_BIZ_article-00042_1) - Lỗi trùng lặp dữ kiện do lặp từ (Tuple Redundancy)
- **item_id và loại lỗi:** `UVN_BIZ_article-00042_1` | Lỗi nhân bản tuple trùng lặp
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Lợi nhuận sau thuế của doanh nghiệp đạt 1.200 tỷ đồng, tăng so với lợi nhuận cùng kỳ."*
- **Gold hoặc đáp án tham chiếu:** 1 tuple duy nhất cho con số `1200 tỷ đồng`.
- **Prediction E0 / E1 / E2:**
  * **E0:** Sinh ra 2 tuple giống hệt nhau do từ khóa `lợi nhuận` xuất hiện 2 lần trong câu.
  * **E1:** Vẫn sinh ra 2 tuple.
  * **E2:** Bộ lọc Deduplication loại bỏ thành công tuple dư thừa.
- **Nguyên nhân khả dĩ:** Ghép cặp đa-đa giữa từ khóa và số lượng không qua tầng kiểm tra duy nhất.
- **Ảnh hưởng đến người dùng:** Số liệu bị nhân đôi trong bảng thống kê.
- **Đề xuất thay đổi:** Bắt buộc có bước lọc trùng (Deduplication) dựa trên khóa `(value, unit, period, evidence)`.

---

### Ca lỗi 10 (ID: UVN_BIZ_article-00049_2) - Lỗi gán nhầm chủ thể doanh nghiệp (Entity Association)
- **item_id và loại lỗi:** `UVN_BIZ_article-00049_2` | Lỗi liên kết sai thực thể sở hữu
- **Đầu vào / nguồn / chứng cứ hợp lệ:** *"Trong khi Hòa Phát lãi lớn, Hoa Sen chỉ ghi nhận lợi nhuận 300 tỷ đồng."*
- **Gold hoặc đáp án tham chiếu:** `indicator: "lợi nhuận Hoa Sen", value: "300", unit: "tỷ đồng", period: "unknown"`
- **Prediction E0 / E1 / E2:**
  * **E0:** `indicator: "lợi nhuận Hòa Phát"` (Sai chủ thể, gán nhầm sang Hòa Phát do đứng trước).
  * **E1:** `indicator: "lợi nhuận"` (Mất tên chủ thể).
  * **E2:** `indicator: "lợi nhuận Hoa Sen"` (Đúng chủ thể trong cùng mệnh đề).
- **Nguyên nhân khả dĩ:** Hiện tượng đa chủ thể trong cùng một câu văn phức hợp so sánh.
- **Ảnh hưởng đến người dùng:** Gán nhầm kết quả kinh doanh của doanh nghiệp này cho doanh nghiệp đối thủ.
- **Đề xuất thay đổi:** Kết hợp phân tích Dependency Parsing để liên kết ngữ pháp giữa Chủ ngữ và Vị ngữ.
