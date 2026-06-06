import os
import pandas as pd


def load_all(input_dir="input"):
    """
    Loads all CSV files from the input directory.cd
    Returns a dictionary: { "TS001": DataFrame, "TS007": DataFrame, ... }
    """
    datasets = {}

    for filename in os.listdir(input_dir):
        if not filename.endswith(".csv"):
            print(f"[ingest] Skipping non-CSV file: {filename}")
            continue

        name = os.path.splitext(filename)[0]  # e.g. "TS001"
        filepath = os.path.join(input_dir, filename)

        try:
            df = pd.read_csv(filepath)
            datasets[name] = df
            print(f"[ingest] Loaded {name} → {df.shape[0]} rows × {df.shape[1]} columns")
        except Exception as e:
            print(f"[ingest] ERROR loading {filename}: {e}")

    return datasets


if __name__ == "__main__":
    data = load_all()
    print(f"\n[ingest] Done. {len(data)} dataset(s) loaded: {list(data.keys())}")