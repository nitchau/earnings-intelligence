"""
End-to-End 5-Layer Orchestrator for Pre-Earnings (T-1) Tearsheet Generation (Track A + Track B Standard)
Executes the full 5-Layer T-1 workflow:
1. Layer 1: Deterministic Ground-Truth Data Mesh (stage1_fetch_truth.py)
2. Layer 2 & 3: Verifies pre_agent_bus/ files & runs dedicated T-1 draft builder ({TICKER}/build_{ticker}_draft.py)
3. Layer 4A: Deterministic 11-Guardrail Validator (stage3_validate_draft.py)
4. Layer 4B: Read-Only CSS Cloner, Multi-Versioning & Index Updater (stage4_render_html.py)
5. Layer 5: Chief HTML Auditor & Back-Router (agent5_pre_chief_auditor.py) + GitHub Pages Sync
"""

import sys
import subprocess
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

def run_step(cmd: list[str], step_name: str) -> bool:
    print(f"\n>>> RUNNING: {step_name}...")
    res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True, encoding="utf-8")
    if res.returncode != 0:
        print(f"[ERROR] Step '{step_name}' failed with exit code {res.returncode}.", file=sys.stderr)
        return False
    print(f"[SUCCESS] Step '{step_name}' passed.")
    return True

def sync_pre_to_github(ticker: str, earnings_date: str):
    print(f"\n>>> RUNNING: Stage 5 GitHub Pages Sync for {ticker} ({earnings_date})...")
    subprocess.run(
        ["git", "add", "published_reports/", "index.html", "published_ledger.json", "audit_logs/", "ground_truth/", "drafts/", "pre_agent_bus/"],
        cwd=str(BASE_DIR),
        text=True
    )
    commit_msg = f"Auto-publish T-1 Pre-Earnings Tearsheet (Track A+B) for {ticker} ({earnings_date})"
    c_res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR), capture_output=True, text=True)
    if c_res.returncode == 0:
        print("Git commit created successfully.")
        p_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), capture_output=True, text=True)
        if p_res.returncode == 0:
            print("Git push successful! GitHub Pages is updating.")
        else:
            print(f"Git push note: {p_res.stderr.strip() or p_res.stdout.strip()}")
    else:
        print(f"Git commit note: {c_res.stdout.strip() or c_res.stderr.strip()}")

def run_pre_harness_for_ticker(ticker: str, earnings_date: str):
    ticker = ticker.upper()
    print("=" * 75)
    print(f"STARTING 5-LAYER T-1 PRE-EARNINGS ORCHESTRATION: {ticker} ({earnings_date})")
    print("=" * 75)

    # Layer 1: Deterministic Ground-Truth Anchor
    if not run_step([sys.executable, "stage1_fetch_truth.py", ticker, earnings_date], "Layer 1: Deterministic Pre-Earnings Ground Truth"):
        sys.exit(1)

    # Layer 2 & 3: Check pre_agent_bus & run draft builder
    draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_draft.json"
    builder = BASE_DIR / ticker / f"build_{ticker.lower()}_draft.py"
    if builder.exists():
        if not run_step([sys.executable, str(builder)], f"Layer 3: T-1 Draft Builder for {ticker}"):
            sys.exit(1)
    elif not draft_path.exists():
        print(f"[NOTICE] Draft {draft_path.name} not found. Please populate pre_agent_bus/ and build draft.", file=sys.stderr)
        sys.exit(1)

    # Layer 4A: Stage 3 Deterministic Validation (11 Guardrails)
    if not run_step([sys.executable, "stage3_validate_draft.py", ticker, earnings_date], "Layer 4A: Stage 3 Deterministic 11-Guardrail Validation"):
        sys.exit(1)

    # Layer 4B: Stage 4 HTML Rendering & Multi-Versioning
    if not run_step([sys.executable, "stage4_render_html.py", ticker, earnings_date], "Layer 4B: Stage 4 HTML Rendering & Multi-Versioning"):
        sys.exit(1)

    # Layer 5: Agent 5 Chief Pre-Earnings HTML Cross-Audit
    if not run_step([sys.executable, "agent5_pre_chief_auditor.py", ticker, earnings_date], "Layer 5: Agent 5 Chief Pre-Earnings HTML Cross-Audit"):
        sys.exit(1)

    # Stage 5: GitHub Sync
    sync_pre_to_github(ticker, earnings_date)

    print("\n" + "=" * 75)
    print(f"5-LAYER T-1 PRE-EARNINGS HARNESS COMPLETE FOR {ticker} ({earnings_date})")
    print("=" * 75)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_pre_harness.py <TICKER> [EARNINGS_DATE]", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    run_pre_harness_for_ticker(t, d)
