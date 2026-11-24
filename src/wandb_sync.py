"""
Script đồng bộ kết quả thực nghiệm (E0, E1, E2) lên Weights & Biases (W&B)
Nhóm/Team: lein69 | User: andangvn69
Project: csc4007-btl-dt02 (Đề tài 2: Trích xuất thực thể và dữ kiện kinh tế)
"""

import os
import json
import pandas as pd
import wandb

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

WANDB_ENTITY = "lein69"
WANDB_PROJECT = "csc4007-btl-dt02"

EXPERIMENT_MAP = {
    "E0": {
        "name": "E0-Baseline-Regex-Nearest",
        "config_file": "config_E0.json",
        "pred_file": "test_predictions_E0.csv",
        "notes": "Mô hình cơ sở kết hợp Regex trích xuất số liệu + heuristic gán thực thể gần nhất."
    },
    "E1": {
        "name": "E1-LLM-ZeroShot-GeminiFlash",
        "config_file": "config_E1.json",
        "pred_file": "test_predictions_E1.csv",
        "notes": "Mô hình LLM Zero-shot sử dụng gemini-3-flash-preview trả về cấu trúc JSON tự nhiên."
    },
    "E2": {
        "name": "E2-TwoStage-Pipeline-FewShot",
        "config_file": "config_E2.json",
        "pred_file": "test_predictions_E2.csv",
        "notes": "Pipeline hai giai đoạn kết hợp Few-Shot hướng dẫn ca biên giới và tầng lọc Schema Validation."
    }
}

def sync_all_experiments():
    metrics_path = os.path.join(EVAL_DIR, "metrics_summary.csv")
    if not os.path.exists(metrics_path):
        print(f"[ERROR] Không tìm thấy file {metrics_path}. Hãy chạy evaluate.py trước.")
        return

    df_metrics = pd.read_csv(metrics_path)
    print(f"Đã nạp {len(df_metrics)} cấu hình từ metrics_summary.csv")

    for _, row in df_metrics.iterrows():
        run_id = row["run_id"]
        info = EXPERIMENT_MAP.get(run_id)
        if not info:
            continue

        print(f"\n==========================================")
        print(f"🚀 Bắt đầu log {run_id} ({info['name']}) lên W&B...")
        print(f"   Team/Entity: {WANDB_ENTITY} | Project: {WANDB_PROJECT}")
        print(f"==========================================")

        # 1. Đọc file config
        cfg_path = os.path.join(CONFIG_DIR, info["config_file"])
        config_data = {}
        if os.path.exists(cfg_path):
            with open(cfg_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

        config_data.update({
            "run_id": run_id,
            "project_topic": "DT02 - Fact Tuple Extraction",
            "course": "CSC4007 - Xử lý ngôn ngữ tự nhiên",
            "institution": "Trường Đại học Đại Nam",
            "test_samples_count": 50
        })

        # 2. Khởi tạo WandB Run
        run = wandb.init(
            entity=WANDB_ENTITY,
            project=WANDB_PROJECT,
            name=info["name"],
            group="BTL-Evaluation-50-Test",
            notes=info["notes"],
            config=config_data,
            reinit=True
        )

        # 3. Log metrics summary
        metrics_dict = {
            "eval/precision": float(row["precision"]),
            "eval/recall": float(row["recall"]),
            "eval/f1_score": float(row["f1_score"]),
            "eval/exact_match_rate": float(row["exact_match_rate"]),
            "eval/numeric_error_rate": float(row["numeric_error_rate"]),
            "eval/period_mismatch_rate": float(row["period_mismatch_rate"]),
        }
        wandb.log(metrics_dict)
        wandb.summary.update(metrics_dict)

        # 4. Log Predictions Table (50 test samples)
        pred_path = os.path.join(EVAL_DIR, info["pred_file"])
        if os.path.exists(pred_path):
            df_pred = pd.read_csv(pred_path)
            # Giới hạn số cột hiển thị cho gọn
            cols = [c for c in ["sample_id", "text", "indicator", "value", "unit", "period", "evidence"] if c in df_pred.columns]
            table = wandb.Table(dataframe=df_pred[cols].head(100))
            wandb.log({"eval/test_predictions": table})
            print(f"   + Đã log W&B Table cho {len(df_pred)} dự đoán")

        # 5. Log Biểu đồ hình ảnh W&B
        img_bar = os.path.join(REPORTS_DIR, "wandb_metrics_comparison.png")
        img_radar = os.path.join(REPORTS_DIR, "wandb_radar_chart.png")
        
        images_to_log = {}
        if os.path.exists(img_bar):
            images_to_log["charts/metrics_comparison"] = wandb.Image(img_bar, caption="Grouped Bar Chart - So sánh E0, E1, E2")
        if os.path.exists(img_radar):
            images_to_log["charts/radar_chart"] = wandb.Image(img_radar, caption="Radar Chart - Độ bao phủ năng lực")
        
        if images_to_log:
            wandb.log(images_to_log)
            print(f"   + Đã log {len(images_to_log)} biểu đồ hình ảnh lên W&B")

        run.finish()
        print(f"✅ Hoàn tất đồng bộ {run_id} lên W&B!")

    print("\n🎉 Tất cả 3 thực nghiệm E0, E1, E2 đã được đẩy lên W&B thành công!")
    print(f"👉 Xem bảng điều khiển tại: https://wandb.ai/{WANDB_ENTITY}/{WANDB_PROJECT}")

if __name__ == "__main__":
    sync_all_experiments()
