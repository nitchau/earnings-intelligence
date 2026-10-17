import sys
import re
import json
from datetime import datetime
from pathlib import Path
from update_index import update_index_html

BASE_DIR = Path(__file__).parent.resolve()
REPORTS_DIR = BASE_DIR / "published_reports"
MASTER_HTML = BASE_DIR / "Stock_Analysis_v2.html"
LEDGER_PATH = BASE_DIR / "published_ledger.json"
TUNNEL_FILE = BASE_DIR / "tunnel_url.json"

def get_base_tunnel() -> str:
    if TUNNEL_FILE.exists():
        try:
            t_data = json.loads(TUNNEL_FILE.read_text(encoding="utf-8"))
            return t_data.get("tunnel_url", "").rstrip("/")
        except Exception:
            pass
    return ""

GITHUB_PAGES_BASE = "https://nitchau.github.io/earnings-intelligence"

def get_browser_links(filename: str) -> dict:
    links = {
        "local_browser_url": f"http://localhost:8080/published_reports/{filename}",
        "github_pages_url": f"{GITHUB_PAGES_BASE}/published_reports/{filename}"
    }
    base_tunnel = get_base_tunnel()
    if base_tunnel:
        links["public_sharable_url"] = f"{base_tunnel}/published_reports/{filename}"
    else:
        links["public_sharable_url"] = links["github_pages_url"]
    return links

def determine_version(ticker: str, earnings_date: str) -> tuple[int, list[int]]:
    REPORTS_DIR.mkdir(exist_ok=True)
    existing_versions = []
    
    # Check for existing versioned files: {ticker}_T1_{earnings_date}_v{N}.html
    for f in REPORTS_DIR.glob(f"{ticker}_T1_{earnings_date}_v*.html"):
        m = re.search(r"_v(\d+)\.html$", f.name)
        if m:
            existing_versions.append(int(m.group(1)))
            
    canonical_file = REPORTS_DIR / f"{ticker}_T1_{earnings_date}.html"
    
    # If canonical exists but no versioned file exists, preserve canonical as v1
    if canonical_file.exists() and not existing_versions:
        v1_path = REPORTS_DIR / f"{ticker}_T1_{earnings_date}_v1.html"
        v1_path.write_bytes(canonical_file.read_bytes())
        existing_versions = [1]
        
    existing_versions.sort()
    next_ver = (existing_versions[-1] + 1) if existing_versions else 1
    return next_ver, existing_versions

def publish_report(ticker: str, earnings_date: str):
    ticker = ticker.upper()
    audit_file = BASE_DIR / "audit_logs" / f"{ticker}_{earnings_date}_validation.json"
    if not audit_file.exists():
        raise RuntimeError("Cannot publish: Stage 3 validation log does not exist.")
    audit = json.loads(audit_file.read_text(encoding="utf-8"))
    if not audit.get("passed"):
        raise RuntimeError(f"Cannot publish: Stage 3 failed with errors: {audit.get('errors')}")

    master_content = MASTER_HTML.read_text(encoding="utf-8")
    style_start = master_content.find("<style>")
    style_end = master_content.find("</style>") + len("</style>")
    locked_css = master_content[style_start:style_end]

    draft_file = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"
    draft = json.loads(draft_file.read_text(encoding="utf-8"))

    # Determine version
    version_num, prior_versions = determine_version(ticker, earnings_date)
    ver_str = f"v{version_num}"
    timestamp_display = datetime.now().strftime("%b %d, %Y at %I:%M %p")
    iso_timestamp = datetime.now().isoformat()

    # Build comparison banner if prior versions exist
    version_banner_html = ""
    if prior_versions:
        pills = []
        for pv in prior_versions:
            pv_file = f"{ticker}_T1_{earnings_date}_v{pv}.html"
            pills.append(f'<a href="{pv_file}" style="background: rgba(255,255,255,0.08); color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-size: 11.5px; text-decoration: none; font-family: monospace; border: 1px solid rgba(255,255,255,0.15);">v{pv}</a>')
        pills_str = " ".join(pills)
        version_banner_html = f"""
    <!-- VERSION COMPARISON BANNER -->
    <div style="background: #0f172a; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 10px; padding: 10px 18px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
      <div style="display:flex; align-items:center; gap: 8px;">
        <span style="background: rgba(59, 130, 246, 0.2); color: #60a5fa; font-weight: 800; font-family: monospace; padding: 3px 8px; border-radius: 5px; border: 1px solid rgba(59, 130, 246, 0.3);">{ver_str} (Active)</span>
        <span style="color: #cbd5e1;">Generated on <strong>{timestamp_display}</strong></span>
      </div>
      <div style="display:flex; align-items:center; gap: 8px;">
        <span style="color: #94a3b8; font-size: 12px;">Compare prior iterations:</span>
        {pills_str}
      </div>
    </div>
        """

    # Inject version banner into rendered container HTML
    container_html = draft['rendered_container_html']
    # Insert right at the top of container
    container_html_with_ver = f"{version_banner_html}\n{container_html}"

    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[{ver_str}] {draft['header']['page_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  {locked_css}
</head>
<body>
  <div class="container">
    {container_html_with_ver}
  </div>
</body>
</html>"""

    # Save to both versioned file and canonical file
    versioned_filename = f"{ticker}_T1_{earnings_date}_{ver_str}.html"
    canonical_filename = f"{ticker}_T1_{earnings_date}.html"
    
    versioned_path = REPORTS_DIR / versioned_filename
    canonical_path = REPORTS_DIR / canonical_filename
    
    versioned_path.write_text(final_html, encoding="utf-8")
    canonical_path.write_text(final_html, encoding="utf-8")

    link_info_versioned = get_browser_links(versioned_filename)
    link_info_canonical = get_browser_links(canonical_filename)

    # Update ledger with full version tracking
    ledger = {}
    if LEDGER_PATH.exists():
        try:
            ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            ledger = {}

    key = f"{ticker}_{earnings_date}"
    if key not in ledger.get("published", []):
        ledger.setdefault("published", []).append(key)

    # Legacy links entry (points to latest)
    ledger.setdefault("links", {})[key] = link_info_canonical

    # Structured multi-version reports tracking
    reports_dict = ledger.setdefault("reports", {})
    entry = reports_dict.setdefault(key, {
        "ticker": ticker,
        "earnings_date": earnings_date,
        "latest_version": ver_str,
        "latest_file": canonical_filename,
        "versions": []
    })
    entry["latest_version"] = ver_str
    entry["latest_file"] = canonical_filename
    
    # Check if this version already recorded
    v_entry = {
        "version": ver_str,
        "filename": versioned_filename,
        "published_at": iso_timestamp,
        "published_display": timestamp_display,
        "local_browser_url": link_info_versioned.get("local_browser_url"),
        "public_sharable_url": link_info_versioned.get("public_sharable_url")
    }
    
    # Avoid duplicate version entries
    entry["versions"] = [v for v in entry.get("versions", []) if v.get("version") != ver_str]
    entry["versions"].append(v_entry)

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2), encoding="utf-8")

    # Automatically update index.html across root and published_reports
    update_index_html()

    base_tunnel = get_base_tunnel()
    print("=" * 70)
    print(f"SUCCESS: Published verified tearsheet [{ver_str}] for {ticker} ({earnings_date})")
    print(f"VERSION FILE:        {versioned_path}")
    print(f"CANONICAL (LATEST):  {canonical_path}")
    print(f"VERSION LOCAL LINK:  {link_info_versioned.get('local_browser_url')}")
    print(f"GITHUB PAGES URL:    {link_info_versioned.get('github_pages_url')}")
    if base_tunnel and 'public_sharable_url' in link_info_versioned:
        print(f"TUNNEL URL:          {link_info_versioned.get('public_sharable_url')}")
    print(f"INDEX DASHBOARD:     {GITHUB_PAGES_BASE}/")
    print("=" * 70)

if __name__ == "__main__":
    publish_report(sys.argv[1].upper(), sys.argv[2])
