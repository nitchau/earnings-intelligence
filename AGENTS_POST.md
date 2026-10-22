# Antigravity 2.0 Post-Earnings (T+0) Multi-Agent Orchestration Harness (Track A + Track B Standard)

## 1. Core Operating Constraints & LLM Model Standards
1. **Model Requirement**: All specialized post-earnings agents MUST use **Gemini 3.8 Flash High**.
2. **Master HTML/CSS Reference (Read-Only)**: `published_reports/TSLA_T1_2026-10-21.html` (fallback: `Stock_Analysis_v2.html`). NEVER modify or overwrite the master reference file or alter its `<style>` block.
3. **Deterministic Ground Truth Immutability**: NEVER alter or invent numbers from `ground_truth/{TICKER}_{DATE}_post_truth.json`.
4. **Ticker-Specific Isolation**: Intermediate scripts (`build_{ticker}_post_draft.py`, `inspect_{ticker}.py`, `exhibit_99_1.txt`) MUST reside inside `{TICKER}/`.
5. **Agent Bus Storage**: All Layer 2 specialized outputs MUST be written to `post_agent_bus/`.

---

## 2. 5-Layer Multi-Agent Post-Earnings Workflow

### Layer 0 & Layer 1: Deterministic Financial Data Mesh (`stage1_post_deterministic.py`)
- **Gatekeeper (Layer 0)**: Scans `tickers.txt` and `published_ledger.json` for `T+0` earnings. Extracts locked `T-1` baseline (consensus, whisper, implied move, prior guidance).
- **Agent 1A (`SEC_IR_Agent`)**: Scrapes Form 8-K (Item 2.02) / 10-Q / Exhibit 99.1 via `edgartools` and caches `{TICKER}/exhibit_99_1.txt`. Parses both ticker-specific and universal generic condensed income statement / cash flow tables.
- **Agent 1B (`Market_Portal_Agent`)**: Pulls regular close price, after-hours price, and volume from Yahoo & Google Finance. Preserves locked `T+0` snapshot when re-running on `T+1`.
- **Agent 1C (`Data_Reconciliation_Referee`)**: Cross-validates sources, stitches `Q0 (Actual)` onto the 4 prior historical quarters (`Q-4` to `Q-1`), computes all QoQ/YoY/bps deltas, beat/miss deltas, post-print move, and FCF bridge.
  - Locked output: `ground_truth/{TICKER}_{DATE}_post_truth.json`.

---

### Layer 2: Parallel Specialized Research Agents (Gemini 3.8 Flash High)

#### Agent 2A: Company-Specific Key Metrics & Segment Mapper (`KPI_Discovery_Agent`)
- **Output File**: `post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json`
- **Responsibilities**:
  1. Identifies 3 to 5 company-specific operational KPIs that Wall Street trades for `{TICKER}`.
  2. For each KPI, records: `Street Consensus`, `T-1 Whisper`, `Reported Q0 Actual`, `QoQ / YoY Change`, `Beat/Miss Delta`.
  3. Maps `{TICKER}`'s exact reporting segments for the 5-Quarter Table sub-rows across all 5 actual quarters plus `Q+1E` forward estimate.
  4. Generates $\ge 18$ custom plain-English `.tip` (`data-tip="..."`) hover tooltips.
  5. Strictly forbids foreign ticker segment leaks (zero Tesla terms in non-TSLA reports).

#### Agent 2B: Earnings Call Transcript & Guidance Forensic Agent (`Transcript_Forensic_Agent`)
- **Output File**: `post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json`
- **Responsibilities**:
  1. Pulls full `Q0` Earnings Call Transcript (Prepared remarks + Analyst Q&A) and official IR shareholder deck.
  2. **Matrix A — Prior-Quarter Guidance Accountability (`Q0 Actual` vs `Q-1 Guidance`)**:
     - Guided metric, prior guidance, reported delivery, variance, credibility grade (`BEAT OWN GUIDE`, `MET GUIDE`, `MISSED OWN GUIDE`).
  3. **Matrix B — Forward Guidance Reset (`New Q+1 & FY Guidance` vs `Street Pre-Print Consensus`)**:
     - Metric, pre-print consensus, new guidance, delta, action badge (`RAISED`, `MAINTAINED`, `LOWERED`, `WITHDRAWN`).
  4. **Call Q&A Forensic Highlights**: Top 3 hardest analyst questions, management's exact answers, tone shifts/evasion, margin/demand commentary.

#### Agent 2C: Microblogging, Social & Breaking News Crawler (`Social_Pulse_Agent`)
- **Output File**: `post_agent_bus/{TICKER}_{DATE}_agent2c_social.json`
- **Responsibilities**:
  1. Crawls Reddit (`r/wallstreetbets`, `r/stocks`, ticker subreddits), X (FinTwit), Threads, Stocktwits, Bluesky, Substack, Seeking Alpha, and sell-side flash notes.
  2. Extracts real-time retail vs institutional reaction to the print.
  3. Explains the After-Hours price movement (why the stock is rising/falling).
  4. Computes 4-Pillar Post-Earnings Sentiment scores (Retail Pulse, Sell-Side Flash Reactions, Management Call Tone, Post-Print Options IV Crush & Skew).

---

### Layer 3: 9-Section Post-Earnings HTML Schema & Track A + Track B Standards
Every `T+0` report (`drafts/{TICKER}_{DATE}_post_draft.json`) MUST implement all **9 institutional sections** plus **Track A & Track B upgrades**:

#### Track A Mandatory Architectural Rules:
1. **True Rolling 5-Quarter Actuals + Next-Quarter Forward Estimate (`Q+1E`)**:
   - In Row 2 (`5-Quarter Financial Performance & Dynamic Segment Breakdown`), columns MUST be rolled forward to:
     - `Q-4`, `Q-3`, `Q-2`, `Q-1`, `<th class="col-q0">Q0 (Actual)</th>`, and `<th class="col-est">Q+1E (Guided / Street)</th>`.
   - Every P&L row, segment sub-row, margin row, and cash flow row must populate actual reported figures in `col-q0` and forward `Q+1E` estimates (sourced from Management's new `Q+1` guidance in Table 1B-3) in `col-est`.
   - Never leave `<th class="col-est">Q0E (Consensus)</th>` in a post-earnings table.
2. **Zero `T-1` Bleed-Through & Single Version Banner**:
   - Strip all `T-1 PRE-EARNINGS` badges, `T-1 Pre-Release Consensus` banner labels, and duplicate `VERSION COMPARISON BANNER` blocks inherited from `T-1` HTML templates (`stage4_render_post_html.py` injects the canonical post-print version banner automatically).

#### Track B Mandatory Interactive UX Components:
1. **Sticky Section Jump-Nav Bar (`.post-jump-nav`)**:
   - Placed at the top of `<div class="container">` with quick-jump pills (`#sec-scorecard`, `#sec-5q`, `#sec-fcf`, `#sec-audit`, `#sec-comps`, `#sec-sentiment`, `#sec-trade`).
2. **`T-1` vs. `T+0` Thesis Audit Banner (`.t1-vs-t0-audit`)**:
   - 3-card side-by-side comparison inside Row 1B comparing **Pre-Print T-1 Consensus & Whisper**, **Actual Q0 Print & Forward Guide**, and **T-1 Thesis Verdict (`VALIDATED` / `INVALIDATED`)**.
3. **Visual Beat/Miss Magnitude Bars (`.beat-bar-track` & `.beat-bar-fill`)**:
   - Inline visual progress bars inside Table 1B-1 (`vs. Consensus` column) showing relative surprise magnitude alongside numeric and percentage beats.
4. **Management Guidance Credibility Score Gauge (`.credibility-gauge-bar` & `.credibility-gauge-fill`)**:
   - Quantitative track-record header and progress bar (`0-100%`) above Table 1B-2 grading management's historical guide accuracy.

#### 9-Section Container Layout:
1. **Row 1**: Header & Post-Print Executive KPI Banner (`T+0 POST-EARNINGS FORENSIC TEARSHEET`, Regular Close, After-Hours Price & Move %, Move vs Implied Move, Market Cap / EV, Print Verdict Badge).
2. **Row 1B (`#sec-scorecard`)**: Post-Release Print vs Expectations & Prior Guidance Scorecard (`T-1 vs T+0 Thesis Audit Banner`, `Table 1B-1` with `.beat-bar-track`, `Table 1B-2` with `.credibility-gauge-bar`, `Table 1B-3` Forward Guidance Reset).
3. **Row 2 (`#sec-5q`)**: Rolling 5-Quarter Actuals (`Q-4..Q0 Actual`) + Next-Quarter Forward Estimate (`Q+1E`) Financial & Dynamic Segment Table.
4. **Row 3 (`#sec-fcf`)**: Forensic Quality-of-Earnings & True FCF Bridge (`OCF - CapEx - SBC - Leases = True FCF`).
5. **Row 4 (`#sec-audit`)**: What Management Did Right vs Wrong + Earnings Call Q&A Forensic Audit.
6. **Row 5 (`#sec-comps`)**: Post-Print Peer Group Valuation & Multiples Comps (Re-anchored to After-Hours price).
7. **Row 6 (`#sec-sentiment`)**: 4-Pillar Post-Earnings Sentiment & Microblogging Pulse.
8. **Row 7 (`#sec-trade`)**: `T+1` Hedge Fund PM Trade Execution Matrix (Bull / Base / Bear cases anchored to After-Hours price).
9. **Row 8**: SEC Filing Citations, Verification Ledger & Methodology Footer.

---

### Layer 4: Deterministic Validator & Cloner
1. **`stage4_validate_post.py`**:
   - Guardrails 1-9: Inner HTML $\ge 45,000$ chars, all 9 sections & 3 sub-tables present, P&L math (`Gross Profit - OpEx == Operating Income` within $\$2.0\text{M}$ across all 5 quarters), FCF bridge math within $\$2.0\text{M}$, Beat/Miss delta accuracy, verbatim prices/revenue/OCF, `Bull > AH Price > Bear`, $\ge 18$ `.tip` tooltips, zero foreign ticker leaks.
   - **Guardrail 10 (Track A)**: Rejects `T-1 PRE-EARNINGS` bleed-through, duplicate `VERSION COMPARISON BANNER`, and un-rolled 5Q column headers (requires `<th class="col-q0">...Actual` and `<th class="col-est">...E`).
   - **Guardrail 11 (Track B)**: Enforces presence of `post-jump-nav`, `t1-vs-t0-audit`, `beat-bar-track`, and `credibility-gauge-bar`.
   - Writes `audit_logs/{TICKER}_{DATE}_post_validation.json`.
2. **`stage4_render_post_html.py`**:
   - Clones locked CSS from `published_reports/TSLA_T1_2026-10-21.html` and injects Track B CSS classes cleanly.
   - Validates pre-publish HTML size $\ge 75,000$ bytes.
   - Generates versioned (`{TICKER}_T0_POST_{DATE}_v{N}.html`) and canonical (`{TICKER}_T0_POST_{DATE}.html`) reports.

---

### Layer 5: High-Thinking Chief HTML Cross-Validator & Back-Router
1. **Agent 5 (`Chief_HTML_Auditor` — Gemini 3.8 Flash High Standard)**:
   - Run via `python agent5_chief_auditor.py {TICKER} {DATE}`.
   - Cross-checks rendered HTML against `post_truth.json`, all 3 bus files, and Check 6 (Track A & Track B zero-bleed and rolling `Q0 Actual + Q+1E` table audit).
   - **Targeted Back-Routing Protocol**:
     - `route_to: "LAYER_1_DETERMINISTIC"` -> Re-run SEC 8-K extraction.
     - `route_to: "AGENT_2A_KPIS"` -> Fix missing company KPIs or segment rows.
     - `route_to: "AGENT_2B_TRANSCRIPT"` -> Fix missing call Q&A or guidance tables.
     - `route_to: "AGENT_2C_SOCIAL"` -> Enrich Reddit/X/Threads sentiment.
     - `route_to: "AGENT_4B_FINALIZER"` -> Fix HTML layout, rolling 5Q columns, Track B visual elements, or tooltips.
   - Writes `audit_logs/{TICKER}_{DATE}_agent5_signoff.json` (`"status": "APPROVED"` or `"REJECTED"`).
2. **`stage5_publish_github.py` & `run_post_harness.py`**:
   - `python run_post_harness.py {TICKER} {DATE}` runs Layer 1 -> `{TICKER}/build_{ticker}_post_draft.py` -> Layer 4 Validator & Renderer -> Layer 5 Chief Auditor -> GitHub Pages Publisher in a single deterministic loop.
