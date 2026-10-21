# Antigravity 2.0 Post-Earnings (T+0) Multi-Agent Orchestration Harness

## 1. Core Operating Constraints & LLM Model Standards
1. **Model Requirement**: All specialized post-earnings agents MUST use **Gemini 3.8 Flash High**.
2. **Master HTML/CSS Reference (Read-Only)**: `published_reports/TSLA_T1_2026-10-21.html` (fallback: `Stock_Analysis_v2.html`). NEVER modify or overwrite the master reference file or alter its `<style>` block.
3. **Deterministic Ground Truth Immutability**: NEVER alter or invent numbers from `ground_truth/{TICKER}_{DATE}_post_truth.json`.
4. **Ticker-Specific Isolation**: Intermediate scripts inside `{TICKER}/`.
5. **Agent Bus Storage**: All Layer 2 specialized outputs MUST be written to `post_agent_bus/`.

---

## 2. 5-Layer Multi-Agent Post-Earnings Workflow

### Layer 0 & Layer 1: Deterministic Financial Data Mesh (`stage1_post_deterministic.py`)
- **Gatekeeper (Layer 0)**: Scans `tickers.txt` and `published_ledger.json` for T+0 earnings. Extracts locked T-1 baseline (consensus, whisper, implied move, prior guidance).
- **Agent 1A (SEC_IR_Agent)**: Scrapes Form 8-K (Item 2.02) / 10-Q / Exhibit 99.1 via `edgartools` and SEC XBRL API.
- **Agent 1B (Market_Portal_Agent)**: Pulls closing price, after-hours price/volume from Yahoo & Google Finance.
- **Agent 1C (Data_Reconciliation_Referee)**: Cross-validates sources, rolls forward 5Q table (Q0 Actual is col 5), computes all QoQ/YoY/bps deltas, beat/miss deltas, post-print move, and FCF bridge.
  - Locked output: `ground_truth/{TICKER}_{DATE}_post_truth.json`.

---

### Layer 2: Parallel Specialized Research Agents (Gemini 3.8 Flash High)

#### Agent 2A: Company-Specific Key Metrics & Segment Mapper (`KPI_Discovery_Agent`)
- **Output File**: `post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json`
- **Responsibilities**:
  1. Identifies 3 to 5 company-specific operational KPIs that Wall Street trades for `{TICKER}`.
  2. For each KPI, records: `Street Consensus`, `T-1 Whisper`, `Reported Q0 Actual`, `QoQ / YoY Change`, `Beat/Miss Delta`.
  3. Maps `{TICKER}`'s exact reporting segments for the 5-Quarter Table sub-rows.
  4. Generates >= 18 custom plain-English `.tip` (`data-tip="..."`) hover tooltips.
  5. Strictly forbids foreign ticker segment leaks (e.g. zero Tesla terms in non-TSLA reports).

#### Agent 2B: Earnings Call Transcript & Guidance Forensic Agent (`Transcript_Forensic_Agent`)
- **Output File**: `post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json`
- **Responsibilities**:
  1. Pulls full Q0 Earnings Call Transcript (Prepared remarks + Analyst Q&A) and official IR shareholder deck.
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
  3. Explains the After-Hours price movement (why stock is rising/falling).
  4. Computes 4-Pillar Post-Earnings Sentiment scores (Retail Pulse, Sell-Side Flash Reactions, Management Call Tone, Post-Print Options IV Crush & Skew).

---

### Layer 3: 9-Section Post-Earnings HTML Schema
Update `<div class="container">` layout from 8 to **9 sections** by inserting **Row 1B** immediately after the top KPI banner:
1. **Row 1: Header & Post-Print Executive KPI Banner**: Ticker, Company Name, `T+0 POST-EARNINGS FORENSIC TEARSHEET` badge, Regular Close, After-Hours Price & Move %, Move vs Implied Move, Market Cap / EV, Print Verdict Badge.
2. **Row 1B (NEW MANDATORY SECTION): Post-Release Print vs Expectations & Prior Guidance Scorecard**:
   - **Table 1B-1**: Headline & Company-Specific KPI Beat / Miss Scorecard.
   - **Table 1B-2**: Management Execution Accountability (Q0 Actual vs Q-1 Guidance).
   - **Table 1B-3**: Forward Guidance Reset (New Guidance vs Street Expectations).
3. **Row 2: 5-Quarter Historical Financial & Dynamic Segment Table** (Shifted with Q0 Actual as latest column).
4. **Row 3: Forensic Quality-of-Earnings & True FCF Bridge** (`OCF - CapEx - SBC - Leases = True FCF`).
5. **Row 4: What Management Did Right vs Wrong + Earnings Call Q&A Audit**.
6. **Row 5: Post-Print Peer Group Valuation & Multiples Comps** (Re-anchored to After-Hours price).
7. **Row 6: 4-Pillar Post-Earnings Sentiment & Microblogging Pulse**.
8. **Row 7: T+1 Hedge Fund PM Trade Execution Matrix** (Bull / Base / Bear cases anchored to After-Hours price).
9. **Row 8: SEC Filing Citations, Verification Ledger & Methodology Footer**.

---

### Layer 4: Deterministic Validator & Cloner
1. **`stage4_validate_post.py`**:
   - Asserts inner HTML length >= 45,000 chars.
   - Asserts all 9 sections and 3 sub-tables present.
   - Asserts P&L math (`Gross Profit - OpEx == Operating Income`) within $2.0M.
   - Asserts FCF bridge (`OCF - CapEx == Rep FCF` and `Rep FCF - SBC - Leases == True FCF`) within $2.0M.
   - Asserts Beat/Miss math in Table 1B-1 (`Actual - Consensus == Delta`).
   - Asserts After-Hours price, Close price, Revenue, OCF appear verbatim.
   - Asserts Bull Target > After-Hours Price > Bear Target.
   - Asserts >= 18 interactive `.tip` classes with `data-tip="..."`.
   - Asserts zero foreign ticker leaks and zero placeholder tokens (`NaN`, `None`, `TODO`).
   - Writes `audit_logs/{TICKER}_{DATE}_post_validation.json`.
2. **`stage4_render_post_html.py`**:
   - Clones locked CSS from `published_reports/TSLA_T1_2026-10-21.html`.
   - Validates pre-publish HTML size >= 75,000 bytes.
   - Generates versioned and canonical `published_reports/{TICKER}_T0_POST_{DATE}.html`.

---

### Layer 5: High-Thinking Chief HTML Cross-Validator & Back-Router
1. **Agent 5 (`Chief_HTML_Auditor` — Gemini 3.8 Flash High Standard)**:
   - Run via `python agent5_chief_auditor.py {TICKER} {DATE}`.
   - Cross-checks rendered HTML against `post_truth.json` and all 3 bus files.
   - **Targeted Back-Routing Protocol**:
     - `route_to: "LAYER_1_DETERMINISTIC"` -> Re-run SEC 8-K extraction.
     - `route_to: "AGENT_2A_KPIS"` -> Fix missing company KPIs or segment rows.
     - `route_to: "AGENT_2B_TRANSCRIPT"` -> Fix missing call Q&A or guidance tables.
     - `route_to: "AGENT_2C_SOCIAL"` -> Enrich Reddit/X/Threads sentiment.
     - `route_to: "AGENT_4B_FINALIZER"` -> Fix HTML layout, tooltips, or formatting.
   - Writes `audit_logs/{TICKER}_{DATE}_agent5_signoff.json` (`"status": "APPROVED"` or `"REJECTED"`).
2. **`stage5_publish_github.py`**:
   - Verifies both validation and agent 5 signoff pass.
   - Updates `published_ledger.json` and `index.html`.
   - Commits and pushes to GitHub (`origin main`).
   - Publishes to `https://nitchau.github.io/earnings-intelligence/`.
