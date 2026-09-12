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

