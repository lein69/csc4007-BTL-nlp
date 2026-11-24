"""
Mô hình E1: LLM Zero-Shot Fact Tuple Extraction (Gemini Flash Native JSON)
Đặc điểm:
1. Sử dụng mô hình ngôn ngữ lớn (Gemini 3 Flash Preview) ở chế độ Zero-Shot
2. Sử dụng Native JSON Output Mode để sinh trực tiếp cấu trúc bộ dữ kiện (indicator, value, unit, period, evidence)
3. Không cung cấp ví dụ mẫu (Zero-shot) để kiểm chứng khả năng hiểu ngữ nghĩa cơ bản của LLM
"""

import sys
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.gemini_client import call_gemini_json

class RelationModelE1:
    def __init__(self, config=None):
        self.config = config or {}
        self.model_name = self.config.get("model_name", "gemini-3-flash-preview")

    def extract(self, text):
        prompt = f"""Bạn là một chuyên gia trích xuất thông tin kinh tế tiếng Việt.
Nhiệm vụ: Trích xuất tất cả các bộ dữ kiện định lượng trong đoạn văn dưới đây.
Định dạng đầu ra: Một JSON LIST chứa các object có các trường:
- indicator: Tên chỉ tiêu kinh tế kèm chủ thể (doanh nghiệp hoặc quốc gia), ví dụ: 'doanh thu Hòa Phát', 'tổng kim ngạch xuất khẩu'.
- value: Giá trị số (nếu có từ 'giảm', 'mất', 'âm' thì thêm dấu âm '-').
- unit: Đơn vị đo lường (ví dụ: 'tỷ đồng', '%', 'triệu USD', 'USD/thùng').
- period: Mốc thời gian áp dụng số liệu đó. Nếu văn bản không nêu mốc thời gian rõ ràng, bắt buộc ghi 'unknown'.
- evidence: Câu văn trích dẫn nguyên văn trong đoạn văn chứa dữ kiện đó.

Đoạn văn bản cần trích xuất:
\"\"\"{text}\"\"\"
"""
        try:
            results = call_gemini_json(prompt, model_name=self.model_name)
            tuples = []
            for idx, r in enumerate(results):
                tuples.append({
                    "tuple_id": f"E1_T{idx+1}",
                    "indicator": str(r.get("indicator", "chỉ tiêu kinh tế")).strip(),
                    "value": str(r.get("value", "0")).replace(",", ".").strip(),
                    "unit": str(r.get("unit", "")).strip(),
                    "period": str(r.get("period", "unknown")).strip(),
                    "evidence": str(r.get("evidence", text)).strip()
                })
            return tuples
        except Exception as e:
            print(f"[E1] Lỗi trích xuất: {e}")
            return []
