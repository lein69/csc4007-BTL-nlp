# GIAO THỨC ĐÁNH GIÁ (EVALUATION PROTOCOL)

**Đề tài 2 (ĐT02):** Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Học phần:** CSC4007 – Xử lý ngôn ngữ tự nhiên  
**Phiên bản:** 1.0 (Khóa tập test)

---

## 1. Nguyên tắc bất biến
1. **Khóa tập Test:** Tuyệt đối không dùng tập Test (gồm 50 mẫu tại `data/splits/test_ids.txt`) để tinh chỉnh tham số, luật hay prompt. Mọi quyết định lựa chọn cấu hình đều phải dựa trên tập Dev.
2. **Đo lường tự động có thể tái lập:** Tất cả các chỉ số (Precision, Recall, F1, Exact Match, Error Rates) đều được tính toán tự động bằng mã nguồn `src/evaluate.py`, không chấp nhận nhập số liệu thủ công vào báo cáo.
3. **Tính minh bạch:** Mỗi lần chạy thí nghiệm đều xuất ra file kết quả chi tiết từng mẫu tại `evaluation/test_predictions_{RUN_ID}.csv`.

---

## 2. Tiêu chí và Chỉ số đánh giá (Evaluation Metrics)

### 2.1. Fact Tuple Exact Match (EM)
* Một bộ dữ kiện dự đoán $\hat{t} = (\hat{i}, \hat{v}, \hat{u}, \hat{p})$ được coi là khớp chính xác với nhãn gold $t = (i, v, u, p)$ khi và chỉ khi:
  $$\hat{v} = v \quad \land \quad \hat{u} = u \quad \land \quad \hat{p} = p$$
* Tỷ lệ Exact Match:
  $$\text{EM Rate} = \frac{\text{Số tuples khớp chính xác}}{\text{Tổng số tuples trong tập Gold}}$$

### 2.2. Fact Tuple Normalized Match (NM) & Macro-F1
* Cho phép chuẩn hóa:
  * Số học: Chấp nhận dung sai float nếu khác biệt kiểu định dạng dấu thập phân.
  * Đơn vị: Chấp nhận quy đổi tương đương (`%` $\leftrightarrow$ `phần trăm`, `USD` $\leftrightarrow$ `tỷ USD` khi con số đã đồng bộ).
  * Kỳ thời gian: Chấp nhận chuỗi con nếu kỳ trích xuất bao hàm đầy đủ thông tin của nhãn gold.
  * Chỉ tiêu: Độ tương đồng chuỗi ký tự (String Similarity) $\ge 0.4$.
* Từ đó tính toán:
  $$\text{Precision} = \frac{|\text{Predictions} \cap \text{Gold}|}{|\text{Predictions}|}, \quad \text{Recall} = \frac{|\text{Predictions} \cap \text{Gold}|}{|\text{Gold}|}, \quad \text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 2.3. Các chỉ số phân tích lỗi chuyên biệt (Granular Error Metrics)
* **Numeric Error Rate:** Tỷ lệ số liệu bị trích xuất sai giá trị hoặc sai dấu âm/dương.
* **Period Mismatch Rate:** Tỷ lệ gán nhầm mốc thời gian giữa các mệnh đề trong cùng đoạn văn.
