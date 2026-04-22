"""
app.py — SpendSage: Ultra Advanced Expense Tracker
Merged · Smooth · User-Friendly · Advanced UI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import time

st.set_page_config(
    page_title="SpendSage",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

from suchat import chat_with_agent, get_quick_insight

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
  --bg:       #07090f;
  --s1:       #0d1117;
  --s2:       #131923;
  --s3:       #192130;
  --s4:       #1e293b;
  --border:   rgba(255,255,255,0.06);
  --border2:  rgba(255,255,255,0.11);
  --border3:  rgba(255,255,255,0.18);
  --gold:     #f5c842;
  --gold2:    #ffd97d;
  --gold3:    #ffe9a8;
  --green:    #22d98a;
  --green2:   #4ade80;
  --red:      #f8637a;
  --red2:     #fb9daa;
  --blue:     #60a5fa;
  --purple:   #a78bfa;
  --cyan:     #22d3ee;
  --text:     #edf2f8;
  --sub:      #94a3b8;
  --muted:    #546484;
  --radius:   14px;
  --radius2:  10px;
  --shadow:   0 4px 24px rgba(0,0,0,0.4);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased;
}

h1,h2,h3,h4 { font-family:'Syne',sans-serif !important; letter-spacing:-0.025em; }

/* ── Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton { visibility:hidden; display:none; }
[data-testid="stToolbar"] { display:none; }

/* ── Layout ── */
.main .block-container {
  padding: 1.5rem 2rem 3rem !important;
  max-width: 1440px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--s1) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; }

/* ── All Streamlit inputs ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea,
.stSelectbox > div > div, .stDateInput input,
.stMultiSelect > div > div {
  background: var(--s3) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--radius2) !important;
  color: var(--text) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.9rem !important;
  transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus,
.stTextArea textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(245,200,66,0.1) !important;
  outline: none !important;
}

/* ── Primary Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #f5c842 0%, #e8a800 100%) !important;
  color: #09090f !important;
  border: none !important;
  border-radius: var(--radius2) !important;
  font-weight: 700 !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.88rem !important;
  letter-spacing: 0.01em !important;
  padding: 0.55rem 1.4rem !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 2px 12px rgba(245,200,66,0.2) !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(245,200,66,0.38) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Secondary (ghost) button variant via key naming — override specific keys */
button[kind="secondary"] {
  background: var(--s3) !important;
  color: var(--sub) !important;
  border: 1px solid var(--border2) !important;
  box-shadow: none !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--s2) !important;
  border-radius: var(--radius) !important;
  padding: 5px !important;
  gap: 3px !important;
  border: 1px solid var(--border) !important;
  margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 10px !important;
  color: var(--muted) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  padding: 0.5rem 1.3rem !important;
  transition: all 0.2s !important;
  border: none !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text) !important; }
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg,#f5c842,#e8a800) !important;
  color: #09090f !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 10px rgba(245,200,66,0.25) !important;
}

/* ── Dataframe / table ── */
.stDataFrame { border-radius: var(--radius) !important; overflow:hidden; border: 1px solid var(--border) !important; }
.stDataFrame thead tr th {
  background: var(--s3) !important; color: var(--sub) !important;
  font-size: 0.78rem !important; text-transform:uppercase; letter-spacing:0.06em;
  border-bottom: 1px solid var(--border2) !important;
}
.stDataFrame tbody tr td { color: var(--text) !important; border-color: var(--border) !important; font-size:0.88rem !important; }
.stDataFrame tbody tr:hover td { background: var(--s3) !important; }

/* ── Selectbox dropdown ── */
[data-baseweb="popover"] { background: var(--s3) !important; border: 1px solid var(--border2) !important; border-radius:var(--radius2) !important; }
[data-baseweb="menu"] li { color: var(--sub) !important; font-size:0.9rem !important; }
[data-baseweb="menu"] li:hover { background: var(--s4) !important; color: var(--text) !important; }

/* ── Spinner ── */
.stSpinner > div > div { border-top-color: var(--gold) !important; }

/* ── Success / Error alerts ── */
.stSuccess { background: rgba(34,217,138,0.08) !important; border: 1px solid rgba(34,217,138,0.2) !important; border-radius:var(--radius2) !important; color:var(--green2) !important; }
.stError   { background: rgba(248,99,122,0.08) !important; border: 1px solid rgba(248,99,122,0.2) !important; border-radius:var(--radius2) !important; color:var(--red2) !important; }

/* ── Custom scrollbar ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--s1); }
::-webkit-scrollbar-thumb { background:var(--s4); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--muted); }

/* ════════════════════════════════════════
   COMPONENT CLASSES
   ════════════════════════════════════════ */

/* ── Metric Cards ── */
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.5rem; }
.kpi {
  background: var(--s1);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.3rem 1.5rem;
  position: relative;
  overflow: hidden;
  cursor: default;
  transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}
.kpi:hover {
  border-color: var(--border3);
  transform: translateY(-3px);
  box-shadow: var(--shadow);
}
.kpi::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  border-radius:2px 2px 0 0;
}
.kpi.inc::before  { background: linear-gradient(90deg,var(--green),var(--cyan)); }
.kpi.exp::before  { background: linear-gradient(90deg,var(--red),#ff9eb5); }
.kpi.bal::before  { background: linear-gradient(90deg,var(--gold),var(--gold2)); }
.kpi.sav::before  { background: linear-gradient(90deg,var(--purple),#c4b5fd); }
.kpi .k-label { font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); font-weight:700; margin-bottom:0.55rem; }
.kpi .k-val   { font-family:'Syne',sans-serif; font-size:1.9rem; font-weight:800; line-height:1; margin-bottom:0.35rem; }
.kpi.inc .k-val { color:var(--green); }
.kpi.exp .k-val { color:var(--red); }
.kpi.bal .k-val { color:var(--gold); }
.kpi.sav .k-val { color:var(--purple); }
.kpi .k-sub { font-size:0.78rem; color:var(--muted); }
.kpi .k-icon { position:absolute; right:1.2rem; top:50%; transform:translateY(-50%); font-size:2.4rem; opacity:0.07; pointer-events:none; }
.kpi .k-badge {
  display:inline-flex; align-items:center; gap:3px;
  margin-top:0.5rem; padding:2px 8px;
  border-radius:20px; font-size:0.68rem; font-weight:600;
}
.kpi.inc .k-badge { background:rgba(34,217,138,0.12); color:var(--green); }
.kpi.exp .k-badge { background:rgba(248,99,122,0.12); color:var(--red); }
.kpi.bal .k-badge { background:rgba(245,200,66,0.12); color:var(--gold); }
.kpi.sav .k-badge { background:rgba(167,139,250,0.12); color:var(--purple); }

/* ── Welcome Hero ── */
.hero {
  background: linear-gradient(135deg, #0d1829 0%, #0f1420 60%, #0d0f16 100%);
  border: 1px solid rgba(245,200,66,0.12);
  border-radius: 20px;
  padding: 2.2rem 2.8rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content:'';
  position:absolute; top:-60px; right:-60px;
  width:220px; height:220px; border-radius:50%;
  background: radial-gradient(circle, rgba(245,200,66,0.07) 0%, transparent 70%);
  pointer-events:none;
}
.hero::after {
  content:'💎';
  position:absolute; right:2.5rem; top:50%;
  transform:translateY(-50%);
  font-size:4.5rem; opacity:0.05; pointer-events:none;
}
.hero-title {
  font-family:'Syne',sans-serif;
  font-size:2rem; font-weight:800; line-height:1.1;
  background: linear-gradient(135deg,#f5c842 20%,#ffd97d 60%,#ffe9a8 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
  margin-bottom:0.4rem;
}
.hero-sub { color:var(--sub); font-size:0.95rem; line-height:1.5; }
.hero-pills { display:flex; gap:0.6rem; margin-top:1rem; flex-wrap:wrap; }
.pill {
  display:inline-flex; align-items:center; gap:5px;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.09);
  border-radius:20px; padding:4px 12px;
  font-size:0.78rem; color:var(--sub);
}
.pill.active { background:rgba(245,200,66,0.1); border-color:rgba(245,200,66,0.25); color:var(--gold); }

/* ── Section title ── */
.sec-title {
  display:flex; align-items:center; gap:8px;
  margin:0 0 0.9rem 0;
}
.sec-title .bar {
  width:3px; height:18px; border-radius:2px;
  background:linear-gradient(to bottom,var(--gold),var(--gold2));
  flex-shrink:0;
}
.sec-title span {
  font-family:'Syne',sans-serif;
  font-size:1rem; font-weight:700; color:var(--text);
}

/* ── Card wrapper ── */
.card {
  background:var(--s1);
  border:1px solid var(--border);
  border-radius:var(--radius);
  padding:1.3rem 1.5rem;
  transition: border-color 0.2s;
}
.card:hover { border-color:var(--border2); }

/* ── Transaction row ── */
.tr {
  display:flex; align-items:center; gap:0.9rem;
  padding:0.75rem 1rem; border-radius:12px;
  background:var(--s1); border:1px solid var(--border);
  margin-bottom:0.45rem;
  transition: background 0.15s, border-color 0.15s, transform 0.15s;
}
.tr:hover { background:var(--s2); border-color:var(--border2); transform:translateX(2px); }
.tr-ico {
  width:40px; height:40px; border-radius:11px;
  display:flex; align-items:center; justify-content:center;
  font-size:1.15rem; flex-shrink:0;
}
.tr-ico.inc { background:rgba(34,217,138,0.1); }
.tr-ico.exp { background:rgba(248,99,122,0.1); }
.tr-body { flex:1; min-width:0; }
.tr-name { font-weight:600; font-size:0.9rem; color:var(--text); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.tr-meta { font-size:0.74rem; color:var(--muted); margin-top:2px; display:flex; gap:6px; align-items:center; }
.tr-meta .dot { width:3px; height:3px; border-radius:50%; background:var(--muted); }
.tr-amt { font-family:'Syne',sans-serif; font-weight:700; font-size:0.98rem; flex-shrink:0; }
.tr-amt.inc { color:var(--green); }
.tr-amt.exp { color:var(--red); }
.tr-type-badge {
  padding:2px 8px; border-radius:6px; font-size:0.68rem; font-weight:700;
  text-transform:uppercase; letter-spacing:0.05em; flex-shrink:0;
}
.tr-type-badge.inc { background:rgba(34,217,138,0.1); color:var(--green); }
.tr-type-badge.exp { background:rgba(248,99,122,0.1); color:var(--red); }

/* ── AI Insight strip ── */
.ai-strip {
  display:flex; align-items:flex-start; gap:0.9rem;
  background:linear-gradient(135deg,rgba(245,200,66,0.05) 0%,rgba(167,139,250,0.05) 100%);
  border:1px solid rgba(245,200,66,0.18);
  border-radius:var(--radius); padding:1rem 1.4rem;
  margin-bottom:1.5rem;
}
.ai-strip .ai-icon { font-size:1.2rem; flex-shrink:0; margin-top:1px; }
.ai-strip .ai-text { font-size:0.88rem; color:var(--sub); line-height:1.65; }
.ai-strip .ai-text b { color:var(--gold); }

/* ── Category bar ── */
.cat-bar { margin-bottom:0.85rem; }
.cat-bar-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
.cat-bar-name { font-size:0.82rem; color:var(--sub); display:flex; align-items:center; gap:6px; }
.cat-bar-val  { font-size:0.82rem; font-weight:700; }
.cat-track { height:5px; border-radius:3px; background:var(--s3); overflow:hidden; }
.cat-fill  { height:100%; border-radius:3px; transition:width 0.6s ease; }

/* ── Chat UI ── */
.chat-wrap {
  max-height:480px; overflow-y:auto;
  padding:0.5rem 0 1rem 0;
  display:flex; flex-direction:column; gap:0;
}
.msg-user {
  display:flex; justify-content:flex-end;
  margin-bottom:0.8rem; padding:0 0.2rem;
}
.msg-user .bbl {
  background:linear-gradient(135deg,#1a3a5c,#0d2440);
  border:1px solid rgba(96,165,250,0.2);
  border-radius:18px 18px 4px 18px;
  padding:0.7rem 1.1rem;
  max-width:70%; font-size:0.9rem; line-height:1.65;
  color:#bcd6fa;
}
.msg-ai {
  display:flex; justify-content:flex-start;
  margin-bottom:0.8rem; gap:0.65rem; padding:0 0.2rem; align-items:flex-start;
}
.msg-ai .ava {
  width:34px; height:34px; border-radius:50%;
  background:linear-gradient(135deg,#f5c842,#e8a800);
  display:flex; align-items:center; justify-content:center;
  font-size:0.95rem; flex-shrink:0;
  box-shadow:0 3px 10px rgba(245,200,66,0.25);
  margin-top:2px;
}
.msg-ai .bbl {
  background:var(--s2);
  border:1px solid var(--border2);
  border-radius:4px 18px 18px 18px;
  padding:0.7rem 1.1rem;
  max-width:80%; font-size:0.9rem; line-height:1.7;
  color:var(--text);
}
.msg-ai .mdl { font-size:0.68rem; color:var(--muted); margin-top:4px; padding-left:2px; }

/* ── Prompt chip ── */
.prompt-chips { display:flex; flex-wrap:wrap; gap:0.5rem; margin-bottom:1.2rem; }
.pchip {
  display:inline-flex; align-items:center; gap:5px;
  background:var(--s2); border:1px solid var(--border2);
  border-radius:20px; padding:6px 14px;
  font-size:0.82rem; color:var(--sub); cursor:pointer;
  transition:all 0.2s;
}
.pchip:hover { background:var(--s3); border-color:var(--border3); color:var(--text); }

/* ── Stat badge row ── */
.stat-row {
  display:flex; align-items:center; justify-content:space-between;
  padding:0.5rem 0; border-bottom:1px solid var(--border);
  font-size:0.84rem;
}
.stat-row:last-child { border-bottom:none; }
.stat-row .s-label { color:var(--sub); }
.stat-row .s-val   { font-weight:700; color:var(--text); }

/* ── Empty state ── */
.empty-state {
  text-align:center; padding:4rem 2rem;
  background:var(--s1); border:1px solid var(--border);
  border-radius:var(--radius);
}
.empty-state .e-icon { font-size:3rem; margin-bottom:0.8rem; opacity:0.4; }
.empty-state .e-title { font-family:'Syne',sans-serif; font-size:1.1rem; color:var(--sub); margin-bottom:0.4rem; }
.empty-state .e-sub   { font-size:0.85rem; color:var(--muted); }

/* ── Sidebar inner layout ── */
.sb-logo {
  padding:1.6rem 1.4rem 1.2rem;
  border-bottom:1px solid var(--border);
  margin-bottom:0;
}
.sb-logo .logo-row { display:flex; align-items:center; gap:0.7rem; }
.sb-logo .logo-icon { font-size:1.8rem; }
.sb-logo .logo-name {
  font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  background-clip:text;
}
.sb-logo .logo-tag { font-size:0.72rem; color:var(--muted); margin-top:1px; }

.sb-nav { padding:1rem 0.8rem; }
.sb-nav-label { font-size:0.68rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); font-weight:700; padding:0 0.6rem; margin-bottom:0.4rem; margin-top:0.5rem; }

.sb-stats { margin:0 0.8rem 0.8rem; padding:1rem; background:var(--s2); border:1px solid var(--border); border-radius:var(--radius2); }

/* ── Form section card ── */
.form-section {
  background:var(--s1); border:1px solid var(--border);
  border-radius:var(--radius); padding:1.5rem;
}

/* ── Divider ── */
.divider { height:1px; background:var(--border); margin:1.2rem 0; }

/* ── Page header ── */
.page-hdr { margin-bottom:1.5rem; padding-bottom:1rem; border-bottom:1px solid var(--border); }
.page-hdr h2 { font-size:1.7rem !important; font-weight:800 !important; color:var(--text) !important; margin-bottom:0.2rem !important; }
.page-hdr p  { font-size:0.88rem; color:var(--muted); margin:0; }

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════
EXPENSE_CATS = [
    "Food & Dining","Transport","Shopping","Entertainment",
    "Health & Medical","Education","Rent & Housing","Utilities",
    "Travel","EMI / Loans","Personal Care","Subscriptions",
    "Gifts & Donations","Other",
]
INCOME_CATS = [
    "Salary","Freelance","Business","Investments",
    "Rental Income","Bonus","Side Hustle","Gift","Refund","Other",
]
CAT_ICONS = {
    "Food & Dining":"🍔","Transport":"🚗","Shopping":"🛍️",
    "Entertainment":"🎬","Health & Medical":"💊","Education":"📚",
    "Rent & Housing":"🏠","Utilities":"💡","Travel":"✈️",
    "EMI / Loans":"🏦","Personal Care":"💅","Subscriptions":"📱",
    "Gifts & Donations":"🎁","Other":"📦",
    "Salary":"💼","Freelance":"💻","Business":"🏢","Investments":"📈",
    "Rental Income":"🏘️","Bonus":"🎯","Side Hustle":"⚡",
    "Gift":"🎀","Refund":"↩️",
}
CHART_COLORS = ["#f5c842","#22d98a","#f8637a","#60a5fa","#a78bfa",
                "#fb923c","#34d399","#f472b6","#22d3ee","#facc15","#a3e635"]
PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#546484", size=12),
    margin=dict(l=8,r=8,t=36,b=8),
    legend=dict(bgcolor="rgba(13,17,23,0.8)",bordercolor="rgba(255,255,255,0.06)",
                borderwidth=1,font=dict(color="#94a3b8",size=11)),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.04)",
               tickfont=dict(color="#546484")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)",linecolor="rgba(255,255,255,0.04)",
               tickfont=dict(color="#546484")),
)
SAMPLE_DATA = [
    {"date":"2025-01-05","type":"Income","category":"Salary","amount":65000,"note":"Jan salary"},
    {"date":"2025-01-08","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Jan rent"},
    {"date":"2025-01-12","type":"Expense","category":"Food & Dining","amount":3200,"note":"Groceries + Zomato"},
    {"date":"2025-01-18","type":"Expense","category":"Transport","amount":1500,"note":"Uber + fuel"},
    {"date":"2025-01-22","type":"Expense","category":"Entertainment","amount":900,"note":"Netflix + movie"},
    {"date":"2025-01-28","type":"Expense","category":"Health & Medical","amount":1400,"note":"Pharmacy"},
    {"date":"2025-02-05","type":"Income","category":"Salary","amount":65000,"note":"Feb salary"},
    {"date":"2025-02-06","type":"Income","category":"Freelance","amount":12000,"note":"Design project"},
    {"date":"2025-02-10","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Feb rent"},
    {"date":"2025-02-14","type":"Expense","category":"Food & Dining","amount":4100,"note":"Valentines dinner"},
    {"date":"2025-02-20","type":"Expense","category":"Shopping","amount":5500,"note":"Clothes online"},
    {"date":"2025-02-25","type":"Expense","category":"Health & Medical","amount":2200,"note":"Doctor + tests"},
    {"date":"2025-02-27","type":"Expense","category":"Subscriptions","amount":1200,"note":"Prime + Spotify"},
    {"date":"2025-03-05","type":"Income","category":"Salary","amount":65000,"note":"Mar salary"},
    {"date":"2025-03-07","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Mar rent"},
    {"date":"2025-03-10","type":"Expense","category":"EMI / Loans","amount":8000,"note":"Car EMI"},
    {"date":"2025-03-15","type":"Expense","category":"Food & Dining","amount":3800,"note":"Restaurants"},
    {"date":"2025-03-20","type":"Expense","category":"Transport","amount":1800,"note":"Petrol + cab"},
    {"date":"2025-03-28","type":"Income","category":"Bonus","amount":10000,"note":"Performance bonus"},
    {"date":"2025-04-05","type":"Income","category":"Salary","amount":65000,"note":"Apr salary"},
    {"date":"2025-04-08","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Apr rent"},
    {"date":"2025-04-12","type":"Expense","category":"Shopping","amount":3200,"note":"Electronics"},
    {"date":"2025-04-18","type":"Expense","category":"Travel","amount":8500,"note":"Goa trip"},
    {"date":"2025-04-22","type":"Income","category":"Investments","amount":4200,"note":"Dividend"},
]

# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
def _init():
    defs = {
        "transactions":   [],
        "chat_dash":      [],
        "chat_txn":       [],
        "chat_ai":        [],
        "page":           "Dashboard",
        "ai_insight":     None,
        "ai_ts":          0,
        "show_add_form":  False,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════
def get_df() -> pd.DataFrame:
    if not st.session_state.transactions:
        return pd.DataFrame(columns=["date","type","category","amount","note"])
    df = pd.DataFrame(st.session_state.transactions)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False).reset_index(drop=True)

def stats(df):
    if df.empty:
        return 0.0, 0.0, 0.0, 0.0
    inc = df[df["type"]=="Income"]["amount"].sum()
    exp = df[df["type"]=="Expense"]["amount"].sum()
    bal = inc - exp
    sr  = (bal/inc*100) if inc > 0 else 0.0
    return inc, exp, bal, sr

def fmt(v: float) -> str:
    if v >= 1_00_00_000: return f"₹{v/1_00_00_000:.1f}Cr"
    if v >= 1_00_000:    return f"₹{v/1_00_000:.1f}L"
    if v >= 1_000:       return f"₹{int(v):,}"
    return f"₹{v:.0f}"

def sec(title: str):
    st.markdown(f'<div class="sec-title"><div class="bar"></div><span>{title}</span></div>', unsafe_allow_html=True)

def page_hdr(title: str, sub: str):
    st.markdown(f'<div class="page-hdr"><h2>{title}</h2><p>{sub}</p></div>', unsafe_allow_html=True)

def kpi_cards(inc, exp, bal, sr, df):
    n_inc = len(df[df["type"]=="Income"]) if not df.empty else 0
    n_exp = len(df[df["type"]=="Expense"]) if not df.empty else 0
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi inc">
        <div class="k-icon">💰</div>
        <div class="k-label">Total Income</div>
        <div class="k-val">{fmt(inc)}</div>
        <div class="k-sub">{n_inc} transaction{'s' if n_inc!=1 else ''}</div>
        <span class="k-badge">↑ Income</span>
      </div>
      <div class="kpi exp">
        <div class="k-icon">💸</div>
        <div class="k-label">Total Expenses</div>
        <div class="k-val">{fmt(exp)}</div>
        <div class="k-sub">{n_exp} transaction{'s' if n_exp!=1 else ''}</div>
        <span class="k-badge">↓ Expenses</span>
      </div>
      <div class="kpi bal">
        <div class="k-icon">⚖️</div>
        <div class="k-label">Net Balance</div>
        <div class="k-val">{fmt(abs(bal))}</div>
        <div class="k-sub">{'Surplus' if bal>=0 else 'Deficit'}</div>
        <span class="k-badge">{'✓ Positive' if bal>=0 else '⚠ Negative'}</span>
      </div>
      <div class="kpi sav">
        <div class="k-icon">🎯</div>
        <div class="k-label">Savings Rate</div>
        <div class="k-val">{sr:.1f}%</div>
        <div class="k-sub">Of total income</div>
        <span class="k-badge">{'✓ Healthy' if sr>=20 else '⚠ Low' if sr<10 else '~ Moderate'}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

def txn_row(row):
    icon    = CAT_ICONS.get(row["category"], "📦")
    cls     = "inc" if row["type"]=="Income" else "exp"
    prefix  = "+" if row["type"]=="Income" else "−"
    note    = str(row.get("note","")) if row.get("note") else ""
    note_part = f'<span class="dot"></span><span>{note[:28]}{"…" if len(note)>28 else ""}</span>' if note else ""
    st.markdown(f"""
    <div class="tr">
      <div class="tr-ico {cls}">{icon}</div>
      <div class="tr-body">
        <div class="tr-name">{row['category']}</div>
        <div class="tr-meta">
          <span>{row['date'].strftime('%d %b %Y')}</span>
          {note_part}
        </div>
      </div>
      <span class="tr-type-badge {cls}">{row['type']}</span>
      <div class="tr-amt {cls}">{prefix}{fmt(row['amount'])}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CHATBOT COMPONENT
# ══════════════════════════════════════════════════════════════
def chatbot(history_key: str, compact: bool = False):
    hist = st.session_state[history_key]

    # ── Suggested chips (only if empty) ──────────────────────
    if not hist:
        chips = ["💸 Top spending categories?","📅 Monthly expense comparison",
                 "💡 How to save more?","🎯 Budget plan suggestion",
                 "📊 Kitna income aur expense hua?","⚠️ Unusual transactions?"]
        cols  = st.columns(3)
        for i, chip in enumerate(chips):
            with cols[i % 3]:
                if st.button(chip, key=f"chip_{history_key}_{i}", use_container_width=True):
                    clean = chip.split(" ",1)[1] if " " in chip else chip
                    hist.append({"role":"user","content":clean})
                    with st.spinner("SpendSage AI soch raha hai..."):
                        resp, mdl = chat_with_agent(clean, [], st.session_state.transactions)
                    hist.append({"role":"assistant","content":resp,"model":mdl})
                    st.rerun()
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Chat history ─────────────────────────────────────────
    if hist:
        bubbles = ""
        for m in hist:
            if m["role"] == "user":
                bubbles += f'<div class="msg-user"><div class="bbl">{m["content"]}</div></div>'
            else:
                mdl = m.get("model","")
                bubbles += f'''<div class="msg-ai">
                  <div class="ava">💎</div>
                  <div>
                    <div class="bbl">{m["content"]}</div>
                    <div class="mdl">via {mdl}</div>
                  </div>
                </div>'''
        st.markdown(f'<div class="chat-wrap">{bubbles}</div>', unsafe_allow_html=True)

    # ── Input row ─────────────────────────────────────────────
    ci, cb, cc = st.columns([6,1,1])
    with ci:
        inp = st.text_input("msg", placeholder="Kuch bhi pucho apne finances ke baare mein...",
                            label_visibility="collapsed", key=f"inp_{history_key}")
    with cb:
        send = st.button("Send ➤", key=f"snd_{history_key}", use_container_width=True)
    with cc:
        if st.button("Clear", key=f"clr_{history_key}", use_container_width=True):
            st.session_state[history_key] = []
            st.rerun()

    if send and inp.strip():
        hist.append({"role":"user","content":inp.strip()})
        with st.spinner("SpendSage AI soch raha hai..."):
            resp, mdl = chat_with_agent(inp.strip(), hist[:-1], st.session_state.transactions)
        hist.append({"role":"assistant","content":resp,"model":mdl})
        st.rerun()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sb-logo">
      <div class="logo-row">
        <span class="logo-icon">💎</span>
        <div>
          <div class="logo-name">SpendSage</div>
          <div class="logo-tag">Smart Expense Intelligence</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="sb-nav">', unsafe_allow_html=True)
    st.markdown('<div class="sb-nav-label">Navigation</div>', unsafe_allow_html=True)

    nav_items = {
        "Dashboard":    "🏠  Dashboard",
        "Transactions": "💳  Transactions",
        "Analytics":    "📊  Analytics",
        "AI Assistant": "🤖  AI Assistant",
    }
    page = st.radio("nav", list(nav_items.values()),
                    label_visibility="collapsed",
                    index=list(nav_items.keys()).index(st.session_state.page))
    # Map back to key
    st.session_state.page = {v:k for k,v in nav_items.items()}[page]
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Quick mini-stats
    df_sb = get_df()
    if not df_sb.empty:
        inc_sb, exp_sb, bal_sb, _ = stats(df_sb)
        st.markdown(f"""
        <div class="sb-stats">
          <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:700;margin-bottom:0.7rem">Live Summary</div>
          <div class="stat-row"><span class="s-label">Income</span><span class="s-val" style="color:var(--green)">{fmt(inc_sb)}</span></div>
          <div class="stat-row"><span class="s-label">Expenses</span><span class="s-val" style="color:var(--red)">{fmt(exp_sb)}</span></div>
          <div class="stat-row"><span class="s-label">Balance</span><span class="s-val" style="color:var(--gold)">{fmt(bal_sb)}</span></div>
          <div class="stat-row"><span class="s-label">Records</span><span class="s-val">{len(df_sb)}</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Sample data
    if st.button("🎲 Load Sample Data", use_container_width=True, key="sb_sample"):
        st.session_state.transactions.extend(SAMPLE_DATA)
        st.session_state.ai_insight = None
        st.rerun()

    if st.session_state.transactions:
        if st.button("🗑️ Clear All Data", use_container_width=True, key="sb_clear"):
            st.session_state.transactions = []
            st.session_state.ai_insight   = None
            st.rerun()

    # API Key status
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    g_key = st.secrets.get("GOOGLE_API_KEY","")
    q_key = st.secrets.get("GROQ_API_KEY","")
    g_ok  = "🟢" if g_key else "🔴"
    q_ok  = "🟢" if q_key else "🔴"
    st.markdown(f"""
    <div style="padding:0 0.8rem 1rem">
      <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:700;margin-bottom:0.5rem">AI Status</div>
      <div style="font-size:0.78rem;color:var(--sub);margin-bottom:3px">{g_ok} Gemini 2.5 Flash</div>
      <div style="font-size:0.78rem;color:var(--sub)">{q_ok} Groq Llama-3.3</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_dashboard():
    df = get_df()
    inc, exp, bal, sr = stats(df)
    now = datetime.now()

    # Hero
    greet = "Good Morning 🌅" if now.hour<12 else ("Good Afternoon ☀️" if now.hour<17 else "Good Evening 🌙")
    n_txn = len(df)
    date_str = now.strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="hero">
      <div class="hero-title">💎 SpendSage</div>
      <div class="hero-sub">{greet} &nbsp;·&nbsp; {date_str}</div>
      <div class="hero-sub" style="margin-top:0.3rem">
        Your complete financial overview — income, expenses, savings, and AI insights all in one place.
      </div>
      <div class="hero-pills">
        <span class="pill active">✅ {n_txn} Transactions</span>
        <span class="pill">💰 Income: {fmt(inc)}</span>
        <span class="pill">💸 Expenses: {fmt(exp)}</span>
        <span class="pill {'active' if sr>=20 else ''}">🎯 Savings: {sr:.1f}%</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    kpi_cards(inc, exp, bal, sr, df)

    # AI Insight strip
    if not df.empty:
        now_ts = time.time()
        if st.session_state.ai_insight is None or (now_ts - st.session_state.ai_ts) > 300:
            with st.spinner(""):
                st.session_state.ai_insight = get_quick_insight(st.session_state.transactions)
                st.session_state.ai_ts = now_ts
        st.markdown(f"""
        <div class="ai-strip">
          <span class="ai-icon">✨</span>
          <div class="ai-text"><b>AI Insight:</b> {st.session_state.ai_insight}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Charts Row ────────────────────────────────────────────
    col_chart, col_pie = st.columns([3,2])

    with col_chart:
        sec("Monthly Income vs Expenses")
        if not df.empty:
            df2 = df.copy()
            df2["month"] = df2["date"].dt.to_period("M").dt.start_time
            mi = df2[df2["type"]=="Income"].groupby("month")["amount"].sum().reset_index()
            me = df2[df2["type"]=="Expense"].groupby("month")["amount"].sum().reset_index()
            mi["type"]="Income"; me["type"]="Expense"
            all_m = pd.concat([mi,me])
            fig = px.bar(all_m, x="month", y="amount", color="type", barmode="group",
                         color_discrete_map={"Income":"#22d98a","Expense":"#f8637a"},
                         template="plotly_dark")
            fig.update_layout(**PLOTLY_BASE, height=260,
                              title=dict(text="",x=0))
            fig.update_traces(marker_cornerradius=6,
                              hovertemplate="<b>%{x|%b %Y}</b><br>₹%{y:,.0f}<extra></extra>")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown('<div class="empty-state"><div class="e-icon">📊</div><div class="e-title">No chart data yet</div><div class="e-sub">Add transactions to see your monthly overview</div></div>', unsafe_allow_html=True)

    with col_pie:
        sec("Expense Breakdown")
        exp_df = df[df["type"]=="Expense"] if not df.empty else pd.DataFrame()
        if not exp_df.empty:
            cat_g = exp_df.groupby("category")["amount"].sum().reset_index()
            fig2 = go.Figure(go.Pie(
                labels=cat_g["category"], values=cat_g["amount"],
                hole=0.6,
                marker=dict(colors=CHART_COLORS[:len(cat_g)],
                            line=dict(color="rgba(0,0,0,0)",width=0)),
                textinfo="percent",
                textfont=dict(size=11,color="#546484"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
            ))
            fig2.update_layout(**PLOTLY_BASE, height=260, showlegend=True,
                               legend=dict(**PLOTLY_BASE["legend"],
                                           orientation="v", x=1.02, y=0.5),
                               annotations=[dict(
                                   text=f"<b>{fmt(exp)}</b>",
                                   x=0.5, y=0.5, font=dict(size=15,color="#edf2f8"),
                                   showarrow=False)])
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown('<div class="empty-state"><div class="e-icon">🍩</div><div class="e-title">No expenses yet</div><div class="e-sub">Add expense transactions to see breakdown</div></div>', unsafe_allow_html=True)

    # ── Bottom Row: Recent txns + Top categories ──────────────
    col_recent, col_cats = st.columns([3,2])

    with col_recent:
        sec("Recent Transactions")
        if not df.empty:
            for _, row in df.head(7).iterrows():
                txn_row(row)
            if len(df) > 7:
                st.markdown(f"<p style='font-size:0.8rem;color:var(--muted);text-align:center;margin-top:0.5rem'>+{len(df)-7} more — view all in Transactions tab</p>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="e-icon">💳</div><div class="e-title">No transactions yet</div><div class="e-sub">Use the sidebar or Transactions page to add one</div></div>', unsafe_allow_html=True)

    with col_cats:
        sec("Top Expense Categories")
        if not df.empty and not df[df["type"]=="Expense"].empty:
            top5 = df[df["type"]=="Expense"].groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
            max_v = top5.max()
            for i,(cat,amt) in enumerate(top5.items()):
                pct   = amt/max_v*100 if max_v>0 else 0
                color = CHART_COLORS[i]
                icon  = CAT_ICONS.get(cat,"📦")
                st.markdown(f"""
                <div class="cat-bar">
                  <div class="cat-bar-top">
                    <span class="cat-bar-name">{icon} {cat}</span>
                    <span class="cat-bar-val" style="color:{color}">{fmt(amt)}</span>
                  </div>
                  <div class="cat-track"><div class="cat-fill" style="width:{pct:.1f}%;background:{color}"></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state"><div class="e-icon">🏆</div><div class="e-title">No categories yet</div></div>', unsafe_allow_html=True)

    # ── Dashboard Chatbot ─────────────────────────────────────
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    sec("💬 Ask AI About Your Finances")
    st.markdown("<p style='font-size:0.83rem;color:var(--muted);margin-top:-0.5rem;margin-bottom:1rem'>Poora data AI ke paas hai — kuch bhi pucho Hindi/English mein</p>", unsafe_allow_html=True)
    chatbot("chat_dash")


# ══════════════════════════════════════════════════════════════
#  PAGE: TRANSACTIONS
# ══════════════════════════════════════════════════════════════
def page_transactions():
    page_hdr("💳 Transactions", "Add, manage and analyze all your income & expense records")

    tab_add, tab_list, tab_chat = st.tabs(["➕  Add Transaction", "📋  All Records", "🤖  AI Assistant"])

    # ── TAB 1: Add ─────────────────────────────────────────────
    with tab_add:
        col_f, col_r = st.columns([3,2], gap="large")

        with col_f:
            sec("New Transaction")
            with st.form("add_form", clear_on_submit=True):
                r1, r2 = st.columns(2)
                with r1:
                    txn_type = st.selectbox("Type", ["Expense","Income"])
                with r2:
                    txn_date = st.date_input("Date", value=date.today())
                r3, r4 = st.columns(2)
                with r3:
                    cats = EXPENSE_CATS if txn_type=="Expense" else INCOME_CATS
                    txn_cat = st.selectbox("Category", cats)
                with r4:
                    txn_amt = st.number_input("Amount (₹)", min_value=0.01, step=100.0, format="%.2f")
                txn_note = st.text_area("Note / Description", height=72,
                                        placeholder="e.g. Salary credit, Zomato dinner, Car EMI...")
                submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

            if submitted:
                if txn_amt > 0:
                    st.session_state.transactions.append({
                        "date":     str(txn_date),
                        "type":     txn_type,
                        "category": txn_cat,
                        "amount":   float(txn_amt),
                        "note":     txn_note.strip(),
                    })
                    st.session_state.ai_insight = None
                    st.success(f"✅ {txn_type} of {fmt(txn_amt)} saved to {txn_cat}!")
                else:
                    st.error("Amount must be greater than ₹0")

        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            sec("Quick Actions")

            df_r = get_df()
            if not df_r.empty:
                inc_r, exp_r, bal_r, sr_r = stats(df_r)
                st.markdown(f"""
                <div class="card" style="margin-bottom:1rem">
                  <div class="stat-row"><span class="s-label">Total Records</span><span class="s-val">{len(df_r)}</span></div>
                  <div class="stat-row"><span class="s-label">Income entries</span><span class="s-val" style="color:var(--green)">{len(df_r[df_r['type']=='Income'])}</span></div>
                  <div class="stat-row"><span class="s-label">Expense entries</span><span class="s-val" style="color:var(--red)">{len(df_r[df_r['type']=='Expense'])}</span></div>
                  <div class="stat-row"><span class="s-label">Net Balance</span><span class="s-val" style="color:var(--gold)">{fmt(bal_r)}</span></div>
                </div>
                """, unsafe_allow_html=True)

            if st.button("🎲 Load Sample Data", use_container_width=True, key="txn_sample"):
                st.session_state.transactions.extend(SAMPLE_DATA)
                st.session_state.ai_insight = None
                st.success("✅ Sample data loaded!")
                st.rerun()

            st.markdown("""
            <div class="card" style="margin-top:1rem">
              <div style="font-size:0.78rem;color:var(--muted);line-height:1.6">
                <b style="color:var(--sub)">💡 Tips:</b><br>
                • Add transactions regularly for accurate insights<br>
                • Use specific notes for better AI analysis<br>
                • Try loading sample data to explore features
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 2: All Records ─────────────────────────────────────
    with tab_list:
        df = get_df()
        if df.empty:
            st.markdown('<div class="empty-state"><div class="e-icon">💳</div><div class="e-title">No transactions yet</div><div class="e-sub">Add some using the Add Transaction tab</div></div>', unsafe_allow_html=True)
        else:
            # Filters
            f1,f2,f3,f4,f5 = st.columns([1.5,2,1.5,1.5,1])
            with f1:
                f_type = st.selectbox("Type", ["All","Income","Expense"], key="ft")
            with f2:
                ucats = ["All"] + sorted(df["category"].unique().tolist())
                f_cat = st.selectbox("Category", ucats, key="fc")
            with f3:
                f_from = st.date_input("From", value=df["date"].min().date(), key="ff")
            with f4:
                f_to   = st.date_input("To",   value=df["date"].max().date(), key="fe")
            with f5:
                f_sort = st.selectbox("Sort", ["Newest","Oldest","Highest","Lowest"], key="fs")

            fdf = df.copy()
            if f_type != "All":   fdf = fdf[fdf["type"]==f_type]
            if f_cat  != "All":   fdf = fdf[fdf["category"]==f_cat]
            fdf = fdf[(fdf["date"].dt.date>=f_from)&(fdf["date"].dt.date<=f_to)]
            if f_sort=="Oldest":  fdf = fdf.sort_values("date",ascending=True)
            elif f_sort=="Highest": fdf = fdf.sort_values("amount",ascending=False)
            elif f_sort=="Lowest":  fdf = fdf.sort_values("amount",ascending=True)

            # Filter stats
            fi,fe,fb,_ = stats(fdf)
            st.markdown(f"""
            <div style="display:flex;gap:1rem;margin-bottom:1rem;flex-wrap:wrap">
              <span style="font-size:0.82rem;color:var(--muted)">Showing <b style="color:var(--text)">{len(fdf)}</b> of {len(df)} records</span>
              <span style="font-size:0.82rem;color:var(--green)">+{fmt(fi)}</span>
              <span style="font-size:0.82rem;color:var(--red)">−{fmt(fe)}</span>
              <span style="font-size:0.82rem;color:var(--gold)">Balance: {fmt(fb)}</span>
            </div>
            """, unsafe_allow_html=True)

            for _, row in fdf.iterrows():
                txn_row(row)

            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            c_del,_ = st.columns([2,5])
            with c_del:
                if st.button("🗑️ Delete All Records", key="del_all", use_container_width=True):
                    st.session_state.transactions = []
                    st.session_state.ai_insight   = None
                    st.rerun()

    # ── TAB 3: AI ──────────────────────────────────────────────
    with tab_chat:
        sec("🤖 AI Assistant — Transactions Analysis")
        st.markdown("<p style='font-size:0.83rem;color:var(--muted);margin-top:-0.4rem;margin-bottom:1.2rem'>Specific transactions, date ranges, category trends — sab pucho</p>", unsafe_allow_html=True)
        chatbot("chat_txn")


# ══════════════════════════════════════════════════════════════
#  PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════
def page_analytics():
    page_hdr("📊 Analytics", "Deep-dive into your spending patterns, trends and category breakdowns")

    df = get_df()
    if df.empty:
        st.markdown('<div class="empty-state"><div class="e-icon">📊</div><div class="e-title">No data to analyze</div><div class="e-sub">Add transactions to unlock full analytics</div></div>', unsafe_allow_html=True)
        return

    inc, exp, bal, sr = stats(df)
    kpi_cards(inc, exp, bal, sr, df)

    # ── Row 1: Trend + Inc vs Exp pie ─────────────────────────
    c1,c2 = st.columns([3,2])
    with c1:
        sec("📈 Weekly Expense Trend")
        df_we = df[df["type"]=="Expense"].copy()
        if not df_we.empty:
            weekly = df_we.groupby(df_we["date"].dt.to_period("W").dt.start_time)["amount"].sum().reset_index()
            weekly.columns = ["week","amount"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=weekly["week"], y=weekly["amount"],
                fill="tozeroy",
                fillcolor="rgba(248,99,122,0.07)",
                line=dict(color="#f8637a",width=2.5),
                mode="lines+markers",
                marker=dict(size=6,color="#f8637a",
                            line=dict(color="#f8637a",width=2)),
                hovertemplate="<b>Week of %{x|%d %b}</b><br>₹%{y:,.0f}<extra></extra>",
            ))
            fig.update_layout(**PLOTLY_BASE, height=270)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        sec("⚖️ Income vs Expenses")
        fig2 = go.Figure(go.Pie(
            labels=["Income","Expenses"],
            values=[max(inc,1), max(exp,1)],
            hole=0.58,
            marker=dict(colors=["#22d98a","#f8637a"],
                        line=dict(color="rgba(0,0,0,0)",width=0)),
            textinfo="label+percent",
            textfont=dict(size=12,color="#546484"),
            hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
        ))
        fig2.update_layout(**PLOTLY_BASE, height=270, showlegend=False,
                           annotations=[dict(
                               text=f"<b>{fmt(bal)}</b><br><span style='font-size:9px'>balance</span>",
                               x=0.5, y=0.5, font=dict(size=14,color="#edf2f8"), showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    # ── Row 2: Treemap + Savings bar ──────────────────────────
    c3,c4 = st.columns(2)
    with c3:
        sec("🗂️ Category Heatmap (Expenses)")
        cat_df = df[df["type"]=="Expense"].groupby("category")["amount"].sum().reset_index()
        if not cat_df.empty:
            fig3 = px.treemap(
                cat_df, path=["category"], values="amount",
                color="amount",
                color_continuous_scale=["#131923","#1e293b","#f5c842"],
                template="plotly_dark",
                hover_data={"amount":":.0f"},
            )
            fig3.update_layout(**PLOTLY_BASE, height=300,
                               coloraxis_showscale=False)
            fig3.update_traces(
                textinfo="label+value",
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>",
                textfont=dict(size=13,color="#edf2f8"),
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

    with c4:
        sec("💰 Monthly Savings")
        df2 = df.copy()
        df2["m"] = df2["date"].dt.to_period("M")
        m_inc = df2[df2["type"]=="Income"].groupby("m")["amount"].sum()
        m_exp = df2[df2["type"]=="Expense"].groupby("m")["amount"].sum()
        m_sav = (m_inc - m_exp).fillna(0).reset_index()
        m_sav.columns = ["m","savings"]
        m_sav["label"] = m_sav["m"].dt.strftime("%b %Y")
        m_sav["color"] = m_sav["savings"].apply(lambda x:"#22d98a" if x>=0 else "#f8637a")
        if not m_sav.empty:
            fig4 = go.Figure(go.Bar(
                x=m_sav["label"], y=m_sav["savings"],
                marker_color=m_sav["color"],
                marker_cornerradius=6,
                hovertemplate="<b>%{x}</b><br>Savings: ₹%{y:,.0f}<extra></extra>",
            ))
            fig4.update_layout(**PLOTLY_BASE, height=300)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})

    # ── Row 3: Full monthly grouped bar + income categories ───
    c5,c6 = st.columns(2)
    with c5:
        sec("📅 Income Category Breakdown")
        inc_df = df[df["type"]=="Income"].groupby("category")["amount"].sum().reset_index()
        if not inc_df.empty:
            fig5 = go.Figure(go.Bar(
                x=inc_df["category"], y=inc_df["amount"],
                marker_color=CHART_COLORS[:len(inc_df)],
                marker_cornerradius=6,
                hovertemplate="<b>%{x}</b><br>₹%{y:,.0f}<extra></extra>",
            ))
            fig5.update_layout(**PLOTLY_BASE, height=280,
                               xaxis_tickangle=-30)
            st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar":False})

    with c6:
        sec("📋 Category Summary")
        cat_sum = df.groupby(["type","category"])["amount"].agg(["sum","count"]).reset_index()
        cat_sum.columns = ["Type","Category","Total","Count"]
        cat_sum["Total"] = cat_sum["Total"].apply(lambda x:f"₹{x:,.0f}")
        st.dataframe(
            cat_sum, use_container_width=True, hide_index=True, height=280,
            column_config={
                "Type":     st.column_config.TextColumn("Type",width=80),
                "Category": st.column_config.TextColumn("Category",width=150),
                "Total":    st.column_config.TextColumn("Total",width=110),
                "Count":    st.column_config.NumberColumn("Txns",width=60),
            }
        )


# ══════════════════════════════════════════════════════════════
#  PAGE: AI ASSISTANT
# ══════════════════════════════════════════════════════════════
def page_ai():
    page_hdr("🤖 AI Financial Assistant",
             "Powered by Google Gemini 2.5 Flash · Groq Llama-3.3 fallback · Hindi/English/Hinglish")

    df = get_df()
    inc, exp, bal, sr = stats(df)

    # Context bar
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;margin-bottom:1.5rem">
      <div style="background:var(--s1);border:1px solid var(--border);border-radius:var(--radius2);padding:0.9rem;text-align:center">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:4px">Income</div>
        <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:var(--green)">{fmt(inc)}</div>
      </div>
      <div style="background:var(--s1);border:1px solid var(--border);border-radius:var(--radius2);padding:0.9rem;text-align:center">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:4px">Expenses</div>
        <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:var(--red)">{fmt(exp)}</div>
      </div>
      <div style="background:var(--s1);border:1px solid var(--border);border-radius:var(--radius2);padding:0.9rem;text-align:center">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:4px">Balance</div>
        <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:var(--gold)">{fmt(bal)}</div>
      </div>
      <div style="background:var(--s1);border:1px solid var(--border);border-radius:var(--radius2);padding:0.9rem;text-align:center">
        <div style="font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);margin-bottom:4px">Records</div>
        <div style="font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:var(--purple)">{len(df)}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Mini charts next to chat
    col_chat, col_info = st.columns([3,1])

    with col_chat:
        sec("💬 Chat with SpendSage AI")
        chatbot("chat_ai")

    with col_info:
        sec("Quick Topics")
        topics = [
            ("📊","Spending analysis"),("💡","Savings tips"),
            ("📅","Monthly trends"),("🎯","Budget planning"),
            ("⚠️","Overspending alert"),("🏦","EMI management"),
        ]
        for icon,label in topics:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:0.55rem 0.8rem;
                        border-radius:8px;background:var(--s2);border:1px solid var(--border);
                        margin-bottom:6px;cursor:default">
              <span style="font-size:1rem">{icon}</span>
              <span style="font-size:0.82rem;color:var(--sub)">{label}</span>
            </div>""", unsafe_allow_html=True)

        if not df.empty:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            sec("Data Context")
            top_exp = df[df["type"]=="Expense"].groupby("category")["amount"].sum().idxmax() if not df[df["type"]=="Expense"].empty else "—"
            st.markdown(f"""
            <div class="card">
              <div class="stat-row"><span class="s-label">Top Expense</span><span class="s-val" style="font-size:0.78rem">{top_exp}</span></div>
              <div class="stat-row"><span class="s-label">Savings Rate</span><span class="s-val" style="color:{'var(--green)' if sr>=20 else 'var(--red)'}">{sr:.1f}%</span></div>
              <div class="stat-row"><span class="s-label">Total Records</span><span class="s-val">{len(df)}</span></div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
p = st.session_state.page
if   p == "Dashboard":    page_dashboard()
elif p == "Transactions":  page_transactions()
elif p == "Analytics":     page_analytics()
elif p == "AI Assistant":  page_ai()
