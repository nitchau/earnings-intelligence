# Antigravity 2.0 Zero-Hallucination T-1 Earnings Harness

## Core Operating Rules
1. **NEVER modify or overwrite `Stock_Analysis_v2.html`.** It is our read-only structural and CSS master reference.
2. **NEVER invent or alter numbers from `ground_truth/{TICKER}_{DATE}_truth.json`.** All pre-computed 5-quarter numbers, QoQ/YoY deltas, spot prices, and options-implied moves from Stage 1 are immutable ground truth.
3. **Ticker-Specific Directory Isolation**: Any intermediate scripts, inspection utilities, or ticker-specific helper files (e.g. `inspect_{ticker}.py`, `build_{ticker}_draft.py`, `verify_{ticker}.py`) MUST be created inside a dedicated ticker folder: `{TICKER}/` (e.g., `ISRG/`, `TSLA/`). If the directory does not exist, create it before writing the file. Never place symbol-specific files in the repository root.

## 4-Stage Execution Workflow

### Stage 1: Deterministic Ground-Truth Anchor
Run `python stage1_fetch_truth.py` for batch scanning across `tickers.txt`.
- The engine automatically filters for tickers with earnings strictly in the T-1 window (upcoming in 1-2 trading days, or released within the last 24 hours).
- If checking an individual symbol: `python stage1_fetch_truth.py {TICKER}`. If the symbol's earnings date is outside the T-1 window, it will be skipped unless forced explicitly with `--force` (e.g. `python stage1_fetch_truth.py {TICKER} --force`).
- Inspect `schedule_verification.confirmation_flag` in `ground_truth/{TICKER}_{DATE}_truth.json`. Confirm the exact investor relations webcast date and BMO/AMC release time via web search.

### Stage 2: Forensic Research & Synthesis Agent
Using `ground_truth/{TICKER}_{DATE}_truth.json` and live web search for 10-Q/10-K footnote disclosures, segment revenue breakdowns, consensus/whisper estimates, and 4-pillar sentiment:
- If creating intermediate inspection or draft builder scripts, place them inside `{TICKER}/` (create the directory if it does not exist).
- Map `{TICKER}`'s actual reporting segments into the sub-rows under `Total Revenue ($M)` in the 5-quarter table (do not leave Tesla segment names for non-Tesla tickers).
- Preserve at least 15 interactive `.tip` hover tooltips with `data-tip="..."` plain-English definitions across the HTML.
- Save `drafts/{TICKER}_{DATE}_draft.json` containing:
  - `"header"`: `{"page_title": "...", "spot_price_num": <float>}`
  - `"historical_table_5q_nums"`: Array of 5 dicts `[{"gross_profit": <float>, "operating_expenses": <float>, "operating_income": <float>}, ...]`
  - `"forensic_callout"`: `{"fcf_bridge_q0_nums": {"ocf": <float>, "capex": <float>, "reported_fcf": <float>, "sbc": <float>, "finance_leases": <float>, "true_fcf": <float>}}`
  - `"trade_matrix"`: `{"bull_target_low_num": <float>, "bear_target_high_num": <float>}`
  - `"rendered_container_html"`: Complete inner HTML of `<div class="container">...</div>` matching `Stock_Analysis_v2.html` 1:1.

### Stage 3: Adversarial Critic & Deterministic Validator Loop
Run `python stage3_validate_draft.py {TICKER} {DATE}`.
- If `"passed": false`, fix every error listed in `errors` inside `drafts/{TICKER}_{DATE}_draft.json` and re-run Stage 3 until `"passed": true`.

### Stage 4: Read-Only HTML Injection, Multi-Versioning & Publishing
Run `python stage4_render_html.py {TICKER} {DATE}`.
- **Automatic Multi-Versioning**: Automatically generates versioned files (`{TICKER}_T1_{DATE}_v{N}.html`) and updates the canonical latest file (`{TICKER}_T1_{DATE}.html`). A version banner is embedded at the top of the tearsheet linking directly to prior versions for gap analysis.
- **Automatic Index Updating**: Automatically regenerates `published_reports/index.html` and root `index.html` displaying all reports, live metrics, and version comparison pills.
- Records all version links and public tunnel URLs in `published_ledger.json`. Always populate and display these active public browser links in the final report summary.
