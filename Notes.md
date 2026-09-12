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
