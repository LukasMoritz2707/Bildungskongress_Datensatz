import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def collect_json_data(folder):
    gesamtnoten = []
    criteria_stats = defaultdict(lambda: defaultdict(int))
    gesamtnote_stats = defaultdict(int)

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
            gesamtnoten.append(gesamtnote)
            gesamtnote_stats[gesamtnote] += 1

        abschnitte = bewertung.get("abschnitte", {})
        for section in abschnitte.values():
            kriterien = section.get("kriterien", [])
            for kriterium in kriterien:
                kriterium_id = kriterium.get("id")
                status = kriterium.get("status")

                if kriterium_id is not None and status is not None:
                    criteria_stats[kriterium_id][status] += 1

    return gesamtnoten, criteria_stats, gesamtnote_stats

def create_bar_chart(grades, output_file, llm):
    distribution = {i: grades.count(i) for i in range(1, 7)}

    plt.figure(figsize=(8, 5))
    plt.bar(distribution.keys(), distribution.values())
    plt.xlabel("Gesamtnote")
    plt.ylabel("Anzahl")
    plt.title(f"Verteilung der Gesamtnoten ({llm})")
    plt.xticks(range(1, 7))
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

def save_summary(criteria_stats, gesamtnote_stats, output_file):
    result = {}

    for key, value in criteria_stats.items():
        result[key] = {str(status): count for status, count in value.items()}

    result["gesamtnote"] = {str(note): count for note, count in gesamtnote_stats.items()}

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    GENERAL_FOLDER = "CachedData_Info/NoContext_ZeroShot_WrongImplementation"
    LLM = "ChatGPT"
    JSON_FOLDER = f"{GENERAL_FOLDER}/{LLM}"

    OUTPUT_SUMMARY = f"{JSON_FOLDER}/bewertung_summary.json"
    OUTPUT_GRAPH = f"{JSON_FOLDER}/gesamtnoten_verteilung.png"

    grades, criteria, gesamtnote_stats = collect_json_data(JSON_FOLDER)
    print(f"{len(grades)} JSON files analyzed.")
    create_bar_chart(grades, OUTPUT_GRAPH, llm=LLM)
    save_summary(criteria, gesamtnote_stats, OUTPUT_SUMMARY)
    print(f"Graph saved as: {OUTPUT_GRAPH}")
    print(f"Statistics saved as: {OUTPUT_SUMMARY}")
