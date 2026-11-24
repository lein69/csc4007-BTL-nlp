"""
Mô hình E2: Two-Stage Pipeline (LLM Few-Shot + Schema Validation & Normalization)
Đặc điểm:
1. Giai đoạn 1 (Few-Shot LLM Extraction): Cung cấp các ví dụ mẫu phức tạp về câu đa chỉ tiêu,
   xử lý giảm âm, quy đổi tiền tệ kép trong ngoặc đơn và quy tắc gán 'unknown'.
2. Giai đoạn 2 (Post-Processing Schema Validation):
   - Chuẩn hóa đơn vị đo lường ('phần trăm' -> '%', 'euro' -> 'EUR', 'tỷ usd' -> 'tỷ USD')
   - Kiểm tra tính hợp lệ số học của 'value'
   - Lọc bỏ các tuple trùng lặp dữ kiện (Deduplication)
"""

import sys
import os
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.gemini_client import call_gemini_json

FEW_SHOT_PROMPT = """Bạn là chuyên gia trích xuất dữ kiện kinh tế tiếng Việt có kiểm chứng khoa học.
Nhiệm vụ: Trích xuất chính xác các bộ dữ kiện định lượng từ đoạn văn thành một JSON LIST các object:
- indicator: Tên chỉ tiêu kinh tế gắn với chủ thể (doanh nghiệp/quốc gia).
- value: Giá trị định lượng (nếu ngữ cảnh là giảm/sụt sút thì bắt buộc thêm dấu âm '-').
- unit: Đơn vị đo lường chuẩn ('tỷ đồng', '%', 'EUR', 'USD', 'triệu USD'...).
- period: Mốc thời gian. Nếu câu không nói rõ năm/quý/tháng thì điền 'unknown', không được tự ý bịa.
- evidence: Trích dẫn nguyên văn câu chứa thông tin đó.

Dưới đây là một số ví dụ chuẩn:
---
Ví dụ 1:
Đoạn văn: "Quý III/2023, Hòa Phát đạt doanh thu 28.766 tỷ đồng, giảm 16% so với cùng kỳ năm trước."
Kết quả:
[
  {"indicator": "doanh thu Hòa Phát", "value": "28766", "unit": "tỷ đồng", "period": "Quý III/2023", "evidence": "Quý III/2023, Hòa Phát đạt doanh thu 28.766 tỷ đồng, giảm 16% so với cùng kỳ năm trước."},
  {"indicator": "tăng trưởng doanh thu Hòa Phát", "value": "-16", "unit": "%", "period": "Quý III/2023 so với cùng kỳ năm trước", "evidence": "giảm 16% so với cùng kỳ năm trước."}
]

Ví dụ 2:
Đoạn văn: "Dư nợ tín dụng đối với nền kinh tế đạt trên 13,5 triệu tỷ đồng."
Kết quả:
[
  {"indicator": "dư nợ tín dụng nền kinh tế", "value": "13.5", "unit": "triệu tỷ đồng", "period": "unknown", "evidence": "Dư nợ tín dụng đối với nền kinh tế đạt trên 13,5 triệu tỷ đồng."}
]
---

Hãy trích xuất cho đoạn văn sau:
\"\"\"{text}\"\"\"
"""

class RefinedPipelineE2:
    def __init__(self, config=None):
        self.config = config or {}
        self.model_name = self.config.get("model_name", "gemini-3-flash-preview")

    def normalize_unit(self, unit_str):
        u = str(unit_str).strip().lower()
        if u in ["phần trăm", "pt"]:
            return "%"
        if u == "euro":
            return "EUR"
        if u == "usd":
            return "USD"
        if u in ["tỷ usd", "ty usd"]:
            return "tỷ USD"
        if u in ["triệu usd", "trieu usd"]:
            return "triệu USD"
        return str(unit_str).strip()

    def extract(self, text):
        prompt = FEW_SHOT_PROMPT.replace("{text}", text)
        try:
            raw_tuples = call_gemini_json(prompt, model_name=self.model_name)
        except Exception as e:
            print(f"[E2] Lỗi gọi LLM: {e}")
            raw_tuples = []

        validated_tuples = []
        seen = set()
        t_id = 1

        for r in raw_tuples:
            ind = str(r.get("indicator", "chỉ tiêu kinh tế")).strip()
            raw_val = str(r.get("value", "0")).replace(",", ".").strip()
            raw_unit = str(r.get("unit", "")).strip()
            period = str(r.get("period", "unknown")).strip()
            evidence = str(r.get("evidence", text)).strip()

            # 1. Kiểm chuẩn số học
            # Tách lấy phần số nếu model lỡ đưa đơn vị vào value
            clean_num = re.sub(r"[^\d.-]", "", raw_val)
            if not clean_num:
                continue

            # 2. Chuẩn hóa đơn vị
            norm_unit = self.normalize_unit(raw_unit)

            # 3. Lọc trùng lặp dữ kiện (Deduplication)
            dedup_key = (clean_num, norm_unit, period)
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            validated_tuples.append({
                "tuple_id": f"E2_T{t_id}",
                "indicator": ind,
                "value": clean_num,
                "unit": norm_unit,
                "period": period,
                "evidence": evidence
            })
            t_id += 1

        return validated_tuples
