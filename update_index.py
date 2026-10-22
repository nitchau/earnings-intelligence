"""
Enhanced Dashboard Generator for Institutional Earnings Intelligence
Discovers and displays both:
- T-1 Pre-Earnings Briefings ({TICKER}_T1_{DATE}.html)
- T+0 Post-Earnings Forensic Tearsheets ({TICKER}_T0_POST_{DATE}.html)
Features interactive Pre vs. Post filtering and real-time ticker search.
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
        
    m_price = re.search(r'<div class="price-value">\$([0-9,.]+)', content)
    if m_price:
        meta["spot_price"] = f"${m_price.group(1)}"
        
    m_move = re.search(r'Options-Implied Move[^<]*</span>\s*<span class="strip-val"[^>]*>([^<]+)</span>', content)
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
        category_val = "post" if is_post else "pre"
        
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
        price_label = "After-Hours Price" if is_post else "Spot Price"

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
        <div class="report-card" data-category="{category_val}" data-ticker="{ticker.lower()}" data-company="{company_name.lower()}">
          <div class="card-top">
            <div class="ticker-box">
              <span class="ticker-symbol">{ticker}</span>
              <span class="version-tag">{latest_ver_label}</span>
            </div>
            <span class="badge-status" style="{badge_style}">{status_label}</span>
          </div>

          <div class="company-title">{company_name}</div>
          <div class="sector-line">{sector} • {e_date_display}</div>

          <div class="stats-row">
            <div class="stat-item">
              <span class="stat-label">{price_label}</span>
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

    return "\n".join(cards_html)

def build_full_page(cards_html: str, grouped: dict, public_base: str) -> str:
    total_count = len(grouped)
    pre_count = sum(1 for item in grouped.values() if not item["is_post"])
    post_count = sum(1 for item in grouped.values() if item["is_post"])

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
      --accent-blue-glow: rgba(59, 130, 246, 0.25);
      --bull-green: #10b981;
      --bull-green-glow: rgba(16, 185, 129, 0.25);
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
      margin-bottom: 24px;
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
    .tunnel-bar {{
      background: rgba(59, 130, 246, 0.1);
      border: 1px solid rgba(59, 130, 246, 0.25);
      border-radius: 8px;
      padding: 10px 16px;
      margin-bottom: 20px;
      font-size: 13px;
      text-align: center;
      color: #cbd5e1;
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
  </style>
</head>
<body>
  <div class="dashboard-container">
    <header class="header">
      <h1>Institutional Earnings Intelligence Dashboard</h1>
      <p>Multi-Agent Autonomous Research Mesh: T-1 Pre-Earnings Briefings &amp; T+0 Post-Earnings Forensic Accounting Tearsheets</p>
    </header>

    {tunnel_link_html}

    <!-- INTERACTIVE FILTER & SEARCH TOOLBAR -->
    <div class="filter-bar">
      <div class="filter-tabs">
        <button class="filter-btn active" data-filter="all" onclick="setFilter('all')">
          All Reports <span class="filter-count" id="count-all">{total_count}</span>
        </button>
        <button class="filter-btn" data-filter="pre" onclick="setFilter('pre')">
          <span class="dot-pre"></span> T-1 Pre-Earnings <span class="filter-count" id="count-pre">{pre_count}</span>
        </button>
        <button class="filter-btn" data-filter="post" onclick="setFilter('post')">
          <span class="dot-post"></span> T+0 Post-Earnings <span class="filter-count" id="count-post">{post_count}</span>
        </button>
      </div>

      <div class="search-box">
        <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input type="text" id="tickerSearch" placeholder="Filter by ticker or name..." oninput="handleSearch(this.value)" />
      </div>
    </div>

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

    <footer class="footer">
      <div>Antigravity 2.0 Autonomous Financial Research Harness • Deterministic SEC Edgar Ground Truth</div>
    </footer>
  </div>

  <!-- INTERACTIVE FILTERING SCRIPT -->
  <script>
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

      if (window.history && window.history.replaceState) {{
        const newHash = filterType === 'all' ? '' : '#' + filterType;
        window.history.replaceState(null, null, window.location.pathname + window.location.search + newHash);
      }}
      applyFilters();
    }}

    function handleSearch(val) {{
      searchQuery = (val || '').trim().toLowerCase();
      applyFilters();
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      const hash = (window.location.hash || '').replace('#', '').toLowerCase();
      if (hash === 'pre' || hash === 'post' || hash === 'all') {{
        setFilter(hash);
      }} else {{
        applyFilters();
      }}
    }});
  </script>
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
    html_for_reports = build_full_page(cards_for_reports, grouped, public_base)
    (REPORTS_DIR / "index.html").write_text(html_for_reports, encoding="utf-8")

    # 2. Generate for root index.html
    cards_for_root = build_cards_html(grouped, link_prefix="published_reports/")
    html_for_root = build_full_page(cards_for_root, grouped, public_base)
    (BASE_DIR / "index.html").write_text(html_for_root, encoding="utf-8")

    pre_count = sum(1 for item in grouped.values() if not item["is_post"])
    post_count = sum(1 for item in grouped.values() if item["is_post"])
    print(f"Successfully updated index.html: {total_count} total ({pre_count} Pre-Earnings, {post_count} Post-Earnings).")

if __name__ == "__main__":
    update_index_html()
