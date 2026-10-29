"""
Antigravity 2.0 Institutional Earnings Data Warehouse (SQLite System-of-Record)
Maintains `earnings_warehouse.db` with 5 normalized, ACID-constrained tables:
  1. companies                     - Master issuer metadata, SEC CIK, currency, fiscal year-end month
  2. earnings_events               - Discrete quarterly earnings prints, prices, straddle bands, HTML tearsheet links
  3. consensus_snapshots           - Point-in-time T-1 locked & T+0 scorecard consensus with immutability trigger
  4. quarterly_financials          - 3-month isolated quarterly P&L + FCF waterfall rows (80..100d duration CHECK)
  5. segment_and_guidance_ledger   - Operational KPIs, reporting segments, prior-guide accountability & forward resets

Also compiles static zero-server manifests for GitHub Pages:
  - published_reports/history_catalog.js
  - published_reports/warehouse_summary.json
"""

from __future__ import annotations

import json
import math
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from archive_topbar import format_short_date, resolve_quarter_label

try:
    from news_facts import reporting_currency as _resolve_reporting_currency
except Exception:
    def _resolve_reporting_currency(ticker: str) -> str:
        return "€" if ticker.upper() == "NOK" else "$"


BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "earnings_warehouse.db"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
PRE_BUS_DIR = BASE_DIR / "pre_agent_bus"
POST_BUS_DIR = BASE_DIR / "post_agent_bus"
REPORTS_DIR = BASE_DIR / "published_reports"
AUDIT_DIR = BASE_DIR / "audit_logs"


SCHEMA_SQL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    ticker                  TEXT PRIMARY KEY,
    cik                     TEXT,
    company_name            TEXT NOT NULL,
    sector                  TEXT,
    industry                TEXT,
    reporting_currency      TEXT NOT NULL DEFAULT '$',
    fiscal_year_end_month   INTEGER CHECK (fiscal_year_end_month IS NULL OR (fiscal_year_end_month BETWEEN 1 AND 12)),
    updated_at_utc          TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_companies_cik ON companies(cik);

CREATE TABLE IF NOT EXISTS earnings_events (
    event_id                TEXT PRIMARY KEY,
    ticker                  TEXT NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    cik                     TEXT,
    fiscal_year             INTEGER NOT NULL CHECK (fiscal_year BETWEEN 2000 AND 2100),
    fiscal_quarter          INTEGER NOT NULL CHECK (fiscal_quarter BETWEEN 1 AND 4),
    quarter_label           TEXT NOT NULL,
    release_date            TEXT NOT NULL,
    timing_hint             TEXT,
    spot_price_t1           REAL,
    regular_close_price     REAL,
    after_hours_price       REAL,
    post_print_move_pct     REAL,
    atm_straddle_usd        REAL,
    implied_move_pct        REAL,
    overall_print_verdict   TEXT,
    t1_html_filename        TEXT,
    t0_html_filename        TEXT,
    t1_signoff_status       TEXT,
    t0_signoff_status       TEXT,
    updated_at_utc          TEXT NOT NULL,
    UNIQUE (ticker, release_date),
    UNIQUE (ticker, fiscal_year, fiscal_quarter)
);

CREATE INDEX IF NOT EXISTS idx_events_ticker_date ON earnings_events(ticker, release_date DESC);

CREATE TABLE IF NOT EXISTS consensus_snapshots (
    snapshot_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                TEXT NOT NULL REFERENCES earnings_events(event_id) ON DELETE CASCADE,
    ticker                  TEXT NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    stage                   TEXT NOT NULL CHECK (stage IN ('T-1_LOCKED', 'T+0_SCORECARD')),
    captured_at_utc         TEXT NOT NULL,
    source                  TEXT NOT NULL,
    rev_consensus_m         REAL,
    rev_whisper_m           REAL,
    rev_low_m               REAL,
    rev_high_m              REAL,
    eps_nongaap_consensus   REAL,
    eps_gaap_consensus      REAL,
    eps_whisper             REAL,
    analyst_count           INTEGER,
    target_mean_price       REAL,
    immutable_locked        INTEGER NOT NULL DEFAULT 1 CHECK (immutable_locked IN (0, 1)),
    UNIQUE (event_id, stage)
);

CREATE TRIGGER IF NOT EXISTS trg_protect_locked_consensus
BEFORE UPDATE ON consensus_snapshots
WHEN OLD.stage = 'T-1_LOCKED' AND OLD.immutable_locked = 1 AND NEW.immutable_locked = 1
BEGIN
    SELECT CASE
        WHEN (OLD.rev_consensus_m IS NOT NULL AND NEW.rev_consensus_m IS NOT NULL AND ABS(OLD.rev_consensus_m - NEW.rev_consensus_m) > 0.05)
          OR (OLD.eps_nongaap_consensus IS NOT NULL AND NEW.eps_nongaap_consensus IS NOT NULL AND ABS(OLD.eps_nongaap_consensus - NEW.eps_nongaap_consensus) > 0.005)
          OR (OLD.eps_gaap_consensus IS NOT NULL AND NEW.eps_gaap_consensus IS NOT NULL AND ABS(OLD.eps_gaap_consensus - NEW.eps_gaap_consensus) > 0.005)
        THEN RAISE(ABORT, 'IMMUTABLE_CONSENSUS_LOCK: Cannot overwrite locked T-1 consensus figures without explicit unlock (immutable_locked=0)')
    END;
END;

CREATE TABLE IF NOT EXISTS quarterly_financials (
    ticker                  TEXT NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    cik                     TEXT,
    fiscal_year             INTEGER NOT NULL CHECK (fiscal_year BETWEEN 2000 AND 2100),
    fiscal_quarter          INTEGER NOT NULL CHECK (fiscal_quarter BETWEEN 1 AND 4),
    period_label            TEXT NOT NULL,
    period_end_date         TEXT,
    duration_days           INTEGER NOT NULL DEFAULT 91 CHECK (duration_days BETWEEN 80 AND 100),
    source_filing           TEXT NOT NULL,
    reporting_currency      TEXT NOT NULL DEFAULT '$',
    revenue_m               REAL,
    cost_of_revenue_m       REAL,
    gross_profit_m          REAL,
    opex_m                  REAL,
    rd_m                    REAL,
    sm_m                    REAL,
    ga_m                    REAL,
    ebit_m                  REAL,
    net_income_gaap_m       REAL,
    eps_gaap                REAL,
    eps_nongaap             REAL,
    ocf_3m_m                REAL,
    capex_3m_m              REAL,
    reported_fcf_3m_m       REAL,
    sbc_3m_m                REAL,
    leases_3m_m             REAL,
    true_fcf_3m_m           REAL,
    updated_at_utc          TEXT NOT NULL,
    PRIMARY KEY (ticker, fiscal_year, fiscal_quarter),
    CHECK (
        ocf_3m_m IS NULL OR capex_3m_m IS NULL OR reported_fcf_3m_m IS NULL
        OR ABS((ocf_3m_m - capex_3m_m) - reported_fcf_3m_m) <= 2.5
    ),
    CHECK (
        reported_fcf_3m_m IS NULL OR true_fcf_3m_m IS NULL
        OR ABS((reported_fcf_3m_m - COALESCE(sbc_3m_m, 0.0) - COALESCE(leases_3m_m, 0.0)) - true_fcf_3m_m) <= 2.5
    )
);

CREATE INDEX IF NOT EXISTS idx_qf_cik_period ON quarterly_financials(cik, fiscal_year, fiscal_quarter);

CREATE TABLE IF NOT EXISTS segment_and_guidance_ledger (
    ledger_id               INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id                TEXT NOT NULL REFERENCES earnings_events(event_id) ON DELETE CASCADE,
    ticker                  TEXT NOT NULL REFERENCES companies(ticker) ON DELETE CASCADE,
    entry_type              TEXT NOT NULL CHECK (entry_type IN (
                                'REPORTING_SEGMENT',
                                'OPERATIONAL_KPI',
                                'GUIDANCE_ACCOUNTABILITY',
                                'FORWARD_GUIDANCE',
                                'CREDIBILITY_SCORE'
                            )),
    metric_name             TEXT NOT NULL,
    target_period           TEXT,
    prior_or_consensus_text TEXT,
    actual_or_guided_text   TEXT,
    value_actual            REAL,
    value_consensus         REAL,
    value_whisper           REAL,
    delta_text              TEXT,
    verdict_or_badge        TEXT,
    source_file             TEXT NOT NULL,
    updated_at_utc          TEXT NOT NULL,
    UNIQUE (event_id, entry_type, metric_name)
);

CREATE INDEX IF NOT EXISTS idx_ledger_ticker ON segment_and_guidance_ledger(ticker, entry_type);
"""


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _num(val: Any) -> float | None:
    if isinstance(val, bool) or val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val) if math.isfinite(val) else None
    if isinstance(val, str):
        s = val.strip()
        if not s or s in ("—", "-", "N/A", "NM"):
            return None
        m = re.search(r"([+\-])?\s*[$€]?\s*(\d[\d,]*(?:\.\d+)?)\s*([BMK])?(?![0-9A-Za-z.%])", s)
        if m:
            v = float(m.group(2).replace(",", ""))
            if m.group(1) == "-":
                v = -v
            unit = m.group(3)
            if unit == "B":
                v *= 1000.0
            elif unit == "K":
                v /= 1000.0
            return v
    return None


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def parse_quarter_year(label: str, fallback_date: str | None = None) -> tuple[int, int, str]:
    """Parse 'Q3 2026', 'Q3 2026 (Ended Sep 30, 2026)', 'Q1 FY2027', or 'Q3 FY27' -> (year, quarter, clean_label)."""
    clean = re.sub(r"\s*\(Actual\)\s*$", "", str(label or "")).strip()
    m = re.search(r"\bQ([1-4])\s+(?:FY)?(\d{2,4})\b", clean, re.IGNORECASE)
    if m:
        q = int(m.group(1))
        yr_raw = m.group(2)
        yr = (2000 + int(yr_raw)) if len(yr_raw) == 2 else int(yr_raw)
        has_fy = "FY" in clean.upper()
        short_lbl = f"Q{q} {'FY' if has_fy else ''}{yr}"
        return yr, q, short_lbl
    if fallback_date:
        try:
            dt = datetime.strptime(fallback_date, "%Y-%m-%d")
            q = (max(dt.month - 2, 0) // 3) + 1
            return dt.year, min(max(q, 1), 4), f"Q{q} {dt.year}"
        except Exception:
            pass
    return 2026, 3, "Q3 2026"


def parse_period_end_date(period_header: str) -> str | None:
    """Extract ISO end date from 'Q2 2026 (Ended Jun 30, 2026)' -> '2026-06-30'."""
    m = re.search(r"Ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", str(period_header or ""))
    if m:
        try:
            return datetime.strptime(m.group(1), "%b %d, %Y").strftime("%Y-%m-%d")
        except Exception:
            return None
    return None


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.commit()


def _infer_fye_month(t1_data: dict) -> int | None:
    filings = (((t1_data.get("stitched_5q_financials") or {}).get("sec_edgar_filings_meta") or {}).get("recent_10q_10k_filings")) or []
    for f in filings:
        if str(f.get("form") or "").upper() in ("10-K", "20-F"):
            por = str(f.get("period_of_report") or "")
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", por):
                return int(por.split("-")[1])
    hdrs = (((t1_data.get("stitched_5q_financials") or {}).get("income_statement_5q") or {}).get("period_headers")) or []
    for h in hdrs:
        if str(h).strip().upper().startswith("Q4 "):
            ed = parse_period_end_date(h)
            if ed:
                return int(ed.split("-")[1])
    return 12


def _extract_5q_series(metrics_dict: dict, candidate_keys: list[str], idx: int) -> float | None:
    for k in candidate_keys:
        entry = metrics_dict.get(k)
        if isinstance(entry, dict):
            arr = entry.get("values_5q_chronological")
            if isinstance(arr, list) and idx < len(arr):
                v = _num(arr[idx])
                if v is not None:
                    return v
    return None


def _upsert_company(
    conn: sqlite3.Connection,
    ticker: str,
    company_name: str | None = None,
    cik: str | None = None,
    sector: str | None = None,
    industry: str | None = None,
    fye_month: int | None = None,
) -> tuple[str, str]:
    ticker = ticker.upper()
    ccy = _resolve_reporting_currency(ticker)
    now = _utc_now()
    existing = conn.execute("SELECT * FROM companies WHERE ticker = ?", (ticker,)).fetchone()
    if existing:
        final_cik = cik or existing["cik"]
        final_name = (company_name if company_name and company_name != ticker else None) or existing["company_name"] or ticker
        final_sec = sector or existing["sector"]
        final_ind = industry or existing["industry"]
        final_fye = fye_month or existing["fiscal_year_end_month"]
        conn.execute(
            """
            UPDATE companies
               SET cik = ?, company_name = ?, sector = ?, industry = ?,
                   reporting_currency = ?, fiscal_year_end_month = ?, updated_at_utc = ?
             WHERE ticker = ?
            """,
            (final_cik, final_name, final_sec, final_ind, ccy, final_fye, now, ticker),
        )
        return final_cik, ccy
    else:
        final_name = company_name or ticker
        conn.execute(
            """
            INSERT INTO companies (ticker, cik, company_name, sector, industry, reporting_currency, fiscal_year_end_month, updated_at_utc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (ticker, cik, final_name, sector, industry, ccy, fye_month, now),
        )
        return cik, ccy


def _resolve_published_html_and_signoffs(ticker: str, release_date: str) -> tuple[str | None, str | None, str | None, str | None]:
    ticker = ticker.upper()
    t1_signoff = _load_json(AUDIT_DIR / f"{ticker}_{release_date}_pre_agent5_signoff.json").get("status")
    t0_signoff = _load_json(AUDIT_DIR / f"{ticker}_{release_date}_agent5_signoff.json").get("status")

    t1_canon = REPORTS_DIR / f"{ticker}_T1_{release_date}.html"
    t1_file = t1_canon.name if t1_canon.exists() else None
    if not t1_file:
        v_files = sorted(REPORTS_DIR.glob(f"{ticker}_T1_{release_date}_v*.html"))
        if v_files:
            t1_file = v_files[-1].name

    t0_file = None
    if t0_signoff is None or t0_signoff == "APPROVED":
        t0_canon = REPORTS_DIR / f"{ticker}_T0_POST_{release_date}.html"
        if t0_canon.exists():
            t0_file = t0_canon.name
        else:
            v_files = sorted(REPORTS_DIR.glob(f"{ticker}_T0_POST_{release_date}_v*.html"))
            if v_files:
                t0_file = v_files[-1].name

    return t1_file, t0_file, t1_signoff, t0_signoff


def _extract_t1_html_consensus_fallback(t1_html_name: str | None) -> tuple[float | None, float | None, float | None, float | None]:
    """Fallback consensus/whisper parser from published T-1 HTML strip for legacy pre-Oct-29 truth files."""
    if not t1_html_name:
        return None, None, None, None
    p = REPORTS_DIR / t1_html_name
    if not p.exists():
        return None, None, None, None
    try:
        content = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None, None, None, None

    html_cons_rev = None
    html_whisp_rev = None
    m_dual = re.search(
        r'Consensus(?:\s+(?:Total|Core|Net|Consolidated))?\s+(?:Revenue|Sales|Net Sales).*?<span class="strip-val">[$€]([0-9,.]+)\s*([MB])?\s*/\s*[$€]([0-9,.]+)\s*([MB])?',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if m_dual:
        u1 = m_dual.group(2) or ("B" if "B" in m_dual.group(0) else "M")
        u2 = m_dual.group(4) or ("B" if "B" in m_dual.group(0) else "M")
        html_cons_rev = round(float(m_dual.group(1).replace(",", "")) * (1000.0 if u1.upper() == "B" else 1.0), 2)
        html_whisp_rev = round(float(m_dual.group(3).replace(",", "")) * (1000.0 if u2.upper() == "B" else 1.0), 2)
    else:
        m_single = re.search(
            r'Consensus(?:\s+(?:Total|Core|Net|Consolidated))?\s+(?:Revenue|Sales|Net Sales).*?<span class="strip-val">[$€]\s*([0-9,.]+)\s*([MB])?',
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if m_single:
            raw_v = float(m_single.group(1).replace(",", ""))
            u = m_single.group(2) or ("B" if ("B" in m_single.group(0) and raw_v < 500) else "M")
            html_cons_rev = round(raw_v * (1000.0 if u.upper() == "B" else 1.0), 2)

    html_cons_eps = None
    html_whisp_eps = None
    m_eps_dual = re.search(
        r'Consensus.*?EPS.*?<span class="strip-val">([+\-]?[$€]?[0-9.]+)[^/<]*[/\\]\s*([+\-]?[$€]?[0-9.]+)\s*Whisper',
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if m_eps_dual:
        html_cons_eps = _num(m_eps_dual.group(1))
        html_whisp_eps = _num(m_eps_dual.group(2))
    else:
        m_eps = re.search(
            r'Consensus.*?EPS.*?<span class="strip-val">([+\-]?[$€]?\s*[0-9.]+)',
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if m_eps:
            html_cons_eps = _num(m_eps.group(1))

    return html_cons_rev, html_whisp_rev, html_cons_eps, html_whisp_eps


def ingest_t1_truth(
    ticker: str,
    release_date: str,
    db_path: Path = DB_PATH,
    allow_unlock_consensus: bool = False,
) -> None:
    """Ingest ground_truth/{TICKER}_{DATE}_truth.json + pre_agent_bus/* into earnings_warehouse.db."""
    init_db(db_path)
    ticker = ticker.upper()
    truth_path = GROUND_TRUTH_DIR / f"{ticker}_{release_date}_truth.json"
    t1 = _load_json(truth_path)
    if not t1:
        return

    now = _utc_now()
    s5 = t1.get("stitched_5q_financials") or {}
    cik = ((s5.get("sec_edgar_filings_meta") or {}).get("cik")) or None
    fye_month = _infer_fye_month(t1)

    q_label = resolve_quarter_label(ticker, release_date)
    fy, fq, clean_q_lbl = parse_quarter_year(q_label, fallback_date=release_date)
    event_id = f"{ticker}_{release_date}"

    sched = t1.get("schedule_verification") or {}
    pval = t1.get("price_validation") or {}
    opt = t1.get("options_positioning") or {}
    targets = t1.get("street_consensus_and_targets") or {}
    fwd_q0e = targets.get("forward_consensus_q0e") or {}

    t1_html, t0_html, t1_sig, t0_sig = _resolve_published_html_and_signoffs(ticker, release_date)

    # Whisper & legacy consensus enrichment from pre_agent_bus 2A or published T-1 HTML if truth.json predated forward_consensus_q0e
    pre_2a = _load_json(PRE_BUS_DIR / f"{ticker}_{release_date}_pre_agent2a_kpis.json")
    bus_rev_cons = None
    whisper_rev_m = None
    whisper_eps = None
    for row in pre_2a.get("headline_and_company_kpis") or []:
        m_lbl = str(row.get("metric") or "").lower()
        if (
            any(w in m_lbl for w in ("revenue", "sales"))
            and any(k in m_lbl for k in ("consolidated", "total", "core"))
            and not any(x in m_lbl for x in ("eps", "margin", "%", "growth", "transaction", "subscription", "consumables", "instrument"))
        ):
            bus_rev_cons = bus_rev_cons or _num(row.get("street_consensus_q0e"))
            whisper_rev_m = whisper_rev_m or _num(row.get("whisper_bogey_q0e"))
        elif "eps" in m_lbl:
            whisper_eps = whisper_eps or _num(row.get("whisper_bogey_q0e"))

    rev_cons = (
        _num(fwd_q0e.get("revenue_avg_millions"))
        or _num(targets.get("yahoo_consensus_revenue_q0e"))
        or _num(sched.get("yahoo_consensus_revenue"))
        or bus_rev_cons
    )
    eps_cons = (
        _num(fwd_q0e.get("eps_avg"))
        or _num(targets.get("yahoo_consensus_eps_q0e"))
        or _num(sched.get("yahoo_consensus_eps"))
    )

    h_rev_cons, h_rev_whisp, h_eps_cons, h_eps_whisp = _extract_t1_html_consensus_fallback(t1_html)
    if rev_cons is None and h_rev_cons is not None:
        rev_cons = h_rev_cons
    if whisper_rev_m is None and h_rev_whisp is not None:
        # Only attach HTML whisper if HTML consensus matches rev_cons within 2% (prevents stale whisper pairing)
        if rev_cons is None or (h_rev_cons is not None and abs(h_rev_cons - rev_cons) / max(abs(rev_cons), 1.0) <= 0.02 and h_rev_whisp >= rev_cons):
            whisper_rev_m = h_rev_whisp
    if eps_cons is None and h_eps_cons is not None:
        eps_cons = h_eps_cons
    if whisper_eps is None and h_eps_whisp is not None:
        whisper_eps = h_eps_whisp

    with get_connection(db_path) as conn:
        final_cik, ccy = _upsert_company(
            conn,
            ticker=ticker,
            company_name=t1.get("company_name"),
            cik=cik,
            sector=t1.get("sector"),
            industry=t1.get("industry"),
            fye_month=fye_month,
        )

        # Upsert earnings_events (preserving T+0 columns if already populated)
        existing_ev = conn.execute("SELECT * FROM earnings_events WHERE event_id = ?", (event_id,)).fetchone()
        if existing_ev:
            conn.execute(
                """
                UPDATE earnings_events
                   SET cik = COALESCE(?, cik),
                       fiscal_year = ?,
                       fiscal_quarter = ?,
                       quarter_label = ?,
                       timing_hint = COALESCE(?, timing_hint),
                       spot_price_t1 = COALESCE(?, spot_price_t1),
                       atm_straddle_usd = COALESCE(?, atm_straddle_usd),
                       implied_move_pct = COALESCE(?, implied_move_pct),
                       t1_html_filename = COALESCE(?, t1_html_filename),
                       t0_html_filename = COALESCE(?, t0_html_filename),
                       t1_signoff_status = COALESCE(?, t1_signoff_status),
                       t0_signoff_status = COALESCE(?, t0_signoff_status),
                       updated_at_utc = ?
                 WHERE event_id = ?
                """,
                (
                    final_cik,
                    fy,
                    fq,
                    clean_q_lbl,
                    sched.get("release_timing_hint"),
                    _num(pval.get("yahoo_spot_price")),
                    _num(opt.get("atm_straddle_usd")),
                    _num(opt.get("atm_implied_move_pct")),
                    t1_html,
                    t0_html,
                    t1_sig,
                    t0_sig,
                    now,
                    event_id,
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO earnings_events (
                    event_id, ticker, cik, fiscal_year, fiscal_quarter, quarter_label,
                    release_date, timing_hint, spot_price_t1, atm_straddle_usd, implied_move_pct,
                    t1_html_filename, t0_html_filename, t1_signoff_status, t0_signoff_status, updated_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    ticker,
                    final_cik,
                    fy,
                    fq,
                    clean_q_lbl,
                    release_date,
                    sched.get("release_timing_hint"),
                    _num(pval.get("yahoo_spot_price")),
                    _num(opt.get("atm_straddle_usd")),
                    _num(opt.get("atm_implied_move_pct")),
                    t1_html,
                    t0_html,
                    t1_sig,
                    t0_sig,
                    now,
                ),
            )

        # Upsert T-1_LOCKED consensus snapshot (respecting immutability trigger unless allow_unlock_consensus=True)
        existing_cs = conn.execute(
            "SELECT * FROM consensus_snapshots WHERE event_id = ? AND stage = 'T-1_LOCKED'",
            (event_id,),
        ).fetchone()
        if existing_cs:
            if allow_unlock_consensus:
                conn.execute("UPDATE consensus_snapshots SET immutable_locked = 0 WHERE snapshot_id = ?", (existing_cs["snapshot_id"],))
                conn.execute(
                    """
                    UPDATE consensus_snapshots
                       SET captured_at_utc = ?, source = ?, rev_consensus_m = ?, rev_whisper_m = ?,
                           rev_low_m = ?, rev_high_m = ?, eps_nongaap_consensus = ?,
                           eps_whisper = ?, analyst_count = ?, target_mean_price = ?, immutable_locked = 1
                     WHERE snapshot_id = ?
                    """,
                    (
                        now,
                        f"ground_truth/{truth_path.name}",
                        rev_cons,
                        whisper_rev_m,
                        _num(fwd_q0e.get("revenue_low_millions")),
                        _num(fwd_q0e.get("revenue_high_millions")),
                        eps_cons,
                        whisper_eps,
                        targets.get("analyst_count"),
                        _num(targets.get("target_mean_price")),
                        existing_cs["snapshot_id"],
                    ),
                )
            else:
                # Only enrich NULL fields so locked figures are never mutated
                conn.execute(
                    """
                    UPDATE consensus_snapshots
                       SET rev_consensus_m = COALESCE(rev_consensus_m, ?),
                           rev_whisper_m = COALESCE(rev_whisper_m, ?),
                           rev_low_m = COALESCE(rev_low_m, ?),
                           rev_high_m = COALESCE(rev_high_m, ?),
                           eps_nongaap_consensus = COALESCE(eps_nongaap_consensus, ?),
                           eps_whisper = COALESCE(eps_whisper, ?),
                           analyst_count = COALESCE(analyst_count, ?),
                           target_mean_price = COALESCE(target_mean_price, ?)
                     WHERE snapshot_id = ?
                    """,
                    (
                        rev_cons,
                        whisper_rev_m,
                        _num(fwd_q0e.get("revenue_low_millions")),
                        _num(fwd_q0e.get("revenue_high_millions")),
                        eps_cons,
                        whisper_eps,
                        targets.get("analyst_count"),
                        _num(targets.get("target_mean_price")),
                        existing_cs["snapshot_id"],
                    ),
                )
        else:
            conn.execute(
                """
                INSERT INTO consensus_snapshots (
                    event_id, ticker, stage, captured_at_utc, source,
                    rev_consensus_m, rev_whisper_m, rev_low_m, rev_high_m,
                    eps_nongaap_consensus, eps_gaap_consensus, eps_whisper,
                    analyst_count, target_mean_price, immutable_locked
                ) VALUES (?, ?, 'T-1_LOCKED', ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, 1)
                """,
                (
                    event_id,
                    ticker,
                    now,
                    f"ground_truth/{truth_path.name}",
                    rev_cons,
                    whisper_rev_m,
                    _num(fwd_q0e.get("revenue_low_millions")),
                    _num(fwd_q0e.get("revenue_high_millions")),
                    eps_cons,
                    whisper_eps,
                    targets.get("analyst_count"),
                    _num(targets.get("target_mean_price")),
                ),
            )

        # Ingest 5 historical quarters from stitched_5q_financials (only inserting or filling if not already populated by T+0 8-K)
        inc_5q = s5.get("income_statement_5q") or {}
        cf_5q = s5.get("cash_flow_5q") or {}
        inc_m = inc_5q.get("metrics_millions") or {}
        cf_m = cf_5q.get("metrics_millions") or {}
        hdrs = inc_5q.get("period_headers") or []

        for idx, hdr in enumerate(hdrs):
            q_yr, q_num, q_short = parse_quarter_year(hdr)
            end_dt = parse_period_end_date(hdr)
            existing_qf = conn.execute(
                "SELECT source_filing FROM quarterly_financials WHERE ticker = ? AND fiscal_year = ? AND fiscal_quarter = ?",
                (ticker, q_yr, q_num),
            ).fetchone()
            # Never overwrite an authoritative T+0 / SEC 8-K Exhibit 99.1 row with yfinance T-1 historicals
            if existing_qf and any(tag in str(existing_qf["source_filing"]) for tag in ("SEC ", "8-K", "6-K", "T+0")):
                continue

            rev_v = _extract_5q_series(inc_m, ["Total Revenue", "Operating Revenue"], idx)
            cor_v = _extract_5q_series(inc_m, ["Cost Of Revenue", "Reconciled Cost Of Revenue"], idx)
            gp_v = _extract_5q_series(inc_m, ["Gross Profit"], idx)
            opex_v = _extract_5q_series(inc_m, ["Operating Expense"], idx)
            rd_v = _extract_5q_series(inc_m, ["Research And Development"], idx)
            sm_v = _extract_5q_series(inc_m, ["Selling And Marketing Expense"], idx)
            ga_v = _extract_5q_series(inc_m, ["General And Administrative Expense", "Selling General And Administration"], idx)
            ebit_v = _extract_5q_series(inc_m, ["Operating Income", "Total Operating Income As Reported"], idx)
            ni_v = _extract_5q_series(inc_m, ["Net Income Common Stockholders", "Net Income"], idx)
            eps_g_v = _extract_5q_series(inc_m, ["Diluted EPS"], idx)

            ocf_v = _extract_5q_series(cf_m, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"], idx)
            capex_raw = _extract_5q_series(cf_m, ["Capital Expenditure", "Purchase Of PPE"], idx)
            capex_v = abs(capex_raw) if capex_raw is not None else None
            sbc_v = _extract_5q_series(cf_m, ["Stock Based Compensation"], idx)
            rep_fcf_v = round(ocf_v - capex_v, 2) if (ocf_v is not None and capex_v is not None) else None
            true_fcf_v = round(rep_fcf_v - (sbc_v or 0.0), 2) if rep_fcf_v is not None else None

            src_filing = "10-K (Q4 Isolated)" if q_num == 4 else "10-Q (Stage 1 Stitched)"
            conn.execute(
                """
                INSERT INTO quarterly_financials (
                    ticker, cik, fiscal_year, fiscal_quarter, period_label, period_end_date,
                    duration_days, source_filing, reporting_currency,
                    revenue_m, cost_of_revenue_m, gross_profit_m, opex_m, rd_m, sm_m, ga_m,
                    ebit_m, net_income_gaap_m, eps_gaap, eps_nongaap,
                    ocf_3m_m, capex_3m_m, reported_fcf_3m_m, sbc_3m_m, leases_3m_m, true_fcf_3m_m,
                    updated_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?, 91, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, 0.0, ?, ?)
                ON CONFLICT(ticker, fiscal_year, fiscal_quarter) DO UPDATE SET
                    cik = COALESCE(excluded.cik, quarterly_financials.cik),
                    period_end_date = COALESCE(excluded.period_end_date, quarterly_financials.period_end_date),
                    revenue_m = COALESCE(excluded.revenue_m, quarterly_financials.revenue_m),
                    cost_of_revenue_m = COALESCE(excluded.cost_of_revenue_m, quarterly_financials.cost_of_revenue_m),
                    gross_profit_m = COALESCE(excluded.gross_profit_m, quarterly_financials.gross_profit_m),
                    opex_m = COALESCE(excluded.opex_m, quarterly_financials.opex_m),
                    rd_m = COALESCE(excluded.rd_m, quarterly_financials.rd_m),
                    sm_m = COALESCE(excluded.sm_m, quarterly_financials.sm_m),
                    ga_m = COALESCE(excluded.ga_m, quarterly_financials.ga_m),
                    ebit_m = COALESCE(excluded.ebit_m, quarterly_financials.ebit_m),
                    net_income_gaap_m = COALESCE(excluded.net_income_gaap_m, quarterly_financials.net_income_gaap_m),
                    eps_gaap = COALESCE(excluded.eps_gaap, quarterly_financials.eps_gaap),
                    ocf_3m_m = COALESCE(excluded.ocf_3m_m, quarterly_financials.ocf_3m_m),
                    capex_3m_m = COALESCE(excluded.capex_3m_m, quarterly_financials.capex_3m_m),
                    reported_fcf_3m_m = COALESCE(excluded.reported_fcf_3m_m, quarterly_financials.reported_fcf_3m_m),
                    sbc_3m_m = COALESCE(excluded.sbc_3m_m, quarterly_financials.sbc_3m_m),
                    leases_3m_m = CASE WHEN excluded.true_fcf_3m_m IS NOT NULL THEN excluded.leases_3m_m ELSE quarterly_financials.leases_3m_m END,
                    true_fcf_3m_m = COALESCE(excluded.true_fcf_3m_m, quarterly_financials.true_fcf_3m_m),
                    updated_at_utc = excluded.updated_at_utc
                """,
                (
                    ticker,
                    final_cik,
                    q_yr,
                    q_num,
                    q_short,
                    end_dt,
                    src_filing,
                    ccy,
                    rev_v,
                    cor_v,
                    gp_v,
                    opex_v,
                    rd_v,
                    sm_v,
                    ga_v,
                    ebit_v,
                    ni_v,
                    eps_g_v,
                    ocf_v,
                    capex_v,
                    rep_fcf_v,
                    sbc_v,
                    true_fcf_v,
                    now,
                ),
            )

        _ingest_pre_bus_ledger(conn, event_id, ticker, release_date, now)
        conn.commit()


def ingest_t0_post_truth(ticker: str, release_date: str, db_path: Path = DB_PATH) -> None:
    """Ingest ground_truth/{TICKER}_{DATE}_post_truth.json + post_agent_bus/* into earnings_warehouse.db."""
    init_db(db_path)
    ticker = ticker.upper()
    # Ensure T-1 baseline is ingested first if present on disk
    if (GROUND_TRUTH_DIR / f"{ticker}_{release_date}_truth.json").exists():
        ingest_t1_truth(ticker, release_date, db_path=db_path)

    post_path = GROUND_TRUTH_DIR / f"{ticker}_{release_date}_post_truth.json"
    pt = _load_json(post_path)
    if not pt:
        return

    now = _utc_now()
    event_id = f"{ticker}_{release_date}"
    s5c = pt.get("stitched_5q_chronological") or {}
    p_labels = s5c.get("period_labels") or []
    q0_label_raw = p_labels[-1] if p_labels else resolve_quarter_label(ticker, release_date)
    fy, fq, clean_q_lbl = parse_quarter_year(q0_label_raw, fallback_date=release_date)

    rx = pt.get("post_print_reaction") or {}
    t1_base = pt.get("t1_baseline") or {}
    sc = pt.get("beat_miss_scorecard") or {}
    rev_sc = sc.get("revenue") or {}
    eps_ng_sc = sc.get("eps_nongaap") or {}
    eps_g_sc = sc.get("eps_gaap") or {}
    facts = pt.get("company_specific_facts") or {}

    t1_html, t0_html, t1_sig, t0_sig = _resolve_published_html_and_signoffs(ticker, release_date)

    with get_connection(db_path) as conn:
        final_cik, ccy = _upsert_company(conn, ticker=ticker)

        conn.execute(
            """
            INSERT INTO earnings_events (
                event_id, ticker, cik, fiscal_year, fiscal_quarter, quarter_label, release_date,
                regular_close_price, after_hours_price, post_print_move_pct,
                atm_straddle_usd, implied_move_pct, overall_print_verdict,
                t1_html_filename, t0_html_filename, t1_signoff_status, t0_signoff_status, updated_at_utc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
                fiscal_year = excluded.fiscal_year,
                fiscal_quarter = excluded.fiscal_quarter,
                quarter_label = excluded.quarter_label,
                regular_close_price = excluded.regular_close_price,
                after_hours_price = excluded.after_hours_price,
                post_print_move_pct = excluded.post_print_move_pct,
                atm_straddle_usd = COALESCE(excluded.atm_straddle_usd, earnings_events.atm_straddle_usd),
                implied_move_pct = COALESCE(excluded.implied_move_pct, earnings_events.implied_move_pct),
                overall_print_verdict = excluded.overall_print_verdict,
                t1_html_filename = COALESCE(excluded.t1_html_filename, earnings_events.t1_html_filename),
                t0_html_filename = excluded.t0_html_filename,
                t1_signoff_status = COALESCE(excluded.t1_signoff_status, earnings_events.t1_signoff_status),
                t0_signoff_status = excluded.t0_signoff_status,
                updated_at_utc = excluded.updated_at_utc
            """,
            (
                event_id,
                ticker,
                final_cik,
                fy,
                fq,
                clean_q_lbl,
                release_date,
                _num(rx.get("regular_close_price")),
                _num(rx.get("after_hours_price")),
                _num(rx.get("post_print_move_pct")),
                _num(t1_base.get("atm_straddle_usd")),
                _num(rx.get("t1_options_implied_move_pct")) or _num(t1_base.get("options_implied_move_pct")),
                rx.get("overall_print_verdict"),
                t1_html,
                t0_html,
                t1_sig,
                t0_sig,
                now,
            ),
        )

        # Upsert T+0_SCORECARD consensus snapshot (recording exact consensus used in beat/miss scorecard)
        conn.execute(
            """
            INSERT INTO consensus_snapshots (
                event_id, ticker, stage, captured_at_utc, source,
                rev_consensus_m, rev_whisper_m, eps_nongaap_consensus, eps_gaap_consensus, eps_whisper,
                immutable_locked
            ) VALUES (?, ?, 'T+0_SCORECARD', ?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(event_id, stage) DO UPDATE SET
                captured_at_utc = excluded.captured_at_utc,
                source = excluded.source,
                rev_consensus_m = excluded.rev_consensus_m,
                rev_whisper_m = excluded.rev_whisper_m,
                eps_nongaap_consensus = excluded.eps_nongaap_consensus,
                eps_gaap_consensus = excluded.eps_gaap_consensus,
                eps_whisper = excluded.eps_whisper
            """,
            (
                event_id,
                ticker,
                now,
                f"ground_truth/{post_path.name}",
                _num(rev_sc.get("street_consensus_millions")),
                _num(rev_sc.get("whisper_millions")),
                _num(eps_ng_sc.get("street_consensus")),
                _num(eps_g_sc.get("street_consensus")),
                _num(eps_ng_sc.get("whisper")),
            ),
        )

        # Upsert all 5 chronological quarters from stitched_5q_chronological (Q0 is authoritative 8-K Exhibit 99.1)
        rev_arr = s5c.get("total_revenue") or []
        gp_arr = s5c.get("gross_profit") or []
        opex_arr = s5c.get("operating_expenses") or []
        ebit_arr = s5c.get("operating_income") or []
        ni_arr = s5c.get("gaap_net_income") or []
        eps_g_arr = s5c.get("gaap_diluted_eps") or []
        eps_ng_arr = s5c.get("nongaap_diluted_eps") or []
        ocf_arr = s5c.get("operating_cash_flow") or []
        cap_arr = s5c.get("capital_expenditures") or []
        rep_arr = s5c.get("reported_fcf") or []
        sbc_arr = s5c.get("stock_based_compensation") or []
        lse_arr = s5c.get("finance_leases") or []
        tfcf_arr = s5c.get("true_fcf") or []

        def _at(arr: list, i: int) -> float | None:
            return _num(arr[i]) if i < len(arr) else None

        for i, pl in enumerate(p_labels):
            q_yr, q_num, q_short = parse_quarter_year(pl)
            is_q0 = (i == len(p_labels) - 1)
            src_filing = (
                f"SEC {((pt.get('sec_filing_metadata') or {}).get('form') or '8-K')} Exhibit 99.1 ({release_date})"
                if is_q0
                else ("10-K (T+0 Q4 Isolated)" if q_num == 4 else "10-Q (T+0 Stitched)")
            )
            lse_val = _at(lse_arr, i)
            if lse_val is None and len(lse_arr) == 1:
                lse_val = _num(lse_arr[0])

            cor_val = _num(facts.get("cost_of_revenue_q0")) if is_q0 else None
            rd_val = _num(facts.get("rd_q0")) if is_q0 else None
            sm_val = _num(facts.get("sm_q0")) if is_q0 else None
            ga_val = (_num(facts.get("ga_q0")) or _num(facts.get("sga_q0"))) if is_q0 else None
            eps_ng_val = (_num(eps_ng_sc.get("reported_actual")) if is_q0 else None) or _at(eps_ng_arr, i)

            conn.execute(
                """
                INSERT INTO quarterly_financials (
                    ticker, cik, fiscal_year, fiscal_quarter, period_label, period_end_date,
                    duration_days, source_filing, reporting_currency,
                    revenue_m, cost_of_revenue_m, gross_profit_m, opex_m, rd_m, sm_m, ga_m,
                    ebit_m, net_income_gaap_m, eps_gaap, eps_nongaap,
                    ocf_3m_m, capex_3m_m, reported_fcf_3m_m, sbc_3m_m, leases_3m_m, true_fcf_3m_m,
                    updated_at_utc
                ) VALUES (?, ?, ?, ?, ?, NULL, 91, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticker, fiscal_year, fiscal_quarter) DO UPDATE SET
                    cik = COALESCE(excluded.cik, quarterly_financials.cik),
                    source_filing = CASE
                        WHEN quarterly_financials.source_filing LIKE 'SEC %' AND excluded.source_filing NOT LIKE 'SEC %'
                        THEN quarterly_financials.source_filing
                        ELSE excluded.source_filing
                    END,
                    revenue_m = COALESCE(excluded.revenue_m, quarterly_financials.revenue_m),
                    cost_of_revenue_m = COALESCE(excluded.cost_of_revenue_m, quarterly_financials.cost_of_revenue_m),
                    gross_profit_m = COALESCE(excluded.gross_profit_m, quarterly_financials.gross_profit_m),
                    opex_m = COALESCE(excluded.opex_m, quarterly_financials.opex_m),
                    rd_m = COALESCE(excluded.rd_m, quarterly_financials.rd_m),
                    sm_m = COALESCE(excluded.sm_m, quarterly_financials.sm_m),
                    ga_m = COALESCE(excluded.ga_m, quarterly_financials.ga_m),
                    ebit_m = COALESCE(excluded.ebit_m, quarterly_financials.ebit_m),
                    net_income_gaap_m = COALESCE(excluded.net_income_gaap_m, quarterly_financials.net_income_gaap_m),
                    eps_gaap = COALESCE(excluded.eps_gaap, quarterly_financials.eps_gaap),
                    eps_nongaap = COALESCE(excluded.eps_nongaap, quarterly_financials.eps_nongaap),
                    ocf_3m_m = COALESCE(excluded.ocf_3m_m, quarterly_financials.ocf_3m_m),
                    capex_3m_m = COALESCE(excluded.capex_3m_m, quarterly_financials.capex_3m_m),
                    reported_fcf_3m_m = COALESCE(excluded.reported_fcf_3m_m, quarterly_financials.reported_fcf_3m_m),
                    sbc_3m_m = COALESCE(excluded.sbc_3m_m, quarterly_financials.sbc_3m_m),
                    leases_3m_m = COALESCE(excluded.leases_3m_m, quarterly_financials.leases_3m_m),
                    true_fcf_3m_m = COALESCE(excluded.true_fcf_3m_m, quarterly_financials.true_fcf_3m_m),
                    updated_at_utc = excluded.updated_at_utc
                """,
                (
                    ticker,
                    final_cik,
                    q_yr,
                    q_num,
                    q_short,
                    src_filing,
                    ccy,
                    _at(rev_arr, i),
                    cor_val,
                    _at(gp_arr, i),
                    _at(opex_arr, i),
                    rd_val,
                    sm_val,
                    ga_val,
                    _at(ebit_arr, i),
                    _at(ni_arr, i),
                    _at(eps_g_arr, i),
                    eps_ng_val,
                    _at(ocf_arr, i),
                    _at(cap_arr, i),
                    _at(rep_arr, i),
                    _at(sbc_arr, i),
                    lse_val if lse_val is not None else 0.0,
                    _at(tfcf_arr, i),
                    now,
                ),
            )

        _ingest_post_bus_ledger(conn, event_id, ticker, release_date, now)
        conn.commit()


def _upsert_ledger_row(
    conn: sqlite3.Connection,
    event_id: str,
    ticker: str,
    entry_type: str,
    metric_name: str,
    target_period: str | None,
    prior_or_cons: str | None,
    actual_or_guided: str | None,
    v_act: float | None,
    v_cons: float | None,
    v_whisp: float | None,
    delta_txt: str | None,
    verdict: str | None,
    source_file: str,
    now: str,
) -> None:
    if not metric_name:
        return
    conn.execute(
        """
        INSERT INTO segment_and_guidance_ledger (
            event_id, ticker, entry_type, metric_name, target_period,
            prior_or_consensus_text, actual_or_guided_text,
            value_actual, value_consensus, value_whisper,
            delta_text, verdict_or_badge, source_file, updated_at_utc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(event_id, entry_type, metric_name) DO UPDATE SET
            target_period = COALESCE(excluded.target_period, segment_and_guidance_ledger.target_period),
            prior_or_consensus_text = COALESCE(excluded.prior_or_consensus_text, segment_and_guidance_ledger.prior_or_consensus_text),
            actual_or_guided_text = COALESCE(excluded.actual_or_guided_text, segment_and_guidance_ledger.actual_or_guided_text),
            value_actual = COALESCE(excluded.value_actual, segment_and_guidance_ledger.value_actual),
            value_consensus = COALESCE(excluded.value_consensus, segment_and_guidance_ledger.value_consensus),
            value_whisper = COALESCE(excluded.value_whisper, segment_and_guidance_ledger.value_whisper),
            delta_text = COALESCE(excluded.delta_text, segment_and_guidance_ledger.delta_text),
            verdict_or_badge = COALESCE(excluded.verdict_or_badge, segment_and_guidance_ledger.verdict_or_badge),
            source_file = excluded.source_file,
            updated_at_utc = excluded.updated_at_utc
        """,
        (
            event_id,
            ticker,
            entry_type,
            metric_name.strip(),
            target_period,
            prior_or_cons,
            actual_or_guided,
            v_act,
            v_cons,
            v_whisp,
            delta_txt,
            verdict,
            source_file,
            now,
        ),
    )


def _ingest_pre_bus_ledger(conn: sqlite3.Connection, event_id: str, ticker: str, release_date: str, now: str) -> None:
    p2a_rel = f"pre_agent_bus/{ticker}_{release_date}_pre_agent2a_kpis.json"
    p2a = _load_json(BASE_DIR / p2a_rel)
    if p2a:
        up_q = p2a.get("upcoming_quarter_label")
        for row in p2a.get("headline_and_company_kpis") or []:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "OPERATIONAL_KPI",
                str(row.get("metric") or ""),
                up_q,
                str(row.get("street_consensus_q0e") or ""),
                str(row.get("whisper_bogey_q0e") or ""),
                None,
                _num(row.get("street_consensus_q0e")),
                _num(row.get("whisper_bogey_q0e")),
                str(row.get("whisper_spread_display") or ""),
                str(row.get("hurdle_badge") or "PRE_PRINT"),
                p2a_rel,
                now,
            )

    p2b_rel = f"pre_agent_bus/{ticker}_{release_date}_pre_agent2b_guidance.json"
    p2b = _load_json(BASE_DIR / p2b_rel)
    if p2b:
        if p2b.get("credibility_score") is not None:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "CREDIBILITY_SCORE",
                "Executive Guidance Credibility Score (0-100)",
                None,
                None,
                str(p2b.get("credibility_label") or p2b.get("credibility_score")),
                _num(p2b.get("credibility_score")),
                None,
                None,
                None,
                "CREDIBILITY",
                p2b_rel,
                now,
            )
        for row in p2b.get("matrix_b_forward_guidance_bogeys") or []:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "FORWARD_GUIDANCE",
                str(row.get("forward_metric") or ""),
                "Forward Bogey",
                str(row.get("street_consensus_hurdle") or ""),
                str(row.get("bull_case_bogey") or ""),
                None,
                None,
                None,
                str(row.get("bear_case_breakdown") or ""),
                str(row.get("sensitivity_badge") or ""),
                p2b_rel,
                now,
            )


def _ingest_post_bus_ledger(conn: sqlite3.Connection, event_id: str, ticker: str, release_date: str, now: str) -> None:
    q_lbl = resolve_quarter_label(ticker, release_date)
    b2a_rel = f"post_agent_bus/{ticker}_{release_date}_agent2a_kpis.json"
    b2a = _load_json(BASE_DIR / b2a_rel)
    if b2a:
        for row in b2a.get("company_operational_kpis") or []:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "OPERATIONAL_KPI",
                str(row.get("kpi_name") or row.get("metric") or ""),
                q_lbl,
                str(row.get("street_consensus") or ""),
                str(row.get("reported_q0_actual") or ""),
                _num(row.get("reported_q0_actual")),
                _num(row.get("street_consensus")),
                _num(row.get("t1_whisper")),
                str(row.get("vs_consensus_delta") or ""),
                str(row.get("verdict") or ""),
                b2a_rel,
                now,
            )
        seg_map = b2a.get("reporting_segments_5q_mapping")
        seg_list = seg_map if isinstance(seg_map, list) else (seg_map.get("segments") if isinstance(seg_map, dict) else [])
        for seg in seg_list or []:
            if not isinstance(seg, dict):
                continue
            s_name = str(seg.get("segment_name") or seg.get("name") or "")
            vals = seg.get("values_5q_plus_q1e") or seg.get("values") or []
            q0_v = _num(seg.get("q0_revenue_millions"))
            if q0_v is None and isinstance(vals, list) and len(vals) >= 5:
                q0_v = _num(vals[4])
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "REPORTING_SEGMENT",
                s_name,
                q_lbl,
                None,
                f"{q0_v}M" if q0_v is not None else None,
                q0_v,
                None,
                None,
                str(seg.get("yoy_growth_q0") or ""),
                "SEGMENT_Q0",
                b2a_rel,
                now,
            )

    b2b_rel = f"post_agent_bus/{ticker}_{release_date}_agent2b_transcript.json"
    b2b = _load_json(BASE_DIR / b2b_rel)
    if b2b:
        for row in b2b.get("guidance_accountability_matrix_a") or []:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "GUIDANCE_ACCOUNTABILITY",
                str(row.get("guided_metric") or ""),
                q_lbl,
                str(row.get("prior_quarter_guidance") or ""),
                str(row.get("reported_q0_actual") or ""),
                None,
                None,
                None,
                str(row.get("variance_commentary") or ""),
                str(row.get("credibility_grade") or ""),
                b2b_rel,
                now,
            )
        for row in b2b.get("forward_guidance_reset_matrix_b") or []:
            _upsert_ledger_row(
                conn,
                event_id,
                ticker,
                "FORWARD_GUIDANCE",
                str(row.get("forward_horizon_and_metric") or ""),
                "Forward Reset",
                str(row.get("preprint_street_consensus") or ""),
                str(row.get("new_management_guidance") or ""),
                None,
                None,
                None,
                str(row.get("delta_vs_street") or ""),
                str(row.get("action_badge") or ""),
                b2b_rel,
                now,
            )


def get_locked_t1_consensus(ticker: str, release_date: str, db_path: Path = DB_PATH) -> dict | None:
    """Retrieve immutable T-1 locked consensus snapshot for (ticker, release_date) from SQLite if present."""
    if not db_path.exists():
        return None
    event_id = f"{ticker.upper()}_{release_date}"
    try:
        with get_connection(db_path) as conn:
            row = conn.execute(
                "SELECT * FROM consensus_snapshots WHERE event_id = ? AND stage = 'T-1_LOCKED'",
                (event_id,),
            ).fetchone()
            return dict(row) if row else None
    except Exception:
        return None


def sync_orphan_published_html(db_path: Path = DB_PATH) -> None:
    """Ensure every canonical HTML report in published_reports/ is linked in earnings_events (even legacy ones without truth.json)."""
    init_db(db_path)
    now = _utc_now()
    with get_connection(db_path) as conn:
        for f in sorted(REPORTS_DIR.glob("*.html")):
            if f.name in ("index.html", "news.html"):
                continue
            m_t1 = re.match(r"^([A-Z0-9.\-]+)_T1_(\d{4}-\d{2}-\d{2})\.html$", f.name)
            m_t0 = re.match(r"^([A-Z0-9.\-]+)_T0_POST_(\d{4}-\d{2}-\d{2})\.html$", f.name)
            m = m_t1 or m_t0
            if not m:
                continue
            tk, dt = m.group(1), m.group(2)
            event_id = f"{tk}_{dt}"
            t1_html, t0_html, t1_sig, t0_sig = _resolve_published_html_and_signoffs(tk, dt)
            ev = conn.execute("SELECT event_id FROM earnings_events WHERE event_id = ?", (event_id,)).fetchone()
            if ev:
                conn.execute(
                    """
                    UPDATE earnings_events
                       SET t1_html_filename = COALESCE(?, t1_html_filename),
                           t0_html_filename = ?,
                           t1_signoff_status = COALESCE(?, t1_signoff_status),
                           t0_signoff_status = COALESCE(?, t0_signoff_status),
                           updated_at_utc = ?
                     WHERE event_id = ?
                    """,
                    (t1_html, t0_html, t1_sig, t0_sig, now, event_id),
                )
            else:
                q_lbl = resolve_quarter_label(tk, dt)
                fy, fq, clean_q_lbl = parse_quarter_year(q_lbl, fallback_date=dt)
                _upsert_company(conn, ticker=tk)
                conn.execute(
                    """
                    INSERT INTO earnings_events (
                        event_id, ticker, fiscal_year, fiscal_quarter, quarter_label, release_date,
                        t1_html_filename, t0_html_filename, t1_signoff_status, t0_signoff_status, updated_at_utc
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (event_id, tk, fy, fq, clean_q_lbl, dt, t1_html, t0_html, t1_sig, t0_sig, now),
                )
        conn.commit()


def backfill_all(db_path: Path = DB_PATH, allow_unlock_consensus: bool = False) -> dict[str, int]:
    """Idempotently backfill all T-1 truth files, T+0 post_truth files, agent bus ledgers, and published HTML links."""
    init_db(db_path)
    t1_files = sorted(p for p in GROUND_TRUTH_DIR.glob("*_truth.json") if not p.name.endswith("_post_truth.json"))
    t0_files = sorted(GROUND_TRUTH_DIR.glob("*_post_truth.json"))

    for p in t1_files:
        m = re.match(r"^([A-Z0-9.\-]+)_(\d{4}-\d{2}-\d{2})_truth\.json$", p.name)
        if m:
            ingest_t1_truth(m.group(1), m.group(2), db_path=db_path, allow_unlock_consensus=allow_unlock_consensus)

    for p in t0_files:
        m = re.match(r"^([A-Z0-9.\-]+)_(\d{4}-\d{2}-\d{2})_post_truth\.json$", p.name)
        if m:
            ingest_t0_post_truth(m.group(1), m.group(2), db_path=db_path)

    sync_orphan_published_html(db_path=db_path)
    return get_table_counts(db_path=db_path)


def get_table_counts(db_path: Path = DB_PATH) -> dict[str, int]:
    tables = (
        "companies",
        "earnings_events",
        "consensus_snapshots",
        "quarterly_financials",
        "segment_and_guidance_ledger",
    )
    with get_connection(db_path) as conn:
        return {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in tables}


def export_static_manifests(db_path: Path = DB_PATH) -> dict[str, Any]:
    """
    Compile static browser manifests directly from `earnings_warehouse.db` for zero-server GitHub Pages hosting:
      1. published_reports/history_catalog.js (window.EARNINGS_HISTORY_CATALOG)
      2. published_reports/warehouse_summary.json (companies, events, consensus, and 5Q+ financials)
    """
    init_db(db_path)
    sync_orphan_published_html(db_path=db_path)
    REPORTS_DIR.mkdir(exist_ok=True)

    history_catalog: dict[str, list[dict[str, Any]]] = {}
    warehouse_summary: dict[str, Any] = {
        "generated_at_utc": _utc_now(),
        "database_engine": "SQLite 3 (earnings_warehouse.db)",
        "table_counts": get_table_counts(db_path=db_path),
        "tickers": {},
    }

    with get_connection(db_path) as conn:
        comp_rows = conn.execute("SELECT * FROM companies ORDER BY ticker").fetchall()
        for comp in comp_rows:
            tk = comp["ticker"]
            ev_rows = conn.execute(
                """
                SELECT e.*,
                       c_t1.rev_consensus_m AS t1_rev_cons_m,
                       c_t1.eps_nongaap_consensus AS t1_eps_cons,
                       c_t0.rev_consensus_m AS t0_rev_cons_m
                  FROM earnings_events e
                  LEFT JOIN consensus_snapshots c_t1 ON c_t1.event_id = e.event_id AND c_t1.stage = 'T-1_LOCKED'
                  LEFT JOIN consensus_snapshots c_t0 ON c_t0.event_id = e.event_id AND c_t0.stage = 'T+0_SCORECARD'
                 WHERE e.ticker = ?
                 ORDER BY e.release_date DESC
                """,
                (tk,),
            ).fetchall()

            qf_rows = conn.execute(
                """
                SELECT fiscal_year, fiscal_quarter, period_label, period_end_date, duration_days,
                       source_filing, reporting_currency, revenue_m, gross_profit_m, opex_m, ebit_m,
                       net_income_gaap_m, eps_gaap, eps_nongaap, ocf_3m_m, capex_3m_m,
                       reported_fcf_3m_m, sbc_3m_m, leases_3m_m, true_fcf_3m_m
                  FROM quarterly_financials
                 WHERE ticker = ?
                 ORDER BY fiscal_year ASC, fiscal_quarter ASC
                """,
                (tk,),
            ).fetchall()

            qf_by_yq = {(r["fiscal_year"], r["fiscal_quarter"]): dict(r) for r in qf_rows}

            cat_entries = []
            events_out = []
            for ev in ev_rows:
                qf_match = qf_by_yq.get((ev["fiscal_year"], ev["fiscal_quarter"]))
                rev_act = qf_match["revenue_m"] if (qf_match and ev["t0_html_filename"]) else None
                rev_cons = ev["t0_rev_cons_m"] if ev["t0_rev_cons_m"] is not None else ev["t1_rev_cons_m"]

                if ev["t1_html_filename"] or ev["t0_html_filename"]:
                    cat_entries.append(
                        {
                            "date": ev["release_date"],
                            "quarter": ev["quarter_label"],
                            "date_display": format_short_date(ev["release_date"]),
                            "t1": ev["t1_html_filename"],
                            "t0": ev["t0_html_filename"],
                            "verdict": ev["overall_print_verdict"],
                            "post_move_pct": ev["post_print_move_pct"],
                            "rev_actual_m": rev_act,
                            "rev_consensus_m": rev_cons,
                            "currency": comp["reporting_currency"],
                        }
                    )

                events_out.append(
                    {
                        "event_id": ev["event_id"],
                        "quarter_label": ev["quarter_label"],
                        "fiscal_year": ev["fiscal_year"],
                        "fiscal_quarter": ev["fiscal_quarter"],
                        "release_date": ev["release_date"],
                        "spot_price_t1": ev["spot_price_t1"],
                        "regular_close_price": ev["regular_close_price"],
                        "after_hours_price": ev["after_hours_price"],
                        "post_print_move_pct": ev["post_print_move_pct"],
                        "implied_move_pct": ev["implied_move_pct"],
                        "overall_print_verdict": ev["overall_print_verdict"],
                        "rev_consensus_m": rev_cons,
                        "rev_actual_m": rev_act,
                        "t1_html": ev["t1_html_filename"],
                        "t0_html": ev["t0_html_filename"],
                    }
                )

            if cat_entries:
                history_catalog[tk] = cat_entries

            warehouse_summary["tickers"][tk] = {
                "company_name": comp["company_name"],
                "cik": comp["cik"],
                "sector": comp["sector"],
                "reporting_currency": comp["reporting_currency"],
                "fiscal_year_end_month": comp["fiscal_year_end_month"],
                "events": events_out,
                "quarterly_financials": [dict(r) for r in qf_rows],
            }

    catalog_js = (
        "// Auto-generated Historical Quarter Archive Catalog from earnings_warehouse.db\n"
        f"window.EARNINGS_HISTORY_CATALOG = {json.dumps(history_catalog, indent=2)};\n"
    )
    (REPORTS_DIR / "history_catalog.js").write_text(catalog_js, encoding="utf-8")
    (REPORTS_DIR / "warehouse_summary.json").write_text(json.dumps(warehouse_summary, indent=2), encoding="utf-8")
    return history_catalog


def audit_warehouse(db_path: Path = DB_PATH) -> list[str]:
    """
    Deterministic relational integrity audit across all 5 tables:
      1. Foreign key integrity (`PRAGMA foreign_key_check`)
      2. Zero YTD rows (`duration_days` outside 80..100) and zero FCF formula mismatches
      3. Dual-class CIK parity (e.g. GOOGL vs GOOG sharing CIK 0001652044 must match on Q0 corporate revenue & OCF)
      4. T-1_LOCKED vs T+0_SCORECARD consensus parity (zero post-print consensus drift)
      5. 100% coverage of canonical published HTML tearsheets in `earnings_events`
    """
    errors: list[str] = []
    with get_connection(db_path) as conn:
        fk_errs = conn.execute("PRAGMA foreign_key_check;").fetchall()
        for r in fk_errs:
            errors.append(f"[FK_VIOLATION] {dict(r)}")

        # 2. Check duration_days & FCF math
        bad_dur = conn.execute(
            "SELECT ticker, period_label, duration_days FROM quarterly_financials WHERE duration_days NOT BETWEEN 80 AND 100"
        ).fetchall()
        for r in bad_dur:
            errors.append(f"[DURATION_VIOLATION] {r['ticker']} {r['period_label']} duration={r['duration_days']}d")

        # 3. Dual-class CIK corporate parity (e.g., GOOGL vs GOOG on 8-K Q0 rows)
        cik_mismatch = conn.execute(
            """
            SELECT a.cik, a.fiscal_year, a.fiscal_quarter, a.ticker AS tk_a, b.ticker AS tk_b,
                   a.revenue_m AS rev_a, b.revenue_m AS rev_b, a.ocf_3m_m AS ocf_a, b.ocf_3m_m AS ocf_b
              FROM quarterly_financials a
              JOIN quarterly_financials b
                ON a.cik = b.cik
               AND a.fiscal_year = b.fiscal_year
               AND a.fiscal_quarter = b.fiscal_quarter
               AND a.ticker < b.ticker
             WHERE a.cik IS NOT NULL
               AND (
                   (a.revenue_m IS NOT NULL AND b.revenue_m IS NOT NULL AND ABS(a.revenue_m - b.revenue_m) > 1.0)
                   OR (a.ocf_3m_m IS NOT NULL AND b.ocf_3m_m IS NOT NULL AND ABS(a.ocf_3m_m - b.ocf_3m_m) > 1.0)
               )
            """
        ).fetchall()
        for r in cik_mismatch:
            errors.append(
                f"[CIK_SHARE_CLASS_DRIFT] CIK {r['cik']} Q{r['fiscal_quarter']} {r['fiscal_year']}: "
                f"{r['tk_a']} (rev={r['rev_a']}, ocf={r['ocf_a']}) != {r['tk_b']} (rev={r['rev_b']}, ocf={r['ocf_b']})"
            )

        # 4. Consensus drift check between T-1_LOCKED and T+0_SCORECARD
        cons_drift = conn.execute(
            """
            SELECT t1.event_id, t1.rev_consensus_m AS t1_rev, t0.rev_consensus_m AS t0_rev
              FROM consensus_snapshots t1
              JOIN consensus_snapshots t0
                ON t1.event_id = t0.event_id
               AND t1.stage = 'T-1_LOCKED'
               AND t0.stage = 'T+0_SCORECARD'
             WHERE t1.rev_consensus_m IS NOT NULL
               AND t0.rev_consensus_m IS NOT NULL
               AND ABS(t1.rev_consensus_m - t0.rev_consensus_m) / MAX(ABS(t1.rev_consensus_m), 1.0) > 0.015
            """
        ).fetchall()
        for r in cons_drift:
            errors.append(
                f"[CONSENSUS_DRIFT] {r['event_id']}: T-1_LOCKED rev={r['t1_rev']}M vs T+0_SCORECARD rev={r['t0_rev']}M"
            )

        # 5. Verify every canonical HTML in published_reports/ (unless rejected by Agent 5) is registered
        for f in sorted(REPORTS_DIR.glob("*.html")):
            if f.name in ("index.html", "news.html") or "_v" in f.stem:
                continue
            m_t1 = re.match(r"^([A-Z0-9.\-]+)_T1_(\d{4}-\d{2}-\d{2})\.html$", f.name)
            m_t0 = re.match(r"^([A-Z0-9.\-]+)_T0_POST_(\d{4}-\d{2}-\d{2})\.html$", f.name)
            if m_t1:
                row = conn.execute("SELECT t1_html_filename FROM earnings_events WHERE t1_html_filename = ?", (f.name,)).fetchone()
                if not row:
                    errors.append(f"[UNLINKED_HTML] {f.name} missing from earnings_events.t1_html_filename")
            elif m_t0:
                tk, dt = m_t0.group(1), m_t0.group(2)
                sig = _load_json(AUDIT_DIR / f"{tk}_{dt}_agent5_signoff.json").get("status")
                if sig is None or sig == "APPROVED":
                    row = conn.execute("SELECT t0_html_filename FROM earnings_events WHERE t0_html_filename = ?", (f.name,)).fetchone()
                    if not row:
                        errors.append(f"[UNLINKED_HTML] {f.name} missing from earnings_events.t0_html_filename")

    return errors


if __name__ == "__main__":
    flags = {a.lower() for a in sys.argv[1:]}
    allow_unlock = "--force-unlock-consensus" in flags

    if "--audit-only" not in flags:
        counts = backfill_all(DB_PATH, allow_unlock_consensus=allow_unlock)
        catalog = export_static_manifests(DB_PATH)
        print(f"[WAREHOUSE] Backfilled & exported {DB_PATH.name}:")
        for tbl, cnt in counts.items():
            print(f"  - {tbl:30s}: {cnt:4d} rows")
        print(f"  - Static Archive Tickers      : {len(catalog):4d} tickers -> published_reports/history_catalog.js & warehouse_summary.json")

    audit_errs = audit_warehouse(DB_PATH)
    if audit_errs:
        print(f"[WAREHOUSE AUDIT FAILED] {len(audit_errs)} violations:")
        for err in audit_errs:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("[WAREHOUSE AUDIT PASSED] 0 relational, FCF, CIK share-class, consensus-lock, or HTML-link violations.")
        sys.exit(0)
