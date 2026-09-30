"""
Step 4 — Inventory script.

Enumerates what we actually have in data/ (files, sizes, row counts,
columns/dtypes, missing-value rates) and checks specific verification
targets pulled from the Step 3 paper read (Sept-2025 AEI geographic
report) against the actual 2026-06-26 release files.

Run from repo root: python src/inventory.py
Writes a full text report to stdout; the claimed-vs-actual table is
hand-copied into NOTES.md 
"""

import os
import json
import pandas as pd

DATA_DIR = "data"
FILES = [
    "C:\\Users\\ramab\\OneDrive\\Desktop\\capstone-1\\data-science-capstone\\data\\aei_claude_ai_2026-06-26.csv",
    "C:\\Users\\ramab\\OneDrive\\Desktop\\capstone-1\\data-science-capstone\\data\\aei_1p_api_2026-06-26.csv",
]

EXPECTED_COLUMNS = {
    "date_start": "object",
    "date_end": "object",
    "geo_id": "object",
    "geo_level": "object",
    "category_name": "object",
    "hierarchy_level": "int64",
    "metric_id": "object",
    "value": "float64",
    "node_name": "object",
    "node_external_id": "object",
}


def file_inventory(path):
    size_bytes = os.path.getsize(path)
    df = pd.read_csv(path)
    n_rows, n_cols = df.shape

    col_report = {}
    for col in df.columns:
        col_report[col] = {
            "dtype": str(df[col].dtype),
            "expected_dtype": EXPECTED_COLUMNS.get(col, "UNKNOWN"),
            "pct_missing": round(100 * df[col].isna().mean(), 3),
            "n_unique": int(df[col].nunique()),
        }

    return df, {
        "path": path,
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / 1e6, 1),
        "n_rows": n_rows,
        "n_cols": n_cols,
        "columns": col_report,
        "geo_level_counts": df["geo_level"].value_counts().to_dict(),
        "category_name_counts": df["category_name"].value_counts().to_dict(),
        "date_start_min": str(df["date_start"].min()),
        "date_start_max": str(df["date_start"].max()),
        "n_unique_geo_id": int(df["geo_id"].nunique()),
    }


def get_metric(df, geo_id, category_name, metric_id):
    """Pull a single metric value for a given geography, or None if absent."""
    hit = df[
        (df["geo_id"] == geo_id)
        & (df["category_name"] == category_name)
        & (df["metric_id"] == metric_id)
    ]
    if hit.empty:
        return None
    if hit.shape[0] > 1:
        # multiple rows (e.g. different date windows) -- return all
        return hit["value"].tolist()
    return hit["value"].iloc[0]


def main():
    reports = {}
    dfs = {}
    for fname in FILES:
        path = os.path.join(DATA_DIR, fname)
        df, report = file_inventory(path)
        dfs[fname] = df
        reports[fname] = report
        print(f"\n=== {fname} ===")
        print(json.dumps(report, indent=2, default=str))

    # ---- Claimed-vs-actual checks against Step 3 verification targets ----
    claude_ai = dfs["aei_claude_ai_2026-06-26.csv"]

    print("\n=== Verification-target spot checks (Step 3 headline numbers) ===")
    checks = [
        ("USA", "overall", "usage_per_capita_index", "US AUI ~= 3.62 (Sept 2025)"),
        ("GBR", "overall", "usage_per_capita_index", "UK AUI ~= 2.67 (Sept 2025)"),
        ("CAN", "overall", "usage_per_capita_index", "Canada AUI ~= 2.91 (Sept 2025)"),
        ("US-DC", "overall", "usage_per_capita_index", "DC AUI ~= 3.82 (Sept 2025)"),
        ("US-UT", "overall", "usage_per_capita_index", "Utah AUI ~= 3.78 (Sept 2025)"),
    ]
    results = []
    for geo_id, cat, metric, claim in checks:
        actual = get_metric(claude_ai, geo_id, cat, metric)
        results.append((geo_id, claim, actual))
        print(f"{geo_id:8s} | claimed: {claim:35s} | actual (2026-06-26 file): {actual}")

    return reports, results


if __name__ == "__main__":
    main()
