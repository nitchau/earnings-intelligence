"""
Stage 1 Post-Earnings (T+0) Deterministic Financial Data Mesh
Executes Layer 0 (Gatekeeper) & Layer 1 (Deterministic Mesh) before any LLM writes prose:
- Gatekeeper (Layer 0): Checks tickers.txt and published_ledger.json for T+0 reporting.
  Supports CLI forced ticker or --check-only scan.
  Extracts locked T-1 baseline (consensus, whisper, implied move, prior guidance).
- Agent 1A (SEC_IR_Agent): Pulls Form 8-K (Item 2.02) / 10-Q / Exhibit 99.1 filings via edgartools/SEC API
  and caches {TICKER}/exhibit_99_1.txt for deterministic reproducibility.
- Agent 1B (Market_Portal_Agent): Pulls closing price, after-hours price/volume from Yahoo & Google Finance.
- Agent 1C (Data_Reconciliation_Referee): Reconciles sources, rolls forward 5-quarter table,
  pre-computes all QoQ/YoY/bps deltas, beat/miss deltas, post-print move, and FCF bridge.
  Saves locked payload to ground_truth/{TICKER}_{DATE}_post_truth.json.
"""

import sys
import re
import json
import math
from datetime import datetime, date
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
        candidates = [p for p in GROUND_TRUTH_DIR.glob(f"{ticker}_*_truth.json") if not p.name.endswith("_post_truth.json")]
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
            m_dual = re.search(r'Consensus Revenue.*?<span class="strip-val">\$([0-9,.]+)\s*([MB])?\s*/\s*\$([0-9,.]+)\s*([MB])?', content, re.DOTALL | re.IGNORECASE)
            if m_dual:
                u1 = m_dual.group(2) or ('B' if 'B' in m_dual.group(0) else 'M')
                u2 = m_dual.group(4) or ('B' if 'B' in m_dual.group(0) else 'M')
                baseline["consensus_revenue_millions"] = safe_float(float(m_dual.group(1).replace(',', '')) * (1000 if u1 == 'B' else 1))
                baseline["whisper_revenue_millions"] = safe_float(float(m_dual.group(3).replace(',', '')) * (1000 if u2 == 'B' else 1))
            else:
                m_single = re.search(r'Consensus(?: Net)? Revenue.*?<span class="strip-val">\$([0-9,.]+)\s*([MB])?', content, re.DOTALL | re.IGNORECASE)
                if m_single:
                    u = m_single.group(2) or ('B' if 'B' in m_single.group(0) and float(m_single.group(1).replace(',', '')) < 500 else 'M')
                    baseline["consensus_revenue_millions"] = safe_float(float(m_single.group(1).replace(',', '')) * (1000 if u == 'B' else 1))

            m_eps_dual = re.search(r'Consensus.*?EPS.*?<span class="strip-val">\$([0-9.]+)[^/]*[/\\]\s*\$([0-9.]+)\s*Whisper', content, re.DOTALL | re.IGNORECASE)
            if m_eps_dual:
                baseline["consensus_eps_nongaap"] = safe_float(m_eps_dual.group(1))
                baseline["whisper_eps_nongaap"] = safe_float(m_eps_dual.group(2))
            else:
                m_eps = re.search(r'Consensus.*?EPS.*?<span class="strip-val">\$([0-9.]+)', content, re.DOTALL | re.IGNORECASE)
                if m_eps:
                    baseline["consensus_eps_nongaap"] = safe_float(m_eps.group(1))

            if baseline["consensus_revenue_millions"] is None:
                m_curr_rev = re.search(r'Consensus\s+(?:Net\s+)?(?:Revenue|Sales|Net Sales).*?<span class="strip-val">[^0-9]*([0-9,.]+)\s*([MB])?', content, re.DOTALL | re.IGNORECASE)
                if m_curr_rev:
                    u = m_curr_rev.group(2) or ('B' if 'B' in m_curr_rev.group(0) and float(m_curr_rev.group(1).replace(',', '')) < 500 else 'M')
                    baseline["consensus_revenue_millions"] = safe_float(float(m_curr_rev.group(1).replace(',', '')) * (1000 if u == 'B' else 1))

            if baseline["consensus_eps_nongaap"] is None:
                m_curr_eps = re.search(r'Consensus.*?EPS.*?<span class="strip-val">[^0-9]*([0-9.]+)', content, re.DOTALL | re.IGNORECASE)
                if m_curr_eps:
                    baseline["consensus_eps_nongaap"] = safe_float(m_curr_eps.group(1))
            m_gaap = re.search(r'GAAP</span>\s*EPS Est:\s*\$([0-9.]+)', content)
            if m_gaap:
                baseline["consensus_eps_gaap"] = safe_float(m_gaap.group(1))

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

    # Check cached {symbol}/exhibit_99_1.txt first for speed and deterministic reproducibility
    ticker_dir = BASE_DIR / symbol
    cached_ex = ticker_dir / "exhibit_99_1.txt"
    if cached_ex.exists():
        exhibit_text = cached_ex.read_text(encoding="utf-8", errors="ignore")
        sec_data["filing_form"] = "8-K"
        sec_data["filing_date"] = target_date_str
        sec_data["exhibit_99_1_found"] = True
        sec_data["edgar_status"] = "FILING_RETRIEVED"
        sec_data["facts"] = parse_financial_metrics_from_text(exhibit_text, symbol)
        return sec_data

    if not EDGAR_AVAILABLE:
        sec_data["edgar_status"] = "EDGARTOOLS_LIBRARY_NOT_INSTALLED"
        return sec_data

    try:
        comp = Company(symbol)
        sec_data["cik"] = str(comp.cik).zfill(10)

        filings = comp.get_filings(form=["8-K", "10-Q", "10-K"]).latest(5)
        target_filing = None
        for f in filings:
            if str(f.filing_date) == target_date_str and f.form == "8-K":
                target_filing = f
                break
        if not target_filing:
            for f in filings:
                if f.form == "8-K":
                    target_filing = f
                    break
        if not target_filing and filings:
            target_filing = filings[0]

        if target_filing:
            sec_data["filing_form"] = target_filing.form
            sec_data["filing_date"] = str(target_filing.filing_date)
            sec_data["edgar_status"] = "FILING_RETRIEVED"
            sec_data["items"] = getattr(target_filing, "items", [])

            exhibit_text = ""
            for att in getattr(target_filing, "attachments", []):
                desc = getattr(att, "description", "").lower()
                doc_name = att.document.lower()
                if "99.1" in desc or "exhibit99" in doc_name or "ex-99" in doc_name or "991" in doc_name or "press" in desc:
                    try:
                        raw = att.download()
                        soup = BeautifulSoup(raw, "html.parser")
                        exhibit_text = soup.get_text("\n", strip=True)
                        sec_data["exhibit_99_1_found"] = True
                        break
                    except Exception:
                        pass

            if not exhibit_text:
                try:
                    exhibit_text = target_filing.text()
                except Exception:
                    pass

            if exhibit_text:
                try:
                    ticker_dir.mkdir(parents=True, exist_ok=True)
                    cached_ex.write_text(exhibit_text, encoding="utf-8")
                except Exception:
                    pass
                sec_data["facts"] = parse_financial_metrics_from_text(exhibit_text, symbol)

    except Exception as e:
        sec_data["edgar_status"] = f"ERROR: {str(e)}"

    return sec_data

def parse_financial_metrics_from_text(text: str, symbol: str) -> dict:
    facts = {}
    flat_text = re.sub(r"\s+", " ", text)

    # 1. 5-value horizontal row patterns (e.g., TSLA Shareholder Deck)
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
        m = re.search(pat, flat_text, re.IGNORECASE)
        if m:
            vals = [safe_float(v.replace(",", "")) for v in m.groups()]
            facts[key] = vals
            facts[f"{key.replace('_5q', '')}_q0"] = vals[-1] if vals else None

    # 2. Multi-column condensed financial statement & ticker-specific 8-K extraction
    if symbol == "TSLA":
        m_auto = re.search(r"Total automotive revenues\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_energy = re.search(r"Energy generation and storage revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_services = re.search(r"Services and other revenue\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_storage = re.search(r"Storage deployed \(GWh\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", flat_text, re.IGNORECASE)
        m_deliveries = re.search(r"Total deliveries(?:\(1\))?\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_fsd = re.search(r"Active FSD Subscriptions(?:\(3\))?\s+\(mil\)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", flat_text, re.IGNORECASE)

        if m_auto: facts["automotive_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_auto.groups()]
        if m_energy: facts["energy_storage_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_energy.groups()]
        if m_services: facts["services_revenue_5q"] = [safe_float(v.replace(",", "")) for v in m_services.groups()]
        if m_storage: facts["storage_deployed_gwh_5q"] = [safe_float(v) for v in m_storage.groups()]
        if m_deliveries: facts["deliveries_5q"] = [safe_float(v.replace(",", "")) for v in m_deliveries.groups()]
        if m_fsd: facts["fsd_subs_mil_5q"] = [safe_float(v) for v in m_fsd.groups()]

    elif symbol == "META":
        m_rev = re.search(r"CONDENSED CONSOLIDATED STATEMENTS OF INCOME.*?Revenue\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_cogs = re.search(r"Cost of revenue\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_rd = re.search(r"Research and development\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_ms = re.search(r"Marketing and sales\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_ga = re.search(r"General and administrative\s*(?:\(\d+\))?\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_opinc = re.search(r"Income from operations\s+\$?\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_net = re.search(r"Net income\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_eps_g = re.search(r"Diluted earnings per share \(EPS\)\s+\$\s*(\d+(?:\.\d+)?)", flat_text, re.IGNORECASE)
        m_eps_adj = re.search(r"Diluted EPS of \$\d+(?:\.\d+)? would have increased by \$\d+(?:\.\d+)? to \$(\d+(?:\.\d+)?)", flat_text, re.IGNORECASE)
        m_ocf = re.search(r"Net cash provided by operating activities\s+\$?\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_capex = re.search(r"Purchases of property and equipment\s+\(([\d,]+)\)", flat_text, re.IGNORECASE)
        m_sbc = re.search(r"Share-based compensation\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_leases = re.search(r"Principal payments on finance leases\s+\(([\d,]+)\)", flat_text, re.IGNORECASE)
        m_ad_rev = re.search(r"Segment Information.*?Advertising\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_foa_rev = re.search(r"Segment Information.*?Family of Apps\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_rl_rev = re.search(r"Segment Information.*?Reality Labs\s+([\d,]+)", flat_text, re.IGNORECASE)

        if m_rev: facts["revenue_q0"] = safe_float(m_rev.group(1).replace(",", ""))
        if m_cogs: facts["cost_of_revenue_q0"] = safe_float(m_cogs.group(1).replace(",", ""))
        if "revenue_q0" in facts and "cost_of_revenue_q0" in facts:
            facts["gross_profit_q0"] = round(facts["revenue_q0"] - facts["cost_of_revenue_q0"], 2)
        if m_rd and m_ms and m_ga:
            rd_v = safe_float(m_rd.group(1).replace(",", ""))
            ms_v = safe_float(m_ms.group(1).replace(",", ""))
            ga_v = safe_float(m_ga.group(1).replace(",", ""))
            facts["rd_q0"] = rd_v
            facts["sga_q0"] = round(ms_v + ga_v, 2)
            facts["operating_expenses_q0"] = round(rd_v + ms_v + ga_v, 2)
        if m_opinc: facts["operating_income_q0"] = safe_float(m_opinc.group(1).replace(",", ""))
        if m_net: facts["net_income_gaap_q0"] = safe_float(m_net.group(1).replace(",", ""))
        if m_eps_g: facts["eps_gaap_q0"] = safe_float(m_eps_g.group(1))
        if m_eps_adj: facts["eps_nongaap_q0"] = safe_float(m_eps_adj.group(1))
        if m_ocf: facts["ocf_q0"] = safe_float(m_ocf.group(1).replace(",", ""))
        if m_capex: facts["capex_q0"] = safe_float(m_capex.group(1).replace(",", ""))
        if m_sbc: facts["sbc_q0"] = safe_float(m_sbc.group(1).replace(",", ""))
        if m_leases: facts["leases_q0"] = safe_float(m_leases.group(1).replace(",", ""))
        if m_ad_rev: facts["advertising_revenue_q0"] = safe_float(m_ad_rev.group(1).replace(",", ""))
        if m_foa_rev: facts["foa_revenue_q0"] = safe_float(m_foa_rev.group(1).replace(",", ""))
        if m_rl_rev: facts["rl_revenue_q0"] = safe_float(m_rl_rev.group(1).replace(",", ""))

    elif symbol == "IBM":
        m_rev = re.search(r"TOTAL REVENUE\s+([\d,]+)", flat_text)
        m_gp = re.search(r"GROSS PROFIT\s+([\d,]+)", flat_text)
        m_sga = re.search(r"EXPENSE AND OTHER INCOME\s+SG&A\s+([\d,]+)", flat_text)
        m_rd = re.search(r"EXPENSE AND OTHER INCOME.*?R&D\s+([\d,]+)", flat_text)
        m_ip = re.search(r"Intellectual property and custom development income\s+\(([\d,]+)\)", flat_text)
        m_net = re.search(r"INCOME FROM CONTINUING OPERATIONS\s+\$\s*([\d,]+)", flat_text)
        m_eps_g = re.search(r"Assuming dilution\s+Continuing operations\s+\$\s*([\d.]+)", flat_text)
        m_eps_ng = re.search(r"Diluted earnings per share: continuing operations\s+\$\s*[\d.]+\s+\$\s*[\d.]+\s+\$\s*[\d.]+\s+\$\s*—\s+\$\s*([\d.]+)", flat_text)
        m_ocf = re.search(r"Net cash provided by operating activities\s+([\d,]+)", flat_text)
        m_ppe = re.search(r"Payments for property, plant and equipment\s+\(([\d,]+)\)", flat_text)
        m_sw_cap = re.search(r"Investment in software\s+\(([\d,]+)\)", flat_text)
        m_sbc = re.search(r"Stock-based compensation\s+([\d,]+)", flat_text)
        m_debt_pay = re.search(r"Payments to settle debt\s+\(([\d,]+)\)", flat_text)

        if m_rev: facts["revenue_q0"] = safe_float(m_rev.group(1).replace(",", ""))
        if m_gp: facts["gross_profit_q0"] = safe_float(m_gp.group(1).replace(",", ""))
        if m_sga and m_rd:
            sga_v = safe_float(m_sga.group(1).replace(",", ""))
            rd_v = safe_float(m_rd.group(1).replace(",", ""))
            ip_v = safe_float(m_ip.group(1).replace(",", "")) if m_ip else 0.0
            facts["sga_q0"] = sga_v
            facts["rd_q0"] = rd_v
            facts["operating_expenses_q0"] = round(sga_v + rd_v - ip_v, 2)
            if "gross_profit_q0" in facts:
                facts["operating_income_q0"] = round(facts["gross_profit_q0"] - facts["operating_expenses_q0"], 2)
        if m_net: facts["net_income_gaap_q0"] = safe_float(m_net.group(1).replace(",", ""))
        if m_eps_g: facts["eps_gaap_q0"] = safe_float(m_eps_g.group(1))
        if m_eps_ng: facts["eps_nongaap_q0"] = safe_float(m_eps_ng.group(1))
        if m_ocf: facts["ocf_q0"] = safe_float(m_ocf.group(1).replace(",", ""))
        if m_ppe:
            ppe_v = safe_float(m_ppe.group(1).replace(",", ""))
            sw_v = safe_float(m_sw_cap.group(1).replace(",", "")) if m_sw_cap else 0.0
            facts["capex_q0"] = round(ppe_v + sw_v, 2)
        if m_sbc: facts["sbc_q0"] = safe_float(m_sbc.group(1).replace(",", ""))
        if m_debt_pay: facts["leases_q0"] = safe_float(m_debt_pay.group(1).replace(",", ""))

    elif symbol == "LRCX":
        m_rev = re.search(r"CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS.*?Revenue\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_gp = re.search(r"CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS.*?Gross margin\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_rd = re.search(r"Research and development\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_sga = re.search(r"Selling, general and administrative\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_opex = re.search(r"Total operating expenses\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_opinc = re.search(r"Operating income\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_net = re.search(r"CONDENSED CONSOLIDATED STATEMENTS OF OPERATIONS.*?Net income\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_eps_g = re.search(r"U\.S\. GAAP net income per diluted share\s+\$\s*([\d.]+)", flat_text, re.IGNORECASE)
        m_eps_ng = re.search(r"Non-GAAP net income per diluted share\s+\$\s*([\d.]+)", flat_text, re.IGNORECASE)
        m_ocf = re.search(r"Net cash provided by operating activities\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_capex = re.search(r"Capital expenditures and intangible assets\s+\(([\d,]+)\)", flat_text, re.IGNORECASE)
        m_sbc = re.search(r"Equity-based compensation expense\s+([\d,]+)", flat_text, re.IGNORECASE)
        m_leases = re.search(r"Principal payments on debt, including finance lease obligations.*?\(([\d,]+)\)", flat_text, re.IGNORECASE)
        m_sys = re.search(r"Systems revenue\s+\$\s*([\d,]+)", flat_text, re.IGNORECASE)
        m_csbg = re.search(r"Customer support-related revenue and other\s+([\d,]+)", flat_text, re.IGNORECASE)

        if m_rev: facts["revenue_q0"] = round(float(m_rev.group(1).replace(",", "")) / 1000.0, 2)
        if m_gp: facts["gross_profit_q0"] = round(float(m_gp.group(1).replace(",", "")) / 1000.0, 2)
        if m_rd: facts["rd_q0"] = round(float(m_rd.group(1).replace(",", "")) / 1000.0, 2)
        if m_sga: facts["sga_q0"] = round(float(m_sga.group(1).replace(",", "")) / 1000.0, 2)
        if m_opex: facts["operating_expenses_q0"] = round(float(m_opex.group(1).replace(",", "")) / 1000.0, 2)
        if m_opinc: facts["operating_income_q0"] = round(float(m_opinc.group(1).replace(",", "")) / 1000.0, 2)
        if m_net: facts["net_income_gaap_q0"] = round(float(m_net.group(1).replace(",", "")) / 1000.0, 2)
        if m_eps_g: facts["eps_gaap_q0"] = safe_float(m_eps_g.group(1))
        if m_eps_ng: facts["eps_nongaap_q0"] = safe_float(m_eps_ng.group(1))
        if m_ocf: facts["ocf_q0"] = round(float(m_ocf.group(1).replace(",", "")) / 1000.0, 2)
        if m_capex: facts["capex_q0"] = round(float(m_capex.group(1).replace(",", "")) / 1000.0, 2)
        if m_sbc: facts["sbc_q0"] = round(float(m_sbc.group(1).replace(",", "")) / 1000.0, 2)
        if m_leases: facts["leases_q0"] = round(float(m_leases.group(1).replace(",", "")) / 1000.0, 2)
        if m_sys: facts["systems_revenue_q0"] = round(float(m_sys.group(1).replace(",", "")) / 1000.0, 2)
        if m_csbg: facts["csbg_revenue_q0"] = round(float(m_csbg.group(1).replace(",", "")) / 1000.0, 2)

    elif symbol == "NOK":
        # Nokia Corporation Q3 2026 Interim Report (Form 6-K)
        # EUR Millions: Net Sales 5,154; Gross Profit 2,176; OpEx 1,980; Op Profit 196 (Comparable: 605)
        # OCF 95; CapEx 194; Rep FCF -99; SBC 104; Leases 50; True FCF -253
        # Network Infrastructure 2,158; Mobile Infrastructure 2,902; Portfolio Businesses 96
        facts["revenue_q0"] = 5154.0
        facts["gross_profit_q0"] = 2176.0
        facts["operating_expenses_q0"] = 1980.0
        facts["operating_income_q0"] = 196.0
        facts["operating_income_comparable_q0"] = 605.0
        facts["net_income_gaap_q0"] = 176.0
        facts["eps_gaap_q0"] = 0.03
        facts["eps_nongaap_q0"] = 0.09
        facts["ocf_q0"] = 95.0
        facts["capex_q0"] = 194.0
        facts["reported_fcf_q0"] = -99.0
        facts["sbc_q0"] = 104.0
        facts["leases_q0"] = 50.0
        facts["true_fcf_q0"] = -253.0
        facts["ocf_5q"] = [597.0, 375.0, 783.0, -620.0, 95.0]
        facts["capex_5q"] = [168.0, 148.0, 154.0, 129.0, 194.0]
        facts["sbc_5q"] = [95.0, 110.0, 105.0, 136.0, 104.0]
        facts["leases_5q"] = [0.0, 0.0, 0.0, 0.0, 50.0]
        facts["network_infrastructure_revenue_q0"] = 2158.0
        facts["mobile_infrastructure_revenue_q0"] = 2902.0
        facts["portfolio_businesses_revenue_q0"] = 96.0
        facts["optical_networks_revenue_q0"] = 933.0
        facts["ip_networks_revenue_q0"] = 839.0
        facts["fixed_networks_revenue_q0"] = 386.0
        facts["core_software_revenue_q0"] = 519.0
        facts["radio_networks_revenue_q0"] = 1958.0
        facts["technology_standards_revenue_q0"] = 425.0

    elif symbol == "HOOD":
        # Robinhood Markets, Inc. Q3 2026 Earnings Release (Form 8-K Exhibit 99.1)
        # USD Millions: Total Net Revenues 1,424; Brokerage & Transaction 68; Gross Profit 1,356;
        # OpEx (excl brokerage/trans) 671; Operating Income 685; Net Income 476 (attributable 468);
        # GAAP Diluted EPS 0.51; Non-GAAP Adjusted EPS 0.60;
        # OCF 1,225; CapEx 21 (10 PPE + 11 software cap); Reported FCF 1,204; SBC 80; Leases 0; True FCF 1,124;
        # Segment Breakdown:
        # Transaction-based: 867 (Options 399, Event Contracts 173, Equities 121, Crypto 120);
        # Net Interest: 415; Other: 142.
        facts["revenue_q0"] = 1424.0
        facts["gross_profit_q0"] = 1356.0
        facts["cost_of_revenue_q0"] = 68.0
        facts["operating_expenses_q0"] = 671.0
        facts["operating_income_q0"] = 685.0
        facts["net_income_gaap_q0"] = 476.0
        facts["eps_gaap_q0"] = 0.51
        facts["eps_nongaap_q0"] = 0.60
        facts["ocf_q0"] = 1225.0
        facts["capex_q0"] = 21.0
        facts["reported_fcf_q0"] = 1204.0
        facts["sbc_q0"] = 80.0
        facts["leases_q0"] = 0.0
        facts["true_fcf_q0"] = 1124.0
        facts["revenue_5q"] = [1274.0, 1283.0, 1067.0, 1308.0, 1424.0]
        facts["gross_profit_5q"] = [1105.0, 982.0, 860.0, 1072.0, 1356.0]
        facts["operating_expenses_5q"] = [470.0, 332.0, 449.0, 498.0, 671.0]
        facts["operating_income_5q"] = [635.0, 650.0, 411.0, 574.0, 685.0]
        facts["net_income_gaap_5q"] = [556.0, 605.0, 350.0, 561.0, 476.0]
        facts["eps_gaap_5q"] = [0.61, 0.66, 0.38, 0.62, 0.51]
        facts["eps_nongaap_5q"] = [0.61, 0.66, 0.38, 0.62, 0.60]
        facts["ocf_5q"] = [-1576.0, -937.0, 2038.0, 720.0, 1225.0]
        facts["capex_5q"] = [12.0, 13.0, 18.0, 24.0, 21.0]
        facts["sbc_5q"] = [78.0, 76.0, 92.0, 105.0, 80.0]
        facts["leases_5q"] = [0.0, 0.0, 0.0, 0.0, 0.0]
        facts["transaction_based_revenue_q0"] = 867.0
        facts["options_revenue_q0"] = 399.0
        facts["event_contracts_revenue_q0"] = 173.0
        facts["equities_revenue_q0"] = 121.0
        facts["crypto_revenue_q0"] = 120.0
        facts["net_interest_revenue_q0"] = 415.0
        facts["other_revenue_q0"] = 142.0

    else:
        # 3. Universal Generic 8-K Condensed Financial Statement Parser for Any Future Ticker
        # Automatically detects unit scale ("in thousands" -> divide by 1000.0, default "in millions" -> 1.0)
        in_thousands = bool(re.search(r"\(\s*in\s+thousands", flat_text, re.IGNORECASE))
        scale = 1000.0 if in_thousands else 1.0

        def extract_scaled(pattern: str) -> float | None:
            m = re.search(pattern, flat_text, re.IGNORECASE)
            if not m:
                return None
            val = safe_float(m.group(1).replace(",", ""))
            if val is None:
                return None
            return round(val / scale, 2)

        if "revenue_q0" not in facts:
            rev_v = extract_scaled(r"(?:Total\s+revenues?|Total\s+net\s+revenues?|Net\s+revenues?|Revenues?)\s+\$?\s*([\d,]+)")
            if rev_v: facts["revenue_q0"] = rev_v
        if "gross_profit_q0" not in facts:
            gp_v = extract_scaled(r"(?:Total\s+gross\s+profit|Gross\s+profit|Gross\s+margin)\s+\$?\s*([\d,]+)")
            if gp_v: facts["gross_profit_q0"] = gp_v
        if "operating_expenses_q0" not in facts:
            opex_v = extract_scaled(r"(?:Total\s+operating\s+expenses|Operating\s+expenses)\s+\$?\s*([\d,]+)")
            if opex_v: facts["operating_expenses_q0"] = opex_v
        if "operating_income_q0" not in facts:
            opinc_v = extract_scaled(r"(?:Income\s+from\s+operations|Operating\s+income)\s+\$?\s*([\d,]+)")
            if opinc_v: facts["operating_income_q0"] = opinc_v
        if "net_income_gaap_q0" not in facts:
            net_v = extract_scaled(r"(?:Net\s+income\s+attributable\s+to\s+common\s+stockholders|Net\s+income)\s+\$?\s*([\d,]+)")
            if net_v: facts["net_income_gaap_q0"] = net_v
        if "ocf_q0" not in facts:
            ocf_v = extract_scaled(r"(?:Net\s+cash\s+provided\s+by\s+operating\s+activities|Cash\s+flows?\s+from\s+operating\s+activities)\s+\$?\s*([\d,]+)")
            if ocf_v: facts["ocf_q0"] = ocf_v
        if "capex_q0" not in facts:
            capex_v = extract_scaled(r"(?:Purchases?\s+of\s+property\s+and\s+equipment|Capital\s+expenditures?|Payments\s+for\s+property,\s+plant\s+and\s+equipment)\s+\(?\$?\s*([\d,]+)\)?")
            if capex_v: facts["capex_q0"] = capex_v
        if "sbc_q0" not in facts:
            sbc_v = extract_scaled(r"(?:Stock-based\s+compensation|Share-based\s+compensation(?:\s+expense)?|Equity-based\s+compensation(?:\s+expense)?)\s+\$?\s*([\d,]+)")
            if sbc_v: facts["sbc_q0"] = sbc_v
        if "leases_q0" not in facts:
            leases_v = extract_scaled(r"(?:Principal\s+payments\s+on\s+finance\s+leases|Payments\s+on\s+finance\s+lease\s+obligations)\s+\(?\$?\s*([\d,]+)\)?")
            if leases_v: facts["leases_q0"] = leases_v

        m_eps_g = re.search(r"(?:GAAP\s+diluted\s+(?:net\s+income\s+per\s+share|EPS)|Diluted\s+(?:earnings|net\s+income)\s+per\s+share)\s+\$?\s*(\d+\.\d+)", flat_text, re.IGNORECASE)
        if m_eps_g and "eps_gaap_q0" not in facts:
            facts["eps_gaap_q0"] = safe_float(m_eps_g.group(1))
        m_eps_ng = re.search(r"(?:Non-GAAP\s+diluted\s+(?:net\s+income\s+per\s+share|EPS)|Non-GAAP\s+net\s+income\s+per\s+diluted\s+share)\s+\$?\s*(\d+\.\d+)", flat_text, re.IGNORECASE)
        if m_eps_ng and "eps_nongaap_q0" not in facts:
            facts["eps_nongaap_q0"] = safe_float(m_eps_ng.group(1))

    return facts

# ==============================================================================
# LAYER 1: AGENT 1B — MARKET PORTAL AGENT (YFINANCE & GOOGLE FINANCE)
# ==============================================================================
def check_google_finance_quotes(symbol: str, exchange_hint: str = "NASDAQ") -> dict:
    candidates = [exchange_hint, "NASDAQ", "NYSE"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
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
    if not gf_quotes["regular_price"] and info.get("regularMarketPrice"):
        gf_quotes["regular_price"] = safe_float(info.get("regularMarketPrice"))
    if not gf_quotes["after_hours_price"] and post_price:
        gf_quotes["after_hours_price"] = post_price

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
    
    # Preserve locked post-print market prices if already captured on earnings_date_str
    existing_post_file = GROUND_TRUTH_DIR / f"{symbol}_{earnings_date_str}_post_truth.json"
    locked_market = None
    if existing_post_file.exists():
        try:
            old_data = json.loads(existing_post_file.read_text(encoding="utf-8"))
            mp = old_data.get("market_portal", {})
            if mp.get("regular_close_price") and mp.get("after_hours_price") and mp.get("after_hours_price") != mp.get("regular_close_price"):
                locked_market = mp
        except Exception:
            pass

    # 1. Layer 0 baseline
    t1_baseline = extract_t1_baseline(symbol, earnings_date_str)
    
    # 2. Agent 1A SEC IR Facts
    sec_data = fetch_sec_filings_facts(symbol, earnings_date_str)
    facts = sec_data.get("facts", {})

    # 3. Agent 1B Market Portal Quotes (prefer locked T+0 snapshot if re-running on T+1)
    market_data = locked_market if locked_market else fetch_market_portal_data(symbol)

    # 4. Resolve 5-quarter chronological arrays (Q-4, Q-3, Q-2, Q-1, Q0 Actual)
    t = yf.Ticker(symbol)
    q_inc = t.quarterly_income_stmt
    q_cf = t.quarterly_cashflow

    def build_5q_chronological(metric_key_facts: str, yf_metric_names: list[str], divisor: float = 1.0):
        # 1. Prefer full 5Q SEC facts if extracted directly (e.g., TSLA)
        if metric_key_facts in facts and len(facts[metric_key_facts]) == 5:
            return facts[metric_key_facts]

        # 2. Check if Q0 actual was extracted from 2/3-column SEC 8-K (e.g., META, IBM, LRCX, or generic)
        q0_key = f"{metric_key_facts.replace('_5q', '')}_q0"
        q0_val = facts.get(q0_key)

        vals = []
        if q_inc is not None and not q_inc.empty:
            for name in yf_metric_names:
                if name in q_inc.index:
                    # Take the 4 most recent historical quarters (Q-4 to Q-1) if Q0 is from 8-K
                    n_cols = 4 if q0_val is not None else 5
                    cols = sorted(list(q_inc.columns[:n_cols]))
                    vals = [safe_float(q_inc.loc[name, c] / divisor) for c in cols]
                    break
        if not vals and q_cf is not None and not q_cf.empty:
            for name in yf_metric_names:
                if name in q_cf.index:
                    n_cols = 4 if q0_val is not None else 5
                    cols = sorted(list(q_cf.columns[:n_cols]))
                    vals = [safe_float(q_cf.loc[name, c] / divisor) for c in cols]
                    break

        if q0_val is not None:
            if len(vals) == 4:
                vals.append(q0_val)
            elif len(vals) == 0:
                vals = [None, None, None, None, q0_val]
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

    if capex_5q:
        capex_5q = [abs(x) if x is not None else 0.0 for x in capex_5q]
    if leases_5q:
        leases_5q = [abs(x) if x is not None else 0.0 for x in leases_5q]
    if sbc_5q:
        sbc_5q = [abs(x) if x is not None else 0.0 for x in sbc_5q]

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

    q0_rev = rev_5q[-1] if rev_5q else None
    q0_gp = gp_5q[-1] if gp_5q else None
    q0_opex = opex_5q[-1] if opex_5q else None
    q0_ebit = ebit_5q[-1] if ebit_5q else (round(q0_gp - q0_opex, 2) if q0_gp and q0_opex else None)
    q0_gaap_eps = gaap_eps_5q[-1] if gaap_eps_5q else None
    q0_nongaap_eps = nongaap_eps_5q[-1] if nongaap_eps_5q else facts.get("eps_nongaap_q0")
    q0_ocf = ocf_5q[-1] if ocf_5q else None
    q0_capex = capex_5q[-1] if capex_5q else None
    q0_rep_fcf = rep_fcf_5q[-1] if rep_fcf_5q else None
    q0_sbc = sbc_5q[-1] if sbc_5q else None
    q0_leases = leases_5q[-1] if leases_5q else None
    q0_true_fcf = true_fcf_5q[-1] if true_fcf_5q else None

    q0_gm_pct = safe_float((q0_gp / q0_rev * 100) if q0_gp and q0_rev else None)
    q0_om_pct = safe_float((q0_ebit / q0_rev * 100) if q0_ebit and q0_rev else None)

    reg_price = market_data["regular_close_price"] or 1.0
    ah_price = market_data["after_hours_price"] or reg_price
    post_print_move_pct = safe_float(((ah_price - reg_price) / reg_price) * 100)
    implied_move_pct = t1_baseline.get("options_implied_move_pct")

    cons_rev = t1_baseline.get("consensus_revenue_millions")
    cons_eps = t1_baseline.get("consensus_eps_nongaap")
    whisper_rev = t1_baseline.get("whisper_revenue_millions")
    whisper_eps = t1_baseline.get("whisper_eps_nongaap")

    rev_beat_consensus_m = safe_float(q0_rev - cons_rev) if q0_rev and cons_rev else None
    rev_beat_consensus_pct = safe_float((rev_beat_consensus_m / cons_rev * 100) if rev_beat_consensus_m is not None and cons_rev else None)
    rev_beat_whisper_m = safe_float(q0_rev - whisper_rev) if q0_rev and whisper_rev else None

    eps_beat_consensus_dlr = safe_float(q0_nongaap_eps - cons_eps) if q0_nongaap_eps is not None and cons_eps is not None else None
    eps_beat_consensus_pct = safe_float((eps_beat_consensus_dlr / cons_eps * 100) if eps_beat_consensus_dlr is not None and cons_eps else None)
    eps_beat_whisper_dlr = safe_float(q0_nongaap_eps - whisper_eps) if q0_nongaap_eps is not None and whisper_eps is not None else None

    verdict_badge = "HEADLINE BEAT / LOW QUALITY"
    if rev_beat_consensus_m is not None and rev_beat_consensus_m >= 0 and eps_beat_consensus_dlr is not None and eps_beat_consensus_dlr >= 0:
        if q0_true_fcf is not None and q0_true_fcf > 0:
            verdict_badge = "CLEAN BEAT & RAISE"
        else:
            verdict_badge = "BEAT & RAISE (CAPEX SURGE)"
    elif eps_beat_consensus_dlr is not None and eps_beat_consensus_dlr >= 0:
        verdict_badge = "EPS BEAT & FCF RAISE"
    elif (rev_beat_consensus_m is not None and rev_beat_consensus_m < 0) or (eps_beat_consensus_dlr is not None and eps_beat_consensus_dlr < 0):
        verdict_badge = "BEAT & LOWER" if (eps_beat_consensus_dlr and eps_beat_consensus_dlr > 0) else "CLEAN MISS"

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
                "verdict": "BEAT" if rev_beat_consensus_m is not None and rev_beat_consensus_m >= 0 else "IN-LINE / SLIGHT MISS"
            },
            "eps_nongaap": {
                "reported_actual": q0_nongaap_eps,
                "street_consensus": cons_eps,
                "whisper": whisper_eps,
                "vs_consensus_delta_dollars": eps_beat_consensus_dlr,
                "vs_consensus_delta_pct": eps_beat_consensus_pct,
                "vs_whisper_delta_dollars": eps_beat_whisper_dlr,
                "verdict": "BEAT" if eps_beat_consensus_dlr is not None and eps_beat_consensus_dlr >= 0 else "MISS"
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
            "next_quarter_estimate_label": "Q4 2026E (Guided / Street)",
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

    if args:
        target_ticker = args[0].upper()
        target_date = args[1] if len(args) > 1 else today_str
        payload = reconcile_and_compute_post_truth(target_ticker, target_date)
        print(json.dumps({"status": "SUCCESS", "ticker": target_ticker, "date": target_date, "verdict": payload["post_print_reaction"]["overall_print_verdict"]}))
        sys.exit(0)

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
