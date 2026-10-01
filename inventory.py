#!/usr/bin/env python3
"""
Step 4 — Dataset inventory script (v2: handles both schema versions).

Walks the data/ directory, reports what's actually on disk for every CSV
(file size, row count, columns + dtypes, missing-value rates), then
re-derives the automation/augmentation split for every release found and
prints a release-over-release trend table plus a claimed-vs-actual check
against the Step 3 verification targets.

Two schema versions exist in this dataset and are both handled here:
  - Releases 3-5: long format with facet/variable/cluster_name columns.
    Automation = sum of 'directive' + 'feedback loop' cluster rows where
    variable == 'collaboration_pct' and facet == 'collaboration'.
  - Release 6+: wide format with category_name/metric_id/node_name columns.
    Automation/augmentation are pre-aggregated as
    'collaboration_bucket_automation_pct' / '..._augmentation_pct' under
    category_name == 'overall'.

Usage:
    python3 src/inventory.py [--data-dir data/economic_index]
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

AUTOMATION_LABELS = ["directive", "feedback loop"]
AUGMENTATION_LABELS = ["learning", "task iteration", "validation"]

# Targets recorded in step3_documentation_summary.md (as of this writing)
CLAIMED = {
    "release_2025_09_15": {"claude_automation": 49.10, "api_automation": 77.37},
    "release_2026_01_15": {"claude_automation": 45.36, "api_automation": 74.61},
    "release_2026_03_24": {"claude_automation": 44.16, "api_automation": 67.63},
    "release_2026_06_26": {"claude_automation": 48.62, "api_automation": 94.22},  # most recent monthly snapshot
}
TOLERANCE_PP = 1.0


# ---------------------------------------------------------------------------
# Part 1: generic file inventory
# ---------------------------------------------------------------------------

def human_size(num_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}TB"


def inventory_csv(path: Path) -> dict:
    size = path.stat().st_size
    df = pd.read_csv(path, low_memory=False)
    missing_rates = (df.isna().mean() * 100).round(2).to_dict()
    return {
        "path": str(path),
        "size_human": human_size(size),
        "size_bytes": size,
        "n_rows": len(df),
        "n_cols": len(df.columns),
        "columns": list(df.columns),
        "missing_pct": missing_rates,
    }


def print_inventory(data_dir: Path) -> None:
    print("=" * 100)
    print("FILE INVENTORY")
    print("=" * 100)
    for path in sorted(data_dir.rglob("*.csv")):
        r = inventory_csv(path)
        print(f"\n{r['path']}")
        print(f"  size: {r['size_human']} ({r['size_bytes']:,} bytes)")
        print(f"  rows: {r['n_rows']:,}   cols: {r['n_cols']}")
        print(f"  columns: {', '.join(r['columns'])}")
        nonzero = [(c, p) for c, p in r["missing_pct"].items() if p > 0]
        if nonzero:
            print("  missing-value rates (>0% only):")
            for col, pct in sorted(nonzero, key=lambda kv: -kv[1])[:5]:
                print(f"    {col}: {pct}%")
        else:
            print("  missing-value rates: 0% across all columns")


# ---------------------------------------------------------------------------
# Part 2: automation/augmentation extraction, both schema versions
# ---------------------------------------------------------------------------

def extract_long_format(api_path: Path, claude_path: Path) -> dict:
    """Releases 3-5: facet/variable/cluster_name long format."""
    api = pd.read_csv(api_path, low_memory=False)
    claude = pd.read_csv(claude_path, low_memory=False)

    def pct(df, geo_col, geo_val):
        sub = df[(df["facet"] == "collaboration") & (df["variable"] == "collaboration_pct") & (df[geo_col] == geo_val)]
        return sub.set_index("cluster_name")["value"]

    api_pct = pct(api, "geo_id", "GLOBAL")
    claude_pct = pct(claude, "geography", "global")

    return {
        "api_automation": api_pct[AUTOMATION_LABELS].sum(),
        "api_augmentation": api_pct[AUGMENTATION_LABELS].sum(),
        "claude_automation": claude_pct[AUTOMATION_LABELS].sum(),
        "claude_augmentation": claude_pct[AUGMENTATION_LABELS].sum(),
    }


def extract_bucket_format(api_path: Path, claude_path: Path) -> dict:
    """Release 6+: category_name/metric_id wide format with pre-aggregated buckets."""
    api = pd.read_csv(api_path, low_memory=False)
    claude = pd.read_csv(claude_path, low_memory=False)

    def latest_bucket(df, geo_col, geo_val, metric):
        sub = df[(df["category_name"] == "overall") & (df["metric_id"] == metric) & (df[geo_col] == geo_val)]
        sub = sub.sort_values("date_end")
        return sub["value"].iloc[-1]  # most recent monthly snapshot

    return {
        "api_automation": latest_bucket(api, "geo_id", "GLOBAL", "collaboration_bucket_automation_pct"),
        "api_augmentation": latest_bucket(api, "geo_id", "GLOBAL", "collaboration_bucket_augmentation_pct"),
        "claude_automation": latest_bucket(claude, "geo_id", "GLOBAL", "collaboration_bucket_automation_pct"),
        "claude_augmentation": latest_bucket(claude, "geo_id", "GLOBAL", "collaboration_bucket_augmentation_pct"),
    }


# release folder -> (schema, api glob, claude glob)
RELEASES = [
    ("release_2025_09_15", "long", "aei_raw_1p_api_*.csv", "aei_raw_claude_ai_*.csv"),
    ("release_2026_01_15", "long", "aei_raw_1p_api_*.csv", "aei_raw_claude_ai_*.csv"),
    ("release_2026_03_24", "long", "aei_raw_1p_api_*.csv", "aei_raw_claude_ai_*.csv"),
    ("release_2026_06_26", "bucket", "aei_1p_api_*.csv", "aei_claude_ai_*.csv"),
]


def build_trend(data_dir: Path) -> list[dict]:
    trend = []
    for folder, schema, api_glob, claude_glob in RELEASES:
        rel_dir = data_dir / folder
        if not rel_dir.exists():
            continue
        api_path = next(rel_dir.rglob(api_glob), None)
        claude_path = next(rel_dir.rglob(claude_glob), None)
        if api_path is None or claude_path is None:
            continue
        extractor = extract_long_format if schema == "long" else extract_bucket_format
        stats = extractor(api_path, claude_path)
        stats["release"] = folder
        stats["schema"] = schema
        stats["gap"] = stats["api_automation"] - stats["claude_automation"]
        trend.append(stats)
    return trend


def print_trend_and_verify(trend: list[dict]) -> None:
    print("\n" + "=" * 100)
    print("RELEASE-OVER-RELEASE AUTOMATION GAP TREND")
    print("=" * 100)
    header = f"{'Release':22} {'Schema':8} {'API auto':>10} {'API aug':>10} {'Claude auto':>12} {'Claude aug':>12} {'Gap (pp)':>10}"
    print(header)
    print("-" * len(header))
    for t in trend:
        print(f"{t['release']:22} {t['schema']:8} {t['api_automation']:>9.2f}% {t['api_augmentation']:>9.2f}% "
              f"{t['claude_automation']:>11.2f}% {t['claude_augmentation']:>11.2f}% {t['gap']:>9.2f}")

    print("\n" + "=" * 100)
    print("CLAIMED vs. ACTUAL (Step 3 targets)")
    print("=" * 100)
    any_mismatch = False
    for t in trend:
        claimed = CLAIMED.get(t["release"])
        if not claimed:
            continue
        for key in ("claude_automation", "api_automation"):
            diff = t[key] - claimed[key]
            match = abs(diff) <= TOLERANCE_PP
            any_mismatch = any_mismatch or not match
            flag = "OK" if match else "MISMATCH"
            print(f"{t['release']:22} {key:20} claimed={claimed[key]:>6.2f}% actual={t[key]:>6.2f}% diff={diff:>+6.2f}pp  {flag}")

    if any_mismatch:
        print("\n[FINDING] mismatch(es) found — see above.")
    else:
        print(f"\nAll claimed targets matched within {TOLERANCE_PP}pp tolerance.")

    print("\n[CAUTION] The gap widens sharply at release 6 (schema change: weekly "
          "snapshot -> monthly aggregate, pre-computed bucket field instead of "
          "summed cluster rows). Verify this is a real trend and not a "
          "measurement-method artifact before drawing conclusions in the final report.")


# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data/economic_index"))
    args = parser.parse_args()

    if not args.data_dir.exists():
        print(f"Data directory not found: {args.data_dir}", file=sys.stderr)
        return 1

    print_inventory(args.data_dir)
    trend = build_trend(args.data_dir)
    print_trend_and_verify(trend)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
