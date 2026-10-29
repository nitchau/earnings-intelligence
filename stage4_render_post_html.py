"""
Stage 4 Post-Earnings (T+0) Read-Only CSS Cloner & Candidate HTML Assembler
- Clones locked CSS from published_reports/TSLA_T1_2026-10-21.html in read-only mode.
- Wraps rendered_container_html into published_reports/{TICKER}_T0_POST_{DATE}.html
- Injects Historical Quarter Archive Topbar (zero v1/v2 iteration clutter).
- Pre-publish size check: Enforces rendered HTML >= 75,000 bytes.
"""

import sys
import re
import json
from pathlib import Path
from archive_topbar import build_archive_topbar_html

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
    pattern = rf"^{ticker}_T0_POST_{earnings_date}_v(\d+)\.html$"
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
    version_num, _ = determine_post_version(ticker, earnings_date)

    archive_topbar_html = build_archive_topbar_html(ticker, earnings_date, is_post=True)
    container_html = draft["rendered_container_html"]
    container_with_topbar = f"{archive_topbar_html}\n{container_html}"

    page_title = draft.get("header", {}).get("page_title", f"{ticker} T+0 Post-Earnings Forensic Tearsheet")

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  {locked_css}
</head>
<body>
  <div class="container">
    {container_with_topbar}
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

    # Write versioned backup file and canonical file
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
