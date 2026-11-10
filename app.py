"""
White. · monthly money check-in (DPM 2026, Group 9)

One user:      mid-career professionals who manage their own money
One use case:  salary day, "Am I on track for my goal, and what should I do with this month's money?"
One workflow:  1 Where I stand -> 2 Set a goal -> 3 Investment options -> 4 My plan (+ "What if…?" check)
One AI job:    Gemini EXPLAINS and COMPARES numbers in plain language.
               Every number is calculated by fixed rules in this file, never by the AI.

Nothing is stored. Values live only in this browser session.
"""

import datetime as dt
import json
import math

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="White · Your money, nothing hidden", page_icon="○", layout="wide",
                   initial_sidebar_state="collapsed")


# ═════════════════════════════════════════════════════════════
# 1. LOOK AND FEEL
#    White, calm, premium. Warm off-white page, white cards with a hairline and a soft shadow,
#    one accent (deep navy), gold only on the AI card. Desktop: inputs left, results right.
#    Phone: single column, sticky Back/Next bar. Native widgets are restyled; results are HTML blocks.
# ═════════════════════════════════════════════════════════════
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root { --bg:#F7F7F5; --surface:#FFFFFF; --line:#E8E7E3; --line-2:#DCDBD6;
        --ink:#111114; --ink-2:#55565E; --ink-3:#8A8B92;
        --accent:#14213D; --accent-soft:#E9EDF5;
        --gold:#B8862B; --gold-tint:#F3E7C9; --gold-soft:#FBF6EA;
        --good:#1F8A5B; --good-bg:#E7F5EE; --warn:#B4462B; --warn-bg:#FBECE7;
        --shadow: 0 1px 2px rgba(16,17,20,.04), 0 8px 24px rgba(16,17,20,.06);
        --sans: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        --display: 'Sora', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }

html, body, .stApp, p, label, input, textarea, select, button { font-family: var(--sans); }
.stApp { background: var(--bg); color: var(--ink); }
.block-container { max-width: 1120px; padding-top: 0.6rem; padding-bottom: 3rem; }
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stElementToolbar"] { display: none; }
h1, h2, h3, h4 { font-family: var(--display) !important; letter-spacing: -0.4px; color: var(--ink); font-weight: 600 !important; }
h2 { font-size: 28px !important; margin: 4px 0 2px !important; padding: 0 !important; }
.lede { color: var(--ink-2); font-size: 15px; margin: 0 0 18px; }
p, li { color: var(--ink); }

/* ── top bar: logo, step progress, AI toggle ───────────────────────── */
div[data-testid="stHorizontalBlock"]:has(.topbar) { align-items: center; flex-wrap: nowrap !important; gap: 8px;
  padding: 10px 0 10px; border-bottom: 1px solid var(--line); margin-bottom: 14px; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"] { min-width: 0 !important; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"]:last-child { flex: 0 0 auto !important; width: auto !important; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"]:first-child { flex: 1 1 auto !important; }
.topbar { display:flex; align-items:center; gap:22px; min-height:36px; }
.logo { display:flex; align-items:center; gap:10px; text-decoration:none; }
.logo .mark { width:28px; height:28px; border-radius:8px; background:#fff; border:1px solid var(--line-2);
  box-shadow: 0 1px 2px rgba(16,17,20,.06); position:relative; flex:0 0 auto; }
.logo .mark::after { content:""; position:absolute; width:7px; height:7px; border-radius:50%; background:var(--accent);
  right:6px; bottom:6px; }
.logo .word { font-family: var(--display); font-weight:600; font-size:20px; letter-spacing:-.4px; color:var(--ink); }
.logo .word b { color: var(--accent); }
.logo .tag { font-size:12.5px; color: var(--ink-3); margin-left:2px; }
.steps { display:none; align-items:center; gap:6px; }
.steps .st { display:flex; align-items:center; gap:7px; font-size:12.5px; color: var(--ink-3); font-weight:600; white-space:nowrap; }
.steps .st .n { width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-size:11px; font-weight:700; border:1.5px solid var(--line-2); color: var(--ink-3); background:#fff; flex:0 0 auto; }
.steps .st.done .n { border-color: var(--accent); color: var(--accent); }
.steps .st.now .n { background: var(--accent); border-color: var(--accent); color:#fff; }
.steps .st.now { color: var(--ink); }
.steps .ln { width:22px; height:1px; background: var(--line-2); }
.steps .ln.done { background: var(--accent); }

/* ── cards and type ────────────────────────────────────────────────── */
.card { background: var(--surface); border:1px solid var(--line); border-radius:20px; padding:22px 24px;
        margin-bottom:14px; box-shadow: var(--shadow); animation: rise .18s ease-out both; }
.card.flat { box-shadow:none; }
.card.ai { border-left: 3px solid var(--gold); background: var(--surface); }
@keyframes rise { from { opacity:0; transform: translateY(4px);} to { opacity:1; transform:none;} }
@media (prefers-reduced-motion: reduce) { .card { animation: none; } }
.k { font-size:13px; color: var(--ink-2); font-weight:600; }
.cap { font-size:12.5px; color: var(--ink-3); line-height:1.5; }
.num { font-family: var(--display); font-weight:600; letter-spacing:-1px; line-height:1.05; color: var(--ink);
       font-variant-numeric: tabular-nums; }
.num.xl { font-size:56px; letter-spacing:-2px; } .num.lg { font-size:32px; } .num.md { font-size:22px; letter-spacing:-.5px; }
.num .u { font-size:.4em; font-weight:500; color: var(--ink-3); letter-spacing:0; margin-left:4px; }
.good { color: var(--good) !important; } .warn { color: var(--warn) !important; }
.row { display:flex; justify-content:space-between; align-items:center; gap:10px; }
.pill { display:inline-block; font-size:11px; font-weight:700; letter-spacing:.6px; padding:4px 10px; border-radius:999px;
        border:1px solid var(--line-2); color: var(--ink-2); background:#fff; white-space:nowrap; }
.pill.ok { color: var(--good); border-color: transparent; background: var(--good-bg); }
.pill.warn { color: var(--warn); border-color: transparent; background: var(--warn-bg); }
.pill.gold { color: var(--gold); border-color: transparent; background: var(--gold-tint); }
.pill.navy { color:#fff; border-color: transparent; background: var(--accent); }
.hair { height:1px; background: var(--line); margin:16px 0; }

/* stacked bar + legend */
.split { display:flex; height:12px; gap:3px; margin:18px 0 10px; }
.split span { display:block; border-radius:4px; min-width:3px; }
.legend { display:flex; flex-wrap:wrap; gap:8px 18px; font-size:12.5px; color: var(--ink-2); }
.legend i { display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:7px; vertical-align:-1px; }
.legend b { color: var(--ink); font-weight:700; font-variant-numeric: tabular-nums; }

/* KPI tiles */
.kpis { display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:12px; margin-bottom:14px; }
.kpi { background: var(--surface); border:1px solid var(--line); border-radius:16px; padding:16px 18px; box-shadow: var(--shadow); }
.kpi .ic { width:30px; height:30px; border-radius:9px; background: var(--bg); border:1px solid var(--line);
           display:flex; align-items:center; justify-content:center; margin-bottom:12px; }
.kpi .k { margin-bottom:4px; }

/* gauge / ring blocks */
.gauge { display:flex; align-items:center; gap:20px; }
.gauge svg { flex:0 0 auto; }
.gauge .mid { font-family: var(--display); font-weight:600; font-size:22px; letter-spacing:-.5px; fill: var(--ink); }
.gauge .sub { font-size:10.5px; fill: var(--ink-3); font-weight:600; }

/* key/value rows, option cards */
.kv { display:flex; justify-content:space-between; gap:8px; font-size:13px; padding:7px 0; color: var(--ink-2);
      border-bottom:1px solid var(--line); }
.kv:last-child { border-bottom:none; }
.kv b { color: var(--ink); font-weight:700; text-align:right; font-variant-numeric: tabular-nums; }
.opt { background: var(--surface); border:1px solid var(--line); border-radius:18px; padding:18px 18px 14px; margin-bottom:10px;
       box-shadow: var(--shadow); position:relative; }
.opt.sel { border:2px solid var(--accent); padding:17px 17px 13px; }
.opt .name { font-family: var(--display); font-weight:600; font-size:17px; display:flex; align-items:center; gap:9px; }
.opt .name i { width:10px; height:10px; border-radius:50%; display:inline-block; }
.opt .foot { margin-top:12px; min-height:58px; }

/* what-if timeline */
.tl { display:flex; align-items:center; gap:10px; margin:14px 0 6px; }
.tl .d { font-family: var(--display); font-weight:600; font-size:22px; letter-spacing:-.5px; font-variant-numeric: tabular-nums; white-space:nowrap; }
.tl .d small { display:block; font-family: var(--sans); font-size:11.5px; color: var(--ink-3); font-weight:600; letter-spacing:0; margin-bottom:2px; }
.tl .line { flex:1; height:2px; background: var(--line-2); position:relative; min-width:30px; }
.tl .line::after { content:""; position:absolute; right:-1px; top:-4px; border:5px solid transparent; border-left:7px solid var(--line-2); }

/* AI card */
.ai-head { display:flex; align-items:center; gap:8px; font-size:11px; font-weight:800; letter-spacing:1.1px; color: var(--gold); margin-bottom:10px; }
.ai-text { color: var(--ink); font-size:15.5px; line-height:1.6; margin:0; }
.ai-src { font-size:12px; color: var(--ink-3); margin-top:12px; }

.hero-title { font-size:56px; line-height:1.02; margin:8px 0 18px; letter-spacing:-2px; font-weight:600 !important; }
.hero-title .dim { color: var(--ink-3); }
.step-tile { background: var(--surface); border:1px solid var(--line); border-radius:16px; padding:16px; box-shadow: var(--shadow); }
.step-tile b { font-family: var(--display); color: var(--accent); font-size:12px; font-weight:600; }
.step-tile div { font-weight:600; margin-top:6px; font-size:14.5px; }
.footer { text-align:center; font-size:12px; color: var(--ink-3); margin-top:30px; }
.grid2 { display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:12px; }
.grid3 { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:12px; }

/* ── native widgets, restyled ──────────────────────────────────────── */
button[data-testid="stBaseButton-primary"], div.stDownloadButton > button {
  background: var(--accent) !important; color:#fff !important; border:none !important; border-radius:12px !important;
  font-weight:700 !important; min-height:48px; box-shadow: 0 1px 2px rgba(20,33,61,.2), 0 6px 16px rgba(20,33,61,.18) !important;
  transition: transform .08s ease, box-shadow .08s ease; }
button[data-testid="stBaseButton-primary"] p, div.stDownloadButton > button p { color:#fff !important; font-weight:700 !important; }
button[data-testid="stBaseButton-primary"]:hover, div.stDownloadButton > button:hover { background:#1B2C50 !important; }
button[data-testid="stBaseButton-primary"]:active { transform: translateY(1px); }
button[data-testid="stBaseButton-secondary"] { background:#fff !important; color: var(--ink) !important;
  border:1px solid var(--line-2) !important; border-radius:12px !important; min-height:48px; font-weight:600 !important; }
button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
button[data-testid="stBaseButton-tertiary"] { color: var(--ink-2) !important; }
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div {
  background:#fff !important; border-color: var(--line-2) !important; border-radius:12px !important; }
div[data-baseweb="input"]:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft); }
[data-testid="stNumberInput"] button { background:#fff !important; border-color: var(--line-2) !important; }
[data-testid="stWidgetLabel"] p { color: var(--ink-2) !important; font-weight:600 !important; font-size:13.5px !important; }
[data-testid="stTabs"] button p { font-weight:600; color: var(--ink-2); }
[data-testid="stTabs"] [aria-selected="true"] p { color: var(--ink) !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { background: var(--accent) !important; }
[data-testid="stTabs"] [data-baseweb="tab-border"] { background: var(--line) !important; }
[data-testid="stExpander"] details { border:1px solid var(--line) !important; border-radius:14px !important; background:#fff; }
[data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span { color: var(--ink-2) !important; font-weight:600; }
[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid var(--line) !important; border-radius:20px !important;
  background: var(--surface); box-shadow: var(--shadow); padding: 6px 8px; }
button[data-variant="segmented_control"], button[data-variant="pills"] {
  border-radius:999px !important; border:1px solid var(--line-2) !important; background:#fff !important; color: var(--ink-2) !important;
  font-weight:600 !important; min-height:38px; padding: 0 14px !important; }
button[data-variant="segmented_control"][aria-checked="true"], button[data-variant="pills"][aria-checked="true"] {
  background: var(--accent) !important; border-color: var(--accent) !important; color:#fff !important; }
button[data-variant="segmented_control"][aria-checked="true"] p, button[data-variant="pills"][aria-checked="true"] p { color:#fff !important; }
[data-testid="stButtonGroup"] [role="radiogroup"] { gap:6px; }
/* step tabs (key="nav"): a quiet, clickable progress row */
.st-key-nav button[data-variant="segmented_control"] { background: transparent !important; border-color: transparent !important;
  color: var(--ink-3) !important; min-height:36px; padding: 0 12px !important; }
.st-key-nav button[data-variant="segmented_control"] p { font-size:13.5px; font-variant-numeric: tabular-nums; }
.st-key-nav button[data-variant="segmented_control"]:hover { color: var(--ink) !important; background: #fff !important; border-color: var(--line) !important; }
.st-key-nav button[data-variant="segmented_control"][aria-checked="true"] { background: var(--accent-soft) !important; border-color: transparent !important; }
.st-key-nav button[data-variant="segmented_control"][aria-checked="true"] p { color: var(--accent) !important; font-weight:700; }
.st-key-nav { margin-bottom: 6px; }
[data-testid="stRadio"] label p { color: var(--ink) !important; font-weight:500 !important; }
.st-key-use_ai label p { color: var(--ink-2) !important; font-weight:600 !important; }
[data-testid="stAlert"] { border-radius:14px; }
[data-testid="stCode"] pre, [data-testid="stCode"] code { background:#F7F7F5 !important; border-radius:10px; font-size:12px; }
div[data-testid="stCaptionContainer"] p { color: var(--ink-3) !important; }

/* ── phones ────────────────────────────────────────────────────────── */
@media (max-width: 760px) {
  .block-container { padding-left: 16px; padding-right: 16px; }
  div[data-testid="stHorizontalBlock"] { gap: 0.9rem !important; }
  .steps { display:flex; gap:5px; }
  .steps .st span.l, .steps .ln, .logo .tag { display:none; }
  .steps .st .n { width:18px; height:18px; font-size:0; }
  .steps .st.now .n { width:22px; }
  .topbar { gap:10px; }
  div[data-testid="stHorizontalBlock"]:has(.topbar) { gap: 6px; }
  .st-key-use_ai label p { font-size:12px !important; white-space:nowrap; }
  .st-key-use_ai [data-testid="stTooltipIcon"], .st-key-use_ai [data-testid="stTooltipHoverTarget"] { display:none; }
  .num.xl { font-size:40px; } .num.lg { font-size:26px; } .num.md { font-size:19px; }
  .hero-title { font-size:38px; letter-spacing:-1.2px; }
  .card { padding:18px; border-radius:18px; }
  .kpi { padding:14px; }
  .grid3 { gap:8px; }
  .tl .d { font-size:18px; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-back"]) { position: sticky; bottom: 0; z-index: 30;
    background: rgba(247,247,245,.92); backdrop-filter: blur(8px); padding: 10px 0 12px; margin: 6px -16px 0; padding-left:16px; padding-right:16px;
    border-top: 1px solid var(--line); flex-wrap: nowrap !important; }
  div[data-testid="stHorizontalBlock"]:has([class*="st-key-back"]) > div[data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


def icon(path, color="#55565E", size=16):
    """Small decorative line icon."""
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>')


I_WALLET = '<rect x="3" y="6" width="18" height="13" rx="3"/><path d="M16 13h2M3 10h18"/>'
I_SHIELD = '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>'
I_TREND = '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'
I_CAL = '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>'
I_SPARK = '<path d="M12 3l1.8 4.6L18 9.4l-4.2 1.8L12 16l-1.8-4.8L6 9.4l4.2-1.8z"/>'
I_LOCK = '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
I_CHECK = '<path d="M5 12l5 5L20 7"/>'
GOAL_ICONS = {"Car": '<path d="M5 16l1.5-5h11L19 16"/><rect x="3" y="16" width="18" height="4" rx="1"/><circle cx="7" cy="20" r="1"/><circle cx="17" cy="20" r="1"/>',
              "Bike": '<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M6 17l4-7h5l3 7M10 10l2 7"/>',
              "House": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/>',
              "Trip": '<path d="M2 16l20-6-4 4 2 6-4-2-3 3-1-5z"/>',
              "Gadget": '<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M11 18h2"/>',
              "Wedding": '<circle cx="9" cy="13" r="5"/><circle cx="15" cy="13" r="5"/>',
              "Other": '<path d="M12 3l1.8 4.6L18 9.4l-4.2 1.8L12 16l-1.8-4.8L6 9.4l4.2-1.8z"/>'}


# ═════════════════════════════════════════════════════════════
# 2. HELPERS (formatting and the core savings maths)
# ═════════════════════════════════════════════════════════════
def inr(x):
    """Indian number format: 145000 -> ₹1,45,000."""
    neg = x < 0
    s = str(int(round(abs(x))))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        groups = []
        while len(head) > 2:
            groups.insert(0, head[-2:])
            head = head[:-2]
        if head:
            groups.insert(0, head)
        s = ",".join(groups) + "," + tail
    return ("−" if neg else "") + "₹" + s


def short_inr(x):
    """₹6.8 L / ₹1.2 Cr style for big amounts."""
    sign = "−" if x < 0 else ""
    if abs(x) >= 1e7:
        return f"{sign}₹{abs(x) / 1e7:.1f} Cr"
    if abs(x) >= 1e5:
        return f"{sign}₹{abs(x) / 1e5:.1f} L"
    return inr(x)


def add_months(d, n):
    m = d.month - 1 + n
    return dt.date(d.year + m // 12, m % 12 + 1, min(d.day, 28))


def months_between(a, b):
    return max(1, (b.year - a.year) * 12 + (b.month - a.month))


def fmt_month(d):
    return d.strftime("%b %Y")


def months_to_goal(saved, monthly, target, annual_return):
    """Months until saved + monthly contributions (growing at annual_return) reach target. None if > 50 years."""
    i = annual_return / 12
    bal, n = saved, 0
    while bal < target:
        n += 1
        bal = bal * (1 + i) + monthly
        if n > 600:
            return None
    return n


def path(saved, monthly, annual_return, months):
    """Balance at the end of each month, month 0..months (for the charts)."""
    i = annual_return / 12
    bal, out = saved, [saved]
    for _ in range(months):
        bal = bal * (1 + i) + monthly
        out.append(bal)
    return out


def card(html, cls="card"):
    st.markdown(f'<div class="{cls}">{html}</div>', unsafe_allow_html=True)


def ring(frac, color, size=112, stroke=10, label="", sub=""):
    """Full progress ring (SVG). frac 0..1; text in the middle."""
    r = (size - stroke) / 2
    c = 2 * math.pi * r
    frac = max(0.0, min(1.0, frac))
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="{label} {sub}">'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="#EEEEEA" stroke-width="{stroke}"/>'
            f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-dasharray="{frac*c:.1f} {c:.1f}" transform="rotate(-90 {size/2} {size/2})"/>'
            f'<text x="50%" y="50%" dy="2" text-anchor="middle" dominant-baseline="middle" class="mid">{label}</text>'
            f'<text x="50%" y="50%" dy="20" text-anchor="middle" class="sub">{sub}</text></svg>')


def gauge(value, max_value, marker, color, size=128, stroke=11, label="", sub=""):
    """270° gauge (SVG) with a marker tick, e.g. emergency buffer 0–6 months with a 3-month marker."""
    r = (size - stroke) / 2 - 4
    c = 2 * math.pi * r
    arc = 0.75 * c
    frac = max(0.0, min(1.0, value / max_value))
    cx = cy = size / 2
    ang = math.radians(135 + 270 * marker / max_value)
    x1, y1 = cx + (r - stroke) * math.cos(ang), cy + (r - stroke) * math.sin(ang)
    x2, y2 = cx + (r + stroke) * math.cos(ang), cy + (r + stroke) * math.sin(ang)
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="{label} {sub}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EEEEEA" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-dasharray="{arc:.1f} {c:.1f}" transform="rotate(135 {cx} {cy})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-dasharray="{frac*arc:.1f} {c:.1f}" transform="rotate(135 {cx} {cy})"/>'
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8A8B92" stroke-width="2" stroke-dasharray="2 2"/>'
            f'<text x="50%" y="50%" dy="2" text-anchor="middle" dominant-baseline="middle" class="mid">{label}</text>'
            f'<text x="50%" y="50%" dy="22" text-anchor="middle" class="sub">{sub}</text></svg>')


def bar3(a, b, c, colors, margin="14px 0 8px"):
    """Three-part stacked bar (salary split, debt/equity/gold)."""
    tot = max(a + b + c, 1)
    return (f'<div class="split" style="margin:{margin}">'
            + "".join(f'<span style="width:{max(v, 0) / tot * 100:.1f}%;background:{col}"></span>'
                      for v, col in zip((a, b, c), colors)) + '</div>')


ALLOC = ("#9AA3B2", "#14213D", "#D9B45B")        # debt, equity, gold
SPLIT = ("#9AA3B2", "#D5D8DE", "#14213D")        # committed, everyday, free


# ═════════════════════════════════════════════════════════════
# 3. SESSION STATE (sample numbers so the demo works immediately; nothing saved to disk)
# ═════════════════════════════════════════════════════════════
TODAY = dt.date.today()
STEPS = ["Where I stand", "Set a goal", "Investment options", "My plan"]
DEFAULTS = {
    "step": 0, "nav": None,
    "salary": 145000, "salary_day": 1,
    "rent": 32000, "emi": 28500, "sip": 15000, "bills": 10100, "usual": 21000,
    "savings": 210000, "invest": 680000, "loans": 600000, "cards": 18000,
    "goal_type": "Car", "goal_name": "New car", "goal_cost": 800000,
    "goal_date": add_months(TODAY, 30), "goal_saved": 150000, "goal_monthly": 18000,
    "q_drop": "Wait it out", "q_exp": "Some experience", "q_early": "Maybe",
    "r_debt": 7.0, "r_equity": 11.0, "r_gold": 8.0, "choice": "Balanced",
    "wi_kind": "One-off spend", "wi_amount": 15000, "wi_from": "This month's goal money", "wi_monthly": 3000,
    "use_ai": True,
}
for k, v in DEFAULTS.items():                      # re-assigning keeps values when moving between steps
    st.session_state[k] = st.session_state.get(k, v)
S = st.session_state


def go(step):
    """Buttons call this. Keeps the step tabs in sync."""
    S.step = step
    S.nav = STEPS[step - 1] if step > 0 else None


def nav_changed():
    """Step tabs call this."""
    if S.nav in STEPS:
        S.step = STEPS.index(S.nav) + 1
    else:                                           # clicking the selected tab again un-selects it
        S.nav = STEPS[S.step - 1]


def pick(name):
    """Option-card buttons call this (step 3)."""
    S.choice = name


# ═════════════════════════════════════════════════════════════
# 4. THE ONE AI CAPABILITY: explain and compare (Gemini)
# ═════════════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are the explanation layer inside a personal-finance check-in app for working
professionals in India. You receive numbers that the app has ALREADY calculated.
Rules:
- Use only the facts given. Never invent or recalculate numbers.
- Plain, warm, everyday English. Short sentences. Keep rupee formats as given (₹, L).
- Never name specific funds, stocks, banks or products. Never promise or predict returns.
- When comparing options or a decision, describe trade-offs only. Never say which option is best
  or whether the user should do it. The user decides.
- If something is at risk (short timeline with high equity, thin emergency buffer), say so gently.
- Maximum 80 words. No headings, no bullet points, no greeting."""


def get_secret(name, default=None):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


@st.cache_data(show_spinner=False, ttl=3600)
def call_gemini(task, facts_json, api_key, model):
    """One task + the calculated facts -> Gemini -> short text. Cached so reruns don't call again."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    try:
        resp = client.models.generate_content(
            model=model,
            contents=f"TASK: {task}\n\nFACTS (calculated by the app):\n{facts_json}",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.4),
        )
    except Exception as e:                           # model name retired? try the stable one once
        if "not found" in str(e).lower() and model != "gemini-2.5-flash":
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"TASK: {task}\n\nFACTS (calculated by the app):\n{facts_json}",
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.4),
            )
        else:
            raise
    return (resp.text or "").strip()


def explain(task, facts, fallback_text, title):
    """AI explanation card (gold rule). Uses a rule-based sentence if AI is off, has no key, or fails."""
    facts_json = json.dumps(facts, ensure_ascii=False, indent=1)
    key = get_secret("GEMINI_API_KEY")
    text, source = fallback_text, "Calculations only · AI is off"
    if S.use_ai and key:
        try:
            with st.spinner("Explaining…"):
                out = call_gemini(task, facts_json, key, get_secret("GEMINI_MODEL", "gemini-flash-latest"))
            if out:
                text, source = out, "Explained by Gemini · numbers calculated by the app"
        except Exception as e:
            source = f"AI unavailable ({type(e).__name__}) · showing calculations only"
    elif S.use_ai:
        source = "No Gemini key set · showing calculations only"
    card(f'<div class="ai-head">{icon(I_SPARK, "#B8862B", 14)} {title}</div>'
         f'<p class="ai-text">{text}</p><div class="ai-src">{source}</div>', "card ai")
    with st.expander("What's sent to the AI"):
        st.caption("Only these summary numbers. No names, account numbers or transactions. Nothing is stored.")
        st.code(facts_json, language="json")
    return text


# ═════════════════════════════════════════════════════════════
# 5. CALCULATIONS (fixed rules, recomputed on every interaction)
# ═════════════════════════════════════════════════════════════
committed = S.rent + S.emi + S.sip + S.bills
free = S.salary - committed - S.usual
essential = S.rent + S.emi + S.bills + S.usual            # monthly cost of living (SIPs excluded)
buffer_months = S.savings / essential if essential else 0
net_worth = S.savings + S.invest - S.loans - S.cards
daily_spend = S.usual / 30
next_salary = dt.date(TODAY.year, TODAY.month, min(S.salary_day, 28))
if next_salary <= TODAY:
    next_salary = add_months(next_salary, 1)

goal_months = months_between(TODAY, S.goal_date)
goal_left = max(0, S.goal_cost - S.goal_saved)
need_pm = goal_left / goal_months
pace_months = math.ceil(goal_left / S.goal_monthly) if S.goal_monthly > 0 else None
on_track = S.goal_monthly >= need_pm

SCORE = {"Sell to stop losses": 0, "Wait it out": 1, "Invest more": 2,
         "New to investing": 0, "Some experience": 1, "Experienced": 2,
         "Likely": 0, "Maybe": 1, "Unlikely": 2}
score = SCORE.get(S.q_drop, 1) + SCORE.get(S.q_exp, 1) + SCORE.get(S.q_early, 1)
comfort = "Low" if score <= 2 else ("Medium" if score <= 4 else "High")

MIXES = {"Steady": (70, 20, 10), "Balanced": (40, 50, 10), "Growth": (20, 70, 10)}  # debt, equity, gold %
MIX_COMFORT = {"Steady": "Low", "Balanced": "Medium", "Growth": "High"}
MIX_COLOR = {"Steady": "#3987e5", "Balanced": "#d95926", "Growth": "#199e70"}       # colour-blind checked on white
WEAK_YEAR = (3.0, -20.0, -5.0)                                                     # bad-year returns %
choice = S.choice if S.choice in MIXES else "Balanced"


def mix_stats(name):
    d, e, g = MIXES[name]
    exp_r = (d * S.r_debt + e * S.r_equity + g * S.r_gold) / 10000
    low_r = (d * S.r_debt + e * 4.0 + g * 4.0) / 10000
    high_r = (d * S.r_debt + e * 15.0 + g * 10.0) / 10000
    n_exp = months_to_goal(S.goal_saved, S.goal_monthly, S.goal_cost, exp_r)
    n_low = months_to_goal(S.goal_saved, S.goal_monthly, S.goal_cost, low_r)
    n_high = months_to_goal(S.goal_saved, S.goal_monthly, S.goal_cost, high_r)
    order = ["Low", "Medium", "High"]
    return {
        "debt": d, "equity": e, "gold": g, "exp_r": exp_r, "months": n_exp, "n_low": n_low, "n_high": n_high,
        "goal_date": fmt_month(add_months(TODAY, n_exp)) if n_exp else "50+ years",
        "range": (f"{fmt_month(add_months(TODAY, n_high))} – {fmt_month(add_months(TODAY, n_low))}"
                  if n_low and n_high else "—"),
        "dip": round((d * WEAK_YEAR[0] + e * WEAK_YEAR[1] + g * WEAK_YEAR[2]) / 100, 1),
        "fits": order.index(MIX_COMFORT[name]) <= order.index(comfort),
        "short_risk": goal_months <= 36 and e >= 50,
    }


# ═════════════════════════════════════════════════════════════
# 6. CHARTS (Altair, light theme: thin lines, dashed goal line, hover tooltip, direct labels)
# ═════════════════════════════════════════════════════════════
FONT = "Manrope, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"
AXIS = dict(labelColor="#8A8B92", titleColor="#8A8B92", gridColor="#EEEEEA", domainColor="#E8E7E3",
            tickColor="#E8E7E3", labelFont=FONT, labelFontSize=11)
LAKH = "'₹' + format(datum.value / 100000, '.1f') + ' L'"
GOLD, INK3 = "#B8862B", "#8A8B92"


def goal_chart(series, target, target_date, height=260):
    """series = {name: (colour, [balance by month])}. Lines + dashed goal line + target-date line + hover."""
    rows = []
    for name, (_, vals) in series.items():
        for m, v in enumerate(vals):
            d = add_months(TODAY, m)
            rows.append({"series": name, "date": pd.Timestamp(d), "value": v, "amount": short_inr(v),
                         "month": fmt_month(d)})
    df = pd.DataFrame(rows)
    names = list(series)
    color = alt.Color("series:N", scale=alt.Scale(domain=names, range=[series[n][0] for n in names]),
                      legend=alt.Legend(orient="top", title=None, labelColor="#55565E", labelFont=FONT,
                                        labelFontSize=12, symbolType="stroke", symbolStrokeWidth=3))
    x = alt.X("date:T", title=None, axis=alt.Axis(format="%b %y", tickCount=5, **AXIS))
    y = alt.Y("value:Q", title=None, scale=alt.Scale(zero=False, nice=False), axis=alt.Axis(labelExpr=LAKH, tickCount=5, **AXIS))
    hover = alt.selection_point(fields=["date"], nearest=True, on="pointerover", empty=False, clear="pointerout")
    base = alt.Chart(df)
    lines = base.mark_line(strokeWidth=2.5, interpolate="monotone").encode(x=x, y=y, color=color)
    pts = base.mark_point(size=80, filled=True, stroke="#FFFFFF", strokeWidth=2).encode(
        x=x, y=y, color=color, opacity=alt.condition(hover, alt.value(1), alt.value(0)),
        tooltip=[alt.Tooltip("series:N", title="Line"), alt.Tooltip("month:N", title="Month"),
                 alt.Tooltip("amount:N", title="Saved")]).add_params(hover)
    rule = base.mark_rule(color="#C9C8C3").encode(x=x).transform_filter(hover)
    gdf = pd.DataFrame({"v": [target], "t": [f"Goal {short_inr(target)}"]})
    goal = alt.Chart(gdf).mark_rule(color=GOLD, strokeDash=[5, 4], strokeWidth=1.5).encode(y="v:Q")
    goal_txt = alt.Chart(gdf).mark_text(align="left", dx=4, dy=-8, color=GOLD, font=FONT,
                                        fontSize=11, fontWeight=700).encode(y="v:Q", x=alt.value(0), text="t:N")
    tdf = pd.DataFrame({"d": [pd.Timestamp(target_date)], "t": ["Target"]})
    tdate = alt.Chart(tdf).mark_rule(color="#B9B9B4", strokeDash=[2, 3]).encode(x="d:T")
    tdate_txt = alt.Chart(tdf).mark_text(align="left", dx=4, y=8, color=INK3, font=FONT,
                                         fontSize=11).encode(x="d:T", text="t:N")
    chart = (goal + goal_txt + tdate + tdate_txt + lines + rule + pts).properties(height=height).configure_view(
        strokeWidth=0).configure(background="transparent", padding={"left": 4, "right": 12, "top": 4, "bottom": 4})
    st.altair_chart(chart, width="stretch")


def range_chart(stats, target_date, height=200):
    """When each mix could reach the goal: bar = likely range (good to weak markets), dot = expected."""
    rows = []
    for n, s in stats.items():
        if not (s["months"] and s["n_low"] and s["n_high"]):
            continue
        rows.append({"mix": n, "start": pd.Timestamp(add_months(TODAY, s["n_high"])),
                     "end": pd.Timestamp(add_months(TODAY, s["n_low"])),
                     "mid": pd.Timestamp(add_months(TODAY, s["months"])),
                     "expected": s["goal_date"], "range": s["range"]})
    if not rows:
        return
    df = pd.DataFrame(rows)
    names = list(stats)
    y = alt.Y("mix:N", sort=names, title=None, axis=alt.Axis(labelColor="#55565E", labelFont=FONT, labelFontWeight=600,
                                                              labelFontSize=12, domain=False, ticks=False, labelPadding=10))
    color = alt.Color("mix:N", scale=alt.Scale(domain=names, range=[MIX_COLOR[n] for n in names]), legend=None)
    tip = [alt.Tooltip("mix:N", title="Mix"), alt.Tooltip("expected:N", title="Expected"),
           alt.Tooltip("range:N", title="Likely range")]
    bars = alt.Chart(df).mark_bar(height=14, cornerRadius=7, opacity=0.3).encode(
        x=alt.X("start:T", title=None, axis=alt.Axis(format="%b %y", tickCount=6, **AXIS)), x2="end:T",
        y=y, color=color, tooltip=tip)
    dots = alt.Chart(df).mark_point(size=160, filled=True, stroke="#FFFFFF", strokeWidth=2, opacity=1).encode(
        x="mid:T", y=y, color=color, tooltip=tip)
    labels = alt.Chart(df).mark_text(align="left", dx=12, font=FONT, fontSize=11, fontWeight=600, color="#55565E").encode(
        x="mid:T", y=y, text="expected:N")
    tdf = pd.DataFrame({"d": [pd.Timestamp(target_date)], "t": ["Your target"]})
    rule = alt.Chart(tdf).mark_rule(color=GOLD, strokeDash=[5, 4], strokeWidth=1.5).encode(x="d:T")
    txt = alt.Chart(tdf).mark_text(align="left", dx=5, y=4, baseline="top", color=GOLD, font=FONT,
                                   fontSize=11, fontWeight=700).encode(x="d:T", text="t:N")
    ch = (rule + txt + bars + dots + labels).properties(height=height).configure_view(strokeWidth=0).configure(
        background="transparent", padding={"left": 4, "right": 12, "top": 4, "bottom": 4})
    st.altair_chart(ch, width="stretch")


# ═════════════════════════════════════════════════════════════
# 7. TOP BAR (logo, step progress, AI toggle) + STEP TABS
# ═════════════════════════════════════════════════════════════
def progress_html():
    out = []
    for i, name in enumerate(STEPS, start=1):
        cls = "now" if i == S.step else ("done" if i < S.step else "")
        inner = icon(I_CHECK, "#14213D", 12) if i < S.step else str(i)
        out.append(f'<div class="st {cls}"><span class="n">{inner}</span><span class="l">{name}</span></div>')
        if i < len(STEPS):
            out.append(f'<div class="ln {"done" if i < S.step else ""}"></div>')
    return '<div class="steps">' + "".join(out) + '</div>'


t1, t2 = st.columns([4, 1], vertical_alignment="center")
t1.markdown('<div class="topbar"><div class="logo"><div class="mark"></div><div class="word">White<b>.</b></div>'
            '<div class="tag">Your money, nothing hidden</div></div>'
            + (progress_html() if S.step > 0 else "") + '</div>', unsafe_allow_html=True)
t2.toggle("AI explanations", key="use_ai", help="Turn off to see calculations only.")
if S.step > 0:
    if S.nav not in STEPS:
        S.nav = STEPS[S.step - 1]
    st.segmented_control("Steps", STEPS, key="nav", on_change=nav_changed, label_visibility="collapsed",
                         format_func=lambda n: f"{STEPS.index(n) + 1}  {n}")


def nav_buttons(back, nxt, nxt_label):
    b1, b2 = st.columns([1, 1.6])
    b1.button("← Back", width="stretch", on_click=go, args=(back,), key=f"back{S.step}")
    b2.button(nxt_label, type="primary", width="stretch", on_click=go, args=(nxt,), key=f"next{S.step}")


def title(text, lede):
    st.markdown(f'<h2>{text}</h2><p class="lede">{lede}</p>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# 8. STEP 0: SALARY DAY WELCOME
# ═════════════════════════════════════════════════════════════
if S.step == 0:
    left, right = st.columns([1.1, 1], gap="large")
    with left:
        st.markdown(f'<div class="cap" style="margin-top:40px;font-weight:600">{TODAY.strftime("%A, %d %B")}</div>'
                    '<h1 class="hero-title">Salary\'s in.<br><span class="dim">Let\'s make it count.</span></h1>'
                    '<p style="color:#55565E;font-size:16.5px;line-height:1.6;max-width:460px;margin-bottom:22px">A 10-minute check-in '
                    'that answers <b style="color:#111114">"Am I on track for my goal, and what should I do with this '
                    'month\'s money?"</b> Then test a decision before you make it.</p>', unsafe_allow_html=True)
        st.button("Start check-in", type="primary", on_click=go, args=(1,))
        st.markdown(f'<div class="cap" style="margin-top:16px;display:flex;gap:8px;align-items:center">{icon(I_LOCK, "#8A8B92", 14)}'
                    'No bank login · no SMS reading · nothing stored · you make every decision</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div style="height:34px"></div>', unsafe_allow_html=True)
        card(f'<div class="row"><span class="k">Free to use this month</span><span class="pill gold">Sample</span></div>'
             f'<div class="num xl" style="margin-top:8px">{inr(free)}</div>'
             + bar3(committed, S.usual, max(free, 0), SPLIT, "20px 0 12px") +
             f'<div class="legend"><span><i style="background:{SPLIT[0]}"></i>Committed <b>{inr(committed)}</b></span>'
             f'<span><i style="background:{SPLIT[1]}"></i>Everyday <b>{inr(S.usual)}</b></span>'
             f'<span><i style="background:{SPLIT[2]}"></i>Free <b>{inr(free)}</b></span></div>')
        st.markdown('<div class="grid2">' + "".join(
            f'<div class="step-tile"><b>Step {i + 1}</b><div>{s}</div></div>'
            for i, s in enumerate(STEPS)) + '</div>', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
# 9. STEP 1: WHERE I STAND
# ═════════════════════════════════════════════════════════════
elif S.step == 1:
    title("Where I stand", f"This month's picture, salary to salary. Next salary {next_salary.strftime('%d %b')}.")
    buf_ok = buffer_months >= 3
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="k" style="padding:6px 0 0">Your monthly numbers</div>', unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["Income", "Commitments", "Have & owe"])
            with tab1:
                st.number_input("Take-home salary (₹/month)", min_value=0, step=5000, key="salary")
                st.number_input("Salary day (date of month)", min_value=1, max_value=31, step=1, key="salary_day",
                                help="Your check-in runs salary to salary.")
                st.number_input("Usual everyday spending (₹/month)", min_value=0, step=1000, key="usual",
                                help="Food, travel, shopping. A rough 3-month average is enough.")
            with tab2:
                c1, c2 = st.columns(2)
                c1.number_input("Rent", min_value=0, step=1000, key="rent")
                c2.number_input("Loan EMIs", min_value=0, step=1000, key="emi")
                c1, c2 = st.columns(2)
                c1.number_input("SIPs running", min_value=0, step=1000, key="sip")
                c2.number_input("Insurance & bills", min_value=0, step=500, key="bills")
            with tab3:
                c1, c2 = st.columns(2)
                c1.number_input("Savings & FDs", min_value=0, step=10000, key="savings")
                c2.number_input("Investments", min_value=0, step=10000, key="invest", help="MFs, stocks, PF, NPS…")
                c1, c2 = st.columns(2)
                c1.number_input("Loans outstanding", min_value=0, step=10000, key="loans")
                c2.number_input("Credit card dues", min_value=0, step=1000, key="cards")
        if free <= 0:
            st.error("Commitments and usual spending are more than your salary this month.")
    with right:
        card(f'<div class="row"><span class="k">Free this month</span><span class="cap">of {inr(S.salary)} take-home</span></div>'
             f'<div class="num xl" style="margin-top:8px">{inr(free)}</div>'
             + bar3(committed, S.usual, max(free, 0), SPLIT, "20px 0 12px") +
             f'<div class="legend"><span><i style="background:{SPLIT[0]}"></i>Committed <b>{inr(committed)}</b></span>'
             f'<span><i style="background:{SPLIT[1]}"></i>Everyday <b>{inr(S.usual)}</b></span>'
             f'<span><i style="background:{SPLIT[2]}"></i>Free <b>{inr(free)}</b></span></div>')
        st.markdown(
            '<div class="kpis">'
            f'<div class="kpi"><div class="ic">{icon(I_CAL)}</div><div class="k">Everyday budget</div>'
            f'<div class="num md">{inr(daily_spend)}<span class="u">/day</span></div><div class="cap">till {next_salary.strftime("%d %b")}</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_TREND)}</div><div class="k">Net worth</div>'
            f'<div class="num md">{short_inr(net_worth)}</div><div class="cap">after loans and dues</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_WALLET)}</div><div class="k">Committed</div>'
            f'<div class="num md">{inr(committed)}</div><div class="cap">rent, EMIs, SIPs, bills</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_SHIELD)}</div><div class="k">Investments</div>'
            f'<div class="num md">{short_inr(S.invest)}</div><div class="cap">MFs, stocks, PF, NPS</div></div>'
            '</div>', unsafe_allow_html=True)
        card('<div class="gauge">'
             + gauge(buffer_months, 6, 3, "#1F8A5B" if buf_ok else "#B4462B", label=f"{buffer_months:.1f}", sub="months")
             + f'<div><div class="row" style="justify-content:flex-start;gap:10px"><span class="k">Emergency buffer</span>'
               f'<span class="pill {"ok" if buf_ok else "warn"}">{"Healthy" if buf_ok else "Thin"}</span></div>'
               f'<div class="cap" style="margin-top:8px;max-width:300px">Savings cover {buffer_months:.1f} months of rent, EMIs, bills and everyday '
               f'spending. The dotted mark is 3 months, the usual minimum; the dial runs to 6.</div></div></div>')
    explain(
        "Explain this person's position this month in 2-3 sentences: what is free, how healthy the "
        "emergency buffer is, and one thing to keep in mind.",
        {"take_home_salary": inr(S.salary), "committed": inr(committed), "usual_spending": inr(S.usual),
         "free_this_month": inr(free), "emergency_buffer_months": round(buffer_months, 1),
         "investments": short_inr(S.invest), "loans_outstanding": short_inr(S.loans), "net_worth": short_inr(net_worth)},
        f"You have {inr(free)} free this month after commitments and usual spending. Your savings cover about "
        f"{buffer_months:.1f} months of living costs"
        + (", below the common 3–6 month cushion, so topping it up may come first." if not buf_ok
           else ", a healthy cushion."),
        "WHERE YOU STAND")
    nav_buttons(0, 2, "Set a goal")


# ═════════════════════════════════════════════════════════════
# 10. STEP 2: SET A GOAL
# ═════════════════════════════════════════════════════════════
elif S.step == 2:
    title("Set a goal", "One thing you are saving for. We check whether this month's amount gets you there in time.")
    pct = min(100, S.goal_saved / S.goal_cost * 100) if S.goal_cost else 0
    reach = add_months(TODAY, pace_months) if pace_months else None
    delay = (pace_months - goal_months) if pace_months else None
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        with st.container(border=True):
            st.pills("What are you saving for?", ["Car", "Bike", "House", "Trip", "Gadget", "Wedding", "Other"],
                     key="goal_type")
            st.text_input("Name it", key="goal_name")
            c1, c2 = st.columns(2)
            c1.number_input("Cost (₹)", min_value=0, step=10000, key="goal_cost")
            c2.date_input("When do you want it?", min_value=add_months(TODAY, 1), key="goal_date")
            c1, c2 = st.columns(2)
            c1.number_input("Already saved (₹)", min_value=0, step=10000, key="goal_saved")
            c2.number_input("Put aside (₹/month)", min_value=0, step=1000, key="goal_monthly",
                            help=f"You have {inr(free)} free this month.")
            if S.goal_monthly > free > 0:
                st.warning(f"That's more than the {inr(free)} you have free this month.")
    with right:
        status_color = "#1F8A5B" if on_track else "#B4462B"
        card(f'<div class="gauge">{ring(pct / 100, status_color, size=116, stroke=11, label=f"{pct:.0f}%", sub="saved")}'
             f'<div style="flex:1;min-width:0"><div class="row"><div class="k" style="display:flex;align-items:center;gap:7px">'
             f'{icon(GOAL_ICONS.get(S.goal_type or "Other", GOAL_ICONS["Other"]), "#55565E", 15)}{S.goal_type or "Goal"}</div>'
             f'<span class="pill {"ok" if on_track else "warn"}">{"On track" if on_track else "Behind"}</span></div>'
             f'<div class="num lg" style="margin-top:4px;font-size:26px">{S.goal_name}</div>'
             f'<div class="cap" style="margin-top:4px">{short_inr(S.goal_saved)} of {short_inr(S.goal_cost)} saved · target {fmt_month(S.goal_date)}</div></div></div>'
             f'<div class="hair"></div><div class="grid3">'
             f'<div><div class="k">Needed</div><div class="num md">{inr(need_pm)}</div><div class="cap">per month</div></div>'
             f'<div><div class="k">You put aside</div><div class="num md">{inr(S.goal_monthly)}</div><div class="cap">per month</div></div>'
             f'<div><div class="k">You reach it</div><div class="num md">{fmt_month(reach) if reach else "—"}</div>'
             f'<div class="cap {"warn" if delay and delay > 0 else "good"}" style="font-weight:700">'
             f'{f"{delay} months late" if delay and delay > 0 else "on time"}</div></div></div>')
        with st.container(border=True):
            st.markdown('<div class="k" style="padding:6px 0 0">Your pace vs what\'s needed</div>'
                        '<div class="cap">Saving only, no growth. The next step adds investing.</div>', unsafe_allow_html=True)
            horizon = min(120, max(goal_months, pace_months or goal_months) + 2)
            goal_chart({"Your pace": ("#3987e5", path(S.goal_saved, S.goal_monthly, 0, horizon)),
                        "Needed pace": ("#d95926", path(S.goal_saved, need_pm, 0, min(goal_months, 120)))},
                       S.goal_cost, S.goal_date, height=240)
    facts = {"goal": S.goal_name, "cost": inr(S.goal_cost), "already_saved": inr(S.goal_saved),
             "target_date": fmt_month(S.goal_date), "months_left": goal_months, "needed_per_month": inr(need_pm),
             "put_aside_per_month": inr(S.goal_monthly), "free_this_month": inr(free),
             "reached_at_this_pace_without_growth": fmt_month(reach) if reach else "never",
             "status": "on track" if on_track else "behind"}
    fb = (f"Putting aside {inr(S.goal_monthly)} a month gets you to {S.goal_name} by about {fmt_month(reach)}, "
          f"on or before your target." if on_track and reach else
          f"You need about {inr(need_pm)} a month to reach {S.goal_name} by {fmt_month(S.goal_date)}. At "
          f"{inr(S.goal_monthly)} a month you'd get there around {fmt_month(reach) if reach else 'much later'}"
          + (f", about {delay} months late" if delay and delay > 0 else "")
          + ". The next step shows how investing the money changes this.")
    explain("Explain in 2-3 sentences whether the person is on track for this goal and why, and what the gap "
            "means in months or rupees.", facts, fb, "AM I ON TRACK?")
    nav_buttons(1, 3, "See investment options")


# ═════════════════════════════════════════════════════════════
# 11. STEP 3: INVESTMENT OPTIONS (illustrative mixes; the user chooses)
# ═════════════════════════════════════════════════════════════
elif S.step == 3:
    title("Investment options", f"Three illustrative mixes for {inr(S.goal_monthly)} a month. You choose; nothing is recommended.")
    stats = {n: mix_stats(n) for n in MIXES}
    left, right = st.columns([1, 1.5], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="k" style="padding:6px 0 4px">Your comfort with ups and downs</div>', unsafe_allow_html=True)
            st.segmented_control("If your investments fell 15% in a year, you would…",
                                 ["Sell to stop losses", "Wait it out", "Invest more"], key="q_drop")
            st.segmented_control("Your investing experience", ["New to investing", "Some experience", "Experienced"], key="q_exp")
            st.segmented_control("Could you need this money earlier than planned?", ["Likely", "Maybe", "Unlikely"], key="q_early")
            st.markdown(f'<div class="hair" style="margin:10px 0"></div><div class="row"><span class="k">Stated comfort</span>'
                        f'<span class="pill navy">{comfort}</span></div>'
                        f'<div class="cap" style="margin-top:6px;padding-bottom:6px">Goal is {goal_months} months away</div>', unsafe_allow_html=True)
        with st.expander("Assumptions (edit them)"):
            st.caption("Illustrative long-run yearly returns, not predictions. Weak year: debt +3%, equity −20%, "
                       "gold −5%. Ranges use equity at 4%–15%.")
            c1, c2, c3 = st.columns(3)
            c1.number_input("Debt %", 0.0, 20.0, step=0.5, key="r_debt")
            c2.number_input("Equity %", 0.0, 25.0, step=0.5, key="r_equity")
            c3.number_input("Gold %", 0.0, 20.0, step=0.5, key="r_gold")
    with right:
        with st.container(border=True):
            st.markdown(f'<div class="k" style="padding:6px 0 0">When could {S.goal_name} happen?</div>'
                        '<div class="cap">Dot = expected · bar = likely range from weak to strong markets · dashed line = your target</div>',
                        unsafe_allow_html=True)
            range_chart(stats, S.goal_date)
    cols = st.columns(3)
    for col, n in zip(cols, MIXES):
        s = stats[n]
        sel = n == choice
        with col:
            st.markdown(
                f'<div class="opt{" sel" if sel else ""}">'
                f'<div class="name"><i style="background:{MIX_COLOR[n]}"></i>{n}</div>'
                + bar3(s["debt"], s["equity"], s["gold"], ALLOC, "14px 0 8px") +
                f'<div class="cap">Debt {s["debt"]} · Equity {s["equity"]} · Gold {s["gold"]}</div>'
                f'<div style="margin-top:10px"><div class="kv"><span>Goal reached</span><b>{s["goal_date"]}</b></div>'
                f'<div class="kv"><span>Likely range</span><b style="font-size:12px">{s["range"]}</b></div>'
                f'<div class="kv"><span>Weak-year dip</span><b>{s["dip"]}%</b></div></div>'
                f'<div class="foot"><span class="pill {"ok" if s["fits"] else "warn"}">'
                f'{"Fits comfort" if s["fits"] else "Above comfort"}</span>'
                + ('<div class="cap warn" style="margin-top:10px;font-weight:600">Short timeline: could be down when you need it.</div>'
                   if s["short_risk"] else "") + '</div></div>', unsafe_allow_html=True)
            st.button("Chosen ✓" if sel else f"Choose {n}", key=f"pick_{n}", width="stretch",
                      type="primary" if sel else "secondary", on_click=pick, args=(n,))
    explain("Compare the three mixes for this goal in 3-4 sentences: reaching the goal sooner vs the size of a "
            "bad-year dip vs the timeline. Mention the stated comfort. Do not pick one.",
            {"goal": S.goal_name, "target_date": fmt_month(S.goal_date), "months_left": goal_months,
             "monthly_amount": inr(S.goal_monthly), "stated_comfort": comfort,
             "emergency_buffer_months": round(buffer_months, 1),
             "options": {n: {"mix": f"debt {s['debt']}%, equity {s['equity']}%, gold {s['gold']}%",
                             "goal_reached": s["goal_date"], "likely_range": s["range"], "weak_year_dip_pct": s["dip"],
                             "fits_comfort": s["fits"], "short_timeline_risk": s["short_risk"]} for n, s in stats.items()}},
            f"Steady is the smoothest ride (about {stats['Steady']['dip']}% in a weak year) and reaches the goal around "
            f"{stats['Steady']['goal_date']}. Growth could get there around {stats['Growth']['goal_date']} but could fall "
            f"about {abs(stats['Growth']['dip'])}% in a bad year"
            + (", which matters with a short timeline." if goal_months <= 36 else ".")
            + f" Balanced sits in between. Your stated comfort is {comfort.lower()}.",
            "COMPARING YOUR OPTIONS")
    st.markdown('<div class="cap" style="margin-bottom:12px">Illustrative mixes for your own decision. Not investment '
                'advice; no specific funds or stocks are suggested.</div>', unsafe_allow_html=True)
    nav_buttons(2, 4, f"Plan with {choice}")


# ═════════════════════════════════════════════════════════════
# 12. STEP 4: MY PLAN + "WHAT IF…?" DECISION CHECK
# ═════════════════════════════════════════════════════════════
elif S.step == 4:
    s = mix_stats(choice)
    left_after = free - S.goal_monthly
    title("Your plan for this month", "What you decided, in one place. Then test a decision before you make it.")
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        card(f'<div class="row"><span class="k">{S.goal_name}</span><span class="pill" style="color:{MIX_COLOR[choice]}">{choice} mix</span></div>'
             f'<div class="num xl" style="margin-top:8px">{inr(S.goal_monthly)}<span class="u">/month</span></div>'
             + bar3(s["debt"], s["equity"], s["gold"], ALLOC, "20px 0 10px") +
             f'<div class="legend"><span><i style="background:{ALLOC[0]}"></i>Debt <b>{s["debt"]}%</b></span>'
             f'<span><i style="background:{ALLOC[1]}"></i>Equity <b>{s["equity"]}%</b></span>'
             f'<span><i style="background:{ALLOC[2]}"></i>Gold <b>{s["gold"]}%</b></span></div>'
             f'<div class="hair"></div>'
             f'<div class="kv"><span>Expected to reach</span><b>{s["goal_date"]}</b></div>'
             f'<div class="kv"><span>Your target</span><b>{fmt_month(S.goal_date)}</b></div>'
             f'<div class="kv"><span>Likely range</span><b>{s["range"]}</b></div>'
             f'<div class="kv"><span>Weak-year dip</span><b>about {s["dip"]}%</b></div>'
             f'<div class="kv"><span>Left free this month</span><b>{inr(left_after)}</b></div>'
             f'<div class="kv"><span>Next check-in</span><b>{next_salary.strftime("%d %b %Y")}</b></div>')
        plan = explain(
            "Write a short, encouraging plan summary (3 sentences) the user can save: what they chose, the monthly "
            "amount, when they may reach the goal, and one thing to check at the next check-in.",
            {"goal": S.goal_name, "chosen_mix": choice, "monthly_amount": inr(S.goal_monthly),
             "expected_goal_date": s["goal_date"], "likely_range": s["range"], "target_date": fmt_month(S.goal_date),
             "left_free_after_goal": inr(left_after), "emergency_buffer_months": round(buffer_months, 1),
             "next_check_in": next_salary.strftime("%d %b %Y")},
            f"You chose the {choice} mix for {S.goal_name}: {inr(S.goal_monthly)} a month, reaching it around "
            f"{s['goal_date']} (likely {s['range']}). That leaves {inr(left_after)} free this month. At your next "
            f"check-in on {next_salary.strftime('%d %b')}, see whether spending and your buffer still support this.",
            "YOUR PLAN, IN WORDS")

    with right:
        # "What if…?": test a decision before making it
        with st.container(border=True):
            st.markdown('<h3 style="margin:6px 0 2px;font-size:22px">What if…?</h3>'
                        '<div class="cap" style="margin-bottom:10px">Test a decision before you make it.</div>',
                        unsafe_allow_html=True)
            st.segmented_control("Decision", ["One-off spend", "Change monthly amount"], key="wi_kind",
                                 label_visibility="collapsed")
            if S.wi_kind != "Change monthly amount":
                c1, c2 = st.columns(2)
                c1.number_input("Amount (₹)", min_value=0, step=1000, key="wi_amount",
                                help="e.g. a phone, trip or repair")
                c2.radio("Paid from", ["This month's goal money", "Emergency savings"], key="wi_from")
            else:
                st.number_input("Change per month (₹, minus to reduce)", step=1000, key="wi_monthly")

        exp_r = s["exp_r"]
        after_saved, after_monthly, after_savings = S.goal_saved, S.goal_monthly, S.savings
        if S.wi_kind != "Change monthly amount":
            if S.wi_from == "This month's goal money":
                after_saved = max(0, S.goal_saved - S.wi_amount)
            else:
                after_savings = max(0, S.savings - S.wi_amount)
            decision = f"spend {inr(S.wi_amount)} this month, paid from {S.wi_from.lower()}"
        else:
            after_monthly = max(0, S.goal_monthly + S.wi_monthly)
            decision = (f"{'increase' if S.wi_monthly >= 0 else 'reduce'} the monthly goal amount by "
                        f"{inr(abs(S.wi_monthly))} to {inr(after_monthly)}")
        before_n = months_to_goal(S.goal_saved, S.goal_monthly, S.goal_cost, exp_r)
        after_n = months_to_goal(after_saved, after_monthly, S.goal_cost, exp_r)
        after_buffer = after_savings / essential if essential else 0
        before_date = fmt_month(add_months(TODAY, before_n)) if before_n else "50+ years"
        after_date = fmt_month(add_months(TODAY, after_n)) if after_n else "not reached"
        shift = (after_n - before_n) if (after_n and before_n) else None
        if shift is None:
            shift_txt, shift_cls = "goal not reached", "warn"
        elif shift > 0:
            shift_txt, shift_cls = f"{shift} month{'s' if shift != 1 else ''} later", "warn"
        elif shift < 0:
            shift_txt, shift_cls = f"{-shift} month{'s' if shift != -1 else ''} sooner", "ok"
        else:
            shift_txt, shift_cls = "no change", ""
        buf_delta = after_buffer - buffer_months
        buf_txt = "no change" if abs(buf_delta) < 0.05 else f"{buf_delta:+.1f} months"
        buf_cls = "warn" if buf_delta < -0.04 else ("ok" if buf_delta > 0.04 else "")
        card(f'<div class="row"><span class="k">{S.goal_name} reached</span><span class="pill {shift_cls}">{shift_txt}</span></div>'
             f'<div class="tl"><div class="d"><small>Before</small>{before_date}</div><div class="line"></div>'
             f'<div class="d {"warn" if shift_cls == "warn" else ("good" if shift_cls == "ok" else "")}"><small>After</small>{after_date}</div></div>'
             f'<div class="hair"></div>'
             f'<div class="row"><span class="k">Emergency buffer</span><span class="pill {buf_cls}">{buf_txt}</span></div>'
             f'<div class="tl"><div class="d"><small>Before</small>{buffer_months:.1f} mo</div><div class="line"></div>'
             f'<div class="d {"warn" if buf_cls == "warn" else ""}"><small>After</small>{after_buffer:.1f} mo</div></div>')
        explain("Explain in 2-3 sentences what this decision does to the goal date and the emergency buffer, and "
                "the trade-off. Do not tell the user whether to do it.",
                {"decision": decision, "goal": S.goal_name, "mix": choice, "goal_date_before": before_date,
                 "goal_date_after": after_date, "change": shift_txt,
                 "buffer_months_before": round(buffer_months, 1), "buffer_months_after": round(after_buffer, 1)},
                f"If you {decision}, {S.goal_name} moves from {before_date} to {after_date} ({shift_txt})"
                + (f", and your buffer goes from {buffer_months:.1f} to {after_buffer:.1f} months. "
                   if abs(buf_delta) >= 0.05 else ", and your buffer stays the same. ")
                + "Whether that trade-off is worth it is your call.",
                "WHAT THIS DECISION DOES")

    summary = (f"White · monthly plan · {TODAY.strftime('%d %b %Y')}\n\n"
               f"Goal: {S.goal_name} ({inr(S.goal_cost)}, target {fmt_month(S.goal_date)})\n"
               f"Monthly amount: {inr(S.goal_monthly)}\n"
               f"Chosen mix: {choice} (debt {s['debt']}%, equity {s['equity']}%, gold {s['gold']}%)\n"
               f"Expected: {s['goal_date']} · likely range {s['range']}\n"
               f"Free this month after goal: {inr(left_after)}\nEmergency buffer: {buffer_months:.1f} months\n"
               f"Next check-in: {next_salary.strftime('%d %b %Y')}\n\n{plan}\n\n"
               "Illustrative figures based on your inputs and editable assumptions. Not investment advice. "
               "You made this decision.\n")
    st.download_button("Download my plan", summary, file_name="white-plan.txt", width="stretch",
                       help="A plain-text copy of this page. Nothing is stored by the app.")
    d1, d2 = st.columns(2)
    d1.button("← Change something", width="stretch", on_click=go, args=(3,), key="back4")
    d2.button("Start over", width="stretch", on_click=go, args=(0,), key="restart")

st.markdown('<div class="footer">Read-only · nothing stored · you make every decision · '
            'DPM 2026 · Group 9 prototype</div>', unsafe_allow_html=True)
