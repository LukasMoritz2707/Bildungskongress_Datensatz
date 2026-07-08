import os
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path("CachedData_PoWi")
OUTPUT_DIR = Path("graphs")
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAMES = ["ChatGPT", "Gemini", "DeepSeek"]

def compute_average_grade(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = 0
    count = 0

    for key, value in data.items():
        # Skip nested sections like "sachliche_noten"
        if not isinstance(value, dict):
            continue
        if key == "sachliche_noten":
            continue

        for grade_str, num in value.items():
            grade = int(grade_str)
            total += grade * num
            count += num

    return total / count if count > 0 else None

def collect_subject_averages(subject_folder):
    averages = {}
    for model in MODEL_NAMES:
        json_path = BASE_DIR / subject_folder / model / "bewertung_summary.json"
        if json_path.exists():
            averages[model] = compute_average_grade(json_path)
        else:
            averages[model] = None
    return averages

def plot_subject(subject_folder, averages):
    models = list(averages.keys())
    values = [averages[m] if averages[m] is not None else 0 for m in models]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(models, values, color=["#4C78A8", "#F58518", "#54A24B", "#E45756"])
    plt.ylim(0, 6)
    plt.ylabel("Durchschnittsnote")
    plt.title(f"Durchschnittsnote pro Modell - {subject_folder}")

    for bar, val in zip(bars, values):
        if val > 0:
            plt.text(bar.get_x() + bar.get_width()/2, val + 0.05, f"{val:.2f}",
                     ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    out_path = OUTPUT_DIR / f"{subject_folder}_average_grade.png"
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"Saved: {out_path}")

def main():
    for subject_dir in BASE_DIR.iterdir():
        if subject_dir.is_dir():
            averages = collect_subject_averages(subject_dir.name)
            plot_subject(subject_dir.name, averages)

if __name__ == "__main__":
    main()
