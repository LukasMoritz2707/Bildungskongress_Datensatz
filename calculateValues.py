import json
from pathlib import Path
import pandas as pd


def calculate_highest_value_percentages():
    """
    Read aggregated LLM data and calculate percentages based on highest values.
    For each category, finds the maximum value and calculates what percentage
    of total attempts (20) that represents.
    Returns a table with categories as rows and LLMs as columns.
    """

    llm_names = [
        "Gemini",
        "ChatGPT",
        "DeepSeek"
    ]

    base_path = Path("LLMData_Info")
    llm_results = {}
    all_categories = set()

    print(f"\n{'=' * 80}")
    print("CALCULATING HIGHEST VALUE PERCENTAGES")
    print(f"{'=' * 80}\n")

    # First pass: collect all data and categories
    for llm in llm_names:
        input_file = base_path / llm / "aggregated_data.json"

        if not input_file.exists():
            print(f"✗ File not found: {input_file}")
            continue

        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                llm_data = json.load(f)

            print(f"Processing {llm}...")

            # Dictionary to store results for this LLM
            llm_results[llm] = {}

            # Process all contexts and categories
            for context, context_data in llm_data.items():
                print(f"  Context: {context}")

                for category, values in context_data.items():
                    # Skip non-numeric category entries (like sachliche_noten which is a dict of dicts)
                    if not isinstance(values, dict):
                        continue

                    # Check if values are numeric
                    try:
                        numeric_values = {k: int(v) for k, v in values.items()}
                    except (ValueError, TypeError):
                        continue

                    # Find the maximum value
                    max_value = max(numeric_values.values())
                    total = sum(numeric_values.values())

                    # Calculate percentage
                    percentage = (max_value / total * 100) if total > 0 else 0

                    # Track all categories
                    all_categories.add(category)

                    # Store results
                    if category not in llm_results[llm]:
                        llm_results[llm][category] = {
                            "max_values": [],
                            "totals": [],
                            "percentages": []
                        }

                    llm_results[llm][category]["max_values"].append(max_value)
                    llm_results[llm][category]["totals"].append(total)
                    llm_results[llm][category]["percentages"].append(percentage)

            print(f"  ✓ Completed {llm}\n")

        except json.JSONDecodeError as e:
            print(f"✗ Error reading JSON from {input_file}: {e}")
        except Exception as e:
            print(f"✗ Error processing {input_file}: {e}")

    # Second pass: create table with categories as rows and LLMs as columns
    if llm_results:
        table_data = []

        for category in sorted(all_categories):
            row = {"Category": category}

            for llm in llm_names:
                if llm in llm_results and category in llm_results[llm]:
                    data = llm_results[llm][category]
                    avg_percentage = sum(data["percentages"]) / len(data["percentages"]) if data["percentages"] else 0
                    row[llm] = round(avg_percentage, 2)
                else:
                    row[llm] = None

            table_data.append(row)

        # Create DataFrame with Category as first column
        df = pd.DataFrame(table_data)
        df = df.set_index("Category")

        print(f"{'=' * 80}")
        print("SUMMARY TABLE - CATEGORIES vs LLMs (Average Percentages)")
        print(f"{'=' * 80}\n")
        print(df.to_string())

        # Save summary to CSV
        csv_file = base_path / "summary_percentages.csv"
        df.to_csv(csv_file)
        print(f"\n✓ Summary saved to: {csv_file}")

        # Also save detailed analysis for each LLM
        for llm in llm_names:
            if llm in llm_results:
                output_file = base_path / llm / "highest_value_analysis.json"

                # Create summary for detailed analysis
                llm_summary = {}
                for category, data in llm_results[llm].items():
                    avg_percentage = sum(data["percentages"]) / len(data["percentages"]) if data["percentages"] else 0
                    llm_summary[category] = {
                        "avg_percentage": round(avg_percentage, 2),
                        "count": len(data["percentages"])
                    }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(llm_summary, f, indent=2, ensure_ascii=False)

                print(f"✓ Detailed analysis saved: {output_file}")

        return df
    else:
        print("No data could be processed.")
        return None


# Execute the function
if __name__ == "__main__":
    calculate_highest_value_percentages()
