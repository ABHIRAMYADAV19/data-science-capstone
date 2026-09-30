Q3. Do consumers and businesses use AI differently on the same tasks? With Claude.ai and enterprise-API columns, you can hold the task fixed and compare interaction styles. Are companies systematically more automation-heavy than individuals? Does the gap differ by occupation category? This bears directly on the "will firms automate faster than workers augment?" debate, and the release-over-release trend in that gap is unstudied.

# Step 2 — Dataset Provenance
## Dataset
**The Anthropic Economic Index**

**Source URL:** https://huggingface.co/datasets/Anthropic/EconomicIndex

## Releases 

| # | Release folder | Report date | Window type | Has Claude.ai vs. API split? | Downloaded? |
|---|---|---|---|---|---|
| 3 | `release_2025_09_15` | 2025-09-15 | Weekly snapshot (Aug 4–11, 2025) | Yes | 
| 4 | `release_2026_01_15` | 2026-01-15 | Weekly snapshot (Nov 13–20, 2025) | Yes |
| 5 | `release_2026_03_24` | 2026-03-24 | Weekly snapshot (Feb 5–12, 2026) | Yes | 
| 6 | `release_2026_06_26` | 2026-06-26 | Monthly aggregate (Apr–May & May–Jun 2026) | Yes | 

Releases 1–2 remain excluded — no platform split exists yet.

**Schema note:** releases 3–5 share one long-format schema (`facet`/`variable`/`cluster_name` columns). Release 6 uses a different wide-format schema (`category_name`/`metric_id`/`node_name` columns) with automation/augmentation pre-aggregated. 

**Download date:** `<<September 18 2026 >>`

**License:** "Data released under CC-BY, code released under MIT License."

## Citations

**Methodology paper:**
Handa, K., Tamkin, A., McCain, M., Huang, S., Durmus, E., Heck, S., Mueller, J., Hong, J., Ritchie, S., Belonax, T., Troy, K.K., Amodei, D., Kaplan, J., Clark, J., & Ganguli, D. (2025). *Which Economic Tasks are Performed with AI? Evidence from Millions of Claude Conversations.* arXiv:2503.04761. https://arxiv.org/abs/2503.04761

**Per-release report citations:**
- **3rd release:** Appel, R., McCrory, P., Tamkin, A., Stern, M., McCain, M., & Neylon, T. (2025). *Uneven Geographic and Enterprise AI Adoption.* https://www.anthropic.com/research/anthropic-economic-index-september-2025-report
- **4th release:** Appel, R., Massenkoff, M., McCrory, P., McCain, M., Heller, R., Neylon, T., & Tamkin, A. (2026). *Economic Primitives.* https://www.anthropic.com/research/anthropic-economic-index-january-2026-report
- **5th release:** Massenkoff, M., Lyubich, E., McCrory, P., Appel, R., & Heller, R. (2026). *Learning Curves.* https://www.anthropic.com/research/economic-index-march-2026-report
- **6th release:** Massenkoff, M., Lyubich, E., Sacher, S., Hitzig, Z., Zhang, S., Heller, R., & McCrory, P. (2026). *Cadences.* https://www.anthropic.com/research/economic-index-june-2026-report

### Release 3 — `release_2025_09_15` (Aug 4–11, 2025)
| File | Size | Rows | Cols |
|---|---|---|---|
|  `aei_raw_1p_api_2025-08-04_to_2025-08-11.csv` | 6.7 MB | 33,794 | 10 |
|  `aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv` | 18.0 MB | 100,062 | 10 |

### Release 4 — `release_2026_01_15` (Nov 13–20, 2025)
| File | Size | Rows | Cols |
|---|---|---|---|
|  `aei_raw_1p_api_2025-11-13_to_2025-11-20.csv` | 41.5 MB | 187,772 | 10 |
|  `aei_raw_claude_ai_2025-11-13_to_2025-11-20.csv` | 94.1 MB | 458,778 | 10 |

### Release 5 — `release_2026_03_24` (Feb 5–12, 2026)
| File | Size | Rows | Cols |
|---|---|---|---|
|  `aei_raw_1p_api_2026-02-05_to_2026-02-12.csv` | 44.0 MB | 195,156 | 10 |
|  `aei_raw_claude_ai_2026-02-05_to_2026-02-12.csv` | 103.3 MB | 477,717 | 10 |

### Release 6 — `release_2026_06_26` (Apr–May & May–Jun 2026, monthly aggregate)
| File | Size | Rows | Cols |
|---|---|---|---|
|  `aei_1p_api_2026-06-26.csv` | 73.7 MB | 491,705 | 10 |
|  `aei_claude_ai_2026-06-26.csv` | 209.0 MB | 1,636,573 | 10 |


---



# Step 3 — Dataset Summary

## How the data was collected
Anthropic runs an internal, privacy-preserving pipeline called **Clio** over a sample of anonymized Claude conversations — roughly one million conversations drawn from a ~7-day window per release for releases 3–5 (e.g., Aug 4–11, 2025 for release 3; Nov 13–20, 2025 for release 4; Feb 5–12, 2026 for release 5). **Release 6 changes this: it reports monthly aggregates** (e.g., Apr 1–May 1, 2026 and May 1–Jun 1, 2026) rather than a single 7-day snapshot — a real methodology shift to note when comparing release 6 against releases 3–5. The sample is filtered down to conversations judged to be about *work*. No human ever reads an individual conversation; classification is fully automated, and only aggregate counts/shares are published — never raw text.

## Unit of observation
A row (in the raw/intermediate files) = one Claude conversation, automatically matched to a single task from **O\*NET** (the US Dept. of Labor's taxonomy of ~20,000 tasks under ~1,000 occupations — e.g., "debug software programs"). Each conversation also carries: a **platform** tag (`claude_ai` vs. `1p_api`) and an **interaction-pattern** tag. For RQ3, the platform tag is the key column — it's literally what lets us hold task fixed and compare consumer vs. enterprise behavior.


**New fields introduced in release 6, not present in releases 3–5:**
- `node_external_id` — an actual SOC occupation code (e.g. `49-9021.00`) alongside the occupation name, more reliable for joins than the long O*NET task-description strings used in earlier releases.
.

**Schema change in release 6, worth recording:** releases 3–5 use a long format with `facet`/`variable`/`cluster_name` columns, requiring you to sum `directive` + `feedback loop` cluster rows to get "automation." Release 6 uses an entirely different schema (`category_name`/`metric_id`/`node_name`) and, conveniently, provides the automation/augmentation split **pre-aggregated** as `collaboration_bucket_automation_pct` / `collaboration_bucket_augmentation_pct` — no manual summing needed. 

## How labels were produced
Both the O*NET task match and the automation/augmentation label are produced by an automated classifier (Claude itself, prompted against the O*NET catalog), not by human raters. Interaction patterns roll up into two buckets:
- **Automation** = *directive* (user delegates the whole task) + *feedback-loop* patterns
- **Augmentation** = *learning* + *task iteration* + *validation* patterns

## Headline numbers — verification targets, now with the full release-over-release trend

All four numbers below were **computed directly from the primary source files**, at the global level, using the collaboration facet/bucket fields:

| Release | Window | API automation | API augmentation | Claude.ai automation | Claude.ai augmentation | **Gap (API − Claude.ai)** |
|---|---|---|---|---|---|---|
| 3 | Aug 2025 (1 week) | 77.37% | 12.41% | 49.10% | 47.04% | **28.27 pp** |
| 4 | Nov 2025 (1 week) | 74.61% | 14.35% | 45.36% | 51.68% | **29.25 pp** |
| 5 | Feb 2026 (1 week) | 67.63% | 17.18% | 44.16% | 52.79% | **23.47 pp** |
| 6a | Apr–May 2026 (monthly) | 93.66% | 6.34% | 48.98% | 51.02% | **44.68 pp** |
| 6b | May–Jun 2026 (monthly) | 94.22% | 5.78% | 48.62% | 51.38% | **45.60 pp** |

**This is the actual RQ3 finding, and it is not a smooth trend — flag this explicitly rather than smoothing it over:**
- The gap first **narrows** from release 3 → 5 (28.3pp → 29.3pp → 23.5pp) — API automation drifts down (77% → 68%) while Claude.ai holds roughly steady (~44–49%).
- Then the gap **nearly doubles** by release 6 (23.5pp → ~45pp) — API automation jumps sharply back up to ~94%, while Claude.ai stays flat around 49%.
- **Before treating this as a real finding, rule out a measurement artifact first:** release 6's jump coincides exactly with the schema change (weekly snapshot → monthly aggregate, and a different pre-computed bucket field). This is Step 4's job — verify the release-6 numbers a second way if possible, and check release 6's `data_documentation.md` for whether the automation/augmentation bucket definition changed alongside the schema.

**Citations for the releases:**
- Handa, K. et al. (2025). *Which Economic Tasks are Performed with AI?* arXiv:2503.04761 (methodology; baseline 57/43 split, Claude.ai only, pre-dates API data).
- Appel, R. et al. (2025). *Anthropic Economic Index Report: Uneven Geographic and Enterprise AI Adoption* (release 3, Sep 2025).
- Appel, R. et al. (2026). *Anthropic Economic Index report: Economic Primitives* (release 4, Jan 2026).
- Massenkoff, M. et al. (2026). *Anthropic Economic Index report: Learning Curves* (release 5, Mar 2026).
- Massenkoff, M. et al. (2026). *Anthropic Economic Index report: Cadences* (release 6, Jun 2026).
---


# Step 4 — Inventory

## Task
Build an inventory. Write a script (not a one-off shell command) that enumerates what you actually have: files, sizes, row counts, columns/fields with types, and missing-value rates. Compare every count against the verification targets from Step 3 and record every mismatch. Mismatches are findings, not problems to hide.

## Script
`src/inventory.py` — walks `data/economic_index/`, reports size/rows/columns/missing-value rates for every CSV, then re-derives automation/augmentation shares for **all four releases** (handling both schema versions present in the data) and prints a release-over-release trend plus a claimed-vs-actual check against Step 3.
```bash
python3 src/inventory.py --data-dir data/economic_index
```

## File inventory — 

| Release | File | Size | Rows | Cols | Missing values |
|---|---|---|---|---|---|
| 3 | `aei_raw_1p_api_2025-08-04_to_2025-08-11.csv` | 6.7 MB | 33,794 | 10 | none |
| 3 | `aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv` | 18.0 MB | 100,062 | 10 | `cluster_name` 0.45%, `geo_id` 0.02% |
| 4 | `aei_raw_1p_api_2025-11-13_to_2025-11-20.csv` | 41.5 MB | 187,772 | 10 | `cluster_name` 0.02% |
| 4 | `aei_raw_claude_ai_2025-11-13_to_2025-11-20.csv` | 94.1 MB | 458,778 | 10 | `cluster_name` **10.62%**, `geo_id` 0.01% |
| 5 | `aei_raw_1p_api_2026-02-05_to_2026-02-12.csv` | 44.0 MB | 195,156 | 10 | `cluster_name` 0.01% |
| 5 | `aei_raw_claude_ai_2026-02-05_to_2026-02-12.csv` | 103.3 MB | 477,717 | 10 | `cluster_name` **11.59%**, `geo_id` 0.02% |
| 6 | `aei_1p_api_2026-06-26.csv` | 73.7 MB | 491,705 | 10 | none |
| 6 | `aei_claude_ai_2026-06-26.csv` | 209.0 MB | 1,636,573 | 10 | none |

**Missing-value finding, now precisely quantified:** `cluster_name` nulls on Claude.ai files climb steadily release over release — 0.45% (R3) → 10.62% (R4) → 11.59% (R5) → 0%. This is a structural pattern (facets like `country`/`state_us` don't use a cluster dimension, so `cluster_name` is null there by design), but the *rate* growing 25x from release 3 to release 5 is itself worth investigating — it likely means later releases added more non-cluster facets (e.g., more geographic breakdowns) rather than data quality degrading. 

**Schema finding:** releases 3–5 share one 10-column long format (`geo_id, geography, date_start, date_end, platform_and_product, facet, level, variable, cluster_name, value`). Release 6 uses a **different** 10-column wide format (`date_start, date_end, geo_id, geo_level, category_name, hierarchy_level, metric_id, value, node_name, node_external_id`) — same column count, genuinely different fields. Release 6 also has **zero missing values**.

## Release-over-release automation gap — the actual RQ3 finding

| Release | Window | API automation | Claude.ai automation | **Gap (pp)** |
|---|---|---|---|---|
| 3 | Aug 2025 (weekly) | 77.37% | 49.10% | **28.27** |
| 4 | Nov 2025 (weekly) | 74.61% | 45.36% | **29.25** |
| 5 | Feb 2026 (weekly) | 67.63% | 44.16% | **23.47** |
| 6 | May–Jun 2026 (monthly) | 94.22% | 48.62% | **45.60** |

**This is not a smooth trend, and that's the finding, not a problem to explain away:**
1. Releases 3→5: the gap **shrinks** (28.3 → 29.3 → 23.5 pp), driven mostly by API automation drifting down (77% → 68%) while Claude.ai holds steady (~44–49%).
2. Release 6: the gap **nearly doubles** to 45.6pp, driven by API automation jumping back up to 94%.

**Caution flagged by the script itself:** release 6's jump lines up exactly with the schema/methodology change (weekly snapshot → monthly aggregate; summed cluster rows → pre-computed bucket field). Before writing "the automation gap surged in mid-2026" as a real finding, this needs a robustness check — e.g., see if release 6's `data_documentation.md` confirms the bucket definition is identical to summing `directive` + `feedback loop` in the old schema.

## Claimed vs. Actual — verification

All four releases' `claude_automation` and `api_automation` figures matched the Step 3 claims exactly (0.00pp difference) — expected, since Step 3's targets were themselves computed from these same 8 primary files rather than secondary sources.

| Release | Metric | Claimed | Actual | Diff | Match? |
|---|---|---|---|---|---|
| 3 | Claude.ai automation | 49.10% | 49.10% | 0.00pp | 
| 3 | API automation | 77.37% | 77.37% | 0.00pp | 
| 4 | Claude.ai automation | 45.36% | 45.36% | 0.00pp | 
| 4 | API automation | 74.61% | 74.61% | 0.00pp | 
| 5 | Claude.ai automation | 44.16% | 44.16% | 0.00pp | 
| 5 | API automation | 67.63% | 67.63% | 0.00pp | 
| 6 | Claude.ai automation | 48.62% | 48.62% | 0.00pp | 
| 6 | API automation | 94.22% | 94.22% | 0.00pp | 

---

- `value` has 10,182 unique values in the Claude.ai file vs. only 9,497 in the API file, consistent with the Claude.ai file simply having ~3.3x more rows, not a scale/units mismatch.

---

# Step 5 — Raw Example Impressions

## Important framing note
This dataset has **no raw conversations to read** — Anthropic's Clio pipeline never releases individual conversation text, only aggregated statistics, for privacy reasons. So "raw record" here means one **row of the aggregate CSV** (one geography × facet × variable × cluster_name statistic), not a transcript. The five examples below were pulled from across the downloaded files.

---

### Example 1 — Collaboration pattern, business platform
```
variable=collaboration_pct, cluster_name=directive, value=66.30
```
This is one of two rows that together make up the "automation" share on the business/API platform (automation = directive + feedback loop). The label makes sense — directive is by far the largest single bucket — but it's a reminder that no single row is a finished statistic on its own; you have to sum multiple rows to get a usable number.

### Example 2 — Task-specific automation rate
```
cluster_name="Analyze and categorize news content...::directive", value=92.96 (pct)
```
A specific task is over 92% directive on the business platform — well above the overall average. This shows the automation gap is not uniform across tasks, which is a strong hint that the "does the gap differ by category?" part of the research question has a real, non-trivial answer worth digging into further.

### Example 3 — A missing-value pattern that isn't actually a problem
```
geo_id=AD, variable=usage_count, cluster_name=NaN, value=40
```
Only 40 conversations recorded for this small country in one week — a reminder that country-level rows for small geographies will be noisy. `cluster_name` is null here simply because this particular row is a plain usage count, not a collaboration-pattern breakdown — structural, not a data-quality defect.

### Example 4 — A category whose direction isn't self-evident from the name alone
```
cluster_name=no, variable=human_only_ability_pct, value=5.67%
```
Only 5.67% of tasks fall into this category on the business platform. The label itself is ambiguous without checking the documentation — is "no" answering "can a human do this without AI?" or "is this human-only"? Worth resolving against the data dictionary before using this field, since guessing the wrong direction would flip the interpretation entirely.

### Example 5 — A real-world confound spotted directly in the data
```
platform_and_product = "Claude AI (Free and Pro)"   [earlier snapshot]
platform_and_product = "Claude AI (Free, Pro, and Max)"   [later snapshot]
```
The product name itself changes between snapshots — a new tier was added to the consumer product partway through the data's time range. Not a data-quality issue, but a genuine confound worth flagging: the underlying user population being measured isn't identical across the full time period, which matters for any comparison over time.

---


