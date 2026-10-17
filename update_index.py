import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
LEDGER_PATH = BASE_DIR / "published_ledger.json"
TUNNEL_FILE = BASE_DIR / "tunnel_url.json"

def get_base_urls():
    local_base = "http://localhost:8080"
    public_base = "https://nitchau.github.io/earnings-intelligence"
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
    meta = {
        "title": html_path.stem,
        "company_name": "",
        "ticker": "",
        "earnings_date": "",
        "spot_price": "",
        "implied_move": "",
        "sector": "",
        "status_badge": "PRE-EARNINGS BRIEFING"
    }
    
    # Extract ticker
    m = re.search(r'<span class="ticker-symbol">([A-Z0-9]+)</span>', content)
    if m:
        meta["ticker"] = m.group(1)
        
    # Extract company name
    m = re.search(r'<h1 class="company-name">([^<]+)</h1>', content)
    if m:
        meta["company_name"] = m.group(1).strip()
        
    # Extract sector tag
    m = re.search(r'<div class="sector-tag">([^<]+)', content)
    if m:
        meta["sector"] = m.group(1).split("•")[0].strip()
        
    # Extract spot price
    m = re.search(r'<div class="price-value">\$([0-9,.]+)', content)
    if m:
        meta["spot_price"] = f"${m.group(1)}"
        
    # Extract implied move
    m = re.search(r'Options-Implied Move[^<]*</span>\s*<span class="strip-val"[^>]*>([^<]+)</span>', content)
    if m:
        meta["implied_move"] = m.group(1).replace("±", "&plusmn;").strip()
        
    # Extract release date
    m = re.search(r'Upcoming[^<]*Release Date</span>\s*<span class="strip-val">([^<]+)', content)
    if not m:
        m = re.search(r'Official Earnings Release Date</span>\s*<span class="strip-val">([^<]+)', content)
    if m:
        meta["earnings_date"] = m.group(1).strip()
        
    return meta

def build_cards_html(grouped: dict, link_prefix: str) -> str:
    cards_html = []
    sorted_keys = sorted(
        grouped.keys(),
        key=lambda k: (grouped[k]["earnings_date"], grouped[k]["ticker"]),
        reverse=True
    )
    
    for key in sorted_keys:
        item = grouped[key]
        ticker = item["ticker"]
        e_date = item["earnings_date"]
        
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
        
        # Build version comparison pills
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
            <span class="badge-status">{e_date_display}</span>
          </div>

          <div class="company-title">{company_name}</div>
          <div class="sector-line">{sector}</div>

          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-label">Spot Price</span>
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
            <span class="version-label">Version History:</span>
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

    return "\n".join(cards_html)

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
  <title>Institutional T-1 Pre-Earnings Intelligence Dashboard</title>
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
      max-width: 1100px;
      width: 100%;
    }}
    .header {{
      text-align: center;
      margin-bottom: 28px;
    }}
    .header h1 {{
      font-size: 32px;
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
      max-width: 680px;
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
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
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
      font-weight: 600;
      color: #4ade80;
      background: rgba(34, 197, 94, 0.12);
      border: 1px solid rgba(34, 197, 94, 0.25);
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
      <h1>Institutional T-1 Earnings Tearsheets</h1>
      <p>Deterministic Zero-Hallucination SEC Form 10-Q / 10-K Forensic Accounting Research, Segment Disclosures &amp; PM Options Playbooks</p>
    </header>

    {tunnel_link_html}

    <div class="summary-bar">
      <div class="summary-stat">Active Tearsheets: <strong>{total_count}</strong></div>
      <div class="summary-stat">Multi-Version Tracking: <strong>Enabled</strong></div>
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
    
    # Scan all HTML files in published_reports
    all_html_files = [f for f in REPORTS_DIR.glob("*.html") if f.name != "index.html"]
    
    # Group files by key (TICKER_DATE)
    grouped = {}
    for f in all_html_files:
        m = re.match(r"^([A-Z0-9]+)_T1_(\d{4}-\d{2}-\d{2})(?:_v(\d+))?\.html$", f.name)
        if m:
            ticker, e_date, ver = m.group(1), m.group(2), m.group(3)
            key = f"{ticker}_{e_date}"
            if key not in grouped:
                grouped[key] = {
                    "ticker": ticker,
                    "earnings_date": e_date,
                    "canonical": None,
                    "versions": {}
                }
            if ver:
                grouped[key]["versions"][int(ver)] = f
            else:
                grouped[key]["canonical"] = f

    total_count = len(grouped)

    # 1. Generate for published_reports/index.html (where files are in the SAME directory -> prefix="")
    cards_for_reports = build_cards_html(grouped, link_prefix="")
    html_for_reports = build_full_page(cards_for_reports, total_count, public_base)
    (REPORTS_DIR / "index.html").write_text(html_for_reports, encoding="utf-8")

    # 2. Generate for root index.html (where files are in published_reports/ -> prefix="published_reports/")
    cards_for_root = build_cards_html(grouped, link_prefix="published_reports/")
    html_for_root = build_full_page(cards_for_root, total_count, public_base)
    (BASE_DIR / "index.html").write_text(html_for_root, encoding="utf-8")

    print(f"Successfully updated index.html (published_reports/ uses relative links, root uses published_reports/ links).")

if __name__ == "__main__":
    update_index_html()
