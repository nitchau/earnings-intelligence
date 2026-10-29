"""
Shared In-Page Historical Quarter Archive Topbar & Quarter Resolver
Replaces legacy v1/v2 iteration banners inside rendered T-1 and T+0 tearsheets with:
- Back to Tearsheet Portal link
- Paired T-1 <-> T+0 stage toggle (hydrated from history_catalog.js)
- Historical Quarter <select> dropdown (hydrated from published_reports/history_catalog.js)
"""

import html
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
GROUND_TRUTH_DIR = BASE_DIR / "ground_truth"


def _advance_quarter_token(q_num: int, yr_tok: str, steps: int = 1) -> str:
    fy_prefix = "FY" if yr_tok.upper().startswith("FY") else ""
    yr_digits = yr_tok[2:] if fy_prefix else yr_tok
    total_q = (int(yr_digits) * 4 + (q_num - 1)) + steps
    ny = total_q // 4
    nq = (total_q % 4) + 1
    ny_str = f"{ny:02d}" if len(yr_digits) == 2 else f"{ny}"
    return f"Q{nq} {fy_prefix}{ny_str}"


def resolve_quarter_label(ticker: str, earnings_date: str) -> str:
    """Resolve human-readable reported/upcoming fiscal quarter label (e.g. 'Q3 2026') for (ticker, earnings_date)."""
    ticker = ticker.upper()
    post_path = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_post_truth.json"
    if post_path.exists():
        try:
            pt = json.loads(post_path.read_text(encoding="utf-8"))
            labels = (pt.get("stitched_5q_chronological") or {}).get("period_labels") or []
            if labels:
                return re.sub(r"\s*\(Actual\)\s*$", "", str(labels[-1])).strip()
        except Exception:
            pass

    pre_2a_path = BASE_DIR / "pre_agent_bus" / f"{ticker}_{earnings_date}_pre_agent2a_kpis.json"
    if pre_2a_path.exists():
        try:
            p2a = json.loads(pre_2a_path.read_text(encoding="utf-8"))
            up_lbl = str(p2a.get("upcoming_quarter_label") or "").strip()
            m_up = re.search(r"\b(Q[1-4])\s+((?:FY)?\d{2,4})E?\b", up_lbl, re.IGNORECASE)
            if m_up:
                return f"{m_up.group(1).upper()} {m_up.group(2).upper()}"
        except Exception:
            pass

    pre_path = GROUND_TRUTH_DIR / f"{ticker}_{earnings_date}_truth.json"
    if pre_path.exists():
        try:
            t1 = json.loads(pre_path.read_text(encoding="utf-8"))
            hdrs = (((t1.get("stitched_5q_financials") or {}).get("income_statement_5q") or {}).get("period_headers")) or []
            pl = str(hdrs[-1]) if hdrs else str(((t1.get("forensic_fcf_bridge_latest") or {}).get("period_label")) or "")
            m = re.search(r"\bQ([1-4])\s+((?:FY)?\d{2,4})\b", pl, re.IGNORECASE)
            if m:
                pq = int(m.group(1))
                yr_tok = m.group(2)
                steps = 1
                m_end = re.search(r"Ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", pl)
                if m_end:
                    try:
                        end_dt = datetime.strptime(m_end.group(1), "%b %d, %Y")
                        rel_dt = datetime.strptime(earnings_date, "%Y-%m-%d")
                        gap_days = (rel_dt - end_dt).days
                        # If period_headers[-1] ended 15..78 days before release_date, yfinance already captured Q0
                        if 15 <= gap_days <= 78:
                            steps = 0
                    except Exception:
                        pass
                return _advance_quarter_token(pq, yr_tok, steps=steps)
        except Exception:
            pass

    try:
        ref = datetime.strptime(earnings_date, "%Y-%m-%d") - timedelta(days=45)
        q_num = (ref.month - 1) // 3 + 1
        return f"Q{q_num} {ref.year}"
    except Exception:
        return "Current Quarter"


def format_short_date(earnings_date: str) -> str:
    try:
        dt = datetime.strptime(earnings_date, "%Y-%m-%d")
        return f"{dt:%b} {dt.day}, {dt.year}"
    except Exception:
        return earnings_date


def build_archive_topbar_html(ticker: str, earnings_date: str, is_post: bool) -> str:
    """Build clean institutional Historical Quarter Archive topbar HTML (zero v1/v2 iteration clutter)."""
    ticker = ticker.upper()
    q_label = resolve_quarter_label(ticker, earnings_date)
    d_label = format_short_date(earnings_date)
    curr_file = f"{ticker}_T0_POST_{earnings_date}.html" if is_post else f"{ticker}_T1_{earnings_date}.html"
    paired_file = f"{ticker}_T1_{earnings_date}.html" if is_post else f"{ticker}_T0_POST_{earnings_date}.html"
    stage_code = "t0" if is_post else "t1"

    # Note: Never emit uppercase 'T-1 PRE-EARNINGS' inside T+0 HTML (Guardrail 10 bleed check)
    active_badge_text = "T+0 Post-Earnings Forensic" if is_post else "T-1 Pre-Earnings Briefing"
    active_badge_style = (
        "background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);"
        if is_post
        else "background: rgba(59, 130, 246, 0.18); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);"
    )
    paired_link_label = "Switch to T-1 Pre-Earnings Setup" if is_post else "Switch to T+0 Post-Earnings Report →"

    esc_tk = html.escape(ticker, quote=True)
    esc_dt = html.escape(earnings_date, quote=True)
    esc_q = html.escape(q_label, quote=True)
    esc_d = html.escape(d_label, quote=True)
    esc_curr = html.escape(curr_file, quote=True)
    esc_paired = html.escape(paired_file, quote=True)

    return f"""
    <!-- HISTORICAL QUARTER ARCHIVE TOPBAR -->
    <div class="archive-topbar" style="background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(59, 130, 246, 0.32); border-radius: 10px; padding: 10px 16px; margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 12.5px;">
      <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <a href="index.html" style="color: #93c5fd; text-decoration: none; font-weight: 600; padding: 4px 10px; border-radius: 6px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12);">← Portal Home</a>
        <span style="{active_badge_style} font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 3px 9px; border-radius: 5px;">{active_badge_text}</span>
        <a id="archive-paired-stage-link" href="{esc_paired}" style="display: none; color: #cbd5e1; text-decoration: none; font-size: 11.5px; padding: 3px 9px; border-radius: 5px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.12);">{paired_link_label}</a>
      </div>
      <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
        <label for="quarter-archive-select" style="color: #94a3b8; font-size: 12px; font-weight: 600;">📅 Historical Quarter:</label>
        <select id="quarter-archive-select" data-ticker="{esc_tk}" data-date="{esc_dt}" data-stage="{stage_code}" style="background: #090d16; color: #f8fafc; border: 1px solid rgba(59, 130, 246, 0.45); border-radius: 6px; padding: 5px 10px; font-size: 12px; font-family: 'Inter', sans-serif; font-weight: 600; cursor: pointer; outline: none;">
          <option value="{esc_curr}" selected>{esc_q} ({esc_d}) — Latest</option>
          <option value="" disabled>No prior quarters archived yet (history initiated {esc_q})</option>
        </select>
      </div>
    </div>
    <script src="history_catalog.js"></script>
    <script>
      (function() {{
        var sel = document.getElementById('quarter-archive-select');
        if (!sel) return;
        var tk = sel.getAttribute('data-ticker');
        var curDate = sel.getAttribute('data-date');
        var stage = sel.getAttribute('data-stage');
        var cat = (window.EARNINGS_HISTORY_CATALOG || {{}})[tk];
        if (Array.isArray(cat) && cat.length > 0) {{
          sel.innerHTML = '';
          cat.forEach(function(entry, idx) {{
            var targetFile = (stage === 't0') ? (entry.t0 || entry.t1) : (entry.t1 || entry.t0);
            if (!targetFile) return;
            var opt = document.createElement('option');
            opt.value = targetFile;
            var suffix = (idx === 0) ? ' — Latest' : '';
            var stageHint = (stage === 't0' && !entry.t0) ? ' [T-1 Only]' : ((stage === 't1' && !entry.t1) ? ' [T+0 Only]' : '');
            opt.textContent = entry.quarter + ' (' + entry.date_display + ')' + stageHint + suffix;
            if (entry.date === curDate) opt.selected = true;
            sel.appendChild(opt);
          }});
          if (cat.length === 1) {{
            var note = document.createElement('option');
            note.value = '';
            note.disabled = true;
            note.textContent = '── Prior quarters will appear here starting next quarter ──';
            sel.appendChild(note);
          }}
          var curEntry = cat.find(function(e) {{ return e.date === curDate; }});
          var pairedLink = document.getElementById('archive-paired-stage-link');
          if (curEntry && pairedLink) {{
            var pairedHref = (stage === 't0') ? curEntry.t1 : curEntry.t0;
            if (pairedHref) {{
              pairedLink.href = pairedHref;
              pairedLink.style.display = 'inline-block';
            }}
          }}
        }}
        sel.addEventListener('change', function() {{
          if (this.value && !window.location.pathname.endsWith('/' + this.value)) {{
            window.location.href = this.value;
          }}
        }});
      }})();
    </script>"""
