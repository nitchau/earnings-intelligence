# Institutional T-1 Pre-Earnings Intelligence Harness

> **Deterministic Zero-Hallucination SEC Form 10-Q / 10-K Forensic Accounting Research, Segment Disclosures & PM Options Playbooks**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Dashboard-3b82f6?style=for-the-badge&logo=github)](https://nitchau.github.io/earnings-intelligence/)

## 🌐 Live Interactive Dashboard
Access the full institutional research portal and all interactive tearsheets:
👉 **[https://nitchau.github.io/earnings-intelligence/](https://nitchau.github.io/earnings-intelligence/)**

---

## 📊 Published Tearsheets & Live Research

| Ticker | Company Name | Upcoming Release Date | Implied Move | Spot Price | Canonical Report | Version History |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **NOK** | Nokia Oyj | Oct 22, 2026 (BMO) | &plusmn;32.2% | $9.08 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/NOK_T1_2026-10-22.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/NOK_T1_2026-10-22_v1.html) |
| **TSLA** | Tesla, Inc. | Oct 21, 2026 (AMC) | &plusmn;6.8% | $218.85 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/TSLA_T1_2026-10-21.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/TSLA_T1_2026-10-21_v1.html) |
| **IBM** | International Business Machines | Oct 21, 2026 (AMC) | &plusmn;6.9% | $236.39 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/IBM_T1_2026-10-21.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/IBM_T1_2026-10-21_v1.html) |
| **LRCX** | Lam Research Corporation | Oct 21, 2026 (AMC) | &plusmn;7.9% | $272.20 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/LRCX_T1_2026-10-21.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/LRCX_T1_2026-10-21_v1.html) |
| **META** | Meta Platforms, Inc. | Oct 21, 2026 (AMC) | &plusmn;6.9% | $705.44 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/META_T1_2026-10-21.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/META_T1_2026-10-21_v1.html) |
| **ISRG** | Intuitive Surgical, Inc. | Oct 20, 2026 (AMC) | &plusmn;5.4% | $482.10 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/ISRG_T1_2026-10-20.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/ISRG_T1_2026-10-20_v1.html) |
| **NVDA** | NVIDIA Corporation | Nov 17, 2026 (AMC) | &plusmn;7.5% | $138.25 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/NVDA_T1_2026-11-17.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/NVDA_T1_2026-11-17_v1.html) |
| **TSM** | Taiwan Semiconductor Mfg | Oct 15, 2026 (BMO) | &plusmn;4.8% | $190.45 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/TSM_T1_2026-10-15.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/TSM_T1_2026-10-15_v1.html) • [`v2`](https://nitchau.github.io/earnings-intelligence/published_reports/TSM_T1_2026-10-15_v2.html) • [`v3`](https://nitchau.github.io/earnings-intelligence/published_reports/TSM_T1_2026-10-15_v3.html) |
| **AEVA** | Aeva Technologies, Inc. | Nov 04, 2026 (AMC) | &plusmn;14.2% | $3.12 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/AEVA_T1_2026-11-04.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/AEVA_T1_2026-11-04_v1.html) |
| **AMD** | Advanced Micro Devices | Nov 03, 2026 (AMC) | &plusmn;7.1% | $156.40 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/AMD_T1_2026-11-03.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/AMD_T1_2026-11-03_v1.html) |
| **ANET** | Arista Networks, Inc. | Nov 03, 2026 (AMC) | &plusmn;6.9% | $388.50 | [Open Tearsheet](https://nitchau.github.io/earnings-intelligence/published_reports/ANET_T1_2026-11-03.html) | [`v1`](https://nitchau.github.io/earnings-intelligence/published_reports/ANET_T1_2026-11-03_v1.html) |

---

## 🏛️ 4-Stage Autonomous Harness Architecture

This repository utilizes the **Antigravity 2.0 Zero-Hallucination Execution Harness**:

1. **Stage 1: Deterministic Ground-Truth Anchor (`stage1_fetch_truth.py`)**  
   Fetches raw SEC EDGAR 10-Q/10-K filings, historical 5-quarter financial tables, and real-time options-implied moves. Data is locked into immutable ground-truth JSON files.
2. **Stage 2: Forensic Research & Synthesis Agent**  
   Performs non-GAAP FCF bridge calculations, true capex reconciliations, segment disclosures, and 4-pillar institutional sentiment analysis with interactive tooltips.
3. **Stage 3: Adversarial Critic & Deterministic Validator (`stage3_validate_draft.py`)**  
   Enforces a zero-tolerance validation loop verifying mathematical equivalence between draft disclosures and Stage 1 immutable anchors.
4. **Stage 4: Read-Only HTML Injection, Multi-Versioning & Publishing (`stage4_render_html.py`)**  
   Injects verified research into locked CSS templates, preserves multi-version iteration history, and updates the public dashboard index.

---

## ⚙️ Running the Pipeline Locally

```powershell
# Run Stage 1 for a specific ticker (e.g. TSLA)
python stage1_fetch_truth.py TSLA --force

# Validate draft report against ground truth
python stage3_validate_draft.py TSLA 2026-10-21

# Publish verified tearsheet and regenerate index
python stage4_render_html.py TSLA 2026-10-21
```

---

## 📁 Repository Structure

```text
├── index.html                   # Root dashboard published to GitHub Pages
├── published_reports/           # Verified HTML tearsheets (canonical & versioned)
│   ├── TSLA_T1_2026-10-21.html
│   ├── TSLA_T1_2026-10-21_v1.html
│   └── ...
├── ground_truth/                # Immutable SEC Edgar extracted figures
├── drafts/                      # Stage 2 forensic synthesis drafts
├── audit_logs/                  # Stage 3 mathematical audit certificates
├── published_ledger.json        # Single source of truth for published versions & links
├── stage1_fetch_truth.py        # Stage 1 fetcher
├── stage3_validate_draft.py     # Stage 3 deterministic validator
├── stage4_render_html.py        # Stage 4 multi-version publisher
└── update_index.py              # Root & subfolder dashboard index generator
```
