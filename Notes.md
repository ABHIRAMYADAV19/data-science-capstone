**Research question(Q2):**What explains geographic differences in AI adoption? Join Anthropic Economic Index (AEI) geographic usage data (state- and country-level, 3rd release onward) with public covariates — BLS occupational employment and wages, Census industry mix, and broadband access — and model which regional characteristics predict per-capita adoption and the automation/augmentation ratio.
---
## Step 2 - Dataset Provenance
### Primary dataset: Anthropic Economic Index (AEI), 2026-06-26 release ("Cadences")

- **Source (primary, not a mirror):** Hugging Face dataset repository `Anthropic/EconomicIndex`
  - Repo root: https://huggingface.co/datasets/Anthropic/EconomicIndex
  - Release folder used: https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2026_06_26
  - Exact files acquired:
    - `release_2026_06_26/data/aei_claude_ai_2026-06-26.csv` (Claude.ai consumer usage, geo-disaggregated — this is the file that carries U.S. state and country breakdowns)
    - `release_2026_06_26/data/aei_1p_api_2026-06-26.csv` (first-party API usage — **note:** confirmed by inspection this file ships at `geo_level = global` only in this release, so it cannot supply the state/country join; kept for context/comparison only, not for the geographic regression)
- **Release / version:** 2026-06-26 release, publicly labeled "Cadences" — the 6th major AEI data release. This is the AEI's sixth iteration overall (initial release 2025-02-10; geographic breakdowns were introduced in the 3rd release, 2025-09-15, and have been included in every release since).
- **Accompanying report:** "Anthropic Economic Index report: Cadences" (June 26, 2026) — https://www.anthropic.com/research/economic-index-june-2026-report
- **Download date:** *September 12 2026*
- **License:**
  - Data: **CC-BY 4.0** (Creative Commons Attribution)
  - Any accompanying Anthropic code (e.g., preprocessing notebooks in the repo): MIT License
- **Citation (as requested by the authors, sixth release):**
  ```
  @online{anthropic2026aeiv6,
          author = {Maxim Massenkoff and Eva Lyubich and Szymon Sacher and Zoe Hitzig and Shaoyi Zhang and Ryan Heller and Peter McCrory},
          title = {Anthropic Economic Index report: Cadences},
          date = {2026-06-26},
          year = {2026},
          url = {https://www.anthropic.com/research/economic-index-june-2026-report},
  }
  ```
  - The underlying measurement methodology (O*NET task mapping, automation/augmentation classification, privacy-preserving "Clio" clustering) is described in the original AEI methods paper, which should also be cited:
  ```
  @misc{handa2025economictasksperformedai,
        title={Which Economic Tasks are Performed with AI? Evidence from Millions of Claude Conversations},
        author={Kunal Handa and Alex Tamkin and Miles McCain and Saffron Huang and Esin Durmus and Sarah Heck and Jared Mueller and Jerry Hong and Stuart Ritchie and Tim Belonax and Kevin K. Troy and Dario Amodei and Jared Kaplan and Jack Clark and Deep Ganguli},
        year={2025},
        eprint={2503.04761},
        archivePrefix={arXiv},
        primaryClass={cs.CY},
        url={https://arxiv.org/abs/2503.04761},
  }
  ```

### Planned public covariate sources 

| Covariate | Source | Geographic unit | Status |
|---|---|---|---|
| Occupational employment & wages | BLS Occupational Employment and Wage Statistics (OEWS), May 2025 release (this is the same OEWS vintage the AEI report itself uses for wage data, per the report's methodology notes) | State | Not yet downloaded |
| Industry mix | Census Bureau (County Business Patterns or ACS industry-by-state tables) | State | Not yet downloaded |
| Broadband access | FCC National Broadband Map / ACS broadband subscription tables | State | Not yet downloaded |
| Population (for per-capita denominators) | Census Bureau population estimates (working-age population, to mirror AEI's own per-capita convention) | State / country | Not yet downloaded |

---

## Step 3 — Dataset Summary (from the papers, before opening any data file)

Two papers matter here, for different reasons: the **3rd-release report** (Sept 2025) is where the geographic framing and headline numbers for Q2 come from; the **6th-release report** (the one attached to the actual files downloaded) documents the current collection/labeling pipeline. Both are read below.

### How the data was collected

- The underlying data is **Claude.ai consumer conversations** (Free/Pro/Max accounts; the 6th release also folds in Claude Desktop and "Cowork" sessions) and, separately, **first-party API traffic**. Nothing is scraped or self-reported — it is Anthropic's own product usage logs.
- Conversations are **sampled**, not fully censused. Earlier releases (through the 5th) drew a single ~7-day snapshot per release; the 6th release switched to **continuous daily/hourly sampling**, which is why this file has monthly date ranges (`date_start`/`date_end`) rather than one fixed week.
- **Every conversation is read and classified by another instance of Claude**, not by a human annotator — this is Anthropic's privacy-preserving "Clio" system. Classifiers map each conversation to (a) an O*NET task / SOC occupation, (b) a "collaboration mode" (directive, feedback loop, task iteration, learning, or validation), and, since the 6th release, (c) an "artifact" category (one of ~30 output types, e.g. document, code snippet, presentation).
- **Automation vs. augmentation** is a derived split of the collaboration-mode classifier: *directive* + *feedback loop* → automation; *task iteration*, *learning*, *validation* → augmentation. This is exactly the ratio Q2 asks us to model.
- **Geography is inferred from the IP address** of the conversation (confirmed in the 6th-release report's methodology footnotes), then aggregated up to country or, for the US, state (ISO 3166-2 subdivision) before publication — Anthropic never publishes conversation-level geolocation, only pre-aggregated shares/means/indices per geography.
- Cells with too few observations to preserve privacy are suppressed, so state/country coverage is uneven by design.

### Unit of observation

**A row is one metric value for one geography × category × facet combination** — *not* a conversation. E.g. one row might be: *(May 2026, US-CA, subregion, onet task facet, `usage_per_capita_index`, 3.71)*. Confirmed directly from the file's own columns (`date_start, date_end, geo_id, geo_level, category_name, hierarchy_level, metric_id, value, node_name, node_external_id`) and from the release's own documentation, which states each row is "one metric value for a specific geography and facet combination." All the real microdata (individual conversations) stay inside Anthropic; what's published is already-aggregated statistics.

### How labels were produced

- **Occupation/task labels** (`category_name = onet` / `soc_occupation`): automated classifier mapping conversation content to the O*NET-SOC taxonomy (U.S. Dept. of Labor).
- **Collaboration-mode labels** (directive / feedback loop / task iteration / learning / validation, and the automation/augmentation buckets derived from them): automated classifier, described in the original AEI methods paper (Handa et al. 2025) and reused in every subsequent release.
- **Artifact labels** (new in the 6th release): a new classifier that tags each conversation's primary output into one of ~30 categories.
- **Geography**: inferred from IP address, not self-reported.
- None of these labels are human-annotated at the conversation level — they are all classifier output, which matters for Step 5.

### Headline numbers → verification targets for Step 4

From the 3rd-release report:

1. **Global GDP–adoption elasticity:** a 1% higher GDP per capita is associated with a **0.7% higher** Anthropic AI Usage Index (AUI, i.e. `usage_per_capita_index`) across countries.
2. **US state GDP–adoption elasticity:** within the US, a 1% increase in state GDP per capita is associated with a **1.8% increase** in AUI — a steeper elasticity than the global one — and income differences explain **less than half** the cross-state variation.
3. **Specific per-capita index values to spot-check:** US AUI ≈ 3.62, Canada ≈ 2.91, UK ≈ 2.67 (countries); within the US, Washington DC ≈ 3.82 and Utah ≈ 3.78 led per-capita usage. (These are from the Sept-2025 sample, not the June-2026 file we actually have — so in Step 4 I'm checking that our file's `usage_per_capita_index` values for these same geographies are in the same *ballpark and rank order*, not identical, since usage has grown and the sampling method changed between releases.)

---

## Step 4 — Inventory

Script: `src/inventory.py` (run with `python src/inventory.py` from repo root). It enumerates both files' sizes, row/column counts, dtypes, missing-value rates, and re-derives the Step 3 verification-target values directly from the actual data.

### File inventory

| File | Size | Rows | Cols | Date range covered | Unique `geo_id` |
|---|---|---|---|---|---|
| `aei_claude_ai_2026-06-26.csv` | 219.2 MB | 1,636,573 | 10 | 2026-04-01 to 2026-05-01 (i.e. two monthly windows: Apr and May) | 774 |
| `aei_1p_api_2026-06-26.csv` | 77.3 MB | 491,705 | 10 | 2026-04-01 to 2026-05-01 | 1 (`GLOBAL` only) |

### Columns / dtypes 

| Column | dtype | Missing (NaN) rate |
|---|---|---|
| `date_start`, `date_end` | string | 0% |
| `geo_id`, `geo_level` | string | 0% |
| `category_name` | string (`onet` / `soc_occupation` / `request` / `overall`) | 0% |
| `hierarchy_level` | int (0–3) | 0% |
| `metric_id` | string (53 distinct metrics) | 0% |
| `value` | float | 0% |
| `node_name`, `node_external_id` | string | 0% |

**No column has any NaNs in either file.** But this is *not* the same as complete coverage — see the mismatch below. Anthropic's privacy suppression works by **omitting rows entirely**, not by writing nulls, so a "0% missing" column-level number is technically true and also hides the real gap.

### Claimed-vs-actual table (verification targets from Step 3, checked against the actual data)

| Claim (Step 3, from Sept-2025 report) | Actual value found in `aei_claude_ai_2026-06-26.csv` (`usage_per_capita_index`, `overall` category) | Match? |
|---|---|---|
| US AUI ≈ 3.62 | 3.87 (Apr), 4.25 (May) | **Directionally consistent** — higher, as expected given ~9 months of usage growth |
| Canada AUI ≈ 2.91 | 4.65 (Apr), 4.13 (May) | **Consistent with growth**, and now ranks *above* the US, a reordering worth investigating |
| UK AUI ≈ 2.67 | 3.35 (Apr), 3.40 (May) | **Consistent with growth** |
| Washington DC AUI ≈ 3.82 | 3.32 (Apr), 3.72 (May) | **Roughly flat / mild decline**, unlike every other geography checked, which all grew |
| Utah AUI ≈ 3.78 | 1.21 (Apr), 1.26 (May) | **Mismatch.** A ~3x drop, while national and most other geographies grew. This does not fit a simple "measurement noise" explanation and needs investigation (methodology change between releases? sampling-window difference? a real, large shift in Utah's relative usage? population-denominator revision?). Flagging this as a finding, not smoothing it over. |

### Coverage gap 

The `usage_per_capita_index` metric is **not published for every geography** in the file:

- **Country level:** 121/121 countries have it (100% coverage).
- **US states:** 51/52 US subregions have it — every state and DC **except Puerto Rico** (`US-PR`), consistent with the original report's methodology, which was scoped to the 50 states + DC.
- **Non-US subregions (e.g., Canadian provinces, Brazilian states, South African provinces):** **0/651 have it.** The per-capita index is computed at the subregion level for the US only; for the rest of the world it exists only at the country level.

**Why this matters for Q2:** the research question asks to model per-capita adoption using regional characteristics. That regression is only directly feasible **within the US** at the subregion (state) level, or **across countries** at the country level — there is no cross-national state/province-level per-capita comparison available in this dataset. This reshapes the project into two separate regressions (US state-level; global country-level) rather than one pooled subnational model, and that scoping decision should be made explicit in the modeling write-up, not discovered later.

### Other structural notes from the inventory

- `hierarchy_level` takes values {0,1,2,3} — this is a nesting depth indicator within `category_name` (e.g., broad SOC occupation vs. detailed O*NET task), not a data-quality field; worth mapping out before joining, so covariates get matched at a consistent granularity.
- Both files cover the exact same two monthly windows (April, May 2026) — good, no date misalignment to fix before joining.
- `value` has 10,182 unique values in the Claude.ai file vs. only 9,497 in the API file, consistent with the Claude.ai file simply having ~3.3x more rows, not a scale/units mismatch.

---