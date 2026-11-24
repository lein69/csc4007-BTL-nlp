"""
Script: export_charts.py
Tự động xuất biểu đồ chỉ số thực nghiệm phong cách Weights & Biases (W&B)
thành các tệp hình ảnh PNG độ phân giải cao phục vụ chèn vào Slide thuyết trình và Báo cáo PDF.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

# Cấu hình font và style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

def export_grouped_bar_chart():
    categories = ["Precision", "Recall", "Macro-F1", "Exact Match", "Lỗi số học"]
    e0 = [69.05, 69.05, 69.05, 73.81, 16.67]
    e1 = [47.22, 60.71, 53.12, 72.62, 11.90]
    e2 = [40.76, 89.29, 55.97, 89.29, 0.00]

    x = np.arange(len(categories))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    rects1 = ax.bar(x - width, e0, width, label="E0 (Baseline Regex)", color="#4A90E2", edgecolor="white")
    rects2 = ax.bar(x, e1, width, label="E1 (LLM Zero-Shot)", color="#F5A623", edgecolor="white")
    rects3 = ax.bar(x + width, e2, width, label="E2 (Pipeline Few-Shot)", color="#2ECC71", edgecolor="white")

    ax.set_ylabel("Tỷ lệ (%)", fontsize=12, fontweight="bold")
    ax.set_title("SO SÁNH HIỆU NĂNG CÁC CẤU HÌNH THÍ NGHIỆM (E0 - E1 - E2)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor="#e0e0e0", fontsize=10)
    ax.set_ylim(0, 105)

    # Gắn nhãn số liệu lên từng cột
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f"{height:.1f}%",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.tight_layout()
    out_path = os.path.join(REPORTS_DIR, "wandb_metrics_comparison.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Đã xuất biểu đồ cột tại: {out_path}")

def export_radar_chart():
    labels = ["Precision", "Recall", "Macro-F1", "Exact Match", "Độ chuẩn xác số"]
    num_vars = len(labels)

    # Tính toán góc cho radar
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1] # Đóng vòng tròn

    e0 = [69.05, 69.05, 69.05, 73.81, 100 - 16.67]
    e1 = [47.22, 60.71, 53.12, 72.62, 100 - 11.90]
    e2 = [40.76, 89.29, 55.97, 89.29, 100 - 0.00]

    e0 += e0[:1]
    e1 += e1[:1]
    e2 += e2[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), dpi=300)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], labels, fontsize=11, fontweight="bold")
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20%", "40%", "60%", "80%", "100%"], color="#777777", size=9)
    plt.ylim(0, 105)

    # Vẽ từng mô hình
    ax.plot(angles, e0, linewidth=2, linestyle='solid', label="E0 (Baseline)", color="#4A90E2")
    ax.fill(angles, e0, color="#4A90E2", alpha=0.15)

    ax.plot(angles, e1, linewidth=2, linestyle='solid', label="E1 (Zero-Shot)", color="#F5A623")
    ax.fill(angles, e1, color="#F5A623", alpha=0.15)

    ax.plot(angles, e2, linewidth=2.5, linestyle='solid', label="E2 (Pipeline Few-Shot)", color="#2ECC71")
    ax.fill(angles, e2, color="#2ECC71", alpha=0.25)

    plt.title("BIỂU ĐỒ RADAR ĐA CHIỀU (W&B-STYLE)", size=14, fontweight="bold", y=1.08)
    plt.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True, facecolor="white", fontsize=10)

    plt.tight_layout()
    out_path = os.path.join(REPORTS_DIR, "wandb_radar_chart.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Đã xuất biểu đồ radar tại: {out_path}")

if __name__ == "__main__":
    export_grouped_bar_chart()
    export_radar_chart()
