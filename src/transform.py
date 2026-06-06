import pandas as pd
import re


# ── helpers ──────────────────────────────────────────────────────────────────

def _to_float(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def _sum_age_cols(df, age_from, age_to):
    """
    Dynamically finds and sums age columns between age_from and age_to.
    Works by scanning column names for age numbers using regex.
    """
    total = pd.Series(0.0, index=df.index)
    for col in df.columns:
        lc = col.lower()
        if re.search(r"aged_under_1_year", lc):
            yr = 0
        else:
            m = re.search(r"aged_(\d+)_years?(?:_\$)?", lc)
            if not m:
                continue
            yr = int(m.group(1))
        if age_from <= yr <= age_to:
            total += _to_float(df[col])
    return total.astype(int)


# ── dataset-specific transformations ─────────────────────────────────────────

def _transform_ts007(df):
    """TS007 - Age by single year → derive age group features."""
    print("[transform] Engineering age features for TS007...")

    df["pop_0_17"]  = _sum_age_cols(df, 0, 17)
    df["pop_18_64"] = _sum_age_cols(df, 18, 64)
    df["pop_65_plus"] = _sum_age_cols(df, 65, 120)
    df["total_population"] = df["pop_0_17"] + df["pop_18_64"] + df["pop_65_plus"]

    df["pct_working_age"] = (df["pop_18_64"] / df["total_population"] * 100).round(2)
    df["pct_elderly"]     = (df["pop_65_plus"] / df["total_population"] * 100).round(2)
    df["dependency_ratio"] = (
        (df["pop_0_17"] + df["pop_65_plus"]) / df["pop_18_64"].replace(0, 1)
    ).round(3)

    print(f"[transform] TS007: added pct_working_age, pct_elderly, dependency_ratio")
    return df


def _transform_ts066(df):
    """TS066 - Labour market → derive employment features."""
    print("[transform] Engineering labour features for TS066...")

    total_col = "economic_activity_status_total_all_usual_residents_aged_16_years_and_over"
    employed_col = "economic_activity_status_economically_active_excluding_full_time_students_in_employment"
    unemployed_col = "economic_activity_status_economically_active_excluding_full_time_students_unemployed"

    total = _to_float(df[total_col])
    employed = _to_float(df[employed_col])
    unemployed = _to_float(df[unemployed_col])

    df["employment_rate"] = (employed / total.replace(0, 1) * 100).round(2)
    df["unemployment_rate"] = (unemployed / total.replace(0, 1) * 100).round(2)

    print(f"[transform] TS066: added employment_rate, unemployment_rate")
    return df

def _transform_ts067(df):
    """TS067 - Qualifications → derive education features."""
    print("[transform] Engineering education features for TS067...")

    cols = df.columns.tolist()

    level4_col = [c for c in cols if "level_4" in c or "level4" in c]
    no_qual_col = [c for c in cols if "no_qual" in c or "no qual" in c]
    total_col = [c for c in cols if "total" in c or "all_usual" in c]

    if level4_col and total_col:
        level4 = _to_float(df[level4_col[0]])
        total = _to_float(df[total_col[0]])
        df["qualification_rate"] = (level4 / total.replace(0, 1) * 100).round(2)

    if no_qual_col and total_col:
        no_qual = _to_float(df[no_qual_col[0]])
        total = _to_float(df[total_col[0]])
        df["no_qual_rate"] = (no_qual / total.replace(0, 1) * 100).round(2)

    print(f"[transform] TS067: added qualification_rate, no_qual_rate")
    return df


def _transform_ts001(df):
    """TS001 - Demography → no new features needed, pass through."""
    print("[transform] TS001 passed through (no new features needed)")
    return df


# ── routing table ─────────────────────────────────────────────────────────────

ROUTES = {
    "TS001": _transform_ts001,
    "TS007": _transform_ts007,
    "TS066": _transform_ts066,
    "TS067": _transform_ts067,
}


def transform_all(cleaned_datasets):
    """
    Applies the correct transformation to each dataset.
    Returns a dictionary of transformed DataFrames.
    """
    transformed = {}
    for name, df in cleaned_datasets.items():
        # match by prefix e.g. "TS001 . csv" → "TS001"
        key = next((k for k in ROUTES if name.upper().startswith(k)), None)
        if key:
            transformed[name] = ROUTES[key](df.copy())
        else:
            print(f"[transform] No route for {name}, passing through")
            transformed[name] = df.copy()
    return transformed


if __name__ == "__main__":
    from ingest import load_all
    from clean import clean_all
    raw = load_all()
    cleaned = clean_all(raw)
    transformed = transform_all(cleaned)
    print(f"\n[transform] Done. {len(transformed)} dataset(s) transformed.")
    for name, df in transformed.items():
        print(f"  {name}: {df.shape[1]} columns")