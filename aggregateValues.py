import json
import os
from pathlib import Path
from collections import defaultdict


def collect_and_aggregate_by_llm():
    """
    Collect all bewertung_summary.json files grouped by LLM.
    Aggregates all contexts for each LLM into a single JSON file.
    Saves to /LLMData/{LLMName}/aggregated_data.json
    """

    # Define the context and LLM names
    """
    context_names = [
        "NoContext_ZeroShot",
        "NoContext_OneShot_Bad",
        "NoContext_OneShot_Good",
        "Sex_Male_ZeroShot",
        "Sex_Female_ZeroShot",
        "NoContext_ZeroShot_NoErrors"
    ]

    context_names = [
        "NoContext_ZeroShot_BubbleSort_NotWorking",
        "NoContext_ZeroShot_WrongImplementation",
    ]"""

    context_names = [
        "China",
        "Google"
    ]

    llm_names = [
        "Gemini",
        "ChatGPT",
        "DeepSeek"
    ]

    # Base path
    base_path = Path("CachedData_PoWi")
    output_base_path = Path("LLMData")

    # Create output directory if it doesn't exist
    output_base_path.mkdir(exist_ok=True)

    # Process each LLM
    for llm in llm_names:
        print(f"\n{'=' * 60}")
        print(f"Processing LLM: {llm}")
        print(f"{'=' * 60}")

        # Dictionary to store aggregated data for this LLM
        aggregated_data = {}
        file_count = 0

        # Iterate through all contexts for this LLM
        for context in context_names:
            file_path = base_path / context / llm / "bewertung_summary.json"

            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Store data with context as key for reference
                    aggregated_data[context] = data
                    file_count += 1
                    print(f"  ✓ Loaded: {context}")

                except json.JSONDecodeError as e:
                    print(f"  ✗ Error reading JSON from {file_path}: {e}")
                except Exception as e:
                    print(f"  ✗ Error processing {file_path}: {e}")
            else:
                print(f"  ⚠ File not found: {file_path}")

        # Save aggregated data for this LLM
        if aggregated_data:
            output_dir = output_base_path / llm
            output_dir.mkdir(exist_ok=True)

            output_file = output_dir / "aggregated_data.json"

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(aggregated_data, f, indent=2, ensure_ascii=False)

            print(f"\n  ✓ Saved aggregated data for {llm}")
            print(f"    Location: {output_file}")
            print(f"    Files processed: {file_count}")
        else:
            print(f"\n  ✗ No data collected for {llm}")

    print(f"\n{'=' * 60}")
    print("Aggregation Complete!")
    print(f"{'=' * 60}")


# Execute the function
if __name__ == "__main__":
    collect_and_aggregate_by_llm()
