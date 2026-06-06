import pandas as pd
import numpy as np


def _get_df(transformed, key):
    """Find a dataset by its TS prefix."""
    match = next((v for k, v in transformed.items() if k.upper().startswith(key)), None)
    return match


def _quartile_analysis(df, group_col, value_col):
    """Split df into 4 quartiles by group_col, return mean of value_col per quartile."""
    df = df.copy().dropna(subset=[group_col, value_col])
    df["quartile"] = pd.qcut(df[group_col], q=4,
                              labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"])
    return df.groupby("quartile", observed=True)[value_col].mean().round(2)


def analyze_rq1(transformed):
    """RQ1: Does working-age population % influence employment rate?"""
    print("\n[analyze] RQ1: Working-age population vs employment rate")
    ageing = _get_df(transformed, "TS007")
    labour = _get_df(transformed, "TS066")
    if ageing is None or labour is None:
        return {}

    merged = ageing[["area_code", "pct_working_age"]].merge(
        labour[["area_code", "employment_rate"]], on="area_code"
    )
    r = merged[["pct_working_age", "employment_rate"]].corr().iloc[0, 1]
    quartiles = _quartile_analysis(merged, "pct_working_age", "employment_rate")
    print(f"  Pearson r = {r:.2f}")
    print(f"  Quartile means:\n{quartiles}")
    return {"rq1_correlation": round(r, 2), "rq1_quartiles": quartiles}


def analyze_rq2(transformed):
    """RQ2: Which areas have the oldest populations?"""
    print("\n[analyze] RQ2: Geographic distribution of elderly population")
    ageing = _get_df(transformed, "TS007")
    if ageing is None:
        return {}

    top10 = ageing.nlargest(10, "pct_elderly")[["geography", "pct_elderly"]].round(2)
    nat_avg = ageing["pct_elderly"].mean().round(2)
    print(f"  National average: {nat_avg}%")
    print(f"  Top 10 oldest areas:\n{top10.to_string(index=False)}")
    return {"rq2_national_avg": nat_avg, "rq2_top10": top10}


def analyze_rq3(transformed):
    """RQ3: What is the distribution of dependency ratios?"""
    print("\n[analyze] RQ3: Dependency ratio distribution")
    ageing = _get_df(transformed, "TS007")
    if ageing is None:
        return {}

    dr = ageing["dependency_ratio"]
    above_70 = (dr > 0.70).sum()
    pct_above = (above_70 / len(dr) * 100).round(1)
    nat_avg = dr.mean().round(2)
    top10 = ageing.nlargest(10, "dependency_ratio")[["geography", "dependency_ratio"]].round(2)
    print(f"  National average: {nat_avg}")
    print(f"  Areas above 0.70: {above_70} ({pct_above}%)")
    print(f"  Top 10:\n{top10.to_string(index=False)}")
    return {"rq3_nat_avg": nat_avg, "rq3_above_70": int(above_70), "rq3_top10": top10}


def analyze_rq4(transformed):
    """RQ4: Does education attainment affect employment?"""
    print("\n[analyze] RQ4: Education attainment vs employment rate")
    edu = _get_df(transformed, "TS067")
    labour = _get_df(transformed, "TS066")
    if edu is None or labour is None:
        return {}

    merged = edu[["area_code", "qualification_rate", "no_qual_rate"]].merge(
        labour[["area_code", "employment_rate", "unemployment_rate"]], on="area_code"
    )
    r_qual = merged[["qualification_rate", "employment_rate"]].corr().iloc[0, 1]
    r_noqual = merged[["no_qual_rate", "unemployment_rate"]].corr().iloc[0, 1]
    quartiles = _quartile_analysis(merged, "qualification_rate", "employment_rate")
    print(f"  L4+ vs employment r = {r_qual:.2f}")
    print(f"  No quals vs unemployment r = {r_noqual:.2f}")
    print(f"  Quartile means:\n{quartiles}")
    return {"rq4_r_qual": round(r_qual, 2), "rq4_r_noqual": round(r_noqual, 2)}


def analyze_rq5(transformed):
    """RQ5: Regional inequality within comparable population bands."""
    print("\n[analyze] RQ5: Employment inequality within population bands")
    demog = _get_df(transformed, "TS001")
    labour = _get_df(transformed, "TS066")
    if demog is None or labour is None:
        return {}

    total_col = [c for c in demog.columns if "total" in c]
    if not total_col:
        print("  Could not find total population column")
        return {}

    merged = demog[["area_code", "geography", total_col[0]]].merge(
        labour[["area_code", "employment_rate"]], on="area_code"
    )
    merged.rename(columns={total_col[0]: "population"}, inplace=True)
    bands = [0, 50000, 100000, 200000, 400000, float("inf")]
    labels = ["<50k", "50-100k", "100-200k", "200-400k", "400k+"]
    merged["band"] = pd.cut(merged["population"], bins=bands, labels=labels)
    summary = merged.groupby("band", observed=True)["employment_rate"].agg(
        ["min", "mean", "max"]
    ).round(2)
    print(f"  Employment rate range by population band:\n{summary}")
    return {"rq5_summary": summary}


def analyze_all(transformed):
    results = {}
    results.update(analyze_rq1(transformed))
    results.update(analyze_rq2(transformed))
    results.update(analyze_rq3(transformed))
    results.update(analyze_rq4(transformed))
    results.update(analyze_rq5(transformed))
    print("\n[analyze] All research questions answered!")
    return results


if __name__ == "__main__":
    from ingest import load_all
    from clean import clean_all
    from transform import transform_all
    raw = load_all()
    cleaned = clean_all(raw)
    transformed = transform_all(cleaned)
    analyze_all(transformed)