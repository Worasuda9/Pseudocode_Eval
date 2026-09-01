"""
compare_scores.py — Inter-rater agreement analysis (Cohen's Kappa)
=====================================================================

Compares qualitative scores (Excellent/Good/Fair/Poor) across four
sources — two human raters and two LLM evaluators (Gemini, OpenAI) —
using Cohen's Weighted Kappa for every pairwise combination, across
all four rubric dimensions.

Expected input files (same folder as this script, or edit INPUT_DIR):
    rater1_scores.csv
    rater2_scores.csv
    gemini_scores.csv
    openai_scores.csv

Expected columns in each CSV:
    problem_id, model, level, question, pseudocode,
    correctness, completeness, clarity, efficiency

Rows are matched across files using (problem_id, model, level) as the
join key — this triple should uniquely identify a submission across
all four files.

Output:
    - Printed kappa table for every pair x every dimension
    - A CSV summary: kappa_results.csv
    - A human-readable interpretation guide for each kappa value

Usage:
    python compare_scores.py
"""

import pandas as pd
from sklearn.metrics import cohen_kappa_score
from itertools import combinations
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────

INPUT_DIR = Path(".")  # change if your CSVs are in a different folder

SOURCES = {
    "rater1": "full_human1.csv",
    "rater2": "full_human2.csv",
    "gemini": "full_gemini4.2.csv",
    "openai": "full_gemini4.2.csv",
}

DIMENSIONS = ["correctness", "completeness", "clarity", "efficiency"]

# Ordinal mapping — required for WEIGHTED kappa, which accounts for
# how far apart two disagreeing scores are (Poor vs Fair is a smaller
# disagreement than Poor vs Excellent). Plain (unweighted) kappa treats
# every disagreement as equally bad, which understates agreement on an
# ordinal qualitative scale like this one.
SCORE_ORDER = {"Poor": 0, "Fair": 1, "Good": 2, "Excellent": 3}

JOIN_KEYS = ["problem_id", "model", "level"]

# ──────────────────────────────────────────────────────────────────────
# Kappa interpretation guide (Landis & Koch, 1977 — standard reference)
# ──────────────────────────────────────────────────────────────────────

def interpret_kappa(k: float) -> str:
    if k < 0:
        return "Poor (worse than chance)"
    elif k < 0.20:
        return "Slight"
    elif k < 0.40:
        return "Fair"
    elif k < 0.60:
        return "Moderate"
    elif k < 0.80:
        return "Substantial"
    else:
        return "Almost perfect"


# ──────────────────────────────────────────────────────────────────────
# Load and align data
# ──────────────────────────────────────────────────────────────────────

def load_all_sources() -> dict[str, pd.DataFrame]:
    """Load each CSV, forward-fill missing 'question' values per problem_id."""
    data = {}
    for name, filename in SOURCES.items():
        path = INPUT_DIR / filename
        if not path.exists():
            raise FileNotFoundError(
                f"Expected file not found: {path}\n"
                f"Make sure all four CSVs are in {INPUT_DIR.resolve()}"
            )
        df = pd.read_csv(path)

        missing_cols = set(JOIN_KEYS + DIMENSIONS) - set(df.columns)
        if missing_cols:
            raise ValueError(
                f"{filename} is missing required columns: {missing_cols}"
            )

        # Normalise key columns for safe joining
        df["problem_id"] = df["problem_id"].astype(str).str.strip()
        df["model"] = df["model"].astype(str).str.strip()
        df["level"] = df["level"].astype(str).str.strip()

        # Normalise score values (strip whitespace, fix casing)
        for dim in DIMENSIONS:
            df[dim] = df[dim].astype(str).str.strip().str.capitalize()

        data[name] = df

    return data


def merge_on_keys(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge all four sources on (problem_id, model, level) so every row
    represents one submission scored by all four sources.

    Uses an inner join — only submissions scored by ALL FOUR sources
    are kept. Prints a warning if any submissions are dropped.
    """
    merged = None
    for name, df in data.items():
        subset = df[JOIN_KEYS + DIMENSIONS].copy()
        subset = subset.rename(columns={dim: f"{dim}__{name}" for dim in DIMENSIONS})

        if merged is None:
            merged = subset
        else:
            before = len(merged)
            merged = merged.merge(subset, on=JOIN_KEYS, how="inner")
            after = len(merged)
            if after < before:
                print(
                    f"⚠  Merging '{name}' dropped {before - after} rows "
                    f"(submissions not found in '{name}')"
                )

    return merged


# ──────────────────────────────────────────────────────────────────────
# Kappa computation
# ──────────────────────────────────────────────────────────────────────

def compute_kappa(
    merged: pd.DataFrame,
    source_a: str,
    source_b: str,
    dimension: str,
) -> dict:
    """
    Compute weighted Cohen's Kappa for one dimension between two sources.

    Returns a dict with the kappa value, n (number of compared rows),
    and the count of exact agreements.
    """
    col_a = f"{dimension}__{source_a}"
    col_b = f"{dimension}__{source_b}"

    scores_a = merged[col_a]
    scores_b = merged[col_b]

    # Drop rows where either score is missing or unrecognised
    valid_mask = scores_a.isin(SCORE_ORDER) & scores_b.isin(SCORE_ORDER)
    scores_a = scores_a[valid_mask]
    scores_b = scores_b[valid_mask]

    n = len(scores_a)
    if n == 0:
        return {"kappa": None, "n": 0, "agreement_pct": None}

    # Map to ordinal integers for weighted kappa
    ord_a = scores_a.map(SCORE_ORDER)
    ord_b = scores_b.map(SCORE_ORDER)

    kappa = cohen_kappa_score(ord_a, ord_b, weights="linear")
    exact_agreement = (ord_a == ord_b).sum()
    agreement_pct = 100 * exact_agreement / n

    return {"kappa": kappa, "n": n, "agreement_pct": agreement_pct}


def run_all_comparisons(merged: pd.DataFrame) -> pd.DataFrame:
    """
    Compute kappa for every pair of sources, across every dimension.

    Returns a tidy DataFrame: one row per (pair, dimension).
    """
    rows = []
    source_names = list(SOURCES.keys())

    for source_a, source_b in combinations(source_names, 2):
        for dim in DIMENSIONS:
            result = compute_kappa(merged, source_a, source_b, dim)
            rows.append({
                "comparison": f"{source_a} vs {source_b}",
                "dimension": dim,
                "n": result["n"],
                "kappa": result["kappa"],
                "agreement_pct": result["agreement_pct"],
                "interpretation": (
                    interpret_kappa(result["kappa"])
                    if result["kappa"] is not None else "N/A"
                ),
            })

    return pd.DataFrame(rows)


# ──────────────────────────────────────────────────────────────────────
# Reporting
# ──────────────────────────────────────────────────────────────────────

def print_summary(results: pd.DataFrame) -> None:
    print("\n" + "=" * 78)
    print("COHEN'S WEIGHTED KAPPA — ALL PAIRWISE COMPARISONS")
    print("=" * 78)

    for comparison in results["comparison"].unique():
        subset = results[results["comparison"] == comparison]
        print(f"\n{comparison}")
        print("-" * len(comparison))
        for _, row in subset.iterrows():
            if row["kappa"] is None:
                print(f"  {row['dimension']:14s}: no comparable data")
                continue
            print(
                f"  {row['dimension']:14s}: "
                f"κ = {row['kappa']:.3f}  "
                f"({row['interpretation']:15s})  "
                f"exact agreement = {row['agreement_pct']:.1f}%  "
                f"(n={row['n']})"
            )

    print("\n" + "=" * 78)
    print("KEY COMPARISONS FOR YOUR VALIDATION STUDY")
    print("=" * 78)

    human_pair = results[results["comparison"] == "rater1 vs rater2"]
    if not human_pair.empty:
        avg_human_kappa = human_pair["kappa"].mean()
        print(f"\nHuman-human baseline (rater1 vs rater2): "
              f"average κ = {avg_human_kappa:.3f}")
        print("  → This is your ceiling. No LLM should be expected to")
        print("    exceed human-human agreement.")

    for llm in ["gemini", "openai"]:
        llm_vs_r1 = results[
            results["comparison"].isin([f"rater1 vs {llm}", f"{llm} vs rater1"])
        ]
        llm_vs_r2 = results[
            results["comparison"].isin([f"rater2 vs {llm}", f"{llm} vs rater2"])
        ]
        if not llm_vs_r1.empty and not llm_vs_r2.empty:
            avg_llm_human = pd.concat([llm_vs_r1, llm_vs_r2])["kappa"].mean()
            print(f"\n{llm.capitalize()} vs human raters (averaged): "
                  f"κ = {avg_llm_human:.3f}")

    print("\nInterpretation guide (Landis & Koch, 1977):")
    print("  < 0.00        Poor (worse than chance)")
    print("  0.00 – 0.20   Slight")
    print("  0.20 – 0.40   Fair")
    print("  0.40 – 0.60   Moderate")
    print("  0.60 – 0.80   Substantial")
    print("  0.80 – 1.00   Almost perfect")


def print_per_dimension_breakdown(results: pd.DataFrame) -> None:
    """Show which dimension has the weakest/strongest agreement overall."""
    print("\n" + "=" * 78)
    print("AVERAGE KAPPA PER DIMENSION (across all pairwise comparisons)")
    print("=" * 78)

    dim_avg = (
        results.dropna(subset=["kappa"])
        .groupby("dimension")["kappa"]
        .mean()
        .sort_values(ascending=False)
    )

    for dim, avg_k in dim_avg.items():
        print(f"  {dim:14s}: average κ = {avg_k:.3f}  ({interpret_kappa(avg_k)})")

    print("\nDimensions with lower average kappa are the least reliably")
    print("scored across raters/models — worth investigating first if")
    print("you need to improve agreement.")


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main():
    print("Loading score files...")
    data = load_all_sources()

    print("Merging on (problem_id, model, level)...")
    merged = merge_on_keys(data)
    print(f"✓ {len(merged)} submissions matched across all 4 sources\n")

    if len(merged) == 0:
        print("✗ No matching rows found. Check that problem_id, model, "
              "and level values are consistent across all four CSVs.")
        return

    results = run_all_comparisons(merged)

    print_summary(results)
    print_per_dimension_breakdown(results)

    output_path = INPUT_DIR / "kappa_results.csv"
    results.to_csv(output_path, index=False)
    print(f"\n✓ Full results saved to {output_path}")


if __name__ == "__main__":
    main()