"""
Daily Automated Earnings Harness Runner with Multi-Company Staggering
Schedules execution every weekday at 6:00 AM.
If multiple companies report on the same day, staggers execution sequentially
with a configurable delay to prevent API throttling and ensure clean versioning.
"""

import sys
import json
import time
import subprocess
from datetime import datetime, date
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
LEDGER_PATH = BASE_DIR / "published_ledger.json"
AUDIT_DIR = BASE_DIR / "audit_logs"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

DEFAULT_STAGGER_DELAY_SECONDS = 60  # Pacing delay between multiple companies

def log_msg(msg: str, log_file: Path = None):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

def run_command(cmd: list[str], cwd: Path = BASE_DIR) -> tuple[int, str, str]:
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            timeout=300
        )
        return res.returncode, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 300s"
    except Exception as e:
        return -1, "", str(e)

def run_git_sync(ticker: str, earnings_date: str, log_file: Path):
    log_msg(f"Initiating GitHub Pages sync for {ticker} ({earnings_date})...", log_file)
    run_command(["git", "add", "index.html", "published_reports", "published_ledger.json", "audit_logs", "ground_truth", "drafts"])
    code, stdout, stderr = run_command(["git", "commit", "-m", f"publish: auto-publish {ticker} ({earnings_date}) tearsheet"])
    if code == 0:
        log_msg("Git commit created successfully.", log_file)
        p_code, p_out, p_err = run_command(["git", "push", "origin", "main"])
        if p_code == 0:
            log_msg("Successfully pushed to GitHub repository (GitHub Pages updating).", log_file)
        else:
            log_msg(f"Git push warning: {p_err.strip() or p_out.strip()}", log_file)
    else:
        log_msg(f"Git commit info (clean working tree or no changes): {stdout.strip() or stderr.strip()}", log_file)

def run_daily_workflow(stagger_delay: int = DEFAULT_STAGGER_DELAY_SECONDS):
    today_str = date.today().isoformat()
    log_file = LOGS_DIR / f"daily_run_{today_str}.log"
    log_msg("=" * 75, log_file)
    log_msg(f"STARTING T-1 MORNING EARNINGS HARNESS RUN — {today_str}", log_file)
    log_msg("=" * 75, log_file)

    # 1. Execute Stage 1 scan across tickers.txt to detect T-1 candidates
    log_msg("Running Stage 1 batch scan across tickers.txt...", log_file)
    code, stdout, stderr = run_command([sys.executable, "stage1_fetch_truth.py"])
    
    matches = []
    for line in stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and "t1_matches" in line:
            try:
                data = json.loads(line)
                matches = data.get("t1_matches", [])
            except Exception:
                pass

    if not matches:
        log_msg("No upcoming earnings found in the T-1 window for today. Execution complete.", log_file)
        return

    # Group by earnings date to check for same-day multiple companies
    by_date: dict[str, list[dict]] = {}
    for m in matches:
        e_date = m.get("earnings_date")
        by_date.setdefault(e_date, []).append(m)

    log_msg(f"Found {len(matches)} total candidate(s) in T-1 window across {len(by_date)} reporting date(s).", log_file)

    # Flatten and prioritize companies
    # Stagger logic: Sort by date, then sort by company ticker
    all_targets = []
    for e_date, items in sorted(by_date.items()):
        if len(items) > 1:
            tickers_list = ", ".join([x["ticker"] for x in items])
            log_msg(f"⚠️ MULTI-COMPANY ALERT: {len(items)} companies reporting on {e_date} [{tickers_list}].", log_file)
            log_msg(f"   Staggering execution with {stagger_delay}s cooldown between reports to avoid rate-limiting.", log_file)
        for itm in sorted(items, key=lambda x: x["ticker"]):
            all_targets.append(itm)

    ledger = {}
    if LEDGER_PATH.exists():
        try:
            ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    published_keys = set(ledger.get("published", []))

    processed_count = 0
    for idx, target in enumerate(all_targets, 1):
        ticker = target["ticker"].upper()
        earnings_date = target["earnings_date"]
        key = f"{ticker}_{earnings_date}"

        log_msg("-" * 65, log_file)
        log_msg(f"[{idx}/{len(all_targets)}] Processing target: {ticker} (Earnings Date: {earnings_date})", log_file)

        # 1. Ensure ground truth is freshly anchored
        log_msg(f"[{ticker}] Running Stage 1 anchor...", log_file)
        s1_code, s1_out, s1_err = run_command([sys.executable, "stage1_fetch_truth.py", ticker, "--force"])
        if s1_code != 0:
            log_msg(f"[{ticker}] Error during Stage 1: {s1_err.strip()}", log_file)
            continue

        # 2. Check draft existence
        draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"
        if not draft_path.exists():
            log_msg(f"[{ticker}] Notice: Draft {draft_path.name} not found. Needs Stage 2 synthesis.", log_file)
            # If draft builder exists in dedicated folder {TICKER}/, run it
            builder_script = BASE_DIR / ticker / f"build_{ticker.lower()}_draft.py"
            if builder_script.exists():
                log_msg(f"[{ticker}] Found automated draft builder at {builder_script.name}, running...", log_file)
                b_code, b_out, b_err = run_command([sys.executable, str(builder_script)])
                if b_code != 0:
                    log_msg(f"[{ticker}] Draft builder error: {b_err.strip()}", log_file)
                    continue

        if not draft_path.exists():
            log_msg(f"[{ticker}] Skipping validation: Draft file does not exist yet.", log_file)
            continue

        # 3. Stage 3 Deterministic Validation
        log_msg(f"[{ticker}] Running Stage 3 validation loop...", log_file)
        s3_code, s3_out, s3_err = run_command([sys.executable, "stage3_validate_draft.py", ticker, earnings_date])
        if s3_code != 0:
            log_msg(f"[{ticker}] Stage 3 validation failed. Details: {s3_err.strip() or s3_out.strip()}", log_file)
            continue

        # 4. Stage 4 Publishing & Index Updating
        log_msg(f"[{ticker}] Stage 3 passed! Running Stage 4 HTML rendering and multi-version publishing...", log_file)
        s4_code, s4_out, s4_err = run_command([sys.executable, "stage4_render_html.py", ticker, earnings_date])
        if s4_code == 0:
            log_msg(f"[{ticker}] Successfully rendered and published tearsheet.", log_file)
            run_git_sync(ticker, earnings_date, log_file)
            processed_count += 1
        else:
            log_msg(f"[{ticker}] Stage 4 publishing error: {s4_err.strip()}", log_file)

        # STAGGER LOGIC: If more companies remain, pause execution
        if idx < len(all_targets):
            log_msg(f"Pacing: Staggering next report generation by {stagger_delay} seconds...", log_file)
            time.sleep(stagger_delay)

    log_msg("=" * 75, log_file)
    log_msg(f"DAILY HARNESS RUN COMPLETED. Processed {processed_count}/{len(all_targets)} reports.", log_file)
    log_msg("=" * 75, log_file)

if __name__ == "__main__":
    delay = DEFAULT_STAGGER_DELAY_SECONDS
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        delay = int(sys.argv[1])
    run_daily_workflow(stagger_delay=delay)
