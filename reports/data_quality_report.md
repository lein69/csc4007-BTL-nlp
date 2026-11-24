# BÁO CÁO KIỂM TRA CHẤT LƯỢNG DỮ LIỆU (DATA QUALITY REPORT)

**Mã đề tài:** ĐT02 – Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Ngày kiểm toán:** 2026-11-24  
**Người thực hiện:** Nhóm nghiên cứu CSC4007  

---

## 1. Kiểm tra Lược đồ (Schema Validation)
* **Tổng số dòng đọc được:** 200 / 200 đoạn văn bản.
* **Tỷ lệ trường bắt buộc bị rỗng:** 0% (tất cả các trường `item_id`, `document_id`, `text`, `split` đều đầy đủ).
* **Bản mã Unicode:** 100% văn bản đã được chuẩn hóa về định dạng UTF-8 chuẩn NFC.

## 2. Kiểm tra Nội dung & Rà soát văn bản
* **Kiểm tra độ dài văn bản:**
  * Độ dài trung bình: 185 ký tự / đoạn.
  * Đoạn ngắn nhất: 65 ký tự.
  * Đoạn dài nhất: 420 ký tự.
* **Loại bỏ thẻ HTML và khoảng trắng thừa:** Toàn bộ thẻ HTML từ nguồn báo đã được bóc tách và làm sạch triệt để.
* **Phát hiện bản tin đăng lại và gần trùng (Near-duplicates):**
  * Đã quét tương đồng bằng thuật toán SequenceMatcher.
  * Phát hiện **3 cặp đoạn văn gần trùng** do các báo đăng tải cùng một thông cáo báo chí (ví dụ bài `article-00011` và `article-00012`).
  * *Biện pháp xử lý:* Đưa vào danh sách theo dõi để cô lập, bảo đảm không bị phân rải vào hai tập khác nhau (đảm bảo chia split theo `document_id`).

## 3. Kiểm toán số liệu kinh tế và đơn vị
* **Xử lý số thập phân:** Giữ nguyên các định dạng `15,5%` và `15.637 tỷ đồng`, chuẩn hóa về dấu chấm thập phân khi lưu giá trị `value`.
* **Xử lý số âm/tăng giảm:** Đã kiểm tra các động từ `giảm`, `mất`, `thâm hụt` để gán dấu âm `-` vào `value` (tránh sai sót về mặt bản chất kinh tế).
* **Đơn vị:** 100% đơn vị được phân tách riêng khỏi con số, bao phủ các loại: `tỷ đồng`, `triệu USD`, `%`, `USD/thùng`, `tấn`...

## 4. Kiểm tra Chống rò rỉ dữ liệu (Data Leakage Audit)
* **Nguyên tắc phân chia:** Split dựa hoàn toàn trên `document_id`.
* **Kiểm tra giao thoa tập dữ liệu:**
  * Giao giữa Train và Dev: 0 văn bản trùng ID.
  * Giao giữa Train và Test: 0 văn bản trùng ID.
  * Giao giữa Dev và Test: 0 văn bản trùng ID.
* $ightarrow$ **Kết luận:** Hoàn toàn không xảy ra rò rỉ dữ liệu (Zero Data Leakage).

## 5. Kết quả Hậu kiểm chéo và Độ đồng thuận (Inter-Annotator Agreement)
* **Số mẫu kiểm toán chéo:** 50 mẫu (đạt 25.0% tổng tập dữ liệu, vượt ngưỡng tối thiểu 20%).
* **Tỷ lệ đồng thuận ban đầu:** 96.0%.
* **Hệ số Cohen's Kappa:** $\kappa = 0.88$ (độ đồng thuận cao).
* **Các nguyên nhân bất đồng chính đã xử lý:**
  1. *Ranh giới chỉ tiêu (Span boundary):* Ưu tiên mở rộng cụm từ để giữ tên tổ chức/doanh nghiệp.
  2. *Thời gian không rõ:* Thống nhất gán `period: "unknown"` thay vì suy diễn từ ngày xuất bản bài viết.
  3. *Dấu âm định lượng:* Bắt buộc thêm dấu âm khi văn bản mô tả mức độ sụt giảm.
