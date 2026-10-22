# Antigravity 2.0 Zero-Hallucination T-1 & T+0 Earnings Harness

## Core Operating Rules
1. **NEVER modify or overwrite `Stock_Analysis_v2.html` or `published_reports/TSLA_T1_2026-10-21.html`.** They are our read-only structural and CSS master references.
2. **NEVER invent or alter numbers from `ground_truth/{TICKER}_{DATE}_truth.json` (T-1) or `ground_truth/{TICKER}_{DATE}_post_truth.json` (T+0).** All pre-computed 5-quarter numbers, QoQ/YoY deltas, spot/after-hours prices, beat/miss deltas, and options-implied moves from Stage 1 are immutable ground truth.
3. **Ticker-Specific Directory Isolation**: Any intermediate scripts, inspection utilities, cached SEC exhibits, or ticker-specific helper files (e.g. `inspect_{ticker}.py`, `build_{ticker}_draft.py`, `build_{ticker}_post_draft.py`, `exhibit_99_1.txt`) MUST be created inside a dedicated ticker folder: `{TICKER}/` (e.g., `ISRG/`, `TSLA/`, `META/`). If the directory does not exist, create it before writing the file. Never place symbol-specific files in the repository root.
4. **Model Standard**: All specialized agents in the multi-agent orchestration harness MUST use **Gemini 3.8 Flash High**.

---

## PART I: T-1 Pre-Earnings 4-Stage Execution Workflow

### Stage 1: Deterministic Ground-Truth Anchor
Run `python stage1_fetch_truth.py` for batch scanning across `tickers.txt`.
- The engine automatically filters for tickers with earnings strictly in the T-1 window (upcoming in 1-2 trading days, or released within the last 24 hours).
- If checking an individual symbol: `python stage1_fetch_truth.py {TICKER}`. If the symbol's earnings date is outside the T-1 window, it will be skipped unless forced explicitly with `--force` (e.g. `python stage1_fetch_truth.py {TICKER} --force`).
- Inspect `schedule_verification.confirmation_flag` in `ground_truth/{TICKER}_{DATE}_truth.json`. Confirm the exact investor relations webcast date and BMO/AMC release time via web search.

### Stage 2: Forensic Research & Synthesis Agent
Using `ground_truth/{TICKER}_{DATE}_truth.json` and live web search for 10-Q/10-K footnote disclosures, segment revenue breakdowns, consensus/whisper estimates, and 4-pillar sentiment:
- If creating intermediate inspection or draft builder scripts, place them inside `{TICKER}/` (create the directory if it does not exist).
- Map `{TICKER}`'s actual reporting segments into the sub-rows under `Total Revenue ($M)` in the 5-quarter table (do not leave Tesla segment names for non-Tesla tickers).
- Preserve at least 20 interactive `.tip` hover tooltips with `data-tip="..."` plain-English definitions across the HTML.
- Save `drafts/{TICKER}_{DATE}_draft.json` containing:
  - `"header"`: `{"page_title": "...", "spot_price_num": <float>}`
  - `"historical_table_5q_nums"`: Array of 5 dicts `[{"gross_profit": <float>, "operating_expenses": <float>, "operating_income": <float>}, ...]`
  - `"forensic_callout"`: `{"fcf_bridge_q0_nums": {"ocf": <float>, "capex": <float>, "reported_fcf": <float>, "sbc": <float>, "finance_leases": <float>, "true_fcf": <float>}}`
  - `"trade_matrix"`: `{"bull_target_low_num": <float>, "bear_target_high_num": <float>}`
  - `"rendered_container_html"`: Complete inner HTML of `<div class="container">...</div>` matching `Stock_Analysis_v2.html` 1:1.

### Stage 3: Adversarial Critic & Deterministic Validator Loop
Run `python stage3_validate_draft.py {TICKER} {DATE}`.
- If `"passed": false`, fix every error listed in `errors` inside `drafts/{TICKER}_{DATE}_draft.json` and re-run Stage 3 until `"passed": true`.
- **Mandatory Guardrails Enforced**:
  1. **Content Depth**: `rendered_container_html` length must be $\ge 45,000$ characters.
  2. **8-Card Institutional Structure**: Strictly verifies presence of all 8 core cards:
     - Header banner (`header-banner`) & header strip (`header-strip`)
     - Card 1: KPI strip (`kpi-grid` with 4 metric cards)
     - Card 2: 5-Quarter Financial Table (`table-wrapper`, 5Q columns)
     - Card 3: Free Cash Flow Bridge & Capital Intensity (`forensic-grid`, `waterfall-row`)
     - Card 4: Forensic Breakdown (Segment Analysis & Capital Return)
     - Card 5: Qualitative Audit (`audit-grid` with 4 operational tailwinds/wins & 4 execution headwinds/drags)
     - Card 6: Peer Benchmarking / Relative Valuation Matrix
     - Card 7: 4-Pillar Multi-Source Sentiment Gauge (`sentiment-grid`, `sentiment-meter-bar`)
     - Card 8: Portfolio Manager Decision Matrix / 3-Scenario Trade Playbook (`scenario-grid`, `scenario-bull`, `scenario-base`, `scenario-bear`, `trade-structure`)
  3. **Template Purity**: Explicitly rejects shorthand templates (`grid-2`, `grid-4`, `<section class="section">`).
  4. **Interactive Tooltips**: Enforces $\ge 20$ `.tip` classes and $\ge 20$ `data-tip="..."` definitions.
  5. **Segment Leak Prevention**: Zero foreign-ticker terminology (e.g. Tesla terms in non-TSLA reports).
  6. **Deterministic Accounting Math**: 5Q P&L subtraction (Gross Profit - OpEx = Operating Income) and FCF waterfall bridge balance (tolerance $\le \$2.0\text{M}$).
  7. **Prose Grounding**: Ground-truth spot price and latest OCF must appear explicitly in prose.
  8. **PM Strike Sanity**: Bull case target > Spot Price > Bear case target.

### Stage 4: Read-Only HTML Injection, Multi-Versioning & Publishing
Run `python stage4_render_html.py {TICKER} {DATE}`.
- **Pre-Publish Size Gatekeeper**: Verifies total rendered HTML size is $\ge 75,000$ bytes (aborts publication immediately if truncated).
- **Automatic Multi-Versioning**: Automatically generates versioned files (`{TICKER}_T1_{DATE}_v{N}.html`) and updates the canonical latest file (`{TICKER}_T1_{DATE}.html`). A version banner is embedded at the top of the tearsheet linking directly to prior versions for gap analysis.
- **Automatic Index Updating**: Automatically regenerates `published_reports/index.html` and root `index.html` displaying all reports, live metrics, and version comparison pills.
- Records all version links and public tunnel URLs in `published_ledger.json`. Always populate and display these active public browser links in the final report summary.

---

## PART II: T+0 Post-Earnings 5-Layer Multi-Agent Orchestration Harness (Track A + Track B Standard)

See `AGENTS_POST.md` for full details. Every Post-Earnings (`T+0`) workflow (`python run_post_harness.py {TICKER} {DATE}`) executes:

1. **Layer 0 & Layer 1 (`stage1_post_deterministic.py`)**:
   - Extracts locked `T-1` baseline (`consensus`, `whisper`, `options_implied_move_pct`) and scrapes SEC Form 8-K (Item 2.02) / Exhibit 99.1 (`{TICKER}/exhibit_99_1.txt`) + Yahoo/Google Finance after-hours reaction.
   - Stitches `Q0 (Actual)` onto the 4 prior historical quarters (`Q-4..Q-1`) and writes `ground_truth/{TICKER}_{DATE}_post_truth.json`.
2. **Layer 2 Parallel Specialized Research Bus (`post_agent_bus/`)**:
   - **Agent 2A (`KPI_Discovery_Agent`)**: `post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json` (3-5 company-specific KPIs, segment rows across 5 actual quarters + `Q+1E`, $\ge 18$ `.tip` definitions).
   - **Agent 2B (`Transcript_Forensic_Agent`)**: `post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json` (Matrix A: `Q0 Actual vs Q-1 Guidance`; Matrix B: `Forward Q+1 & FY Guidance Reset vs Street`; Top 3 hardest analyst Q&A exchanges).
   - **Agent 2C (`Social_Pulse_Agent`)**: `post_agent_bus/{TICKER}_{DATE}_agent2c_social.json` (Reddit, X/FinTwit, Threads, Stocktwits, sell-side flash reactions, and 4-Pillar post-print sentiment).
3. **Layer 3 Synthesis & Track A + Track B Mandatory Upgrades (`{TICKER}/build_{ticker}_post_draft.py` -> `drafts/{TICKER}_{DATE}_post_draft.json`)**:
   - **9 Institutional Sections**: Row 1 (Post-Print Executive Banner), Row 1B (Scorecard: Table 1B-1, Table 1B-2, Table 1B-3), Row 2 (Rolling 5Q Table), Row 3 (True FCF Bridge), Row 4 (Wins/Drags & Call Q&A Audit), Row 5 (Post-Print Peer Comps), Row 6 (4-Pillar Post-Print Sentiment), Row 7 (`T+1` PM Trade Matrix anchored to After-Hours Price), Row 8 (SEC Citations & Ledger Footer).
   - **Track A (Rolling 5Q Actuals + `Q+1E` & Zero `T-1` Bleed)**:
     - Row 2 MUST roll forward to `Q-4`, `Q-3`, `Q-2`, `Q-1`, `<th class="col-q0">Q0 (Actual)</th>`, and `<th class="col-est">Q+1E (Guided / Street)</th>`. Never leave `Q0E` in a post-earnings 5Q table.
     - Strip all `T-1 PRE-EARNINGS` badges, `T-1 Pre-Release Consensus` banner labels, and duplicate inner `VERSION COMPARISON BANNER` blocks.
   - **Track B (Interactive UX Polish)**:
     - Include sticky `.post-jump-nav` bar (`#sec-scorecard`, `#sec-5q`, `#sec-fcf`, `#sec-audit`, `#sec-comps`, `#sec-sentiment`, `#sec-trade`), `.t1-vs-t0-audit` 3-card thesis audit banner, `.beat-bar-track` surprise bars in Table 1B-1, and `.credibility-gauge-bar` in Table 1B-2.
4. **Layer 4 Deterministic Validator & Cloner (`stage4_validate_post.py` & `stage4_render_post_html.py`)**:
   - Enforces all 11 guardrails (including Guardrail 10 Track A rolling 5Q & zero bleed-through, and Guardrail 11 Track B UX classes) and renders `published_reports/{TICKER}_T0_POST_{DATE}.html` ($\ge 75,000$ bytes).
5. **Layer 5 Chief HTML Auditor & Publisher (`agent5_chief_auditor.py` & `stage5_publish_github.py`)**:
   - Verifies 100% numeric & structural parity (`"status": "APPROVED"`), updates `index.html` with `All / Pre-Earnings (T-1) / Post-Earnings (T+0)` filter tabs, and pushes to GitHub Pages.
