"""
Perplexity Discover-Style AI Financial & Portfolio News Portal Builder
Complements tickers.txt and links directly to T+0 Post-Earnings & T-1 Pre-Earnings Tearsheets.
- Section 1: Top News Impacting Financial Markets (Bento tiles generated from ground truth + agent bus)
- Section 2: Portfolio News & Post-Earnings Intelligence (one tile per ticker's latest published tearsheet)
- Click Tile -> Opens Perplexity Discover-style Detailed AI Report Modal (<dialog closedby="any">)
- Click Stock / Ticker -> Navigates to its latest tearsheet (watchlist tickers filter Portfolio News instead)
- Hover Stock / Ticker -> Quick Pop-Up Summary Hovercard (popover="hint" + interestfor)
Every figure is resolved through news_facts.Ledger and re-verified by validate_news_portal.py (AGENTS.md Rule 2).
"""

import html
import json
import math
import re
from datetime import datetime, time as dtime
from pathlib import Path
from zoneinfo import ZoneInfo

from news_facts import (Ledger, band_side, exhibit_release_time_et, filing_form, flag_from_basis, fmt_date_short, format_value, is_number,
                        load_json, reporting_currency, resolve)

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
POST_BUS_DIR = BASE_DIR / "post_agent_bus"
PRE_BUS_DIR = BASE_DIR / "pre_agent_bus"
DRAFTS_DIR = BASE_DIR / "drafts"
AUDIT_DIR = BASE_DIR / "audit_logs"
TICKERS_FILE = BASE_DIR / "tickers.txt"

ET = ZoneInfo("America/New_York")
TICKER_RE = r"[A-Z0-9.\-]+"

# Theme membership is editorial configuration (which portfolio names belong together), never numbers.
# A theme tile only renders when at least one member has a published T+0 / T-1 tearsheet.
MARKET_THEMES = [
    {"id": "mkt-ai-platforms", "category": "AI Platforms & Hyperscaler CapEx", "color": "emerald",
     "badge": "MEGA-CAP AI • CAPEX & MONETIZATION",
     "tickers": ["META", "GOOGL", "GOOG", "AMZN", "ORCL", "CRWV", "PLTR", "AI", "SOUN", "U"]},
    {"id": "mkt-semis-wfe", "category": "Semiconductors & WFE Supply Chain", "color": "blue",
     "badge": "SECTOR • SEMICONDUCTORS",
     "tickers": ["LRCX", "TSM", "NVDA", "AMD", "AVGO", "MRVL", "MU", "INTC", "QCOM", "CRDO", "RGTI"]},
    {"id": "mkt-networks-power", "category": "Networking, Optical & Data-Center Power", "color": "purple",
     "badge": "AI INFRASTRUCTURE • NETWORKS & POWER",
     "tickers": ["NOK", "ANET", "CIEN", "VRT", "NVT", "CBRS"]},
    {"id": "mkt-enterprise-software", "category": "Enterprise Software & Cybersecurity", "color": "purple",
     "badge": "SOFTWARE & CLOUD • ENTERPRISE AI",
     "tickers": ["IBM", "NOW", "FTNT", "CRWD", "PANW", "NET", "DDOG", "MDB", "ESTC", "GTLB"]},
    {"id": "mkt-physical-ai", "category": "Autonomy, EVs & Physical AI", "color": "emerald",
     "badge": "PHYSICAL AI & ENERGY • AUTONOMY",
     "tickers": ["TSLA", "AUR", "RIVN", "AEVA", "LIDR", "UBER", "HYZN", "PLUG", "SYM", "XMTR", "NKE"]},
    {"id": "mkt-fintech-crypto", "category": "Fintech, Crypto & Capital Markets", "color": "blue",
     "badge": "FINTECH & DIGITAL ASSETS",
     "tickers": ["HOOD", "COIN", "IBIT", "FISV", "CLSK"]},
    {"id": "mkt-health-genomics", "category": "MedTech, Genomics & Biotech", "color": "amber",
     "badge": "HEALTHCARE • GENOMICS & ROBOTICS",
     "tickers": ["ISRG", "ILMN", "PACB", "TXG", "CRSP", "EDIT", "TEM", "GUTS", "MSPR"]},
]
OTHER_THEME = {"id": "mkt-other-catalysts", "category": "Other Portfolio Catalysts", "color": "amber",
               "badge": "PORTFOLIO • OTHER PRINTS", "tickers": []}


def load_portfolio_tickers() -> list[str]:
    if not TICKERS_FILE.exists():
        return []
    lines = TICKERS_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()
    tickers = []
    for line in lines:
        t = line.strip().upper()
        if t and re.match(rf"^{TICKER_RE}$", t) and t not in tickers:
            tickers.append(t)
    return tickers


def _rel(path: Path) -> str:
    return path.relative_to(BASE_DIR).as_posix()


def _esc(text) -> str:
    return html.escape(str(text)) if text is not None else ""


def _fmt(val, fmt: str, ccy: str = "$") -> str | None:
    return format_value(val, fmt, ccy) if is_number(val) else None


def _trim(text: str, limit: int = 260) -> str:
    if not text or len(text) <= limit:
        return text or ""
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def _short_name(name: str) -> str:
    out = re.sub(r",?\s+(Inc\.?|Incorporated|Corporation|Corp\.?|Holdings,? Inc\.?|Holdings|Oyj|plc|N\.V\.|Ltd\.?|Limited|Co\.,? Ltd\.?|Company|Co\.?)$", "", name or "").strip()
    out = re.sub(r",?\s+(Inc\.?|Corporation|Holdings)$", "", out).strip()
    return out or name


def _timing_short(hint) -> str:
    h = hint.upper() if isinstance(hint, str) else ""
    if h.startswith("AMC"):
        return "AMC"
    if h.startswith("BMO"):
        return "BMO"
    return "time TBC"


def _plural(n, one: str, many: str) -> str:
    return one if str(n) == "1" else many


_VERDICT_WORDS = {"EPS": "EPS", "FCF": "FCF", "GAAP": "GAAP", "AI": "AI", "AH": "AH", "SBC": "SBC", "OCF": "OCF", "CAPEX": "CapEx"}


def _title_verdict(verdict: str) -> str:
    """'BEAT & RAISE (CAPEX SURGE)' -> 'Beat & Raise (CapEx Surge)'; finance acronyms stay upper-case."""
    return re.sub(r"[A-Za-z]+", lambda m: _VERDICT_WORDS.get(m.group(0).upper(), m.group(0).capitalize()),
                  (verdict or "").replace("_", " "))


_TIMING_RANK = {"BMO": 0, "time TBC": 1, "AMC": 2}


def _event_key(entry: dict) -> tuple:
    """Chronological order of earnings events: date, then pre-market before unknown before after-close."""
    return (entry["earnings_date"], _TIMING_RANK.get(_timing_short(entry.get("timing_hint", "")), 1), entry["ticker"])


def release_has_passed(earnings_date: str, timing_hint, now_et: datetime | None = None) -> bool:
    """True once the scheduled release is out (BMO -> 7:00 AM ET; AMC / unknown -> 4:00 PM ET close)."""
    now = (now_et or datetime.now(ET)).astimezone(ET)
    try:
        d = datetime.strptime(earnings_date, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return False
    if d != now.date():
        return d < now.date()
    cutoff = dtime(7, 0) if _timing_short(timing_hint) == "BMO" else dtime(16, 0)
    return now.time() >= cutoff


def _post_publishable(tk: str, d: str) -> bool:
    """
    A T+0 event is featured only when Agent 5 APPROVED it (the same gate stage5 publishes on) and its post truth
    was generated after the scheduled release (a post truth captured before the print is never featured).
    """
    post_rel = f"ground_truth/{tk}_{d}_post_truth.json"
    if not (BASE_DIR / post_rel).exists():
        return False
    if load_json(f"audit_logs/{tk}_{d}_agent5_signoff.json").get("status") != "APPROVED":
        return False
    stamp = load_json(post_rel).get("timestamp_generated")
    if isinstance(stamp, str):
        try:
            generated = datetime.fromisoformat(stamp)
        except ValueError:
            return True
        generated = generated.astimezone(ET)  # naive stamps are the harness machine's local time
        hint = resolve(load_json(f"ground_truth/{tk}_{d}_truth.json"), "schedule_verification.release_timing_hint")
        return release_has_passed(d, hint, generated)
    return True


def _scrape_report_identity(report: Path) -> tuple[str, str]:
    raw = report.read_text(encoding="utf-8", errors="ignore")
    name, sector = "", ""
    m_name = re.search(r'<h1 class="company-name">([^<]+)</h1>', raw)
    if m_name:
        name = html.unescape(m_name.group(1).strip())
    m_sec = re.search(r'<div class="sector-tag">([^<]+)', raw)
    if m_sec:
        sector = html.unescape(m_sec.group(1).split("•")[0].strip())
    return name, sector


def _new_entry(tk: str, portfolio: list[str]) -> dict:
    return {
        "ticker": tk, "in_portfolio": tk in portfolio, "company_name": tk, "sector": "",
        "state": "watchlist", "earnings_date": "", "timing_hint": "",
        "has_post_report": False, "has_pre_report": False,
        "post_report_url": "", "pre_report_url": "", "primary_report_url": "",
        "report_file": "", "files": {}, "currency": "$", "filing_form": "", "session": "",
        "date_unconfirmed": False, "days_since_release": 0,
        "post_truth_pending": False, "hover_summary": {}, "hover_ledger": None,
    }


def discover_ticker_intelligence(link_prefix: str = "published_reports/", now_et: datetime | None = None) -> dict[str, dict]:
    """
    One entry per ticker (tickers.txt + any ticker with a published tearsheet), describing its CURRENT event:
    - state "post": latest T+0 tearsheet is newer than (or same date as) the latest T-1 briefing
    - state "pre_upcoming" / "pre_reported": latest event is a T-1 briefing whose release is ahead / already out
    - state "watchlist": no published tearsheet
    Truth, agent-bus and draft files are matched to that event's date, never mixed across quarters.
    """
    portfolio = load_portfolio_tickers()
    now = now_et or datetime.now(ET)
    t0_files: dict[str, dict[str, Path]] = {}
    t1_files: dict[str, dict[str, Path]] = {}
    if REPORTS_DIR.exists():
        for f in REPORTS_DIR.glob("*.html"):
            m_t0 = re.match(rf"^({TICKER_RE})_T0_POST_(\d{{4}}-\d{{2}}-\d{{2}})\.html$", f.name)
            if m_t0:
                t0_files.setdefault(m_t0.group(1), {})[m_t0.group(2)] = f
                continue
            m_t1 = re.match(rf"^({TICKER_RE})_T1_(\d{{4}}-\d{{2}}-\d{{2}})\.html$", f.name)
            if m_t1:
                t1_files.setdefault(m_t1.group(1), {})[m_t1.group(2)] = f

    intel: dict[str, dict] = {tk: _new_entry(tk, portfolio) for tk in portfolio}
    for tk in sorted(set(t0_files) | set(t1_files)):
        # One malformed truth / bus file must only drop that ticker back to watchlist, never the whole portal
        try:
            _resolve_current_event(intel, tk, portfolio, t0_files, t1_files, link_prefix, now)
        except Exception as exc:
            print(f"[news_portal] skipping {tk}: {type(exc).__name__}: {exc}")
            if tk in portfolio:
                intel[tk] = _new_entry(tk, portfolio)
            else:
                intel.pop(tk, None)

    for tk, entry in intel.items():
        try:
            entry["hover_summary"] = build_hover_summary(entry)
        except Exception as exc:
            print(f"[news_portal] hovercard for {tk} unavailable: {type(exc).__name__}: {exc}")
            entry["hover_summary"] = build_hover_summary({**_new_entry(tk, portfolio), "company_name": entry.get("company_name", tk)})
    return intel


def _resolve_current_event(intel: dict, tk: str, portfolio: list[str], t0_files: dict, t1_files: dict,
                           link_prefix: str, now: datetime):
    t0_date = max((d for d in t0_files.get(tk, {}) if _post_publishable(tk, d)), default="")
    t1_date = max(t1_files.get(tk, {}), default="")
    if not t0_date and not t1_date:
        return
    entry = intel.setdefault(tk, _new_entry(tk, portfolio))
    if t0_date and t0_date >= t1_date:
        d = t0_date
        report = t0_files[tk][d]
        entry["state"] = "post"
        entry["has_post_report"] = True
        entry["post_report_url"] = f"{link_prefix}{report.name}"
        entry["primary_report_url"] = entry["post_report_url"]
        if d in t1_files.get(tk, {}):
            entry["has_pre_report"] = True
            entry["pre_report_url"] = f"{link_prefix}{t1_files[tk][d].name}"
    else:
        d = t1_date
        report = t1_files[tk][d]
        entry["has_pre_report"] = True
        entry["pre_report_url"] = f"{link_prefix}{report.name}"
        entry["primary_report_url"] = entry["pre_report_url"]

    files = {
        "t1_truth": f"ground_truth/{tk}_{d}_truth.json",
        "pre_2a": f"pre_agent_bus/{tk}_{d}_pre_agent2a_kpis.json",
        "pre_2b": f"pre_agent_bus/{tk}_{d}_pre_agent2b_guidance.json",
        "pre_2c": f"pre_agent_bus/{tk}_{d}_pre_agent2c_sentiment.json",
        "pre_draft": f"drafts/{tk}_{d}_draft.json",
    }
    if entry["state"] == "post":
        files.update({
            "post_truth": f"ground_truth/{tk}_{d}_post_truth.json",
            "post_2a": f"post_agent_bus/{tk}_{d}_agent2a_kpis.json",
            "post_2b": f"post_agent_bus/{tk}_{d}_agent2b_transcript.json",
            "post_2c": f"post_agent_bus/{tk}_{d}_agent2c_social.json",
            "post_draft": f"drafts/{tk}_{d}_post_draft.json",
            "exhibit": f"{tk}/exhibit_99_1.txt",
        })
    entry["files"] = {k: v for k, v in files.items() if (BASE_DIR / v).exists()}
    entry["earnings_date"] = d
    entry["report_file"] = _rel(report)

    t1 = load_json(files["t1_truth"])
    hint = resolve(t1, "schedule_verification.release_timing_hint")
    entry["timing_hint"] = hint if isinstance(hint, str) else ""
    flag = resolve(t1, "schedule_verification.confirmation_flag")
    entry["date_unconfirmed"] = isinstance(flag, str) and flag.upper().startswith("UNCONFIRMED")
    if entry["state"] != "post":
        entry["state"] = "pre_reported" if release_has_passed(d, entry["timing_hint"], now) else "pre_upcoming"
        entry["post_truth_pending"] = (GROUND_TRUTH_DIR / f"{tk}_{d}_post_truth.json").exists()
        entry["days_since_release"] = (now.astimezone(ET).date() - datetime.strptime(d, "%Y-%m-%d").date()).days
    # Release session: pre-market prints react in the regular session, after-close prints in after-hours trading
    released = exhibit_release_time_et(tk) if entry["state"] == "post" else None
    if _timing_short(entry["timing_hint"]) == "BMO" or (released and released.strftime("%Y-%m-%d") == d and released.time() < dtime(9, 30)):
        entry["session"] = "BMO"
    else:
        entry["session"] = _timing_short(entry["timing_hint"])

    name, sector = _scrape_report_identity(report)
    company = t1.get("company_name")
    entry["company_name"] = company if isinstance(company, str) and company else (name or tk)
    if isinstance(t1.get("industry"), str) and t1.get("industry"):
        entry["sector"] = " • ".join(x for x in (t1.get("sector"), t1.get("industry")) if isinstance(x, str) and x)
    else:
        entry["sector"] = sector
    entry["currency"] = reporting_currency(tk)
    meta_form = resolve(load_json(entry["files"].get("post_truth", "")), "sec_filing_metadata.form")
    entry["filing_form"] = filing_form(tk, meta_form if isinstance(meta_form, str) else "")


# ---------------------------------------------------------------------------
# Hovercard summaries (mode-specific labels; any missing truth field drops its row)
# ---------------------------------------------------------------------------

def _box(label: str, value: str | None, small: str | None = None, sub: str | None = None):
    return {"label": label, "value": value, "small": small, "sub": sub} if value else None


def build_hover_summary(entry: dict) -> dict:
    """Pop-up summary for one ticker, built from the same ledger-backed facts as the articles (entry['hover_ledger'])."""
    tk, state = entry["ticker"], entry["state"]
    L, S = Ledger(), SourceList()
    entry["hover_ledger"] = L

    F = gather_post_facts(L, entry) if state == "post" else None
    if F:
        reaction_lbl = "Prior Close → Release-Day Close" if F["bmo"] else "Close → After-Hours"
        prices = f"{F['prev_close']} → {F['close']}" if F["bmo"] else (f"{F['close']} → {F['ah']}" if F["close"] and F["ah"] else F["ah"])
        cells = [
            (reaction_lbl, prices, ""),
            ("Print Reaction (Regular Session)" if F["bmo"] else "Print Reaction (After Hours)", F["move"],
             "hc-pos" if is_number(F["move_raw"]) and F["move_raw"] >= 0 else "hc-neg"),
            ("T-1 Implied Band", f"{F['band']} ({F['side']})" if F["band"] and F["side"] else F["band"], ""),
        ]
        boxes = [
            _box(f"{F['q'] or 'Q0'} Revenue vs Street", F["rev"], F["rev_delta"],
                 " • ".join(x for x in (f"Street {F['rev_cons']}" if F["rev_cons"] else "", F["rev_verdict"]) if x)),
            _box(f"{F['eps_kind']} EPS vs Street", F["eps"], F["eps_delta"],
                 " • ".join(x for x in (f"Street {F['eps_cons']}" if F["eps_cons"] else "", F["eps_verdict"]) if x)),
            _box("Gross / Operating Margin", f"{F['gm']} / {F['om']}" if F["gm"] and F["om"] else (F["gm"] or F["om"])),
            _box("True FCF (ex-SBC & Leases)", F["true_fcf"], None,
                 " | ".join(x for x in (f"OCF {F['ocf']}" if F["ocf"] else "", f"CapEx {F['capex']}" if F["capex"] else "") if x)),
        ]
        draft = entry["files"].get("post_draft")
        bull = L.num(draft, "trade_matrix.bull_target_low_num", "price", "$", f"{tk} bull trade target") if draft else None
        bear = L.num(draft, "trade_matrix.bear_target_high_num", "price", "$", f"{tk} bear trade target") if draft else None
        p2c, p2b = entry["files"].get("post_2c"), entry["files"].get("post_2b")
        driver = L.text(p2c, "retail_vs_institutional_reaction.after_hours_movement_driver") if p2c else None
        guide = ""
        g_metric = L.text(p2b, "forward_guidance_reset_matrix_b[0].forward_horizon_and_metric") if p2b else None
        g_new = L.text(p2b, "forward_guidance_reset_matrix_b[0].new_management_guidance") if p2b else None
        if g_new:
            guide = f"{g_metric or 'Forward guide'}: {g_new}"
        return {
            "mode": "POST", "badge": "T+0 POST-EARNINGS FORENSIC", "verdict": print_verdict(L, F),
            "date": f"Reported {F['date']} ({F['session_label']})",
            "cells": [c for c in cells if c[1]], "boxes": [b for b in boxes if b],
            "driver": _trim(driver or "", 320), "driver_src": "Agent 2C social & sell-side pulse",
            "guide": guide, "guide_src": "Agent 2B transcript forensics",
            "footer": ("Bull / Bear Trade Targets (T+0 draft)", f"{bull} / {bear}") if bull and bear else None,
            "cta": f"Click {tk} to open the T+0 post-earnings tearsheet →",
        }

    F = gather_pre_facts(L, entry) if state in ("pre_upcoming", "pre_reported") else None
    if F:
        valuation = " • ".join(x for x in (f"Fwd P/E {F['fwd_pe']}" if F["fwd_pe"] else "",
                                           f"EV/EBITDA {F['ev_ebitda']}" if F["ev_ebitda"] else "") if x)
        cells = [
            ("Stage 1 Spot", F["spot"], ""),
            ("Implied Move", f"{F['band']} ({F['straddle']})" if F["band"] and F["straddle"] else F["band"], ""),
            (f"ATM IV (exp {F['expiry']})" if F["expiry"] else "ATM IV", F["iv"], ""),
        ]
        boxes = [
            _box("Consensus EPS (Q0E)", F["cons_eps"]),
            _box("EPS Beat Rate (Last 4Q)", F["beat_rate"], None, f"Avg 1-day move {F['avg_move']}" if F["avg_move"] else None),
            _box("Street Mean Target", F["mean_pt"], F["upside"], f"{F['analysts']} analysts" if F["analysts"] else None),
            _box("Valuation", valuation or None),
            _box(f"True FCF ({F['fcf_q']})" if F["fcf_q"] else "True FCF", F["true_fcf"], None,
                 " | ".join(x for x in (f"OCF {F['ocf']}" if F["ocf"] else "", f"CapEx {F['capex']}" if F["capex"] else "") if x)),
        ]
        p2c, p2b = entry["files"].get("pre_2c"), entry["files"].get("pre_2b")
        driver = L.text(p2c, "retail_vs_institutional_positioning.institutional_positioning_summary") if p2c else None
        guide = ""
        b_metric = L.text(p2b, "matrix_b_forward_guidance_bogeys[0].forward_metric") if p2b else None
        b_street = L.text(p2b, "matrix_b_forward_guidance_bogeys[0].street_consensus_hurdle") if p2b else None
        b_bull = L.text(p2b, "matrix_b_forward_guidance_bogeys[0].bull_case_bogey") if p2b else None
        if b_street:
            guide = f"{b_metric or 'Forward bogey'}: Street {b_street}" + (f" • Bull {b_bull}" if b_bull else "")
        if state == "pre_reported":
            tail = "NO T+0 TEARSHEET" if F["stale"] else "T+0 TEARSHEET PENDING"
            verdict = f"REPORTED {F['date'].upper()} • {tail}"
        else:
            verdict = f"UPCOMING PRINT • {F['date'].upper()} {F['timing'].upper()}" + (" (DATE UNCONFIRMED)" if F["unconfirmed"] else "")
        return {
            "mode": "PRE", "badge": "T-1 PRE-EARNINGS BRIEFING", "verdict": verdict,
            "date": f"Release {F['when']}",
            "cells": [c for c in cells if c[1]], "boxes": [b for b in boxes if b][:4],
            "driver": _trim(driver or "", 320), "driver_src": "Agent 2C positioning",
            "guide": guide, "guide_src": "Agent 2B guidance bogeys",
            "footer": ("Street PT High / Low", f"{F['pt_high']} / {F['pt_low']}") if F["pt_high"] and F["pt_low"] else None,
            "cta": f"Click {tk} to open the T-1 pre-earnings briefing →",
        }

    return {
        "mode": "WATCHLIST", "badge": "PORTFOLIO WATCHLIST (tickers.txt)",
        "verdict": "NO T-1 / T+0 REPORT YET", "date": "",
        "cells": [], "boxes": [],
        "driver": f"{tk} is on your tickers.txt watchlist. Its T-1 briefing is generated automatically when the Stage 1 calendar scan finds its earnings window.",
        "driver_src": "", "guide": "", "guide_src": "", "footer": None,
        "cta": f"Click {tk} to filter Portfolio News →",
    }


# ---------------------------------------------------------------------------
# Ledger-backed fact gathering shared by Section 1 and Section 2
# ---------------------------------------------------------------------------

class SourceList:
    """Numbered source cards for one article; only files that exist in the repo can be cited."""

    def __init__(self):
        self.items: list[dict] = []
        self._by_path: dict[str, int] = {}

    def cite(self, path: str | None, name: str, detail: str) -> int | None:
        if not path or not (BASE_DIR / path).exists():
            return None
        if path in self._by_path:
            return self._by_path[path]
        n = len(self.items) + 1
        self.items.append({"id": n, "name": name, "detail": detail, "path": path})
        self._by_path[path] = n
        return n


def _cite(*ids) -> str:
    ids = sorted({i for i in ids if i})
    return f" [{', '.join(str(i) for i in ids)}]" if ids else ""


def _join_clauses(clauses: list[str | None], sep: str = ", ") -> str:
    return sep.join(c for c in clauses if c)


def _join_and(clauses: list[str | None]) -> str:
    """'a, b and c' for prose lists."""
    parts = [c for c in clauses if c]
    if len(parts) <= 1:
        return "".join(parts)
    return ", ".join(parts[:-1]) + " and " + parts[-1]


class Cites:
    """Per-ticker citation specs; a source is only added to the article's list when a sentence cites it."""

    def __init__(self, S: "SourceList", specs: dict[str, tuple[str | None, str, str]]):
        self.S, self.specs = S, specs

    def ref(self, *keys) -> str:
        return _cite(*(self.S.cite(*self.specs[k]) for k in keys if k in self.specs))


def _first_text(L: Ledger, rel: str | None, paths: list[str], label: str = "") -> str | None:
    """First non-empty agent-bus string among schema variants (bus files from different runs use different keys)."""
    for path in paths if rel else []:
        val = L.text(rel, path, label)
        if val:
            return val
    return None


def _rows(rel: str | None, key: str) -> list[int]:
    """Indices of dict rows in an agent-bus array (tolerates strings / missing keys from schema drift)."""
    rows = resolve(load_json(rel), key) if rel else None
    return [i for i, r in enumerate(rows) if isinstance(r, dict)] if isinstance(rows, list) else []


def _paren(*parts) -> str:
    parts = [p for p in parts if p]
    return f" ({', '.join(parts)})" if parts else ""


def gather_post_facts(L: Ledger, entry: dict) -> dict | None:
    tk, ccy = entry["ticker"], entry["currency"]
    pt = entry["files"].get("post_truth")
    if not pt:
        return None
    F = {"tk": tk, "pt": pt, "ccy": ccy, "entry": entry, "bmo": entry.get("session") == "BMO"}
    q_raw = L.text(pt, "stitched_5q_chronological.period_labels[-1]", f"{tk} reported quarter")
    F["q"] = re.sub(r"\s*\(Actual\)\s*$", "", q_raw or "")
    F["prior_q"] = L.text(pt, "t1_baseline.prior_quarter_label", f"{tk} prior quarter")
    F["rev"] = L.num(pt, "beat_miss_scorecard.revenue.reported_actual_millions", "money_m", ccy, f"{tk} revenue")
    F["rev_cons"] = L.num(pt, "beat_miss_scorecard.revenue.street_consensus_millions", "money_m", ccy, f"{tk} revenue consensus")
    F["rev_delta"] = L.num(pt, "beat_miss_scorecard.revenue.vs_consensus_delta_pct", "pct", ccy, f"{tk} revenue surprise")
    F["rev_delta_raw"] = L.raw(pt, "beat_miss_scorecard.revenue.vs_consensus_delta_pct")
    F["rev_verdict"] = L.text(pt, "beat_miss_scorecard.revenue.verdict") or ""
    eps_path = "eps_nongaap" if is_number(resolve(load_json(pt), "beat_miss_scorecard.eps_nongaap.reported_actual")) else "eps_gaap"
    F["eps_verdict_path"] = f"beat_miss_scorecard.{eps_path}.verdict"
    # Stage 1's eps_nongaap is the company's adjusted / ex-items EPS (not every issuer calls it non-GAAP)
    F["eps_kind"] = "Adj." if eps_path == "eps_nongaap" else "GAAP"
    F["eps"] = L.num(pt, f"beat_miss_scorecard.{eps_path}.reported_actual", "eps", ccy, f"{tk} {F['eps_kind']} EPS")
    F["eps_cons"] = L.num(pt, f"beat_miss_scorecard.{eps_path}.street_consensus", "eps", ccy, f"{tk} EPS consensus")
    F["eps_delta"] = L.num(pt, f"beat_miss_scorecard.{eps_path}.vs_consensus_delta_pct", "pct", ccy, f"{tk} EPS surprise")
    F["eps_verdict"] = L.text(pt, F["eps_verdict_path"]) or ""
    F["close"] = L.num(pt, "post_print_reaction.regular_close_price", "price", "$", f"{tk} regular close")
    F["ah"] = L.num(pt, "post_print_reaction.after_hours_price", "price", "$", f"{tk} after-hours price")
    F["band"] = L.num(pt, "post_print_reaction.t1_options_implied_move_pct", "band", "$", f"{tk} T-1 implied move")
    F["band_raw"] = L.raw(pt, "post_print_reaction.t1_options_implied_move_pct")
    F["ah_move"] = L.num(pt, "post_print_reaction.post_print_move_pct", "pct", "$", f"{tk} after-hours move")
    basis = None
    if F["bmo"]:
        # Pre-market print: the reaction is the release-day regular session (prior close -> close), derived from truth prices
        prev_raw = L.raw(pt, "market_portal.previous_close_price")
        close_raw = L.raw(pt, "market_portal.regular_close_price")
        F["prev_close"] = L.num(pt, "market_portal.previous_close_price", "price", "$", f"{tk} prior close")
        F["close"] = L.num(pt, "market_portal.regular_close_price", "price", "$", f"{tk} release-day close")
        ok = is_number(prev_raw) and is_number(close_raw) and prev_raw != 0
        F["move"] = L.derived("pct_change", [close_raw, prev_raw], "pct", "$", f"{tk} release-day move") if ok else None
        F["move_raw"] = (close_raw - prev_raw) / abs(prev_raw) * 100.0 if ok else None
        if is_number(F["move_raw"]) and is_number(F["band_raw"]):
            m, bd = F["move_raw"], F["band_raw"]
            basis = lambda side: {"kind": "abs_vs_band", "move": m, "band": bd, "side": side}
        F["session_label"] = "pre-market"
    else:
        F["prev_close"] = None
        F["move"] = F["ah_move"]
        F["move_raw"] = L.raw(pt, "post_print_reaction.post_print_move_pct")
        basis = lambda side: {"kind": "side_text", "file": pt, "path": "post_print_reaction.move_vs_implied_status",
                              "band_path": "post_print_reaction.t1_options_implied_move_pct", "side": side}
        F["session_label"] = "after the close" if entry.get("session") == "AMC" else "session TBC"
    F["side_basis"] = basis
    F["side"] = ""
    if basis is not None:
        F["side"] = "outside" if flag_from_basis(basis("outside")) else ("inside" if flag_from_basis(basis("inside")) else "")
    F["gm"] = L.num(pt, "beat_miss_scorecard.margins.reported_gross_margin_pct", "pct_plain", ccy, f"{tk} gross margin")
    F["om"] = L.num(pt, "beat_miss_scorecard.margins.reported_operating_margin_pct", "pct_plain", ccy, f"{tk} operating margin")
    for k in ("ocf", "capex", "reported_fcf", "sbc", "finance_leases", "true_fcf"):
        F[k] = L.num(pt, f"forensic_fcf_bridge_q0.{k}", "money_m", ccy, f"{tk} {k.replace('_', ' ')}")
    F["filing_date"] = L.date(pt, "sec_filing_metadata.filing_date", f"{tk} filing date")
    F["date"] = L.file_date(entry["report_file"], entry["earnings_date"], f"{tk} earnings date")
    F["rev_beat"] = F["rev_verdict"] == "BEAT"
    F["eps_beat"] = F["eps_verdict"] == "BEAT"
    p2b = entry["files"].get("post_2b")
    F["guide_action"] = L.text(p2b, "forward_guidance_reset_matrix_b[0].action_badge") if _rows(p2b, "forward_guidance_reset_matrix_b") else None
    return F


def print_verdict(L: Ledger, F: dict) -> str:
    """Factual verdict from the beat/miss scorecard (+ Agent 2B guidance action), not Stage 1's composite label."""
    parts = []
    if F["rev_verdict"]:
        parts.append(f"Revenue {_title_verdict(F['rev_verdict'])}")
    if F["eps_verdict"]:
        parts.append(f"{F['eps_kind']} EPS {_title_verdict(F['eps_verdict'])}")
    action = (F.get("guide_action") or "").upper()
    if action in ("RAISED", "LOWERED", "CUT", "REAFFIRMED", "MAINTAINED", "INITIATED", "WITHDRAWN"):
        parts.append(f"Guide {_title_verdict(action)}")
    return " • ".join(parts) or "Post-Print Audit"


def gather_pre_facts(L: Ledger, entry: dict) -> dict | None:
    tk = entry["ticker"]
    t1 = entry["files"].get("t1_truth")
    if not t1:
        return None
    ccy = entry["currency"]
    F = {"tk": tk, "t1": t1, "entry": entry, "timing": _timing_short(entry["timing_hint"]),
         "unconfirmed": entry.get("date_unconfirmed", False),
         "stale": entry["state"] == "pre_reported" and entry.get("days_since_release", 0) > 5}
    F["date"] = L.file_date(entry["report_file"], entry["earnings_date"], f"{tk} earnings date")
    F["when"] = f"{F['date']} ({F['timing']}{', date unconfirmed' if F['unconfirmed'] else ''})"
    F["spot"] = L.num(t1, "price_validation.yahoo_spot_price", "price", "$", f"{tk} Stage 1 spot")
    F["band"] = L.num(t1, "options_positioning.atm_implied_move_pct", "band", "$", f"{tk} implied move")
    F["band_raw"] = L.raw(t1, "options_positioning.atm_implied_move_pct")
    F["straddle"] = L.num(t1, "options_positioning.atm_straddle_usd", "price", "$", f"{tk} ATM straddle")
    F["iv"] = L.num(t1, "options_positioning.atm_implied_volatility_pct", "pct_plain", "$", f"{tk} ATM IV")
    F["expiry"] = L.date(t1, "options_positioning.expiry_strictly_after_earnings", f"{tk} option expiry")
    expiry_iso = resolve(load_json(t1), "options_positioning.expiry_strictly_after_earnings")
    try:
        F["expiry_days"] = (datetime.strptime(expiry_iso[:10], "%Y-%m-%d") - datetime.strptime(entry["earnings_date"], "%Y-%m-%d")).days
    except (TypeError, ValueError):
        F["expiry_days"] = None
    F["weekly"] = F["expiry_days"] is not None and 0 < F["expiry_days"] <= 7
    F["pcr"] = L.num(t1, "options_positioning.put_call_oi_ratio", "mult", "$", f"{tk} put/call OI")
    F["cons_eps"] = (L.num(t1, "street_consensus_and_targets.yahoo_consensus_eps_q0e", "eps", "$", f"{tk} consensus EPS")
                     or L.num(t1, "schedule_verification.yahoo_consensus_eps", "eps", "$", f"{tk} consensus EPS"))
    F["beat_rate"] = L.num(t1, "historical_earnings_track_record.beat_rate_pct", "pct_plain", "$", f"{tk} EPS beat rate")
    F["avg_move"] = L.num(t1, "historical_earnings_track_record.avg_historical_1d_move_abs_pct", "band", "$", f"{tk} avg 1-day move")
    F["mean_pt"] = L.num(t1, "street_consensus_and_targets.target_mean_price", "price", "$", f"{tk} mean target")
    F["upside"] = L.num(t1, "street_consensus_and_targets.implied_upside_to_mean_pct", "pct", "$", f"{tk} upside to mean")
    F["pt_high"] = L.num(t1, "street_consensus_and_targets.target_high_price", "price", "$", f"{tk} high target")
    F["pt_low"] = L.num(t1, "street_consensus_and_targets.target_low_price", "price", "$", f"{tk} low target")
    F["analysts"] = L.num(t1, "street_consensus_and_targets.analyst_count", "int", "$", f"{tk} analyst count")
    F["fwd_pe"] = L.num(t1, "valuation_and_market.forward_pe", "mult", "$", f"{tk} forward P/E")
    F["ev_ebitda"] = L.num(t1, "valuation_and_market.ev_to_ebitda", "mult", "$", f"{tk} EV/EBITDA")
    F["fcf_period"] = L.text(t1, "forensic_fcf_bridge_latest.period_label", f"{tk} Stage 1 FCF quarter")
    F["fcf_q"] = re.sub(r"\s*\(.*$", "", F["fcf_period"] or "")
    for k in ("ocf", "capex", "reported_fcf", "sbc", "true_fcf"):
        F[k] = L.num(t1, f"forensic_fcf_bridge_latest.{k}", "money_m", ccy, f"{tk} Stage 1 FCF {k.replace('_', ' ')}")
    return F


def cite_post_sources(S: SourceList, entry: dict, F: dict) -> Cites:
    tk, f = entry["ticker"], entry["files"]
    filed = f" • filed {F['filing_date']}" if F.get("filing_date") else ""
    return Cites(S, {
        "exhibit": (f.get("exhibit"), f"SEC Form {entry['filing_form']} Exhibit 99.1 ({tk})", f"{f.get('exhibit', '')}{filed}"),
        "truth": (f.get("post_truth"), f"Stage 1 Post-Print Truth ({tk})", f"{f.get('post_truth', '')} • beat/miss, after-hours reaction, FCF bridge"),
        "p2b": (f.get("post_2b"), f"Agent 2B Transcript Forensics ({tk})", f.get("post_2b", "")),
        "p2c": (f.get("post_2c"), f"Agent 2C Social & Sell-Side Pulse ({tk})", f.get("post_2c", "")),
        "report": (entry.get("report_file"), f"Published T+0 Tearsheet ({tk})", entry.get("report_file", "")),
    })


def cite_pre_sources(S: SourceList, entry: dict) -> Cites:
    tk, f = entry["ticker"], entry["files"]
    return Cites(S, {
        "truth": (f.get("t1_truth"), f"Stage 1 T-1 Truth ({tk})", f"{f.get('t1_truth', '')} • spot, options, consensus, targets"),
        "p2b": (f.get("pre_2b"), f"Agent 2B Guidance & Debates ({tk})", f.get("pre_2b", "")),
        "p2c": (f.get("pre_2c"), f"Agent 2C Positioning ({tk})", f.get("pre_2c", "")),
        "report": (entry.get("report_file"), f"Published T-1 Briefing ({tk})", entry.get("report_file", "")),
    })


def reaction_clause(F: dict) -> str:
    """'moved -3.32% after hours to $373.63 from a $386.47 close' (AMC) or the release-day session move (BMO)."""
    if not F["move"]:
        return ""
    if F["bmo"]:
        out = f"moved {F['move']} in the release-day regular session to {F['close']}"
        out += f" from a {F['prev_close']} prior close" if F["prev_close"] else ""
    else:
        out = f"moved {F['move']} after hours" + (f" to {F['ah']}" if F["ah"] else "") + (f" from a {F['close']} close" if F["close"] else "")
    if F["band"] and F["side"]:
        out += f", {F['side']} the T-1 options-implied {F['band']} band"
    return out


def post_print_sentence(F: dict) -> str:
    tk = F["tk"]
    rev = (f"revenue of {F['rev']}" + (f" vs {F['rev_cons']} Street" if F["rev_cons"] else "") + _paren(F["rev_delta"])) if F["rev"] else None
    eps = (f"{F['eps_kind']} EPS of {F['eps']}" + (f" vs {F['eps_cons']}" if F["eps_cons"] else "") + _paren(F["eps_delta"])) if F["eps"] else None
    head = f"${tk} reported {F['q']} " if F["q"] else f"${tk} reported "
    out = head + _join_and([rev, eps]) + "."
    reaction = reaction_clause(F)
    if reaction:
        out += f" Shares {reaction}."
    if F["bmo"] and F["ah_move"]:
        out += f" After-hours drift: {F['ah_move']}."
    return out


def pre_setup_sentence(F: dict, lead: bool = True) -> str:
    tk = F["tk"]
    if F["entry"]["state"] == "pre_reported":
        tail = "no T+0 forensic tearsheet was published." if F["stale"] else "its T+0 forensic tearsheet is pending."
        out = f"${tk} reported {F['when']}; {tail}"
        if F["spot"] and F["band"]:
            out += f" Stage 1 setup: {F['spot']} spot with a {F['band']} options-implied move."
        return out
    straddle = ""
    if F["straddle"]:
        straddle = f" ({F['straddle']} ATM straddle" + (f", exp {F['expiry']}" if F["expiry"] else "") + ")"
    clauses = [
        f"{F['spot']} spot" if F["spot"] and lead else None,
        f"a {F['band']} options-implied move{straddle}" if F["band"] else None,
        f"consensus EPS of {F['cons_eps']}" if F["cons_eps"] else None,
        f"a {F['mean_pt']} Street mean target{_paren(F['upside'])}" if F["mean_pt"] else None,
    ]
    body = _join_and(clauses)
    return f"${tk} reports {F['when']}" + (f" with {body}." if body else ".")


# ---------------------------------------------------------------------------
# Data-driven tile chart: after-hours move vs options-implied band (or implied band alone for upcoming prints)
# ---------------------------------------------------------------------------

def build_chart_rows(post_facts: list[dict], pre_facts: list[dict]) -> list[dict]:
    rows = []
    for F in post_facts:
        if is_number(F.get("band_raw")):
            window = "release-day session" if F.get("bmo") else "after hours"
            rows.append({"tk": F["tk"], "band": abs(float(F["band_raw"])),
                         "move": float(F["move_raw"]) if is_number(F.get("move_raw")) else None,
                         "outside": F.get("side") == "outside", "move_txt": F.get("move") or "", "band_txt": F.get("band") or "",
                         "alt": f"{F['tk']} {F['move']} {window} vs {F['band']}" if F.get("move") else f"{F['tk']} implied {F['band']}"})
    for F in pre_facts:
        if is_number(F.get("band_raw")):
            rows.append({"tk": F["tk"], "band": abs(float(F["band_raw"])), "move": None, "outside": False,
                         "move_txt": "", "band_txt": F.get("band") or "",
                         "alt": f"{F['tk']} implied {F['band']} ({F['date']})"})
    return rows


def render_move_band_chart_svg(rows: list[dict], max_cols: int = 12, wide: bool = False, pin: str | None = None,
                               extra_class: str = "") -> tuple[str, str]:
    """Returns (svg, alt_text). Columns: dashed band = T-1 implied move, dot = actual print reaction (T+0 only)."""
    if not rows:
        return "", ""
    shown = rows[:max_cols]
    if pin and pin not in {r["tk"] for r in shown}:
        pinned = next((r for r in rows if r["tk"] == pin), None)
        if pinned:
            shown = shown[:-1] + [pinned]
    hidden = len(rows) - len(shown)
    W, H, top, bottom = (840, 150, 22, 116) if wide else (420, 110, 18, 80)
    left, right = 14, W - 14
    mid = (top + bottom) / 2
    peak = max(max(r["band"], abs(r["move"] or 0)) for r in shown) * 1.15 or 1.0
    scale = (bottom - top) / 2 / peak
    step = (right - left) / len(shown)
    bw = min(24.0, step * 0.5)
    has_moves = any(r["move"] is not None for r in shown)
    label_moves = wide or len(shown) <= 6
    label_bands = not has_moves and len(shown) <= 8
    caption = "Print reaction vs. T-1 options-implied band" if has_moves else "Options-implied move into the print"
    parts = [
        f'<text class="ch-cap" x="{left}" y="10">{caption}</text>',
        f'<line class="ch-zero" x1="{left}" x2="{right}" y1="{mid:.1f}" y2="{mid:.1f}"/>',
    ]
    for i, r in enumerate(shown):
        cx = left + step * (i + 0.5)
        bh = r["band"] * scale
        band_cls = "ch-band" if r["move"] is not None else "ch-band ch-band-pre"
        parts.append(f'<rect class="{band_cls}" x="{cx - bw / 2:.1f}" y="{mid - bh:.1f}" width="{bw:.1f}" height="{2 * bh:.1f}" rx="3"/>')
        if r["move"] is not None:
            cy = mid - r["move"] * scale
            tone = "ch-up" if r["move"] > 0 else ("ch-down" if r["move"] < 0 else "ch-flat")
            out_cls = " ch-out" if r["outside"] else ""
            parts.append(f'<line class="ch-stem {tone}" x1="{cx:.1f}" x2="{cx:.1f}" y1="{mid:.1f}" y2="{cy:.1f}"/>')
            parts.append(f'<circle class="ch-dot {tone}{out_cls}" cx="{cx:.1f}" cy="{cy:.1f}" r="4"/>')
            if label_moves and r.get("move_txt"):
                ty = cy - 8 if r["move"] >= 0 else cy + 15
                parts.append(f'<text class="ch-val {tone}" x="{cx + 8:.1f}" y="{ty:.1f}">{_esc(r["move_txt"])}</text>')
        elif label_bands and r.get("band_txt"):
            parts.append(f'<text class="ch-val ch-pre" x="{cx:.1f}" y="{mid - bh - 4:.1f}" text-anchor="middle">{_esc(r["band_txt"])}</text>')
        parts.append(f'<text class="ch-lbl" x="{cx:.1f}" y="{H - 8}" text-anchor="middle">{_esc(r["tk"])}</text>')
    if hidden:
        parts.append(f'<text class="ch-cap" x="{right}" y="10" text-anchor="end">+{hidden} more in brief</text>')
    alt = "; ".join(r["alt"] for r in rows)
    svg = (f'<svg class="tile-art-svg tile-chart {extra_class}" viewBox="0 0 {W} {H}" role="img" aria-label="{_esc(alt)}">'
           f'<title>{_esc(alt)}</title>{"".join(parts)}</svg>')
    return svg, alt


def _read_time(item: dict) -> str:
    text = " ".join([item.get("headline", ""), item.get("summary", "")] + item.get("key_takeaways", []) +
                    [s.get("body", "") for s in item.get("sections", [])])
    words = len(re.sub(r"<[^>]+>", " ", text).split())
    return f"{max(1, math.ceil(words / 200))} min read"


# ---------------------------------------------------------------------------
# Section 1: Top News Impacting the Financial Markets
# ---------------------------------------------------------------------------

def _post_takeaway(F: dict, c: Cites) -> str:
    parts = []
    if F["rev"]:
        parts.append(f"revenue <strong>{F['rev']}</strong>" + (f" vs {F['rev_cons']} Street" if F["rev_cons"] else "")
                     + _paren(F["rev_delta"], _esc(F["rev_verdict"])))
    if F["eps"]:
        parts.append(f"{F['eps_kind']} EPS <strong>{F['eps']}</strong>" + (f" vs {F['eps_cons']}" if F["eps_cons"] else "") + _paren(F["eps_delta"]))
    reaction = reaction_clause(F)
    if reaction:
        parts.append(reaction)
    if F["true_fcf"]:
        parts.append(f"True FCF {F['true_fcf']}")
    label = f"${F['tk']} ({_esc(F['q'])})" if F["q"] else f"${F['tk']}"
    return f"<strong>{label}:</strong> " + "; ".join(parts) + "." + c.ref("truth", "exhibit")


def _pre_takeaway(F: dict, c: Cites) -> str:
    if F["entry"]["state"] == "pre_reported":
        body = f"reported {F['when']}; " + ("no T+0 forensic tearsheet was published" if F["stale"] else "T+0 forensic tearsheet pending")
        if F["spot"] and F["band"]:
            body += f" (Stage 1 setup {F['spot']} spot, {F['band']} implied)"
        return f"<strong>${F['tk']}:</strong> {body}." + c.ref("truth", "report")
    straddle = ""
    if F["straddle"]:
        straddle = f" ({F['straddle']} straddle" + (f", exp {F['expiry']}" if F["expiry"] else "") + ")"
    parts = [
        f"Stage 1 spot {F['spot']}" if F["spot"] else None,
        f"implied move <strong>{F['band']}</strong>{straddle}" if F["band"] else None,
        f"consensus EPS {F['cons_eps']}" if F["cons_eps"] else None,
        f"EPS beat rate {F['beat_rate']} over the last four quarters" if F["beat_rate"] else None,
        f"Street mean target {F['mean_pt']}{_paren(F['upside'])}" if F["mean_pt"] else None,
    ]
    return f"<strong>${F['tk']} ({F['when']}):</strong> " + "; ".join(p for p in parts if p) + "." + c.ref("truth")


def _post_desk_section(L: Ledger, F: dict, c: Cites) -> dict | None:
    p2c = F["entry"]["files"].get("post_2c")
    if not p2c:
        return None
    drv = L.text(p2c, "retail_vs_institutional_reaction.after_hours_movement_driver")
    inst = L.text(p2c, "retail_vs_institutional_reaction.institutional_sentiment_summary")
    if not drv and not inst:
        return None
    body = ""
    if drv:
        body += f"<p><strong>Price-Move Driver:</strong> {_esc(drv)}{c.ref('p2c')}</p>"
    if inst:
        body += f"<p><strong>Institutional Desk Read:</strong> {_esc(inst)}{c.ref('p2c')}</p>"
    return {"heading": f"{_short_name(F['entry']['company_name'])} (${F['tk']}) — Post-Print Desk Synthesis (Agent 2C)", "body": body}


DEBATE_LISTS = ["section_4b_pre_print_debates", "section_4b_institutional_debates"]


def _pre_debate_section(L: Ledger, F: dict, c: Cites) -> dict | None:
    p2b = F["entry"]["files"].get("pre_2b")
    if not p2b:
        return None
    key = next((k for k in DEBATE_LISTS if _rows(p2b, k)), None)
    if not key:
        return None
    base = f"{key}[{_rows(p2b, key)[0]}]"
    title = _first_text(L, p2b, [f"{base}.debate_title", f"{base}.title"])
    if not title:
        return None
    framing = _first_text(L, p2b, [f"{base}.bull_vs_bear_framing"])
    bull = None if framing else _first_text(L, p2b, [f"{base}.bull_thesis", f"{base}.bull_case"])
    bear = None if framing else _first_text(L, p2b, [f"{base}.bear_thesis", f"{base}.bear_case"])
    question = _first_text(L, p2b, [f"{base}.call_focus_question", f"{base}.analyst_focus_question"])
    body = f"<p><strong>{_esc(title)}</strong>{c.ref('p2b')}</p>"
    if framing:
        body += f"<p>{_esc(framing)}</p>"
    if bull:
        body += f"<p><strong>Bull:</strong> {_esc(bull)}</p>"
    if bear:
        body += f"<p><strong>Bear:</strong> {_esc(bear)}</p>"
    if question:
        body += f"<p><em>{_esc(question)}</em></p>"
    return {"heading": f"{_short_name(F['entry']['company_name'])} (${F['tk']}) — Top Pre-Print Debate (Agent 2B)", "body": body}


def _market_item(theme: dict, L: Ledger, S: SourceList, headline: str, summary: str, metrics: list, takeaways: list,
                 sections: list, tickers: list[str], chart_rows: list[dict], published: str, hero: bool = False,
                 pin: str | None = None) -> dict:
    if hero:
        wide_svg, chart_alt = render_move_band_chart_svg(chart_rows, wide=True, pin=pin, extra_class="chart-wide")
        narrow_svg, _ = render_move_band_chart_svg(chart_rows, pin=pin, extra_class="chart-narrow")
        chart_svg = wide_svg + narrow_svg
    else:
        chart_svg, chart_alt = render_move_band_chart_svg(chart_rows, pin=pin)
    item = {
        "id": theme["id"], "category": theme["category"], "is_hero": hero,
        "impact_badge": theme["badge"], "impact_color": theme["color"],
        "published": published, "headline": headline, "summary": summary,
        "tickers": tickers, "chart_svg": chart_svg, "chart_alt": chart_alt, "chart_cols": len(chart_rows),
        "metrics_strip": [m for m in metrics if m and m.get("val")][:3],
        "sources": S.items, "sources_count": len(S.items),
        "key_takeaways": takeaways, "sections": [s for s in sections if s], "ledger": L,
    }
    item["read_time"] = _read_time(item)
    return item


def _latest_date_label(L: Ledger, entries: list[dict], prefix: str) -> str:
    if not entries:
        return ""
    latest = max(entries, key=lambda e: e["earnings_date"])
    return f"{prefix} {L.file_date(latest['report_file'], latest['earnings_date'], 'as-of date')}"


def _safe_facts(gather, L: Ledger, entries: list[dict]) -> list[dict]:
    out = []
    for e in entries:
        try:
            F = gather(L, e)
        except Exception as exc:
            print(f"[news_portal] {e['ticker']} facts unavailable: {type(exc).__name__}: {exc}")
            continue
        if F:
            out.append(F)
    return out


def build_scorecard_item(intel: dict[str, dict]) -> dict | None:
    posts = sorted((e for e in intel.values() if e["state"] == "post"), key=lambda e: (e["earnings_date"], e["ticker"]), reverse=True)
    L, S = Ledger(), SourceList()
    facts = _safe_facts(gather_post_facts, L, posts)
    if not facts:
        return None
    cites = {F["tk"]: cite_post_sources(S, F["entry"], F) for F in facts}
    tickers = [F["tk"] for F in facts]
    n = L.tally(tickers, "T+0 prints in scorecard")
    eps_beats = L.count([{"kind": "text_in", "file": F["pt"], "path": F["eps_verdict_path"], "accept": ["BEAT"]} for F in facts], "EPS beats")
    rev_beats = L.count([{"kind": "text_in", "file": F["pt"], "path": "beat_miss_scorecard.revenue.verdict", "accept": ["BEAT"]} for F in facts],
                        "revenue beats")
    banded = [F for F in facts if F["side_basis"]]
    n_banded = L.tally([F["tk"] for F in banded], "prints with a T-1 implied band")
    inside = L.count([F["side_basis"]("inside") for F in banded], "reactions inside implied band")
    outside = L.count([F["side_basis"]("outside") for F in banded], "reactions outside implied band")
    surprises = [F["rev_delta_raw"] for F in facts if is_number(F.get("rev_delta_raw"))]
    avg_rev = L.derived("mean", surprises, "pct", "$", "average revenue surprise") if surprises else None
    quarters = {F["q"] for F in facts if F["q"]}
    q = quarters.pop() if len(quarters) == 1 else "Earnings Season"
    movers = [F for F in facts if is_number(F.get("move_raw"))]
    big = max(movers, key=lambda F: abs(F["move_raw"])) if movers else None

    headline = f"Portfolio {q} Scorecard: {eps_beats} of {n} Beat EPS, {rev_beats} of {n} Beat Revenue"
    if banded:
        headline += f" — {outside} of {n_banded} Moved Beyond Their Options-Implied Band"
    summary = f"Across {n} published T+0 forensic {_plural(n, 'audit', 'audits')}"
    summary += f", the average revenue surprise vs consensus was {avg_rev}." if avg_rev else "."
    if big and big["move"] and big["band"]:
        window = "in the release-day session" if big["bmo"] else "after hours"
        summary += f" Biggest print reaction: ${big['tk']} at {big['move']} {window} vs a {big['band']} implied band."
    if banded:
        summary += f" {inside} of {n_banded} {_plural(n_banded, 'reaction', 'reactions')} stayed inside the T-1 straddle range."
    metrics = [
        {"label": "EPS Beats", "val": f"{eps_beats} / {n}", "tone": "bull"},
        {"label": "Avg Revenue Surprise", "val": avg_rev, "tone": "bull" if surprises and sum(surprises) >= 0 else "warn"},
        {"label": "Reactions Inside Implied Band", "val": f"{inside} / {n_banded}" if banded else None, "tone": "blue"},
    ]
    takeaways = [_post_takeaway(F, cites[F["tk"]]) for F in facts]
    band_body = ("<p>Each column shows the T-1 at-the-money straddle (nearest expiry after the print) as a dashed band, the move "
                 "the options market priced, and the actual print reaction as a dot: after-hours trading for after-close prints, "
                 "the release-day regular session for pre-market prints. Ringed dots moved more than options implied.</p>")
    sections = [{"heading": "How to Read the Reaction Chart", "body": band_body}]
    for F in facts:
        p2c = F["entry"]["files"].get("post_2c")
        quote = L.text(p2c, "four_pillar_post_sentiment_scores.pillar_4_options_iv_crush_and_skew.top_quote") if p2c else None
        if quote:
            sections.append({"heading": f"${F['tk']} — Options Desk Read (Agent 2C)",
                             "body": f"<p>{_esc(quote)}{cites[F['tk']].ref('p2c')}</p>"})
    return _market_item(
        {"id": "mkt-earnings-scorecard", "category": "Portfolio Earnings Scorecard", "color": "emerald",
         "badge": "T+0 PRINTS • BEAT / MISS & OPTIONS REACTION"},
        L, S, headline, summary, metrics, takeaways, sections, tickers,
        build_chart_rows(facts, []), _latest_date_label(L, posts, "Latest print"), hero=True)


def build_catalyst_item(intel: dict[str, dict]) -> dict | None:
    upcoming = sorted((e for e in intel.values() if e["state"] == "pre_upcoming"), key=_event_key)
    pending = sorted((e for e in intel.values() if e["state"] == "pre_reported"), key=lambda e: e["earnings_date"], reverse=True)
    if not upcoming and not pending:
        return None
    L, S = Ledger(), SourceList()
    up_facts = _safe_facts(gather_pre_facts, L, upcoming)
    pend_facts = [F for F in _safe_facts(gather_pre_facts, L, pending) if not F["stale"]]
    if not up_facts and not pend_facts:
        return None
    cites = {F["tk"]: cite_pre_sources(S, F["entry"]) for F in up_facts + pend_facts}
    k = L.tally([F["tk"] for F in up_facts], "upcoming T-1 prints")
    # Only weekly straddles (expiry within 7 days of the print) are comparable as "the" priced earnings move
    weeklies = [F for F in up_facts if F["weekly"] and is_number(F.get("band_raw"))]
    widest = max(weeklies, key=lambda F: F["band_raw"]) if len(weeklies) > 1 else None

    if up_facts:
        first = up_facts[0]
        name = _short_name(first["entry"]["company_name"])
        if len(up_facts) > 1:
            headline = f"{k} Portfolio Prints Ahead: {name} Leads on {first['date']}"
        else:
            headline = f"Next Portfolio Print: {name} on {first['date']}"
        if widest:
            headline += f"; Widest Weekly Implied Move ${widest['tk']} {widest['band']}"
        lead = ", ".join(f"${F['tk']} {F['date']}" + (f" ({F['band']})" if F["band"] else "") for F in up_facts[:5])
        summary = f"Next up: {lead}"
        if len(up_facts) > 5:
            summary += f", plus {L.tally([F['tk'] for F in up_facts[5:]], 'more upcoming prints')} more in the brief"
        summary += "."
    else:
        headline = "No Upcoming Portfolio Prints Scheduled — T+0 Tearsheets Pending"
        summary = ""
    if pend_facts:
        summary += " Reported, T+0 tearsheet pending: " + ", ".join(f"${F['tk']} ({F['date']})" for F in pend_facts) + "."
    metrics = []
    if up_facts:
        metrics.append({"label": "Next Print", "val": f"${up_facts[0]['tk']} • {up_facts[0]['date']}", "tone": "blue"})
    if widest:
        metrics.append({"label": "Widest Weekly Implied Move", "val": f"${widest['tk']} {widest['band']}", "tone": "warn"})
    if up_facts:
        metrics.append({"label": "Upcoming Prints", "val": k, "tone": "bull"})
    takeaways = [_pre_takeaway(F, cites[F["tk"]]) for F in up_facts + pend_facts]
    sections = [{"heading": "How to Read the Implied Move",
                 "body": "<p>The implied move is the at-the-money straddle price (nearest expiry after the print) divided by the "
                         "Stage 1 spot price: the post-print range the options market is pricing. Straddles that expire weeks after "
                         "the print also price non-earnings days, so compare them with care. Each T-1 briefing sets this against the "
                         "name's historical average one-day earnings move.</p>"}]
    for F in up_facts[:2]:
        sections.append(_pre_debate_section(L, F, cites[F["tk"]]))
    published = f"Next print {up_facts[0]['date']}" if up_facts else _latest_date_label(L, pending, "Latest print")
    return _market_item(
        {"id": "mkt-catalyst-calendar", "category": "Earnings Catalyst Calendar", "color": "amber",
         "badge": "UPCOMING T-1 PRINTS • OPTIONS-IMPLIED MOVES"},
        L, S, headline, summary.strip(), metrics, takeaways, sections, [F["tk"] for F in up_facts + pend_facts],
        build_chart_rows([], up_facts), published, pin=widest["tk"] if widest else None)


def build_theme_item(theme: dict, members: list[dict]) -> dict | None:
    posts = sorted((e for e in members if e["state"] == "post"), key=lambda e: e["earnings_date"], reverse=True)
    ups = sorted((e for e in members if e["state"] == "pre_upcoming"), key=_event_key)
    pends = sorted((e for e in members if e["state"] == "pre_reported"), key=lambda e: e["earnings_date"], reverse=True)
    if not (posts or ups or pends):
        return None
    L, S = Ledger(), SourceList()
    post_f = _safe_facts(gather_post_facts, L, posts)
    up_f = _safe_facts(gather_pre_facts, L, ups)
    pend_f = _safe_facts(gather_pre_facts, L, pends)
    if not (post_f or up_f or pend_f):
        return None
    cites = {F["tk"]: cite_post_sources(S, F["entry"], F) for F in post_f}
    cites.update({F["tk"]: cite_pre_sources(S, F["entry"]) for F in up_f + pend_f})
    label = theme.get("headline_label", theme["category"])

    if post_f:
        lead = post_f[0]
        headline = f"{_short_name(lead['entry']['company_name'])} {lead['q']}".strip() + ":"
        if lead["rev"] and lead["rev_cons"]:
            headline += f" Revenue {lead['rev']} vs {lead['rev_cons']} Street" + _paren(lead["rev_delta"])
        if lead["move"]:
            headline += f"; Shares {lead['move']} " + ("on the Day" if lead["bmo"] else "After Hours")
        if up_f:
            n_up = L.tally([F["tk"] for F in up_f], "upcoming theme prints")
            headline += f" — {n_up} Theme {_plural(n_up, 'Print', 'Prints')} Next"
        summary_parts = [post_print_sentence(F) for F in post_f[:2]]
    elif up_f:
        lead = up_f[0]
        name = _short_name(lead["entry"]["company_name"])
        if len(up_f) > 1:
            n_up = L.tally([F["tk"] for F in up_f], "upcoming theme prints")
            headline = f"{n_up} {label} Prints Ahead: {name} Leads on {lead['date']}"
        else:
            headline = f"{label} Catalyst: {name} Reports {lead['date']}"
        if lead["band"]:
            headline += f" With a {lead['band']} Implied Move"
        summary_parts = [pre_setup_sentence(lead)]
    else:
        lead = pend_f[0]
        tail = "No T+0 Tearsheet Published" if lead["stale"] else "T+0 Forensic Tearsheet Pending"
        headline = f"{_short_name(lead['entry']['company_name'])} Reported {lead['date']}: {tail}"
        summary_parts = [pre_setup_sentence(F) for F in pend_f]
    rest_up = up_f if post_f else up_f[1:]
    if rest_up:
        summary_parts.append("Next: " + ", ".join(f"${F['tk']} {F['date']}" + (f" ({F['band']})" if F["band"] else "") for F in rest_up) + ".")
    if pend_f and (post_f or up_f):
        summary_parts.append("Reported, no T+0 tearsheet yet: " + ", ".join(f"${F['tk']} ({F['date']})" for F in pend_f) + ".")

    metrics = []
    for F in post_f[:2]:
        if F["rev"] and F["rev_delta"]:
            metrics.append({"label": f"{F['tk']} Revenue vs Street", "val": f"{F['rev']} ({F['rev_delta']})", "tone": "bull" if F["rev_beat"] else "warn"})
        if F["move"] and F["band"]:
            down = is_number(F["move_raw"]) and F["move_raw"] < 0
            tone = ("bear" if down else "warn") if F["side"] == "outside" else "bull"
            metrics.append({"label": f"{F['tk']} Reaction vs Implied", "val": f"{F['move']} vs {F['band']}", "tone": tone})
    for F in up_f[:3]:
        if F["band"]:
            metrics.append({"label": f"{F['tk']} Implied • {F['date']}", "val": F["band"], "tone": "blue"})

    takeaways = [_post_takeaway(F, cites[F["tk"]]) for F in post_f] + [_pre_takeaway(F, cites[F["tk"]]) for F in up_f + pend_f]
    sections = [_post_desk_section(L, F, cites[F["tk"]]) for F in post_f[:2]]
    sections += [_pre_debate_section(L, F, cites[F["tk"]]) for F in up_f[:2]]
    active = [F["tk"] for F in post_f + up_f + pend_f]
    others = [e["ticker"] for e in members if e["ticker"] not in active and e["in_portfolio"]]
    if posts:
        published = _latest_date_label(L, posts, "Latest print")
    elif up_f:
        published = f"Next print {up_f[0]['date']}"
    else:
        published = _latest_date_label(L, pends, "Latest print")
    return _market_item(theme, L, S, headline, " ".join(summary_parts), metrics, takeaways, sections,
                        active + others, build_chart_rows(post_f, up_f), published)


def build_market_news_items(intel: dict[str, dict]) -> list[dict]:
    """
    'Top News Impacting the Financial Markets' tiles, generated from ground truth + agent bus:
    hero earnings scorecard, catalyst calendar, then one tile per portfolio theme with published tearsheets.
    """
    builders = [lambda: build_scorecard_item(intel), lambda: build_catalyst_item(intel)]
    assigned = set()
    for theme in MARKET_THEMES:
        members = [intel[t] for t in theme["tickers"] if t in intel]
        assigned.update(theme["tickers"])
        builders.append(lambda theme=theme, members=members: build_theme_item(theme, members))
    leftovers = [e for tk, e in sorted(intel.items()) if tk not in assigned and e["state"] != "watchlist"]
    if leftovers:
        builders.append(lambda: build_theme_item(OTHER_THEME, leftovers))
    items = []
    for build in builders:
        try:
            item = build()
        except Exception as exc:
            print(f"[news_portal] market tile skipped: {type(exc).__name__}: {exc}")
            continue
        if item:
            items.append(item)
    fixed = [i for i in items if i["id"] in ("mkt-earnings-scorecard", "mkt-catalyst-calendar")]
    themed = [i for i in items if i not in fixed]

    def activity(t):
        # Themes with fresh T+0 prints first (newest first), then themes by their nearest upcoming print
        posts = [intel[tk]["earnings_date"] for tk in t["tickers"] if intel[tk]["state"] == "post"]
        ups = [intel[tk]["earnings_date"] for tk in t["tickers"] if intel[tk]["state"] == "pre_upcoming"]
        if posts:
            return (0, -int(max(posts).replace("-", "")))
        if ups:
            return (1, int(min(ups).replace("-", "")))
        return (2, 0)

    themed.sort(key=activity)
    return fixed + themed


# ---------------------------------------------------------------------------
# Section 2: Portfolio News (one tile per ticker's current published event)
# ---------------------------------------------------------------------------

def build_post_portfolio_item(entry: dict) -> dict | None:
    L, S = Ledger(), SourceList()
    F = gather_post_facts(L, entry)
    if not F:
        return None
    tk, f = entry["ticker"], entry["files"]
    c = cite_post_sources(S, entry, F)
    name = _short_name(entry["company_name"])
    verdict = print_verdict(L, F)
    headline = f"{name} (${tk}) {F['q']}: {verdict}".replace("  ", " ")
    if F["rev"] and F["rev_cons"]:
        headline += f" — Revenue {F['rev']} vs {F['rev_cons']} Street" + _paren(F["rev_delta"])
    if F["move"]:
        headline += f", {F['move']} " + ("on the Day" if F["bmo"] else "After Hours")

    takeaways = []
    if F["rev"]:
        eps_txt = ""
        if F["eps"]:
            eps_txt = (f" and {F['eps_kind']} EPS of <strong>{F['eps']}</strong>"
                       + (f" vs <strong>{F['eps_cons']}</strong> consensus" if F["eps_cons"] else "") + _paren(F["eps_delta"]))
        cons = f" vs Street consensus of <strong>{F['rev_cons']}</strong>" if F["rev_cons"] else ""
        verdict_txt = f"verdict <strong>{_esc(F['rev_verdict'])}</strong>" if F["rev_verdict"] else None
        takeaways.append(f"<strong>Headline Print vs. Consensus:</strong> {_esc(F['q'])} revenue of <strong>{F['rev']}</strong>{cons}"
                         + _paren(F["rev_delta"], verdict_txt) + f"{eps_txt}." + c.ref("truth", "exhibit"))
    reaction = reaction_clause(F)
    if reaction:
        label = "Release-Day Price Action (pre-market print)" if F["bmo"] else "After-Hours Price Action"
        extra = f" After-hours drift {F['ah_move']}." if F["bmo"] and F["ah_move"] else ""
        takeaways.append(f"<strong>{label}:</strong> shares {reaction}.{extra}" + c.ref("truth"))
    if F["ocf"] and F["true_fcf"]:
        bridge = _join_clauses([f"OCF <strong>{F['ocf']}</strong>", f"CapEx <strong>{F['capex']}</strong>" if F["capex"] else None,
                                f"Reported FCF {F['reported_fcf']}" if F["reported_fcf"] else None,
                                f"SBC {F['sbc']}" if F["sbc"] else None, f"Finance Leases {F['finance_leases']}" if F["finance_leases"] else None,
                                f"True FCF <strong>{F['true_fcf']}</strong>"], " | ")
        margin = f" Gross margin {F['gm']}, operating margin {F['om']}." if F["gm"] and F["om"] else ""
        takeaways.append(f"<strong>Forensic Cash Flow Bridge ({_esc(F['q'])}):</strong> {bridge}.{margin}" + c.ref("truth"))

    p2b = f.get("post_2b")
    fwd_rows, lead_row = [], None
    for i in _rows(p2b, "forward_guidance_reset_matrix_b"):
        cell = lambda k: L.text(p2b, f"forward_guidance_reset_matrix_b[{i}].{k}") or ""
        metric, guide = cell("forward_horizon_and_metric"), cell("new_management_guidance")
        if not (metric or guide):
            continue
        row = {k: _esc(cell(k)) for k in ("preprint_street_consensus", "delta_vs_street", "action_badge")}
        row.update(metric=_esc(metric), guide=_esc(guide))
        fwd_rows.append(f"<tr><td><strong>{row['metric']}</strong></td><td>{row['preprint_street_consensus']}</td>"
                        f"<td style='color:#34d399;font-weight:700;'>{row['guide']}</td><td>{row['delta_vs_street']}</td>"
                        f"<td><span class='modal-badge'>{row['action_badge']}</span></td></tr>")
        if lead_row is None and guide:
            lead_row = row
    if lead_row:
        street = f" vs pre-print Street {lead_row['preprint_street_consensus']}" if lead_row["preprint_street_consensus"] else ""
        takeaways.append(f"<strong>Forward Guidance Reset ({lead_row['metric'] or 'Next Period'}):</strong> management guided "
                         f"<strong>{lead_row['guide']}</strong>{street}" + _paren(lead_row["delta_vs_street"]) + "." + c.ref("p2b"))

    sections = []
    desk = _post_desk_section(L, F, c)
    p2c = f.get("post_2c")
    retail = L.text(p2c, "retail_vs_institutional_reaction.retail_sentiment_summary") if p2c else None
    if desk:
        if retail:
            desk["body"] += f"<p><strong>Retail &amp; FinTwit Pulse:</strong> {_esc(retail)}{c.ref('p2c')}</p>"
        desk["heading"] = "Institutional vs. Retail Post-Print Desk Synthesis (Agent 2C)"
        sections.append(desk)
    if fwd_rows:
        sections.append({"heading": "Forward Guidance Reset Matrix (Agent 2B)",
                         "body": "<div class='modal-table-wrap'><table class='modal-table'><thead><tr><th>Metric / Horizon</th><th>Pre-Print Street</th>"
                                 "<th>New Management Guide</th><th>Delta vs. Street</th><th>Action</th></tr></thead><tbody>" + "".join(fwd_rows) + "</tbody></table></div>"})
    qa_html = ""
    for i in _rows(p2b, "call_qa_forensic_highlights")[:3]:
        base = f"call_qa_forensic_highlights[{i}]"
        question = _first_text(L, p2b, [f"{base}.question", f"{base}.question_focus"])
        answer = _first_text(L, p2b, [f"{base}.executive_response", f"{base}.management_response"])
        if not (question or answer):
            continue
        analyst = _first_text(L, p2b, [f"{base}.analyst_name", f"{base}.analyst"]) or "Analyst"
        topic = _first_text(L, p2b, [f"{base}.topic", f"{base}.question_focus"])
        qa_html += (f"<div class='qa-block'><div class='qa-analyst'><strong>{_esc(analyst)}</strong>" + (f" — <em>{_esc(topic)}</em>" if topic else "") + "</div>"
                    + (f"<div class='qa-q'><strong>Q:</strong> {_esc(question)}</div>" if question else "")
                    + (f"<div class='qa-a'><strong>Executive Response:</strong> {_esc(answer)}</div>" if answer else "") + "</div>")
    if qa_html:
        sections.append({"heading": "Top Conference Call Q&A Exchanges (Agent 2B)", "body": qa_html})
    acc_rows = ""
    for i in _rows(p2b, "guidance_accountability_matrix_a"):
        t = lambda k: _esc(L.text(p2b, f"guidance_accountability_matrix_a[{i}].{k}") or "")
        if not (t("guided_metric") or t("reported_q0_actual")):
            continue
        acc_rows += (f"<tr><td><strong>{t('guided_metric')}</strong></td><td>{t('prior_quarter_guidance')}</td>"
                     f"<td style='color:#60a5fa;font-weight:600;'>{t('reported_q0_actual')}</td><td>{t('variance_commentary')}</td></tr>")
    if acc_rows:
        prior = _esc(F["prior_q"] or "Prior Quarter")
        sections.append({"heading": "Prior-Quarter Guidance Accountability (Agent 2B)",
                         "body": f"<div class='modal-table-wrap'><table class='modal-table'><thead><tr><th>Guided Metric</th><th>Guidance Issued ({prior})</th>"
                                 f"<th>Reported {_esc(F['q'])} Actual</th><th>Forensic Commentary</th></tr></thead><tbody>{acc_rows}</tbody></table></div>"})

    if F["bmo"]:
        price_metric = {"label": "Release-Day Close", "val": f"{F['close']} ({F['move']})" if F["close"] and F["move"] else None}
    else:
        price_metric = {"label": "After-Hours Price", "val": f"{F['ah']} ({F['move']})" if F["ah"] and F["move"] else None}
    price_metric["tone"] = "bull" if is_number(F["move_raw"]) and F["move_raw"] >= 0 else "warn"
    metrics = [
        price_metric,
        {"label": f"{F['q'] or 'Q0'} Revenue vs Street", "val": f"{F['rev']} ({F['rev_delta']})" if F["rev"] and F["rev_delta"] else F["rev"],
         "tone": "bull" if F["rev_beat"] else "warn"},
        {"label": f"{F['eps_kind']} EPS / True FCF", "val": " / ".join(x for x in (F["eps"], F["true_fcf"]) if x) or None, "tone": "bull"},
    ]
    item = {
        "id": f"port-post-{tk.lower()}", "primary_ticker": tk, "company_name": entry["company_name"],
        "report_type": "post", "status_badge": "T+0 POST-EARNINGS", "verdict_badge": verdict,
        "earnings_date": F["date"], "report_url": entry["post_report_url"], "pre_report_url": entry["pre_report_url"],
        "headline": headline, "summary": post_print_sentence(F), "tickers": [tk],
        "metrics_strip": [m for m in metrics if m["val"]],
        "sources": S.items, "sources_count": len(S.items), "key_takeaways": takeaways, "sections": sections, "ledger": L,
    }
    item["read_time"] = _read_time(item)
    return item


def build_pre_portfolio_item(entry: dict) -> dict | None:
    L, S = Ledger(), SourceList()
    F = gather_pre_facts(L, entry)
    if not F:
        return None
    tk, f = entry["ticker"], entry["files"]
    c = cite_pre_sources(S, entry)
    name = _short_name(entry["company_name"])
    reported = entry["state"] == "pre_reported"
    if reported:
        tail = "No T+0 Tearsheet Published" if F["stale"] else "T+0 Forensic Tearsheet Pending"
        headline = f"{name} (${tk}) Reported {F['when']} — {tail}"
    else:
        headline = f"{name} (${tk}) Reports {F['when']}"
        extras = _join_clauses([f"{F['spot']} Spot" if F["spot"] else None, f"{F['band']} Implied Move" if F["band"] else None,
                                f"{F['mean_pt']} Street Target{_paren(F['upside'])}" if F["mean_pt"] else None])
        if extras:
            headline += f": {extras}"

    takeaways = []
    val = _join_clauses([f"Stage 1 spot <strong>{F['spot']}</strong>" if F["spot"] else None,
                         f"forward P/E <strong>{F['fwd_pe']}</strong>" if F["fwd_pe"] else None,
                         f"EV/EBITDA <strong>{F['ev_ebitda']}</strong>" if F["ev_ebitda"] else None])
    status = "reported" if reported else "reports"
    takeaways.append(f"<strong>Release Schedule &amp; Valuation:</strong> {_esc(name)} (${tk}) {status} on <strong>{F['when']}</strong>"
                     + (f"; {val}" if val else "") + "." + c.ref("truth"))
    straddle_txt = None
    if F["band"]:
        expiry = f" (exp {F['expiry']})" if F["expiry"] else ""
        straddle_txt = f"ATM straddle{expiry} implies <strong>{F['band']}</strong>" + (f" ({F['straddle']})" if F["straddle"] else "")
        if F["expiry_days"] and F["expiry_days"] > 7:
            straddle_txt += " — a multi-week expiry, so it also prices non-earnings trading days"
    opt = _join_clauses([straddle_txt, f"ATM IV {F['iv']}" if F["iv"] else None, f"put/call OI {F['pcr']}" if F["pcr"] else None])
    if opt:
        hist = (f" Over the last four quarters it beat EPS consensus at a <strong>{F['beat_rate']}</strong> rate, with an average one-day "
                f"post-print move of <strong>{F['avg_move']}</strong>." if F["beat_rate"] and F["avg_move"] else "")
        takeaways.append(f"<strong>Options Positioning:</strong> {opt}.{hist}" + c.ref("truth"))
    if F["mean_pt"]:
        rng = f", high {F['pt_high']} / low {F['pt_low']}" if F["pt_high"] and F["pt_low"] else ""
        cov = f"{F['analysts']} analysts, " if F["analysts"] else ""
        takeaways.append(f"<strong>Street Consensus &amp; Targets:</strong> {cov}mean target <strong>{F['mean_pt']}</strong>{_paren(F['upside'])}{rng}"
                         + (f"; consensus EPS {F['cons_eps']}" if F["cons_eps"] else "") + "." + c.ref("truth"))
    elif F["cons_eps"]:
        takeaways.append(f"<strong>Street Consensus:</strong> consensus EPS <strong>{F['cons_eps']}</strong>." + c.ref("truth"))
    if F["ocf"] and F["true_fcf"]:
        bridge = _join_clauses([f"OCF <strong>{F['ocf']}</strong>", f"CapEx <strong>{F['capex']}</strong>" if F["capex"] else None,
                                f"Reported FCF {F['reported_fcf']}" if F["reported_fcf"] else None, f"SBC {F['sbc']}" if F["sbc"] else None,
                                f"True FCF <strong>{F['true_fcf']}</strong>"], " | ")
        takeaways.append(f"<strong>Stage 1 FCF Bridge ({_esc(F['fcf_period'] or 'last stitched quarter')}):</strong> {bridge}." + c.ref("truth"))

    sections = []
    p2c, p2b = f.get("pre_2c"), f.get("pre_2b")
    inst = L.text(p2c, "retail_vs_institutional_positioning.institutional_positioning_summary") if p2c else None
    ret = L.text(p2c, "retail_vs_institutional_positioning.retail_positioning_summary") if p2c else None
    if inst or ret:
        body = f"<p><strong>Institutional Desk Positioning:</strong> {_esc(inst)}{c.ref('p2c')}</p>" if inst else ""
        body += f"<p><strong>Retail &amp; FinTwit Positioning:</strong> {_esc(ret)}{c.ref('p2c')}</p>" if ret else ""
        sections.append({"heading": "Institutional & Retail Pre-Earnings Positioning (Agent 2C)", "body": body})
    flagship = _first_text(L, p2c, ["verified_live_product_context.flagship_products", "verified_live_product_context.flagship_ai_models"])
    channels = _first_text(L, p2c, ["verified_live_product_context.commercialization_channels"])
    if flagship or channels:
        body = f"<p><strong>Flagship Products &amp; Growth Drivers:</strong> {_esc(flagship)}{c.ref('p2c')}</p>" if flagship else ""
        body += f"<p><strong>Commercialization Channels:</strong> {_esc(channels)}</p>" if channels else ""
        sections.append({"heading": "Verified Live Product & Architecture Context (Agent 2C)", "body": body})
    debate = _pre_debate_section(L, F, c)
    if debate:
        debate["heading"] = "Top Pre-Print Debate & Call Focus Question (Agent 2B)"
        sections.append(debate)
    rows = ""
    for i in _rows(p2b, "matrix_b_forward_guidance_bogeys"):
        t = lambda k: _esc(L.text(p2b, f"matrix_b_forward_guidance_bogeys[{i}].{k}") or "")
        if not (t("forward_metric") or t("street_consensus_hurdle")):
            continue
        rows += (f"<tr><td><strong>{t('forward_metric')}</strong></td><td>{t('street_consensus_hurdle')}</td>"
                 f"<td style='color:#34d399;font-weight:700;'>{t('bull_case_bogey')}</td><td>{t('bear_case_breakdown')}</td></tr>")
    if rows:
        sections.append({"heading": "Forward Guidance Bogeys Required for a Re-Rating (Agent 2B)",
                         "body": "<div class='modal-table-wrap'><table class='modal-table'><thead><tr><th>Forward Metric</th><th>Street Hurdle</th>"
                                 "<th>Buy-Side Bull Bogey</th><th>Bear Breakdown</th></tr></thead><tbody>" + rows + "</tbody></table></div>"})

    metrics = [
        {"label": "Stage 1 Spot", "val": F["spot"], "tone": "blue"},
        {"label": "Implied Straddle Move", "val": f"{F['band']} ({F['straddle']})" if F["band"] and F["straddle"] else F["band"], "tone": "warn"},
        {"label": "Street Mean Target", "val": f"{F['mean_pt']}{_paren(F['upside'])}" if F["mean_pt"] else None, "tone": "bull"},
        {"label": "Consensus EPS", "val": F["cons_eps"], "tone": "bull"},
    ]
    if reported:
        badge = f"REPORTED {F['date'].upper()} • " + ("NO T+0 TEARSHEET" if F["stale"] else "T+0 PENDING")
    else:
        badge = f"T-1 BRIEFING • {F['date'].upper()}" + (" (UNCONFIRMED)" if F["unconfirmed"] else "")
    item = {
        "id": f"port-pre-{tk.lower()}", "primary_ticker": tk, "company_name": entry["company_name"],
        "report_type": "pending" if reported else "pre", "status_badge": badge,
        "verdict_badge": f"IMPLIED {F['band']}" if F["band"] else "T-1 SETUP",
        "earnings_date": F["date"], "report_url": entry["pre_report_url"], "pre_report_url": entry["pre_report_url"],
        "headline": headline, "summary": pre_setup_sentence(F), "tickers": [tk],
        "metrics_strip": [m for m in metrics if m["val"]][:3],
        "sources": S.items, "sources_count": len(S.items), "key_takeaways": takeaways, "sections": sections, "ledger": L,
    }
    item["read_time"] = _read_time(item)
    return item


def build_portfolio_news_items(intel: dict[str, dict]) -> list[dict]:
    """
    Portfolio News tiles: one per ticker's current published event, ordered
    T+0 post-earnings (newest first) -> upcoming T-1 (soonest first) -> reported / T+0 pending (newest first).
    """
    entries = list(intel.values())
    posts = sorted((e for e in entries if e["state"] == "post"), key=lambda e: (e["earnings_date"], e["ticker"]), reverse=True)
    ups = sorted((e for e in entries if e["state"] == "pre_upcoming"), key=_event_key)
    pends = sorted((e for e in entries if e["state"] == "pre_reported"), key=lambda e: (e["earnings_date"], e["ticker"]), reverse=True)
    items = []
    for builder, e in [(build_post_portfolio_item, e) for e in posts] + [(build_pre_portfolio_item, e) for e in ups + pends]:
        try:
            item = builder(e)
        except Exception as exc:
            print(f"[news_portal] portfolio tile for {e['ticker']} skipped: {type(exc).__name__}: {exc}")
            continue
        if item:
            items.append(item)
    return items


CITE_SUFFIX = re.compile(r" \[\d+(?:, \d+)*\]$")


def safe_script_json(obj) -> str:
    """JSON for an inline <script>: escapes <, >, & and JS line separators so bus text can never close the tag."""
    return (json.dumps(obj, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def render_ticker_pill(tk: str, intel: dict[str, dict], extra_class: str = "") -> str:
    """
    Renders an interactive stock/ticker pill:
    - T+0 / T-1 tickers link to their latest tearsheet; watchlist tickers filter the Portfolio News section.
    - Hovering / focusing opens the quick pop-up summary hovercard (popover="hint" + interestfor).
    """
    entry = intel.get(tk, {})
    state = entry.get("state", "watchlist")
    href = entry.get("primary_report_url") or "#section-portfolio-news"
    if state == "post":
        mode_cls, dot, tag = "pill-post", "dot-emerald", '<span class="pill-tag">T+0</span>'
    elif state in ("pre_upcoming", "pre_reported"):
        mode_cls, dot, tag = "pill-pre", "dot-blue", '<span class="pill-tag">T-1</span>'
    else:
        mode_cls, dot, tag = "pill-watch", "dot-slate", ""
    filter_attr = f' data-filter-ticker="{_esc(tk)}"' if state == "watchlist" else ""
    return (
        f'<a href="{_esc(href)}" interestfor="hovercard-{_esc(tk)}" data-hovercard-id="hovercard-{_esc(tk)}" '
        f'data-ticker="{_esc(tk)}"{filter_attr} class="stock-pill-link {mode_cls} {extra_class}">'
        f'<span class="pill-dot {dot}" aria-hidden="true"></span><span class="pill-sym">${_esc(tk)}</span>{tag}</a>'
    )


def render_all_hovercards_html(intel: dict[str, dict]) -> str:
    """
    Renders native popover="hint" hovercard elements for every ticker in intel.
    Follows modern-web-guidance `hovercard`:
    - Uses `popover="hint"` on the card container.
    - Does NOT set `role="tooltip"` on the popover or `aria-describedby`/`aria-details` on triggers.
    - Does NOT include a redundant link inside the hovercard.
    """
    cards = []
    for tk, entry in sorted(intel.items()):
        hs = entry.get("hover_summary", {})
        mode = hs.get("mode", "WATCHLIST")
        mode_border = "hc-post" if mode == "POST" else ("hc-pre" if mode == "PRE" else "hc-watch")
        cells_html = "".join(
            f'<div class="hc-p-cell"><span class="hc-p-lbl">{_esc(lbl)}</span><span class="hc-p-val {cls}">{_esc(val)}</span></div>'
            for lbl, val, cls in hs.get("cells", [])
        )
        box_parts = []
        for b in hs.get("boxes", []):
            small = f" <small>({_esc(b['small'])})</small>" if b.get("small") else ""
            sub = f'<span class="hc-m-sub">{_esc(b["sub"])}</span>' if b.get("sub") else ""
            box_parts.append(f'<div class="hc-m-box"><span class="hc-m-lbl">{_esc(b["label"])}</span>'
                             f'<span class="hc-m-val">{_esc(b["value"])}{small}</span>{sub}</div>')
        boxes_html = "".join(box_parts)
        guide_src = hs.get("guide_src") or "Forward guide"
        guide_html = f'<div class="hc-guidance-box"><strong>{_esc(guide_src)}:</strong> {_esc(hs["guide"])}</div>' if hs.get("guide") else ""
        footer = hs.get("footer")
        footer_html = f'<span>{_esc(footer[0])}: <strong>{_esc(footer[1])}</strong></span>' if footer else "<span></span>"
        price_html = f'<div class="hc-price-strip">{cells_html}</div>' if cells_html else ""
        metrics_html = f'<div class="hc-metrics-grid">{boxes_html}</div>' if boxes_html else ""
        driver_src = f'<span class="hc-src">{_esc(hs["driver_src"])}:</span> ' if hs.get("driver_src") else ""
        driver_html = f'<p class="hc-driver">{driver_src}{_esc(hs["driver"])}</p>' if hs.get("driver") else ""
        name = entry.get("company_name", tk)
        name_html = f'<span class="hc-name">{_esc(name)}</span>' if name and name != tk else ""
        cards.append(f"""
        <div id="hovercard-{_esc(tk)}" popover="hint" class="hovercard {mode_border}">
          <div class="hc-top">
            <div class="hc-id">
              <span class="hc-sym">${_esc(tk)}</span>
              {name_html}
            </div>
            <span class="hc-badge">{_esc(hs.get("badge", ""))}</span>
          </div>
          <div class="hc-verdict-bar">
            <span class="hc-verdict-label">{"Verdict: " if mode == "POST" else ""}<strong>{_esc(hs.get("verdict", ""))}</strong></span>
            <span class="hc-date">{_esc(hs.get("date", ""))}</span>
          </div>
          {price_html}
          {metrics_html}
          {driver_html}
          {guide_html}
          <div class="hc-footer">
            {footer_html}
            <span class="hc-cta-hint">{_esc(hs.get("cta", ""))}</span>
          </div>
        </div>
        """)
    return "\n".join(cards)


def _ledger_rows(item: dict) -> tuple[list[str], list[list]]:
    """
    Compact provenance for the modal's Source Ledger: (files, rows) where each row is
    [label, value, file_index (-1 = derived), json_path_or_note] and files is the article's de-duplicated file table.
    """
    files: list[str] = []
    file_idx: dict[str, int] = {}
    rows, seen = [], set()
    for fact in item["ledger"].facts:
        if fact["kind"] not in ("num", "date", "derived", "file") or not fact.get("label"):
            continue
        key = (fact.get("label"), fact.get("display"))
        if key in seen:
            continue
        seen.add(key)
        if fact["kind"] == "derived":
            rows.append([fact["label"], fact["display"], -1, f"derived: {fact['op']} of {len(fact['inputs'])} ledger values"])
            continue
        if fact["file"] not in file_idx:
            file_idx[fact["file"]] = len(files)
            files.append(fact["file"])
        rows.append([fact["label"], fact["display"], file_idx[fact["file"]], fact.get("path", "")])
    return files, rows


def _article_payload(item: dict, section: str, category: str, badge: str, published: str, extra: dict) -> dict:
    ledger_files, ledger = _ledger_rows(item)
    return {
        "id": item["id"], "section": section, "category": category, "badge": badge,
        "published": published, "read_time": item["read_time"],
        "headline": item["headline"], "summary": item["summary"], "tickers": item["tickers"],
        "metrics_strip": item["metrics_strip"], "sources": item["sources"],
        "key_takeaways": item["key_takeaways"], "sections": item["sections"],
        "ledger_files": ledger_files, "ledger": ledger, **extra,
    }


def build_discover_portal_section_html(intel: dict[str, dict]) -> tuple[str, str]:
    """
    Returns (portal_html_fragment, articles_json_str) so it can be embedded in both
    `news.html` and `index.html`. The JSON string is already escaped for an inline <script>.
    """
    market_items = build_market_news_items(intel)
    portfolio_items = build_portfolio_news_items(intel)
    portfolio_tickers = load_portfolio_tickers()

    articles_map = {}
    for item in market_items:
        articles_map[item["id"]] = _article_payload(
            item, "TOP FINANCIAL MARKET IMPACT REPORT", item["category"], item["impact_badge"], item["published"],
            {"primary_report_url": "", "primary_ticker": "",
             "library_filter": "post" if any(intel.get(t, {}).get("state") == "post" for t in item["tickers"]) else "pre"})
    for item in portfolio_items:
        articles_map[item["id"]] = _article_payload(
            item, f"PORTFOLIO FORENSIC AI REPORT • ${item['primary_ticker']}",
            f"{item['company_name']} (${item['primary_ticker']})",
            f"{item['status_badge']} • {item['verdict_badge']}", f"Release {item['earnings_date']}",
            {"primary_report_url": item["report_url"], "pre_report_url": item.get("pre_report_url", ""),
             "primary_ticker": item["primary_ticker"], "report_type": item["report_type"]})

    # 1. Market Impact Tiles (Bento Grid). Row 1 = hero (8 cols) + first regular tile (4 cols); the remaining
    #    tiles fill rows of three, so the last row is widened instead of leaving an orphan tile.
    span_overrides = {}
    rest = [i for i in market_items if not i.get("is_hero")]
    if rest:
        tail = rest[1:] if any(i.get("is_hero") for i in market_items) else rest
        if len(tail) % 3 == 1:
            span_overrides[tail[-1]["id"]] = "tile-span-12"
        elif len(tail) % 3 == 2:
            span_overrides[tail[-1]["id"]] = "tile-span-6"
            span_overrides[tail[-2]["id"]] = "tile-span-6"
    mkt_tiles_html = []
    for item in market_items:
        hero_cls = "discover-tile-hero" if item.get("is_hero") else span_overrides.get(item["id"], "")
        pills_html = " ".join(render_ticker_pill(tk, intel) for tk in item.get("tickers", []))
        metrics_html = "".join(
            f'<div class="tile-mini-stat"><span class="tms-lbl">{_esc(m["label"])}</span>'
            f'<span class="tms-val tone-{_esc(m["tone"])}">{_esc(m["val"])}</span></div>'
            for m in item.get("metrics_strip", [])
        )
        visual_html = f'<div class="tile-visual-wrap">{item["chart_svg"]}</div>' if item.get("chart_svg") else ""
        digest_html = ""
        if item.get("is_hero") and item.get("key_takeaways"):
            lines = "".join(f"<li>{CITE_SUFFIX.sub('', t)}</li>" for t in item["key_takeaways"])
            digest_html = f'<ul class="tile-digest">{lines}</ul>'
        published_html = f"<span>•</span><span>{_esc(item['published'])}</span>" if item.get("published") else ""
        mkt_tiles_html.append(f"""
        <article class="discover-tile {hero_cls}" data-article-id="{_esc(item['id'])}" data-tickers="{_esc(','.join(item['tickers']).lower())}">
          <div class="tile-header-bar">
            <span class="tile-cat-pill">{_esc(item['category'])}</span>
            <span class="tile-impact-tag impact-{_esc(item['impact_color'])}">{_esc(item['impact_badge'])}</span>
          </div>
          {visual_html}
          <h3 class="tile-headline">{_esc(item['headline'])}</h3>
          <p class="tile-summary">{_esc(item['summary'])}</p>
          {digest_html}
          <div class="tile-metrics-row">
            {metrics_html}
          </div>
          <div class="tile-tickers-row">
            <span class="tile-tickers-label">Portfolio Stocks in This Brief (Hover for Summary • Click for Report):</span>
            <div class="tile-pills-wrap">
              {pills_html}
            </div>
          </div>
          <div class="tile-footer-bar">
            <div class="tile-meta-left">
              <span class="tile-sources-badge">📚 {item['sources_count']} Repo Sources</span>
              <span>•</span>
              <span>{_esc(item['read_time'])}</span>
              {published_html}
            </div>
            <button type="button" class="tile-open-btn" data-open-article="{_esc(item['id'])}" aria-haspopup="dialog">
              <span>Read AI Synthesis</span>
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>
        </article>
        """)

    # 2. Portfolio Ticker Ribbon: T+0 first, then T-1, then the remaining watchlist alphabetically
    state_rank = {"post": 0, "pre_upcoming": 1, "pre_reported": 1}
    sorted_port_tickers = sorted(portfolio_tickers, key=lambda t: (state_rank.get(intel.get(t, {}).get("state"), 2), t))
    ribbon_pills_html = " ".join(render_ticker_pill(tk, intel, extra_class="ribbon-pill") for tk in sorted_port_tickers)

    # 3. Portfolio News Tiles
    type_meta = {
        "post": ("port-tile-post", "status-post", "Open {tk} Post-Earnings Report"),
        "pre": ("port-tile-pre", "status-pre", "Open {tk} T-1 Briefing"),
        "pending": ("port-tile-pre port-tile-pending", "status-pending", "Open {tk} T-1 Briefing"),
    }
    port_tiles_html = []
    for item in portfolio_items:
        tk = item["primary_ticker"]
        card_cls, status_cls, link_label = type_meta[item["report_type"]]
        metrics_html = "".join(
            f'<div class="tile-mini-stat"><span class="tms-lbl">{_esc(m["label"])}</span>'
            f'<span class="tms-val tone-{_esc(m["tone"])}">{_esc(m["val"])}</span></div>'
            for m in item.get("metrics_strip", [])
        )
        port_tiles_html.append(f"""
        <article class="discover-tile portfolio-news-tile {card_cls}" id="portfolio-stock-{_esc(tk)}" data-article-id="{_esc(item['id'])}" data-port-type="{item['report_type']}" data-ticker="{_esc(tk.lower())}" data-company="{_esc(item['company_name'].lower())}">
          <div class="tile-header-bar">
            <div class="tile-stock-id">
              {render_ticker_pill(tk, intel, extra_class="tile-primary-pill")}
              <span class="tile-comp-name">{_esc(item['company_name'])}</span>
            </div>
            <span class="tile-status-badge {status_cls}">{_esc(item['status_badge'])}</span>
          </div>
          <div class="tile-verdict-row">
            <span class="verdict-chip">{_esc(item['verdict_badge'])}</span>
            <span class="verdict-date">Release: {_esc(item['earnings_date'])}</span>
          </div>
          <h3 class="tile-headline">{_esc(item['headline'])}</h3>
          <p class="tile-summary">{_esc(item['summary'])}</p>
          <div class="tile-metrics-row">
            {metrics_html}
          </div>
          <div class="tile-footer-bar">
            <button type="button" class="tile-open-btn" data-open-article="{_esc(item['id'])}" aria-haspopup="dialog">
              <span>✨ AI Discover Brief</span>
            </button>
            <a href="{_esc(item['report_url'])}" interestfor="hovercard-{_esc(tk)}" data-hovercard-id="hovercard-{_esc(tk)}" data-ticker="{_esc(tk)}" class="tile-direct-report-link">
              <span>{link_label.format(tk=_esc(tk))}</span>
              <svg width="13" height="13" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
            </a>
          </div>
        </article>
        """)

    count_type = lambda t: sum(1 for x in portfolio_items if x["report_type"] == t)
    n_post, n_pre, n_pending = count_type("post"), count_type("pre"), count_type("pending")
    pending_tab = ""
    if n_pending:
        pending_tab = (f'<button type="button" class="port-tab-btn" data-port-filter="pending" aria-pressed="false">'
                       f'<span class="port-dot port-dot-pending" aria-hidden="true"></span> Reported • T+0 Pending ({n_pending})</button>')

    portal_section_html = f"""
    <!-- ==========================================================================
         PERPLEXITY DISCOVER-STYLE AI MARKET & PORTFOLIO NEWS PORTAL
         ========================================================================== -->
    <section class="discover-portal-wrapper" id="discover-news-portal" aria-label="AI Financial Market and Portfolio Discover Portal">

      <!-- INTERACTIVE INSTRUCTION CALLOUT -->
      <div class="discover-ux-banner">
        <div class="ux-banner-left">
          <span class="ux-pulse-dot" aria-hidden="true"></span>
          <span><strong>Interactive Discover Controls:</strong> <strong>Click any News Tile</strong> to open its AI Synthesis Report with sources and a figure-by-figure ledger • <strong>Hover any <span class="ux-code-pill">$TICKER</span></strong> for a quick pop-up (T+0 results, T-1 setup, or watchlist status) • <strong>Click any <span class="ux-code-pill">$TICKER</span></strong> to open its tearsheet.</span>
        </div>
        <div class="ux-banner-right">
          <span class="ux-stat-pill">Portfolio: <strong>{len(portfolio_tickers)} Tickers</strong></span>
          <span class="ux-stat-pill pill-emerald">T+0 Post-Print: <strong>{n_post}</strong></span>
          <span class="ux-stat-pill pill-blue">T-1 Upcoming: <strong>{n_pre}</strong></span>
        </div>
      </div>

      <!-- SECTION 1: TOP NEWS IMPACTING THE FINANCIAL MARKETS -->
      <div class="discover-section-header" id="section-market-news">
        <div>
          <div class="sec-eyebrow">⚡ EARNINGS SCORECARD, CATALYST CALENDAR &amp; SECTOR THEMES</div>
          <h2 class="sec-title">1. Top News Impacting the Financial Markets</h2>
          <p class="sec-subtitle">Bento briefings generated from Stage 1 ground truth, SEC Exhibit 99.1 filings and the agent research bus. Click any tile for the multi-source report, or hover/click any portfolio stock.</p>
        </div>
      </div>

      <div class="market-bento-grid" id="marketNewsGrid">
        {"".join(mkt_tiles_html)}
      </div>

      <!-- SECTION 2: MY PORTFOLIO NEWS (COMPLEMENTING TICKERS.TXT) -->
      <div class="discover-section-header" id="section-portfolio-news" style="margin-top: 42px;">
        <div>
          <div class="sec-eyebrow">🎯 PERSONALIZED FOR YOUR {len(portfolio_tickers)}-STOCK TICKERS.TXT PORTFOLIO</div>
          <h2 class="sec-title">2. My Portfolio News &amp; Post-Earnings Intelligence</h2>
          <p class="sec-subtitle">Post-earnings forensic headlines and T-1 setups for your <code>tickers.txt</code> holdings. <strong>Hover any stock/ticker</strong> for its quick pop-up summary, or <strong>click it</strong> to open the full tearsheet.</p>
        </div>
        <search class="port-news-controls">
          <div class="port-type-tabs" role="group" aria-label="Filter Portfolio News by Report Type">
            <button type="button" class="port-tab-btn active" data-port-filter="all" aria-pressed="true">All Portfolio News ({len(portfolio_items)})</button>
            <button type="button" class="port-tab-btn" data-port-filter="post" aria-pressed="false">
              <span class="port-dot port-dot-post" aria-hidden="true"></span> T+0 Post-Earnings ({n_post})
            </button>
            <button type="button" class="port-tab-btn" data-port-filter="pre" aria-pressed="false">
              <span class="port-dot port-dot-pre" aria-hidden="true"></span> T-1 Upcoming ({n_pre})
            </button>
            {pending_tab}
          </div>
          <div class="port-search-input-wrap">
            <label for="portfolioNewsSearch" class="sr-only">Search portfolio news by ticker or company</label>
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            <input type="search" id="portfolioNewsSearch" placeholder="Filter portfolio news ($META, $TSLA...)" />
          </div>
        </search>
      </div>

      <!-- PORTFOLIO TICKER RIBBON (EVERY TICKER IN TICKERS.TXT) -->
      <div class="portfolio-ribbon-card">
        <div class="ribbon-header">
          <span class="ribbon-title">📋 Your <code>tickers.txt</code> Portfolio Universe ({len(portfolio_tickers)} Equities) — Hover for Quick Pop-Up Summary • Click to Open Tearsheet:</span>
          <div class="ribbon-legend">
            <span><i class="pill-dot dot-emerald" aria-hidden="true"></i> T+0 Post-Earnings Live</span>
            <span><i class="pill-dot dot-blue" aria-hidden="true"></i> T-1 Briefing Ready</span>
            <span><i class="pill-dot dot-slate" aria-hidden="true"></i> Active Watchlist</span>
          </div>
        </div>
        <div class="ribbon-pills-container">
          {ribbon_pills_html}
        </div>
      </div>

      <!-- PORTFOLIO NEWS TILES GRID -->
      <div class="portfolio-tiles-grid" id="portfolioNewsGrid">
        {"".join(port_tiles_html)}
      </div>
      <div class="port-empty-state" id="portfolioNewsEmpty" hidden>
        <strong>No matching portfolio news.</strong>
        <span id="portfolioNewsEmptyText">Watchlist names get a T-1 briefing automatically when their earnings window opens.</span>
      </div>
    </section>

    <!-- ==========================================================================
         PERPLEXITY DISCOVER DETAILED AI REPORT MODAL (<dialog closedby="any">)
         ========================================================================== -->
    <dialog id="discover-article-dialog" closedby="any" aria-labelledby="discover-article-title">
      <div class="discover-modal-inner">
        <div class="discover-modal-topbar">
          <div class="dm-breadcrumbs">
            <span class="dm-sec-badge" id="dm-section-badge">AI DISCOVER SYNTHESIS</span>
            <span class="dm-cat-badge" id="dm-category-badge">Market Intelligence</span>
            <span class="dm-meta-text" id="dm-meta-text"></span>
          </div>
          <form method="dialog" class="dm-close-form">
            <button type="submit" class="dm-close-btn" autofocus aria-label="Close Detailed AI Report">
              <span>Close</span>
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </form>
        </div>

        <article class="discover-modal-body">
          <h1 id="discover-article-title" class="dm-headline">Detailed AI Synthesis Report</h1>
          <p id="dm-lead-summary" class="dm-lead"></p>

          <!-- PRIMARY SOURCES STRIP (PERPLEXITY STYLE) -->
          <div class="dm-sources-section">
            <div class="dm-subhead">📚 Sources &amp; Filings (Repo Files)</div>
            <div class="dm-sources-grid" id="dm-sources-grid"></div>
          </div>

          <!-- PORTFOLIO STOCKS BAR (HOVER FOR SUMMARY / CLICK FOR TEARSHEET) -->
          <div class="dm-tickers-bar">
            <span class="dm-tickers-lbl">Portfolio Tickers in This Report (Hover for Pop-Up Summary • Click for Full Page):</span>
            <div class="dm-tickers-list" id="dm-tickers-list"></div>
          </div>

          <!-- HEADLINE METRICS STRIP -->
          <div class="dm-metrics-strip" id="dm-metrics-strip"></div>

          <!-- EXECUTIVE AI TAKEAWAYS -->
          <div class="dm-takeaways-card">
            <div class="dm-subhead">⚡ Executive AI Synthesis &amp; Key Takeaways</div>
            <ul class="dm-takeaways-list" id="dm-takeaways-list"></ul>
          </div>

          <!-- DEEP-DIVE NARRATIVE SECTIONS -->
          <div class="dm-narrative-container" id="dm-narrative-container"></div>

          <!-- FIGURE-BY-FIGURE GROUND-TRUTH LEDGER -->
          <details class="dm-ledger" id="dm-ledger">
            <summary>🧾 Ground-Truth Source Ledger — every figure in this brief and the file it came from</summary>
            <div class="modal-table-wrap"><table class="modal-table dm-ledger-table"><thead><tr><th>Figure</th><th>Value</th><th>Source</th></tr></thead><tbody id="dm-ledger-body"></tbody></table></div>
          </details>

          <!-- BOTTOM CTA TO FULL TEARSHEET -->
          <div class="dm-footer-cta" id="dm-footer-cta"></div>
        </article>
      </div>
    </dialog>

    <!-- ==========================================================================
         QUICK POP-UP SUMMARY HOVERCARDS (popover="hint")
         ========================================================================== -->
    {render_all_hovercards_html(intel)}
    """

    return portal_section_html, safe_script_json(articles_map)


def get_discover_portal_css() -> str:
    return """
    /* ==========================================================================
       PERPLEXITY DISCOVER NEWS PORTAL & HOVERCARD / DIALOG STYLES
       ========================================================================== */
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }

    .discover-portal-wrapper {
      width: 100%;
      margin-bottom: 44px;
    }

    .discover-ux-banner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
      background: linear-gradient(90deg, rgba(16, 185, 129, 0.12), rgba(59, 130, 246, 0.12));
      border: 1px solid rgba(59, 130, 246, 0.32);
      border-left: 4px solid #10b981;
      border-radius: 12px;
      padding: 12px 18px;
      margin-bottom: 26px;
      font-size: 13px;
      color: #e2e8f0;
    }
    .ux-banner-left {
      display: flex;
      align-items: center;
      gap: 10px;
      line-height: 1.45;
      flex: 1;
      min-width: 280px;
    }
    .ux-pulse-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      flex-shrink: 0;
    }
    .ux-code-pill {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      padding: 1px 6px;
      border-radius: 5px;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .ux-banner-right {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .ux-stat-pill {
      font-size: 11.5px;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 4px 10px;
      border-radius: 8px;
      color: #cbd5e1;
      font-family: 'JetBrains Mono', monospace;
    }
    .ux-stat-pill.pill-emerald strong { color: #34d399; }
    .ux-stat-pill.pill-blue strong { color: #60a5fa; }

    .discover-section-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 18px;
      padding-bottom: 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .sec-eyebrow {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #34d399;
      margin-bottom: 4px;
      font-family: 'JetBrains Mono', monospace;
    }
    .sec-title {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin: 0 0 6px 0;
      color: #f8fafc;
    }
    .sec-subtitle {
      font-size: 13.5px;
      color: #94a3b8;
      margin: 0;
      max-width: 780px;
      line-height: 1.45;
    }
    .sec-subtitle code, .ribbon-title code {
      font-family: 'JetBrains Mono', monospace;
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.15);
      padding: 1px 6px;
      border-radius: 4px;
    }

    /* BENTO GRID FOR TOP FINANCIAL MARKET NEWS */
    .market-bento-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }
    .market-bento-grid > .discover-tile {
      grid-column: span 4;
    }
    .market-bento-grid > .discover-tile.discover-tile-hero {
      grid-column: span 8;
      background: linear-gradient(145deg, #131c31 0%, #0f172a 100%);
      border-color: rgba(16, 185, 129, 0.32);
    }
    @media (max-width: 1024px) {
      .market-bento-grid > .discover-tile,
      .market-bento-grid > .discover-tile.discover-tile-hero {
        grid-column: span 6;
      }
    }
    @media (max-width: 680px) {
      .market-bento-grid > .discover-tile,
      .market-bento-grid > .discover-tile.discover-tile-hero {
        grid-column: span 12;
      }
    }

    /* DISCOVER TILE CARD */
    .discover-tile {
      background: #111827;
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      position: relative;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }
    .discover-tile:hover, .discover-tile:focus-visible {
      transform: translateY(-3px);
      border-color: rgba(59, 130, 246, 0.5);
      box-shadow: 0 14px 30px -8px rgba(59, 130, 246, 0.28);
      outline: none;
    }
    .discover-tile.port-tile-post:hover, .discover-tile.port-tile-post:focus-visible {
      border-color: rgba(16, 185, 129, 0.55);
      box-shadow: 0 14px 30px -8px rgba(16, 185, 129, 0.28);
    }

    .tile-header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }
    .tile-cat-pill {
      font-size: 11px;
      font-weight: 700;
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.14);
      border: 1px solid rgba(59, 130, 246, 0.3);
      padding: 3px 9px;
      border-radius: 999px;
    }
    .tile-impact-tag {
      font-size: 10px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.04em;
    }
    .impact-emerald {
      background: rgba(16, 185, 129, 0.16);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .impact-amber {
      background: rgba(245, 158, 11, 0.16);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .impact-blue {
      background: rgba(59, 130, 246, 0.16);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .impact-purple {
      background: rgba(168, 85, 247, 0.16);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.35);
    }

    .tile-visual-wrap {
      background: rgba(9, 13, 22, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
      padding: 6px 10px;
      margin-bottom: 12px;
      overflow: hidden;
    }
    .tile-art-svg {
      width: 100%;
      height: 76px;
      display: block;
    }
    .discover-tile-hero .tile-art-svg {
      height: 98px;
    }

    .tile-headline {
      font-size: 17px;
      font-weight: 700;
      color: #f8fafc;
      line-height: 1.38;
      margin: 0 0 10px 0;
      letter-spacing: -0.01em;
    }
    .discover-tile-hero .tile-headline {
      font-size: 20px;
    }
    .tile-summary {
      font-size: 13.2px;
      color: #cbd5e1;
      line-height: 1.55;
      margin: 0 0 14px 0;
    }

    .tile-metrics-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      background: rgba(15, 23, 42, 0.72);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
      padding: 9px 10px;
      margin-bottom: 14px;
    }
    .tile-mini-stat {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .tms-lbl {
      font-size: 9.5px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: #94a3b8;
    }
    .tms-val {
      font-size: 12px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #f8fafc;
    }
    .tms-val.tone-bull { color: #34d399; }
    .tms-val.tone-warn { color: #fcd34d; }
    .tms-val.tone-bear { color: #f87171; }
    .tms-val.tone-blue { color: #60a5fa; }

    .tile-tickers-row {
      margin-bottom: 14px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
    }
    .tile-tickers-label {
      display: block;
      font-size: 10.5px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 7px;
    }
    .tile-pills-wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    /* INTERACTIVE STOCK / TICKER PILL LINKS */
    .stock-pill-link {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 7px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s ease;
      position: relative;
      z-index: 3;
    }
    .stock-pill-link.pill-post {
      background: rgba(16, 185, 129, 0.16);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.42);
    }
    .stock-pill-link.pill-post:hover,
    .stock-pill-link.pill-post:is(:interest-source, .interest-source) {
      background: rgba(16, 185, 129, 0.32);
      color: #ffffff;
      border-color: #10b981;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.45);
      transform: translateY(-1px);
    }
    .stock-pill-link.pill-pre {
      background: rgba(59, 130, 246, 0.16);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.38);
    }
    .stock-pill-link.pill-pre:hover,
    .stock-pill-link.pill-pre:is(:interest-source, .interest-source) {
      background: rgba(59, 130, 246, 0.32);
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 0 12px rgba(59, 130, 246, 0.45);
      transform: translateY(-1px);
    }
    .stock-pill-link.pill-watch {
      background: rgba(255, 255, 255, 0.05);
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .stock-pill-link.pill-watch:hover,
    .stock-pill-link.pill-watch:is(:interest-source, .interest-source) {
      background: rgba(255, 255, 255, 0.14);
      color: #ffffff;
      border-color: #94a3b8;
    }
    .pill-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      display: inline-block;
    }
    .dot-emerald { background: #10b981; box-shadow: 0 0 6px #10b981; }
    .dot-blue { background: #3b82f6; box-shadow: 0 0 6px #3b82f6; }
    .dot-slate { background: #64748b; }
    .pill-tag {
      font-size: 9px;
      padding: 1px 4px;
      border-radius: 4px;
      background: rgba(0, 0, 0, 0.35);
      color: #e2e8f0;
      white-space: nowrap;
    }
    .tile-primary-pill { flex-shrink: 0; white-space: nowrap; }

    .tile-footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      flex-wrap: wrap;
    }
    .tile-meta-left {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11.5px;
      color: #94a3b8;
      flex-wrap: wrap;
    }
    .tile-sources-badge {
      color: #cbd5e1;
      font-weight: 600;
    }
    .tile-open-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(59, 130, 246, 0.16);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.35);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .tile-open-btn:hover {
      background: #3b82f6;
      color: #ffffff;
      border-color: #3b82f6;
    }
    .tile-direct-report-link {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: rgba(16, 185, 129, 0.16);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.38);
      border-radius: 8px;
      padding: 6px 11px;
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.15s ease;
      position: relative;
      z-index: 3;
    }
    .port-tile-pre .tile-direct-report-link {
      background: rgba(59, 130, 246, 0.15);
      color: #93c5fd;
      border-color: rgba(59, 130, 246, 0.35);
    }
    .tile-direct-report-link:hover {
      background: #059669;
      color: #ffffff;
      border-color: #10b981;
    }
    .port-tile-pre .tile-direct-report-link:hover {
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
    }

    /* PORTFOLIO CONTROLS & RIBBON */
    .port-news-controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .port-type-tabs {
      display: flex;
      flex-wrap: wrap;
      max-width: 100%;
      min-width: 0;
      gap: 6px;
      background: #0f172a;
      padding: 4px;
      border-radius: 10px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .port-tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: #94a3b8;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 7px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: inherit;
      transition: all 0.15s ease;
    }
    .port-tab-btn:hover { color: #f8fafc; }
    .port-tab-btn.active {
      background: #1e293b;
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.15);
    }
    .port-search-input-wrap {
      display: flex;
      align-items: center;
      gap: 8px;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 6px 12px;
      min-width: 240px;
    }
    .port-search-input-wrap input {
      background: transparent;
      border: none;
      color: #f8fafc;
      font-size: 12.5px;
      font-family: inherit;
      width: 100%;
      outline: none;
    }

    .portfolio-ribbon-card {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 14px 16px;
      margin-bottom: 20px;
    }
    .ribbon-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 10px;
      font-size: 12px;
      color: #cbd5e1;
    }
    .ribbon-legend {
      display: flex;
      gap: 14px;
      font-size: 11.5px;
      color: #94a3b8;
    }
    .ribbon-legend span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .ribbon-pills-container {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    /* PORTFOLIO NEWS TILES GRID */
    .portfolio-tiles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(360px, 100%), 1fr));
      gap: 18px;
    }
    .tile-stock-id {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tile-comp-name {
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
      min-width: 0;
      overflow-wrap: anywhere;
    }
    .tile-status-badge {
      font-size: 10.5px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 8px;
      border-radius: 6px;
    }
    .status-post {
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .status-pre {
      background: rgba(59, 130, 246, 0.16);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.35);
    }
    .status-pending {
      background: rgba(245, 158, 11, 0.14);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .port-tile-pending { border-style: dashed; }

    /* Portal-scoped tab dots (index.html's .dot-pre/.dot-post are not available on news.html) */
    .port-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; margin-right: 2px; vertical-align: 1px; }
    .port-dot-post { background: #10b981; }
    .port-dot-pre { background: #3b82f6; }
    .port-dot-pending { background: #f59e0b; }
    .port-empty-state {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 14px;
      padding: 18px;
      border: 1px dashed rgba(148, 163, 184, 0.35);
      border-radius: 12px;
      color: #94a3b8;
      font-size: 13px;
      text-align: center;
    }
    .port-empty-state[hidden] { display: none; }
    .port-empty-state strong { color: #e2e8f0; }

    /* Bento last-row spans (set at build time so the grid never leaves an orphan tile) */
    .market-bento-grid > .discover-tile.tile-span-6 { grid-column: span 6; }
    .market-bento-grid > .discover-tile.tile-span-12 { grid-column: span 12; }
    @media (max-width: 680px) {
      .market-bento-grid > .discover-tile.tile-span-6,
      .market-bento-grid > .discover-tile.tile-span-12 { grid-column: span 12; }
    }
    [id^="section-"] { scroll-margin-top: 84px; }

    /* Data-driven tile chart: dashed band = T-1 implied move, dot = actual after-hours move */
    .tile-art-svg.tile-chart { width: 100%; height: auto; max-height: 128px; }
    .discover-tile-hero .tile-art-svg.tile-chart { max-height: 170px; }
    .tile-chart.chart-narrow { display: none; }
    .tile-span-12 .tile-art-svg.tile-chart { max-width: 560px; margin: 0 auto; }
    .tile-chart .ch-pre { fill: #93c5fd; }
    .hc-src { color: #93c5fd; font-weight: 700; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.02em; }
    @media (max-width: 680px) {
      .tile-chart.chart-wide { display: none; }
      .tile-chart.chart-narrow { display: block; }
      .port-tab-btn { flex: 1 1 auto; justify-content: center; }
      .port-search-input-wrap { min-width: 0; flex: 1 1 100%; }
    }
    .tile-chart .ch-val { font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace; stroke: none; }
    .tile-digest { list-style: none; margin: 0 0 14px 0; padding: 0; display: grid; gap: 6px; }
    .tile-digest li { font-size: 12.4px; line-height: 1.5; color: #cbd5e1; padding: 7px 10px; border-radius: 8px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.05); }
    .tile-digest li strong { color: #f8fafc; }
    .tile-chart .ch-cap { fill: #94a3b8; font-size: 10px; font-family: 'Inter', sans-serif; }
    .tile-chart .ch-lbl { fill: #cbd5e1; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .tile-chart .ch-zero { stroke: rgba(148, 163, 184, 0.45); stroke-width: 1; }
    .tile-chart .ch-band { fill: rgba(148, 163, 184, 0.12); stroke: rgba(148, 163, 184, 0.55); stroke-dasharray: 3 2; }
    .tile-chart .ch-band-pre { fill: rgba(59, 130, 246, 0.16); stroke: rgba(96, 165, 250, 0.7); }
    .tile-chart .ch-stem { stroke-width: 2; }
    .tile-chart .ch-dot { stroke: #0b111c; stroke-width: 1.5; }
    .tile-chart .ch-up { stroke: #34d399; fill: #34d399; }
    .tile-chart .ch-down { stroke: #f87171; fill: #f87171; }
    .tile-chart .ch-flat { stroke: #94a3b8; fill: #94a3b8; }
    .tile-chart .ch-dot.ch-out { stroke: #fbbf24; stroke-width: 2.5; }

    /* Modal ground-truth ledger */
    .dm-ledger {
      margin: 6px 0 22px 0;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      background: rgba(9, 13, 22, 0.55);
      padding: 10px 14px;
    }
    .dm-ledger summary { cursor: pointer; font-size: 13px; font-weight: 700; color: #e2e8f0; }
    .dm-ledger-src { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94a3b8; word-break: break-all; }
    .tile-verdict-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-size: 11.5px;
    }
    .verdict-chip {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: #fcd34d;
      background: rgba(245, 158, 11, 0.12);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 2px 8px;
      border-radius: 5px;
    }
    .port-tile-post .verdict-chip {
      color: #34d399;
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.3);
    }
    .verdict-date {
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }

    /* ==========================================================================
       MODERN-WEB-GUIDANCE HOVERCARD (popover="hint" + interestfor + Anchor Pos)
       ========================================================================== */
    [interestfor] {
      --interest-delay-start: 0.2s;
      interest-delay-start: var(--interest-delay-start);
      --interest-delay-end: 0.1s;
      interest-delay-end: var(--interest-delay-end);
      interest-delay: 0.2s 0.1s;
    }
    :root:has(:is(:interest-source, .interest-source)) [interestfor] {
      --interest-delay-start: 0s;
      interest-delay-start: 0s;
    }

    /* Positioned by JS (getBoundingClientRect fallback from the hovercard guide) because CSS anchor
       positioning is not available in Chrome/Edge/Firefox. One card is shared by many triggers, so it
       must be re-anchored to whichever trigger opened it; it stays invisible until that happens. */
    [popover].hovercard {
      position: fixed;
      inset: auto;
      top: 0;
      left: 0;
      margin: 0;
      width: min(430px, calc(100vw - 24px));
      max-height: calc(100vh - 24px);
      overflow-y: auto;
      overscroll-behavior: contain;
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid rgba(59, 130, 246, 0.45);
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.75), 0 0 0 1px rgba(255, 255, 255, 0.08);
      z-index: 9999;
      opacity: 0;
      transform-origin: top left;
      pointer-events: auto;
    }
    [popover].hovercard:not([data-positioned]) {
      visibility: hidden;
    }
    [popover].hovercard[data-placement="above"] {
      transform-origin: bottom left;
    }
    [popover].hovercard.hc-post {
      border-color: rgba(16, 185, 129, 0.55);
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.8), 0 0 20px rgba(16, 185, 129, 0.2);
    }
    [popover].hovercard:is(:popover-open, .\\:popover-open, .hc-fallback-open) {
      display: block;
      opacity: 1;
      transform: translateY(0) scale(1);
    }
    @starting-style {
      [popover].hovercard:is(:popover-open, .\\:popover-open) {
        opacity: 0;
        transform: translateY(-8px) scale(0.96);
      }
    }
    @media (prefers-reduced-motion: no-preference) {
      [popover].hovercard {
        transition:
          opacity 0.22s ease,
          transform 0.22s ease,
          display 0.22s allow-discrete,
          overlay 0.22s allow-discrete;
        transition-behavior: allow-discrete;
      }
    }

    .hc-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }
    .hc-id {
      display: flex;
      align-items: baseline;
      gap: 8px;
    }
    .hc-sym {
      font-family: 'JetBrains Mono', monospace;
      font-size: 18px;
      font-weight: 800;
      color: #34d399;
    }
    .hc-pre .hc-sym { color: #60a5fa; }
    .hc-name {
      font-size: 13px;
      font-weight: 700;
      color: #f1f5f9;
    }
    .hc-badge {
      font-size: 9.5px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 5px;
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .hc-pre .hc-badge {
      background: rgba(59, 130, 246, 0.18);
      color: #93c5fd;
      border-color: rgba(59, 130, 246, 0.35);
    }
    .hc-verdict-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.04);
      padding: 5px 10px;
      border-radius: 7px;
      margin-bottom: 10px;
    }
    .hc-verdict-bar strong { color: #fcd34d; font-family: 'JetBrains Mono', monospace; }
    .hc-post .hc-verdict-bar strong { color: #34d399; }
    .hc-date { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #94a3b8; }

    .hc-price-strip {
      display: grid;
      grid-template-columns: 1.3fr 1fr 1fr;
      gap: 6px;
      background: rgba(9, 13, 22, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 8px;
      padding: 8px;
      margin-bottom: 10px;
    }
    .hc-p-cell { display: flex; flex-direction: column; gap: 2px; }
    .hc-p-lbl { font-size: 9.5px; color: #94a3b8; text-transform: uppercase; }
    .hc-p-val { font-size: 11.5px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #f8fafc; }
    .hc-pos { color: #34d399; }
    .hc-neg { color: #f87171; }

    .hc-metrics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 10px;
    }
    .hc-m-box {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 7px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .hc-m-lbl { font-size: 9.5px; color: #94a3b8; text-transform: uppercase; }
    .hc-m-val { font-size: 11.5px; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #e2e8f0; }
    .hc-m-val small { color: #34d399; font-size: 10.5px; }
    .hc-m-sub { font-size: 10px; color: #94a3b8; }

    .hc-driver {
      font-size: 11.5px;
      line-height: 1.45;
      color: #cbd5e1;
      margin: 0 0 8px 0;
    }
    .hc-guidance-box {
      font-size: 11px;
      line-height: 1.4;
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.1);
      border-left: 3px solid #3b82f6;
      padding: 5px 8px;
      border-radius: 5px;
      margin-bottom: 8px;
    }
    .hc-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      padding-top: 8px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 10.5px;
      color: #94a3b8;
      flex-wrap: wrap;
    }
    .hc-cta-hint {
      color: #34d399;
      font-weight: 700;
    }

    /* ==========================================================================
       MODERN-WEB-GUIDANCE MODAL DIALOG (<dialog closedby="any">)
       ========================================================================== */
    dialog#discover-article-dialog {
      max-width: 920px;
      width: calc(100vw - 32px);
      max-height: calc(100vh - 48px);
      background: #0f172a;
      color: #f8fafc;
      border: 1px solid rgba(59, 130, 246, 0.4);
      border-radius: 18px;
      padding: 0;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
      overflow-y: auto;
    }
    dialog#discover-article-dialog[open] {
      display: flex;
      flex-direction: column;
    }
    /* MANDATORY (both rules): stops scroll gestures in the dialog or backdrop chaining to the page */
    dialog:modal {
      overscroll-behavior: contain;
    }
    dialog::backdrop {
      overflow: hidden;
      overscroll-behavior: contain;
      background-color: rgba(5, 8, 15, 0.78);
      backdrop-filter: blur(6px);
    }

    .discover-modal-inner {
      display: flex;
      flex-direction: column;
      width: 100%;
    }
    .discover-modal-topbar {
      position: sticky;
      top: 0;
      z-index: 10;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }
    .dm-breadcrumbs {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .dm-sec-badge {
      font-size: 10.5px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      padding: 3px 9px;
      border-radius: 6px;
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .dm-cat-badge {
      font-size: 11.5px;
      font-weight: 700;
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.15);
      padding: 3px 9px;
      border-radius: 6px;
    }
    .dm-meta-text {
      font-size: 12px;
      color: #94a3b8;
      font-family: 'JetBrains Mono', monospace;
    }
    .dm-close-form { margin: 0; }
    .dm-close-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #e2e8f0;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 11.5px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .dm-close-btn:hover {
      background: rgba(239, 68, 68, 0.25);
      border-color: #ef4444;
      color: #ffffff;
    }

    .discover-modal-body {
      padding: 26px 28px 32px 28px;
    }
    .dm-headline {
      font-size: 26px;
      font-weight: 800;
      line-height: 1.3;
      letter-spacing: -0.02em;
      color: #ffffff;
      margin: 0 0 14px 0;
    }
    .dm-lead {
      font-size: 15px;
      line-height: 1.6;
      color: #cbd5e1;
      background: rgba(255, 255, 255, 0.03);
      border-left: 4px solid #3b82f6;
      padding: 12px 16px;
      border-radius: 8px;
      margin: 0 0 22px 0;
    }
    .dm-subhead {
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #93c5fd;
      margin-bottom: 10px;
      font-family: 'JetBrains Mono', monospace;
    }
    .dm-sources-section {
      margin-bottom: 20px;
    }
    .dm-sources-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
    }
    .dm-source-card {
      background: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .dm-src-top {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 700;
      color: #f1f5f9;
    }
    .dm-src-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      background: rgba(59, 130, 246, 0.25);
      color: #93c5fd;
      padding: 1px 6px;
      border-radius: 4px;
    }
    .dm-src-detail {
      font-size: 11.5px;
      color: #94a3b8;
      line-height: 1.35;
    }

    .dm-tickers-bar {
      background: rgba(17, 24, 39, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .dm-tickers-lbl {
      font-size: 12px;
      font-weight: 600;
      color: #cbd5e1;
    }
    .dm-tickers-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .dm-metrics-strip {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-bottom: 22px;
    }
    .dm-metric-box {
      background: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 10px;
      padding: 12px 14px;
    }
    .dm-m-lbl {
      font-size: 10.5px;
      text-transform: uppercase;
      color: #94a3b8;
      display: block;
      margin-bottom: 4px;
    }
    .dm-m-val {
      font-size: 16px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: #34d399;
    }

    .dm-takeaways-card {
      background: linear-gradient(145deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.95));
      border: 1px solid rgba(16, 185, 129, 0.3);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 24px;
    }
    .dm-takeaways-list {
      margin: 0;
      padding-left: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 14px;
      line-height: 1.6;
      color: #e2e8f0;
    }

    .dm-narrative-sec {
      margin-bottom: 22px;
    }
    .dm-narrative-sec h3 {
      font-size: 17px;
      font-weight: 700;
      color: #f8fafc;
      margin: 0 0 10px 0;
      padding-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }
    .dm-narrative-sec p, .dm-narrative-body {
      font-size: 14px;
      line-height: 1.65;
      color: #cbd5e1;
      margin: 0 0 10px 0;
    }
    .modal-table-wrap {
      overflow-x: auto;
      margin-top: 8px;
    }
    .modal-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
    }
    .modal-table th, .modal-table td {
      padding: 8px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      text-align: left;
    }
    .modal-table th {
      color: #93c5fd;
      font-size: 11px;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.03);
    }
    .modal-badge {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      padding: 2px 7px;
      border-radius: 5px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-weight: 700;
    }
    .qa-block {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 10px;
      padding: 12px 14px;
      margin-bottom: 10px;
    }
    .qa-analyst { color: #93c5fd; font-size: 13px; margin-bottom: 6px; }
    .qa-q { color: #e2e8f0; font-size: 13px; margin-bottom: 6px; line-height: 1.5; }
    .qa-a { color: #cbd5e1; font-size: 13px; line-height: 1.55; }

    .dm-footer-cta {
      margin-top: 24px;
      padding-top: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .dm-primary-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: linear-gradient(135deg, #059669, #10b981);
      color: #ffffff;
      text-decoration: none;
      font-weight: 700;
      font-size: 14px;
      padding: 11px 20px;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
      transition: transform 0.15s ease;
    }
    .dm-primary-cta-btn:hover {
      transform: translateY(-2px);
    }
    .dm-secondary-cta-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(59, 130, 246, 0.18);
      border: 1px solid rgba(59, 130, 246, 0.4);
      color: #93c5fd;
      text-decoration: none;
      font-weight: 700;
      font-size: 13px;
      padding: 10px 16px;
      border-radius: 10px;
    }
    """


_PORTAL_JS_TEMPLATE = """
  <!-- CONDITIONAL POLYFILLS PER MODERN-WEB-GUIDANCE (hovercard); versions pinned -->
  <script type="module">
    if (!("popover" in HTMLElement.prototype)) {
      import("https://unpkg.com/@oddbird/popover-polyfill@0.7.3/dist/popover.min.js").catch(() => {});
    }
    if (!HTMLButtonElement.prototype.hasOwnProperty("interestForElement")) {
      import("https://unpkg.com/interestfor@1.0.10/src/interestfor.min.js").catch(() => {});
    }
  </script>

  <script>
    const DISCOVER_ARTICLES = __ARTICLES_JSON__;
    const PORTFOLIO_TICKER_META = __TICKER_META_JSON__;

    (function initDiscoverPortal() {
      const dialog = document.getElementById('discover-article-dialog');
      const ESC_MAP = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
      const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ESC_MAP[c]);
      const NATIVE_POPOVER = 'popover' in HTMLElement.prototype;

      // MANDATORY fallback for browsers without closedby support (light-dismiss-a-dialog)
      if (dialog && !('closedBy' in HTMLDialogElement.prototype)) {
        dialog.addEventListener('click', (event) => {
          if (event.target !== dialog) return;
          const rect = dialog.getBoundingClientRect();
          const isDialogContent = (
            rect.top <= event.clientY && event.clientY <= rect.top + rect.height &&
            rect.left <= event.clientX && event.clientX <= rect.left + rect.width
          );
          if (!isDialogContent) dialog.close();
        });
      }
      if (dialog) {
        dialog.addEventListener('close', () => {
          dialog.returnValue = '';
          dialog.querySelectorAll(':scope > .hovercard').forEach((card) => {
            try { if (card.matches(':popover-open')) card.hidePopover(); } catch (_) {}
            if (card._home) card._home.appendChild(card);
          });
        });
      }

      function tickerState(tk) {
        const info = PORTFOLIO_TICKER_META[tk] || { url: '#section-portfolio-news', state: 'watchlist' };
        return { info, isPost: info.state === 'post', isPre: info.state === 'pre_upcoming' || info.state === 'pre_reported' };
      }

      function buildModalTickerPillHTML(tk) {
        const { info, isPost, isPre } = tickerState(tk);
        const modeCls = isPost ? 'pill-post' : (isPre ? 'pill-pre' : 'pill-watch');
        const dotCls = isPost ? 'dot-emerald' : (isPre ? 'dot-blue' : 'dot-slate');
        const tag = isPost ? '<span class="pill-tag">T+0 POST</span>' : (isPre ? '<span class="pill-tag">T-1 PRE</span>' : '');
        const filter = (!isPost && !isPre) ? ` data-filter-ticker="${esc(tk)}"` : '';
        return `<a href="${esc(info.url)}" interestfor="hovercard-${esc(tk)}" data-hovercard-id="hovercard-${esc(tk)}" data-ticker="${esc(tk)}"${filter} class="stock-pill-link ${modeCls}"><span class="pill-dot ${dotCls}" aria-hidden="true"></span><span class="pill-sym">$${esc(tk)}</span>${tag}</a>`;
      }

      function openDiscoverArticle(articleId) {
        const art = DISCOVER_ARTICLES[articleId];
        if (!art || !dialog) return;

        document.getElementById('dm-section-badge').textContent = art.section || 'AI DISCOVER SYNTHESIS';
        document.getElementById('dm-category-badge').textContent = art.category || '';
        document.getElementById('dm-meta-text').textContent = [art.read_time, art.published].filter(Boolean).join(' • ');
        document.getElementById('discover-article-title').textContent = art.headline || '';
        document.getElementById('dm-lead-summary').textContent = art.summary || '';

        document.getElementById('dm-sources-grid').innerHTML = (art.sources || []).map((s) => `
          <div class="dm-source-card">
            <div class="dm-src-top"><span class="dm-src-num">[${esc(s.id)}]</span><span>${esc(s.name)}</span></div>
            <div class="dm-src-detail">${esc(s.detail)}</div>
          </div>`).join('');

        const tkList = document.getElementById('dm-tickers-list');
        tkList.innerHTML = (art.tickers || []).map((tk) => buildModalTickerPillHTML(tk)).join(' ');
        bindHovercardTriggers(tkList);

        document.getElementById('dm-metrics-strip').innerHTML = (art.metrics_strip || []).map((m) => `
          <div class="dm-metric-box">
            <span class="dm-m-lbl">${esc(m.label)}</span>
            <span class="dm-m-val">${esc(m.val)}</span>
          </div>`).join('');

        // Takeaways and narrative bodies are built (and escaped) at build time by build_news_portal.py
        document.getElementById('dm-takeaways-list').innerHTML = (art.key_takeaways || []).map((t) => `<li>${t}</li>`).join('');
        document.getElementById('dm-narrative-container').innerHTML = (art.sections || []).map((sec) => `
          <div class="dm-narrative-sec">
            <h3>${esc(sec.heading)}</h3>
            <div class="dm-narrative-body">${sec.body}</div>
          </div>`).join('');

        const ledger = document.getElementById('dm-ledger');
        // Ledger rows: [label, value, file_index (-1 = derived), json_path_or_note]
        const ledgerFiles = art.ledger_files || [];
        document.getElementById('dm-ledger-body').innerHTML = (art.ledger || []).map((r) => {
          const src = r[2] >= 0 ? ledgerFiles[r[2]] + (r[3] ? ' → ' + r[3] : '') : r[3];
          return `<tr><td>${esc(r[0])}</td><td><strong>${esc(r[1])}</strong></td><td class="dm-ledger-src">${esc(src)}</td></tr>`;
        }).join('');
        if (ledger) {
          ledger.open = false;
          ledger.hidden = !(art.ledger || []).length;
        }

        // Single-ticker briefs link to that ticker's tearsheet; multi-ticker market briefs link to the filtered library
        const pTk = art.primary_ticker || ((art.tickers || []).length === 1 ? art.tickers[0] : '');
        const { info: pInfo, isPost: pPost } = tickerState(pTk);
        const targetUrl = art.primary_report_url || (pTk ? pInfo.url : '') || '';
        let ctaHtml = '<div style="font-size:12.5px;color:#94a3b8;">💡 Tip: Hover any <strong>$TICKER</strong> chip above for its pop-up summary, or click it to open its tearsheet.</div><div style="display:flex;gap:10px;flex-wrap:wrap;">';
        if (!pTk && art.library_filter) {
          const lbl = art.library_filter === 'post' ? 'Browse All T+0 Post-Earnings Tearsheets →' : 'Browse All T-1 Pre-Earnings Briefings →';
          ctaHtml += `<a href="index.html?filter=${esc(art.library_filter)}#section-tearsheet-library" class="dm-primary-cta-btn">${lbl}</a>`;
        }
        if (pTk && targetUrl && !targetUrl.startsWith('#')) {
          const btnText = (art.report_type === 'post' || (!art.report_type && pPost))
            ? `Open Full ${esc(pTk)} T+0 Post-Earnings Forensic Tearsheet →`
            : `Open Full ${esc(pTk)} T-1 Pre-Earnings Briefing →`;
          ctaHtml += `<a href="${esc(targetUrl)}" class="dm-primary-cta-btn">${btnText}</a>`;
        }
        if (art.pre_report_url && art.pre_report_url !== targetUrl) {
          ctaHtml += `<a href="${esc(art.pre_report_url)}" class="dm-secondary-cta-btn">Compare Paired ${esc(pTk)} T-1 Briefing</a>`;
        }
        document.getElementById('dm-footer-cta').innerHTML = ctaHtml + '</div>';

        dialog.showModal();
      }

      // Tile clicks open the Discover modal; links inside tiles (tickers, tearsheets) keep their own behaviour.
      // The tile's "Read AI Synthesis" / "AI Discover Brief" <button> is the keyboard-accessible control.
      document.querySelectorAll('.discover-tile').forEach((tile) => {
        tile.addEventListener('click', (e) => {
          if (e.target.closest('a')) return;
          const artId = tile.getAttribute('data-article-id');
          if (artId) openDiscoverArticle(artId);
        });
      });

      // Portfolio News Filter Tabs, Search & Empty State
      let portFilter = 'all';
      let portQuery = '';
      const portSearchInput = document.getElementById('portfolioNewsSearch');
      const emptyEl = document.getElementById('portfolioNewsEmpty');
      const emptyText = document.getElementById('portfolioNewsEmptyText');

      function filterPortfolioNews() {
        const q = portQuery.replace(/\\$/g, '').trim().toLowerCase();
        // A known ticker ($U, $AI, $NET) matches exactly; anything else is a free-text ticker / company search
        const exact = !!PORTFOLIO_TICKER_META[q.toUpperCase()];
        let visible = 0;
        document.querySelectorAll('.portfolio-news-tile').forEach((tile) => {
          const matchType = portFilter === 'all' || tile.getAttribute('data-port-type') === portFilter;
          const tk = (tile.getAttribute('data-ticker') || '').toLowerCase();
          const comp = (tile.getAttribute('data-company') || '').toLowerCase();
          const show = matchType && (!q || (exact ? tk === q : (tk.includes(q) || comp.includes(q))));
          tile.style.display = show ? '' : 'none';
          if (show) visible += 1;
        });
        if (!emptyEl) return;
        emptyEl.hidden = visible > 0;
        if (!visible && emptyText) {
          const meta = PORTFOLIO_TICKER_META[q.toUpperCase()];
          emptyText.textContent = (meta && meta.state === 'watchlist')
            ? `$${q.toUpperCase()} is on your tickers.txt watchlist with no T-1 or T+0 report yet. Its T-1 briefing is generated automatically when its earnings window opens.`
            : 'Try another ticker or filter. Watchlist names get a T-1 briefing automatically when their earnings window opens.';
        }
      }

      function setPortFilter(value) {
        portFilter = value;
        document.querySelectorAll('.port-tab-btn').forEach((b) => {
          const on = (b.getAttribute('data-port-filter') || 'all') === value;
          b.classList.toggle('active', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        filterPortfolioNews();
      }

      document.querySelectorAll('.port-tab-btn').forEach((btn) => {
        btn.addEventListener('click', () => setPortFilter(btn.getAttribute('data-port-filter') || 'all'));
      });
      if (portSearchInput) {
        portSearchInput.addEventListener('input', (e) => {
          portQuery = (e.target.value || '').trim().toLowerCase();
          filterPortfolioNews();
        });
      }

      // Watchlist tickers have no tearsheet yet: clicking one filters Portfolio News to that ticker instead.
      document.addEventListener('click', (e) => {
        const pill = e.target.closest('[data-filter-ticker]');
        if (!pill) return;
        e.preventDefault();
        const tk = pill.getAttribute('data-filter-ticker') || '';
        if (dialog && dialog.open) dialog.close();
        if (activeHovercard) hideHovercardImmediate(activeHovercard, activeTrigger);
        if (portSearchInput) portSearchInput.value = tk;
        portQuery = tk.toLowerCase();
        setPortFilter('all');
        const sec = document.getElementById('section-portfolio-news');
        if (sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });

      // Progressive-Enhancement Hovercard Controller:
      // one card is shared by many triggers, so it is re-anchored to whichever trigger opened it and stays
      // invisible (CSS :not([data-positioned])) until it has been measured and placed inside the viewport.
      let activeHovercard = null;
      let activeTrigger = null;
      let showTimer = null;
      let hideTimer = null;

      function positionHovercard(trigger, card) {
        const rect = trigger.getBoundingClientRect();
        const vw = window.innerWidth;
        const vh = window.innerHeight;
        const pad = 12;
        const gap = 8;
        const cardWidth = Math.min(430, vw - 2 * pad);
        card.style.maxHeight = '';
        const natural = card.offsetHeight || 320;
        const left = Math.max(pad, Math.min(rect.left, vw - cardWidth - pad));
        const roomBelow = vh - rect.bottom - gap - pad;
        const roomAbove = rect.top - gap - pad;
        // Prefer below, then above; if neither fits, use the roomier side and let the card scroll so it never covers its trigger.
        let placement = natural <= roomBelow ? 'below' : (natural <= roomAbove ? 'above' : (roomBelow >= roomAbove ? 'below' : 'above'));
        const room = placement === 'below' ? roomBelow : roomAbove;
        const cardHeight = Math.min(natural, Math.max(160, room));
        if (cardHeight < natural) card.style.maxHeight = cardHeight + 'px';
        let top = placement === 'below' ? rect.bottom + gap : rect.top - gap - cardHeight;
        top = Math.max(pad, Math.min(top, vh - cardHeight - pad));
        card.style.left = left + 'px';
        card.style.top = top + 'px';
        card.dataset.placement = placement;
        card.dataset.positioned = '';
      }

      function resetHovercard(card) {
        card.classList.remove('interest-target', 'hc-fallback-open');
        delete card.dataset.positioned;
      }

      function showHovercard(trigger, card) {
        clearTimeout(hideTimer);
        if (activeHovercard && activeHovercard !== card) {
          hideHovercardImmediate(activeHovercard, activeTrigger);
        }
        activeHovercard = card;
        activeTrigger = trigger;
        // A modal <dialog> makes everything outside it inert, so cards opened from modal pills move inside it
        if (dialog && dialog.open && trigger.closest('dialog') === dialog && card.parentNode !== dialog) {
          card._home = card._home || card.parentNode;
          dialog.appendChild(card);
        }
        trigger.classList.add('interest-source');
        card.classList.add('interest-target');
        if (!NATIVE_POPOVER) card.classList.add('hc-fallback-open');
        try {
          if (NATIVE_POPOVER && !card.matches(':popover-open')) card.showPopover();
        } catch (_) {}
        positionHovercard(trigger, card);
      }

      function hideHovercardImmediate(card, trigger) {
        if (!card) return;
        resetHovercard(card);
        if (trigger) trigger.classList.remove('interest-source');
        try {
          if (NATIVE_POPOVER && card.matches(':popover-open')) card.hidePopover();
        } catch (_) {}
        if (activeHovercard === card) {
          activeHovercard = null;
          activeTrigger = null;
        }
      }

      function scheduleHide() {
        clearTimeout(showTimer);
        clearTimeout(hideTimer);
        hideTimer = setTimeout(() => {
          if (activeHovercard) hideHovercardImmediate(activeHovercard, activeTrigger);
        }, 140);
      }

      function bindHovercardTriggers(rootEl = document) {
        rootEl.querySelectorAll('[data-hovercard-id]').forEach((trigger) => {
          if (trigger.dataset.hcBound === '1') return;
          trigger.dataset.hcBound = '1';
          const card = document.getElementById(trigger.getAttribute('data-hovercard-id'));
          if (!card) return;
          trigger.addEventListener('mouseenter', () => {
            clearTimeout(hideTimer);
            clearTimeout(showTimer);
            showTimer = setTimeout(() => showHovercard(trigger, card), activeHovercard ? 30 : 150);
          });
          trigger.addEventListener('mouseleave', scheduleHide);
          trigger.addEventListener('focus', () => {
            clearTimeout(hideTimer);
            showHovercard(trigger, card);
          });
          trigger.addEventListener('blur', scheduleHide);
        });
      }

      document.querySelectorAll('.hovercard').forEach((card) => {
        card.addEventListener('mouseenter', () => clearTimeout(hideTimer));
        card.addEventListener('mouseleave', scheduleHide);
        // Native dismissal (Escape / light dismiss / lost interest) must not leave an orphaned, positioned card behind.
        card.addEventListener('toggle', (e) => {
          if (e.newState !== 'closed') return;
          resetHovercard(card);
          if (activeHovercard === card) {
            if (activeTrigger) activeTrigger.classList.remove('interest-source');
            activeHovercard = null;
            activeTrigger = null;
          }
        });
      });
      const reposition = () => {
        if (activeHovercard && activeTrigger) positionHovercard(activeTrigger, activeHovercard);
      };
      window.addEventListener('scroll', reposition, { passive: true });
      window.addEventListener('resize', reposition);

      bindHovercardTriggers(document);
    })();
  </script>
"""


def get_discover_portal_js(articles_json_str: str, intel: dict[str, dict]) -> str:
    """articles_json_str must come from build_discover_portal_section_html (already <script>-safe)."""
    tk_meta = {
        tk: {"url": entry.get("primary_report_url") or "#section-portfolio-news", "state": entry.get("state", "watchlist")}
        for tk, entry in intel.items()
    }
    payloads = {"ARTICLES": articles_json_str, "TICKER_META": safe_script_json(tk_meta)}
    # Single pass, so placeholder-like text inside a payload is never substituted again
    return re.sub(r"__(ARTICLES|TICKER_META)_JSON__", lambda m: payloads[m.group(1)], _PORTAL_JS_TEMPLATE)


def get_market_snapshot_safe() -> dict:
    """Fetch the US Markets quick-view snapshot (reuses a <2 min cache so multi-page builds fetch once)."""
    try:
        from market_snapshot import fetch_market_snapshot
        return fetch_market_snapshot(max_age_seconds=120)
    except Exception as exc:
        print(f"[news_portal] market snapshot unavailable: {exc}")
        return {"items": [], "as_of_display": "Market data unavailable"}


def render_market_strip_html(snapshot: dict) -> str:
    """Top-of-page US Markets quick view (indices, 10Y, VIX, Gold, Crude, BTC, US Private Equity)."""
    items = snapshot.get("items", [])
    if not items:
        # Skeleton cells (no values) so the live poller can still fill the strip after a build-time outage
        try:
            from market_snapshot import INSTRUMENTS, PE_BASKET
        except Exception:
            return ""
        items = [{"key": c["key"], "label": c["label"], "basket": c.get("basket"), "direction": "flat", "stale": True,
                  "last_fmt": "—", "change_fmt": "", "pct_fmt": "", "spark_line": "", "spark_area": "", "spark_base_y": 13}
                 for c in INSTRUMENTS]
        snapshot = {**snapshot, "pe_basket": PE_BASKET, "as_of_display": snapshot.get("as_of_display") or "Market data unavailable"}
    cells = []
    for it in items:
        name_html = html.escape(it["label"])
        if it.get("basket"):
            name_html += ' <span class="mq-tag">EW6</span>'
        cells.append(f"""
        <li class="mq-cell mq-{it['direction']}{' mq-stale' if it.get('stale') else ''}" data-mq-key="{it['key']}">
          <div class="mq-text">
            <span class="mq-name">{name_html}</span>
            <span class="mq-last">{html.escape(it['last_fmt'])}</span>
            <span class="mq-chg"><span class="mq-abs">{html.escape(it['change_fmt'])}</span> <span class="mq-pct">{html.escape(it['pct_fmt'])}</span></span>
          </div>
          <svg class="mq-spark" viewBox="0 0 64 26" preserveAspectRatio="none" aria-hidden="true">
            <line class="mq-base" x1="0" x2="64" y1="{it['spark_base_y']}" y2="{it['spark_base_y']}"/>
            <path class="mq-area" d="{it['spark_area']}"/>
            <path class="mq-line" d="{it['spark_line']}"/>
          </svg>
        </li>""")

    pe_note = ", ".join(snapshot.get("pe_basket", []))
    return f"""
  <section class="market-quickview" id="market-quickview" aria-label="US Markets quick view">
    <div class="mq-label">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="2"/><path d="M16.24 7.76a6 6 0 0 1 0 8.49M7.76 16.24a6 6 0 0 1 0-8.49M19.07 4.93a10 10 0 0 1 0 14.14M4.93 19.07a10 10 0 0 1 0-14.14"/></svg>
      <span>US Markets</span>
    </div>
    <ul class="mq-list">
      {"".join(cells)}
    </ul>
    <div class="mq-asof">
      <span class="mq-status" data-mq-status><span class="mq-live-dot" aria-hidden="true"></span><span data-mq-status-text>Snapshot</span></span>
      <span>As of <strong data-mq-asof>{html.escape(snapshot.get('as_of_display', ''))}</strong></span>
      <span class="mq-footnote">US Private Equity = EW {html.escape(pe_note)}</span>
    </div>
  </section>
"""


def get_market_strip_css() -> str:
    return """
    /* ==========================================================================
       US MARKETS QUICK-VIEW STRIP
       ========================================================================== */
    .market-quickview {
      width: 100%;
      display: grid;
      grid-template-columns: auto minmax(0, 1fr) auto;
      align-items: stretch;
      background: #0b111c;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      margin: 0 0 18px 0;
      overflow: hidden;
    }
    .mq-label {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 16px;
      font-size: 14px;
      font-weight: 700;
      color: #f8fafc;
      border-right: 1px solid rgba(255, 255, 255, 0.08);
      white-space: nowrap;
    }
    .mq-label svg { color: #34d399; }
    /* Wrapping grid (no internal scroller): every instrument stays visible at any width */
    .mq-list {
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(164px, 1fr));
      min-width: 0;
    }
    .mq-cell {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      min-width: 0;
      padding: 8px 12px;
      border-right: 1px solid rgba(255, 255, 255, 0.06);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    }
    .mq-text {
      display: flex;
      flex-direction: column;
      gap: 1px;
      min-width: 0;
    }
    .mq-name {
      font-size: 11.5px;
      font-weight: 600;
      color: #cbd5e1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      min-width: 0;
    }
    .mq-tag {
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5px;
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.16);
      padding: 0 3px;
      border-radius: 3px;
      vertical-align: middle;
    }
    .mq-last {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      color: #f8fafc;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }
    .mq-chg {
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      font-variant-numeric: tabular-nums;
      white-space: nowrap;
    }
    .mq-up .mq-chg { color: #34d399; }
    .mq-down .mq-chg { color: #f87171; }
    .mq-flat .mq-chg { color: #94a3b8; }
    .mq-stale .mq-last { color: #94a3b8; }
    .mq-spark {
      flex: none;
      width: 56px;
      height: 26px;
      overflow: visible;
    }
    .mq-line {
      fill: none;
      stroke-width: 1.4;
      vector-effect: non-scaling-stroke;
    }
    .mq-area { stroke: none; opacity: 0.18; }
    .mq-base {
      stroke: rgba(148, 163, 184, 0.45);
      stroke-width: 1;
      stroke-dasharray: 2 2;
      vector-effect: non-scaling-stroke;
    }
    .mq-up .mq-line { stroke: #34d399; }
    .mq-up .mq-area { fill: #34d399; }
    .mq-down .mq-line { stroke: #f87171; }
    .mq-down .mq-area { fill: #f87171; }
    .mq-flat .mq-line { stroke: #94a3b8; }
    .mq-flat .mq-area { fill: #94a3b8; }
    .mq-asof {
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 2px;
      padding: 6px 14px;
      font-size: 10.5px;
      color: #94a3b8;
      border-left: 1px solid rgba(255, 255, 255, 0.08);
      white-space: nowrap;
    }
    .mq-asof strong { color: #e2e8f0; font-family: 'JetBrains Mono', monospace; font-weight: 600; }
    .mq-status { display: inline-flex; align-items: center; gap: 5px; font-weight: 700; color: #94a3b8; }
    .mq-live-dot { width: 6px; height: 6px; border-radius: 50%; background: #64748b; }
    .market-quickview.mq-live .mq-status { color: #34d399; }
    .market-quickview.mq-live .mq-live-dot { background: #10b981; box-shadow: 0 0 6px #10b981; }
    .mq-footnote { font-size: 9.5px; color: #64748b; white-space: normal; max-width: 190px; }
    @media (max-width: 900px) {
      .market-quickview { grid-template-columns: minmax(0, 1fr); }
      .mq-label { border-right: none; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding: 8px 12px; }
      .mq-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .mq-spark { width: 44px; }
      .mq-asof {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 4px 12px;
        border-left: none;
        white-space: normal;
        padding: 7px 12px;
      }
    }
    """


def get_market_strip_js() -> str:
    """Polls /api/market-snapshot (served by serve_reports.py); never polls on GitHub Pages, which has no API."""
    return """
  <script>
    (function initMarketQuickView() {
      const strip = document.getElementById('market-quickview');
      if (!strip || !/^https?:$/.test(location.protocol) || /\\.github\\.io$/i.test(location.hostname)) return;
      const statusText = strip.querySelector('[data-mq-status-text]');
      const asofEl = strip.querySelector('[data-mq-asof]');
      const BASE_MS = 60000;
      const MAX_MS = 600000;
      let live = false;
      let stopped = false;
      let delay = BASE_MS;
      let timer = null;
      let inflight = false;

      function apply(snap) {
        (snap.items || []).forEach((it) => {
          const cell = strip.querySelector('[data-mq-key="' + it.key + '"]');
          if (!cell) return;
          cell.classList.remove('mq-up', 'mq-down', 'mq-flat', 'mq-stale');
          cell.classList.add('mq-' + it.direction);
          if (it.stale) cell.classList.add('mq-stale');
          cell.querySelector('.mq-last').textContent = it.last_fmt;
          cell.querySelector('.mq-abs').textContent = it.change_fmt;
          cell.querySelector('.mq-pct').textContent = it.pct_fmt;
          cell.querySelector('.mq-line').setAttribute('d', it.spark_line);
          cell.querySelector('.mq-area').setAttribute('d', it.spark_area);
          const base = cell.querySelector('.mq-base');
          base.setAttribute('y1', it.spark_base_y);
          base.setAttribute('y2', it.spark_base_y);
        });
        if (asofEl && snap.as_of_display) asofEl.textContent = snap.as_of_display;
      }

      function schedule(ms) {
        clearTimeout(timer);
        timer = setTimeout(refresh, ms);
      }

      async function refresh() {
        if (inflight || stopped) return;
        if (document.hidden) {
          schedule(delay);
          return;
        }
        inflight = true;
        try {
          const opts = { cache: 'no-store' };
          if (typeof AbortSignal !== 'undefined' && AbortSignal.timeout) opts.signal = AbortSignal.timeout(15000);
          const res = await fetch('/api/market-snapshot', opts);
          if (res.status === 404 || res.status === 405) {
            // No API on this host (static hosting): keep the build-time snapshot and stop polling.
            stopped = true;
            if (statusText) statusText.textContent = 'Snapshot';
            return;
          }
          if (!res.ok) throw new Error('HTTP ' + res.status);
          const snap = await res.json();
          if (!snap.items || !snap.items.length) {
            strip.querySelectorAll('.mq-cell').forEach((cell) => cell.classList.add('mq-stale'));
            strip.classList.remove('mq-live');
            if (statusText) statusText.textContent = 'Snapshot (live data unavailable)';
            delay = Math.min(delay * 2, MAX_MS);
            schedule(delay);
            return;
          }
          apply(snap);
          live = true;
          delay = BASE_MS;
          strip.classList.add('mq-live');
          if (statusText) statusText.textContent = 'Live \\u2022 refresh 60s';
          schedule(delay);
        } catch (err) {
          // Transient failure (5xx, timeout, network): keep the last values and retry with backoff capped at 10 min.
          strip.classList.remove('mq-live');
          if (statusText) statusText.textContent = live ? 'Reconnecting\\u2026' : 'Snapshot';
          delay = Math.min(delay * 2, MAX_MS);
          schedule(delay);
        } finally {
          inflight = false;
        }
      }

      refresh();
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden && !stopped) schedule(0);
      });
    })();
  </script>
"""


def ledger_check_status(intel: dict[str, dict]) -> str:
    """Footer line from validate_news_portal (re-resolves every ledger figure from its source file)."""
    try:
        from validate_news_portal import validate_portal
        report = validate_portal(intel)
    except Exception as exc:
        print(f"[news_portal] ledger validation unavailable: {exc}")
        return "Ground-truth ledger check unavailable"
    if report["passed"]:
        return f"Ground-truth ledger check passed: {report['facts_verified']:,} figures re-resolved from their source files"
    print(f"[news_portal] ledger validation FAILED: {len(report['errors'])} issue(s); run python validate_news_portal.py")
    return f"Ground-truth ledger check FAILED ({len(report['errors'])} issues) — run python validate_news_portal.py"


FAVICON_LINK = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E'
                '%3Crect width=%2732%27 height=%2732%27 rx=%277%27 fill=%27%2310b981%27/%3E%3Cpath d=%27M7 22l6-7 5 4 7-10%27 '
                'stroke=%27white%27 stroke-width=%273%27 fill=%27none%27/%3E%3C/svg%3E">')


def build_standalone_news_page(link_prefix: str, index_href: str, snapshot: dict | None = None) -> str:
    # Each component degrades on its own (like index.html) so one failure never blocks the whole page
    portal_css = get_discover_portal_css()
    try:
        intel = discover_ticker_intelligence(link_prefix=link_prefix)
        portal_html, articles_json_str = build_discover_portal_section_html(intel)
        portal_js = get_discover_portal_js(articles_json_str, intel)
        ledger_status = ledger_check_status(intel)
    except Exception as exc:
        print(f"[news_portal] Discover portal unavailable: {type(exc).__name__}: {exc}")
        portal_html = ('<section class="discover-portal-wrapper"><div class="port-empty-state"><strong>News portal temporarily '
                       'unavailable.</strong><span>Run python validate_news_portal.py for details.</span></div></section>')
        portal_js, ledger_status = "", "Ground-truth ledger check unavailable"
    try:
        market_strip_html = render_market_strip_html(snapshot if snapshot is not None else get_market_snapshot_safe())
        market_strip_css, market_strip_js = get_market_strip_css(), get_market_strip_js()
    except Exception as exc:
        print(f"[news_portal] market strip unavailable: {type(exc).__name__}: {exc}")
        market_strip_html = market_strip_css = market_strip_js = ""
    built = datetime.now(ET)
    last_updated = built.strftime("%B %d, %Y at %I:%M %p ET")
    n_tickers = len(load_portfolio_tickers())

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Financial Market &amp; Portfolio Discover Portal | Institutional Earnings Intelligence</title>
  {FAVICON_LINK}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #090d16;
      --card-bg: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-blue: #3b82f6;
      --bull-green: #10b981;
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
      padding: 28px 20px 50px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}
    .portal-shell {{
      max-width: 1260px;
      width: 100%;
    }}
    .top-portal-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 12px;
      padding: 10px 18px;
      margin-bottom: 24px;
    }}
    .nav-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 14px;
      color: #f8fafc;
    }}
    .nav-brand-badge {{
      background: linear-gradient(135deg, #10b981, #3b82f6);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 6px;
    }}
    .nav-links {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .nav-pill-link {{
      color: #cbd5e1;
      text-decoration: none;
      font-size: 12.5px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(255, 255, 255, 0.03);
      transition: all 0.15s ease;
    }}
    .nav-pill-link:hover, .nav-pill-link.active {{
      background: rgba(59, 130, 246, 0.2);
      color: #ffffff;
      border-color: rgba(59, 130, 246, 0.5);
    }}
    .portal-hero-header {{
      text-align: center;
      margin-bottom: 26px;
    }}
    .portal-hero-header h1 {{
      font-size: 34px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin: 0 0 10px 0;
      background: linear-gradient(135deg, #ffffff 30%, #34d399 70%, #60a5fa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .portal-hero-header p {{
      color: var(--text-muted);
      font-size: 14.5px;
      max-width: 780px;
      margin: 0 auto;
      line-height: 1.5;
    }}
    .build-age-note {{
      margin: 10px auto 0 auto;
      max-width: 780px;
      color: #fbbf24;
      font-size: 12.5px;
    }}
    .portal-footer {{
      margin-top: 40px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--card-border);
      padding-top: 20px;
    }}
    {portal_css}
    {market_strip_css}
  </style>
</head>
<body>
  <div class="portal-shell">
    {market_strip_html}
    <header>
      <nav class="top-portal-nav" aria-label="Primary Platform Navigation">
        <div class="nav-brand">
          <span class="nav-brand-badge">DISCOVER AI</span>
          <span>Institutional Financial &amp; Portfolio News Portal</span>
        </div>
        <div class="nav-links">
          <a href="#section-market-news" class="nav-pill-link active">⚡ 1. Market Impact News</a>
          <a href="#section-portfolio-news" class="nav-pill-link">🎯 2. My Portfolio News (tickers.txt)</a>
          <a href="{index_href}?filter=post#section-tearsheet-library" class="nav-pill-link">📊 T+0 Post-Earnings Tearsheets</a>
          <a href="{index_href}#section-tearsheet-library" class="nav-pill-link">🗂️ Full Tearsheet Library</a>
        </div>
      </nav>

      <div class="portal-hero-header">
        <h1>AI Market &amp; Portfolio Discover Portal</h1>
        <p>Perplexity Discover-style briefings for your {n_tickers}-stock <code>tickers.txt</code> portfolio • Built from SEC earnings exhibits (8-K / 6-K), Stage 1 ground truth &amp; agent-bus research • Updated {last_updated}</p>
        <p class="build-age-note" id="build-age-note" data-built="{built.isoformat()}" hidden>This page was built more than a day ago, so "upcoming" and "reported" states may be out of date. Re-run <code>python update_index.py</code> to refresh it.</p>
      </div>
    </header>

    <main>
      {portal_html}
    </main>

    <footer class="portal-footer">
      <div>Antigravity 2.0 Earnings Intelligence • {html.escape(ledger_status)} • Hover any $TICKER for its pop-up summary • Click any tile for the full AI synthesis</div>
    </footer>
  </div>
  {portal_js}
  {market_strip_js}
  <script>
    (function flagStaleBuild() {{
      const note = document.getElementById('build-age-note');
      const built = note && Date.parse(note.getAttribute('data-built'));
      if (built && Date.now() - built > 24 * 3600 * 1000) note.hidden = false;
    }})();
  </script>
</body>
</html>
"""


def generate_news_portal_files(snapshot: dict | None = None) -> bool:
    """Writes news.html and published_reports/news.html; returns True once both are written."""
    REPORTS_DIR.mkdir(exist_ok=True)
    snap = snapshot if snapshot is not None else get_market_snapshot_safe()
    root_html = build_standalone_news_page(link_prefix="published_reports/", index_href="index.html", snapshot=snap)
    (BASE_DIR / "news.html").write_text(root_html, encoding="utf-8")

    rep_html = build_standalone_news_page(link_prefix="", index_href="index.html", snapshot=snap)
    (REPORTS_DIR / "news.html").write_text(rep_html, encoding="utf-8")
    print("Successfully generated standalone news.html and published_reports/news.html.")
    return True


if __name__ == "__main__":
    generate_news_portal_files()
