import sys
import os

# Add src folder to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ingest import load_all
from clean import clean_all
from transform import transform_all
from analyze import analyze_all


def main():
    print("=" * 60)
    print("  UK Census Pipeline")
    print("  MSc Computer Science - Group Project")
    print("=" * 60)

    # Stage 1 - Ingest
    print("\n[pipeline] Stage 1: Ingesting data...")
    raw = load_all()
    print(f"[pipeline] Loaded {len(raw)} dataset(s)")

    # Stage 2 - Clean
    print("\n[pipeline] Stage 2: Cleaning data...")
    cleaned = clean_all(raw)
    print(f"[pipeline] Cleaned {len(cleaned)} dataset(s)")

    # Stage 3 - Transform
    print("\n[pipeline] Stage 3: Transforming data...")
    transformed = transform_all(cleaned)
    print(f"[pipeline] Transformed {len(transformed)} dataset(s)")

    # Stage 4 - Analyze
    print("\n[pipeline] Stage 4: Analysing data...")
    results = analyze_all(transformed)
    print(f"[pipeline] Analysis complete. {len(results)} result(s) generated")

    print("\n" + "=" * 60)
    print("  Pipeline complete!")
    print("=" * 60)

    # Stage 5 - Visualise
    print("\n[pipeline] Stage 5: Generating charts...")
    from visualise import visualise_all
    visualise_all(transformed, results)


if __name__ == "__main__":
    main()