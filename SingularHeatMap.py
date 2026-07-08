import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path("CachedData_German")
OUTPUT_DIR = Path("graphs")
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAMES = ["ChatGPT", "Gemini", "Grok", "DeepSeek"]

CRITERIA = [
    "1_1",
    "2_1", "2_2", "2_3", "2_4",
    "3_1", "3_2", "3_3", "3_4", "3_5", "3_6",
    "4_1", "4_2",
    "5_1", "5_2", "5_3",
]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def dominant_percentage(criterion_data):
    if not criterion_data:
        return None

    total = sum(criterion_data.values())
    if total == 0:
        return None

    best_grade, best_count = max(
        criterion_data.items(),
        key=lambda x: (x[1], int(x[0]))
    )
    return (best_count / total) * 100

def build_heatmap_df(subject_folder):
    rows = []
    for criterion in CRITERIA:
        row = {"Category": criterion}
        for model in MODEL_NAMES:
            json_path = BASE_DIR / subject_folder / model / "bewertung_summary.json"
            if not json_path.exists():
                row[model] = float("nan")
                continue

            data = load_json(json_path)
            criterion_data = data.get(criterion, {})
            row[model] = dominant_percentage(criterion_data)

        rows.append(row)

    return pd.DataFrame(rows)

def heat_map(df, output_path, title):
    df = df.set_index("Category")

    fig, ax = plt.subplots(figsize=(10, 10))

    sns.heatmap(
        df,
        annot=True,
        fmt=".1f",
        cmap="RdYlGn",
        vmin=50,
        vmax=100,
        cbar_kws={"label": "Percentage (%)"},
        ax=ax,
        linewidths=0.5
    )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("LLM", fontsize=12, fontweight="bold")
    ax.set_ylabel("Category", fontsize=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def main():
    for subject_dir in BASE_DIR.iterdir():
        if subject_dir.is_dir():
            df = build_heatmap_df(subject_dir.name)
            output_path = OUTPUT_DIR / f"{subject_dir.name}_heatmap.png"
            heat_map(df, output_path, f"{subject_dir.name} - LLM Performance Heatmap by Category")
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()
