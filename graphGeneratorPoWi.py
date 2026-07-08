import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def collect_json_data(folder):
    gesamtnoten = []

    criteria_stats = defaultdict(lambda: defaultdict(int))
    note_stats = defaultdict(lambda: defaultdict(int))

    for filename in os.listdir(folder):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(folder, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Could not read {filename}: {e}")
            continue

        bewertung = data.get("bewertung", {})
        gesamtnote = bewertung.get("gesamtnote")

        if gesamtnote is not None:
            try:
                gesamtnote_int = int(gesamtnote)
                gesamtnoten.append(gesamtnote_int)
                note_stats["gesamtnote"][gesamtnote_int] += 1
            except ValueError:
                print(f"Invalid gesamtnote in {filename}: {gesamtnote}")

        abschnitte = bewertung.get("abschnitte", {})
        for section in abschnitte.values():
            kriterien = section.get("kriterien", [])
            for kriterium in kriterien:
                kriterium_id = kriterium.get("id")
                status = kriterium.get("status")

                if kriterium_id is not None and status is not None:
                    try:
                        status_int = int(status)
                        criteria_stats[kriterium_id][status_int] += 1
                    except (ValueError, TypeError):
                        print(f"Invalid status in {filename}: {status}")

    return gesamtnoten, criteria_stats, note_stats


def create_bar_chart(grades, output_file, LLM):
    if not grades:
        print("No grades found.")
        return

    min_grade = min(grades)
    max_grade = max(grades)

    distribution = {g: grades.count(g) for g in range(1,7)}

    plt.figure(figsize=(8, 5))
    plt.bar(distribution.keys(), distribution.values())
    plt.xlabel("Gesamtnote")
    plt.ylabel("Anzahl")
    plt.title(f"Verteilung der Gesamtnoten ({LLM})")
    plt.xticks(list(distribution.keys()))
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()


def save_summary(criteria_stats, note_stats, output_file):
    result = {}

    for key, value in criteria_stats.items():
        result[key] = {str(status): count for status, count in value.items()}

    result["gesamtnote"] = {}
    for key, value in note_stats.items():
        result["gesamtnote"][key] = {str(status): count for status, count in value.items()}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    GENERAL_FOLDER = "CachedData_PoWi/Google"
    LLM = "DeepSeek"
    JSON_FOLDER = f"{GENERAL_FOLDER}/{LLM}"

    OUTPUT_SUMMARY = f"{JSON_FOLDER}/bewertung_summary.json"
    OUTPUT_GRAPH = f"{JSON_FOLDER}/gesamtnoten_verteilung.png"

    grades, criteria, notes = collect_json_data(JSON_FOLDER)
    print(f"{len(grades)} JSON files analyzed.")
    create_bar_chart(grades, OUTPUT_GRAPH, LLM=LLM)
    save_summary(criteria, notes, OUTPUT_SUMMARY)
    print(f"Graph saved as: {OUTPUT_GRAPH}")
    print(f"Statistics saved as: {OUTPUT_SUMMARY}")
