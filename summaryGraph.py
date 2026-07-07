import os
import json
from pathlib import Path
import matplotlib.pyplot as plt


def calculate_average_grade(gesamtnote_data):
    """
    Calculate average grade from gesamtnote distribution.
    gesamtnote_data: dict like {"1": 5, "2": 13, "3": 0, ...}
    """
    total = 0
    count = 0
    for grade, frequency in gesamtnote_data.items():
        total += int(grade) * frequency
        count += frequency

    return total / count if count > 0 else 0


def collect_llm_averages(root_folder):
    """
    Collect average grades for all LLMs across all folders.
    Returns: dict with structure {folder_name: {llm_name: average_grade}}
    """
    additional_folders = [
    #    "NoContext_ZeroShot",
    #    "NoContext_OneShot_Good",
    #    "NoContext_OneShot_Bad",
    #    "Sex_Male_ZeroShot",
    #    "Sex_Female_ZeroShot",
    #    "Migration_Context_ZeroShot",
    #    "NoContext_ZeroShot_NoErrors"
        "NoContext_ZeroShot_BubbleSort_NotWorking"
    ]

    llms = ["DeepSeek", "ChatGPT", "Gemini", "Grok"]

    results = {folder: {} for folder in additional_folders}

    for folder in additional_folders:
        folder_path = os.path.join(root_folder, folder)

        if not os.path.exists(folder_path):
            print(f"Warning: Folder {folder_path} does not exist")
            continue

        for llm in llms:
            llm_path = os.path.join(folder_path, llm)
            summary_file = os.path.join(llm_path, "bewertung_summary.json")

            if not os.path.exists(summary_file):
                print(f"Warning: {summary_file} not found")
                continue

            try:
                with open(summary_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                #gesamtnote_data = data.get("sachliche_noten", {}).get("gesamtnote", {})
                gesamtnote_data = data.get("gesamtnote", {})

                if gesamtnote_data:
                    average = calculate_average_grade(gesamtnote_data)
                    results[folder][llm] = average
                    print(f"✓ {folder}/{llm}: {average:.2f}")
                else:
                    print(f"✗ {folder}/{llm}: No gesamtnote data found")

            except Exception as e:
                print(f"✗ {folder}/{llm}: Error reading file - {e}")

    return results


def save_results_to_json(results, output_file):
    """
    Export calculated averages to a JSON file.
    """
    # Convert results to ensure all values are rounded to 2 decimal places
    export_data = {}

    for folder, llm_data in results.items():
        export_data[folder] = {}
        for llm, average in llm_data.items():
            export_data[folder][llm] = round(average, 2)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=4, ensure_ascii=False)

        print(f"✓ Results saved to: {output_file}")

    except Exception as e:
        print(f"✗ Error saving JSON: {e}")


def create_comparison_graph(results, output_file):
    """
    Create a grouped bar chart comparing LLMs across folders.
    """
    llms = ["DeepSeek", "ChatGPT", "Gemini", "Grok"]
    folders = list(results.keys())

    # Prepare data for plotting
    x_positions = {}
    bar_data = {llm: [] for llm in llms}

    for folder in folders:
        for llm in llms:
            bar_data[llm].append(results[folder].get(llm, 0))

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set up bar positions
    import numpy as np
    x = np.arange(len(folders))
    width = 0.2

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

    # Plot bars for each LLM
    for i, llm in enumerate(llms):
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, bar_data[llm], width, label=llm, color=colors[i])

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom', fontsize=9)

    # Customize chart
    ax.set_xlabel('Folder', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Gesamtnote', fontsize=12, fontweight='bold')
    ax.set_title('LLM Performance Comparison Across Evaluation Contexts', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(folders, rotation=15, ha='right')
    ax.legend(title='LLM', loc='upper left')
    ax.set_ylim(0, 6)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Graph saved as: {output_file}")


if __name__ == "__main__":
    ROOT_FOLDER = "CachedData_Info"
    OUTPUT_GRAPH = os.path.join(ROOT_FOLDER, "llm_comparison.png")
    OUTPUT_JSON = os.path.join(ROOT_FOLDER, "llm_averages.json")

    print("Collecting LLM averages...\n")
    results = collect_llm_averages(ROOT_FOLDER)

    print("\n" + "=" * 50)
    print("Summary of Average Grades:")
    print("=" * 50)
    for folder in results:
        print(f"\n{folder}:")
        for llm, avg in results[folder].items():
            print(f"  {llm}: {avg:.2f}")

    print("\n" + "=" * 50)
    save_results_to_json(results, OUTPUT_JSON)
    create_comparison_graph(results, OUTPUT_GRAPH)
