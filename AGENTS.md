# Antigravity 2.0 Zero-Hallucination T-1 & T+0 Earnings Harness

## Core Operating Rules
1. **NEVER modify or overwrite `Stock_Analysis_v2.html` or `published_reports/TSLA_T1_2026-10-21.html`.** They are our read-only structural and CSS master references.
2. **NEVER invent or alter numbers from `ground_truth/{TICKER}_{DATE}_truth.json` (T-1) or `ground_truth/{TICKER}_{DATE}_post_truth.json` (T+0).** All pre-computed 5-quarter numbers, QoQ/YoY deltas, spot/after-hours prices, historical beat/miss track records, analyst price targets, beat/miss deltas, and options-implied moves from Stage 1 are immutable ground truth.
3. **Ticker-Specific Directory Isolation**: Any intermediate scripts, inspection utilities, cached SEC exhibits, or ticker-specific helper files (e.g. `inspect_{ticker}.py`, `build_{ticker}_draft.py`, `build_{ticker}_post_draft.py`, `exhibit_99_1.txt`) MUST be created inside a dedicated ticker folder: `{TICKER}/` (e.g., `ISRG/`, `TSLA/`, `META/`). If the directory does not exist, create it before writing the file. Never place symbol-specific files in the repository root.
4. **Model Standard**: All specialized agents in both the T-1 and T+0 multi-agent orchestration harnesses MUST use **Gemini 3.8 Flash High**.

---

## PART I: T-1 Pre-Earnings 5-Layer Multi-Agent Orchestration Harness (Track A + Track B Standard)

Every Pre-Earnings (`T-1`) workflow (`python run_pre_harness.py {TICKER} {DATE}`) executes:

### Layer 1: Deterministic Ground-Truth Data Mesh (`stage1_fetch_truth.py`)
- Run `python stage1_fetch_truth.py` for batch scanning across `tickers.txt` (strictly upcoming earnings in the `T-1` window: today + next 1–2 trading days; excludes already-released yesterday prints) or `python stage1_fetch_truth.py {TICKER} {DATE}` for an individual symbol.
- Deterministically computes and writes `ground_truth/{TICKER}_{DATE}_truth.json`:
  - `schedule_verification`: Release date, BMO/AMC timing hint, and consensus EPS.
  - `price_validation` & `valuation_and_market`: Cross-validated Yahoo/Google spot price, Market Cap, EV, P/E, EV/EBITDA, short float (locked if re-run on/after release date).
  - `options_positioning`: 1-Wk ATM weekly straddle USD & implied move %, 30D IV, and Put/Call OI ratio.
  - `historical_earnings_track_record`: Last 4 reported quarters' EPS consensus vs actual, surprise %, beat rate %, and actual 1-day post-earnings stock move % vs current options-implied move (`options_vol_regime`).
  - `street_consensus_and_targets`: Wall Street analyst mean, median, high, and low price targets, upside %, analyst count, and recommendation key.
  - `forensic_fcf_bridge_latest`: Pre-computed latest reported quarter (`Q-1`) FCF waterfall (`ocf`, `capex`, `reported_fcf`, `sbc`, `finance_leases`, `true_fcf`).
  - `stitched_5q_financials`: 5 historical quarters with Q4 10-K isolation and pre-computed QoQ/YoY deltas.

### Layer 2: Parallel Specialized Pre-Earnings Research Bus (`pre_agent_bus/`)
- **Agent 2A (`Pre_KPI_Consensus_Agent`)**: `pre_agent_bus/{TICKER}_{DATE}_pre_agent2a_kpis.json`
  - Identifies 3–5 company-specific operational KPIs that Wall Street trades on (with `Q-1 Actual`, `Q-4 YoY Baseline`, `Street Consensus Q0E`, `Buy-Side Whisper Bogey`, `Whisper vs Street Spread`, and visual bar widths).
  - Maps `{TICKER}`'s reporting segments across all 5 historical quarters + `Q0E (Consensus)` and defines $\ge 20$ `.tip` tooltips.
- **Agent 2B (`Pre_Guidance_Debate_Agent`)**: `pre_agent_bus/{TICKER}_{DATE}_pre_agent2b_guidance.json`
  - **Matrix A (Table 1B-2)**: Management Prior Guidance issued in `Q-1` for upcoming `Q0` vs Current Street Consensus, 4Q Historical Beat Rate, and Executive Sandbagging / Credibility Score (`0–100`).
  - **Matrix B (Table 1B-3)**: Forward `Q+1E` & Full-Year Guidance Bogeys Required for Re-Rating (Street Consensus Hurdle vs Buy-Side Bull Bogey vs Bear Breakdown).
  - **Section 4B (`#row-4b-debates`)**: Top 3 Institutional Pre-Print Debates & Analyst Conference Call Focus Questions.
- **Agent 2C (`Pre_Whisper_Sentiment_Agent`)**: `pre_agent_bus/{TICKER}_{DATE}_pre_agent2c_sentiment.json`
  - Verifies live product & architecture releases (preventing stale training-data product naming drift).
  - Triangulates Retail trader positioning (Reddit `r/wallstreetbets`, X/FinTwit, Threads) vs Institutional desk positioning (sell-side preview notes, hedge fund crowding, options skew) and 4-Pillar Pre-Earnings Sentiment scores.

### Layer 3: 9-Section Pre-Earnings Synthesis & Track A + Track B Standards (`{TICKER}/build_{ticker}_draft.py` -> `drafts/{TICKER}_{DATE}_draft.json`)
- **9 Institutional Sections**:
  1. **Header Banner & Strip**: `T-1 PRE-EARNINGS BRIEFING`, Spot Price, Market Cap/EV, Release Date, ATM Straddle Implied Move, Consensus vs Whisper Revenue & EPS, Guidance Corridor.
  2. **Track B Sticky Jump-Nav (`.pre-jump-nav`)**: Quick-jump pills to all 9 sections + one-click switcher to paired `T+0 Post-Earnings` tearsheet (`{TICKER}_T0_POST_{DATE}.html`).
  3. **Row 1 (`#row-1-kpis`)**: 4 Executive KPI Cards (Cash Flow & CapEx, Profitability, Balance Sheet Fortress, Segment Mix & Multiples).
  4. **Row 1B (`#row-1b-scorecard`)**: Pre-Release Expectations, Whisper Spread & Historical Track Record Scorecard:
     - `.t1-setup-audit` 3-card Pre-Print Setup & Implied vs Historical Move Audit Banner.
     - `Table 1B-1`: Headline & Company KPI Consensus vs Buy-Side Whisper Scorecard (with `.beat-bar-track` visual bars).
     - `Table 1B-2`: Management Guidance Credibility & 4Q Historical Beat/Miss Track Record (with `.credibility-gauge-bar` 0–100 score).
     - `Table 1B-3`: Forward `Q+1E` & FY Guidance Bogeys Required for Post-Print Multiple Expansion.
  5. **Row 2 (`#row-2-financials`)**: 5-Quarter Historical Financials (`col-q0` on latest actual quarter) + Upcoming Quarter Consensus (`col-est` on `Q0E`).
  6. **Row 3 (`#row-3-fcf`)**: Forensic Quality-of-Earnings & True FCF Waterfall Bridge (`OCF - CapEx - SBC - Leases = True FCF`).
  7. **Row 4 (`#row-4-segments`) & Section 4B (`#row-4b-debates`)**: 4 Operational Tailwinds vs 4 Execution Headwinds + Top 3 Institutional Pre-Print Debates & Call Focus Questions.
  8. **Row 5 (`#row-5-peers`) & Row 6 (`#row-6-sentiment`)**: Peer Valuation Comps + 4-Pillar Pre-Earnings Sentiment Gauge & Agent 2C Retail/Institutional Positioning Cards.
  9. **Row 7 (`#row-7-pm-matrix`) & Footer**: 3-Scenario Hedge Fund PM Options Playbook (`Bull > Spot > Bear`) + Verbatim Ground-Truth Verification Ledger.

### Layer 4: Deterministic 11-Guardrail Validator & HTML Cloner (`stage3_validate_draft.py` & `stage4_render_html.py`)
- `python stage3_validate_draft.py {TICKER} {DATE}` enforces all **11 Guardrails** (`pre_agent_bus/` existence, $\ge 45,000$ chars, all 9 sections + `Table 1B-1..3` + `#row-4b-debates`, template purity, $\ge 20$ `.tip` tooltips, zero foreign ticker leaks, 5Q P&L math, FCF bridge math, verbatim Spot/OCF grounding, `Bull > Spot > Bear`, Track A headers & zero duplicate banners, Track B `.pre-jump-nav`, `.t1-setup-audit`, `.beat-bar-track`, `.credibility-gauge-bar`).
- `python stage4_render_html.py {TICKER} {DATE}` enforces the **75,000-byte pre-publish gatekeeper**, generates multi-versioned tearsheets (`{TICKER}_T1_{DATE}_v{N}.html` and canonical `{TICKER}_T1_{DATE}.html`), and updates `index.html`.

### Layer 5: Chief Pre-Earnings HTML Auditor & Publisher (`agent5_pre_chief_auditor.py` & `run_pre_harness.py`)
- `python agent5_pre_chief_auditor.py {TICKER} {DATE}` cross-validates the rendered HTML against `truth.json` and all 3 `pre_agent_bus/` files, with targeted back-routing (`LAYER_1_DETERMINISTIC`, `AGENT_2A_KPIS`, `AGENT_2B_GUIDANCE`, `AGENT_2C_SENTIMENT`, `AGENT_4B_FINALIZER`), writing `audit_logs/{TICKER}_{DATE}_pre_agent5_signoff.json` (`"status": "APPROVED"`).

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
