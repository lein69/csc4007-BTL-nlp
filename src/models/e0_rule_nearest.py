"""
Mô hình E0: Baseline Regex + Nearest Neighbor Heuristic
Cơ chế:
1. Regex tìm kiếm các cặp (số, đơn vị)
2. Tìm từ khóa chỉ tiêu và mốc thời gian gần nhất trong cùng câu dựa trên khoảng cách ký tự
3. Không xử lý mệnh đề phức tạp, không tự động đảo dấu âm khi có từ 'giảm'
"""

import re

class BaselineE0:
    def __init__(self, config=None):
        self.config = config or {}
        self.num_unit_pattern = re.compile(
            r"(\b\d+([.,]\d+)?)\s*(tỷ đồng|nghìn tỷ|triệu đồng|tỷ usd|triệu usd|euro|usd|%|phần trăm|điểm phần trăm|đồng/cổ phiếu|usd/thùng|tấn)",
            re.IGNORECASE
        )
        self.period_pattern = re.compile(
            r"(quý\s+[iIvVxX\d]+(/\d{4})?|năm\s+\d{4}|tháng\s+\d{1,2}(/\d{4})?|trong vòng\s+\d+\s+năm)",
            re.IGNORECASE
        )
        self.indicator_pattern = re.compile(
            r"(doanh thu|lợi nhuận|tiền thuế|thuế nhập khẩu|kim ngạch|xuất khẩu|nhập khẩu|gdp|cpi|lạm phát|lãi suất|vốn đầu tư|dư nợ|giá xăng|giá dầu|thị phần|sản lượng|tiết kiệm)",
            re.IGNORECASE
        )

    def extract(self, text):
        tuples = []
        sentences = re.split(r"(?<=[.!?])\s+", text)
        t_id = 1
        
        for sent in sentences:
            sent_str = sent.strip()
            if not sent_str:
                continue
                
            matches = list(self.num_unit_pattern.finditer(sent_str))
            if not matches:
                continue
                
            # Tìm tất cả indicators trong câu kèm vị trí
            indicators = [(m.start(), m.group(0)) for m in self.indicator_pattern.finditer(sent_str)]
            # Tìm tất cả periods trong câu kèm vị trí
            periods = [(m.start(), m.group(0)) for m in self.period_pattern.finditer(sent_str)]
            
            for m in matches:
                val = m.group(1).replace(",", ".")
                unit = m.group(3).strip()
                val_pos = m.start()
                
                # Heuristic gán indicator gần nhất theo khoảng cách
                best_ind = "chỉ tiêu kinh tế"
                if indicators:
                    best_ind = min(indicators, key=lambda x: abs(x[0] - val_pos))[1]
                    
                # Heuristic gán period gần nhất theo khoảng cách
                best_period = "unknown"
                if periods:
                    best_period = min(periods, key=lambda x: abs(x[0] - val_pos))[1]
                    
                tuples.append({
                    "tuple_id": f"E0_T{t_id}",
                    "indicator": best_ind,
                    "value": val,  # Không xử lý dấu âm khi giảm
                    "unit": unit,
                    "period": best_period,
                    "evidence": sent_str
                })
                t_id += 1
                
        return tuples
