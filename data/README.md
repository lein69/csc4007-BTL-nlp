# THƯ MỤC DỮ LIỆU (DATA REPOSITORY)

Thư mục này quản lý toàn bộ dữ liệu 3 tầng (Raw, Processed, Gold) theo quy định của môn học:

## 1. Cấu trúc tệp tin
* `data_manifest.csv`: Bảng tổng kê dữ liệu với đầy đủ metadata nguồn gốc, ID, URL, license CC BY-NC 4.0 và phân chia split.
* `data_schema.md`: Đặc tả chi tiết các trường dữ liệu và cấu trúc bộ dữ kiện.
* `splits/`:
  * `train_ids.txt`: 120 mẫu huấn luyện / thử nghiệm.
  * `dev_ids.txt`: 30 mẫu kiểm tra và tinh chỉnh cấu hình.
  * `test_ids.txt`: 50 mẫu test bị khóa độc lập cho nghiệm thu.
* `annotations/`:
  * `annotation_guideline.md`: Hướng dẫn gắn nhãn chi tiết (v1.1).
  * `gold_labels.jsonl`: 439 fact tuples được chuẩn hóa đầy đủ `(indicator, value, unit, period, evidence)`.
  * `review_log.csv`: Nhật ký hậu kiểm chéo 25% mẫu giữa 2 người kiểm thử, độ đồng thuận đạt 96%.
* `raw/`:
  * `chunks_pool.jsonl`: 200 đoạn văn kinh tế trích xuất từ 116 bài báo chuyên mục Kinh doanh của `undertheseanlp/UVN-1`.

## 2. Cam kết Chống rò rỉ dữ liệu (Zero Leakage)
* Tập Train, Dev và Test được phân chia theo `document_id`.
* Không có hiện tượng hai đoạn văn cùng thuộc một bài báo gốc nằm ở hai tập split khác nhau.
