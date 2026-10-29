"""
Enhanced Dashboard & AI Discover News Portal Generator for Institutional Earnings Intelligence
Discovers and displays:
- Perplexity Discover-Style Top Financial Market News & tickers.txt Portfolio News Portal
- Interactive Hovercards (popover="hint" + interestfor) showing Quick Pop-Up Summaries from Post-Earnings Reports
- Modal Detailed AI Synthesis Reports (<dialog closedby="any">) on Tile Click
- T-1 Pre-Earnings Briefings ({TICKER}_T1_{DATE}.html)
- T+0 Post-Earnings Forensic Tearsheets ({TICKER}_T0_POST_{DATE}.html)
"""

import html
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from archive_topbar import resolve_quarter_label, format_short_date

# The news portal is optional: a portal bug must never fail a tearsheet publish (Stage 4 imports this module).
try:
    import build_news_portal as news_portal
except Exception as exc:
    news_portal = None
    print(f"WARNING: build_news_portal import failed ({type(exc).__name__}: {exc}); index will render without the news portal.", file=sys.stderr)

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"
AUDIT_DIR = BASE_DIR / "audit_logs"
LEDGER_PATH = BASE_DIR / "published_ledger.json"
TUNNEL_FILE = BASE_DIR / "tunnel_url.json"
GITHUB_PAGES_BASE = "https://nitchau.github.io/earnings-intelligence"
# Quick tunnels (trycloudflare.com) die with the serve_reports.py process; an older URL is presumed dead.
TUNNEL_MAX_AGE_SECONDS = 6 * 3600
try:
    ET = ZoneInfo("America/New_York")
except Exception:  # no tz database (Windows without tzdata): Stage 4 imports this module and must not fail
    ET = None


def warn(msg: str):
    print(f"WARNING: {msg}", file=sys.stderr)


def portal_call(name: str, *args, default="", **kwargs):
    if news_portal is None:
        return default
    try:
        return getattr(news_portal, name)(*args, **kwargs)
    except Exception as exc:
        warn(f"news portal {name}() failed ({type(exc).__name__}: {exc}); continuing without it.")
        return default


def get_base_urls(now_epoch: float | None = None):
    """The tunnel URL is used only while tunnel_url.json is fresh (< 6h); otherwise GitHub Pages."""
    local_base = "http://localhost:8080"
    public_base = GITHUB_PAGES_BASE
    if TUNNEL_FILE.exists():
        try:
            t_data = json.loads(TUNNEL_FILE.read_text(encoding="utf-8"))
            tunnel = str(t_data.get("tunnel_url") or "").strip().rstrip("/")
            updated_at = t_data.get("updated_at")
            age = (time.time() if now_epoch is None else now_epoch) - float(updated_at)
            # small negative age tolerates clock skew; a far-future stamp is not trusted
            if tunnel.startswith(("https://", "http://")) and -300 <= age <= TUNNEL_MAX_AGE_SECONDS:
                public_base = tunnel
        except Exception:
            pass
    return local_base, public_base


def scraped_text(fragment: str) -> str:
    """Scraped HTML text -> raw (unescaped) string; it is escaped exactly once when rendered."""
    return html.unescape(fragment).strip()


def extract_metadata_from_html(html_path: Path) -> dict:
    """All returned strings are raw text (entities decoded), never HTML."""
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

    m_sym = re.search(r'<span class="ticker-symbol">([A-Z0-9.\-]+)</span>', content)
    if m_sym:
        meta["ticker"] = m_sym.group(1)

    m_name = re.search(r'<h1 class="company-name">([^<]+)</h1>', content)
    if m_name:
        meta["company_name"] = scraped_text(m_name.group(1))

    m_sec = re.search(r'<div class="sector-tag">([^<]+)', content)
    if m_sec:
        meta["sector"] = scraped_text(m_sec.group(1)).split("•")[0].strip()

    m_price = re.search(r'<div class="price-value">\$([0-9,.]+)(?:\s*/\s*<span[^>]*>\$([0-9,.]+))?', content)
    if m_price:
        # T+0 headers read "close / after-hours"; only the after-hours figure belongs on a T+0 card
        price = m_price.group(2) if is_post else m_price.group(1)
        if price:
            meta["spot_price"] = f"${price}"

    m_move = re.search(r'Options-Implied Move[^<]*</span>\s*<span class="strip-val"[^>]*>([^<]+)</span>', content)
    if m_move:
        meta["implied_move"] = scraped_text(m_move.group(1))

    m_date = re.search(r'(?:Upcoming|Official Earnings|Reported Date)[^<]*Release Date</span>\s*<span class="strip-val">([^<]+)', content)
    if m_date:
        # the strip value continues "<date> • <span>AMC</span>"; drop the dangling separator
        meta["earnings_date"] = scraped_text(m_date.group(1)).rstrip("•· \t\r\n")

    return meta


def format_earnings_date(display: str, iso_date: str) -> str:
    """Scraped display date if present (ISO strings reformatted), else the filename date as 'Oct 21, 2026'."""
    for value in (display, iso_date):
        value = (value or "").strip().rstrip("•· \t\r\n")
        if not value:
            continue
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            try:
                d = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                return value
            return f"{d:%b} {d.day}, {d.year}"
        return value
    return ""


def _eastern_fallback_tz(ts: float) -> timezone:
    """US Eastern offset by the post-2007 DST rule (2nd Sun Mar 07:00 UTC .. 1st Sun Nov 06:00 UTC)."""
    utc = datetime.fromtimestamp(ts, timezone.utc).replace(tzinfo=None)
    mar8, nov1 = datetime(utc.year, 3, 8), datetime(utc.year, 11, 1)
    dst_start = mar8 + timedelta(days=(6 - mar8.weekday()) % 7, hours=7)
    dst_end = nov1 + timedelta(days=(6 - nov1.weekday()) % 7, hours=6)
    return timezone(timedelta(hours=-4 if dst_start <= utc < dst_end else -5))


def format_et(ts: float, fmt: str) -> str:
    """Epoch seconds -> America/New_York wall time with an explicit ET suffix."""
    tz = ET if ET is not None else _eastern_fallback_tz(ts)
    return datetime.fromtimestamp(ts, tz).strftime(fmt) + " ET"


def signoff_rejected(ticker: str, e_date: str) -> bool:
    """True when the T+0 Agent 5 signoff exists but is not APPROVED (unreadable signoff fails closed)."""
    path = AUDIT_DIR / f"{ticker}_{e_date}_agent5_signoff.json"
    if not path.exists():
        return False
    status = load_truth_json(path).get("status")
    return status != "APPROVED"


def load_truth_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def truth_section(data: dict, key: str) -> dict:
    section = data.get(key)
    return section if isinstance(section, dict) else {}


def as_positive_number(value):
    if isinstance(value, bool):
        return None
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    return num if num > 0 else None


def extract_metadata_from_truth(ticker: str, e_date: str, is_post: bool) -> dict:
    """Card numbers come verbatim from Stage 1 ground truth (AGENTS.md Rule 2), never from defaults."""
    t1_truth = load_truth_json(GROUND_TRUTH_DIR / f"{ticker}_{e_date}_truth.json")
    if is_post:
        post_truth = load_truth_json(GROUND_TRUTH_DIR / f"{ticker}_{e_date}_post_truth.json")
        reaction = truth_section(post_truth, "post_print_reaction")
        price = as_positive_number(reaction.get("after_hours_price"))
        move = as_positive_number(reaction.get("t1_options_implied_move_pct"))
        if move is None:
            move = as_positive_number(truth_section(post_truth, "t1_baseline").get("options_implied_move_pct"))
    else:
        price = as_positive_number(truth_section(t1_truth, "price_validation").get("yahoo_spot_price"))
        move = as_positive_number(truth_section(t1_truth, "options_positioning").get("atm_implied_move_pct"))

    # raw strings: build_cards_html escapes every interpolated value exactly once
    return {
        "company_name": str(t1_truth.get("company_name") or "").strip(),
        "sector": str(t1_truth.get("sector") or "").strip(),
        "price": f"${price:,.2f}" if price is not None else "",
        "implied_move": f"±{move:.2f}%" if move is not None else "",
    }


def esc(value) -> str:
    """Single point of HTML escaping for card output (attributes and text)."""
    return html.escape(str(value), quote=True)


def post_hovercard_tickers(grouped: dict) -> set:
    """
    Tickers whose portal hovercard (hovercard-{TICKER}) shows the T+0 summary: the latest listed T+0 date is
    on/after the latest T-1 date (mirrors build_news_portal.discover_ticker_intelligence). T-1 cards of these
    tickers are superseded and must not open that hovercard.
    """
    latest = {}
    for item in grouped.values():
        slot = latest.setdefault(item["ticker"], {"post": "", "pre": ""})
        kind = "post" if item["is_post"] else "pre"
        slot[kind] = max(slot[kind], item["earnings_date"])
    return {tk for tk, d in latest.items() if d["post"] and d["post"] >= d["pre"]}


def build_cards_html(grouped: dict, link_prefix: str) -> str:
    cards_html = []
    sorted_keys = sorted(
        grouped.keys(),
        key=lambda k: (grouped[k]["earnings_date"], grouped[k]["is_post"], grouped[k]["ticker"]),
        reverse=True
    )
    superseded_pre = post_hovercard_tickers(grouped)

    for key in sorted_keys:
        item = grouped[key]
        ticker = item["ticker"]
        e_date = item["earnings_date"]
        is_post = item["is_post"]
        category_val = "post" if is_post else "pre"

        ver_nums = sorted(item["versions"].keys())
        latest_file = item["canonical"] or (item["versions"][ver_nums[-1]] if ver_nums else None)
        if not latest_file:
            continue

        latest_ver_label = f"v{ver_nums[-1]}" if ver_nums else "v1"
        mod_time = format_et(latest_file.stat().st_mtime, "%b %d, %Y • %I:%M %p")

        # Raw (unescaped) values; each is escaped exactly once at interpolation below.
        meta = extract_metadata_from_html(latest_file)
        truth = extract_metadata_from_truth(ticker, e_date, is_post)
        company_name = meta["company_name"] or truth["company_name"] or ticker
        spot_price = truth["price"] or meta["spot_price"] or "—"
        implied_move = truth["implied_move"] or meta["implied_move"] or "—"
        sector = meta["sector"] or truth["sector"]
        e_date_display = format_earnings_date(meta["earnings_date"], e_date)
        sector_line = " • ".join(x for x in (sector, e_date_display) if x)

        badge_style = "background: rgba(16, 185, 129, 0.2); border-color: rgba(16, 185, 129, 0.4); color: #34d399;" if is_post else "background: rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3); color: #60a5fa;"
        status_label = "T+0 POST-EARNINGS" if is_post else "T-1 PRE-EARNINGS"
        price_label = "After-Hours Price" if is_post else "Spot Price"

        # The ticker hovercard summarizes the T+0 event once one exists; a T-1 card keeps its links but drops the trigger.
        if not is_post and ticker in superseded_pre:
            hc_attrs = ""
        else:
            hc_id = esc(f"hovercard-{ticker}")
            hc_attrs = f' interestfor="{hc_id}" data-hovercard-id="{hc_id}" data-ticker="{esc(ticker)}"'

        q_label = resolve_quarter_label(ticker, e_date)
        canonical_href = esc(f"{link_prefix}{latest_file.name}")

        card = f"""
        <div class="report-card" data-category="{esc(category_val)}" data-ticker="{esc(ticker.lower())}" data-company="{esc(company_name.lower())}">
          <div class="card-top">
            <div class="ticker-box">
              <a href="{canonical_href}"{hc_attrs} class="ticker-symbol" style="text-decoration:none;">{esc(ticker)}</a>
              <span class="version-tag">{esc(q_label)}</span>
            </div>
            <span class="badge-status" style="{esc(badge_style)}">{esc(status_label)}</span>
          </div>

          <div class="company-title"><a href="{canonical_href}"{hc_attrs} style="color:inherit;text-decoration:none;">{esc(company_name)}</a></div>
          <div class="sector-line">{esc(sector_line)}</div>

          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-label">{esc(price_label)}</span>
              <span class="stat-val">{esc(spot_price)}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Implied Move</span>
              <span class="stat-val" style="color: #f59e0b;">{esc(implied_move)}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Updated</span>
              <span class="stat-val" style="font-size: 11.5px; color: #94a3b8;">{esc(mod_time)}</span>
            </div>
          </div>

          <div class="card-footer">
            <a href="{canonical_href}"{hc_attrs} class="btn-view">
              <span>Open Tearsheet</span>
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </a>
          </div>
        </div>
        """
        cards_html.append(card)

    return "\n".join(cards_html)


def build_full_page(cards_html: str, grouped: dict, public_base: str, link_prefix: str = "", snapshot: dict = None) -> str:
    total_count = len(grouped)
    pre_count = sum(1 for item in grouped.values() if not item["is_post"])
    post_count = sum(1 for item in grouped.values() if item["is_post"])

    portal_html, articles_json_str, portal_css, portal_js = "", "{}", "", ""
    if news_portal is not None:
        try:
            intel = news_portal.discover_ticker_intelligence(link_prefix=link_prefix)
            portal_html, articles_json_str = news_portal.build_discover_portal_section_html(intel)
            portal_css = news_portal.get_discover_portal_css()
            portal_js = news_portal.get_discover_portal_js(articles_json_str, intel)
        except Exception as exc:
            warn(f"Discover news portal failed ({type(exc).__name__}: {exc}); rendering the tearsheet library only.")
            portal_html, articles_json_str, portal_css, portal_js = "", "{}", "", ""

    market_strip_html = market_strip_css = market_strip_js = ""
    if snapshot is not None:
        market_strip_html = portal_call("render_market_strip_html", snapshot)
        if market_strip_html:
            market_strip_css = portal_call("get_market_strip_css")
            market_strip_js = portal_call("get_market_strip_js")

    last_updated_str = format_et(time.time(), "%B %d, %Y at %I:%M %p")
    tunnel_link_html = ""
    if public_base:
        label = "🌐 <strong>Production Live URL (GitHub Pages):</strong>" if "github.io" in public_base else "🌐 <strong>Public Live Tunnel:</strong>"
        safe_base = html.escape(public_base, quote=True)
        tunnel_link_html = f'<div class="tunnel-bar">{label} <a href="{safe_base}" target="_blank" rel="noopener" style="color:#60a5fa; text-decoration:none;">{safe_base}</a></div>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Institutional Earnings Intelligence &amp; AI Discover News Portal</title>
  {getattr(news_portal, 'FAVICON_LINK', '') if news_portal else ''}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #090d16;
      --card-bg: #111827;
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-blue: #3b82f6;
      --accent-blue-glow: rgba(59, 130, 246, 0.25);
      --bull-green: #10b981;
      --bull-green-glow: rgba(16, 185, 129, 0.25);
      --warn-amber: #f59e0b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; }}
    [id^="section-"] {{ scroll-margin-top: 84px; }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 26px 20px 50px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}
    .dashboard-container {{
      max-width: 1260px;
      width: 100%;
    }}
    .top-platform-nav {{
      position: sticky;
      top: 10px;
      z-index: 100;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      background: rgba(15, 23, 42, 0.92);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(59, 130, 246, 0.3);
      border-radius: 12px;
      padding: 10px 16px;
      margin-bottom: 24px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.45);
    }}
    .tp-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      font-weight: 800;
      color: #f8fafc;
    }}
    .tp-badge {{
      background: linear-gradient(135deg, #10b981, #3b82f6);
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      padding: 3px 8px;
      border-radius: 6px;
    }}
    .tp-links {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .tp-link {{
      color: #cbd5e1;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.08);
      background: rgba(255, 255, 255, 0.04);
      transition: all 0.15s ease;
    }}
    .tp-link:hover {{
      color: #ffffff;
      background: rgba(59, 130, 246, 0.22);
      border-color: rgba(59, 130, 246, 0.5);
    }}
    .tp-link.tp-highlight {{
      background: rgba(16, 185, 129, 0.16);
      border-color: rgba(16, 185, 129, 0.4);
      color: #34d399;
    }}
    .header {{
      text-align: center;
      margin-bottom: 22px;
    }}
    .header h1 {{
      font-size: 34px;
      font-weight: 800;
      letter-spacing: -0.03em;
      margin: 0 0 10px 0;
      background: linear-gradient(135deg, #ffffff 35%, #34d399 70%, #93c5fd 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .header p {{
      color: var(--text-muted);
      font-size: 15px;
      margin: 0 auto;
      max-width: 780px;
      line-height: 1.5;
    }}
    .tunnel-bar {{
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 8px;
      padding: 10px 16px;
      margin-bottom: 20px;
      font-size: 13px;
      text-align: center;
      color: #cbd5e1;
      overflow-wrap: anywhere;
    }}

    /* ==========================================================================
       FILTER NAVIGATION BAR & LIVE SEARCH
       ========================================================================== */
    .filter-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }}
    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      background: #0f172a;
      padding: 5px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
    }}
    .filter-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 600;
      padding: 8px 16px;
      border-radius: 7px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: inherit;
    }}
    .filter-btn:hover {{
      color: #f8fafc;
      background: rgba(255, 255, 255, 0.05);
    }}
    .filter-btn.active {{
      background: #1e293b;
      color: #ffffff;
      border-color: rgba(255, 255, 255, 0.15);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    .filter-btn.active[data-filter="pre"] {{
      border-color: rgba(59, 130, 246, 0.6);
      color: #93c5fd;
      background: rgba(59, 130, 246, 0.16);
    }}
    .filter-btn.active[data-filter="post"] {{
      border-color: rgba(16, 185, 129, 0.6);
      color: #34d399;
      background: rgba(16, 185, 129, 0.16);
    }}
    .filter-count {{
      background: rgba(255, 255, 255, 0.08);
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
    }}
    .filter-btn.active .filter-count {{
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }}
    .dot-pre, .dot-post {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      display: inline-block;
    }}
    .dot-pre {{
      background-color: var(--accent-blue);
      box-shadow: 0 0 8px var(--accent-blue-glow);
    }}
    .dot-post {{
      background-color: var(--bull-green);
      box-shadow: 0 0 8px var(--bull-green-glow);
    }}
    .search-box {{
      display: flex;
      align-items: center;
      gap: 10px;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 8px 16px;
      flex-grow: 1;
      max-width: 320px;
      transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .search-box:focus-within {{
      border-color: var(--accent-blue);
      box-shadow: 0 0 12px var(--accent-blue-glow);
    }}
    .search-box svg {{
      color: var(--text-muted);
      flex-shrink: 0;
    }}
    .search-box input {{
      background: transparent;
      border: none;
      color: #f8fafc;
      font-size: 13px;
      font-family: inherit;
      width: 100%;
      outline: none;
    }}
    .search-box input::placeholder {{
      color: #64748b;
    }}

    /* SUMMARY BAR */
    .summary-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #0f172a;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 20px;
      margin-bottom: 24px;
      font-size: 13px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .summary-stat {{
      color: var(--text-muted);
    }}
    .summary-stat strong {{
      color: #60a5fa;
      font-family: 'JetBrains Mono', monospace;
    }}

    /* REPORT GRID */
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(340px, 100%), 1fr));
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
    .report-card[data-category="post"]:hover {{
      border-color: rgba(16, 185, 129, 0.45);
      box-shadow: 0 12px 24px -6px rgba(16, 185, 129, 0.25);
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
    .report-card[data-category="post"] .ticker-symbol {{
      color: #34d399;
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
      font-size: 10px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .stat-val {{
      font-size: 13px;
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
    .report-card[data-category="post"] .btn-view:hover {{
      background: #059669;
      border-color: #10b981;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }}

    /* EMPTY STATE */
    #empty-state {{
      display: none;
      grid-column: 1 / -1;
      text-align: center;
      padding: 50px 20px;
      background: var(--card-bg);
      border: 1px dashed var(--card-border);
      border-radius: 14px;
      color: var(--text-muted);
    }}
    #empty-state h3 {{
      color: #f1f5f9;
      font-size: 18px;
      margin-bottom: 8px;
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

    @media (min-width: 641px) and (max-width: 1300px) {{
      /* the sticky nav wraps to 2-3 rows at these widths */
      [id^="section-"] {{
        scroll-margin-top: 148px;
      }}
    }}
    @media (max-width: 640px) {{
      .top-platform-nav {{
        position: static;
      }}
      .tp-links {{
        flex-wrap: nowrap;
        overflow-x: auto;
        width: 100%;
        min-width: 0;
        padding-bottom: 4px;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
      }}
      .tp-link {{
        flex: 0 0 auto;
        white-space: nowrap;
      }}
      [id^="section-"] {{
        scroll-margin-top: 16px;
      }}
      .search-box {{
        max-width: none;
      }}
    }}
    {portal_css}
    {market_strip_css}
  </style>
</head>
<body>
  <div class="dashboard-container">
    {market_strip_html}
    <nav class="top-platform-nav" aria-label="Dashboard Section Navigation">
      <div class="tp-brand">
        <span class="tp-badge">ANTIGRAVITY 2.0</span>
        <span>Institutional Earnings &amp; AI Discover Portal</span>
      </div>
      <div class="tp-links">
        <a href="#section-market-news" class="tp-link tp-highlight">⚡ 1. Market Impact News</a>
        <a href="#section-portfolio-news" class="tp-link tp-highlight">🎯 2. My Portfolio News (tickers.txt)</a>
        <a href="#section-tearsheet-library" class="tp-link">📊 3. All Tearsheets ({total_count})</a>
        <a href="news.html" class="tp-link">↗ Standalone Discover View</a>
      </div>
    </nav>

    <header class="header">
      <h1>Institutional Earnings &amp; AI Discover Portal</h1>
      <p>Perplexity Discover-Style Market &amp; Portfolio Briefings + T-1 Pre-Earnings &amp; T+0 Post-Earnings Forensic Accounting Tearsheets</p>
    </header>

    {tunnel_link_html}

    <main>
      {portal_html}

      <!-- SECTION 3: FULL TEARSHEET LIBRARY -->
      <div class="discover-section-header" id="section-tearsheet-library" style="margin-top: 48px;">
        <div>
          <div class="sec-eyebrow">🗂️ COMPLETE FORENSIC TEARSHEET ARCHIVE</div>
          <h2 class="sec-title">3. Institutional Tearsheet Library (T-1 Pre &amp; T+0 Post)</h2>
          <p class="sec-subtitle">Filter between all published Pre-Earnings and Post-Earnings HTML reports. Hover any ticker symbol for its instant Post-Earnings Pop-Up Summary.</p>
        </div>
      </div>

      <!-- INTERACTIVE FILTER & SEARCH TOOLBAR -->
      <search class="filter-bar">
        <div class="filter-tabs">
          <button type="button" class="filter-btn active" data-filter="all" id="filter-btn-all">
            All Reports <span class="filter-count" id="count-all">{total_count}</span>
          </button>
          <button type="button" class="filter-btn" data-filter="pre" id="filter-btn-pre">
            <span class="dot-pre" aria-hidden="true"></span> T-1 Pre-Earnings <span class="filter-count" id="count-pre">{pre_count}</span>
          </button>
          <button type="button" class="filter-btn" data-filter="post" id="filter-btn-post">
            <span class="dot-post" aria-hidden="true"></span> T+0 Post-Earnings <span class="filter-count" id="count-post">{post_count}</span>
          </button>
        </div>

        <div class="search-box">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input type="search" id="tickerSearch" aria-label="Filter tearsheets by ticker or company name" placeholder="Filter tearsheets by ticker or name..." />
        </div>
      </search>

      <!-- LIVE SUMMARY METRICS -->
      <div class="summary-bar">
        <div class="summary-stat">Showing: <strong id="visible-count">{total_count}</strong> of <strong>{total_count}</strong> Tearsheets</div>
        <div class="summary-stat">Pre-Earnings (T-1): <strong style="color: #60a5fa;">{pre_count}</strong> &bull; Post-Earnings (T+0): <strong style="color: #34d399;">{post_count}</strong></div>
        <div class="summary-stat">Updated: <strong>{last_updated_str}</strong></div>
      </div>

      <!-- REPORT CARD GRID -->
      <div class="grid" id="reportsGrid">
        {cards_html}
        <div id="empty-state">
          <h3>No Matching Tearsheets Found</h3>
          <p>No reports match the current filter selection. Try clearing the search or switching filters.</p>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div>Antigravity 2.0 Autonomous Financial Research Harness • Deterministic SEC Edgar Ground Truth</div>
    </footer>
  </div>

  <!-- INTERACTIVE FILTERING SCRIPT -->
  <script>
    const FILTER_VALUES = ['all', 'pre', 'post'];
    let currentFilter = 'all';
    let searchQuery = '';

    function applyFilters() {{
      const cards = document.querySelectorAll('.report-card');
      let visible = 0;
      cards.forEach(card => {{
        const cat = card.getAttribute('data-category');
        const ticker = (card.getAttribute('data-ticker') || '').toLowerCase();
        const company = (card.getAttribute('data-company') || '').toLowerCase();

        const matchesCat = (currentFilter === 'all') || (cat === currentFilter);
        const matchesSearch = !searchQuery || ticker.includes(searchQuery) || company.includes(searchQuery);

        if (matchesCat && matchesSearch) {{
          card.style.display = 'flex';
          visible++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      const visCountEl = document.getElementById('visible-count');
      if (visCountEl) visCountEl.textContent = visible;

      const emptyState = document.getElementById('empty-state');
      if (emptyState) {{
        emptyState.style.display = (visible === 0) ? 'block' : 'none';
      }}
    }}

    function setFilter(filterType) {{
      currentFilter = filterType;
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        if (btn.getAttribute('data-filter') === filterType) {{
          btn.classList.add('active');
        }} else {{
          btn.classList.remove('active');
        }}
      }});

      syncFilterUrl(filterType);
      applyFilters();
    }}

    // Shareable ?filter=pre|post state; legacy #pre/#post/#all hashes are migrated so section anchors keep working.
    function syncFilterUrl(filterType) {{
      if (!(window.history && window.history.replaceState)) return;
      try {{
        const url = new URL(window.location.href);
        if (filterType === 'all') {{
          url.searchParams.delete('filter');
        }} else {{
          url.searchParams.set('filter', filterType);
        }}
        if (FILTER_VALUES.includes(url.hash.replace('#', '').toLowerCase())) url.hash = '';
        window.history.replaceState(null, '', url.toString());
      }} catch (e) {{}}
    }}

    function scrollToLibrary() {{
      const lib = document.getElementById('section-tearsheet-library');
      if (lib) lib.scrollIntoView({{ block: 'start' }});
    }}

    function handleSearch(val) {{
      searchQuery = (val || '').trim().toLowerCase();
      applyFilters();
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', () => setFilter(btn.getAttribute('data-filter') || 'all'));
      }});
      const searchEl = document.getElementById('tickerSearch');
      if (searchEl) {{
        searchEl.addEventListener('input', (e) => handleSearch(e.target.value));
      }}
      const hash = (window.location.hash || '').replace('#', '').toLowerCase();
      const hashFilter = FILTER_VALUES.includes(hash) ? hash : '';
      const queryFilter = (new URLSearchParams(window.location.search).get('filter') || '').toLowerCase();
      const initialFilter = FILTER_VALUES.includes(queryFilter) ? queryFilter : hashFilter;
      if (initialFilter) {{
        setFilter(initialFilter);
        // The library sits below the portal; jump to it unless the URL targets another section anchor.
        if (!hash || hashFilter) {{
          requestAnimationFrame(scrollToLibrary);
          window.addEventListener('load', scrollToLibrary, {{ once: true }});
        }}
      }} else {{
        applyFilters();
      }}
    }});
  </script>
  {portal_js}
  {market_strip_js}
</body>
</html>
"""


def update_index_html():
    REPORTS_DIR.mkdir(exist_ok=True)
    local_base, public_base = get_base_urls()

    # One market snapshot per build, shared by news.html and both index pages
    snapshot = portal_call("get_market_snapshot_safe", default=None)

    # Also build standalone news.html and published_reports/news.html (returns True on success)
    news_ok = portal_call("generate_news_portal_files", snapshot=snapshot, default=False)

    all_html_files = [f for f in REPORTS_DIR.glob("*.html") if f.name not in ("index.html", "news.html")]
    grouped = {}

    for f in all_html_files:
        # Match T-1 reports
        m_t1 = re.match(r"^([A-Z0-9.\-]+)_T1_(\d{4}-\d{2}-\d{2})(?:_v(\d+))?\.html$", f.name)
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
        m_t0 = re.match(r"^([A-Z0-9.\-]+)_T0_POST_(\d{4}-\d{2}-\d{2})(?:_v(\d+))?\.html$", f.name)
        if m_t0:
            ticker, e_date, ver = m_t0.group(1), m_t0.group(2), m_t0.group(3)
            if signoff_rejected(ticker, e_date):
                continue  # Agent 5 did not approve this T+0 tearsheet: no card, not counted
            key = f"{ticker}_{e_date}_T0_POST"
            if key not in grouped:
                grouped[key] = {"ticker": ticker, "earnings_date": e_date, "is_post": True, "canonical": None, "versions": {}}
            if ver:
                grouped[key]["versions"][int(ver)] = f
            else:
                grouped[key]["canonical"] = f

    # Sync SQLite System-of-Record (earnings_warehouse.db) & export static manifests (history_catalog.js + warehouse_summary.json)
    try:
        import earnings_db
        earnings_db.backfill_all()
        history_catalog = earnings_db.export_static_manifests()
    except Exception as db_err:
        print(f"  [WARN] Falling back to file-scan history_catalog builder ({db_err})")
        catalog_by_tk_date: dict[str, dict[str, dict]] = {}
        for item in grouped.values():
            tk = item["ticker"]
            dt = item["earnings_date"]
            ver_nums = sorted(item["versions"].keys())
            best_file = item["canonical"] or (item["versions"][ver_nums[-1]] if ver_nums else None)
            if not best_file:
                continue
            slot = catalog_by_tk_date.setdefault(tk, {}).setdefault(
                dt,
                {
                    "date": dt,
                    "quarter": resolve_quarter_label(tk, dt),
                    "date_display": format_short_date(dt),
                    "t1": None,
                    "t0": None,
                },
            )
            if item["is_post"]:
                slot["t0"] = best_file.name
            else:
                slot["t1"] = best_file.name

        history_catalog = {
            tk: [ by_dt[dt] for dt in sorted(by_dt.keys(), reverse=True) ]
            for tk, by_dt in sorted(catalog_by_tk_date.items())
        }
        catalog_js = (
            "// Auto-generated Historical Quarter Archive Catalog for In-Page Tearsheet Dropdowns\n"
            f"window.EARNINGS_HISTORY_CATALOG = {json.dumps(history_catalog, indent=2)};\n"
        )
        (REPORTS_DIR / "history_catalog.js").write_text(catalog_js, encoding="utf-8")

    # Deduplicate dashboard tiles: ONLY show the single latest quarter/version per (ticker, stage)
    latest_by_tk_stage: dict[tuple[str, bool], str] = {}
    for k, item in grouped.items():
        pair = (item["ticker"], item["is_post"])
        prev_k = latest_by_tk_stage.get(pair)
        if prev_k is None or item["earnings_date"] > grouped[prev_k]["earnings_date"]:
            latest_by_tk_stage[pair] = k

    latest_grouped = {k: grouped[k] for k in latest_by_tk_stage.values()}
    total_count = len(latest_grouped)

    # 1. Generate for published_reports/index.html
    cards_for_reports = build_cards_html(latest_grouped, link_prefix="")
    html_for_reports = build_full_page(cards_for_reports, latest_grouped, public_base, link_prefix="", snapshot=snapshot)
    (REPORTS_DIR / "index.html").write_text(html_for_reports, encoding="utf-8")

    # 2. Generate for root index.html
    cards_for_root = build_cards_html(latest_grouped, link_prefix="published_reports/")
    html_for_root = build_full_page(cards_for_root, latest_grouped, public_base, link_prefix="published_reports/", snapshot=snapshot)
    (BASE_DIR / "index.html").write_text(html_for_root, encoding="utf-8")

    pre_count = sum(1 for item in latest_grouped.values() if not item["is_post"])
    post_count = sum(1 for item in latest_grouped.values() if item["is_post"])
    totals = f"{total_count} total ({pre_count} Pre-Earnings, {post_count} Post-Earnings)"
    if news_ok is False:
        print(f"index.html updated; news.html NOT regenerated (see warning above): {totals}.")
    else:
        print(f"Successfully updated index.html and news.html: {totals}.")


if __name__ == "__main__":
    update_index_html()
