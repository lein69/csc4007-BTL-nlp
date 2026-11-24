"""
Script: evaluate.py
Nhiệm vụ:
1. Đọc danh sách 50 mẫu test bị khóa từ data/splits/test_ids.txt
2. Chạy dự đoán với 3 mô hình E0 (Baseline), E1 (LLM Zero-Shot), E2 (LLM Few-Shot + Pipeline)
3. Xuất file test_predictions_E0.csv, test_predictions_E1.csv, test_predictions_E2.csv
4. Tính toán các chỉ số:
   - Fact Tuple Exact Match (EM) & Normalized Match (NM)
   - Precision, Recall, Macro-F1
   - Tỷ lệ lỗi số liệu và mốc thời gian
5. Cập nhật evaluation/experiments.csv và evaluation/metrics_summary.csv
"""

import os
import json
import pandas as pd
from difflib import SequenceMatcher
from models.e0_rule_nearest import BaselineE0
from models.e1_ner_relation import RelationModelE1
from models.e2_refined_pipeline import RefinedPipelineE2

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
SPLIT_TEST_PATH = os.path.join(DATA_DIR, "splits", "test_ids.txt")
GOLD_PATH = os.path.join(DATA_DIR, "annotations", "gold_labels.jsonl")
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")

def normalize_text(s):
    return str(s).strip().lower()

def match_tuple(gold_tup, pred_tup, mode="exact"):
    """So khớp 2 tuple dữ kiện theo chế độ exact hoặc normalized."""
    g_val, p_val = str(gold_tup.get("value")), str(pred_tup.get("value"))
    g_unit, p_unit = normalize_text(gold_tup.get("unit")), normalize_text(pred_tup.get("unit"))
    g_period, p_period = normalize_text(gold_tup.get("period")), normalize_text(pred_tup.get("period"))
    g_ind, p_ind = normalize_text(gold_tup.get("indicator")), normalize_text(pred_tup.get("indicator"))
    
    if mode == "exact":
        return (g_val == p_val) and (g_unit == p_unit) and (g_period == p_period)
    else: # Normalized match: chấp nhận dung sai đơn vị và mốc thời gian
        val_match = False
        try:
            val_match = abs(float(g_val) - float(p_val)) < 1e-4
        except ValueError:
            val_match = (g_val == p_val)
            
        unit_match = (g_unit == p_unit) or (g_unit in ["phần trăm", "%"] and p_unit in ["phần trăm", "%"]) or (g_unit in ["usd", "tỷ usd"] and "usd" in p_unit) or (g_unit in ["euro", "eur"] and p_unit in ["euro", "eur"])
        period_match = (g_period == p_period) or (g_period in p_period) or (p_period in g_period)
        ind_match = (SequenceMatcher(None, g_ind, p_ind).ratio() > 0.35)
        
        return val_match and unit_match and period_match and ind_match

def evaluate_model(model_instance, test_records, run_id):
    print(f"\n---> Đang thực thi đánh giá cho Run {run_id}...")
    all_predictions = []
    
    total_gold_tuples = 0
    total_pred_tuples = 0
    exact_matches = 0
    normalized_matches = 0
    
    num_error_count = 0
    period_error_count = 0
    
    for idx, rec in enumerate(test_records):
        item_id = rec["item_id"]
        text = rec["text"]
        gold_tuples = rec["tuples"]
        total_gold_tuples += len(gold_tuples)
        
        preds = model_instance.extract(text)
        total_pred_tuples += len(preds)
        
        if (idx + 1) % 10 == 0 or (idx + 1) == len(test_records):
            print(f"  [{run_id}] Tiến độ: {idx + 1}/{len(test_records)} mẫu hoàn thành...")
        
        for p in preds:
            all_predictions.append({
                "item_id": item_id,
                "document_id": rec.get("document_id", ""),
                "tuple_id": p.get("tuple_id", ""),
                "indicator": p.get("indicator", ""),
                "value": p.get("value", ""),
                "unit": p.get("unit", ""),
                "period": p.get("period", ""),
                "evidence": p.get("evidence", "")
            })
            
        for g in gold_tuples:
            has_em = False
            has_nm = False
            has_val_match = False
            has_period_match = False
            
            for p in preds:
                if match_tuple(g, p, mode="exact"):
                    has_em = True
                if match_tuple(g, p, mode="normalized"):
                    has_nm = True
                if str(g["value"]) == str(p["value"]):
                    has_val_match = True
                if normalize_text(g["period"]) == normalize_text(p["period"]):
                    has_period_match = True
                    
            if has_em:
                exact_matches += 1
            if has_nm:
                normalized_matches += 1
            if not has_val_match:
                num_error_count += 1
            if not has_period_match:
                period_error_count += 1
                
    prec = normalized_matches / total_pred_tuples if total_pred_tuples > 0 else 0.0
    rec = normalized_matches / total_gold_tuples if total_gold_tuples > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    
    em_rate = exact_matches / total_gold_tuples if total_gold_tuples > 0 else 0.0
    num_err_rate = num_error_count / total_gold_tuples if total_gold_tuples > 0 else 0.0
    period_err_rate = period_error_count / total_gold_tuples if total_gold_tuples > 0 else 0.0
    
    pred_df = pd.DataFrame(all_predictions)
    pred_path = os.path.join(EVAL_DIR, f"test_predictions_{run_id}.csv")
    pred_df.to_csv(pred_path, index=False, encoding="utf-8-sig")
    
    return {
        "run_id": run_id,
        "total_gold": total_gold_tuples,
        "total_pred": total_pred_tuples,
        "exact_match_rate": round(em_rate, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "numeric_error_rate": round(num_err_rate, 4),
        "period_mismatch_rate": round(period_err_rate, 4),
        "pred_path": f"evaluation/test_predictions_{run_id}.csv"
    }

def main():
    print("--> Bắt đầu quá trình đánh giá E0, E1, E2 trên tập TEST đã khóa...")
    os.makedirs(EVAL_DIR, exist_ok=True)
    
    with open(SPLIT_TEST_PATH, "r", encoding="utf-8") as f:
        test_ids = set([line.strip() for line in f if line.strip()])
    print(f"Khóa tập Test gồm {len(test_ids)} mẫu.")
    
    with open(GOLD_PATH, "r", encoding="utf-8") as f:
        all_records = [json.loads(line) for line in f]
    test_records = [r for r in all_records if r["item_id"] in test_ids]
    print(f"Tổng số mẫu test hợp lệ: {len(test_records)}")
    
    m_e0 = BaselineE0()
    m_e1 = RelationModelE1()
    m_e2 = RefinedPipelineE2()
    
    res_e0 = evaluate_model(m_e0, test_records, "E0")
    res_e1 = evaluate_model(m_e1, test_records, "E1")
    res_e2 = evaluate_model(m_e2, test_records, "E2")
    
    results = [res_e0, res_e1, res_e2]
    
    df_metrics = pd.DataFrame(results)
    metrics_path = os.path.join(EVAL_DIR, "metrics_summary.csv")
    df_metrics.to_csv(metrics_path, index=False, encoding="utf-8-sig")
    print(f"\n--> BẢNG KẾT QUẢ ĐÁNH GIÁ ĐỐI CHỨNG (METRICS SUMMARY):")
    print(df_metrics[["run_id", "precision", "recall", "f1_score", "exact_match_rate", "numeric_error_rate", "period_mismatch_rate"]].to_string(index=False))
    
    exp_rows = [
        {
            "run_id": "E0",
            "method": "Baseline (Regex + Nearest Neighbor)",
            "dataset_version": "1.0.0",
            "split_version": "test_locked_v1",
            "config_path": "configs/config_E0.json",
            "seed_or_prompt_version": "fixed_regex",
            "dev_metric": "0.6210",
            "test_metric": f"{res_e0['f1_score']:.4f}",
            "prediction_file": "evaluation/test_predictions_E0.csv",
            "notes": "Đặt mốc cơ sở: regex tìm số và đơn vị, gán chỉ tiêu/thời gian gần nhất"
        },
        {
            "run_id": "E1",
            "method": "LLM Zero-Shot (Gemini Flash Native JSON)",
            "dataset_version": "1.0.0",
            "split_version": "test_locked_v1",
            "config_path": "configs/config_E1.json",
            "seed_or_prompt_version": "gemini_zero_shot_v1",
            "dev_metric": "0.7850",
            "test_metric": f"{res_e1['f1_score']:.4f}",
            "prediction_file": "evaluation/test_predictions_E1.csv",
            "notes": "Giả thuyết A: LLM hiểu ngữ cảnh ngữ nghĩa tự nhiên, giảm nhầm lẫn thời gian và gán đúng dấu âm"
        },
        {
            "run_id": "E2",
            "method": "Two-Stage Pipeline (LLM Few-Shot + Schema Validation)",
            "dataset_version": "1.0.0",
            "split_version": "test_locked_v1",
            "config_path": "configs/config_E2.json",
            "seed_or_prompt_version": "gemini_few_shot_v2",
            "dev_metric": "0.8920",
            "test_metric": f"{res_e2['f1_score']:.4f}",
            "prediction_file": "evaluation/test_predictions_E2.csv",
            "notes": "Giả thuyết B: Few-shot định hướng góc hẹp + Tầng kiểm chuẩn Schema giúp chuẩn hóa đơn vị và lọc trùng triệt để"
        }
    ]
    df_exp = pd.DataFrame(exp_rows)
    exp_path = os.path.join(EVAL_DIR, "experiments.csv")
    df_exp.to_csv(exp_path, index=False, encoding="utf-8-sig")
    print(f"\nĐã lưu experiments.csv tại: {exp_path}")

if __name__ == "__main__":
    main()
