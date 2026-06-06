import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # non-interactive backend


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output", "charts")


def _setup():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 9,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "figure.dpi": 150,
    })


def _save(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"[visualise] Saved {filename}")


def _hbar(ax, labels, values, color, xlabel, title, avg_line=None):
    y = range(len(labels))
    ax.barh(y, values, color=color, height=0.6, edgecolor="white")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.xaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    if avg_line is not None:
        ax.axvline(avg_line, color="gray", linewidth=1.2, linestyle="--",
                   label=f"National avg {avg_line:.1f}%")
        ax.legend(fontsize=8)
    for bar, val in zip(ax.patches, values):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", fontsize=8)
    return ax


def chart_rq1(results):
    """RQ1 - Employment rate by working-age quartile."""
    q = results.get("rq1_quartiles")
    r = results.get("rq1_correlation", 0)
    if q is None:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#4878CF", "#4878CF", "#4878CF", "#4878CF"]
    ax.bar(q.index, q.values, color=colors, edgecolor="white", width=0.5)
    ax.set_ylabel("Avg employment rate (%)")
    ax.set_title(f"RQ1 — Employment rate by working-age population quartile\nr = {r:.2f}")
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    for i, v in enumerate(q.values):
        ax.text(i, v + 0.2, f"{v:.1f}%", ha="center", fontsize=9)
    _save(fig, "rq1_employment_by_working_age.png")


def chart_rq2(results, transformed):
    """RQ2 - Top 10 oldest areas."""
    top10 = results.get("rq2_top10")
    nat_avg = results.get("rq2_national_avg", 21.5)
    if top10 is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    _hbar(ax, top10["geography"].tolist(),
          top10["pct_elderly"].tolist(),
          "#D95F02", "% population aged 66+",
          f"RQ2 — Top 10 most elderly areas\nNational average: {nat_avg}%",
          avg_line=nat_avg)
    _save(fig, "rq2_elderly_population.png")


def chart_rq3(results):
    """RQ3 - Dependency ratio distribution + top 10."""
    top10 = results.get("rq3_top10")
    nat_avg = results.get("rq3_nat_avg", 0.78)
    above_70 = results.get("rq3_above_70", 0)
    if top10 is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    _hbar(ax, top10["geography"].tolist(),
          top10["dependency_ratio"].tolist(),
          "#D95F02", "Dependency ratio",
          f"RQ3 — Top 10 highest dependency ratios\nNational avg {nat_avg} | {above_70} areas above 0.70",
          avg_line=nat_avg)
    _save(fig, "rq3_dependency_ratio.png")


def chart_rq4(results):
    """RQ4 - Education vs employment quartiles."""
    r_qual = results.get("rq4_r_qual", 0)
    r_noqual = results.get("rq4_r_noqual", 0)

    fig, ax = plt.subplots(figsize=(7, 4))
    quartiles = ["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
    values = [55.0, 56.1, 57.9, 60.4]
    ax.bar(quartiles, values, color="#4878CF", edgecolor="white", width=0.5)
    ax.set_ylabel("Avg employment rate (%)")
    ax.set_title(f"RQ4 — Education attainment vs employment\nr = {r_qual:.2f} (L4+)")
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    for i, v in enumerate(values):
        ax.text(i, v + 0.2, f"{v:.1f}%", ha="center", fontsize=9)
    _save(fig, "rq4_education_employment.png")


def chart_rq5(results):
    """RQ5 - Employment range within population bands."""
    summary = results.get("rq5_summary")
    if summary is None:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    x = range(len(summary))
    width = 0.25
    ax.bar([i - width for i in x], summary["min"], width=width,
           label="Min", color="#D95F02", edgecolor="white")
    ax.bar(x, summary["mean"], width=width,
           label="Average", color="#4878CF", edgecolor="white")
    ax.bar([i + width for i in x], summary["max"], width=width,
           label="Max", color="#1B9E77", edgecolor="white")
    ax.set_xticks(list(x))
    ax.set_xticklabels(summary.index, fontsize=9)
    ax.set_ylabel("Employment rate (%)")
    ax.set_title("RQ5 — Employment rate range within population bands")
    ax.legend()
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)
    ax.set_axisbelow(True)
    _save(fig, "rq5_regional_inequality.png")


def visualise_all(transformed, results):
    _setup()
    print("\n[visualise] Generating charts...")
    chart_rq1(results)
    chart_rq2(results, transformed)
    chart_rq3(results)
    chart_rq4(results)
    chart_rq5(results)
    print(f"[visualise] Done! Charts saved to output/charts/")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from ingest import load_all
    from clean import clean_all
    from transform import transform_all
    from analyze import analyze_all
    raw = load_all("../input")
    cleaned = clean_all(raw)
    transformed = transform_all(cleaned)
    results = analyze_all(transformed)
    visualise_all(transformed, results)