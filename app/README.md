# HƯỚNG DẪN CHẠY ỨNG DỤNG DEMO (APP README)
**Đề tài 2 (ĐT02):** Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Nhóm thực hiện:** Nhóm 4 | **Trường:** Đại học Đại Nam  

Ứng dụng trực quan hóa chức năng trích xuất bộ dữ kiện `(indicator, value, unit, period, evidence)` từ tin tức kinh tế tiếng Việt.

## 1. Cài đặt thư viện phụ thuộc
Trước khi khởi chạy, đảm bảo đã cài đặt streamlit và pandas:
```bash
pip install streamlit pandas
```

## 2. Lệnh khởi chạy ứng dụng
Từ thư mục gốc của dự án (`d:\Tu Hoc\NLP`), chạy lệnh:
```bash
streamlit run app/app.py
```

## 3. Các tính năng chính trên giao diện
1. **Trích xuất trực tiếp:** Cho phép dán đoạn văn bản bất kỳ hoặc chọn nhanh 3 mẫu văn bản báo chí tiêu biểu, tùy chọn 1 trong 3 mô hình (E0, E1, E2) để xem bảng kết quả và các câu chứng cứ trích dẫn.
2. **So sánh đối chứng:** Hiển thị song song kết quả của cả 3 cấu hình E0 (Baseline), E1 (Mệnh đề cú pháp) và E2 (Pipeline kiểm chuẩn) trên cùng một văn bản.
3. **Báo cáo thực nghiệm:** Hiển thị bảng chỉ số F1, Exact Match, tỷ lệ lỗi số liệu và mốc thời gian được tính toán tự động từ tập Test độc lập.
