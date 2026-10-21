"""
End-to-End Orchestrator for Post-Earnings (T+0) Tearsheet Generation
Executes the full 5-Layer workflow:
1. Stage 1: Deterministic Data Mesh (stage1_post_deterministic.py)
2. Layer 2: Checks bus files or invokes dedicated draft builder
3. Stage 4: stage4_validate_post.py & stage4_render_post_html.py
4. Layer 5: agent5_chief_auditor.py & stage5_publish_github.py
"""

import sys
import json
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

def run_post_harness_for_ticker(ticker: str, earnings_date: str):
    ticker = ticker.upper()
    print("=" * 75)
    print(f"STARTING T+0 POST-EARNINGS ORCHESTRATION: {ticker} ({earnings_date})")
    print("=" * 75)

    # Step 1: Stage 1 Deterministic Anchor
    if not run_step([sys.executable, "stage1_post_deterministic.py", ticker, earnings_date], "Stage 1 Deterministic Anchor"):
        sys.exit(1)

    # Step 2: Check Layer 2 Bus files / run draft builder if present
    draft_path = BASE_DIR / "drafts" / f"{ticker}_{earnings_date}_post_draft.json"
    if not draft_path.exists():
        builder = BASE_DIR / ticker / f"build_{ticker.lower()}_post_draft.py"
        if builder.exists():
            if not run_step([sys.executable, str(builder)], f"Draft Builder for {ticker}"):
                sys.exit(1)
        else:
            print(f"[NOTICE] Draft {draft_path.name} not found. Please populate Layer 2 bus and build draft.", file=sys.stderr)
            sys.exit(1)

    # Step 3: Stage 4 Validation
    if not run_step([sys.executable, "stage4_validate_post.py", ticker, earnings_date], "Stage 4 Deterministic Validation"):
        sys.exit(1)

    # Step 4: Stage 4 HTML Rendering
    if not run_step([sys.executable, "stage4_render_post_html.py", ticker, earnings_date], "Stage 4 HTML Rendering"):
        sys.exit(1)

    # Step 5: Agent 5 Cross-Audit
    if not run_step([sys.executable, "agent5_chief_auditor.py", ticker, earnings_date], "Agent 5 Chief HTML Cross-Audit"):
        sys.exit(1)

    # Step 6: Stage 5 Publish & GitHub Sync
    if not run_step([sys.executable, "stage5_publish_github.py", ticker, earnings_date], "Stage 5 GitHub Publishing"):
        sys.exit(1)

    print("=" * 75)
    print(f"T+0 POST-EARNINGS HARNESS RUN COMPLETE FOR {ticker} ({earnings_date})")
    print("=" * 75)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_post_harness.py <TICKER> [EARNINGS_DATE]", file=sys.stderr)
        sys.exit(1)
    t = sys.argv[1].upper()
    d = sys.argv[2] if len(sys.argv) > 2 else date.today().isoformat()
    run_post_harness_for_ticker(t, d)
