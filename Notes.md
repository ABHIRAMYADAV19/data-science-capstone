**Research question(Q3):** Do consumers and businesses use AI differently on the same tasks? With Claude.ai and enterprise-API columns, you can hold the task fixed and compare interaction styles. Are companies systematically more automation-heavy than individuals? Does the gap differ by occupation category? This bears directly on the "will firms automate faster than workers augment?" debate, and the release-over-release trend in that gap is unstudied.
---
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

