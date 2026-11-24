"""
Module: gemini_client.py
Hỗ trợ gọi Gemini API với cơ chế tự động đọc API Key từ .env,
hạn chế tốc độ gọi (Rate Limiting), bộ nhớ đệm (Cache) và Fallback an toàn.
"""

import os
import json
import time
import re
import urllib.request
import urllib.error

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")
CACHE_PATH = os.path.join(BASE_DIR, "data", ".llm_cache.json")

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key and os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    return api_key

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

_CACHE = load_cache()

def fallback_extract(text):
    """Fallback trích xuất khi LLM gặp sự cố mạng hoặc chạm giới hạn RPM."""
    tuples = []
    num_unit = re.compile(
        r"(-?\b\d+([.,]\d+)?)\s*(tỷ đồng|nghìn tỷ|triệu đồng|tỷ usd|triệu usd|euro|usd|%|phần trăm|điểm phần trăm|đồng/cổ phiếu|usd/thùng|tấn)",
        re.IGNORECASE
    )
    period_pattern = re.compile(
        r"(quý\s+[iIvVxX\d]+(/\d{4})?|năm\s+\d{4}|tháng\s+\d{1,2}(/\d{4})?|trong vòng\s+\d+\s+năm|so với cùng kỳ(\s+năm trước)?|so với năm trước|cùng kỳ\s+\d{4})",
        re.IGNORECASE
    )
    ind_pattern = re.compile(
        r"(doanh thu(\s+hợp nhất)?|lợi nhuận(\s+sau thuế)?|tiền thuế|thuế nhập khẩu|kim ngạch|xuất khẩu|nhập khẩu|gdp|cpi|lạm phát|lãi suất|vốn đầu tư|dư nợ|giá xăng|giá dầu|thị phần|sản lượng|tiết kiệm)",
        re.IGNORECASE
    )
    sentences = re.split(r"(?<=[.!?])\s+", text)
    t_id = 1
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        p_m = period_pattern.search(s)
        period = p_m.group(0).strip() if p_m else "unknown"
        for m in num_unit.finditer(s):
            val = m.group(1).replace(",", ".")
            unit = m.group(3).strip()
            ind_m = ind_pattern.search(s)
            ind = ind_m.group(0).strip() if ind_m else "chỉ tiêu kinh tế"
            prefix = s[max(0, m.start() - 25) : m.start()].lower()
            if any(w in prefix for w in ["giảm", "mất", "sụt"]):
                if not val.startswith("-"):
                    val = f"-{val}"
            tuples.append({
                "indicator": ind,
                "value": val,
                "unit": unit,
                "period": period,
                "evidence": s
            })
            t_id += 1
    return tuples

def call_gemini_json(prompt, model_name="gemini-3-flash-preview", max_retries=2):
    """Gọi Gemini API và nhận kết quả dạng JSON List, có cache và fallback."""
    global _CACHE
    cache_key = f"{model_name}::{prompt}"
    if cache_key in _CACHE:
        return _CACHE[cache_key]
        
    api_key = get_api_key()
    if not api_key:
        return fallback_extract(prompt)
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.1
        }
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                text_out = resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
                
                parsed = json.loads(text_out)
                if isinstance(parsed, dict) and "tuples" in parsed:
                    parsed = parsed["tuples"]
                elif isinstance(parsed, dict):
                    parsed = [parsed]
                    
                _CACHE[cache_key] = parsed
                save_cache(_CACHE)
                time.sleep(2.0) # Nghỉ 2s giữa các request
                return parsed
        except urllib.error.HTTPError as e:
            if e.code == 429: # Rate limit
                print(f"[Gemini API] Bị chạm trần RPM, đợi 12 giây trước khi thử lại lần {attempt+1}...")
                time.sleep(12)
            else:
                time.sleep(2)
        except Exception as e:
            time.sleep(1.5)
            
    # Nếu hết số lần retry do 429, dùng fallback và lưu cache
    fb = fallback_extract(prompt)
    _CACHE[cache_key] = fb
    save_cache(_CACHE)
    return fb
