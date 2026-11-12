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
import html as html_lib
import json
import re
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

:root { --bg:#F2F4F8; --surface:#FFFFFF; --line:#E3E7EE; --line-2:#D3D9E3;
        --ink:#111114; --ink-2:#55565E; --ink-3:#8A8B92;
        --accent:#14213D; --accent-soft:#E9EDF5;
        --gold:#B8862B; --gold-tint:#F3E7C9; --gold-soft:#FBF6EA;
        --good:#1F8A5B; --good-bg:#E7F5EE; --warn:#B4462B; --warn-bg:#FBECE7;
        --shadow: 0 1px 2px rgba(16,17,20,.04), 0 8px 24px rgba(16,17,20,.06);
        --sans: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
        --display: 'Sora', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; }

html, body, .stApp, p, label, input, textarea, select, button { font-family: var(--sans); }
.stApp { background: radial-gradient(1100px 520px at 88% -8%, #D9E1F0 0%, rgba(217,225,240,0) 62%), radial-gradient(900px 420px at -10% 0%, #E7ECF5 0%, rgba(231,236,245,0) 60%), var(--bg); background-attachment: fixed; color: var(--ink); }
.block-container { max-width: 1120px; padding-top: 0.6rem; padding-bottom: 3rem; }
@media (min-width: 1440px) { .block-container { max-width: 1280px; } }
@media (min-width: 1760px) { .block-container { max-width: 1400px; } }
[data-testid="stButtonGroup"] > div:has(> button[data-variant="pills"]) { flex-wrap: wrap !important; overflow: visible !important; row-gap: 6px; }
.gcard .gtop { display:flex; gap:16px; align-items:center; margin:10px 0 6px; }
.gcard .gline { display:flex; justify-content:space-between; gap:10px; font-size:14.5px; color: var(--ink-2); padding:5px 0; border-top:1px solid var(--line); }
.gcard .gline b { color: var(--ink); font-variant-numeric: tabular-nums; }
.gcard svg.spark { width:100%; height:86px; display:block; margin-top:6px; }
header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stElementToolbar"] { display: none; }
h1, h2, h3, h4 { font-family: var(--display) !important; letter-spacing: -0.4px; color: var(--ink); font-weight: 600 !important; }
h2 { font-size: 28px !important; margin: 4px 0 2px !important; padding: 0 !important; }
.lede { color: var(--ink-2); font-size:16.5px; margin: 0 0 18px; }
p, li { color: var(--ink); }

/* ── top bar: logo, step progress, AI toggle ───────────────────────── */
div[data-testid="stHorizontalBlock"]:has(.topbar) { align-items: center; flex-wrap: nowrap !important; gap: 8px;
  padding: 10px 0 10px; border-bottom: 1px solid var(--line); margin-bottom: 14px; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"] { min-width: 0 !important; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"]:last-child { flex: 0 0 auto !important; width: auto !important; }
div[data-testid="stHorizontalBlock"]:has(.topbar) > div[data-testid="stColumn"]:first-child { flex: 1 1 auto !important; }
.topbar { display:flex; align-items:center; gap:22px; min-height:36px; }
.logo { display:flex; align-items:center; gap:10px; text-decoration:none; }
.logo .mark { width:34px; height:34px; border-radius:8px; background:#fff; border:1px solid var(--line-2);
  box-shadow: 0 1px 2px rgba(16,17,20,.06); position:relative; flex:0 0 auto; }
.logo .mark::after { content:""; position:absolute; width:7px; height:7px; border-radius:50%; background:var(--accent);
  right:6px; bottom:6px; }
.logo .word { font-family: var(--display); font-weight:700; font-size:27px; letter-spacing:-.4px; color:var(--ink); }
.logo .word b { color: var(--accent); }
.logo .tag { font-size:14px; color: var(--ink-3); margin-left:2px; white-space:nowrap; }
.steps { display:none; align-items:center; gap:6px; }
.steps .st { display:flex; align-items:center; gap:7px; font-size:14px; color: var(--ink-3); font-weight:600; white-space:nowrap; }
.steps .st .n { width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-size:12.5px; font-weight:700; border:1.5px solid var(--line-2); color: var(--ink-3); background:#fff; flex:0 0 auto; }
.steps .st.done .n { border-color: var(--accent); color: var(--accent); }
.steps .st.now .n { background: var(--accent); border-color: var(--accent); color:#fff; }
.steps .st.now { color: var(--ink); }
.steps .ln { width:22px; height:1px; background: var(--line-2); }
.steps .ln.done { background: var(--accent); }

/* ── cards and type ────────────────────────────────────────────────── */
.card { background: var(--surface); border:1px solid var(--line); border-radius:18px; padding:18px 20px;
        margin-bottom:14px; box-shadow: var(--shadow); animation: rise .18s ease-out both; }
.card.flat { box-shadow:none; }
.card.ai { border-left: 3px solid var(--gold); background: var(--surface); }
.card.hero { background: var(--accent); border-color: var(--accent); color:#fff;
             box-shadow: 0 1px 2px rgba(20,33,61,.2), 0 14px 34px rgba(20,33,61,.22); }
.card.hero .k, .card.hero .cap, .card.hero .legend { color: rgba(255,255,255,.72); }
.card.hero .num, .card.hero .legend b, .card.hero .kv b { color:#fff; }
.card.hero .num .u { color: rgba(255,255,255,.6); }
.card.hero .kv { color: rgba(255,255,255,.72); border-color: rgba(255,255,255,.14); }
.card.hero .hair { background: rgba(255,255,255,.14); }
.card.hero .pill { background: rgba(255,255,255,.12); border-color: transparent; color:#fff; }
.card.hero .pill.gold { background: var(--gold-tint); color: var(--gold); }
.card.hero .delta { display:inline-flex; align-items:center; gap:6px; font-size:14px; font-weight:700; color:#fff;
                    background: rgba(255,255,255,.12); border-radius:999px; padding:4px 10px; margin-top:12px; }
.hist { display:flex; justify-content:space-between; gap:10px; font-size:14.5px; padding:8px 0; border-bottom:1px solid var(--line); color: var(--ink-2); flex-wrap:wrap; }
.hist:last-child { border-bottom:none; }
.hist b { color: var(--ink); font-variant-numeric: tabular-nums; }
@keyframes rise { from { opacity:0; transform: translateY(4px);} to { opacity:1; transform:none;} }
@media (prefers-reduced-motion: reduce) { .card { animation: none; } }
.k { font-size:14.5px; color: var(--ink-2); font-weight:600; }
.cap { font-size:14px; color: var(--ink-3); line-height:1.5; }
.num { font-family: var(--display); font-weight:600; letter-spacing:-1px; line-height:1.05; color: var(--ink);
       font-variant-numeric: tabular-nums; }
.num.xl { font-size:56px; letter-spacing:-2px; } .num.lg { font-size:32px; } .num.md { font-size:22px; letter-spacing:-.5px; }
.num .u { font-size:.4em; font-weight:500; color: var(--ink-3); letter-spacing:0; margin-left:4px; }
.good { color: var(--good) !important; } .warn { color: var(--warn) !important; }
.row { display:flex; justify-content:space-between; align-items:center; gap:10px; }
.pill { display:inline-block; font-size:12.5px; font-weight:700; letter-spacing:.6px; padding:4px 10px; border-radius:999px;
        border:1px solid var(--line-2); color: var(--ink-2); background:#fff; white-space:nowrap; }
.pill.ok { color: var(--good); border-color: transparent; background: var(--good-bg); }
.pill.warn { color: var(--warn); border-color: transparent; background: var(--warn-bg); }
.pill.gold { color: var(--gold); border-color: transparent; background: var(--gold-tint); }
.pill.navy { color:#fff; border-color: transparent; background: var(--accent); }
.hair { height:1px; background: var(--line); margin:16px 0; }

/* stacked bar + legend */
.split { display:flex; height:12px; gap:3px; margin:18px 0 10px; }
.split span { display:block; border-radius:4px; min-width:3px; }
.legend { display:flex; flex-wrap:wrap; gap:8px 18px; font-size:14px; color: var(--ink-2); }
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
.gauge .sub { font-size:12px; fill: var(--ink-3); font-weight:600; }

/* key/value rows, option cards */
.kv { display:flex; justify-content:space-between; gap:8px; font-size:14.5px; padding:7px 0; color: var(--ink-2);
      border-bottom:1px solid var(--line); }
.kv:last-child { border-bottom:none; }
.kv b { color: var(--ink); font-weight:700; text-align:right; font-variant-numeric: tabular-nums; }
.opt { background: var(--surface); border:1px solid var(--line); border-radius:18px; padding:18px 18px 14px; margin-bottom:10px;
       box-shadow: var(--shadow); position:relative; }
.opt { border-top-width:3px; }
.opt.sel { border:2px solid var(--accent); border-top-width:3px; padding:17px 17px 13px; }
.opt .name { font-family: var(--display); font-weight:600; font-size:17px; display:flex; align-items:center; gap:9px; }
.opt .name i { width:10px; height:10px; border-radius:50%; display:inline-block; }
.opt .foot { margin-top:12px; min-height:58px; }

/* what-if timeline */
.tl { display:flex; align-items:center; gap:10px; margin:14px 0 6px; }
.tl .d { font-family: var(--display); font-weight:600; font-size:22px; letter-spacing:-.5px; font-variant-numeric: tabular-nums; white-space:nowrap; }
.tl .d small { display:block; font-family: var(--sans); font-size:13px; color: var(--ink-3); font-weight:600; letter-spacing:0; margin-bottom:2px; }
.tl .line { flex:1; height:2px; background: var(--line-2); position:relative; min-width:30px; }
.tl .line::after { content:""; position:absolute; right:-1px; top:-4px; border:5px solid transparent; border-left:7px solid var(--line-2); }

/* AI card */
.ai-head { display:flex; align-items:center; gap:8px; font-size:12.5px; font-weight:800; letter-spacing:1.1px; color: var(--gold); margin-bottom:10px; }
.ai-text { color: var(--ink); font-size:17px; line-height:1.6; margin:0; }
.ai-src { font-size:13.5px; color: var(--ink-3); margin-top:12px; }

.hero-title { font-size:56px; line-height:1.02; margin:8px 0 18px; letter-spacing:-2px; font-weight:600 !important; }
.hero-title .dim { color: var(--ink-3); }
.step-tile { background: var(--surface); border:1px solid var(--line); border-radius:16px; padding:16px; box-shadow: var(--shadow); }
.step-tile b { font-family: var(--display); color: var(--accent); font-size:13.5px; font-weight:600; }
.step-tile div { font-weight:600; margin-top:6px; font-size:16px; }
.footer { text-align:center; font-size:13.5px; color: var(--ink-3); margin-top:30px; }
.grid2 { display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:12px; }
.grid3 { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:12px; }

/* ── native widgets, restyled ──────────────────────────────────────── */
button[data-testid^="stBaseButton-primary"], div.stDownloadButton > button {
  background: var(--accent) !important; color:#fff !important; border:none !important; border-radius:12px !important;
  font-weight:700 !important; min-height:48px; box-shadow: 0 1px 2px rgba(20,33,61,.2), 0 6px 16px rgba(20,33,61,.18) !important;
  transition: transform .08s ease, box-shadow .08s ease; }
button[data-testid^="stBaseButton-primary"] p, div.stDownloadButton > button p { color:#fff !important; font-weight:700 !important; }
button[data-testid^="stBaseButton-primary"]:hover, div.stDownloadButton > button:hover { background:#1B2C50 !important; }
button[data-testid^="stBaseButton-primary"]:active { transform: translateY(1px); }
button[data-testid="stBaseButton-secondary"] { background:#fff !important; color: var(--ink) !important;
  border:1px solid var(--line-2) !important; border-radius:12px !important; min-height:48px; font-weight:600 !important; }
button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--accent) !important; color: var(--accent) !important; }
button[data-testid="stBaseButton-tertiary"] { color: var(--ink-2) !important; }
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div {
  background:#fff !important; border-color: var(--line-2) !important; border-radius:12px !important; }
div[data-baseweb="input"]:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft); }
[data-testid="stNumberInput"] button { background:#fff !important; border-color: var(--line-2) !important; color: var(--ink) !important; }
[data-testid="stNumberInputStepUp"] svg, [data-testid="stNumberInputStepDown"] svg { color: var(--ink) !important; fill: currentColor !important; }
[data-testid="stTooltipIcon"] button:not([data-testid^="stBaseButton"]) { background: transparent !important; border: 0 !important; box-shadow: none !important; }
[data-testid="stTooltipIcon"] button:not([data-testid^="stBaseButton"]) svg { fill: none !important; color: var(--ink-3) !important; stroke: currentColor; }
[data-testid="stNumberInput"] button:hover, [data-testid="stNumberInput"] button:focus-visible { background: var(--accent-soft) !important; }
[data-testid="stNumberInput"] button:active { background: #DCE1EC !important; }
[data-testid="stNumberInput"] button:hover svg, [data-testid="stNumberInput"] button:active svg { color: var(--accent) !important; }
[data-testid="stWidgetLabel"] p { color: var(--ink-2) !important; font-weight:600 !important; font-size:15px !important; }
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
.st-key-nav button[data-variant="segmented_control"] p { font-size:15px; font-variant-numeric: tabular-nums; }
.st-key-nav button[data-variant="segmented_control"]:hover { color: var(--ink) !important; background: #fff !important; border-color: var(--line) !important; }
.st-key-nav button[data-variant="segmented_control"][aria-checked="true"] { background: var(--accent-soft) !important; border-color: transparent !important; }
.st-key-nav button[data-variant="segmented_control"][aria-checked="true"] p { color: var(--accent) !important; font-weight:700; }
.st-key-nav { margin-bottom: 6px; }
[data-testid="stRadio"] label p { color: var(--ink) !important; font-weight:500 !important; }
.st-key-use_ai label p { color: var(--ink-2) !important; font-weight:600 !important; }
[data-testid="stAlert"] { border-radius:14px; }
[data-testid="stCode"] pre, [data-testid="stCode"] code { background:#F7F7F5 !important; border-radius:10px; font-size:13.5px; }
div[data-testid="stCaptionContainer"] p { color: var(--ink-3) !important; }

/* ── phones ────────────────────────────────────────────────────────── */

/* navy masthead: full-bleed app header with logo, AI switch and steps */
:root { --mw: 1120px; --pl: 80px; }
@media (min-width: 1440px) { :root { --mw: 1280px; } }
@media (min-width: 1760px) { :root { --mw: 1400px; } }
@media (max-width: 760px) { :root { --pl: 16px; } }
.st-key-masthead { background: linear-gradient(115deg, #14213D 0%, #1C2D55 60%, #22376A 100%);
  width: 100vw !important; max-width: 100vw !important; box-sizing: border-box;
  margin: -3.2rem 0 26px calc(50% - 50vw) !important;
  padding: calc(2.6rem - 8px) max(var(--pl), calc((100vw - var(--mw)) / 2 + var(--pl))) 8px !important;
  box-shadow: 0 6px 24px -14px rgba(20,33,61,.55); gap: 2px !important; }
.st-key-masthead .logo .word { color: #FFFFFF !important; }
.st-key-masthead .logo .word b { color: #8FB0FF !important; }
.st-key-masthead .logo .tag { color: #A9B6D3 !important; }
.st-key-masthead .logo .mark { background: #FFFFFF !important; box-shadow: none !important; }
.st-key-masthead .st-key-use_ai label p { color: #DCE3F2 !important; }
.st-key-masthead .st-key-use_ai [data-testid="stTooltipIcon"] svg { color: #A9B6D3 !important; }
.st-key-masthead .st-key-nav button { background: transparent !important; border: 1px solid transparent !important; box-shadow: none !important; border-radius: 999px !important; }
.st-key-masthead .st-key-nav button, .st-key-masthead .st-key-nav button p { color: #C3CCE0 !important; }
.st-key-masthead .st-key-nav button:hover { background: rgba(255,255,255,.08) !important; }
.st-key-masthead .st-key-nav button[aria-checked="true"], .st-key-masthead .st-key-nav button[aria-pressed="true"],
.st-key-masthead .st-key-nav button[kind*="Active"], .st-key-masthead .st-key-nav button[data-testid*="Active"] { background: #FFFFFF !important; }
.st-key-masthead .st-key-nav button[aria-checked="true"] p, .st-key-masthead .st-key-nav button[aria-pressed="true"] p,
.st-key-masthead .st-key-nav button[kind*="Active"] p, .st-key-masthead .st-key-nav button[data-testid*="Active"] p { color: #14213D !important; font-weight: 700 !important; }
.st-key-masthead .st-key-nav [data-testid="stButtonGroup"] > div { flex-wrap: wrap !important; gap: 4px !important; }
.st-key-masthead .st-key-nav { margin-bottom: 0; }
.st-key-masthead .topbar, .st-key-masthead [data-testid="stHorizontalBlock"] { border: 0 !important; box-shadow: none !important; }
.st-key-masthead .steps { display: none !important; }
.st-key-masthead .st-key-use_ai label > div:nth-of-type(1) { background: #6F8FE0 !important; }
.st-key-masthead .st-key-use_ai label > div:nth-of-type(1) > div { background: #FFFFFF !important; }
.st-key-masthead .st-key-use_ai [data-testid="stTooltipIcon"] { display: none !important; }
.st-key-addgoal { border: 1.5px dashed var(--line-2); border-radius: 16px; padding: 20px 20px 16px; background: rgba(255,255,255,.45); }
.st-key-addgoal button { width: 100%; }
.glance { display:grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px; }
.glance .card.mini { padding: 14px 16px; margin: 0; }
.glance .card.mini .num.md { font-size: 22px; margin: 4px 0 2px; }
@media (max-width: 760px) { .glance { grid-template-columns: repeat(3, 1fr); gap: 8px; } .glance .card.mini { padding: 10px 10px; } .glance .card.mini .num.md { font-size: 17px; } .glance .cap { font-size:12.5px; } }
.note-inline { background: var(--accent-soft); color: var(--accent); border-radius: 12px; padding: 10px 14px; font-size:15px; margin: 4px 0 14px; }
.st-key-quick { background: #fff; border: 1px solid var(--line); border-radius: 20px; padding: 16px 18px 14px; margin-top: 12px;
  box-shadow: 0 1px 2px rgba(20,33,61,.04), 0 8px 24px -16px rgba(20,33,61,.18); }
.st-key-quick [data-testid="stButtonGroup"] > div { flex-wrap: wrap !important; row-gap: 6px; }
.quick-out { margin-top: 6px; } .quick-out .pill { margin-bottom: 6px; display: inline-block; }
.quick-out .kv { display:flex; justify-content:space-between; font-size:15px; padding:6px 0; border-top:1px solid var(--line); }
.st-key-assistant { position: fixed !important; right: 24px; bottom: 22px; z-index: 1000; width: auto !important; }
.st-key-assistant button { background: var(--accent) !important; color: #fff !important; border: 0 !important; border-radius: 999px !important;
  padding: 10px 18px !important; box-shadow: 0 10px 28px -10px rgba(20,33,61,.6) !important; }
.st-key-assistant button p, .st-key-assistant button span { color: #fff !important; font-weight: 700 !important; }
[data-testid="stPopoverBody"]:has(form[class*="assist_form"]), [data-testid="stPopoverBody"]:has(.bub) { width: min(430px, 92vw) !important; max-height: 70vh; overflow-y: auto; }
[data-testid="stPopoverBody"] button[data-testid^="stBaseButton-tertiary"] { justify-content: flex-start !important; text-align: left !important;
  border: 1px solid var(--line-2) !important; border-radius: 999px !important; padding: 6px 14px !important; margin: 2px 0 !important; background: #fff !important; }
[data-testid="stPopoverBody"] button[data-testid^="stBaseButton-tertiary"]:hover { background: var(--accent-soft) !important; }
[data-testid="stPopoverBody"] button[data-testid^="stBaseButton-tertiary"] p { color: var(--accent) !important; font-weight: 600 !important; text-align: left !important; }
.bub { border-radius: 14px; padding: 9px 12px; margin: 6px 0; font-size: 14.5px; line-height: 1.45; }
.bub.q { background: var(--accent); color: #fff; margin-left: 40px; }
.bub.a { background: var(--accent-soft); color: var(--ink); margin-right: 20px; }
.bub .src { font-size: 11.5px; color: var(--ink-3); margin-top: 4px; }
.st-key-tune { background:#fff; border:1px solid var(--line); border-radius: 18px; padding: 18px 20px 14px; margin: 18px 0 6px; }
.tune-out { display:flex; gap:12px; align-items:center; flex-wrap:wrap; font-size:15px; padding-top: 8px; border-top: 1px solid var(--line); margin-top: 4px; }
.kv2 { padding: 8px 0; border-top: 1px solid var(--line); font-size: 14.5px; }
.kv2 span { display:block; color: var(--ink-2); } .kv2 b { display:block; font-size: 13.5px; margin-top: 2px; font-variant-numeric: tabular-nums; }
.verdict { border-radius: 16px; padding: 14px 18px; font-size: 16.5px; line-height: 1.5; margin: 2px 0 12px; }
.verdict.ok { background: #E6F4EC; color: #14532D; border: 1px solid #BFE3CC; }
.verdict.warn { background: #FDF0EC; color: #7A2E1A; border: 1px solid #F2CDBF; }
.plan-opt { background:#fff; border:1px solid var(--line); border-radius: 16px; padding: 14px 16px; min-height: 172px; margin-bottom: 6px; }
.plan-opt.dim { opacity: .55; }
.plan-opt .what { font-size: 15.5px; margin: 6px 0 2px; } .plan-opt .when { font-family: var(--display); font-size: 22px; font-weight: 600; color: var(--ink); margin-bottom: 4px; }
@media (min-width: 1760px) { .block-container { max-width: 1560px !important; } :root { --mw: 1560px; } }
.simtable { background:#fff; border:1px solid var(--line); border-radius:16px; padding: 6px 14px; margin-top: 10px; }
.simrow { display:grid; grid-template-columns: 1.7fr 1fr 1fr 1fr 0.9fr; gap: 8px; padding: 9px 0; border-top: 1px solid var(--line); font-size: 14.5px; align-items:center; }
.simrow.head { border-top: 0; color: var(--ink-3); font-size: 12.5px; font-weight: 600; }
.simrow.sel { background: var(--accent-soft); margin: 0 -14px; padding: 9px 14px; }
.simrow i { display:inline-block; width:10px; height:10px; border-radius:3px; margin-right:6px; }
.up { color:#1F8A5B !important; } .down { color:#B4462B !important; }
.ci { background:#fff; border:1px solid var(--line); border-left: 4px solid #1F8A5B; border-radius: 14px; padding: 10px 14px; margin-bottom: 8px; }
.ci.warn { border-left-color: #B4462B; }
.ci .kv { display:flex; justify-content:space-between; font-size: 14px; padding: 3px 0; }
.ci .say { font-size: 14px; color: var(--ink); margin-top: 6px; line-height: 1.45; }
@media (max-width: 760px) { .simrow { grid-template-columns: 1.4fr 1fr 1fr; } .simrow > :nth-child(4), .simrow > :nth-child(5) { display:none; } }
.mob-only { display:none; }
@media (max-width: 760px) {
  .mob-only { display:block; }
  div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"] .opt) { flex-wrap: nowrap !important; overflow-x: auto;
      scroll-snap-type: x mandatory; gap: 10px !important; padding-bottom: 8px; -webkit-overflow-scrolling: touch; }
  div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"] .opt) > div[data-testid="stColumn"] {
      flex: 0 0 84% !important; min-width: 84% !important; width: 84% !important; scroll-snap-align: start; }
  .block-container { padding-left: 16px; padding-right: 16px; }
  div[data-testid="stHorizontalBlock"] { gap: 0.9rem !important; }
  .steps { display:flex; gap:5px; }
  .steps .st span.l, .steps .ln, .logo .tag { display:none; }
  .steps .st .n { width:18px; height:18px; font-size:0; }
  .steps .st.now .n { width:22px; }
  .topbar { gap:10px; }
  div[data-testid="stHorizontalBlock"]:has(.topbar) { gap: 6px; }
  .st-key-use_ai label p { font-size:13.5px !important; white-space:nowrap; }
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

/* paired slider + number box: one value, two ways to set it; stays on one row on phones */
[class*="st-key-pair_"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 10px !important; }
[class*="st-key-pair_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child { flex: 1 1 auto !important; min-width: 0 !important; width: auto !important; }
[class*="st-key-pair_"] [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child { flex: 0 0 150px !important; min-width: 150px !important; width: 150px !important; }
[class*="st-key-pair_"] [data-testid="stSliderTickBar"] { display: none !important; }
[class*="st-key-"][class*="__s"] [data-testid="stSliderThumbValue"], [class*="st-key-"][class*="__s"] [data-testid="stSliderTickBarMin"],
[class*="st-key-"][class*="__s"] [data-testid="stSliderTickBarMax"] { display:none !important; }
[class*="st-key-"][class*="__s"] { margin-bottom: -6px; }
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


def monthly_needed(saved, target, annual_return, months):
    """Monthly amount so that saved + contributions (growing at annual_return) reach target in `months`."""
    i = annual_return / 12
    if months <= 0:
        return 0.0
    if i == 0:
        return max(0.0, (target - saved) / months)
    g = (1 + i) ** months
    return max(0.0, (target - saved * g) * i / (g - 1))


def late_txt(m):
    if m is None:
        return "not reached"
    if m > 0:
        return f"{m} month{'s' if m != 1 else ''} late"
    if m < 0:
        return f"{-m} month{'s' if m != -1 else ''} early"
    return "on time"


def esc(x):
    """Escape text that came from the browser store before it goes into HTML."""
    return html_lib.escape(str(x))


def card(html, cls="card"):
    st.markdown(f'<div class="{cls}">{html}</div>', unsafe_allow_html=True)

def _from_slider(key):
    S[key] = S[key + "__s"]


def _from_box(key):
    S[key + "__s"] = int(S[key] or 0)


def money(label, key, hi, step, help=None, where=None, ratio=(2.2, 1)):
    """One amount, two ways to set it: drag the slider for speed, type in the box for precision."""
    where = where or st
    v = int(S[key] or 0)
    top = int(max(hi, v))
    if S.get(key + "__s") != v:
        S[key + "__s"] = v
    a, b = where.container(key=f"pair_{key}").columns(list(ratio), vertical_alignment="bottom", gap="small")
    a.slider(label, 0, top, step=step, key=key + "__s", on_change=_from_slider, args=(key,), help=help)
    b.number_input(label, min_value=0, step=step, key=key, on_change=_from_box, args=(key,), label_visibility="collapsed")



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
ALLOC_HERO = ("rgba(255,255,255,.35)", "#FFFFFF", "#D9B45B")   # same, on the navy plan card
SPLIT = ("#9AA3B2", "#D5D8DE", "#14213D")        # committed, everyday, free
SPLIT_HERO = ("rgba(255,255,255,.35)", "rgba(255,255,255,.18)", "#F3E7C9")   # same, on the navy hero card


# ═════════════════════════════════════════════════════════════
# 3. SESSION STATE (sample numbers so the demo works immediately; nothing saved to disk)
# ═════════════════════════════════════════════════════════════
TODAY = dt.date.today()
STEPS = ["Where I stand", "Set a goal", "Investment options", "My plan"]
DEFAULTS = {
    "step": 0, "nav": None,
    "salary": 145000, "salary_day": 1,
    "rent": 32000, "emi": 28500, "sip": 15000, "bills": 10100, "usual": 21000, "rent_day": 5, "emi_day": 10, "sip_day": 15, "bills_day": 20,
    "savings": 210000, "invest": 680000, "loans": 600000, "cards": 18000,
    "goal_type": "Car", "goal_name": "New car", "goal_cost": 800000,
    "goal_date": add_months(TODAY, 30), "goal_saved": 150000, "goal_monthly": 18000,
    "q_drop": "Wait it out", "q_exp": "Some experience", "q_early": "Maybe",
    "r_debt": 7.0, "r_equity": 11.0, "r_gold": 8.0, "choice": "Balanced", "sim_scen": "Crash in year 1", "sim_months": 24, "tune_mix": None, "assist": [],
    "wi_kind": "One-off spend", "wi_amount": 15000, "wi_from": "This month's goal money", "wi_monthly": 3000,
    "use_ai": True, "goals": None, "gi": 0, "chat": [], "quick_amt": 0, "quick_src": "Free money",
}
for k, v in DEFAULTS.items():                      # re-assigning keeps values when moving between steps
    st.session_state[k] = st.session_state.get(k, v)
S = st.session_state

# ── several goals: the active one lives in the goal_* keys; all of them live in S.goals
GOAL_KEYS = ["goal_type", "goal_name", "goal_cost", "goal_date", "goal_saved", "goal_monthly"]
if not S.goals:
    S.goals = [{k: S[k] for k in GOAL_KEYS}]
S.gi = min(S.gi, len(S.goals) - 1)
S.goals[S.gi] = {k: S[k] for k in GOAL_KEYS}


def load_goal(i):
    S.goals[S.gi] = {k: S[k] for k in GOAL_KEYS}
    S.gi = i
    for k, v in S.goals[i].items():
        S[k] = v


def add_goal():
    S.goals[S.gi] = {k: S[k] for k in GOAL_KEYS}
    S.goals.append({"goal_type": "Trip", "goal_name": f"Goal {len(S.goals) + 1}", "goal_cost": 150000,
                    "goal_date": add_months(TODAY, 12), "goal_saved": 0, "goal_monthly": 5000})
    load_goal(len(S.goals) - 1)


def quick_entry_fields(e):
    """Saves made from Home still record the active goal's date at the current pace, so history reads correctly."""
    g_ = S.goals[S.gi] if S.goals and S.gi < len(S.goals) else {k: S[k] for k in GOAL_KEYS}
    n_ = months_to_goal(g_["goal_saved"] or 0, g_["goal_monthly"] or 0, g_["goal_cost"] or 1, 0)
    pace = fmt_month(add_months(TODAY, n_)) if n_ else "not reached"
    e["goal"] = g_["goal_name"]
    if not e.get("expected") or e.get("pace_only"):
        e.update({"expected": pace, "monthly": g_["goal_monthly"] or 0, "mix": "current pace", "pace_only": True})
    return e


def mark_paid(i, free_v, buf_v, nw_v, undo=False):
    """Home: 'I've put this month's amount aside' moves the goal forward and saves the check-in in this browser."""
    S.goals[S.gi] = {k: S[k] for k in GOAL_KEYS}
    g = S.goals[i]
    step_amt = (g["goal_monthly"] or 0) * (-1 if undo else 1)
    g["goal_saved"] = max(0, min(g["goal_cost"], (g["goal_saved"] or 0) + step_amt))
    if i == S.gi:
        S.goal_saved = g["goal_saved"]
    month = TODAY.strftime("%b %Y")
    paid = dict(S.get("paid") or {})
    if undo:
        paid.pop(g["goal_name"], None)
    else:
        paid[g["goal_name"]] = month
    S.paid = paid
    e = dict(last) if last and last.get("month") == month else {}
    e.update({"date": TODAY.isoformat(), "month": month, "free": free_v, "buffer": round(buf_v, 2), "net_worth": nw_v,
              "inputs": {k: (S[k].isoformat() if k == "goal_date" else S[k]) for k in INPUT_KEYS},
              "goals": [{k: (v.isoformat() if k == "goal_date" else v) for k, v in gg.items()} for gg in S.goals],
              "paid": paid})
    save_checkin(quick_entry_fields(e))


def set_goal_value(i, free_v, buf_v, nw_v):
    """Goal money that is invested moves with markets: the user types today's value, White re-plans from it."""
    S.goals[S.gi] = {k: S[k] for k in GOAL_KEYS}
    g = S.goals[i]
    old_v = int(g["goal_saved"] or 0)
    g["goal_saved"] = max(0, int(S.get(f"gval{i}") or 0))
    moves = dict(S.get("moves") or {})
    moves[g["goal_name"]] = [old_v, g["goal_saved"], TODAY.strftime("%d %b")]
    S.moves = moves
    if i == S.gi:
        S.goal_saved = g["goal_saved"]
    month = TODAY.strftime("%b %Y")
    e = dict(last) if last and last.get("month") == month else {}
    e.update({"date": TODAY.isoformat(), "month": month, "free": free_v, "buffer": round(buf_v, 2), "net_worth": nw_v,
              "inputs": {k: (S[k].isoformat() if k == "goal_date" else S[k]) for k in INPUT_KEYS},
              "goals": [{k: (v.isoformat() if k == "goal_date" else v) for k, v in gg.items()} for gg in S.goals],
              "paid": dict(S.get("paid") or {}), "moves": dict(S.get("moves") or {})})
    save_checkin(quick_entry_fields(e))


def remove_goal():
    if len(S.goals) > 1:
        S.goals.pop(S.gi)
        S.gi = 0
        for k, v in S.goals[0].items():
            S[k] = v


def go(step):
    """Buttons call this. Keeps the step tabs in sync."""
    S.just_saved = False
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


# ── 3b. HISTORY IN THE BROWSER (localStorage; never on a server) ─────────────
# A tiny st.components.v2 component: on each mount it writes `save` (if given) or clears,
# then reports what the browser holds. Python only ever sees a JSON string.
STORE_JS = """
export default function(component) {
  const { data, setStateValue } = component;
  const KEY = 'white_history';
  try {
    if (data && data.save) { localStorage.setItem(KEY, data.save); }
    if (data && data.wipe) { localStorage.removeItem(KEY); }
    setStateValue('history', localStorage.getItem(KEY) || '');
  } catch (e) { setStateValue('history', ''); }
}
"""
_store = st.components.v2.component("white_store", js=STORE_JS, html="<span></span>")
INPUT_KEYS = ["salary", "salary_day", "rent", "emi", "sip", "bills", "usual", "rent_day", "emi_day", "sip_day", "bills_day", "savings", "invest", "loans", "cards",
              "goal_type", "goal_name", "goal_cost", "goal_date", "goal_saved", "goal_monthly",
              "q_drop", "q_exp", "q_early", "r_debt", "r_equity", "r_gold", "choice"]
for k, v in {"store_nonce": 0, "store_save": None, "store_wipe": False, "just_saved": False}.items():
    S[k] = S.get(k, v)
_res = _store(data={"save": S.store_save, "wipe": S.store_wipe}, key=f"store{S.store_nonce}",
              on_history_change=lambda: None)
S.store_save, S.store_wipe = None, False
try:
    history = json.loads(_res.history or "[]")
    history = [h for h in history if isinstance(h, dict)]
except Exception:
    history = []
last = history[-1] if history else None


def num(h, k, default=0):
    try:
        return float(h.get(k, default))
    except (TypeError, ValueError):
        return default


def save_checkin(entry):
    """'Save this month' button: replace this month's entry if any, append, write back to the browser."""
    hist = [h for h in history if h.get("month") != entry["month"]]
    hist = (hist + [entry])[-12:]
    S.store_nonce += 1
    S.store_save = json.dumps(hist, ensure_ascii=False)
    S.just_saved = True


def wipe_history():
    S.store_nonce += 1
    S.store_wipe = True


def load_last(nav=True):
    """Welcome: start from last month's numbers instead of the sample."""
    inputs = last.get("inputs", {}) if last else {}
    for k in INPUT_KEYS:
        if k in inputs:
            v = inputs[k]
            if k == "goal_date":
                try:
                    v = dt.date.fromisoformat(v)
                except Exception:
                    continue
            S[k] = v
    gl = last.get("goals") if last else None
    if gl:
        try:
            S.goals = [{k: (dt.date.fromisoformat(v) if k == "goal_date" else v) for k, v in g.items()} for g in gl]
            S.gi = 0
            for k, v in S.goals[0].items():
                S[k] = v
        except Exception:
            pass
    if nav:
        go(1)


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


CHAT_PROMPT = SYSTEM_PROMPT + """
You are answering one question from the user about their own plan, inside the app.
- Use only the facts given. If the question needs a number you do not have, say which step of the app
  calculates it (for a purchase or a delay: the What if… check in My plan) instead of guessing.
- Describe the trade-off; never tell the user what to do. Maximum 90 words."""


@st.cache_data(show_spinner=False, ttl=3600)
def call_chat(question, facts_json, api_key, model):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)
    contents = f"QUESTION: {question}\n\nFACTS (calculated by the app):\n{facts_json}"
    for m in (model, "gemini-2.5-flash"):
        try:
            r = client.models.generate_content(model=m, contents=contents,
                                               config=types.GenerateContentConfig(system_instruction=CHAT_PROMPT, temperature=0.4))
            return (r.text or "").strip()
        except Exception as e:
            if "not found" not in str(e).lower() or m == "gemini-2.5-flash":
                raise


def ask(q, facts):
    """'Ask about your plan': Gemini answers from the plan's facts; rule-based reply when AI is off."""
    key = get_secret("GEMINI_API_KEY")
    if S.use_ai and key:
        try:
            a = call_chat(q, json.dumps(facts, ensure_ascii=False), key, get_secret("GEMINI_MODEL", "gemini-flash-latest"))
            S.chat.append((q, a or "No answer came back. Try rephrasing.", "Answered by Gemini · numbers calculated by the app"))
            return
        except Exception as e:
            S.chat.append((q, "The AI is unavailable right now. For a purchase or a delay, use the What if… check above: "
                              "enter the amount and see your goal date and buffer move.", f"AI unavailable ({type(e).__name__})"))
            return
    S.chat.append((q, "AI answers are off or no Gemini key is set. For a purchase or a delay, use the What if… check above: "
                      "enter the amount and see what happens to your goal date and buffer.", "Calculations only · AI is off"))


def _amount(q):
    m = re.search(r"₹?\s*([\d][\d,]*(?:\.\d+)?)\s*(k|K|l|L|lakh|lakhs)?\b", q)
    if not m:
        return None
    v = float(m.group(1).replace(",", ""))
    u = (m.group(2) or "").lower()
    return v * (1000 if u == "k" else 100000 if u.startswith("l") else 1)


def rule_answer(q, ctx):
    """A useful answer without AI: reads the question's intent and amount, and answers from this person's numbers."""
    ql, amt = q.lower(), _amount(q)
    g, sx = ctx["goal"], ctx["mix"]
    if any(w in ql for w in ["best fund", "which fund", "which stock", "recommend", "should i buy"]):
        return "White does not pick funds or stocks. It shows what each mix would do to your goal date; the product is your choice, in your own app."
    if amt and any(w in ql for w in ["afford", "buy", "spend", "trip", "gift", "phone", "purchase", "birthday", "wedding", "laptop"]):
        if amt <= ctx["left_free"]:
            return (f"Yes, from this month's free money: {inr(ctx['left_free'])} → {inr(ctx['left_free'] - amt)} left after goals. "
                    f"{g['name']} stays on its date. Paying from goal money instead would push it about "
                    f"{round(amt / max(1, g['monthly']) * 30.4)} days.")
        d = round(min(amt, g["saved"] + g["monthly"]) / max(1, g["monthly"]) * 30.4)
        return (f"{inr(amt)} is more than this month's free money after goals ({inr(ctx['left_free'])}). From goal money it would push "
                f"{g['name']} about {d} days later; from emergency savings your buffer drops from {ctx['buffer']:.1f} to "
                f"{max(0, ctx['savings'] - amt) / max(1, ctx['essential']):.1f} months.")
    if "late" in ql and "salary" in ql:
        days = int(amt or 5)
        return (f"If salary comes {days} days late, the bills due early in the month still go out: rent on day {ctx['rent_day']} "
                f"({inr(ctx['rent'])}), EMIs on day {ctx['emi_day']} ({inr(ctx['emi'])}). Your savings cover {ctx['buffer']:.1f} months "
                f"of costs, so a short delay is covered; avoid using goal money for it.")
    if any(w in ql for w in ["behind", "far", "on track", "strategy", "change", "catch up", "miss", "late for"]):
        if sx["late"] is not None and sx["late"] <= 0:
            return (f"You're on track: {g['name']} is expected {sx['date']} with the {sx['name']} mix, target {g['target']}. "
                    f"Keep {inr(g['monthly'])} a month and update the goal's value each salary day.")
        gap = max(0, sx["need_pm"] - g["monthly"])
        lt = sx["late"]
        lt_txt = "not reached at this pace" if lt is None else f"about {lt} month{'s' if lt != 1 else ''} behind"
        return (f"{g['name']} is {lt_txt} ({sx['date']} vs {g['target']}). Ways back: "
                f"put aside {inr(sx['need_pm'])} a month (+{inr(gap)}), add about {inr(sx['lump'])} once, move the target "
                f"to {sx['date']}, or compare the Growth mix in step 3 (bigger bad-year fall). Try them in “Tune your plan”.")
    if "sip" in ql:
        return ("SIPs are counted as committed money because they leave your account every month, already invested. If a SIP "
                "is for this goal, include it in “Put aside” and set SIPs to 0, so it isn't counted twice.")
    if any(w in ql for w in ["buffer", "emergency"]):
        return (f"Your emergency buffer is {ctx['buffer']:.1f} months: how long savings of {inr(ctx['savings'])} would pay rent, "
                f"EMIs, bills and daily spending if salary stopped. 3–6 months is the usual cushion.")
    if any(w in ql for w in ["invest for me", "wallet", "hold my money"]):
        return "White never holds or invests money. You invest in your own bank or fund app; White shows what that does to your goal."
    return (f"This month: {inr(ctx['free'])} free, {inr(ctx['left_free'])} left after goals, buffer {ctx['buffer']:.1f} months. "
            f"{g['name']}: {inr(g['saved'])} of {inr(g['cost'])}, expected {sx['date']} vs target {g['target']}. "
            "Ask about a purchase with an amount, a late salary, or whether you're behind.")


def assistant(ctx, suggestions):
    """Ask White: a chat pinned to the corner of every screen, answering from this person's numbers."""
    def _ask(q):
        key = get_secret("GEMINI_API_KEY")
        base = rule_answer(q, ctx)
        if S.use_ai and key:
            try:
                facts = json.dumps({**{k: v for k, v in ctx.items() if k not in ("goal", "mix")},
                                    "goal": ctx["goal"], "mix": ctx["mix"], "calculated_answer": base}, ensure_ascii=False, default=str)
                a = call_chat(q, facts, key, get_secret("GEMINI_MODEL", "gemini-flash-latest"))
                S.assist.append((q, a or base, "Gemini, from your numbers"))
                return
            except Exception:
                pass
        S.assist.append((q, base, "Calculated from your numbers"))
    with st.container(key="assistant"):
        with st.popover("Ask White", icon=":material/auto_awesome:"):
            st.markdown('<b style="font-size:17px">Ask White</b><div class="cap">Answers from your numbers on this screen. '
                        'It never picks a product or tells you what to do.</div>', unsafe_allow_html=True)
            for i, sq in enumerate(suggestions):
                st.button(sq, key=f"as{S.step}_{i}", width="stretch", type="tertiary", on_click=_ask, args=(sq,))
            for cq, ca, csrc in S.assist[-4:]:
                st.markdown(f'<div class="bub q">{esc(cq)}</div><div class="bub a">{esc(ca)}<div class="src">{csrc}</div></div>',
                            unsafe_allow_html=True)
            with st.form(f"assist_form{S.step}", clear_on_submit=True, border=False):
                fa, fb = st.columns([4, 1], vertical_alignment="bottom")
                q_ = fa.text_input("Ask", placeholder="e.g. Can I afford a ₹25,000 trip?", label_visibility="collapsed")
                if fb.form_submit_button("Ask", type="primary") and q_.strip():
                    _ask(q_.strip())
                    st.rerun()


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
total_goal_monthly = sum((g.get("goal_monthly") or 0) for g in S.goals)   # all goals together

SCORE = {"Sell to stop losses": 0, "Wait it out": 1, "Invest more": 2,
         "New to investing": 0, "Some experience": 1, "Experienced": 2,
         "Likely": 0, "Maybe": 1, "Unlikely": 2}
score = SCORE.get(S.q_drop, 1) + SCORE.get(S.q_exp, 1) + SCORE.get(S.q_early, 1)
comfort = "Low" if score <= 2 else ("Medium" if score <= 4 else "High")

MIXES = {"Steady": (85, 5, 10), "Balanced": (40, 50, 10), "Growth": (10, 85, 5)}  # debt, equity, gold %
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
        "need_pm": monthly_needed(S.goal_saved, S.goal_cost, exp_r, goal_months),   # to be on time with this mix
        "fv": path(S.goal_saved, S.goal_monthly, exp_r, goal_months)[-1],              # value on the target date
        "late": (n_exp - goal_months) if n_exp else None,                               # months late (+) / early (−)
        "drop_amt": abs((d * WEAK_YEAR[0] + e * WEAK_YEAR[1] + g * WEAK_YEAR[2]) / 100) / 100 * S.goal_saved,
        "risk": {"Steady": 2, "Balanced": 3, "Growth": 4}[name],                        # 1–5, from the equity share
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
    x = alt.X("date:T", title=None, axis=alt.Axis(format="%b ’%y", tickCount=5, **AXIS))
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


def value_chart(stats, target, height=220):
    """How much each mix could be worth on the target date, against the goal (dashed)."""
    names = list(stats)
    df = pd.DataFrame([{"mix": n, "value": s["fv"], "label": short_inr(s["fv"])} for n, s in stats.items()])
    x = alt.X("mix:N", sort=names, title=None, axis=alt.Axis(labelColor="#55565E", labelFont=FONT, labelFontSize=12,
                                                             labelFontWeight=600, labelAngle=0, domain=False, ticks=False))
    y = alt.Y("value:Q", title=None, scale=alt.Scale(domain=[0, max(target, df["value"].max()) * 1.18]),
              axis=alt.Axis(labelExpr=LAKH, tickCount=4, **AXIS))
    color = alt.Color("mix:N", scale=alt.Scale(domain=names, range=[MIX_COLOR[n] for n in names]), legend=None)
    bars = alt.Chart(df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, size=46).encode(
        x=x, y=y, color=color, tooltip=[alt.Tooltip("mix:N", title="Mix"), alt.Tooltip("label:N", title="By target date")])
    txt = alt.Chart(df).mark_text(dy=-9, font=FONT, fontSize=12, fontWeight=700, color="#111114").encode(x=x, y=y, text="label:N")
    gdf = pd.DataFrame({"v": [target], "t": [f"Goal {short_inr(target)}"]})
    rule = alt.Chart(gdf).mark_rule(color=GOLD, strokeDash=[5, 4], strokeWidth=1.5).encode(y="v:Q")
    rt = alt.Chart(gdf).mark_text(align="left", dx=4, dy=-7, color=GOLD, font=FONT, fontSize=11, fontWeight=700).encode(
        y="v:Q", x=alt.value(0), text="t:N")
    st.altair_chart((bars + txt + rule).properties(height=height).configure_view(strokeWidth=0).configure(
        background="transparent", padding={"left": 4, "right": 12, "top": 8, "bottom": 4}), width="stretch")


def runway(start, end, salary, events, daily, goal_out):
    """Balance from one salary to the next: salary in, goal money out first, bills on their days, daily spending spread."""
    days = (end - start).days
    rows, bal = [], salary - goal_out
    marks = [{"d": pd.Timestamp(start), "v": bal, "t": f"Salary in, {inr(goal_out)} to goals"}]
    for i in range(days):
        d = start + dt.timedelta(days=i)
        bal -= daily
        for name, amt, day in events:
            if d.day == day and i < days:
                bal -= amt
                marks.append({"d": pd.Timestamp(d), "v": bal, "t": f"{name} {short_inr(amt)}"})
        rows.append({"d": pd.Timestamp(d), "v": bal})
    return pd.DataFrame(rows), pd.DataFrame(marks)


def runway_chart(df, marks, today, height=230):
    lo = df.loc[df["v"].idxmin()]
    base = alt.Chart(df).encode(x=alt.X("d:T", title=None, axis=alt.Axis(format="%d %b", tickCount=6, **AXIS)))
    area = base.mark_area(interpolate="step-after", color="#14213D", opacity=0.08).encode(y=alt.Y("v:Q", title=None, axis=alt.Axis(labelExpr=LAKH, tickCount=4, **AXIS)))
    line = base.mark_line(interpolate="step-after", color="#14213D", strokeWidth=2.2).encode(y="v:Q", tooltip=[alt.Tooltip("d:T", title="Day", format="%d %b"), alt.Tooltip("v:Q", title="Left", format=",.0f")])
    dots = alt.Chart(marks).mark_point(filled=True, size=55, color="#2453B8").encode(x="d:T", y="v:Q", tooltip=[alt.Tooltip("t:N", title="Event"), alt.Tooltip("d:T", title="Day", format="%d %b")])
    tdf = pd.DataFrame({"d": [pd.Timestamp(today)], "t": ["Today"]})
    trule = alt.Chart(tdf).mark_rule(color=GOLD, strokeDash=[4, 4]).encode(x="d:T")
    ttxt = alt.Chart(tdf).mark_text(align="left", dx=5, y=6, baseline="top", color=GOLD, font=FONT, fontSize=11, fontWeight=700).encode(x="d:T", text="t:N")
    ldf = pd.DataFrame([{"d": lo["d"], "v": lo["v"], "t": f"Before payday: {short_inr(lo['v'])}"}])
    lpt = alt.Chart(ldf).mark_point(filled=True, size=90, color="#B4462B").encode(x="d:T", y="v:Q")
    ltx = alt.Chart(ldf).mark_text(align="right", dx=-4, dy=-16, color="#B4462B", font=FONT, fontSize=11, fontWeight=700).encode(x="d:T", y="v:Q", text="t:N")
    ch = (area + line + trule + ttxt + dots + lpt + ltx).properties(height=height).configure_view(strokeWidth=0).configure(background="transparent", padding={"left": 4, "right": 12, "top": 6, "bottom": 4})
    st.altair_chart(ch, width="stretch")


SCENARIOS = {"Calm markets": "Returns arrive as assumed, every month.",
             "Crash in year 1": "Shares fall about 30% over six months, then recover; gold rises while shares fall.",
             "Bumpy ride": "Normal ups and downs: the same random months for every mix, so the comparison is fair."}


def simulate(name, scenario, months, saved, monthly):
    """Month-by-month value of the goal money in one mix. Same market for every mix, so they can be compared."""
    d, e, g = MIXES[name]
    rd, re_, rg = S.r_debt / 1200, S.r_equity / 1200, S.r_gold / 1200
    rng = __import__("random").Random(7)
    v, out, low = float(saved), [], float(saved)
    for m in range(1, months + 1):
        if scenario == "Crash in year 1":
            eq = -0.058 if m <= 6 else (0.026 if m <= 18 else re_)
            gd = 0.012 if m <= 6 else rg
            dbt = rd
        elif scenario == "Bumpy ride":
            eq, gd, dbt = rng.gauss(re_, 0.045), rng.gauss(rg, 0.035), rng.gauss(rd, 0.003)
        else:
            eq, gd, dbt = re_, rg, rd
        r = (d * dbt + e * eq + g * gd) / 100
        v = (v + monthly) * (1 + r)
        low = min(low, v - (saved + monthly * m))
        out.append(v)
    return out, low


def sim_section(choice_, s_):
    st.markdown('<div class="row" style="margin:30px 0 4px;align-items:flex-end;flex-wrap:wrap;gap:4px 16px"><div>'
                '<h3 style="margin:0;font-size:22px">See it work: your next salary days, simulated</h3>'
                '<div class="cap">You set up an auto-transfer or SIP in your own bank or fund app; each salary day you tick it and type '
                'what the goal money is worth. This plays that forward so you can see what White would tell you, in good and bad markets.</div></div></div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1], vertical_alignment="bottom")
    scen = c1.segmented_control("Market", list(SCENARIOS), key="sim_scen")
    months = c2.slider("Months to play forward", 6, 36, step=6, key="sim_months")
    scen = scen or "Crash in year 1"
    st.caption(SCENARIOS[scen] + " Illustrative only; not a forecast.")
    sv, mo, cost = S.goal_saved or 0, S.goal_monthly or 0, S.goal_cost or 1
    runs = {n: simulate(n, scen, months, sv, mo) for n in MIXES}
    exp_m = s_["exp_r"] / 12
    plan_ = []
    v = float(sv)
    for m in range(1, months + 1):
        v = (v + mo) * (1 + exp_m)
        plan_.append(v)
    put_in = [sv + mo * m for m in range(1, months + 1)]
    rows = []
    for m in range(months + 1):
        dte = pd.Timestamp(add_months(TODAY, m))
        for n, (vals, _) in runs.items():
            rows.append({"d": dte, "v": 0 if m == 0 else vals[m - 1] - put_in[m - 1], "s": n})
        rows.append({"d": dte, "v": 0 if m == 0 else plan_[m - 1] - put_in[m - 1], "s": "Your plan (expected)"})
    df = pd.DataFrame(rows)
    names = list(MIXES) + ["Your plan (expected)"]
    colors = [MIX_COLOR[n] for n in MIXES] + ["#14213D"]
    sw = alt.condition(alt.datum.s == choice_, alt.value(3.4), alt.value(1.8))
    base = alt.Chart(df).encode(
        x=alt.X("d:T", title=None, axis=alt.Axis(format="%b ’%y", tickCount=6, **AXIS)),
        y=alt.Y("v:Q", title=None, axis=alt.Axis(format="~s", labelExpr="(datum.value < 0 ? '−₹' : '₹') + format(abs(datum.value) / 1000, ',.0f') + 'k'", tickCount=6, **AXIS)),
        color=alt.Color("s:N", scale=alt.Scale(domain=names, range=colors), legend=alt.Legend(orient="top", title=None, labelFont=FONT, labelFontSize=12, symbolType="stroke")),
        tooltip=[alt.Tooltip("s:N", title=""), alt.Tooltip("d:T", title="Month", format="%b %Y"), alt.Tooltip("v:Q", title="Value", format=",.0f")])
    lines = base.transform_filter(alt.FieldOneOfPredicate("s", list(MIXES))).mark_line(interpolate="monotone").encode(strokeWidth=sw)
    ref = base.transform_filter(alt.FieldOneOfPredicate("s", ["Your plan (expected)"])).mark_line(strokeDash=[5, 4], strokeWidth=1.6)
    zero = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule(color="#8A8B92", strokeWidth=1).encode(y="y:Q")
    left, right = st.columns([1.6, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="cap">Gain or loss compared with the money you put in. Below the grey line = worth less than you put in.</div>', unsafe_allow_html=True)
            st.altair_chart((zero + lines + ref).properties(height=290).configure_view(strokeWidth=0).configure(background="transparent"), width="stretch")
        cmp = ""
        for n, (vals, low) in runs.items():
            gain = vals[-1] - put_in[-1]
            n_left = months_to_goal(vals[-1], mo, cost, mix_stats(n)["exp_r"])
            land = fmt_month(add_months(TODAY, months + n_left)) if n_left is not None else "—"
            cmp += (f'<div class="simrow {"sel" if n == choice_ else ""}"><span><i style="background:{MIX_COLOR[n]}"></i>{n} '
                    f'<span class="cap">{MIXES[n][0]}/{MIXES[n][1]}/{MIXES[n][2]}</span></span><b>{inr(vals[-1])}</b>'
                    f'<span class="{"up" if gain >= 0 else "down"}">{"+" if gain >= 0 else "−"}{inr(abs(gain))}</span>'
                    f'<span class="{"down" if low < -1000 else ""}">{("−" + inr(abs(low))) if low < -1000 else "never below"}</span><span>{land}</span></div>')
        st.markdown(f'<div class="simtable"><div class="simrow head"><span>Mix · debt/equity/gold</span><span>Worth after {months} mo</span>'
                    f'<span>vs money put in</span><span>Lowest point</span><span>Goal lands</span></div>{cmp}</div>', unsafe_allow_html=True)
    with right:
        vals, _ = runs[choice_]
        pts = sorted(set([m for m in (3, 6, 12) if m < months] + [months]))
        html_ = ""
        prev_v = float(sv)
        for m in pts:
            actual, planned, pin = vals[m - 1], plan_[m - 1], put_in[m - 1]
            n_left = months_to_goal(actual, mo, cost, s_["exp_r"])
            plan_n = s_["months"] or goal_months
            land = None if n_left is None else m + n_left
            drift = None if land is None else land - plan_n
            moved = actual - prev_v - mo * (m - (pts[pts.index(m) - 1] if pts.index(m) else 0))
            if drift is not None and drift <= 0:
                if abs(actual - planned) < 1000:
                    say = f"Right on plan: {esc(S.goal_name)} still lands around {s_['goal_date']}. Keep going."
                elif actual > planned:
                    say = f"Ahead of plan by {inr(actual - planned)}. Still lands around {s_['goal_date']} or sooner. Keep going."
                else:
                    say = f"{inr(planned - actual)} below plan, but still lands around {s_['goal_date']}. No action needed."
                tone = "ok"
            else:
                rem = max(1, plan_n - m)
                lump = max(0, cost - path(actual, mo, s_["exp_r"], rem)[-1]) / ((1 + s_["exp_r"] / 12) ** rem)
                land_txt = fmt_month(add_months(TODAY, land)) if land else "not reached"
                say = (f"{inr(planned - actual)} below plan after a market fall. At today's value it lands {land_txt}, "
                       f"{drift} month{'s' if drift != 1 else ''} later than planned. Your {inr(mo)} now buys at lower prices; "
                       f"add about {inr(lump)} once to stay on plan, or keep going and wait for the recovery.")
                tone = "warn"
            html_ += (f'<div class="ci {tone}"><div class="row"><b>Salary day, {fmt_month(add_months(TODAY, m))}</b>'
                      f'<span class="cap">month {m}</span></div>'
                      f'<div class="kv"><span>Worth today</span><b>{inr(actual)}</b></div>'
                      f'<div class="kv"><span>Market move since last check-in</span><b class="{"up" if moved >= 0 else "down"}">'
                      f'{"+" if moved >= 0 else "−"}{inr(abs(moved))}</b></div>'
                      f'<div class="say">White: {say}</div></div>')
            prev_v = actual
        st.markdown(f'<div class="k" style="margin-bottom:6px">What White tells you · {choice_} mix</div>{html_}', unsafe_allow_html=True)


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
        x=alt.X("start:T", title=None, axis=alt.Axis(format="%b ’%y", tickCount=6, **AXIS)), x2="end:T",
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


masthead = st.container(key="masthead")
t1, t2 = masthead.columns([4, 1], vertical_alignment="center")
t1.markdown('<div class="topbar"><div class="logo"><div class="mark"></div><div class="word">White<b>.</b></div>'
            '<div class="tag">Your money, nothing hidden</div></div>'
            + (progress_html() if S.step > 0 else "") + '</div>', unsafe_allow_html=True)
t2.toggle("AI explanations", key="use_ai", help="Turn off to see calculations only.")
if S.step > 0:
    if S.nav not in STEPS:
        S.nav = STEPS[S.step - 1]
    masthead.segmented_control("Steps", STEPS, key="nav", on_change=nav_changed, label_visibility="collapsed",
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
        st.markdown(f'<div class="cap" style="margin-top:18px;font-weight:600">{TODAY.strftime("%A, %d %B")}</div>'
                    '<h1 class="hero-title">Salary\'s in.<br><span class="dim">Let\'s make it count.</span></h1>'
                    '<p style="color:#55565E;font-size:16.5px;line-height:1.6;max-width:460px;margin-bottom:22px">A 10-minute check-in '
                    'that answers <b style="color:#111114">"Am I on track for my goal, and what should I do with this '
                    'month\'s money?"</b> Then test a decision before you make it.</p>', unsafe_allow_html=True)
        if last:
            b1, b2 = st.columns([1.3, 1])
            b1.button("Use last month's numbers", type="primary", on_click=load_last, key="loadlast")
            b2.button("Start fresh", on_click=go, args=(1,), key="fresh")
        else:
            st.button("Start check-in", type="primary", on_click=go, args=(1,))
        st.markdown(f'<div class="cap" style="margin-top:16px;display:flex;gap:8px;align-items:center">{icon(I_LOCK, "#8A8B92", 14)}'
                    'No bank login · no SMS reading · nothing on our servers · you make every decision</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div style="height:34px"></div>', unsafe_allow_html=True)
        if last:
            rows = "".join(
                f'<div class="hist"><span>{esc(h.get("month", ""))}</span><span>free <b>{inr(num(h, "free"))}</b></span>'
                f'<span>buffer <b>{num(h, "buffer"):.1f} mo</b></span><span>{esc(h.get("goal", ""))} <b>{esc(h.get("expected", "—"))}</b></span></div>'
                for h in history[-4:][::-1])
            card(f'<div class="row"><span class="k">Your check-ins</span><span class="pill">{len(history)} saved in this browser</span></div>'
                 f'<div class="num lg" style="margin-top:8px">{esc(last.get("goal", "Goal"))}: {esc(last.get("expected", "—"))}</div>'
                 f'<div class="cap">expected at your last check-in ({esc(last.get("month", ""))}), saving {inr(num(last, "monthly"))}/month {"at current pace, no growth" if last.get("pace_only") else "in the " + esc(last.get("mix", "")) + " mix"}</div>'
                 f'<div class="hair"></div>{rows}')
            st.button("Clear history from this browser", on_click=wipe_history, key="wipe", type="tertiary")
        else:
            card(f'<div class="row"><span class="k">Free to use this month</span><span class="pill gold">Sample</span></div>'
                 f'<div class="num xl" style="margin-top:8px">{inr(free)}</div>'
                 + bar3(committed, S.usual, max(free, 0), SPLIT_HERO, "20px 0 12px") +
                 f'<div class="legend"><span><i style="background:{SPLIT_HERO[0]}"></i>Fixed expenses <b>{inr(committed)}</b></span>'
                 f'<span><i style="background:{SPLIT_HERO[1]}"></i>Daily spending <b>{inr(S.usual)}</b></span>'
                 f'<span><i style="background:{SPLIT_HERO[2]}"></i>Free <b>{inr(free)}</b></span></div>', "card hero")
        # this month at a glance: three numbers people act on
        days_left = max(1, (next_salary - TODAY).days)
        glance = [("Everyday budget", f"{inr(daily_spend)}<span class='u'>/day</span>", f"till {next_salary.strftime('%d %b')}"),
                  ("Emergency buffer", f"{buffer_months:.1f}<span class='u'> months</span>", "aim for 3–6"),
                  ("Next salary", next_salary.strftime("%d %b"), f"in {days_left} days")]
        st.markdown('<div class="glance">' + "".join(
            f'<div class="card mini"><div class="k">{k}</div><div class="num md">{v}</div><div class="cap">{c}</div></div>'
            for k, v, c in glance) + '</div>', unsafe_allow_html=True)
        # the decision moment, without the full check-in: "can I afford this?"
        with st.container(key="quick"):
            st.markdown('<div class="k">Thinking of buying something?</div>'
                        '<div class="cap">See what it does before you spend. Rules only.</div>', unsafe_allow_html=True)
            money("Amount (₹)", "quick_amt", 100000, 1000)
            st.segmented_control("Paid from", ["Free money", "Goal money"], key="quick_src")
            amt, src = S.quick_amt or 0, S.quick_src or "Free money"
            if amt > 0 and S.goals:
                g0 = S.goals[0] if S.gi >= len(S.goals) else S.goals[S.gi]
                if src == "Free money":
                    left_free = free - amt
                    verdict = ("ok", "Fits this month") if left_free >= 0 else ("warn", "More than this month's free money")
                    body = (f'<div class="kv"><span>Free this month</span><b>{inr(free)} → {inr(left_free)}</b></div>'
                            f'<div class="kv"><span>{esc(g0["goal_name"])}</span><b>unchanged</b></div>')
                else:
                    cost0, sv0, m0 = g0["goal_cost"] or 1, g0["goal_saved"] or 0, g0["goal_monthly"] or 0
                    n_a, n_b = months_to_goal(sv0, m0, cost0, 0), months_to_goal(max(0, sv0 - amt), m0, cost0, 0)
                    shift = (n_b or 0) - (n_a or 0)
                    days = round(min(amt, sv0) / m0 * 30.4) if m0 else 0
                    late_txt_ = (f"About {days} days later" if days < 45 else f"About {round(days / 30.4)} months later")
                    verdict = ("ok", "No change to the goal date") if days == 0 else ("warn", late_txt_)
                    da = fmt_month(add_months(TODAY, n_a)) if n_a else "—"
                    db = fmt_month(add_months(TODAY, n_b)) if n_b else "—"
                    body = (f'<div class="kv"><span>{esc(g0["goal_name"])} reached</span><b>{da} → {db}</b></div>'
                            f'<div class="kv"><span>Free this month</span><b>unchanged</b></div>')
                st.markdown(f'<div class="quick-out"><span class="pill {verdict[0]}">{verdict[1]}</span>{body}</div>', unsafe_allow_html=True)

    # ── salary-day goal tracker: how close each goal is, and what today's salary changes
    this_month = TODAY.strftime("%b %Y")
    earlier = next((h for h in reversed(history) if h.get("month") != this_month), None)
    prev = {g.get("goal_name"): g for g in (earlier.get("goals") or [])} if earlier else {}
    if last and last.get("month") == this_month and not S.get("synced_month"):
        load_last(nav=False)                          # this month's check-in already exists: pick up where you left off
        S.paid = last.get("paid") or {}
        S.synced_month = True
    if "paid" not in S:
        S.paid = {}
    paid_now = {k: v for k, v in (S.paid or {}).items() if v == this_month}
    behind_n = 0
    cards = []
    for gi_, g in enumerate(S.goals):
        cost, saved, monthly = g["goal_cost"] or 1, g["goal_saved"] or 0, g["goal_monthly"] or 0
        gm = months_between(TODAY, g["goal_date"])
        need = max(0, cost - saved) / gm
        n_pace = months_to_goal(saved, monthly, cost, 0)
        late = None if n_pace is None else n_pace - gm
        ok = late is not None and late <= 0
        behind_n += 0 if ok else 1
        done = g["goal_name"] in paid_now
        after = saved if done else min(cost, saved + monthly)
        pct, pct_after = saved / cost * 100, after / cost * 100
        pace_d = "not reached at this pace" if n_pace is None else fmt_month(add_months(TODAY, n_pace))
        # sparkline: balance at your pace vs the straight line that lands on time
        N = max(gm, min(n_pace or gm * 2, 240))
        X = lambda m: m / N * 300
        Y = lambda v: 82 - min(v, cost) / cost * 74
        pace_pts = " ".join(f"{X(m):.1f},{Y(saved + monthly * m):.1f}" for m in range(0, N + 1, max(1, N // 40)))
        spark = (f'<svg class="spark" viewBox="0 0 300 86" preserveAspectRatio="none" aria-label="Savings path for {esc(g["goal_name"])}">'
                 f'<line x1="0" y1="8" x2="300" y2="8" stroke="#B8862B" stroke-dasharray="4 4" vector-effect="non-scaling-stroke"/>'
                 f'<line x1="{X(gm):.1f}" y1="4" x2="{X(gm):.1f}" y2="84" stroke="#B9B9B4" stroke-dasharray="2 3" vector-effect="non-scaling-stroke"/>'
                 f'<line x1="0" y1="{Y(saved):.1f}" x2="{X(gm):.1f}" y2="8" stroke="#199e70" stroke-width="2" stroke-dasharray="5 4" vector-effect="non-scaling-stroke"/>'
                 f'<polyline points="{pace_pts}" fill="none" stroke="#14213D" stroke-width="2.5" vector-effect="non-scaling-stroke"/></svg>'
                 f'<div class="cap" style="display:flex;justify-content:space-between"><span>Now</span><span>{fmt_month(g["goal_date"])}</span></div>'
                 f'<div class="cap" style="font-size:12px;white-space:nowrap"><b style="color:#14213D">—</b> your pace &nbsp; <b style="color:#199e70">- -</b> on time &nbsp; '
                 f'<b style="color:#B8862B">- -</b> goal</div>')
        p = prev.get(g["goal_name"])
        since = (f'<div class="gline"><span>Since last check-in</span><b>+{inr(max(0, saved - (p.get("goal_saved") or 0)))}</b></div>'
                 if p else "")
        ticks = [h.get("month") for h in history if (h.get("paid") or {}).get(g["goal_name"]) == h.get("month")]
        if done and this_month not in ticks:
            ticks.append(this_month)
        ticks = list(dict.fromkeys(t_ for t_ in ticks if t_))[-6:]
        since += (f'<div class="gline"><span>Months put aside</span><b>{" · ".join(t_.split()[0] + " ✓" for t_ in ticks)}</b></div>'
                  if ticks else "")
        mv = (S.get("moves") or (last.get("moves") if last else None) or {}).get(g["goal_name"])
        if mv and mv[0]:
            dv = mv[1] - mv[0]
            since += (f'<div class="gline"><span>Value update {esc(mv[2])}</span><b class="{"up" if dv >= 0 else "down"}">'
                      f'{"+" if dv >= 0 else "−"}{inr(abs(dv))} ({"+" if dv >= 0 else "−"}{abs(dv / mv[0] * 100):.1f}%)</b></div>')
        status = "On time" if ok else ("Not reached" if late is None else f"{late} month{'s' if late != 1 else ''} late")
        note = f'<div class="cap" style="color:#1F8A5B"><b>✓ {inr(monthly)} put aside for {TODAY.strftime("%b")}</b></div></div></div>' if done else f'<div class="cap">After today\'s {inr(monthly)}: <b style="color:#111114">{pct_after:.0f}%</b></div></div></div>'
        cards.append((
            f'<div class="card gcard"><div class="row"><b style="font-size:16px">{esc(g["goal_name"])}</b>'
            f'<span class="pill {"ok" if ok else "warn"}">{status}</span></div>'
            f'<div class="gtop">{ring(pct / 100, "#14213D", 84, 9, f"{pct:.0f}%", "saved")}'
            f'<div style="flex:1;min-width:0"><div class="num" style="font-size:24px">{short_inr(saved)} <span class="cap">of {short_inr(cost)}</span></div>'
            f'<div class="split" style="margin:8px 0 4px;width:100%"><span style="width:{max(pct, 1):.0f}%;background:#14213D"></span>'
            f'<span style="width:{max(pct_after - pct, 1):.0f}%;background:#8FA0C4"></span>'
            f'<span style="width:{max(100 - pct_after, 0):.0f}%;background:#E8E7E3"></span></div>'
            f'{note}'
            f'{spark}'
            f'<div class="gline" style="margin-top:8px"><span>At this pace</span><b>{pace_d}</b></div>'
            f'<div class="gline"><span>To be on time</span><b>{inr(need)}/month</b></div>{since}</div>'
            , gi_, done, monthly))
    st.markdown(f'<div class="row" style="margin:30px 0 4px;align-items:flex-end;flex-wrap:wrap;gap:4px 16px"><div><div class="k">Salary day · your goals</div>'
                f'<div class="cap">How close each goal is, and what this month\'s amount does. Rules only, no growth assumed.</div></div>'
                f'<span class="cap">{len(S.goals) - behind_n} of {len(S.goals)} on time · {inr(total_goal_monthly)}/month in all</span></div>',
                unsafe_allow_html=True)
    per_row = 3
    slots = cards + ([None] if len(cards) < 6 else [])          # last slot invites another goal
    for i in range(0, len(slots), per_row):
        cols = st.columns(per_row, gap="medium")
        for c, html in zip(cols, slots[i:i + per_row]):
            if html:
                h_, i_, done_, m_ = html
                c.markdown(h_, unsafe_allow_html=True)
                with c.popover("Update today's value", width="stretch"):
                    st.caption("Invested this goal's money in a fund, RD or FD? Check your app and type what it is worth today. "
                               "White re-plans from it. Nothing is linked.")
                    st.number_input("Worth today (₹)", min_value=0, step=1000, key=f"gval{i_}", value=int(S.goals[i_]["goal_saved"] or 0))
                    st.button("Save value", key=f"gsave{i_}", type="primary", width="stretch",
                              on_click=set_goal_value, args=(i_, free, buffer_months, net_worth))
                if done_:
                    c.button("Undo", key=f"unpaid{i_}", on_click=mark_paid, args=(i_, free, buffer_months, net_worth, True))
                else:
                    c.button(f"I've put aside {inr(m_)}", key=f"paid{i_}", type="primary", width="stretch",
                             on_click=mark_paid, args=(i_, free, buffer_months, net_worth),
                             help="Moves this goal forward and saves this month's check-in in this browser only.")
            else:
                box = c.container(key="addgoal")
                box.markdown('<b style="font-size:16px">Saving for something else?</b>'
                             '<div class="cap" style="margin:6px 0 4px">A trip, a laptop, a home deposit. Add it and every goal '
                             'is tracked here each salary day, with what all of them need together.</div>', unsafe_allow_html=True)
                box.button("+ Add a goal", key="home_add_goal", on_click=lambda: (add_goal(), go(2)))

    # ── what changed since the last check-in from an earlier month (bills creep up quietly)
    if earlier and earlier.get("inputs"):
        old = earlier["inputs"]
        labels_ = {"salary": "Take-home", "rent": "Rent", "emi": "EMIs", "sip": "SIPs", "bills": "Insurance & bills", "usual": "Daily spending"}
        chg = [(lbl, (S[k] or 0) - (old.get(k) or 0), k) for k, lbl in labels_.items() if (S[k] or 0) != (old.get(k) or 0)]
        if chg:
            chips = "".join(f'<span class="pill {"ok" if (d > 0) == (k == "salary") else "warn"}">{lbl} {"↑" if d > 0 else "↓"} {inr(abs(d))}</span>' for lbl, d, k in chg)
            st.markdown(f'<div class="row" style="margin:26px 0 6px;justify-content:flex-start;gap:8px;flex-wrap:wrap">'
                        f'<span class="k" style="margin-right:6px">Since {esc(earlier.get("month", "last check-in"))}</span>{chips}</div>', unsafe_allow_html=True)

    # ── payday runway: the month, day by day
    last_salary = add_months(next_salary, -1)
    cycle = max(1, (next_salary - last_salary).days)
    events = [("Rent", S.rent, S.rent_day), ("EMIs", S.emi, S.emi_day), ("SIPs", S.sip, S.sip_day), ("Bills", S.bills, S.bills_day)]
    df_r, marks_r = runway(last_salary, next_salary, S.salary, [e for e in events if e[1]], S.usual / cycle, total_goal_monthly)
    lo_r = df_r.loc[df_r["v"].idxmin()]
    now_left = float(df_r.loc[df_r["d"] <= pd.Timestamp(TODAY), "v"].iloc[-1]) if (df_r["d"] <= pd.Timestamp(TODAY)).any() else float(df_r["v"].iloc[0])
    spare_day = max(0.0, float(df_r["v"].iloc[-1])) / max(1, (next_salary - TODAY).days)
    st.markdown('<div class="row" style="margin:26px 0 4px;align-items:flex-end;flex-wrap:wrap;gap:4px 16px"><div><div class="k">Payday runway</div>'
                f'<div class="cap">Salary in on {last_salary.strftime("%d %b")}, goal money out first, bills on their days, daily spending spread evenly. Rules only.</div></div>'
                f'<span class="cap">Next salary {next_salary.strftime("%d %b")}</span></div>', unsafe_allow_html=True)
    rc1, rc2 = st.columns([2.2, 1], gap="medium")
    with rc1:
        with st.container(border=True):
            runway_chart(df_r, marks_r, TODAY)
    with rc2:
        tight_ok = lo_r["v"] >= 0
        big = max([e for e in events if e[1]], key=lambda e: e[1], default=None)
        card(f'<div class="k">Left today, on plan</div><div class="num md">{inr(now_left)}</div>'
             f'<div class="hair"></div><div class="k">Biggest hit</div><div class="num md">'
             f'{(big[0] + " " + inr(big[1])) if big else "—"}</div><div class="cap">{("on day " + str(big[2])) if big else ""}'
             f'{" · you stay above zero all month" if tight_ok else " · you would run short before payday: move a bill date or spend less early"}</div>'
             f'<div class="hair"></div><div class="k">Truly spare</div><div class="num md">{inr(spare_day)}<span class="u">/day</span></div>'
             f'<div class="cap">after bills, goal money and usual spending, till {next_salary.strftime("%d %b")}</div>')


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
            tab1, tab2, tab3 = st.tabs(["Income", "Fixed monthly expenses", "Savings & loans"])
            with tab1:
                money("Take-home salary (₹/month)", "salary", 500000, 5000)
                st.slider("Salary day (date of month)", min_value=1, max_value=28, step=1, key="salary_day",
                          help="Your check-in runs salary to salary.")
                money("Regular daily spending (₹/month)", "usual", 100000, 1000,
                      help="Food, travel, shopping. A rough 3-month average is enough.")
            with tab2:
                st.caption("SIPs count as committed: that money is already invested each month. If a SIP is for your goal, "
                           "leave SIPs at 0 here and include it in “Put aside” on the next step, so it isn't counted twice.")
                for lab_, k_, st_ in [("Rent", "rent", 1000), ("Loan EMIs", "emi", 1000), ("SIPs running", "sip", 1000), ("Insurance & bills", "bills", 500)]:
                    c1, c2 = st.columns([3.2, 1], vertical_alignment="bottom")
                    money(lab_, k_, 100000, st_, where=c1, ratio=(1.6, 1))
                    c2.number_input("Due day", min_value=1, max_value=28, step=1, key=k_ + "_day",
                                    help="Used for your payday runway: which days money leaves.")
            with tab3:
                money("Savings & FDs you could use in an emergency", "savings", 2000000, 10000)
                with st.expander("Optional · for your net worth"):
                    c1, c2 = st.columns(2)
                    c1.number_input("Investments", min_value=0, step=10000, key="invest", help="MFs, stocks, PF, NPS…")
                    c2.number_input("Credit card dues", min_value=0, step=1000, key="cards")
                    st.number_input("Loans outstanding", min_value=0, step=10000, key="loans")
                st.caption("Why we ask: savings set your emergency buffer (how long you could cope without salary); loans and dues give your net worth. A snapshot of today; FD and loan interest are not projected.")
        if free <= 0:
            st.error("Commitments and usual spending are more than your salary this month.")
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
    with right:
        delta = ""
        if last:
            d = free - num(last, "free")
            delta = (f'<div class="delta">{"▲" if d >= 0 else "▼"} {inr(abs(d))} vs {esc(last.get("month", "last check-in"))}'
                     f' · buffer {num(last, "buffer"):.1f} → {buffer_months:.1f} mo</div>')
        card(f'<div class="row"><span class="k">Free this month</span><span class="cap">of {inr(S.salary)} take-home</span></div>'
             f'<div class="num xl" style="margin-top:8px">{inr(free)}</div>'
             + bar3(committed, S.usual, max(free, 0), SPLIT_HERO, "20px 0 12px") +
             f'<div class="legend"><span><i style="background:{SPLIT_HERO[0]}"></i>Fixed expenses <b>{inr(committed)}</b></span>'
             f'<span><i style="background:{SPLIT_HERO[1]}"></i>Daily spending <b>{inr(S.usual)}</b></span>'
             f'<span><i style="background:{SPLIT_HERO[2]}"></i>Free <b>{inr(free)}</b></span></div>'
             f'<div class="cap" style="margin-top:8px">Rent {inr(S.rent)} · EMIs {inr(S.emi)} · SIPs {inr(S.sip)} · Insurance & bills {inr(S.bills)}</div>'
             + delta, "card hero")
        st.markdown(
            '<div class="kpis">'
            f'<div class="kpi"><div class="ic">{icon(I_CAL)}</div><div class="k">Everyday budget</div>'
            f'<div class="num md">{inr(daily_spend)}<span class="u">/day</span></div><div class="cap">till {next_salary.strftime("%d %b")}</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_TREND)}</div><div class="k">Net worth</div>'
            f'<div class="num md">{short_inr(net_worth)}</div><div class="cap">after loans and dues</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_WALLET)}</div><div class="k">Fixed expenses</div>'
            f'<div class="num md">{inr(committed)}</div><div class="cap">rent, EMIs, SIPs, bills</div></div>'
            f'<div class="kpi"><div class="ic">{icon(I_SHIELD)}</div><div class="k">Investments</div>'
            f'<div class="num md">{short_inr(S.invest)}</div><div class="cap">MFs, stocks, PF, NPS</div></div>'
            '</div>', unsafe_allow_html=True)
        card('<div class="gauge">'
             + gauge(buffer_months, 6, 3, "#1F8A5B" if buf_ok else "#B4462B", label=f"{buffer_months:.1f}", sub="months")
             + f'<div><div class="row" style="justify-content:flex-start;gap:10px"><span class="k">Emergency buffer</span>'
               f'<span class="pill {"ok" if buf_ok else "warn"}">{"Healthy" if buf_ok else "Thin"}</span></div>'
               f'<div class="cap" style="margin-top:8px;max-width:320px">If your salary stopped, your savings would pay rent, EMIs, bills and everyday '
               f'spending for <b>{buffer_months:.1f} months</b>. 3–6 months is the usual cushion; the dotted mark is 3.</div></div></div>')
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
            gcols = st.columns(len(S.goals) + 1)
            for i, g in enumerate(S.goals):
                gcols[i].button(g["goal_name"] or f"Goal {i + 1}", key=f"g{i}", width="stretch",
                                type="primary" if i == S.gi else "secondary", on_click=load_goal, args=(i,))
            gcols[-1].button("+ Add goal", key="gadd", width="stretch", on_click=add_goal)
            st.pills("What are you saving for?", ["Car", "Bike", "House", "Trip", "Gadget", "Wedding", "Other"],
                     key="goal_type")
            st.text_input("Name it", key="goal_name")
            money("Cost (₹)", "goal_cost", 5000000, 10000)
            gm_ = max(1, months_between(TODAY, S.goal_date))
            if S.get("goal_months__s") != gm_:
                S.goal_months__s = gm_
            d1, d2 = st.container(key="pair_goal_months").columns([2.2, 1], vertical_alignment="bottom", gap="small")
            d1.slider("When do you want it? (months from now)", 1, max(120, gm_), key="goal_months__s",
                      on_change=lambda: S.__setitem__("goal_date", add_months(TODAY, S.goal_months__s)))
            d2.date_input("Target date", min_value=add_months(TODAY, 1), key="goal_date", label_visibility="collapsed",
                          format="DD/MM/YYYY")
            money("Already saved (₹)", "goal_saved", max(int(S.goal_cost or 0), 100000), 10000)
            money("Put aside (₹/month)", "goal_monthly", max(200000, int(free)), 1000, help=f"You have {inr(free)} free this month.")
            if S.goal_monthly > free > 0:
                st.warning(f"That's more than the {inr(free)} you have free this month.")
            if len(S.goals) > 1:
                if total_goal_monthly > free > 0:
                    st.warning(f"All goals together need {inr(total_goal_monthly)} a month; you have {inr(free)} free.")
                st.button("Remove this goal", key="grm", type="tertiary", on_click=remove_goal)
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
          + (f", about {delay} month{'s' if delay != 1 else ''} late" if delay and delay > 0 else "")
          + ". The next step shows how investing the money changes this.")
    with left:
        explain("Explain in 2-3 sentences whether the person is on track for this goal and why, and what the gap "
                "means in months or rupees.", facts, fb, "AM I ON TRACK?")
    nav_buttons(1, 3, "See investment options")


# ═════════════════════════════════════════════════════════════
# 11. STEP 3: INVESTMENT OPTIONS (illustrative mixes; the user chooses)
# ═════════════════════════════════════════════════════════════
elif S.step == 3:
    title("Investment options", f"Three illustrative mixes for {inr(S.goal_monthly)} a month, and what each would need "
                                f"to reach {fmt_month(S.goal_date)} on time. You choose; nothing is recommended.")
    st.markdown('<div class="note-inline">White never invests or moves money. You invest through your own bank or fund app; '
                'this shows what each mix would do to your goal date, so you can choose before you do.</div>', unsafe_allow_html=True)
    stats = {n: mix_stats(n) for n in MIXES}
    left, right = st.columns([1.3, 1], gap="large")
    with left:
        with st.container(border=True):
            st.markdown(f'<div class="k" style="padding:6px 0 2px">Three quick questions</div>'
                        f'<div class="cap" style="margin-bottom:10px">Time to goal: <b>{goal_months} months</b>, taken from your goal'
                        f'{", which is short (under 3 years)" if goal_months <= 36 else ""}.</div>', unsafe_allow_html=True)
            QS = [("q_drop", "Risk appetite", "Your ₹1 lakh falls to ₹85,000 in a bad year. You would…",
                   ["Sell to stop losses", "Wait it out", "Invest more"]),
                  ("q_exp", "Experience", "How much have you invested before?", ["New to investing", "Some experience", "Experienced"]),
                  ("q_early", "Flexibility", "Could you need this money before the goal date?", ["Likely", "Maybe", "Unlikely"])]
            for qk, tag, qtext, opts in QS:                      # question on the left, answer on the right
                qa, qb = st.columns([1, 1.5], vertical_alignment="center")
                qa.markdown(f'<div class="cap" style="font-weight:700;color:#B8862B">{tag}</div>'
                            f'<div style="font-size:14px;font-weight:600;line-height:1.35">{qtext}</div>', unsafe_allow_html=True)
                qb.pills(qtext, opts, key=qk, label_visibility="collapsed")
            st.markdown(f'<div class="hair" style="margin:10px 0"></div><div class="row"><span class="k">Stated comfort</span>'
                        f'<span class="pill navy">{comfort}</span></div>'
                        f'<div class="cap" style="margin-top:6px;padding-bottom:6px">Goal is {goal_months} months away</div>', unsafe_allow_html=True)
        with st.expander("Assumptions (edit them)"):
            st.caption("Illustrative long-run yearly returns, not predictions. Bad year: debt +3%, equity −20%, "
                       "gold −5%. Ranges use equity at 4%–15%.")
            c1, c2, c3 = st.columns(3)
            c1.number_input("Debt %", 0.0, 20.0, step=0.5, key="r_debt")
            c2.number_input("Equity %", 0.0, 25.0, step=0.5, key="r_equity")
            c3.number_input("Gold %", 0.0, 20.0, step=0.5, key="r_gold")
    with right:
        with st.container(border=True):
            st.markdown(f'<div class="k" style="padding:6px 0 0">When each mix reaches {esc(S.goal_name)}</div>'
                        f'<div class="cap">Putting aside {inr(S.goal_monthly)} a month. Dot = expected date, bar = likely range '
                        f'from good to weak markets. Dashed line = your target ({fmt_month(S.goal_date)}).</div>',
                        unsafe_allow_html=True)
            range_chart(stats, S.goal_date, height=210)
    st.markdown('<div class="cap mob-only" style="margin:4px 0 -6px">Swipe to compare the three mixes →</div>',
                unsafe_allow_html=True)
    cols = st.columns(3)
    for col, n in zip(cols, MIXES):
        s = stats[n]
        sel = n == choice
        with col:
            st.markdown(
                f'<div class="opt{" sel" if sel else ""}" style="border-top-color:{MIX_COLOR[n]}">'
                f'<div class="name"><i style="background:{MIX_COLOR[n]}"></i>{n}</div>'
                + bar3(s["debt"], s["equity"], s["gold"], ALLOC, "14px 0 8px") +
                f'<div class="cap">Debt {s["debt"]} · Equity {s["equity"]} · Gold {s["gold"]}</div>'
                f'<div style="margin-top:10px"><div class="kv"><span>Goal reached</span><b>{s["goal_date"]}</b></div>'
                f'<div class="kv"><span>Vs your target</span><b class="{"warn" if (s["late"] or 1) > 0 else "good"}">{late_txt(s["late"])}</b></div>'
                f'<div class="kv"><span>Value by {fmt_month(S.goal_date)}</span><b>{short_inr(s["fv"])}</b></div>'
                f'<div class="kv"><span>To be on time</span><b>{inr(s["need_pm"])}/mo</b></div>'
                f'<div class="kv"><span>Bad-year fall</span><b>−{inr(s["drop_amt"])}</b></div>'
                f'<div class="kv"><span>Risk</span><b>{"●" * s["risk"]}{"○" * (5 - s["risk"])} {s["risk"]}/5</b></div></div>'
                f'<div class="foot"><span class="pill {"ok" if s["fits"] else "warn"}">'
                f'{"Fits comfort" if s["fits"] else "Above comfort"}</span>'
                + ('<div class="cap warn" style="margin-top:10px;font-weight:600">Short timeline: could be down when you need it.</div>'
                   if s["short_risk"] else '<div class="cap" style="margin-top:10px;visibility:hidden">Short timeline: could be down when you need it.</div>') + '</div></div>', unsafe_allow_html=True)
            st.button("Chosen ✓" if sel else f"Choose {n}", key=f"pick_{n}", width="stretch",
                      type="primary" if sel else "secondary", on_click=pick, args=(n,))
    explain("Compare the three mixes for this goal in 3-4 sentences: reaching the goal sooner vs the size of a "
            "bad-year dip vs the timeline. Mention the stated comfort. Do not pick one.",
            {"goal": S.goal_name, "target_date": fmt_month(S.goal_date), "months_left": goal_months,
             "monthly_amount": inr(S.goal_monthly), "stated_comfort": comfort,
             "emergency_buffer_months": round(buffer_months, 1),
             "options": {n: {"mix": f"debt {s['debt']}%, equity {s['equity']}%, gold {s['gold']}%",
                             "goal_reached": s["goal_date"], "likely_range": s["range"], "weak_year_dip_pct": s["dip"],
                             "needed_per_month_to_be_on_time": inr(s["need_pm"]),
                             "fits_comfort": s["fits"], "short_timeline_risk": s["short_risk"]} for n, s in stats.items()}},
            f"Steady is the smoothest ride (about {stats['Steady']['dip']}% in a weak year) and reaches the goal around "
            f"{stats['Steady']['goal_date']}. Growth could get there around {stats['Growth']['goal_date']} but could fall "
            f"about {abs(stats['Growth']['dip'])}% in a bad year"
            + (", which matters with a short timeline." if goal_months <= 36 else ".")
            + f" Balanced sits in between. Your stated comfort is {comfort.lower()}.",
            "COMPARING YOUR OPTIONS")
    st.markdown('<div class="cap" style="margin-bottom:12px"><b>Bad-year fall</b>: how much today\'s goal savings could drop in one bad '
                'market year with that mix; markets usually recover with time, which is why short timelines matter. '
                '<b>Risk 1–5</b> follows the share in equity. Illustrative mixes for your own decision. Not investment '
                'advice; no specific funds or stocks are suggested.</div>', unsafe_allow_html=True)
    nav_buttons(2, 4, f"Plan with {choice}")


# ═════════════════════════════════════════════════════════════
# 12. STEP 4: MY PLAN + "WHAT IF…?" DECISION CHECK
# ═════════════════════════════════════════════════════════════
elif S.step == 4:
    s = mix_stats(choice)
    left_after = free - total_goal_monthly
    title("Your plan for this month", "Does it work? If not, pick a plan that does. Then test a decision before you make it.")

    # ── verdict first: does this plan work, and if not, which realistic plans do
    r_ = s["exp_r"]
    other_goals = total_goal_monthly - (S.goal_monthly or 0)
    afford = max(0, int(free - other_goals))                              # most this goal can take this month
    late_m = s["late"]
    over = (S.goal_monthly or 0) > afford
    works = (late_m is not None and late_m <= 0) and not over
    def _ym(n):
        return "never at this pace" if n is None else (f"{n // 12} yr {n % 12} mo" if n >= 12 else f"{n} months")
    if works:
        head = (f'<b>This plan works.</b> {esc(S.goal_name)} lands around <b>{s["goal_date"]}</b>, on or before your '
                f'{fmt_month(S.goal_date)} target, and you keep <b>{inr(free - total_goal_monthly)}</b> free this month.')
        tone = "ok"
    else:
        probs = []
        if late_m is None or late_m > 0:
            probs.append(f'{esc(S.goal_name)} lands <b>{s["goal_date"]}</b>, <b>{_ym(late_m)}</b> after your {fmt_month(S.goal_date)} target')
        if over:
            probs.append(f'{inr(S.goal_monthly)} a month is <b>{inr(S.goal_monthly - afford)} more</b> than you have free after bills and other goals')
        head = "<b>This plan doesn't work yet.</b> " + "; and ".join(probs) + ". Pick one of these instead:"
        tone = "warn"
    st.markdown(f'<div class="verdict {tone}">{head}</div>', unsafe_allow_html=True)
    if not works:
        gm_ = max(1, goal_months)
        m_fit = min(S.goal_monthly or 0, afford) if over else (S.goal_monthly or 0)
        n_fit = months_to_goal(S.goal_saved, m_fit, S.goal_cost, r_) if m_fit > 0 else None
        cost_fit = int(path(S.goal_saved, m_fit, r_, gm_)[-1] // 1000 * 1000)
        n_max = months_to_goal(S.goal_saved, afford, S.goal_cost, r_) if afford > 0 else None
        d_fit = add_months(TODAY, n_fit) if n_fit else S.goal_date
        opts = [
            ("Keep the date", f"Put aside <b>{inr(s['need_pm'])}</b>/month", f"{fmt_month(S.goal_date)}, on time",
             s["need_pm"] <= afford,
             f"Needs {inr(s['need_pm'] - afford)} more than you have free" if s["need_pm"] > afford else "Fits your free money",
             [("goal_monthly", int(math.ceil(s["need_pm"] / 500) * 500))]),
            ("Move the date", f"<b>{inr(m_fit)}</b>/month" + (" (what fits)" if over else ""),
             fmt_month(d_fit) if n_fit else "not reachable", bool(n_fit) and m_fit > 0, "Same goal, later date",
             [("goal_monthly", m_fit), ("goal_date", d_fit)]),
            ("Lower the cost", f"A <b>{inr(cost_fit)}</b> {esc(S.goal_name.lower())}", f"by {fmt_month(S.goal_date)}",
             cost_fit > (S.goal_saved or 0) and m_fit > 0, f"{inr(S.goal_cost - cost_fit)} less, at {inr(m_fit)}/month",
             [("goal_monthly", m_fit), ("goal_cost", cost_fit)]),
        ]
        if over:
            cut = int(S.goal_monthly - afford)
            n_cut = months_to_goal(S.goal_saved, S.goal_monthly, S.goal_cost, r_)
            opts.append(("Spend less day to day", f"Cut <b>{inr(cut)}</b>/month from {inr(S.usual)}",
                         f"keep {inr(S.goal_monthly)}/month", cut <= S.usual * 0.5,
                         (f"Reaches {fmt_month(add_months(TODAY, n_cut))}" if n_cut else "") + (" · a big cut, check it is realistic" if cut > S.usual * 0.25 else ""),
                         [("usual", int(S.usual - cut))]))
        else:
            opts.append(("Put aside all that's free", f"<b>{inr(afford)}</b>/month",
                         fmt_month(add_months(TODAY, n_max)) if n_max else "not reachable", afford > 0 and bool(n_max),
                         "Fastest without borrowing", [("goal_monthly", afford)]))
        oc = st.columns(4, gap="small")
        def _apply(changes):
            for k, v in changes:
                S[k] = v
                if k == "goal_date":
                    S.goal_months__s = max(1, months_between(TODAY, v))
                elif k + "__s" in S:
                    S[k + "__s"] = v
            S.goals[S.gi] = {kk: S[kk] for kk in GOAL_KEYS}
        for col, (name, what, when, ok, note, changes) in zip(oc, opts):
            col.markdown(f'<div class="plan-opt {"" if ok else "dim"}"><div class="k">{name}</div><div class="what">{what}</div>'
                         f'<div class="when">{when}</div><div class="cap">{note}</div></div>', unsafe_allow_html=True)
            col.button("Use this plan", key=f"use_{name}", width="stretch", disabled=not ok, on_click=_apply, args=(changes,),
                       type="primary" if ok else "secondary")
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        card(f'<div class="row"><span class="k">{S.goal_name}</span><span class="pill">{choice} mix</span></div>'
             f'<div class="num xl" style="margin-top:8px">{inr(S.goal_monthly)}<span class="u">/month</span></div>'
             + bar3(s["debt"], s["equity"], s["gold"], ALLOC_HERO, "20px 0 10px") +
             f'<div class="legend"><span><i style="background:{ALLOC_HERO[0]}"></i>Debt <b>{s["debt"]}%</b></span>'
             f'<span><i style="background:{ALLOC_HERO[1]}"></i>Equity <b>{s["equity"]}%</b></span>'
             f'<span><i style="background:{ALLOC_HERO[2]}"></i>Gold <b>{s["gold"]}%</b></span></div>'
             f'<div class="hair"></div>'
             f'<div class="kv"><span>Expected to reach</span><b>{s["goal_date"]}</b></div>'
             f'<div class="kv"><span>Your target</span><b>{fmt_month(S.goal_date)}</b></div>'
             f'<div class="kv"><span>To be on time with this mix</span><b>{inr(s["need_pm"])}/mo</b></div>'
             f'<div class="kv"><span>Likely range</span><b>{s["range"]}</b></div>'
             f'<div class="kv"><span>Bad-year fall</span><b>about −{inr(s["drop_amt"])}</b></div>'
             f'<div class="kv"><span>Left free this month</span><b>{inr(left_after)}</b></div>'
             f'<div class="kv"><span>Next check-in</span><b>{next_salary.strftime("%d %b %Y")}</b></div>', "card hero")
        dd, ee, gg = s["debt"], s["equity"], s["gold"]
        parts = lambda amt: f'Debt {inr(amt * dd / 100)} · Equity {inr(amt * ee / 100)} · Gold {inr(amt * gg / 100)}'
        card(f'<div class="k">Where the goal money sits</div>'
             f'<div class="kv2"><span>This month\'s {inr(S.goal_monthly)}</span><b>{parts(S.goal_monthly)}</b></div>'
             f'<div class="kv2"><span>Already saved {short_inr(S.goal_saved)}</span><b>{parts(S.goal_saved)}</b></div>'
             f'<div class="kv"><span>Safety net, kept separate</span><b>{short_inr(S.savings)} · {buffer_months:.1f} months</b></div>'
             f'<div class="cap" style="margin-top:6px">Goal money and the emergency buffer stay apart, so a bad market year '
             f'or an emergency does not hit both.</div>')
        if s["months"] and s["months"] > goal_months:                 # ways back on track (calculated, not recommended)
            gap_m = s["months"] - goal_months
            i_m = s["exp_r"] / 12
            lump = max(0, S.goal_cost - s["fv"]) / ((1 + i_m) ** goal_months) if i_m else max(0, S.goal_cost - s["fv"])
            g_st = mix_stats("Growth")
            ways = [f'Put aside <b>{inr(s["need_pm"])}</b> a month (+{inr(s["need_pm"] - S.goal_monthly)})',
                    f'Add <b>{inr(lump)}</b> once, now', f'Move the target to <b>{s["goal_date"]}</b>']
            if choice != "Growth" and g_st["months"] and g_st["months"] < s["months"]:
                ways.append(f'Choose Growth: about <b>{g_st["goal_date"]}</b>, with a bigger bad-year fall')
            card(f'<div class="row"><span class="k">You miss {fmt_month(S.goal_date)} by {gap_m} month{"s" if gap_m != 1 else ""}</span>'
                 f'<span class="pill warn">Behind</span></div>'
                 f'<div class="cap" style="margin:6px 0 4px">Ways to get back on track. Calculated, not recommended; you choose.</div>'
                 + "".join(f'<div class="kv"><span>{w}</span></div>' for w in ways))
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
                money("Amount (₹)", "wi_amount", 100000, 1000, help="e.g. a phone, trip or repair")
                st.radio("Paid from", ["This month's goal money", "Emergency savings"], key="wi_from", horizontal=True)
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

        # ── tune the plan right here: every number above recalculates as you move these
        with st.container(key="tune"):
            st.markdown('<div class="row"><div><h3 style="margin:0;font-size:22px">Tune your plan</h3>'
                        '<div class="cap">Invested the goal money? Update what it is worth today. Behind? Try a bigger amount, a later date '
                        'or another mix. The plan updates as you move.</div></div></div>', unsafe_allow_html=True)
            t1 = t2 = st.container()
            with t1:
                money("Goal money worth today (₹)", "goal_saved", max(int(S.goal_cost or 0), 100000), 5000,
                      help="Check your bank or fund app; FD, RD and fund values all count.")
                money("Put aside (₹/month)", "goal_monthly", max(200000, int(free)), 1000)
            with t2:
                gm2 = max(1, months_between(TODAY, S.goal_date))
                if S.get("goal_months__s") != gm2:
                    S.goal_months__s = gm2
                st.slider("Target (months from now)", 1, max(120, gm2), key="goal_months__s",
                          on_change=lambda: S.__setitem__("goal_date", add_months(TODAY, S.goal_months__s)))
                if S.get("tune_mix") != choice:
                    S.tune_mix = choice
                st.segmented_control("Mix", list(MIXES), key="tune_mix",
                                     on_change=lambda: S.__setitem__("choice", S.tune_mix or S.choice))
            v_ok = s["late"] is not None and s["late"] <= 0
            verdict = ("On track" if v_ok else (f"{s['late']} month{'s' if s['late'] != 1 else ''} behind" if s["late"] else "Not reached"))
            st.markdown(f'<div class="tune-out"><span class="pill {"ok" if v_ok else "warn"}">{verdict}</span>'
                        f'<span>Expected <b>{s["goal_date"]}</b> vs target <b>{fmt_month(S.goal_date)}</b> · '
                        f'on time needs <b>{inr(s["need_pm"])}/month</b> · left free <b>{inr(free - total_goal_monthly)}</b></span></div>',
                        unsafe_allow_html=True)

    sim_section(choice, s)

    summary = (f"White · monthly plan · {TODAY.strftime('%d %b %Y')}\n\n"
               f"Goal: {S.goal_name} ({inr(S.goal_cost)}, target {fmt_month(S.goal_date)})\n"
               f"Monthly amount: {inr(S.goal_monthly)}\n"
               f"Chosen mix: {choice} (debt {s['debt']}%, equity {s['equity']}%, gold {s['gold']}%)\n"
               f"Expected: {s['goal_date']} · likely range {s['range']}\n"
               f"Free this month after goal: {inr(left_after)}\nEmergency buffer: {buffer_months:.1f} months\n"
               f"Next check-in: {next_salary.strftime('%d %b %Y')}\n\n{plan}\n\n"
               "Illustrative figures based on your inputs and editable assumptions. Not investment advice. "
               "You made this decision.\n")
    entry = {"date": TODAY.isoformat(), "month": TODAY.strftime("%b %Y"), "free": free, "buffer": round(buffer_months, 2),
             "net_worth": net_worth, "goal": S.goal_name, "goal_saved": S.goal_saved, "monthly": S.goal_monthly,
             "mix": choice, "expected": s["goal_date"],
             "inputs": {k: (S[k].isoformat() if k == "goal_date" else S[k]) for k in INPUT_KEYS},
             "goals": [{k: (v.isoformat() if k == "goal_date" else v) for k, v in g.items()} for g in S.goals]}
    already = bool(last) and last.get("month") == entry["month"]
    ics = ("BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//White//DPM2026 Gr09//EN\r\nBEGIN:VEVENT\r\n"
           f"UID:white-{S.salary_day}-{TODAY.isoformat()}@white.app\r\nDTSTAMP:{TODAY.strftime('%Y%m%d')}T000000Z\r\n"
           f"DTSTART;VALUE=DATE:{next_salary.strftime('%Y%m%d')}\r\nRRULE:FREQ=MONTHLY;BYMONTHDAY={min(S.salary_day, 28)}\r\n"
           "SUMMARY:White. salary-day check-in (10 min)\r\n"
           f"DESCRIPTION:Before the money moves: {S.goal_name.replace(',', ' ').replace(';', ' ')} needs {inr(monthly_needed(S.goal_saved, S.goal_cost, 0, months_between(TODAY, S.goal_date))).replace('₹', 'Rs ')} a month to be on time.\r\n"
           "BEGIN:VALARM\r\nTRIGGER:PT9H\r\nACTION:DISPLAY\r\nDESCRIPTION:Salary-day check-in\r\nEND:VALARM\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n")
    st.download_button("Remind me every salary day", ics, file_name="white-salary-day.ics", mime="text/calendar",
                       width="stretch", icon=":material/event_repeat:",
                       help="Adds a monthly reminder on your salary day to Google, Outlook or Apple Calendar.")
    s1, s2 = st.columns(2)
    s1.button("Update this month's check-in" if already else "Save this month's check-in", type="primary", width="stretch",
              on_click=save_checkin, args=(entry,), key="save",
              help="Kept only in this browser so next month you can compare. Nothing goes to a server.")
    s2.download_button("Download my plan", summary, file_name="white-plan.txt", width="stretch",
                       help="A plain-text copy of this page.")
    if S.just_saved:
        st.success(f"Saved in this browser as {entry['month']}. Next salary day, open White and pick "
                   "\"Use last month's numbers\".")
    d1, d2 = st.columns(2)
    d1.button("← Change something", width="stretch", on_click=go, args=(3,), key="back4")
    d2.button("Start over", width="stretch", on_click=go, args=(0,), key="restart")

_sx = mix_stats(choice)
_ctx = {"free": free, "left_free": free - total_goal_monthly, "buffer": buffer_months, "savings": S.savings, "essential": essential,
        "rent": S.rent, "rent_day": S.rent_day, "emi": S.emi, "emi_day": S.emi_day,
        "goal": {"name": S.goal_name, "cost": S.goal_cost, "saved": S.goal_saved, "monthly": S.goal_monthly,
                 "target": fmt_month(S.goal_date), "months": months_between(TODAY, S.goal_date)},
        "mix": {"name": choice, "date": _sx["goal_date"], "late": _sx["late"], "need_pm": _sx["need_pm"],
                "lump": (max(0, S.goal_cost - _sx["fv"]) / ((1 + _sx["exp_r"] / 12) ** months_between(TODAY, S.goal_date)))}}
_SUG = {0: ["Can I afford a ₹15,000 phone?", "What if my salary is 5 days late?", "Am I behind on my goal?"],
        1: ["What is my emergency buffer?", "Why is my SIP counted?", "Can I afford a ₹15,000 phone?"],
        2: ["Am I behind on my goal?", "How do I catch up?", "Can I afford a ₹20,000 trip?"],
        3: ["Should I change my strategy?", "Which fund should I buy?", "Am I behind on my goal?"],
        4: ["I have a ₹25,000 birthday trip next month. What changes?", "What if my salary is 5 days late?", "Should I change my strategy?"]}
assistant(_ctx, _SUG.get(S.step, _SUG[0]))

st.markdown('<div class="footer">No account linking · history only in your browser · you make every decision · '
            'DPM 2026 · Group 9 prototype</div>', unsafe_allow_html=True)
