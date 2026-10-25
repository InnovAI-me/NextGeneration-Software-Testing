"""
analyze_literature.py

Generates descriptive statistics and figures from the systematic
literature review tracking sheet for the "Next-Generation Software
Testing" review paper.

Inputs:
    literature-review/papers-tracking.csv

Outputs:
    results/figures/publication_trend.png
    results/figures/technique_distribution.png
    results/tables/summary_stats.csv

Usage:
    python scripts/analyze_literature.py
"""

from __future__ import annotations

import pathlib

import pandas as pd
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
TRACKING_CSV = ROOT / "literature-review" / "papers-tracking.csv"
FIGURES_DIR = ROOT / "results" / "figures"
TABLES_DIR = ROOT / "results" / "tables"


def load_included_studies() -> pd.DataFrame:
    """Load the tracking sheet and filter to full-text included studies."""
    df = pd.read_csv(TRACKING_CSV)
    decision = df["decision_full_text"].astype("string").fillna("").str.lower()
    included = df[decision == "include"].copy()
    return included


def plot_publication_trend(df: pd.DataFrame) -> None:
    """Bar chart of included studies per publication year."""
    if df.empty:
        return
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    counts = df["year"].value_counts().sort_index()
    ax = counts.plot(kind="bar", color="#2b6cb0")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of included studies")
    ax.set_title("Publication Trend: Next-Generation Software Testing")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "publication_trend.png", dpi=200)
    plt.close()


def plot_technique_distribution(df: pd.DataFrame) -> None:
    """Bar chart of studies per technique category."""
    if df.empty:
        return
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    counts = df["technique_category"].fillna("unclassified").value_counts()
    ax = counts.plot(kind="barh", color="#2f855a")
    ax.set_xlabel("Number of studies")
    ax.set_ylabel("Technique category")
    ax.set_title("Distribution of Testing Technique Categories")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "technique_distribution.png", dpi=200)
    plt.close()


def write_summary_stats(df: pd.DataFrame) -> None:
    """Write basic summary statistics table."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(
        {
            "metric": [
                "total_included_studies",
                "earliest_year",
                "latest_year",
                "distinct_technique_categories",
                "distinct_venues",
            ],
            "value": [
                len(df),
                df["year"].min() if not df.empty else None,
                df["year"].max() if not df.empty else None,
                df["technique_category"].nunique(),
                df["venue"].nunique(),
            ],
        }
    )
    summary.to_csv(TABLES_DIR / "summary_stats.csv", index=False)


def main() -> None:
    df = load_included_studies()
    if df.empty:
        print(
            "No included studies found yet. Populate "
            f"{TRACKING_CSV} with decision_full_text='include' rows."
        )
    plot_publication_trend(df)
    plot_technique_distribution(df)
    write_summary_stats(df)
    print(f"Analyzed {len(df)} included studies. Outputs written to "
          f"{FIGURES_DIR} and {TABLES_DIR}.")


if __name__ == "__main__":
    main()
