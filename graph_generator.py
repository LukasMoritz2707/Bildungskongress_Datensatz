import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt


# =========================
# Configuration
# =========================

JSON_FOLDER = "CachedData/NoContext_ZeroShot"
OUTPUT_SUMMARY = "bewertung_summary.json"
OUTPUT_GRAPH = "gesamtnoten_verteilung.png"


# =========================
# Data collection
# =========================

def collect_json_data(folder):

    gesamtnoten = []

    criteria_stats = defaultdict(lambda: {
        1: 0,
        2: 0,
        3: 0
    })

    note_stats = defaultdict(lambda: {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    })


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


        # -------------------------
        # Gesamt Note
        # -------------------------

        gesamtnote = bewertung.get("gesamtnote")

        if gesamtnote:
            gesamtnoten.append(gesamtnote)
            note_stats["gesamtnote"][gesamtnote] += 1


        # -------------------------
        # Kriterien
        # -------------------------

        abschnitte = bewertung.get("abschnitte", {})

        for section in abschnitte.values():

            kriterien = section.get("kriterien", [])

            for kriterium in kriterien:

                kriterium_id = kriterium.get("id")
                status = kriterium.get("status")


                if kriterium_id and status:

                    criteria_stats[kriterium_id][status] += 1


        # -------------------------
        # Sachliche Bewertung
        # -------------------------

        sachliches = bewertung.get("6_sachliches", {})

        for name, value in sachliches.items():

            if isinstance(value, dict):

                note = value.get("note")

                if note:
                    note_stats[name][note] += 1


    return gesamtnoten, criteria_stats, note_stats



# =========================
# Plotting
# =========================

def create_bar_chart(grades, output_file):

    distribution = {
        1: grades.count(1),
        2: grades.count(2),
        3: grades.count(3),
        4: grades.count(4),
        5: grades.count(5),
        6: grades.count(6)
    }


    plt.figure(figsize=(8, 5))

    plt.bar(
        distribution.keys(),
        distribution.values()
    )

    plt.xlabel("Gesamtnote")
    plt.ylabel("Anzahl")
    plt.title("Verteilung der Gesamtnoten")

    plt.xticks(range(1, 7))

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()



# =========================
# Save statistics
# =========================

def save_summary(criteria_stats, note_stats, output_file):

    result = {}

    # Convert defaultdicts to normal dictionaries

    for key, value in criteria_stats.items():

        result[key] = {
            str(status): count
            for status, count in value.items()
        }


    result["sachliche_noten"] = {}

    for key, value in note_stats.items():

        result["sachliche_noten"][key] = {
            str(status): count
            for status, count in value.items()
        }


    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )



# =========================
# Main
# =========================

if __name__ == "__main__":

    grades, criteria, notes = collect_json_data(
        JSON_FOLDER
    )


    print(
        f"{len(grades)} JSON files analyzed."
    )


    create_bar_chart(
        grades,
        OUTPUT_GRAPH
    )


    save_summary(
        criteria,
        notes,
        OUTPUT_SUMMARY
    )


    print(
        f"Graph saved as: {OUTPUT_GRAPH}"
    )

    print(
        f"Statistics saved as: {OUTPUT_SUMMARY}"
    )