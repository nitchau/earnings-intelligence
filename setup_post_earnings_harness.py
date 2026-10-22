"""
Non-Destructive Environment Verifier & Initializer for the T+0 Post-Earnings Orchestration Harness.
Ensures all required directories and Track A + Track B pipeline scripts are present and intact
without overwriting live production scripts.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

REQUIRED_DIRS = [
    "ground_truth",
    "post_agent_bus",
    "drafts",
    "audit_logs",
    "published_reports",
    "logs"
]

REQUIRED_FILES = [
    "AGENTS.md",
    "AGENTS_POST.md",
    "stage1_post_deterministic.py",
    "stage4_validate_post.py",
    "stage4_render_post_html.py",
    "agent5_chief_auditor.py",
    "stage5_publish_github.py",
    "run_post_harness.py",
    "daily_runner.py"
]

def verify_post_earnings_harness() -> int:
    print("Verifying T+0 Post-Earnings Multi-Agent Orchestration Harness (Track A + Track B)...")
    for d in REQUIRED_DIRS:
        p = BASE_DIR / d
        p.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] Directory ready: {d}/")

    missing = []
    for f in REQUIRED_FILES:
        fp = BASE_DIR / f
        if fp.exists():
            print(f"  [OK] Core script verified: {f} ({fp.stat().st_size:,} bytes)")
        else:
            print(f"  [MISSING] Required file not found: {f}")
            missing.append(f)

    if missing:
        print(f"ERROR: Missing required orchestration files: {missing}")
        return 1

    print("SUCCESS: All T+0 Post-Earnings Orchestration scripts and directories are verified and active.")
    return 0

if __name__ == "__main__":
    sys.exit(verify_post_earnings_harness())
