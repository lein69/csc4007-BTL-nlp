# TÀI LIỆU LƯỢC ĐỒ DỮ LIỆU (DATA SCHEMA)

**Đề tài 2 (ĐT02):** Trích xuất thực thể và dữ kiện kinh tế từ tin tức tiếng Việt  
**Học phần:** CSC4007 – Xử lý ngôn ngữ tự nhiên  

---

## 1. Lược đồ file `data_manifest.csv`

| Tên cột | Kiểu dữ liệu | Bắt buộc | Mô tả & Quy ước | Ví dụ |
| :--- | :--- | :---: | :--- | :--- |
| `item_id` | String | Có | Định danh duy nhất của từng đoạn văn phân tích | `UVN_BIZ_102_1` |
| `document_id` | String | Có | Định danh bài báo gốc trong corpus UVN-1 | `102` |
| `source_name` | String | Có | Tên nguồn thu thập | `UVN-1/undertheseanlp` |
| `source_url` | String | Có | Đường dẫn bài viết gốc | `https://vnexpress.net/...` |
| `source_version` | String | Có | Phiên bản snapshot của nguồn | `1.0.0` |
| `retrieved_at` | Date (YYYY-MM-DD) | Có | Ngày nhóm truy xuất dữ liệu | `2026-11-24` |
| `published_at` | Date / String | Có | Ngày phát hành từ nguồn (nếu thiếu ghi `null`) | `2023-10-15` |
| `language` | String | Có | Mã ngôn ngữ ISO 639-1 | `vi` |
| `original_category` | String | Có | Chuyên mục gốc của nguồn dữ liệu | `Kinh doanh` |
| `task_label` | String | Có | Tên nhiệm vụ NLP đang giải quyết | `fact_tuple_extraction` |
| `license_status` | String | Có | Giấy phép bản quyền | `CC BY-NC 4.0` |
| `split` | String | Có | Tập phân chia: `train`, `dev`, hoặc `test` | `test` |
| `notes` | String | Không | Ghi chú thêm về đoạn dữ liệu | `Chứa số liệu xuất nhập khẩu` |

---

## 2. Lược đồ Fact Tuple (`gold_labels.jsonl` và `test_predictions_*.csv`)

Mỗi mẫu dữ liệu bao gồm văn bản gốc và một danh sách các bộ dữ kiện (tuples):

```json
{
  "item_id": "UVN_BIZ_105_1",
  "document_id": "105",
  "text": "Năm 2023, tổng kim ngạch xuất nhập khẩu của Việt Nam ước đạt 683 tỷ USD, giảm 6,6% so với năm trước.",
  "tuples": [
    {
      "tuple_id": "T1",
      "indicator": "tổng kim ngạch xuất nhập khẩu Việt Nam",
      "value": "683",
      "unit": "tỷ USD",
      "period": "năm 2023",
      "evidence": "Năm 2023, tổng kim ngạch xuất nhập khẩu của Việt Nam ước đạt 683 tỷ USD"
    },
    {
      "tuple_id": "T2",
      "indicator": "tăng trưởng xuất nhập khẩu Việt Nam",
      "value": "-6.6",
      "unit": "%",
      "period": "năm 2023 so với năm trước",
      "evidence": "giảm 6,6% so với năm trước"
    }
  ]
}
```

### Chi tiết các trường trong Tuple:
1. **`indicator` (Chỉ tiêu / Thực thể):**
   * Định danh chỉ tiêu kinh tế gắn liền với chủ thể (doanh nghiệp hoặc quốc gia).
   * Ví dụ: `doanh thu FPT`, `lợi nhuận sau thuế Vietcombank`, `tổng mức bán lẻ hàng hóa`, `tăng trưởng GDP`.
2. **`value` (Giá trị định lượng):**
   * Chuỗi số học biểu diễn giá trị đo lường được.
   * Xử lý số âm khi có từ ngữ chỉ giảm/âm: `giảm 6,6%` $\rightarrow$ `-6.6`.
3. **`unit` (Đơn vị đo lường):**
   * Đơn vị chuẩn kèm theo số liệu: `tỷ đồng`, `triệu USD`, `%`, `USD/thùng`, `điểm phần trăm`.
4. **`period` (Kỳ thời gian):**
   * Mốc thời gian áp dụng số liệu: `quý III/2023`, `tháng 10/2023`, `năm 2022`, `9 tháng đầu năm 2023`.
   * **Nếu không có trong câu:** Ghi rõ `unknown` (tuyệt đối không bịa đặt).
5. **`evidence` (Chứng cứ nguồn):**
   * Chuỗi ký tự trích dẫn nguyên văn từ câu chứa số liệu và chỉ tiêu đó.
