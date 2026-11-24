# NHẬT KÝ SỬ DỤNG TRÍ TUỆ NHÂN TẠO (AI USAGE LOG)

**Học phần:** CSC4007 – Xử lý ngôn ngữ tự nhiên  
**Đề tài:** ĐT02 – Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Nhóm thực hiện:** Nhóm 4 

---

| STT | Thời điểm | Công cụ / Model | Mục đích sử dụng | Lời nhắc (Prompt) tóm tắt | Nội dung sinh ra | Kiểm chứng & Hậu kiểm của con người |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| 1 | 2026-11-24 | Claude / DeepMind Antigravity | Hỗ trợ thiết kế khung kiến trúc thư mục chuẩn | "Đề xuất cấu trúc thư mục BTL NLP chuẩn hóa theo đề cương môn học" | Cây thư mục `data`, `src`, `evaluation`, `reports`, `app` | Sinh viên trực tiếp kiểm tra và tinh chỉnh theo quy định mục 10.1 |
| 2 | 2026-11-24 | Python Scripting Assistant | Hỗ trợ viết regex nhận diện số và đơn vị kinh tế | "Viết regex nhận diện số thực, tỷ lệ phần trăm và đơn vị tiền tệ tiếng Việt" | Hàm regex pattern cho `value` và `unit` | Sinh viên chạy test thử trên 20 mẫu câu thực tế, bổ sung xử lý số âm khi có từ 'giảm' |
| 3 | 2026-11-24 | NLP Code Assistant | Hỗ trợ xây dựng giao diện tương tác Streamlit | "Tạo giao diện Streamlit hiển thị bảng dữ kiện và đối chứng E0, E1, E2" | Mã nguồn `app/app.py` | Sinh viên tự chạy trên máy cục bộ, kiểm tra độ phản hồi và hiển thị |
| 4 | 2026-11-24 | Annotation Helper | Hỗ trợ rà soát kiểm tra chéo các ca biên giới | "Phân tích ranh giới cụm danh từ chỉ tiêu kinh tế phức" | Danh sách phân tích ngữ nghĩa | Sinh viên đối chiếu với `annotation_guideline.md` và tự quyết định nhãn cuối |

---
**Cam kết:** Mọi mã nguồn thực nghiệm, dữ liệu đánh giá và phân tích lỗi đều do sinh viên kiểm định, kiểm thử và chịu trách nhiệm khoa học 100%. Không sao chép nguyên trạng mà thiếu hiểu biết bản chất thuật toán.
