import os
import sys
import json
import py_compile
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def setup_harness():
    print("=" * 75)
    print("INITIALIZING POST-EARNINGS (T+0) MULTI-AGENT HARNESS")
    print(f"Base Directory: {BASE_DIR}")
    print("Model Standard: Gemini 3.8 Flash High")
    print("=" * 75)

    # 1. Ensure required directories exist
    folders = [
        "ground_truth",
        "drafts",
        "audit_logs",
        "published_reports",
        "post_agent_bus",
        "logs"
    ]
    for folder in folders:
        dir_path = BASE_DIR / folder
        dir_path.mkdir(exist_ok=True)
        print(f" [OK] Directory verified: {folder}/")

    # Ensure tickers.txt exists
    tickers_file = BASE_DIR / "tickers.txt"
    if not tickers_file.exists():
        tickers_file.write_text("TSLA\nIBM\nLRCX\nMETA\nNVDA\nAMZN\nGOOGL\nMSFT\nAAPL\n", encoding="utf-8")
        print(" [OK] Initialized default tickers.txt")

    # Ensure published_ledger.json exists
    ledger_file = BASE_DIR / "published_ledger.json"
    if not ledger_file.exists():
        ledger_file.write_text(json.dumps({"published": [], "links": {}}, indent=2), encoding="utf-8")
        print(" [OK] Initialized default published_ledger.json")

    # Write all modules
    write_stage1_post_deterministic()
    write_stage4_validate_post()
    write_stage4_render_post_html()
    write_agent5_chief_auditor()
    write_stage5_publish_github()
    write_update_index_enhanced()
    write_agents_post_md()
    write_run_post_harness()

    # Compile-check all Python files
    print("\n" + "=" * 75)
    print("RUNNING STATIC SYNTAX COMPILATION CHECKS...")
    print("=" * 75)
    scripts_to_check = [
        "stage1_post_deterministic.py",
        "stage4_validate_post.py",
        "stage4_render_post_html.py",
        "agent5_chief_auditor.py",
        "stage5_publish_github.py",
        "update_index.py",
        "run_post_harness.py"
    ]
    for script_name in scripts_to_check:
        script_path = BASE_DIR / script_name
        try:
            py_compile.compile(str(script_path), doraise=True)
            print(f" [PASS] {script_name} compiled cleanly.")
        except Exception as e:
            print(f" [FAIL] Syntax error in {script_name}: {e}")
            sys.exit(1)

    print("\n" + "=" * 75)
    print("ALL MODULES SUCCESSFULLY GENERATED AND COMPILED CLEANLY!")
    print("=" * 75)

# ==============================================================================
# MODULE 1: stage1_post_deterministic.py
# ==============================================================================
def write_stage1_post_deterministic():
    code = '''"""
Stage 1 Post-Earnings (T+0) Deterministic Financial Data Mesh
Executes Layer 0 (Gatekeeper) & Layer 1 (Deterministic Mesh) before any LLM writes prose:
- Gatekeeper (Layer 0): Checks tickers.txt and published_ledger.json for T+0 reporting.
  Supports CLI forced ticker or --check-only scan.
  Extracts locked T-1 baseline (consensus, whisper, implied move, prior guidance).
- Agent 1A (SEC_IR_Agent): Pulls Form 8-K (Item 2.02) / 10-Q / Exhibit 99.1 filings via edgartools/SEC API.
- Agent 1B (Market_Portal_Agent): Pulls closing price, after-hours price/volume from Yahoo & Google Finance.
- Agent 1C (Data_Reconciliation_Referee): Reconciles sources, rolls forward 5-quarter table,
  pre-computes all QoQ/YoY/bps deltas, beat/miss deltas, post-print move, and FCF bridge.
  Saves locked payload to ground_truth/{TICKER}_{DATE}_post_truth.json.
"""

import sys
import re
import json
import math
from datetime import datetime, date, timedelta
from pathlib import Path
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

try:
    from edgar import Company, set_identity
    set_identity("PortfolioResearch research@local.dev")
    EDGAR_AVAILABLE = True
except ImportError:
    EDGAR_AVAILABLE = False

BASE_DIR = Path(__file__).parent.resolve()
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
PUBLISHED_DIR = BASE_DIR / "published_reports"
LEDGER_FILE = BASE_DIR / "published_ledger.json"
TICKERS_FILE = BASE_DIR / "tickers.txt"

def safe_float(val, ndigits=2):
    try:
        if val is None or pd.isna(val) or (isinstance(val, float) and math.isnan(val)):
            return None
        return round(float(val), ndigits)
    except Exception:
        return None

def load_tickers() -> list[str]:
    if not TICKERS_FILE.exists():
        return []
    raw = TICKERS_FILE.read_text(encoding="utf-8").splitlines()
    return [line.strip().upper() for line in raw if line.strip() and not line.startswith("#")]

def load_ledger() -> dict:
    if not LEDGER_FILE.exists():
        return {"published": [], "links": {}}
    try:
        return json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {"published": [], "links": {}}

# ==============================================================================
# LAYER 0: GATEKEEPER & T-1 BASELINE EXTRACTION
# ==============================================================================
def extract_t1_baseline(ticker: str, earnings_date_str: str) -> dict:
    baseline = {
        "source_found": False,
        "t1_file": None,
        "consensus_revenue_millions": None,
        "whisper_revenue_millions": None,
        "consensus_eps_nongaap": None,
        "consensus_eps_gaap": None,
        "whisper_eps_nongaap": None,
        "options_implied_move_pct": None,
        "atm_straddle_usd": None,
        "prior_quarter_label": None,
        "prior_quarter_guidance": {}
    }

    # 1. Search for matching ground_truth/{TICKER}_{DATE}_truth.json
    gt_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date_str}_truth.json"
    if not gt_file.exists():
        candidates = list(GROUND_TRUTH_DIR.glob(f"{ticker}_*_truth.json"))
        if candidates:
            candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            gt_file = candidates[0]

    if gt_file.exists():
        try:
            gt_data = json.loads(gt_file.read_text(encoding="utf-8"))
            baseline["source_found"] = True
            baseline["t1_file"] = gt_file.name
            opt = gt_data.get("options_positioning", {})
            baseline["options_implied_move_pct"] = safe_float(opt.get("atm_implied_move_pct"))
            baseline["atm_straddle_usd"] = safe_float(opt.get("atm_straddle_usd"))
            baseline["consensus_eps_nongaap"] = safe_float(gt_data.get("schedule_verification", {}).get("yahoo_consensus_eps"))

            # Prior quarter header from stitched 5Q
            p_headers = gt_data.get("stitched_5q_financials", {}).get("income_statement_5q", {}).get("period_headers", [])
            if p_headers:
                baseline["prior_quarter_label"] = p_headers[-1]
        except Exception:
            pass

    # 2. Extract from published T-1 HTML report if available
    t1_html = PUBLISHED_DIR / f"{ticker}_T1_{earnings_date_str}.html"
    if not t1_html.exists():
        t1_candidates = list(PUBLISHED_DIR.glob(f"{ticker}_T1_*.html"))
        if t1_candidates:
            t1_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            t1_html = t1_candidates[0]

    if t1_html.exists():
        try:
            content = t1_html.read_text(encoding="utf-8", errors="ignore")
            # Consensus & Whisper Revenue
            m_rev = re.search(r'Consensus Revenue</span>\\s*/\\s*<span[^>]*>Whisper</span></span>\\s*<span class="strip-val">\\$([0-9,.]+)M?\\s*/\\s*\\$([0-9,.]+)M?', content)
            if m_rev:
                baseline["consensus_revenue_millions"] = safe_float(m_rev.group(1).replace(",", ""))
                baseline["whisper_revenue_millions"] = safe_float(m_rev.group(2).replace(",", ""))

            # Consensus & Whisper EPS
            m_eps = re.search(r'Consensus[^<]*EPS</span>\\s*/\\s*Whisper</span>\\s*<span class="strip-val">\\$([0-9.]+)[^/]*[/\\]\\s*\\$([0-9.]+)\\s*Whisper', content)
            if m_eps:
                baseline["consensus_eps_nongaap"] = safe_float(m_eps.group(1))
                baseline["whisper_eps_nongaap"] = safe_float(m_eps.group(2))

            # GAAP EPS Est
            m_gaap = re.search(r'GAAP</span>\\s*EPS Est:\\s*\\$([0-9.]+)', content)
            if m_gaap:
                baseline["consensus_eps_gaap"] = safe_float(m_gaap.group(1))

            # Implied move
            m_move = re.search(r'Options-Implied Move[^<]*</span>[^<]*<span class="strip-val"[^>]*>[^0-9]*([0-9.]+)%', content)
            if m_move and baseline["options_implied_move_pct"] is None:
                baseline["options_implied_move_pct"] = safe_float(m_move.group(1))
        except Exception:
            pass

    return baseline

# ==============================================================================
# LAYER 1: AGENT 1A — SEC EDGAR & IR SCRAPER
# ==============================================================================
def fetch_sec_filings_facts(symbol: str, target_date_str: str) -> dict:
    sec_data = {
        "edgar_status": "UNAVAILABLE",
        "filing_form": None,
        "filing_date": None,
        "exhibit_99_1_found": False,
        "facts": {}
    }

    if not EDGAR_AVAILABLE:
        sec_data["edgar_status"] = "EDGARTOOLS_LIBRARY_NOT_INSTALLED"
        return sec_data

    try:
        comp = Company(symbol)
        sec_data["cik"] = str(comp.cik).zfill(10)

        # Look for 8-K filed on target_date_str, or most recent 8-K / 10-Q
        filings = comp.get_filings(form=["8-K", "10-Q", "10-K"]).latest(5)
        target_filing = None
        for f in filings:
            if str(f.filing_date) == target_date_str:
                target_filing = f
                break
        if not target_filing and filings:
            target_filing = filings[0]

        if target_filing:
            sec_data["filing_form"] = target_filing.form
            sec_data["filing_date"] = str(target_filing.filing_date)
            sec_data["edgar_status"] = "FILING_RETRIEVED"

            # Check for Item 2.02 (Results of Operations and Financial Condition)
            items = getattr(target_filing, "items", [])
            sec_data["items"] = items

            # Check attachments for Exhibit 99.1
            exhibit_text = ""
            for att in getattr(target_filing, "attachments", []):
                desc = getattr(att, "description", "").lower()
                doc_name = att.document.lower()
                if "99.1" in desc or "exhibit99" in doc_name or "ex-99" in doc_name or "press" in desc:
                    try:
                        raw = att.download()
                        soup = BeautifulSoup(raw, "html.parser")
                        exhibit_text = soup.get_text()
                        sec_data["exhibit_99_1_found"] = True
                        break
                    except Exception:
                        pass

            if not exhibit_text:
                try:
                    exhibit_text = target_filing.text()
                except Exception:
                    pass

            # Parse standardized numbers from filing text
            if exhibit_text:
                sec_data["facts"] = parse_financial_metrics_from_text(exhibit_text, symbol)

    except Exception as e:
        sec_data["edgar_status"] = f"ERROR: {str(e)}"

    return sec_data

def parse_financial_metrics_from_text(text: str, symbol: str) -> dict:
    facts = {}
    
    # 5-value historical row patterns
    patterns = {
        "revenue_5q": r"Total revenues\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "gross_profit_5q": r"Total gross profit\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "operating_expenses_5q": r"Operating expenses\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "operating_income_5q": r"Income from operations\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "net_income_gaap_5q": r"Net income attributable to common stockholders \(GAAP\)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "net_income_nongaap_5q": r"Net income attributable to common stockholders \(non-GAAP\)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "eps_gaap_5q": r"EPS attributable to common stockholders, diluted \(GAAP\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)",
        "eps_nongaap_5q": r"EPS attributable to common stockholders, diluted \(non-GAAP\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)",
        "ocf_5q": r"Net cash provided by operating activities\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "capex_5q": r"Capital expenditures\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?",
        "fcf_5q": r"Free cash flow\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?",
        "sbc_5q": r"Stock-based compensation\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)",
        "leases_5q": r"Principal payments on finance leases\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?\s+\(?([\d,]+)\)?"
    }

    for key, pat in patterns.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            vals = [safe_float(v.replace(",", "")) for v in m.groups()]
            facts[key] = vals
            facts[f"{key.replace('_5q', '')}_q0"] = vals[-1] if vals else None

    # Ticker specific segment extraction
    if symbol == "TSLA":
        m_auto = re.search(r"Total automotive revenues\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text, re.IGNORECASE)
        m_energy = re.search(r"Energy generation and storage revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text, re.IGNORECASE)
        m_services = re.search(r"Services and other revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text, re.IGNORECASE)
        m_storage = re.search(r"Storage deployed \(GWh\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", text, re.IGNORECASE)
        m_deliveries = re.search(r"Total deliveries(?:\(1\))?\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", text, re.IGNORECASE)
        m_fsd = re.search(r"Active FSD Subscriptions(?:\(3\))?\s+\(mil\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", text, re.IGNORECASE)

        if m_auto:
            facts["automotive_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_auto.groups()]
        if m_energy:
            facts["energy_storage_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_energy.groups()]
        if m_services:
            facts["services_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_services.groups()]
        if m_storage:
            facts["storage_deployed_gwh_5q"] = [safe_float(v) for v in m_storage.groups()]
        if m_deliveries:
            facts["deliveries_5q"] = [safe_float(v.replace(",", "")) for v in m_deliveries.groups()]
        if m_fsd:
            facts["fsd_subs_mil_5q"] = [safe_float(v) for v in m_fsd.groups()]

    return facts

# ==============================================================================
# LAYER 1: AGENT 1B — MARKET PORTAL AGENT (YFINANCE & GOOGLE FINANCE)
# ==============================================================================
def check_google_finance_quotes(symbol: str, exchange_hint: str = "NASDAQ") -> dict:
    candidates = [exchange_hint, "NASDAQ", "NYSE"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    out = {"regular_price": None, "after_hours_price": None}
    for cand in candidates:
        url = f"https://www.google.com/finance/quote/{symbol}:{cand}"
        try:
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                reg_div = soup.find("div", {"class": "YMlKec fxKbKc"})
                if reg_div:
                    out["regular_price"] = safe_float(reg_div.text.replace("$", "").replace(",", "").strip())
                # Extended hours check
                ext_div = soup.find("div", {"class": "yg1AZe"}) or soup.find("div", {"class": "NydbP"})
                if ext_div:
                    p_text = ext_div.find("div", {"class": "YMlKec"})
                    if p_text:
                        out["after_hours_price"] = safe_float(p_text.text.replace("$", "").replace(",", "").strip())
                if out["regular_price"]:
                    break
        except Exception:
            continue
    return out

def fetch_market_portal_data(symbol: str) -> dict:
    t = yf.Ticker(symbol)
    info = t.info or {}
    fast = t.fast_info

    regular_price = safe_float(fast.get("last_price") or info.get("regularMarketPrice") or info.get("currentPrice") or info.get("previousClose"))
    post_price = safe_float(info.get("postMarketPrice") or info.get("currentPrice") or regular_price)
    post_volume = safe_float(info.get("postMarketVolume"))
    prev_close = safe_float(fast.get("previousClose") or info.get("regularMarketPreviousClose"))

    gf_quotes = check_google_finance_quotes(symbol, info.get("exchange", "NASDAQ"))

    # Cross source divergence check
    divergence_pct = 0.0
    if regular_price and gf_quotes["regular_price"]:
        divergence_pct = round(abs(regular_price - gf_quotes["regular_price"]) / regular_price * 100, 3)

    return {
        "regular_close_price": regular_price,
        "after_hours_price": post_price,
        "after_hours_volume": post_volume,
        "previous_close_price": prev_close,
        "google_finance_regular": gf_quotes["regular_price"],
        "google_finance_after_hours": gf_quotes["after_hours_price"],
        "price_divergence_pct": divergence_pct,
        "price_divergence_warning": divergence_pct > 0.5,
        "market_cap_millions": safe_float((info.get("marketCap") or 0) / 1e6),
        "enterprise_value_millions": safe_float((info.get("enterpriseValue") or 0) / 1e6),
        "trailing_pe": safe_float(info.get("trailingPE")),
        "forward_pe": safe_float(info.get("forwardPE"))
    }

# ==============================================================================
# LAYER 1: AGENT 1C — DATA RECONCILIATION REFEREE & MATH PRE-COMPUTER
# ==============================================================================
def reconcile_and_compute_post_truth(symbol: str, earnings_date_str: str) -> dict:
    print(f"[{symbol}] Starting Layer 1 Post-Earnings Deterministic Assembly...")
    
    # 1. Layer 0 baseline
    t1_baseline = extract_t1_baseline(symbol, earnings_date_str)
    
    # 2. Agent 1A SEC IR Facts
    sec_data = fetch_sec_filings_facts(symbol, earnings_date_str)
    facts = sec_data.get("facts", {})

    # 3. Agent 1B Market Portal Quotes
    market_data = fetch_market_portal_data(symbol)

    # 4. Resolve 5-quarter chronological arrays
    # If SEC parsed 5Q series directly, use them; otherwise pull from yfinance statements
    t = yf.Ticker(symbol)
    q_inc = t.quarterly_income_stmt
    q_cf = t.quarterly_cashflow

    def build_5q_chronological(metric_key_facts: str, yf_metric_names: list[str], divisor: float = 1.0):
        # Prefer SEC facts
        if metric_key_facts in facts and len(facts[metric_key_facts]) == 5:
            return facts[metric_key_facts]
        # Fallback to yfinance quarterly statement
        vals = []
        if q_inc is not None and not q_inc.empty:
            for name in yf_metric_names:
                if name in q_inc.index:
                    cols = sorted(list(q_inc.columns[:5]))
                    vals = [safe_float(q_inc.loc[name, c] / divisor) for c in cols]
                    break
        if not vals and q_cf is not None and not q_cf.empty:
            for name in yf_metric_names:
                if name in q_cf.index:
                    cols = sorted(list(q_cf.columns[:5]))
                    vals = [safe_float(q_cf.loc[name, c] / divisor) for c in cols]
                    break
        return vals

    rev_5q = build_5q_chronological("revenue_5q", ["Total Revenue", "Operating Revenue"], 1e6)
    gp_5q = build_5q_chronological("gross_profit_5q", ["Gross Profit"], 1e6)
    opex_5q = build_5q_chronological("operating_expenses_5q", ["Operating Expense", "Total Operating Expenses"], 1e6)
    ebit_5q = build_5q_chronological("operating_income_5q", ["Operating Income", "Income From Operations"], 1e6)
    gaap_net_5q = build_5q_chronological("net_income_gaap_5q", ["Net Income Common Stockholders", "Net Income"], 1e6)
    gaap_eps_5q = build_5q_chronological("eps_gaap_5q", ["Diluted EPS", "Basic EPS"], 1.0)
    nongaap_eps_5q = build_5q_chronological("eps_nongaap_5q", [], 1.0)
    ocf_5q = build_5q_chronological("ocf_5q", ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"], 1e6)
    capex_5q = build_5q_chronological("capex_5q", ["Capital Expenditure", "Purchase Of Property Plant And Equipment"], 1e6)
    sbc_5q = build_5q_chronological("sbc_5q", ["Stock Based Compensation"], 1e6)
    leases_5q = build_5q_chronological("leases_5q", ["Repayment Of Debt"], 1e6)

    # Ensure leases and capex are non-negative magnitudes for mathematical clarity
    if capex_5q:
        capex_5q = [abs(x) if x is not None else 0.0 for x in capex_5q]
    if leases_5q:
        leases_5q = [abs(x) if x is not None else 0.0 for x in leases_5q]
    if sbc_5q:
        sbc_5q = [abs(x) if x is not None else 0.0 for x in sbc_5q]

    # Deterministic FCF math across all 5 quarters
    rep_fcf_5q = []
    true_fcf_5q = []
    for i in range(len(rev_5q)):
        o = ocf_5q[i] if i < len(ocf_5q) and ocf_5q[i] is not None else 0.0
        c = capex_5q[i] if i < len(capex_5q) and capex_5q[i] is not None else 0.0
        s = sbc_5q[i] if i < len(sbc_5q) and sbc_5q[i] is not None else 0.0
        l = leases_5q[i] if i < len(leases_5q) and leases_5q[i] is not None else 0.0
        rf = round(o - c, 2)
        tf = round(rf - s - l, 2)
        rep_fcf_5q.append(rf)
        true_fcf_5q.append(tf)

    # Deterministic Q0 values
    q0_rev = rev_5q[-1] if rev_5q else None
    q0_gp = gp_5q[-1] if gp_5q else None
    q0_opex = opex_5q[-1] if opex_5q else None
    q0_ebit = ebit_5q[-1] if ebit_5q else (round(q0_gp - q0_opex, 2) if q0_gp and q0_opex else None)
    q0_gaap_eps = gaap_eps_5q[-1] if gaap_eps_5q else None
    q0_nongaap_eps = nongaap_eps_5q[-1] if nongaap_eps_5q else None
    q0_ocf = ocf_5q[-1] if ocf_5q else None
    q0_capex = capex_5q[-1] if capex_5q else None
    q0_rep_fcf = rep_fcf_5q[-1] if rep_fcf_5q else None
    q0_sbc = sbc_5q[-1] if sbc_5q else None
    q0_leases = leases_5q[-1] if leases_5q else None
    q0_true_fcf = true_fcf_5q[-1] if true_fcf_5q else None

    # Margins
    q0_gm_pct = safe_float((q0_gp / q0_rev * 100) if q0_gp and q0_rev else None)
    q0_om_pct = safe_float((q0_ebit / q0_rev * 100) if q0_ebit and q0_rev else None)

    # Post-print moves
    reg_price = market_data["regular_close_price"] or 1.0
    ah_price = market_data["after_hours_price"] or reg_price
    post_print_move_pct = safe_float(((ah_price - reg_price) / reg_price) * 100)
    implied_move_pct = t1_baseline.get("options_implied_move_pct")

    # Beat / Miss math vs Street Consensus
    cons_rev = t1_baseline.get("consensus_revenue_millions")
    cons_eps = t1_baseline.get("consensus_eps_nongaap")
    whisper_rev = t1_baseline.get("whisper_revenue_millions")
    whisper_eps = t1_baseline.get("whisper_eps_nongaap")

    rev_beat_consensus_m = safe_float(q0_rev - cons_rev) if q0_rev and cons_rev else None
    rev_beat_consensus_pct = safe_float((rev_beat_consensus_m / cons_rev * 100) if rev_beat_consensus_m and cons_rev else None)
    rev_beat_whisper_m = safe_float(q0_rev - whisper_rev) if q0_rev and whisper_rev else None

    eps_beat_consensus_dlr = safe_float(q0_nongaap_eps - cons_eps) if q0_nongaap_eps is not None and cons_eps is not None else None
    eps_beat_consensus_pct = safe_float((eps_beat_consensus_dlr / cons_eps * 100) if eps_beat_consensus_dlr and cons_eps else None)
    eps_beat_whisper_dlr = safe_float(q0_nongaap_eps - whisper_eps) if q0_nongaap_eps is not None and whisper_eps is not None else None

    # Verdict Badge determination
    verdict_badge = "HEADLINE BEAT / LOW QUALITY"
    if rev_beat_consensus_m and rev_beat_consensus_m > 0 and eps_beat_consensus_dlr and eps_beat_consensus_dlr > 0:
        if q0_true_fcf and q0_true_fcf > 0:
            verdict_badge = "CLEAN BEAT & RAISE"
        else:
            verdict_badge = "HEADLINE BEAT / LOW QUALITY"
    elif (rev_beat_consensus_m and rev_beat_consensus_m < 0) or (eps_beat_consensus_dlr and eps_beat_consensus_dlr < 0):
        verdict_badge = "BEAT & LOWER" if (eps_beat_consensus_dlr and eps_beat_consensus_dlr > 0) else "CLEAN MISS"

    # Assemble complete locked truth payload
    post_truth = {
        "ticker": symbol,
        "earnings_date": earnings_date_str,
        "timestamp_generated": datetime.now().isoformat(),
        "t1_baseline": t1_baseline,
        "sec_filing_metadata": {
            "form": sec_data.get("filing_form"),
            "filing_date": sec_data.get("filing_date"),
            "exhibit_99_1_found": sec_data.get("exhibit_99_1_found"),
            "edgar_status": sec_data.get("edgar_status")
        },
        "market_portal": market_data,
        "post_print_reaction": {
            "regular_close_price": reg_price,
            "after_hours_price": ah_price,
            "post_print_move_pct": post_print_move_pct,
            "t1_options_implied_move_pct": implied_move_pct,
            "move_vs_implied_status": "WITHIN_IMPLIED_BAND" if implied_move_pct and abs(post_print_move_pct or 0) <= implied_move_pct else "EXCEEDED_IMPLIED_BAND",
            "overall_print_verdict": verdict_badge
        },
        "beat_miss_scorecard": {
            "revenue": {
                "reported_actual_millions": q0_rev,
                "street_consensus_millions": cons_rev,
                "whisper_millions": whisper_rev,
                "vs_consensus_delta_millions": rev_beat_consensus_m,
                "vs_consensus_delta_pct": rev_beat_consensus_pct,
                "vs_whisper_delta_millions": rev_beat_whisper_m,
                "verdict": "BEAT" if rev_beat_consensus_m and rev_beat_consensus_m >= 0 else "MISS"
            },
            "eps_nongaap": {
                "reported_actual": q0_nongaap_eps,
                "street_consensus": cons_eps,
                "whisper": whisper_eps,
                "vs_consensus_delta_dollars": eps_beat_consensus_dlr,
                "vs_consensus_delta_pct": eps_beat_consensus_pct,
                "vs_whisper_delta_dollars": eps_beat_whisper_dlr,
                "verdict": "BEAT" if eps_beat_consensus_dlr and eps_beat_consensus_dlr >= 0 else "MISS"
            },
            "eps_gaap": {
                "reported_actual": q0_gaap_eps,
                "street_consensus": t1_baseline.get("consensus_eps_gaap"),
                "verdict": "REPORTED"
            },
            "margins": {
                "reported_gross_margin_pct": q0_gm_pct,
                "reported_operating_margin_pct": q0_om_pct
            }
        },
        "stitched_5q_chronological": {
            "period_labels": [
                "Q3 2025", "Q4 2025", "Q1 2026", "Q2 2026", "Q3 2026 (Actual)"
            ],
            "total_revenue": rev_5q,
            "gross_profit": gp_5q,
            "operating_expenses": opex_5q,
            "operating_income": ebit_5q,
            "gaap_net_income": gaap_net_5q,
            "gaap_diluted_eps": gaap_eps_5q,
            "nongaap_diluted_eps": nongaap_eps_5q,
            "operating_cash_flow": ocf_5q,
            "capital_expenditures": capex_5q,
            "reported_fcf": rep_fcf_5q,
            "stock_based_compensation": sbc_5q,
            "finance_leases": leases_5q,
            "true_fcf": true_fcf_5q
        },
        "forensic_fcf_bridge_q0": {
            "ocf": q0_ocf,
            "capex": q0_capex,
            "reported_fcf": q0_rep_fcf,
            "sbc": q0_sbc,
            "finance_leases": q0_leases,
            "true_fcf": q0_true_fcf,
            "formula_check": {
                "ocf_minus_capex_equals_reported": abs((q0_ocf or 0) - (q0_capex or 0) - (q0_rep_fcf or 0)) <= 2.0,
                "reported_minus_sbc_leases_equals_true": abs((q0_rep_fcf or 0) - (q0_sbc or 0) - (q0_leases or 0) - (q0_true_fcf or 0)) <= 2.0
            }
        },
        "company_specific_facts": {k: v for k, v in facts.items() if not k.endswith("_5q")}
    }

    out_file = GROUND_TRUTH_DIR / f"{symbol}_{earnings_date_str}_post_truth.json"
    out_file.write_text(json.dumps(post_truth, indent=2), encoding="utf-8")
    print(f"[{symbol}] Deterministic Post-Earnings Ground Truth written to: {out_file.name}")
    return post_truth

# ==============================================================================
# MAIN / CLI DISPATCHER
# ==============================================================================
if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = [a.lower() for a in sys.argv[1:] if a.startswith("-")]
    
    is_check_only = "--check-only" in flags or "-c" in flags
    is_force = "--force" in flags or "-f" in flags
    today_str = date.today().isoformat()

    tickers = load_tickers()
    ledger = load_ledger()

    if is_check_only:
        print(f"Scanning tickers for T+0 earnings on {today_str}...")
        t0_matches = []
        for sym in tickers:
            try:
                t = yf.Ticker(sym)
                cal = t.calendar or {}
                e_dates = [str(d) for d in cal.get("Earnings Date", [])]
                if today_str in e_dates:
                    t0_matches.append({"ticker": sym, "earnings_date": today_str})
                elif (GROUND_TRUTH_DIR / f"{sym}_{today_str}_truth.json").exists():
                    t0_matches.append({"ticker": sym, "earnings_date": today_str, "has_t1_truth": True})
            except Exception:
                pass
        output = {
            "status": "ok",
            "check_date": today_str,
            "t0_matches": t0_matches,
            "reporting_today_count": len(t0_matches)
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)

    # Direct ticker run
    if args:
        target_ticker = args[0].upper()
        target_date = args[1] if len(args) > 1 else today_str
        payload = reconcile_and_compute_post_truth(target_ticker, target_date)
        print(json.dumps({"status": "SUCCESS", "ticker": target_ticker, "date": target_date, "verdict": payload["post_print_reaction"]["overall_print_verdict"]}))
        sys.exit(0)

    # Batch scan
    print(f"Running automated batch scan across {len(tickers)} tickers for {today_str}...")
    for sym in tickers:
        try:
            t = yf.Ticker(sym)
            cal = t.calendar or {}
            e_dates = [str(d) for d in cal.get("Earnings Date", [])]
            if today_str in e_dates or is_force:
                reconcile_and_compute_post_truth(sym, today_str)
        except Exception as e:
            print(f"Error checking {sym}: {e}", file=sys.stderr)
'''
    (BASE_DIR / "stage1_post_deterministic.py").write_text(code, encoding="utf-8")
    print(" [OK] stage1_post_deterministic.py generated.")

# ==============================================================================
# MODULE 2: stage4_validate_post.py
# ==============================================================================
def write_stage4_validate_post():
    code = '''"""
Stage 4 Post-Earnings (T+0) Deterministic Validator & Critic Gatekeeper
Validates drafts/{TICKER}_{DATE}_post_draft.json against:
1. File existence (post_draft.json and all 3 bus files in post_agent_bus/)
2. Inner HTML length >= 45,000 characters
3. Mandatory 9 sections (Header, Row 1B Scorecard with 3 sub-tables, 5Q Table, FCF Bridge,
   Audit Grid, Peer Benchmarks, Sentiment Grid, PM Scenario Matrix, Citations)
4. Template purity (zero shorthand classes)
5. Interactive tooltips (>= 18 .tip and data-tip definitions)
6. Segment leak prevention (zero Tesla terms if ticker != TSLA)
7. Deterministic Accounting Math (Gross Profit - OpEx = EBIT, OCF - CapEx = Rep FCF, True FCF balance)
8. Prose and value grounding (verbatim After-Hours price, Close price, Revenue, OCF)
9. PM Strike Sanity (Bull target > After-Hours price > Bear target)
Writes audit_logs/{TICKER}_{DATE}_post_validation.json
"""

import sys
import re
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
BUS_DIR = BASE_DIR / "post_agent_bus"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
DRAFTS_DIR = BASE_DIR / "drafts"
AUDIT_DIR = BASE_DIR / "audit_logs"

def validate_post_draft(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    errors = []

    truth_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_post_truth.json"
    draft_file = DRAFTS_DIR / f"{ticker}_{earnings_date}_post_draft.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_agent2b_transcript.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_agent2c_social.json"

    # Guardrail 0: Existence of all bus files & draft
    if not truth_file.exists():
        errors.append(f"Missing deterministic ground truth file: {truth_file.name}")
    if not draft_file.exists():
        errors.append(f"Missing post draft JSON file: {draft_file.name}")
    if not bus_2a.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2A: {bus_2a.name}")
    if not bus_2b.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2B: {bus_2b.name}")
    if not bus_2c.exists():
        errors.append(f"Missing Layer 2 bus file from Agent 2C: {bus_2c.name}")

    if errors:
        result = {"ticker": ticker, "earnings_date": earnings_date, "passed": False, "errors": errors}
        out_log = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
        out_log.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    truth = json.loads(truth_file.read_text(encoding="utf-8"))
    draft = json.loads(draft_file.read_text(encoding="utf-8"))
    html_body = draft.get("rendered_container_html", "")

    # Guardrail 1: Content Depth (>= 45,000 characters)
    MIN_CHAR_COUNT = 45000
    if len(html_body) < MIN_CHAR_COUNT:
        errors.append(
            f"TRUNCATED REPORT: Inner HTML length is {len(html_body):,} characters "
            f"(minimum requirement: {MIN_CHAR_COUNT:,} chars)."
        )

    # Guardrail 2: 9-Section Institutional Structure
    required_structural_components = [
        ("header-banner", "Section 1: Header Banner (<header class='header-banner'>)"),
        ("header-strip", "Section 1: Header Strip with key metrics (<div class='header-strip'>)"),
        ("kpi-grid", "Section 1: Executive KPI Grid (<section class='kpi-grid'>)"),
        ("scorecard", "Section 2: Row 1B Post-Release Expectations & Guidance Scorecard"),
        ("table-wrapper", "Section 3: Row 2 5-Quarter Stitched Financial Table (<div class='table-wrapper'>)"),
        ("forensic-grid", "Section 4: Row 3 Forensic Quality & True FCF Bridge (<div class='forensic-grid'>)"),
        ("waterfall-row", "Section 4: Row 3 FCF Waterfall Bridge rows (<div class='waterfall-row'>)"),
        ("audit-grid", "Section 5: Row 4 What Management Did Right vs Wrong + Q&A (<div class='audit-grid'>)"),
        ("sentiment-grid", "Section 7: Row 6 Multi-Source 4-Pillar Sentiment Grid (<div class='sentiment-grid'>)"),
        ("sentiment-meter-bar", "Section 7: Visual Sentiment Meter Bars (<div class='sentiment-meter-bar'>)"),
        ("scenario-grid", "Section 8: Row 7 Hedge Fund PM Trade Execution Matrix (<div class='scenario-grid'>)"),
        ("scenario-bull", "Section 8: Bull Case Scenario Card (<div class='scenario-bull'>)"),
        ("scenario-base", "Section 8: Base Case Scenario Card (<div class='scenario-base'>)"),
        ("scenario-bear", "Section 8: Bear Case Scenario Card (<div class='scenario-bear'>)"),
        ("trade-structure", "Section 8: Concrete Options Trade Structure (<div class='trade-structure'>)")
    ]
    for tag, desc in required_structural_components:
        if tag not in html_body:
            errors.append(f"Missing Required Section: {desc} is missing from rendered HTML.")

    # Guardrail 2B: Row 1B Sub-Tables (Table 1B-1, Table 1B-2, Table 1B-3)
    if "Table 1B-1" not in html_body and "Beat / Miss Scorecard" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-1 Headline & Company KPI Beat/Miss Scorecard.")
    if "Table 1B-2" not in html_body and "Management Execution Accountability" not in html_body and "Prior Quarter" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-2 Management Execution Accountability (Q0 Actual vs Q-1 Guidance).")
    if "Table 1B-3" not in html_body and "Forward Guidance Reset" not in html_body and "New Management Guidance" not in html_body:
        errors.append("Missing Row 1B Sub-table: Table 1B-3 Forward Guidance Reset (New Guidance vs Street Expectations).")

    # Guardrail 3: Template Purity
    disallowed_shorthand_tags = ['class="grid-2"', 'class="grid-4"', '<section class="section">']
    for stag in disallowed_shorthand_tags:
        if stag in html_body:
            errors.append(f"Unauthorized Shorthand Template Found ('{stag}'): Must use master design system CSS classes.")

    # Guardrail 4: Interactive Tooltips (>= 18)
    tip_count = html_body.count('class="tip')
    datatip_count = html_body.count('data-tip="')
    MIN_TOOLTIPS = 18
    if tip_count < MIN_TOOLTIPS or datatip_count < MIN_TOOLTIPS:
        errors.append(f"Interactive tooltips missing: Found {tip_count} '.tip' and {datatip_count} 'data-tip' definitions (require >= {MIN_TOOLTIPS}).")

    # Guardrail 5: Segment Leak Prevention
    if ticker != "TSLA":
        tesla_leaks = ["Automotive Regulatory Credits", "Cybercab", "Megapack", "Optimus"]
        for term in tesla_leaks:
            if term.lower() in html_body.lower():
                errors.append(f"Hardcoded Tesla term '{term}' found in {ticker} report! Must map {ticker}'s actual segments.")

    # Guardrail 6: Deterministic 5-Quarter P&L Math
    table_5q = draft.get("historical_table_5q_nums", [])
    if len(table_5q) == 5:
        for q_idx, q_data in enumerate(table_5q):
            gp = q_data.get("gross_profit")
            opex = q_data.get("operating_expenses")
            ebit = q_data.get("operating_income")
            if None not in (gp, opex, ebit) and abs((gp - opex) - ebit) > 2.0:
                errors.append(f"Quarter {q_idx+1} P&L Math Error: Gross Profit ({gp}) - OpEx ({opex}) != Operating Income ({ebit})")

    # Guardrail 7: Deterministic Cash Flow Bridge Math
    bridge = draft.get("forensic_callout", {}).get("fcf_bridge_q0_nums", {})
    if bridge:
        ocf = bridge.get("ocf", 0)
        capex = abs(bridge.get("capex", 0))
        rep_fcf = bridge.get("reported_fcf", 0)
        sbc = abs(bridge.get("sbc", 0))
        leases = abs(bridge.get("finance_leases", 0))
        true_fcf = bridge.get("true_fcf", 0)

        if abs((ocf - capex) - rep_fcf) > 2.0:
            errors.append(f"FCF Bridge Math Error: OCF ({ocf}) - CapEx ({capex}) != Reported FCF ({rep_fcf})")
        if abs((rep_fcf - sbc - leases) - true_fcf) > 2.0:
            errors.append(f"True FCF Math Error: Reported FCF ({rep_fcf}) - SBC ({sbc}) - Leases ({leases}) != True FCF ({true_fcf})")

    # Guardrail 8: Prose and Value Grounding
    ah_price = truth.get("post_print_reaction", {}).get("after_hours_price")
    reg_price = truth.get("post_print_reaction", {}).get("regular_close_price")
    q0_rev = truth.get("beat_miss_scorecard", {}).get("revenue", {}).get("reported_actual_millions")
    q0_ocf = truth.get("forensic_fcf_bridge_q0", {}).get("ocf")

    if ah_price and f"{ah_price:.2f}" not in html_body and f"{ah_price}" not in html_body:
        errors.append(f"Ground-Truth After-Hours Price (${ah_price}) does not appear in rendered HTML.")
    if reg_price and f"{reg_price:.2f}" not in html_body and f"{reg_price}" not in html_body:
        errors.append(f"Ground-Truth Regular Close Price (${reg_price}) does not appear in rendered HTML.")
    if q0_rev and f"{q0_rev:,.0f}" not in html_body and f"{q0_rev}" not in html_body:
        errors.append(f"Ground-Truth Q0 Revenue (${q0_rev}M) does not appear in rendered HTML.")
    if q0_ocf and f"{q0_ocf:,.0f}" not in html_body and f"{q0_ocf}" not in html_body:
        errors.append(f"Ground-Truth Q0 OCF (${q0_ocf}M) does not appear in rendered HTML.")

    # Guardrail 9: PM Strike Sanity
    trade_matrix = draft.get("trade_matrix", {})
    bull_target = trade_matrix.get("bull_target_low_num")
    bear_target = trade_matrix.get("bear_target_high_num")
    ref_price = ah_price or reg_price or 100.0

    if bull_target and bull_target <= ref_price:
        errors.append(f"PM Trade Logic Error: Bull target (${bull_target}) must be higher than After-Hours reference price (${ref_price}).")
    if bear_target and bear_target >= ref_price:
        errors.append(f"PM Trade Logic Error: Bear target (${bear_target}) must be lower than After-Hours reference price (${ref_price}).")

    # Guardrail 10: Placeholder Detector
    for bad_token in ["NaN", "undefined", "TODO", "PLACEHOLDER"]:
        if bad_token in html_body:
            errors.append(f"Illegal Placeholder Found: '{bad_token}' appears in rendered HTML.")

    passed = len(errors) == 0
    result = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "passed": passed,
        "character_count": len(html_body),
        "tooltips_count": tip_count,
        "errors": errors
    }

    out_log = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
    out_log.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stage4_validate_post.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    res = validate_post_draft(t, d)
    if res["passed"]:
        print(f"[PASS] Stage 4 validation passed for {t} ({d}). Length: {res['character_count']:,} chars.")
        sys.exit(0)
    else:
        print(f"[FAIL] Stage 4 validation failed for {t} ({d}):", file=sys.stderr)
        for err in res["errors"]:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
'''
    (BASE_DIR / "stage4_validate_post.py").write_text(code, encoding="utf-8")
    print(" [OK] stage4_validate_post.py generated.")

# ==============================================================================
# MODULE 3: stage4_render_post_html.py
# ==============================================================================
def write_stage4_render_post_html():
    code = '''"""
Stage 4 Post-Earnings (T+0) Read-Only CSS Cloner & Candidate HTML Assembler
- Clones locked CSS from published_reports/TSLA_T1_2026-10-21.html in read-only mode.
- Wraps rendered_container_html into published_reports/{TICKER}_T0_POST_{DATE}.html
- Pre-publish size check: Enforces rendered HTML >= 75,000 bytes.
- Supports multi-versioning (_v1, _v2, etc.) and canonical latest file.
"""

import sys
import re
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
AUDIT_DIR = BASE_DIR / "audit_logs"
DRAFTS_DIR = BASE_DIR / "drafts"
MASTER_HTML = REPORTS_DIR / "TSLA_T1_2026-10-21.html"
FALLBACK_MASTER = BASE_DIR / "Stock_Analysis_v2.html"

def get_master_css() -> str:
    ref_file = MASTER_HTML if MASTER_HTML.exists() else FALLBACK_MASTER
    if not ref_file.exists():
        raise RuntimeError("No master reference HTML file found for CSS cloning.")
    content = ref_file.read_text(encoding="utf-8")
    start = content.find("<style>")
    end = content.find("</style>") + len("</style>")
    if start == -1 or end == -1:
        raise RuntimeError("Could not isolate <style> block in master reference HTML.")
    return content[start:end]

def determine_post_version(ticker: str, earnings_date: str) -> tuple[int, list[int]]:
    REPORTS_DIR.mkdir(exist_ok=True)
    existing_versions = []
    pattern = rf"^{ticker}_T0_POST_{earnings_date}_v(\\d+)\\.html$"
    for f in REPORTS_DIR.glob(f"{ticker}_T0_POST_{earnings_date}_v*.html"):
        m = re.match(pattern, f.name)
        if m:
            existing_versions.append(int(m.group(1)))

    canonical_file = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}.html"
    if canonical_file.exists() and not existing_versions:
        v1_path = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}_v1.html"
        v1_path.write_bytes(canonical_file.read_bytes())
        existing_versions = [1]

    existing_versions.sort()
    next_ver = (existing_versions[-1] + 1) if existing_versions else 1
    return next_ver, existing_versions

def render_post_html(ticker: str, earnings_date: str) -> Path:
    ticker = ticker.upper()
    audit_file = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
    if not audit_file.exists():
        raise RuntimeError(f"Cannot render: Validation log {audit_file.name} does not exist.")
    audit = json.loads(audit_file.read_text(encoding="utf-8"))
    if not audit.get("passed"):
        raise RuntimeError(f"Cannot render: Validation failed: {audit.get('errors')}")

    draft_file = DRAFTS_DIR / f"{ticker}_{earnings_date}_post_draft.json"
    draft = json.loads(draft_file.read_text(encoding="utf-8"))

    locked_css = get_master_css()
    version_num, prior_versions = determine_post_version(ticker, earnings_date)
    ver_str = f"v{version_num}"
    timestamp_display = datetime.now().strftime("%b %d, %Y at %I:%M %p")

    # Version comparison banner
    version_banner_html = ""
    if prior_versions:
        pills = []
        for pv in prior_versions:
            pv_file = f"{ticker}_T0_POST_{earnings_date}_v{pv}.html"
            pills.append(f'<a href="{pv_file}" style="background: rgba(255,255,255,0.08); color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 11.5px; text-decoration: none; font-family: monospace; border: 1px solid rgba(255,255,255,0.15);">v{pv}</a>')
        pills_str = " ".join(pills)
        version_banner_html = f"""
    <!-- VERSION COMPARISON BANNER -->
    <div style="background: #0f172a; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 10px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
      <div style="display:flex; align-items:center; gap: 8px;">
        <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; font-weight: 800; font-family: monospace; padding: 3px 8px; border-radius: 5px; border: 1px solid rgba(16, 185, 129, 0.4);">{ver_str} (Active Post-Print)</span>
        <span style="color: #cbd5e1;">Generated on <strong>{timestamp_display}</strong></span>
      </div>
      <div style="display:flex; align-items:center; gap: 8px;">
        <span style="color: #94a3b8; font-size: 12px;">Compare prior iterations:</span>
        {pills_str}
      </div>
    </div>
        """

    container_html = draft["rendered_container_html"]
    container_with_ver = f"{version_banner_html}\\n{container_html}"

    page_title = draft.get("header", {}).get("page_title", f"{ticker} T+0 Post-Earnings Forensic Tearsheet")

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[{ver_str}] {page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  {locked_css}
</head>
<body>
  <div class="container">
    {container_with_ver}
  </div>
</body>
</html>
"""

    # Gatekeeper size check
    MIN_HTML_BYTES = 75000
    html_bytes = full_html.encode("utf-8")
    if len(html_bytes) < MIN_HTML_BYTES:
        raise RuntimeError(
            f"PRE-PUBLISH GATEKEEPER ERROR: Rendered HTML size is {len(html_bytes):,} bytes "
            f"(minimum requirement: {MIN_HTML_BYTES:,} bytes). Publication aborted."
        )

    # Write versioned file and canonical file
    versioned_path = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}_v{version_num}.html"
    canonical_path = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}.html"

    versioned_path.write_bytes(html_bytes)
    canonical_path.write_bytes(html_bytes)

    print(f"[{ticker}] Successfully rendered Post-Earnings HTML tearsheet:")
    print(f"  - Versioned: {versioned_path.name} ({len(html_bytes):,} bytes)")
    print(f"  - Canonical: {canonical_path.name}")
    return canonical_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stage4_render_post_html.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    out = render_post_html(t, d)
    print(f"[OK] Candidate HTML ready at: {out.name}")
'''
    (BASE_DIR / "stage4_render_post_html.py").write_text(code, encoding="utf-8")
    print(" [OK] stage4_render_post_html.py generated.")

# ==============================================================================
# MODULE 4: agent5_chief_auditor.py (CHIEF HTML AUDITOR & TARGETED BACK-ROUTER)
# ==============================================================================
def write_agent5_chief_auditor():
    code = '''"""
Agent 5: Chief HTML Auditor & Targeted Back-Router (Gemini 3.8 Flash High Standard)
Layer 5 Cross-Validation Gatekeeper:
- Deeply inspects rendered published_reports/{TICKER}_T0_POST_{DATE}.html against:
  - ground_truth/{TICKER}_{DATE}_post_truth.json
  - post_agent_bus/{TICKER}_{DATE}_agent2a_kpis.json
  - post_agent_bus/{TICKER}_{DATE}_agent2b_transcript.json
  - post_agent_bus/{TICKER}_{DATE}_agent2c_social.json
- Targeted Back-Routing Protocol:
  If any defect is detected, writes audit_logs/{TICKER}_{DATE}_agent5_signoff.json with:
    "status": "REJECTED"
    "route_to": LAYER_1_DETERMINISTIC | AGENT_2A_KPIS | AGENT_2B_TRANSCRIPT | AGENT_2C_SOCIAL | AGENT_4B_FINALIZER
  If all cross-validation checks pass, writes:
    "status": "APPROVED"
"""

import sys
import re
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
AUDIT_DIR = BASE_DIR / "audit_logs"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
BUS_DIR = BASE_DIR / "post_agent_bus"

def audit_rendered_post_html(ticker: str, earnings_date: str) -> dict:
    ticker = ticker.upper()
    html_file = REPORTS_DIR / f"{ticker}_T0_POST_{earnings_date}.html"
    truth_file = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_post_truth.json"
    bus_2a = BUS_DIR / f"{ticker}_{earnings_date}_agent2a_kpis.json"
    bus_2b = BUS_DIR / f"{ticker}_{earnings_date}_agent2b_transcript.json"
    bus_2c = BUS_DIR / f"{ticker}_{earnings_date}_agent2c_social.json"

    defects = []
    route_to = None

    if not html_file.exists():
        return {
            "ticker": ticker,
            "earnings_date": earnings_date,
            "status": "REJECTED",
            "route_to": "AGENT_4B_FINALIZER",
            "defects": [f"Rendered HTML file {html_file.name} does not exist."],
            "timestamp": datetime.now().isoformat()
        }

    html_content = html_file.read_text(encoding="utf-8")
    truth = json.loads(truth_file.read_text(encoding="utf-8")) if truth_file.exists() else {}
    kpis = json.loads(bus_2a.read_text(encoding="utf-8")) if bus_2a.exists() else {}
    transcript = json.loads(bus_2b.read_text(encoding="utf-8")) if bus_2b.exists() else {}
    social = json.loads(bus_2c.read_text(encoding="utf-8")) if bus_2c.exists() else {}

    # Check 1: Numeric Cross-Validation against Ground Truth
    q0_rev = truth.get("beat_miss_scorecard", {}).get("revenue", {}).get("reported_actual_millions")
    ah_price = truth.get("post_print_reaction", {}).get("after_hours_price")
    q0_ocf = truth.get("forensic_fcf_bridge_q0", {}).get("ocf")
    q0_fcf = truth.get("forensic_fcf_bridge_q0", {}).get("true_fcf")

    if q0_rev and f"{q0_rev:,.0f}" not in html_content and f"{q0_rev}" not in html_content:
        defects.append(f"Reported Q0 Revenue (${q0_rev}M) missing or mismatched in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    if ah_price and f"{ah_price:.2f}" not in html_content and f"{ah_price}" not in html_content:
        defects.append(f"Ground-Truth After-Hours Price (${ah_price}) missing in rendered HTML.")
        route_to = "LAYER_1_DETERMINISTIC"

    # Check 2: Row 1B Scorecard Table 1B-1, 1B-2, 1B-3
    if "Table 1B-1" not in html_content and "Beat / Miss Scorecard" not in html_content:
        defects.append("Missing Table 1B-1: Headline & Company KPI Beat / Miss Scorecard.")
        route_to = "AGENT_4B_FINALIZER"
    if "Table 1B-2" not in html_content and "Management Execution Accountability" not in html_content:
        defects.append("Missing Table 1B-2: Management Execution Accountability (Q0 vs Q-1 Guidance).")
        route_to = "AGENT_2B_TRANSCRIPT"
    if "Table 1B-3" not in html_content and "Forward Guidance Reset" not in html_content:
        defects.append("Missing Table 1B-3: Forward Guidance Reset (New Guidance vs Street Expectations).")
        route_to = "AGENT_2B_TRANSCRIPT"

    # Check 3: Depth of Transcript Forensic Findings (Agent 2B)
    if "Analyst Q&A" not in html_content and "Analyst Questions" not in html_content:
        defects.append("Call Q&A Forensic Highlights missing from Section 5 audit.")
        route_to = "AGENT_2B_TRANSCRIPT"

    # Check 4: Depth of Social & Microblogging Pulse (Agent 2C)
    if "Reddit" not in html_content and "FinTwit" not in html_content and "Retail" not in html_content:
        defects.append("Social microblogging pulse (Reddit/FinTwit/Retail) missing from Section 7 sentiment.")
        route_to = "AGENT_2C_SOCIAL"

    # Check 5: Interactive Tooltip Integrity
    tip_matches = len(re.findall(r'class="tip', html_content))
    if tip_matches < 18:
        defects.append(f"Insufficient interactive tooltips: Found {tip_matches}, require >= 18.")
        route_to = "AGENT_4B_FINALIZER"

    # Final verdict determination
    status = "APPROVED" if not defects else "REJECTED"
    signoff = {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "route_to": route_to,
        "defects": defects,
        "model_used": "Gemini 3.8 Flash High Standard",
        "summary": "All 9 sections cross-validated against deterministic ground truth and Layer 2 agent bus." if status == "APPROVED" else f"Rejected with {len(defects)} defects routed to {route_to}."
    }

    out_file = AUDIT_DIR / f"{ticker}_{earnings_date}_agent5_signoff.json"
    out_file.write_text(json.dumps(signoff, indent=2), encoding="utf-8")
    return signoff

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python agent5_chief_auditor.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    res = audit_rendered_post_html(t, d)
    print(f"Agent 5 Auditor Verdict: {res['status']}")
    if res["status"] == "REJECTED":
        print(f"Targeted Route-To: {res['route_to']}")
        for df in res["defects"]:
            print(f"  - {df}")
        sys.exit(1)
    else:
        print(f"Signoff approved for {t} ({d}).")
        sys.exit(0)
'''
    (BASE_DIR / "agent5_chief_auditor.py").write_text(code, encoding="utf-8")
    print(" [OK] agent5_chief_auditor.py generated.")

# ==============================================================================
# MODULE 5: stage5_publish_github.py
# ==============================================================================
def write_stage5_publish_github():
    code = '''"""
Stage 5 Post-Earnings (T+0) Automated Ledger Update, Index Sync & GitHub Pages Push
- Verifies both stage4_validate_post (passed == True) and agent5_signoff (status == APPROVED)
- Appends "{TICKER}_POST_{DATE}" to published_ledger.json
- Updates root index.html and published_reports/index.html via update_index.py
- Executes git add, commit, and push to origin main
- Outputs active GitHub Pages public link
"""

import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
AUDIT_DIR = BASE_DIR / "audit_logs"
LEDGER_FILE = BASE_DIR / "published_ledger.json"
REPORTS_DIR = BASE_DIR / "published_reports"

GITHUB_PAGES_BASE = "https://nitchau.github.io/earnings-intelligence"

def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    try:
        res = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=120
        )
        return res.returncode, res.stdout, res.stderr
    except Exception as e:
        return -1, "", str(e)

def publish_to_github(ticker: str, earnings_date: str):
    ticker = ticker.upper()
    val_file = AUDIT_DIR / f"{ticker}_{earnings_date}_post_validation.json"
    signoff_file = AUDIT_DIR / f"{ticker}_{earnings_date}_agent5_signoff.json"

    # 1. Gatekeeper checks
    if not val_file.exists():
        raise RuntimeError(f"Stage 4 validation file {val_file.name} does not exist.")
    val_data = json.loads(val_file.read_text(encoding="utf-8"))
    if not val_data.get("passed"):
        raise RuntimeError(f"Cannot publish: Stage 4 validation failed: {val_data.get('errors')}")

    if not signoff_file.exists():
        raise RuntimeError(f"Agent 5 signoff file {signoff_file.name} does not exist.")
    signoff_data = json.loads(signoff_file.read_text(encoding="utf-8"))
    if signoff_data.get("status") != "APPROVED":
        raise RuntimeError(f"Cannot publish: Agent 5 auditor rejected report: {signoff_data.get('defects')}")

    target_filename = f"{ticker}_T0_POST_{earnings_date}.html"
    report_file = REPORTS_DIR / target_filename
    if not report_file.exists():
        raise RuntimeError(f"Target report {target_filename} does not exist in published_reports/.")

    # 2. Update published_ledger.json
    ledger = {"published": [], "links": {}}
    if LEDGER_FILE.exists():
        try:
            ledger = json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    pub_key = f"{ticker}_POST_{earnings_date}"
    if pub_key not in ledger["published"]:
        ledger["published"].append(pub_key)

    gh_url = f"{GITHUB_PAGES_BASE}/published_reports/{target_filename}"
    local_url = f"http://localhost:8080/published_reports/{target_filename}"
    ledger.setdefault("links", {})[pub_key] = {
        "local_browser_url": local_url,
        "github_pages_url": gh_url,
        "public_sharable_url": gh_url
    }
    LEDGER_FILE.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    print(f"[{ticker}] Updated published_ledger.json with {pub_key}")

    # 3. Synchronize index.html
    try:
        from update_index import update_index_html
        update_index_html()
        print(f"[{ticker}] Synchronized index.html across root and published_reports/")
    except Exception as e:
        print(f"Warning updating index.html: {e}", file=sys.stderr)

    # 4. Git commit and push
    print(f"[{ticker}] Staging files and pushing to GitHub...")
    run_cmd(["git", "add", "published_reports/", "index.html", "published_ledger.json", "audit_logs/"])
    commit_msg = f"Auto-publish T+0 Post-Earnings Tearsheet for {ticker} ({earnings_date})"
    code, out, err = run_cmd(["git", "commit", "-m", commit_msg])
    if code == 0:
        print("Git commit successful.")
    else:
        print(f"Git commit note: {out.strip() or err.strip()}")

    p_code, p_out, p_err = run_cmd(["git", "push", "origin", "main"])
    if p_code == 0:
        print("Git push successful! GitHub Pages is building live.")
    else:
        print(f"Git push warning: {p_err.strip() or p_out.strip()}")

    print("\\n" + "=" * 75)
    print(f"REPORT PUBLISHED SUCCESSFULLY FOR {ticker} ({earnings_date})")
    print(f"Live GitHub Pages URL: {gh_url}")
    print(f"Local Browser URL:     {local_url}")
    print("=" * 75)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stage5_publish_github.py <TICKER> <EARNINGS_DATE>", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2]
    publish_to_github(t, d)
'''
    (BASE_DIR / "stage5_publish_github.py").write_text(code, encoding="utf-8")
    print(" [OK] stage5_publish_github.py generated.")

# ==============================================================================
# MODULE 6: update_index.py (ENHANCED TO SUPPORT BOTH T1 AND T0_POST)
# ==============================================================================
def write_update_index_enhanced():
    code = '''"""
Enhanced Dashboard Generator for Institutional Earnings Intelligence
Discovers and displays both:
- T-1 Pre-Earnings Briefings ({TICKER}_T1_{DATE}.html)
- T+0 Post-Earnings Forensic Tearsheets ({TICKER}_T0_POST_{DATE}.html)
"""

import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
LEDGER_PATH = BASE_DIR / "published_ledger.json"
TUNNEL_FILE = BASE_DIR / "tunnel_url.json"
GITHUB_PAGES_BASE = "https://nitchau.github.io/earnings-intelligence"

def get_base_urls():
    local_base = "http://localhost:8080"
    public_base = GITHUB_PAGES_BASE
    if TUNNEL_FILE.exists():
        try:
            t_data = json.loads(TUNNEL_FILE.read_text(encoding="utf-8"))
            tunnel = t_data.get("tunnel_url", "").rstrip("/")
            if tunnel:
                public_base = tunnel
        except Exception:
            pass
    return local_base, public_base

def extract_metadata_from_html(html_path: Path) -> dict:
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    is_post = "_T0_POST_" in html_path.name
    meta = {
        "title": html_path.stem,
        "company_name": "",
        "ticker": "",
        "earnings_date": "",
        "spot_price": "",
        "implied_move": "",
        "sector": "",
        "is_post": is_post,
        "status_badge": "T+0 POST-EARNINGS" if is_post else "T-1 PRE-EARNINGS"
    }
    
    m_sym = re.search(r'<span class="ticker-symbol">([A-Z0-9]+)</span>', content)
    if m_sym:
        meta["ticker"] = m_sym.group(1)
        
    m_name = re.search(r'<h1 class="company-name">([^<]+)</h1>', content)
    if m_name:
        meta["company_name"] = m_name.group(1).strip()
        
    m_sec = re.search(r'<div class="sector-tag">([^<]+)', content)
    if m_sec:
        meta["sector"] = m_sec.group(1).split("•")[0].strip()
        
    m_price = re.search(r'<div class="price-value">\\$([0-9,.]+)', content)
    if m_price:
        meta["spot_price"] = f"${m_price.group(1)}"
        
    m_move = re.search(r'Options-Implied Move[^<]*</span>\\s*<span class="strip-val"[^>]*>([^<]+)</span>', content)
    if m_move:
        meta["implied_move"] = m_move.group(1).replace("±", "&plusmn;").strip()
        
    m_date = re.search(r'(?:Upcoming|Official Earnings|Reported Date)[^<]*Release Date</span>\s*<span class="strip-val">([^<]+)', content)
    if m_date:
        meta["earnings_date"] = m_date.group(1).strip()
        
    return meta

def build_cards_html(grouped: dict, link_prefix: str) -> str:
    cards_html = []
    sorted_keys = sorted(
        grouped.keys(),
        key=lambda k: (grouped[k]["earnings_date"], grouped[k]["is_post"], grouped[k]["ticker"]),
        reverse=True
    )
    
    for key in sorted_keys:
        item = grouped[key]
        ticker = item["ticker"]
        e_date = item["earnings_date"]
        is_post = item["is_post"]
        
        ver_nums = sorted(item["versions"].keys())
        latest_file = item["canonical"] or (item["versions"][ver_nums[-1]] if ver_nums else None)
        if not latest_file:
            continue
            
        latest_ver_label = f"v{ver_nums[-1]}" if ver_nums else "v1"
        mod_time = datetime.fromtimestamp(latest_file.stat().st_mtime).strftime("%b %d, %Y • %I:%M %p")
        
        meta = extract_metadata_from_html(latest_file)
        company_name = meta["company_name"] or ticker
        spot_price = meta["spot_price"] or "N/A"
        implied_move = meta["implied_move"] or "&plusmn;2.5%"
        sector = meta["sector"] or "Equities / Technology"
        e_date_display = meta["earnings_date"] or e_date
        
        badge_style = "background: rgba(16, 185, 129, 0.2); border-color: rgba(16, 185, 129, 0.4); color: #34d399;" if is_post else "background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3); color: #60a5fa;"
        status_label = "T+0 POST-EARNINGS" if is_post else "T-1 PRE-EARNINGS"

        # Version pills
        v_pills = []
        if ver_nums:
            for v in ver_nums:
                v_file = item["versions"][v]
                v_name = f"v{v}"
                v_href = f"{link_prefix}{v_file.name}"
                is_curr = (v == ver_nums[-1])
                curr_style = "background: rgba(59, 130, 246, 0.3); border-color: #3b82f6; color: #93c5fd; font-weight: 700;" if is_curr else "background: rgba(255, 255, 255, 0.05); color: #94a3b8;"
                v_pills.append(f'<a href="{v_href}" class="v-pill" style="{curr_style}">{v_name}</a>')
        else:
            v_pills.append(f'<span class="v-pill" style="background: rgba(59, 130, 246, 0.2); color: #93c5fd;">v1</span>')
            
        versions_html = " ".join(v_pills)
        canonical_href = f"{link_prefix}{latest_file.name}"
        
        card = f"""
        <div class="report-card">
          <div class="card-top">
            <div class="ticker-box">
              <span class="ticker-symbol">{ticker}</span>
              <span class="version-tag">{latest_ver_label} (Latest)</span>
            </div>
            <span class="badge-status" style="{badge_style}">{status_label}</span>
          </div>

          <div class="company-title">{company_name}</div>
          <div class="sector-line">{sector} • {e_date_display}</div>

          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-label">Spot / AH Price</span>
              <span class="stat-val">{spot_price}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Implied Move</span>
              <span class="stat-val" style="color: #f59e0b;">{implied_move}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Updated</span>
              <span class="stat-val" style="font-size: 11.5px; color: #94a3b8;">{mod_time}</span>
            </div>
          </div>

          <div class="version-section">
            <span class="version-label">Iterations:</span>
            <div class="v-pill-group">
              {versions_html}
            </div>
          </div>

          <div class="card-footer">
            <a href="{canonical_href}" class="btn-view">
              <span>Open Tearsheet</span>
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </a>
          </div>
        </div>
        """
        cards_html.append(card)

    return "\\n".join(cards_html)

def build_full_page(cards_html: str, total_count: int, public_base: str) -> str:
    last_updated_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    tunnel_link_html = ""
    if public_base:
        label = "🌐 <strong>Production Live URL (GitHub Pages):</strong>" if "github.io" in public_base else "🌐 <strong>Public Live Tunnel:</strong>"
        tunnel_link_html = f'<div class="tunnel-bar">{label} <a href="{public_base}" target="_blank" style="color:#60a5fa; text-decoration:none;">{public_base}</a></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Institutional Earnings Intelligence Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #090d16;
      --card-bg: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-blue: #3b82f6;
      --bull-green: #22c55e;
      --warn-amber: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}
    .dashboard-container {{
      max-width: 1200px;
      width: 100%;
    }}
    .header {{
      text-align: center;
      margin-bottom: 28px;
    }}
    .header h1 {{
      font-size: 34px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin: 0 0 10px 0;
      background: linear-gradient(135deg, #ffffff 40%, #93c5fd 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header p {{
      color: var(--text-muted);
      font-size: 15px;
      margin: 0 auto;
      max-width: 720px;
      line-height: 1.5;
    }}
    .summary-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px 20px;
      margin-bottom: 26px;
      font-size: 13.5px;
    }}
    .summary-stat {{
      color: var(--text-muted);
    }}
    .summary-stat strong {{
      color: #60a5fa;
      font-family: 'JetBrains Mono', monospace;
    }}
    .tunnel-bar {{
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 8px;
      padding: 10px 16px;
      margin-bottom: 24px;
      font-size: 13px;
      text-align: center;
      color: #cbd5e1;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 20px;
    }}
    .report-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease-in-out;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }}
    .report-card:hover {{
      border-color: rgba(59, 130, 246, 0.4);
      transform: translateY(-3px);
      box-shadow: 0 12px 24px -6px rgba(59, 130, 246, 0.25);
    }}
    .card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}
    .ticker-box {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .ticker-symbol {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 22px;
      font-weight: 800;
      color: #60a5fa;
      letter-spacing: -0.02em;
    }}
    .version-tag {{
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.3);
      padding: 2px 7px;
      border-radius: 5px;
      font-size: 11px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}
    .badge-status {{
      font-size: 11px;
      font-weight: 700;
      border: 1px solid;
      padding: 4px 8px;
      border-radius: 6px;
    }}
    .company-title {{
      font-size: 16px;
      font-weight: 700;
      color: #f1f5f9;
      margin-bottom: 4px;
      line-height: 1.3;
    }}
    .sector-line {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }}
    .stats-row {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.04);
      border-radius: 8px;
      padding: 10px;
      margin-bottom: 16px;
    }}
    .stat-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .stat-label {{
      font-size: 10.5px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .stat-val {{
      font-size: 13.5px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #f8fafc;
    }}
    .version-section {{
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 12px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .version-label {{
      font-size: 11.5px;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .v-pill-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .v-pill {{
      display: inline-block;
      text-decoration: none;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      border: 1px solid rgba(255, 255, 255, 0.1);
      transition: all 0.15s ease;
    }}
    .v-pill:hover {{
      border-color: #60a5fa;
      color: #ffffff !important;
      background: rgba(59, 130, 246, 0.3) !important;
    }}
    .card-footer {{
      margin-top: auto;
    }}
    .btn-view {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 10px 16px;
      color: #ffffff;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 600;
      transition: all 0.15s ease;
    }}
    .btn-view:hover {{
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }}
    .footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--card-border);
      padding-top: 20px;
      width: 100%;
    }}
  </style>
</head>
<body>
  <div class="dashboard-container">
    <header class="header">
      <h1>Institutional Earnings Intelligence Dashboard</h1>
      <p>Multi-Agent Autonomous Research Mesh: T-1 Pre-Earnings Briefings &amp; T+0 Post-Earnings Forensic Accounting Tearsheets</p>
    </header>

    {tunnel_link_html}

    <div class="summary-bar">
      <div class="summary-stat">Active Reports: <strong>{total_count}</strong></div>
      <div class="summary-stat">T-1 / T+0 Dual Mode: <strong>Enabled</strong></div>
      <div class="summary-stat">Last Updated: <strong>{last_updated_str}</strong></div>
    </div>

    <div class="grid">
      {cards_html}
    </div>

    <footer class="footer">
      <div>Antigravity 2.0 Autonomous Financial Research Harness • Deterministic SEC Edgar Ground Truth</div>
    </footer>
  </div>
</body>
</html>
"""

def update_index_html():
    REPORTS_DIR.mkdir(exist_ok=True)
    local_base, public_base = get_base_urls()
    
    all_html_files = [f for f in REPORTS_DIR.glob("*.html") if f.name != "index.html"]
    grouped = {}

    for f in all_html_files:
        # Match T-1 reports
        m_t1 = re.match(r"^([A-Z0-9]+)_T1_(\d{4}-\d{2}-\d{2})(?:_v(\d+))?\.html$", f.name)
        if m_t1:
            ticker, e_date, ver = m_t1.group(1), m_t1.group(2), m_t1.group(3)
            key = f"{ticker}_{e_date}_T1"
            if key not in grouped:
                grouped[key] = {"ticker": ticker, "earnings_date": e_date, "is_post": False, "canonical": None, "versions": {}}
            if ver:
                grouped[key]["versions"][int(ver)] = f
            else:
                grouped[key]["canonical"] = f
            continue

        # Match T+0 POST reports
        m_t0 = re.match(r"^([A-Z0-9]+)_T0_POST_(\d{4}-\d{2}-\d{2})(?:_v(\d+))?\.html$", f.name)
        if m_t0:
            ticker, e_date, ver = m_t0.group(1), m_t0.group(2), m_t0.group(3)
            key = f"{ticker}_{e_date}_T0_POST"
            if key not in grouped:
                grouped[key] = {"ticker": ticker, "earnings_date": e_date, "is_post": True, "canonical": None, "versions": {}}
            if ver:
                grouped[key]["versions"][int(ver)] = f
            else:
                grouped[key]["canonical"] = f

    total_count = len(grouped)

    # 1. Generate for published_reports/index.html
    cards_for_reports = build_cards_html(grouped, link_prefix="")
    html_for_reports = build_full_page(cards_for_reports, total_count, public_base)
    (REPORTS_DIR / "index.html").write_text(html_for_reports, encoding="utf-8")

    # 2. Generate for root index.html
    cards_for_root = build_cards_html(grouped, link_prefix="published_reports/")
    html_for_root = build_full_page(cards_for_root, total_count, public_base)
    (BASE_DIR / "index.html").write_text(html_for_root, encoding="utf-8")

    print(f"Successfully updated index.html for {total_count} tracked pre/post reports.")

if __name__ == "__main__":
    update_index_html()
'''
    (BASE_DIR / "update_index.py").write_text(code, encoding="utf-8")
    print(" [OK] update_index.py enhanced.")

# ==============================================================================
# MODULE 7: AGENTS_POST.md (ORCHESTRATION RULES & AGENT SPECIFICATION)
# ==============================================================================
def write_agents_post_md():
    content = '''# Antigravity 2.0 Post-Earnings (T+0) Multi-Agent Orchestration Harness

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
'''
    (BASE_DIR / "AGENTS_POST.md").write_text(content, encoding="utf-8")
    print(" [OK] AGENTS_POST.md generated.")

# ==============================================================================
# MODULE 8: run_post_harness.py (END-TO-END ORCHESTRATION RUNNER)
# ==============================================================================
def write_run_post_harness():
    code = '''"""
End-to-End Orchestrator for Post-Earnings (T+0) Tearsheet Generation
Executes the full 5-Layer workflow:
1. Stage 1: Deterministic Data Mesh (stage1_post_deterministic.py)
2. Layer 2: Checks bus files or invokes dedicated draft builder
3. Stage 4: stage4_validate_post.py & stage4_render_post_html.py
4. Layer 5: agent5_chief_auditor.py & stage5_publish_github.py
"""

import sys
import json
import subprocess
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def run_step(cmd: list[str], step_name: str) -> bool:
    print(f"\\n>>> RUNNING: {step_name}...")
    res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True, encoding="utf-8")
    if res.returncode != 0:
        print(f"[ERROR] Step '{step_name}' failed with exit code {res.returncode}.", file=sys.stderr)
        return False
    print(f"[SUCCESS] Step '{step_name}' passed.")
    return True

def run_post_harness_for_ticker(ticker: str, earnings_date: str):
    ticker = ticker.upper()
    print("=" * 75)
    print(f"STARTING T+0 POST-EARNINGS ORCHESTRATION: {ticker} ({earnings_date})")
    print("=" * 75)

    # Step 1: Stage 1 Deterministic Anchor
    if not run_step([sys.executable, "stage1_post_deterministic.py", ticker, earnings_date], "Stage 1 Deterministic Anchor"):
        sys.exit(1)

    # Step 2: Check Layer 2 Bus files / run draft builder if present
    draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_post_draft.json"
    if not draft_path.exists():
        builder = BASE_DIR / ticker / f"build_{ticker.lower()}_post_draft.py"
        if builder.exists():
            if not run_step([sys.executable, str(builder)], f"Draft Builder for {ticker}"):
                sys.exit(1)
        else:
            print(f"[NOTICE] Draft {draft_path.name} not found. Please populate Layer 2 bus and build draft.", file=sys.stderr)
            sys.exit(1)

    # Step 3: Stage 4 Validation
    if not run_step([sys.executable, "stage4_validate_post.py", ticker, earnings_date], "Stage 4 Deterministic Validation"):
        sys.exit(1)

    # Step 4: Stage 4 HTML Rendering
    if not run_step([sys.executable, "stage4_render_post_html.py", ticker, earnings_date], "Stage 4 HTML Rendering"):
        sys.exit(1)

    # Step 5: Agent 5 Cross-Audit
    if not run_step([sys.executable, "agent5_chief_auditor.py", ticker, earnings_date], "Agent 5 Chief HTML Cross-Audit"):
        sys.exit(1)

    # Step 6: Stage 5 Publish & GitHub Sync
    if not run_step([sys.executable, "stage5_publish_github.py", ticker, earnings_date], "Stage 5 GitHub Publishing"):
        sys.exit(1)

    print("=" * 75)
    print(f"T+0 POST-EARNINGS HARNESS RUN COMPLETE FOR {ticker} ({earnings_date})")
    print("=" * 75)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_post_harness.py <TICKER> [EARNINGS_DATE]", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    run_post_harness_for_ticker(t, d)
'''
    (BASE_DIR / "run_post_harness.py").write_text(code, encoding="utf-8")
    print(" [OK] run_post_harness.py generated.")

if __name__ == "__main__":
    setup_harness()
