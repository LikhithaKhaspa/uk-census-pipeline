import pandas as pd
import re


def _standardise_column_name(name):
    """
    Converts a column name to lowercase with underscores.
    e.g. 'Geography Code' -> 'geography_code'
         'Area Name (EW) (2021)' -> 'area_name_ew_2021'
    """
    # Known special mappings for ONS area code column variations
    known = {
        r"geography\s*code|mnemonic|area\s*code": "area_code",
        r"geography\s*name|area\s*name.*":        "area_name",
    }
    lower = name.strip().lower()
    for pattern, replacement in known.items():
        if re.search(pattern, lower):
            return replacement

    # General: remove special chars, replace spaces with underscores
    clean = re.sub(r"[^a-z0-9]+", "_", lower)
    clean = clean.strip("_")
    return clean


def clean_dataset(name, df):
    """
    Cleans a single DataFrame.
    Returns the cleaned DataFrame.
    """
    print(f"\n[clean] Processing {name}...")
    original_shape = df.shape

    # 1. Standardise column names
    original_cols = df.columns.tolist()
    df.columns = [_standardise_column_name(c) for c in df.columns]
    renamed = {o: n for o, n in zip(original_cols, df.columns) if o != n}
    if renamed:
        print(f"[clean] Renamed {len(renamed)} columns")

    # 2. Strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    # 3. Convert numeric-looking columns to float
    converted = 0
    for col in df.columns:
        if df[col].dtype == object:
            coerced = pd.to_numeric(df[col].replace({'\\.\\.': None, 'x': None}, regex=True), errors='coerce')
            if coerced.notna().sum() > len(df) * 0.5:
                df[col] = coerced
                converted += 1
    if converted:
        print(f"[clean] Converted {converted} columns to numeric")

    # 4. Fill missing values
    missing_before = df.isna().sum().sum()
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].fillna("unknown")
    missing_after = df.isna().sum().sum()
    if missing_before > 0:
        print(f"[clean] Filled {missing_before - missing_after} missing values")

    # 5. Remove duplicates
    dupes = df.duplicated().sum()
    if dupes > 0:
        df = df.drop_duplicates()
        print(f"[clean] Removed {dupes} duplicate rows")

    print(f"[clean] {name} done: {original_shape} → {df.shape}")
    return df


def clean_all(datasets):
    """
    Cleans all datasets.
    Returns a dictionary of cleaned DataFrames.
    """
    return {name: clean_dataset(name, df.copy()) for name, df in datasets.items()}


if __name__ == "__main__":
    from ingest import load_all
    raw = load_all()
    cleaned = clean_all(raw)
    print(f"\n[clean] Done. {len(cleaned)} dataset(s) cleaned.")