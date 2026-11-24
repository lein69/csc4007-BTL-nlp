# HƯỚNG DẪN GẮN NHÃN DỮ KIỆN KINH TẾ (ANNOTATION GUIDELINE)

**Mã đề tài:** ĐT02 – Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Phiên bản Guideline:** v1.1  
**Mục tiêu:** Chuẩn hóa quy trình gắn nhãn bộ dữ kiện: `(indicator, value, unit, period, evidence)` từ các đoạn văn bản báo chí kinh tế tiếng Việt.

---

## 1. Nguyên tắc tổng quát
1. **Chỉ trích xuất dữ kiện có thật trong văn bản:** Tuyệt đối không suy diễn, ngoại suy hay sử dụng kiến thức bên ngoài để bổ sung số liệu.
2. **Liên kết đúng thực thể - giá trị - mốc thời gian:** Một câu có thể chứa nhiều số liệu và nhiều chỉ tiêu; người gắn nhãn phải gán chính xác giá trị nào thuộc về chỉ tiêu nào.
3. **Mỗi bộ dữ kiện là một Tuple độc lập:**
   $$\text{Tuple} = (\text{indicator}, \text{value}, \text{unit}, \text{period}, \text{evidence})$$

---

## 2. Quy định chi tiết từng trường

### 2.1. Chỉ tiêu kinh tế (`indicator`)
* Bao gồm tên chỉ tiêu kết hợp với tên chủ thể (Doanh nghiệp, Tổ chức, Quốc gia hoặc Ngành hàng) nếu có.
* **Quy ước ranh giới (Boundary):**
  * Lấy cụm danh từ ngắn gọn, đầy đủ nghĩa nhất:
    * Ví dụ đúng: `doanh thu hợp nhất Vietcombank`, `tổng kim ngạch xuất khẩu`, `tăng trưởng GDP Việt Nam`.
    * Ví dụ sai: `đạt 15.000 tỷ`, `Vietcombank` (quá cụ thể hoặc thiếu chỉ tiêu).
* **Trường hợp so sánh:**
  * Nếu là tốc độ tăng/giảm: ghi rõ `tăng trưởng [chỉ tiêu]` hoặc `biến động [chỉ tiêu]`.

### 2.2. Giá trị định lượng (`value`)
* Chỉ trích xuất phần con số (chữ số và dấu phân tách).
* **Chuẩn hóa dấu số:**
  * Giữ nguyên giá trị gốc: `15.637`, `15,5`, `4.5`.
  * Khi gặp số âm hoặc số giảm: Thêm dấu trừ `-` nếu văn bản ghi rõ `giảm 4,5%` $\rightarrow$ `value: "-4.5"`.
  * Không đưa từ đơn vị vào trường này (ví dụ: `15 tỷ` thì `value: "15"`, không để `value: "15 tỷ"`).

### 2.3. Đơn vị đo lường (`unit`)
* Phải tách riêng khỏi con số.
* Danh mục các đơn vị hợp lệ phổ biến:
  * Tiền tệ: `tỷ đồng`, `triệu đồng`, `đồng`, `triệu USD`, `tỷ USD`, `USD`.
  * Tỷ lệ / Biến động: `%`, `phần trăm`, `điểm phần trăm`, `bps`.
  * Đơn vị đo lường khác: `tấn`, `thùng`, `USD/thùng`, `đồng/cổ phiếu`.
* Nếu số liệu là số đếm thuần túy (ví dụ: `34 dự án`): `unit: "dự án"`.

### 2.4. Kỳ thời gian (`period`)
* Mốc thời gian mà số liệu đó phản ánh.
* Các định dạng phổ biến:
  * Năm: `năm 2023`, `năm 2022`.
  * Quý: `quý III/2023`, `quý 1/2024`, `quý IV`.
  * Tháng: `tháng 10/2023`, `9 tháng đầu năm 2023`.
  * So sánh kỳ: `so với cùng kỳ năm trước`, `so với tháng trước`.
* **Chính sách đối với trường hợp không rõ (`unknown`):**
  * Nếu đoạn văn không đề cập bất kỳ mốc thời gian nào liên quan đến con số $\rightarrow$ Bắt buộc điền `"unknown"`.
  * Tuyệt đối không lấy ngày xuất bản bài báo để tự gán làm mốc thời gian của số liệu nếu bài báo không nói rõ.

### 2.5. Câu chứng cứ (`evidence`)
* Trích dẫn nguyên văn câu văn chứa số liệu và chỉ tiêu đó.
* Phải là chuỗi con (substring) chính xác nằm trong đoạn văn gốc.

---

## 3. Ví dụ minh họa thực tế

### Ví dụ 1: Câu phức chứa nhiều chỉ tiêu
* **Đoạn văn:**  
  > *"Quý III/2023, Tập đoàn Hòa Phát đạt doanh thu 28.766 tỷ đồng, giảm 16% so với cùng kỳ năm trước. Tuy nhiên, lợi nhuận sau thuế đạt 2.000 tỷ đồng, tăng mạnh so với mức lỗ 1.786 tỷ đồng cùng kỳ 2022."*
* **Nhãn chuẩn:**
  1. `Tuple 1:`
     * `indicator:` "doanh thu Hòa Phát"
     * `value:` "28766"
     * `unit:` "tỷ đồng"
     * `period:` "Quý III/2023"
     * `evidence:` "Quý III/2023, Tập đoàn Hòa Phát đạt doanh thu 28.766 tỷ đồng"
  2. `Tuple 2:`
     * `indicator:` "tăng trưởng doanh thu Hòa Phát"
     * `value:` "-16"
     * `unit:` "%"
     * `period:` "Quý III/2023 so với cùng kỳ năm trước"
     * `evidence:` "giảm 16% so với cùng kỳ năm trước"
  3. `Tuple 3:`
     * `indicator:` "lợi nhuận sau thuế Hòa Phát"
     * `value:` "2000"
     * `unit:` "tỷ đồng"
     * `period:` "Quý III/2023"
     * `evidence:` "lợi nhuận sau thuế đạt 2.000 tỷ đồng"
  4. `Tuple 4:`
     * `indicator:` "lợi nhuận sau thuế Hòa Phát cùng kỳ"
     * `value:` "-1786"
     * `unit:` "tỷ đồng"
     * `period:` "cùng kỳ 2022"
     * `evidence:` "so với mức lỗ 1.786 tỷ đồng cùng kỳ 2022"

---

## 4. Quy trình hậu kiểm chéo và tính hệ số thỏa thuận
1. **Annotator 1 (Người gắn nhãn chính):** Gắn nhãn toàn bộ các mẫu theo hướng dẫn trên.
2. **Annotator 2 (Người hậu kiểm chéo):** Gắn nhãn độc lập trên ít nhất 20% mẫu (tối thiểu 40–50 mẫu).
3. **Đo lường bất đồng:**
   * Tính toán chỉ số Cohen's Kappa trên quyết định gán nhãn thực thể và so khớp bộ tuple.
   * Tất cả các trường hợp bất đồng phải được ghi chép vào `review_log.csv` kèm lý do và phương án giải quyết cuối cùng.
