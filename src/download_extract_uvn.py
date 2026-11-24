"""
Script: download_extract_uvn.py
Nhiệm vụ:
1. Tải dataset undertheseanlp/UVN-1 từ Hugging Face
2. Lọc các bài viết chuyên mục 'Kinh doanh'
3. Phân tách và trích chọn 200 đoạn văn (chunks) chứa dữ kiện kinh tế (chỉ tiêu, số liệu, đơn vị, mốc thời gian)
4. Phân chia Train (120), Dev (30), Test (50) theo quy tắc KHÔNG RÒ RỈ (chia theo document_id)
5. Xuất data_manifest.csv và danh sách split IDs
"""

import os
import re
import json
import unicodedata
import pandas as pd
from datetime import datetime
from datasets import load_dataset

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
SPLIT_DIR = os.path.join(DATA_DIR, "splits")
RAW_DIR = os.path.join(DATA_DIR, "raw")
MANIFEST_PATH = os.path.join(DATA_DIR, "data_manifest.csv")

INDICATOR_KEYWORDS = [
    r"doanh thu", r"lợi nhuận", r"lãi ròng", r"tăng trưởng", r"kim ngạch",
    r"xuất khẩu", r"nhập khẩu", r"gdp", r"cpi", r"lạm phát", r"lãi suất",
    r"vốn đầu tư", r"fdi", r"tổng mức bán lẻ", r"giá xăng", r"giá dầu",
    r"chỉ số", r"dư nợ", r"huy động", r"tỷ giá", r"thị phần", r"sản lượng"
]

UNIT_KEYWORDS = [
    r"tỷ đồng", r"nghìn tỷ", r"triệu usd", r"tỷ usd", r"%", r"phần trăm",
    r"điểm phần trăm", r"usd/thùng", r"đồng/cổ phiếu", r"tấn", r"triệu đồng"
]

def clean_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text)
    # Loại bỏ thẻ html nếu có
    text = re.sub(r"<[^>]+>", " ", text)
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_candidate_chunks(article_content, max_chunk_sentences=3):
    """Chia văn bản thành các đoạn 2-3 câu chứa ít nhất 1 chỉ tiêu kinh tế, 1 số liệu và 1 đơn vị."""
    # Tách câu cơ bản tiếng Việt
    sentences = re.split(r"(?<=[.!?])\s+", article_content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    candidates = []
    i = 0
    while i < len(sentences):
        # Ghép 2-3 câu thành 1 chunk
        chunk_sentences = sentences[i : i + max_chunk_sentences]
        chunk_text = " ".join(chunk_sentences)
        
        lower_text = chunk_text.lower()
        has_indicator = any(re.search(kw, lower_text) for kw in INDICATOR_KEYWORDS)
        has_unit = any(re.search(kw, lower_text) for kw in UNIT_KEYWORDS)
        has_digit = bool(re.search(r"\d+([.,]\d+)?", chunk_text))
        
        if has_indicator and has_unit and has_digit and len(chunk_text) >= 60:
            candidates.append(chunk_text)
            i += max_chunk_sentences # Bước nhảy để tránh trùng lặp câu quá nhiều
        else:
            i += 1
            
    return candidates

def main():
    print("--> Bắt đầu tải tập dữ liệu undertheseanlp/UVN-1...")
    dataset = load_dataset("undertheseanlp/UVN-1", split="train")
    print(f"Tổng số bài báo tải về: {len(dataset)}")
    
    # Lọc bài viết Kinh doanh
    biz_articles = [doc for doc in dataset if doc.get("category") == "Kinh doanh"]
    print(f"Số lượng bài viết chuyên mục Kinh doanh: {len(biz_articles)}")
    
    selected_items = []
    doc_chunk_count = {}
    
    # Duyệt qua các bài viết và chọn các chunk đại diện
    for doc in biz_articles:
        doc_id = str(doc.get("id", ""))
        title = clean_text(doc.get("title", ""))
        content = clean_text(doc.get("content", ""))
        publish_date = doc.get("publish_date")
        if not publish_date or publish_date.strip() == "":
            publish_date = "null"
        source_url = doc.get("url", "")
        source_name = doc.get("source", "UVN-1/undertheseanlp")
        
        chunks = extract_candidate_chunks(content)
        # Chỉ lấy tối đa 2 chunk chất lượng nhất mỗi bài báo để đảm bảo tính đa dạng ngữ cảnh
        for idx, chunk in enumerate(chunks[:2]):
            item_id = f"UVN_BIZ_{doc_id}_{idx+1}"
            selected_items.append({
                "item_id": item_id,
                "document_id": doc_id,
                "title": title,
                "text": chunk,
                "source_name": source_name,
                "source_url": source_url,
                "source_version": "1.0.0",
                "retrieved_at": datetime.now().strftime("%Y-%m-%d"),
                "published_at": publish_date,
                "language": "vi",
                "original_category": "Kinh doanh",
                "task_label": "fact_tuple_extraction",
                "license_status": "CC BY-NC 4.0",
                "notes": "Đoạn văn trích xuất chứa số liệu và thực thể kinh tế"
            })
            if len(selected_items) >= 200:
                break
        if len(selected_items) >= 200:
            break
            
    print(f"Đã trích chọn thành công {len(selected_items)} đoạn văn kinh tế đa dạng.")
    
    # Phân chia Train/Dev/Test theo document_id để CHỐNG RÒ RỈ (Data Leakage Prevention)
    # Target: Train ~ 120, Dev ~ 30, Test = 50
    # Gom item_id theo document_id
    doc_to_items = {}
    for it in selected_items:
        d_id = it["document_id"]
        if d_id not in doc_to_items:
            doc_to_items[d_id] = []
        doc_to_items[d_id].append(it)
        
    unique_doc_ids = list(doc_to_items.keys())
    
    test_docs = []
    test_items_count = 0
    # Lấy tài liệu cho Test trước (khóa đúng 50 mẫu)
    for d_id in unique_doc_ids:
        if test_items_count + len(doc_to_items[d_id]) <= 50:
            test_docs.append(d_id)
            test_items_count += len(doc_to_items[d_id])
        if test_items_count >= 50:
            break
            
    remaining_docs = [d_id for d_id in unique_doc_ids if d_id not in test_docs]
    
    dev_docs = []
    dev_items_count = 0
    for d_id in remaining_docs:
        if dev_items_count + len(doc_to_items[d_id]) <= 30:
            dev_docs.append(d_id)
            dev_items_count += len(doc_to_items[d_id])
        if dev_items_count >= 30:
            break
            
    train_docs = [d_id for d_id in remaining_docs if d_id not in dev_docs]
    
    # Gán split cho từng item
    train_ids, dev_ids, test_ids = [], [], []
    for it in selected_items:
        d_id = it["document_id"]
        if d_id in test_docs:
            it["split"] = "test"
            test_ids.append(it["item_id"])
        elif d_id in dev_docs:
            it["split"] = "dev"
            dev_ids.append(it["item_id"])
        else:
            it["split"] = "train"
            train_ids.append(it["item_id"])
            
    print(f"Phân chia hoàn tất: Train={len(train_ids)}, Dev={len(dev_ids)}, Test={len(test_ids)}")
    print(f"Số lượng Document ID duy nhất: {len(unique_doc_ids)} (Test docs: {len(test_docs)}, Dev docs: {len(dev_docs)}, Train docs: {len(train_docs)})")
    
    # Lưu data_manifest.csv
    df_manifest = pd.DataFrame(selected_items)
    # Chuẩn hóa cột theo đúng hướng dẫn mục 5.2
    cols_order = [
        "item_id", "document_id", "source_name", "source_url", "source_version",
        "retrieved_at", "published_at", "language", "original_category",
        "task_label", "license_status", "split", "notes"
    ]
    df_manifest[cols_order].to_csv(MANIFEST_PATH, index=False, encoding="utf-8-sig")
    print(f"Đã lưu data_manifest.csv tại: {MANIFEST_PATH}")
    
    # Lưu splits
    os.makedirs(SPLIT_DIR, exist_ok=True)
    with open(os.path.join(SPLIT_DIR, "train_ids.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(train_ids) + "\n")
    with open(os.path.join(SPLIT_DIR, "dev_ids.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(dev_ids) + "\n")
    with open(os.path.join(SPLIT_DIR, "test_ids.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(test_ids) + "\n")
    print(f"Đã lưu các file split IDs tại: {SPLIT_DIR}")
    
    # Lưu pool các chunks thô
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_pool_path = os.path.join(RAW_DIR, "chunks_pool.jsonl")
    with open(raw_pool_path, "w", encoding="utf-8") as f:
        for it in selected_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"Đã lưu danh sách chunks thô tại: {raw_pool_path}")

if __name__ == "__main__":
    main()
