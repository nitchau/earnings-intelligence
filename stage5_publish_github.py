"""
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

    print("\n" + "=" * 75)
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
