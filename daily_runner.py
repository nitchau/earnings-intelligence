"""
Daily Automated Earnings Harness Runner (T-1 Pre-Earnings & T+0 Post-Earnings)
Supports:
  - python daily_runner.py           (runs both T-1 Pre-Earnings and T+0 Post-Earnings scans)
  - python daily_runner.py --pre     (runs only T-1 Pre-Earnings scan)
  - python daily_runner.py --post    (runs only T+0 Post-Earnings scan via run_post_harness.py)
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
    run_command(["git", "add", "index.html", *(["news.html"] if (BASE_DIR / "news.html").exists() else []), "published_reports","published_ledger.json", "audit_logs", "ground_truth", "drafts", "pre_agent_bus", "post_agent_bus"])
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

def run_t1_pre_workflow(today_str: str, log_file: Path, stagger_delay: int = DEFAULT_STAGGER_DELAY_SECONDS):
    log_msg("=" * 75, log_file)
    log_msg(f"STARTING T-1 PRE-EARNINGS 5-LAYER HARNESS SCAN — {today_str}", log_file)
    log_msg("=" * 75, log_file)

    log_msg("Running Stage 1 T-1 batch scan across tickers.txt...", log_file)
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
        log_msg("No upcoming earnings found in the T-1 window for today.", log_file)
        return 0

    by_date: dict[str, list[dict]] = {}
    for m in matches:
        e_date = m.get("earnings_date")
        by_date.setdefault(e_date, []).append(m)

    log_msg(f"Found {len(matches)} total candidate(s) in T-1 window across {len(by_date)} reporting date(s).", log_file)

    all_targets = []
    for e_date, items in sorted(by_date.items()):
        if len(items) > 1:
            tickers_list = ", ".join([x["ticker"] for x in items])
            log_msg(f"⚠️ MULTI-COMPANY ALERT: {len(items)} companies reporting on {e_date} [{tickers_list}].", log_file)
            log_msg(f"   Staggering execution with {stagger_delay}s cooldown between reports to avoid rate-limiting.", log_file)
        for itm in sorted(items, key=lambda x: x["ticker"]):
            all_targets.append(itm)

    processed_count = 0
    for idx, target in enumerate(all_targets, 1):
        ticker = target["ticker"].upper()
        earnings_date = target["earnings_date"]

        log_msg("-" * 65, log_file)
        log_msg(f"[T-1 {idx}/{len(all_targets)}] Running 5-Layer Pre-Earnings Harness for {ticker} ({earnings_date})...", log_file)

        h_code, h_out, h_err = run_command([sys.executable, "run_pre_harness.py", ticker, earnings_date])
        if h_code == 0:
            log_msg(f"[{ticker}] 5-Layer T-1 Pre-Earnings Harness completed and published.", log_file)
            processed_count += 1
        else:
            log_msg(f"[{ticker}] T-1 Pre-Earnings Harness warning/error: {h_err.strip() or h_out.strip()}", log_file)

        if idx < len(all_targets):
            log_msg(f"Pacing: Staggering next T-1 report generation by {stagger_delay} seconds...", log_file)
            time.sleep(stagger_delay)

    return processed_count

def run_t0_post_workflow(today_str: str, log_file: Path, stagger_delay: int = DEFAULT_STAGGER_DELAY_SECONDS):
    log_msg("=" * 75, log_file)
    log_msg(f"STARTING T+0 POST-EARNINGS HARNESS SCAN — {today_str}", log_file)
    log_msg("=" * 75, log_file)

    code, stdout, stderr = run_command([sys.executable, "stage1_post_deterministic.py", "--check-only"])
    t0_matches = []
    try:
        idx_brace = stdout.find("{")
        if idx_brace != -1:
            data = json.loads(stdout[idx_brace:])
            t0_matches = data.get("t0_matches", [])
    except Exception:
        pass

    if not t0_matches:
        log_msg("No T+0 post-earnings candidates found for today.", log_file)
        return 0

    log_msg(f"Found {len(t0_matches)} T+0 post-earnings candidate(s): {[m['ticker'] for m in t0_matches]}", log_file)
    processed_count = 0
    for idx, target in enumerate(t0_matches, 1):
        ticker = target["ticker"].upper()
        earnings_date = target.get("earnings_date", today_str)
        log_msg("-" * 65, log_file)
        log_msg(f"[T+0 {idx}/{len(t0_matches)}] Running 5-Layer Post-Earnings Harness for {ticker} ({earnings_date})...", log_file)

        h_code, h_out, h_err = run_command([sys.executable, "run_post_harness.py", ticker, earnings_date])
        if h_code == 0:
            log_msg(f"[{ticker}] T+0 Post-Earnings Harness completed and published.", log_file)
            processed_count += 1
        else:
            log_msg(f"[{ticker}] T+0 Post-Earnings Harness warning/error: {h_err.strip() or h_out.strip()}", log_file)

        if idx < len(t0_matches):
            log_msg(f"Pacing: Staggering next T+0 report by {stagger_delay} seconds...", log_file)
            time.sleep(stagger_delay)

    return processed_count

def run_daily_workflow(stagger_delay: int = DEFAULT_STAGGER_DELAY_SECONDS, mode: str = "all"):
    today_str = date.today().isoformat()
    log_file = LOGS_DIR / f"daily_run_{today_str}.log"
    t1_count = 0
    t0_count = 0
    if mode in ("all", "pre"):
        t1_count = run_t1_pre_workflow(today_str, log_file, stagger_delay)
    if mode in ("all", "post"):
        t0_count = run_t0_post_workflow(today_str, log_file, stagger_delay)

    log_msg("=" * 75, log_file)
    log_msg(f"DAILY HARNESS RUN COMPLETED. T-1 Processed: {t1_count} | T+0 Processed: {t0_count}", log_file)
    log_msg("=" * 75, log_file)

if __name__ == "__main__":
    delay = DEFAULT_STAGGER_DELAY_SECONDS
    mode = "all"
    for arg in sys.argv[1:]:
        if arg.isdigit():
            delay = int(arg)
        elif arg.lower() in ("--pre", "pre"):
            mode = "pre"
        elif arg.lower() in ("--post", "post"):
            mode = "post"
        elif arg.lower() in ("--all", "all"):
            mode = "all"
    run_daily_workflow(stagger_delay=delay, mode=mode)
