"""
app.py — SpendSage: Ultra Advanced Expense Tracker
Streamlit Frontend | Google Gemini 2.5 Flash + Groq AI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date, timedelta
import json
import time

# ── Page config — MUST be first ──────────────────────────────
st.set_page_config(
    page_title="SpendSage",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import AI agent ──────────────────────────────────────────
from suchat import chat_with_agent, get_quick_insight

# ═════════════════════════════════════════════════════════════
#  GLOBAL CSS — Ultra Premium Dark Theme
# ═════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ── */
:root {
  --bg:        #080b12;
  --surface:   #0f1420;
  --surface2:  #161d2e;
  --surface3:  #1c2540;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --gold:      #f5c842;
  --gold2:     #ffd97d;
  --green:     #3de8a0;
  --red:       #ff6b7a;
  --blue:      #5b9cf6;
  --purple:    #a78bfa;
  --text:      #e8edf5;
  --muted:     #6b7594;
  --muted2:    #8b95b4;
}

/* ── Base Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
  font-family: 'Inter', sans-serif !important;
  background: var(--bg) !important;
  color: var(--text) !important;
}

h1,h2,h3,h4,h5 { font-family:'Syne',sans-serif !important; letter-spacing:-0.02em; }

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display:none; }

/* ── Main Container ── */
.main .block-container {
  padding: 0 2rem 2rem 2rem !important;
  max-width: 1500px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding: 1.5rem 1rem;
}

/* ── Sidebar Nav Radio ── */
[data-testid="stSidebar"] .stRadio label {
  font-size: 0.8rem !important;
  color: var(--muted) !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.95rem !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500;
  color: var(--muted2) !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
  transition: all 0.2s;
  margin-bottom: 2px;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: var(--surface2);
  color: var(--text) !important;
}

/* ── Input Fields ── */
.stTextInput input, .stNumberInput input,
.stSelectbox > div > div, .stDateInput input,
.stTextArea textarea {
  background: var(--surface2) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-family: 'Inter', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus,
.stTextArea textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(245,200,66,0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--gold), #e8a800) !important;
  color: #0a0c12 !important;
  border: none !important;
  border-radius: 10px !important;
  font-weight: 700 !important;
  font-family: 'Syne', sans-serif !important;
  letter-spacing: 0.02em !important;
  padding: 0.6rem 1.6rem !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px rgba(245,200,66,0.35) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  gap: 2px !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 9px !important;
  color: var(--muted2) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500 !important;
  padding: 0.5rem 1.2rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--gold) !important;
  color: #0a0c12 !important;
  font-weight: 700 !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }
.stDataFrame table { background: var(--surface) !important; }
.stDataFrame th { background: var(--surface2) !important; color: var(--muted2) !important; }
.stDataFrame td { color: var(--text) !important; border-color: var(--border) !important; }

/* ── Plotly chart background override ── */
.js-plotly-plot { border-radius: 16px !important; }

/* ── Chat bubbles ── */
.chat-user {
  display:flex; justify-content:flex-end; margin-bottom:1rem;
}
.chat-user .bubble {
  background: linear-gradient(135deg,#1e3a5f,#0f2440);
  border: 1px solid rgba(91,156,246,0.25);
  border-radius: 18px 18px 4px 18px;
  padding: 0.75rem 1.1rem;
  max-width: 72%;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #c8dcf8;
}
.chat-ai {
  display:flex; justify-content:flex-start; margin-bottom:1rem; gap:0.7rem;
}
.chat-ai .avatar {
  width:36px; height:36px; border-radius:50%;
  background: linear-gradient(135deg,var(--gold),#e8a800);
  display:flex; align-items:center; justify-content:center;
  font-size:1rem; flex-shrink:0; margin-top:4px;
  box-shadow: 0 4px 12px rgba(245,200,66,0.3);
}
.chat-ai .bubble {
  background: var(--surface2);
  border: 1px solid var(--border2);
  border-radius: 18px 18px 18px 4px;
  padding: 0.75rem 1.1rem;
  max-width: 78%;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text);
}
.chat-ai .model-tag {
  font-size: 0.7rem;
  color: var(--muted);
  margin-top: 0.3rem;
  padding-left: 0.5rem;
}

/* ── Metric Cards (HTML) ── */
.metric-grid { display:grid; gap:1rem; }
.mcard {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1.4rem 1.6rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, border-color 0.2s;
}
.mcard:hover { transform:translateY(-3px); border-color:var(--border2); }
.mcard::before {
  content:''; position:absolute;
  top:0; left:0; right:0; height:3px;
}
.mcard.income::before  { background: linear-gradient(90deg,var(--green),#00c87a); }
.mcard.expense::before { background: linear-gradient(90deg,var(--red),#e8394a); }
.mcard.balance::before { background: linear-gradient(90deg,var(--gold),var(--gold2)); }
.mcard.savings::before { background: linear-gradient(90deg,var(--purple),#7c3aed); }
.mcard .label {
  font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em;
  color:var(--muted); font-weight:600; margin-bottom:0.5rem;
}
.mcard .value {
  font-family:'Syne',sans-serif; font-size:1.75rem;
  font-weight:800; line-height:1; margin-bottom:0.3rem;
}
.mcard.income  .value { color:var(--green); }
.mcard.expense .value { color:var(--red); }
.mcard.balance .value { color:var(--gold); }
.mcard.savings .value { color:var(--purple); }
.mcard .sub { font-size:0.8rem; color:var(--muted2); }
.mcard .icon {
  position:absolute; right:1.2rem; top:50%;
  transform:translateY(-50%);
  font-size:2rem; opacity:0.12;
}

/* ── Welcome Banner ── */
.welcome-banner {
  background: linear-gradient(135deg, #0f1c35 0%, #111827 50%, #0f1420 100%);
  border: 1px solid rgba(245,200,66,0.15);
  border-radius: 20px;
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.welcome-banner::after {
  content:'💎';
  position:absolute; right:2rem; top:50%;
  transform:translateY(-50%);
  font-size:5rem; opacity:0.06;
}
.welcome-banner h1 {
  font-size:2.2rem !important; font-weight:800 !important;
  margin:0 0 0.5rem 0 !important;
  background: linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.welcome-banner p { color:var(--muted2); font-size:1rem; margin:0; }
.welcome-banner .date-badge {
  display:inline-block; margin-top:1rem;
  background:rgba(245,200,66,0.1);
  border:1px solid rgba(245,200,66,0.2);
  border-radius:20px; padding:0.3rem 1rem;
  font-size:0.8rem; color:var(--gold);
  font-weight:500;
}

/* ── Section Headers ── */
.section-header {
  display:flex; align-items:center; gap:0.7rem;
  margin:1.5rem 0 1rem 0;
}
.section-header .dot {
  width:8px; height:8px; border-radius:50%;
  background:var(--gold); flex-shrink:0;
}
.section-header h3 {
  font-size:1.1rem !important; font-weight:700 !important;
  margin:0 !important; color:var(--text) !important;
}

/* ── Transaction Row ── */
.txn-row {
  display:flex; align-items:center; gap:1rem;
  padding:0.8rem 1rem; border-radius:12px;
  background:var(--surface); border:1px solid var(--border);
  margin-bottom:0.5rem; transition:all 0.15s;
}
.txn-row:hover { border-color:var(--border2); background:var(--surface2); }
.txn-icon {
  width:38px; height:38px; border-radius:10px;
  display:flex; align-items:center; justify-content:center;
  font-size:1.1rem; flex-shrink:0;
}
.txn-icon.income  { background:rgba(61,232,160,0.12); }
.txn-icon.expense { background:rgba(255,107,122,0.12); }
.txn-info { flex:1; min-width:0; }
.txn-name { font-weight:600; font-size:0.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.txn-meta { font-size:0.75rem; color:var(--muted); margin-top:2px; }
.txn-amount { font-family:'Syne',sans-serif; font-weight:700; font-size:1rem; }
.txn-amount.income  { color:var(--green); }
.txn-amount.expense { color:var(--red); }

/* ── AI Insight Box ── */
.insight-box {
  background:linear-gradient(135deg,rgba(245,200,66,0.06),rgba(167,139,250,0.06));
  border:1px solid rgba(245,200,66,0.2);
  border-radius:14px; padding:1rem 1.4rem;
  display:flex; gap:0.8rem; align-items:flex-start;
  margin-bottom:1.5rem;
}
.insight-box .spark { font-size:1.3rem; }
.insight-box .text  { font-size:0.9rem; color:var(--muted2); line-height:1.6; }

/* ── Sidebar Logo ── */
.sidebar-logo {
  text-align:center; padding:1rem 0 2rem 0;
  border-bottom:1px solid var(--border);
  margin-bottom:1.5rem;
}
.sidebar-logo .logo-icon { font-size:2.5rem; }
.sidebar-logo h2 {
  font-family:'Syne',sans-serif !important;
  font-size:1.4rem !important; font-weight:800 !important;
  margin:0.3rem 0 0 0 !important;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.sidebar-logo p { font-size:0.75rem; color:var(--muted); margin:0; }

/* ── Progress Bar ── */
.budget-bar-wrap { margin-bottom:1rem; }
.budget-bar-label {
  display:flex; justify-content:space-between;
  font-size:0.82rem; margin-bottom:0.35rem; color:var(--muted2);
}
.budget-bar-track {
  height:6px; border-radius:3px;
  background:var(--surface3);
  overflow:hidden;
}
.budget-bar-fill {
  height:100%; border-radius:3px;
  transition:width 0.5s;
}

/* ── Form Card ── */
.form-card {
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:16px;
  padding:1.5rem;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--surface); }
::-webkit-scrollbar-thumb { background:var(--surface3); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--muted); }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═════════════════════════════════════════════════════════════

EXPENSE_CATS = ["Food & Dining", "Transport", "Shopping", "Entertainment",
                "Health & Medical", "Education", "Rent & Housing",
                "Utilities", "Travel", "EMI / Loans", "Personal Care",
                "Subscriptions", "Gifts & Donations", "Other"]

INCOME_CATS  = ["Salary", "Freelance", "Business", "Investments",
                "Rental Income", "Bonus", "Side Hustle", "Gift",
                "Refund", "Other"]

CAT_ICONS = {
    "Food & Dining":"🍔", "Transport":"🚗", "Shopping":"🛍️",
    "Entertainment":"🎬", "Health & Medical":"💊", "Education":"📚",
    "Rent & Housing":"🏠", "Utilities":"💡", "Travel":"✈️",
    "EMI / Loans":"🏦", "Personal Care":"💅", "Subscriptions":"📱",
    "Gifts & Donations":"🎁", "Other":"📦",
    "Salary":"💼", "Freelance":"💻", "Business":"🏢",
    "Investments":"📈", "Rental Income":"🏘️", "Bonus":"🎯",
    "Side Hustle":"⚡", "Gift":"🎀", "Refund":"↩️",
}

def init_state():
    defaults = {
        "transactions": [],
        "chat_history_dashboard": [],
        "chat_history_transactions": [],
        "page": "🏠 Dashboard",
        "insight_cache": None,
        "insight_timestamp": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ═════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════

def get_df() -> pd.DataFrame:
    if not st.session_state.transactions:
        return pd.DataFrame(columns=["date","type","category","amount","note"])
    df = pd.DataFrame(st.session_state.transactions)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
    return df

def summary_stats(df):
    if df.empty:
        return 0, 0, 0, 0
    inc = df[df["type"]=="Income"]["amount"].sum()
    exp = df[df["type"]=="Expense"]["amount"].sum()
    bal = inc - exp
    sr  = (bal/inc*100) if inc > 0 else 0
    return inc, exp, bal, sr

def fmt_inr(val: float) -> str:
    if val >= 1_00_00_000:
        return f"₹{val/1_00_00_000:.1f}Cr"
    elif val >= 1_00_000:
        return f"₹{val/1_00_000:.1f}L"
    elif val >= 1_000:
        s = f"{int(val):,}"
        return f"₹{s}"
    return f"₹{val:.0f}"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#8b95b4", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(22,29,46,0.8)",
        bordercolor="rgba(255,255,255,0.07)",
        borderwidth=1,
        font=dict(color="#8b95b4"),
    ),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.05)"),
)

def render_metric_cards(inc, exp, bal, sr):
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "income",  "Total Income",   fmt_inr(inc), f"{len(get_df()[get_df()['type']=='Income']) if not get_df().empty else 0} transactions", "💰"),
        (c2, "expense", "Total Expenses", fmt_inr(exp), f"{len(get_df()[get_df()['type']=='Expense']) if not get_df().empty else 0} transactions", "💸"),
        (c3, "balance", "Net Balance",    fmt_inr(bal), "Income - Expenses", "⚖️"),
        (c4, "savings", "Savings Rate",   f"{sr:.1f}%",  "Of total income saved", "🎯"),
    ]
    for col, cls, label, value, sub, icon in cards:
        with col:
            st.markdown(f"""
            <div class="mcard {cls}">
              <div class="icon">{icon}</div>
              <div class="label">{label}</div>
              <div class="value">{value}</div>
              <div class="sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

def section_header(title: str, emoji: str = ""):
    st.markdown(f"""
    <div class="section-header">
      <div class="dot"></div>
      <h3>{emoji} {title}</h3>
    </div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  SIDEBAR
# ═════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-icon">💎</div>
      <h2>SpendSage</h2>
      <p>Smart Expense Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["🏠 Dashboard", "💳 Transactions", "📊 Analytics", "🤖 AI Assistant"],
        label_visibility="visible",
    )
    st.session_state.page = page

    st.markdown("---")

    # ── Quick Add in sidebar ──────────────────────────────────
    st.markdown("<p style='font-size:0.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-bottom:0.8rem'>Quick Add Transaction</p>", unsafe_allow_html=True)

    with st.form("sidebar_quick_add", clear_on_submit=True):
        q_type   = st.selectbox("Type", ["Expense", "Income"], key="q_type")
        q_cat    = st.selectbox("Category", EXPENSE_CATS if q_type=="Expense" else INCOME_CATS, key="q_cat")
        q_amt    = st.number_input("Amount (₹)", min_value=0.0, step=100.0, key="q_amt")
        q_date   = st.date_input("Date", value=date.today(), key="q_date")
        q_note   = st.text_input("Note (optional)", key="q_note")
        q_submit = st.form_submit_button("➕ Add", use_container_width=True)

    if q_submit and q_amt > 0:
        st.session_state.transactions.append({
            "date": str(q_date), "type": q_type,
            "category": q_cat, "amount": float(q_amt),
            "note": q_note,
        })
        st.session_state.insight_cache = None
        st.success("✅ Added!")

    st.markdown("---")

    # ── Stats summary ─────────────────────────────────────────
    df = get_df()
    if not df.empty:
        inc, exp, bal, sr = summary_stats(df)
        st.markdown(f"""
        <div style='background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:1rem;font-size:0.82rem'>
          <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem'>
            <span style='color:var(--muted)'>Income</span>
            <span style='color:var(--green);font-weight:600'>{fmt_inr(inc)}</span>
          </div>
          <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem'>
            <span style='color:var(--muted)'>Expenses</span>
            <span style='color:var(--red);font-weight:600'>{fmt_inr(exp)}</span>
          </div>
          <div style='display:flex;justify-content:space-between;border-top:1px solid var(--border);padding-top:0.5rem'>
            <span style='color:var(--muted)'>Balance</span>
            <span style='color:var(--gold);font-weight:700'>{fmt_inr(bal)}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:var(--muted);font-size:0.82rem;text-align:center'>No transactions yet</p>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ═════════════════════════════════════════════════════════════

def page_dashboard():
    df = get_df()
    inc, exp, bal, sr = summary_stats(df)

    # Welcome banner
    now = datetime.now()
    hour = now.hour
    greet = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 17 else "Good Evening")
    st.markdown(f"""
    <div class="welcome-banner">
      <h1>💎 SpendSage</h1>
      <p>{greet}! Track smarter, save better. Your financial overview is below.</p>
      <span class="date-badge">📅 {now.strftime('%A, %d %B %Y')}</span>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    render_metric_cards(inc, exp, bal, sr)

    st.markdown("<br>", unsafe_allow_html=True)

    # AI Insight
    if not df.empty:
        ts = time.time()
        if st.session_state.insight_cache is None or (ts - st.session_state.insight_timestamp) > 300:
            with st.spinner(""):
                st.session_state.insight_cache = get_quick_insight(st.session_state.transactions)
                st.session_state.insight_timestamp = ts
        st.markdown(f"""
        <div class="insight-box">
          <span class="spark">✨</span>
          <div class="text"><b style="color:#f5c842">AI Insight:</b> {st.session_state.insight_cache}</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts row
    col_l, col_r = st.columns([3, 2])

    with col_l:
        section_header("Monthly Overview", "📅")
        if not df.empty:
            monthly = df.copy()
            monthly["month"] = monthly["date"].dt.strftime("%b %Y")
            m_inc = monthly[monthly["type"]=="Income"].groupby("month")["amount"].sum().reset_index()
            m_exp = monthly[monthly["type"]=="Expense"].groupby("month")["amount"].sum().reset_index()
            m_inc.columns = ["month","amount"]; m_inc["type"]="Income"
            m_exp.columns = ["month","amount"]; m_exp["type"]="Expense"
            m_all = pd.concat([m_inc, m_exp])

            fig = px.bar(
                m_all, x="month", y="amount", color="type",
                barmode="group",
                color_discrete_map={"Income":"#3de8a0","Expense":"#ff6b7a"},
                template="plotly_dark",
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=280,
                              title=dict(text="", x=0))
            fig.update_traces(marker_cornerradius=5)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown("<div style='height:280px;display:flex;align-items:center;justify-content:center;color:var(--muted);background:var(--surface);border-radius:16px;border:1px solid var(--border)'>Add transactions to see chart</div>", unsafe_allow_html=True)

    with col_r:
        section_header("Spending Breakdown", "🍩")
        if not df.empty and not df[df["type"]=="Expense"].empty:
            exp_df = df[df["type"]=="Expense"].groupby("category")["amount"].sum().reset_index()
            exp_df.columns = ["category","amount"]
            colors = ["#f5c842","#3de8a0","#ff6b7a","#5b9cf6","#a78bfa",
                      "#fb923c","#34d399","#f472b6","#60a5fa","#facc15"]
            fig2 = go.Figure(go.Pie(
                labels=exp_df["category"],
                values=exp_df["amount"],
                hole=0.62,
                marker=dict(colors=colors[:len(exp_df)],
                            line=dict(color="rgba(0,0,0,0)", width=0)),
                textinfo="label+percent",
                textfont=dict(size=11, color="#8b95b4"),
                hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
            ))
            fig2.update_layout(**PLOTLY_LAYOUT, height=280,
                               showlegend=False,
                               annotations=[dict(text=f"<b>{fmt_inr(exp)}</b><br><span style='font-size:10px'>Total</span>",
                                                 x=0.5, y=0.5, font_size=16, font_color="#e8edf5",
                                                 showarrow=False)])
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown("<div style='height:280px;display:flex;align-items:center;justify-content:center;color:var(--muted);background:var(--surface);border-radius:16px;border:1px solid var(--border)'>No expense data yet</div>", unsafe_allow_html=True)

    # Recent transactions + Category bars
    col_a, col_b = st.columns([3, 2])

    with col_a:
        section_header("Recent Transactions", "🕐")
        if not df.empty:
            for _, row in df.head(6).iterrows():
                icon    = CAT_ICONS.get(row["category"], "📦")
                typ_cls = "income" if row["type"]=="Income" else "expense"
                prefix  = "+" if row["type"]=="Income" else "-"
                st.markdown(f"""
                <div class="txn-row">
                  <div class="txn-icon {typ_cls}">{icon}</div>
                  <div class="txn-info">
                    <div class="txn-name">{row['category']}</div>
                    <div class="txn-meta">{row['date'].strftime('%d %b %Y')}{(' · ' + str(row['note'])) if row.get('note') else ''}</div>
                  </div>
                  <div class="txn-amount {typ_cls}">{prefix}{fmt_inr(row['amount'])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:var(--muted);text-align:center;padding:2rem'>No transactions yet. Use the sidebar to add one!</p>", unsafe_allow_html=True)

    with col_b:
        section_header("Top Categories", "🏆")
        if not df.empty and not df[df["type"]=="Expense"].empty:
            cat_totals = df[df["type"]=="Expense"].groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
            max_val    = cat_totals.max()
            bar_colors = ["#f5c842","#3de8a0","#5b9cf6","#a78bfa","#fb923c"]
            for i, (cat, amt) in enumerate(cat_totals.items()):
                pct   = (amt / max_val * 100) if max_val > 0 else 0
                color = bar_colors[i % len(bar_colors)]
                icon  = CAT_ICONS.get(cat, "📦")
                st.markdown(f"""
                <div class="budget-bar-wrap">
                  <div class="budget-bar-label">
                    <span>{icon} {cat}</span>
                    <span style="color:{color};font-weight:600">{fmt_inr(amt)}</span>
                  </div>
                  <div class="budget-bar-track">
                    <div class="budget-bar-fill" style="width:{pct:.1f}%;background:{color}"></div>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:var(--muted);text-align:center;padding:2rem'>No expense categories yet</p>", unsafe_allow_html=True)

    # ── Dashboard chatbot ────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("AI Financial Assistant", "🤖")
    st.markdown("<p style='color:var(--muted);font-size:0.85rem;margin-top:-0.5rem;margin-bottom:1rem'>Ask me anything about your finances — I have full access to your data</p>", unsafe_allow_html=True)

    render_chatbot("dashboard")


# ═════════════════════════════════════════════════════════════
#  PAGE: TRANSACTIONS
# ═════════════════════════════════════════════════════════════

def page_transactions():
    st.markdown("<h2 style='font-size:1.8rem;font-weight:800;margin-bottom:0.3rem'>💳 Transactions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--muted);margin-bottom:1.5rem'>Add, view and manage all your income & expense records</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["➕  Add Transaction", "📋  All Transactions", "🤖  AI Assistant"])

    # ── Tab 1: Add Transaction ──────────────────────────────
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        col_form, col_tip = st.columns([3, 2])

        with col_form:
            st.markdown('<div class="form-card">', unsafe_allow_html=True)
            section_header("New Transaction", "✏️")

            with st.form("add_txn_form", clear_on_submit=True):
                r1c1, r1c2 = st.columns(2)
                with r1c1:
                    txn_type = st.selectbox("Transaction Type", ["Expense", "Income"])
                with r1c2:
                    txn_date = st.date_input("Date", value=date.today())

                r2c1, r2c2 = st.columns(2)
                with r2c1:
                    cats = EXPENSE_CATS if txn_type == "Expense" else INCOME_CATS
                    txn_cat = st.selectbox("Category", cats)
                with r2c2:
                    txn_amt = st.number_input("Amount (₹)", min_value=0.01, step=100.0, format="%.2f")

                txn_note = st.text_area("Note / Description (optional)", height=80, placeholder="E.g. Zomato order, Monthly salary, EMI payment...")

                submitted = st.form_submit_button("💾 Save Transaction", use_container_width=True)

            if submitted:
                if txn_amt > 0:
                    st.session_state.transactions.append({
                        "date": str(txn_date), "type": txn_type,
                        "category": txn_cat, "amount": float(txn_amt),
                        "note": txn_note.strip(),
                    })
                    st.session_state.insight_cache = None
                    st.success(f"✅ {txn_type} of {fmt_inr(txn_amt)} added successfully!")
                else:
                    st.error("Please enter an amount greater than 0.")

            st.markdown("</div>", unsafe_allow_html=True)

        with col_tip:
            st.markdown("<br>", unsafe_allow_html=True)
            # Bulk sample data button
            st.markdown("<p style='color:var(--muted);font-size:0.85rem'>Need sample data to explore?</p>", unsafe_allow_html=True)
            if st.button("🎲 Load Sample Data", use_container_width=True):
                sample = [
                    {"date":"2025-01-05","type":"Income","category":"Salary","amount":65000,"note":"Jan salary"},
                    {"date":"2025-01-08","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Jan rent"},
                    {"date":"2025-01-12","type":"Expense","category":"Food & Dining","amount":3200,"note":"Groceries"},
                    {"date":"2025-01-18","type":"Expense","category":"Transport","amount":1500,"note":"Uber + fuel"},
                    {"date":"2025-01-22","type":"Expense","category":"Entertainment","amount":900,"note":"Netflix + movie"},
                    {"date":"2025-02-05","type":"Income","category":"Salary","amount":65000,"note":"Feb salary"},
                    {"date":"2025-02-06","type":"Income","category":"Freelance","amount":12000,"note":"Design project"},
                    {"date":"2025-02-10","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Feb rent"},
                    {"date":"2025-02-14","type":"Expense","category":"Food & Dining","amount":4100,"note":"Valentines dinner"},
                    {"date":"2025-02-20","type":"Expense","category":"Shopping","amount":5500,"note":"Clothes"},
                    {"date":"2025-02-25","type":"Expense","category":"Health & Medical","amount":2200,"note":"Doctor + meds"},
                    {"date":"2025-03-05","type":"Income","category":"Salary","amount":65000,"note":"Mar salary"},
                    {"date":"2025-03-07","type":"Expense","category":"Rent & Housing","amount":18000,"note":"Mar rent"},
                    {"date":"2025-03-10","type":"Expense","category":"EMI / Loans","amount":8000,"note":"Car EMI"},
                    {"date":"2025-03-15","type":"Expense","category":"Food & Dining","amount":3800,"note":"Restaurants"},
                    {"date":"2025-03-20","type":"Expense","category":"Subscriptions","amount":1200,"note":"Spotify+Prime+Netflix"},
                    {"date":"2025-03-28","type":"Income","category":"Bonus","amount":10000,"note":"Performance bonus"},
                ]
                st.session_state.transactions.extend(sample)
                st.session_state.insight_cache = None
                st.success("✅ Sample data loaded!")
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            df = get_df()
            if not df.empty:
                inc, exp, bal, sr = summary_stats(df)
                st.markdown(f"""
                <div class="form-card">
                  <div class="label" style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:600;margin-bottom:1rem">Quick Stats</div>
                  <div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;font-size:0.88rem">
                    <span style="color:var(--muted2)">Total Records</span>
                    <span style="color:var(--text);font-weight:600">{len(df)}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;margin-bottom:0.6rem;font-size:0.88rem">
                    <span style="color:var(--muted2)">Income Entries</span>
                    <span style="color:var(--green);font-weight:600">{len(df[df['type']=='Income'])}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:0.88rem">
                    <span style="color:var(--muted2)">Expense Entries</span>
                    <span style="color:var(--red);font-weight:600">{len(df[df['type']=='Expense'])}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: All Transactions ─────────────────────────────
    with tab2:
        df = get_df()
        if df.empty:
            st.markdown("<p style='color:var(--muted);text-align:center;padding:3rem'>No transactions yet. Add some in the previous tab!</p>", unsafe_allow_html=True)
        else:
            # Filters
            fc1, fc2, fc3, fc4 = st.columns(4)
            with fc1:
                f_type = st.selectbox("Filter Type", ["All", "Income", "Expense"], key="f_type")
            with fc2:
                all_cats = ["All"] + sorted(df["category"].unique().tolist())
                f_cat = st.selectbox("Filter Category", all_cats, key="f_cat")
            with fc3:
                f_start = st.date_input("From", value=df["date"].min().date(), key="f_start")
            with fc4:
                f_end = st.date_input("To", value=df["date"].max().date(), key="f_end")

            filtered = df.copy()
            if f_type != "All":
                filtered = filtered[filtered["type"] == f_type]
            if f_cat != "All":
                filtered = filtered[filtered["category"] == f_cat]
            filtered = filtered[
                (filtered["date"].dt.date >= f_start) &
                (filtered["date"].dt.date <= f_end)
            ]

            st.markdown(f"<p style='color:var(--muted);font-size:0.85rem;margin-bottom:0.5rem'>Showing {len(filtered)} of {len(df)} transactions</p>", unsafe_allow_html=True)

            # Render rows
            for _, row in filtered.iterrows():
                icon    = CAT_ICONS.get(row["category"], "📦")
                typ_cls = "income" if row["type"]=="Income" else "expense"
                prefix  = "+" if row["type"]=="Income" else "-"
                st.markdown(f"""
                <div class="txn-row">
                  <div class="txn-icon {typ_cls}">{icon}</div>
                  <div class="txn-info">
                    <div class="txn-name">{row['category']}</div>
                    <div class="txn-meta">{row['date'].strftime('%d %b %Y')} · {row['type']}{(' · ' + str(row['note'])) if row.get('note') else ''}</div>
                  </div>
                  <div class="txn-amount {typ_cls}">{prefix}{fmt_inr(row['amount'])}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear All Transactions", key="clear_all"):
                st.session_state.transactions = []
                st.session_state.insight_cache = None
                st.rerun()

    # ── Tab 3: AI on Transactions page ─────────────────────
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        section_header("AI Assistant", "🤖")
        st.markdown("<p style='color:var(--muted);font-size:0.85rem;margin-top:-0.5rem;margin-bottom:1rem'>Ask me about specific transactions, categories or dates</p>", unsafe_allow_html=True)
        render_chatbot("transactions")


# ═════════════════════════════════════════════════════════════
#  PAGE: ANALYTICS
# ═════════════════════════════════════════════════════════════

def page_analytics():
    st.markdown("<h2 style='font-size:1.8rem;font-weight:800;margin-bottom:0.3rem'>📊 Analytics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--muted);margin-bottom:1.5rem'>Deep dive into your financial patterns</p>", unsafe_allow_html=True)

    df = get_df()
    if df.empty:
        st.markdown("""
        <div style='text-align:center;padding:5rem 2rem;background:var(--surface);border:1px solid var(--border);border-radius:16px'>
          <div style='font-size:3rem;margin-bottom:1rem'>📊</div>
          <h3 style='color:var(--muted)'>No data to analyze</h3>
          <p style='color:var(--muted2)'>Add transactions first to see detailed analytics</p>
        </div>
        """, unsafe_allow_html=True)
        return

    inc, exp, bal, sr = summary_stats(df)
    render_metric_cards(inc, exp, bal, sr)
    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: Line chart + Pie
    c1, c2 = st.columns([3, 2])
    with c1:
        section_header("Spending Trend", "📈")
        df_exp = df[df["type"]=="Expense"].copy()
        df_exp["week"] = df_exp["date"].dt.isocalendar().week.astype(str) + "-" + df_exp["date"].dt.year.astype(str)
        weekly = df_exp.groupby(df_exp["date"].dt.to_period("W").dt.start_time)["amount"].sum().reset_index()
        weekly.columns = ["date","amount"]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weekly["date"], y=weekly["amount"],
            fill="tozeroy",
            fillcolor="rgba(255,107,122,0.08)",
            line=dict(color="#ff6b7a", width=2.5),
            mode="lines+markers",
            marker=dict(size=5, color="#ff6b7a"),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.0f}<extra></extra>",
        ))
        fig.update_layout(**PLOTLY_LAYOUT, height=260)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

    with c2:
        section_header("Income vs Expense", "⚖️")
        fig2 = go.Figure(go.Pie(
            labels=["Income","Expenses"],
            values=[inc, exp],
            hole=0.55,
            marker=dict(colors=["#3de8a0","#ff6b7a"],
                        line=dict(color="rgba(0,0,0,0)", width=0)),
            textinfo="label+percent",
            textfont=dict(size=12, color="#8b95b4"),
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=260, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})

    # Row 2: Category treemap + Month bars
    c3, c4 = st.columns(2)
    with c3:
        section_header("Expense Heatmap by Category", "🗂️")
        exp_df = df[df["type"]=="Expense"].groupby("category")["amount"].sum().reset_index()
        exp_df.columns = ["category","amount"]
        if not exp_df.empty:
            fig3 = px.treemap(
                exp_df, path=["category"], values="amount",
                color="amount",
                color_continuous_scale=["#1c2540","#f5c842"],
                template="plotly_dark",
            )
            fig3.update_layout(**PLOTLY_LAYOUT, height=300)
            fig3.update_traces(textinfo="label+value+percent parent",
                               hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<extra></extra>")
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar":False})

    with c4:
        section_header("Monthly Savings", "💰")
        df["month"] = df["date"].dt.strftime("%b %Y")
        m_inc = df[df["type"]=="Income"].groupby("month")["amount"].sum()
        m_exp = df[df["type"]=="Expense"].groupby("month")["amount"].sum()
        m_sav = (m_inc - m_exp).fillna(0).reset_index()
        m_sav.columns = ["month","savings"]
        m_sav["color"] = m_sav["savings"].apply(lambda x: "#3de8a0" if x >= 0 else "#ff6b7a")
        if not m_sav.empty:
            fig4 = go.Figure(go.Bar(
                x=m_sav["month"], y=m_sav["savings"],
                marker_color=m_sav["color"],
                marker_cornerradius=5,
                hovertemplate="<b>%{x}</b><br>Savings: ₹%{y:,.0f}<extra></extra>",
            ))
            fig4.update_layout(**PLOTLY_LAYOUT, height=300)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar":False})

    # Detailed table
    section_header("Category Summary Table", "📋")
    all_cats = df.groupby(["type","category"])["amount"].agg(["sum","count"]).reset_index()
    all_cats.columns = ["Type","Category","Total Amount","Transactions"]
    all_cats["Total Amount"] = all_cats["Total Amount"].apply(lambda x: f"₹{x:,.2f}")
    st.dataframe(
        all_cats, use_container_width=True, hide_index=True,
        column_config={
            "Type": st.column_config.TextColumn("Type", width=90),
            "Category": st.column_config.TextColumn("Category", width=160),
            "Total Amount": st.column_config.TextColumn("Total Amount", width=130),
            "Transactions": st.column_config.NumberColumn("Count", width=80),
        }
    )


# ═════════════════════════════════════════════════════════════
#  PAGE: AI ASSISTANT (standalone)
# ═════════════════════════════════════════════════════════════

def page_ai_assistant():
    st.markdown("<h2 style='font-size:1.8rem;font-weight:800;margin-bottom:0.3rem'>🤖 AI Financial Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:var(--muted);margin-bottom:1.5rem'>Powered by Google Gemini 2.5 Flash · Groq Llama-3.3 fallback</p>", unsafe_allow_html=True)

    df = get_df()
    inc, exp, bal, sr = summary_stats(df)

    # Context panel
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        caps = [
            (c1, "Income", fmt_inr(inc), "#3de8a0"),
            (c2, "Expenses", fmt_inr(exp), "#ff6b7a"),
            (c3, "Balance", fmt_inr(bal), "#f5c842"),
            (c4, "Records", str(len(df)), "#a78bfa"),
        ]
        for col, label, val, color in caps:
            with col:
                st.markdown(f"""
                <div style='background:var(--surface);border:1px solid var(--border);border-radius:12px;
                            padding:0.9rem 1.1rem;text-align:center'>
                  <div style='font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;
                              color:var(--muted);margin-bottom:0.3rem'>{label}</div>
                  <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:{color}'>{val}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Suggested prompts
    if len(st.session_state.chat_history_dashboard) == 0:
        st.markdown("<p style='color:var(--muted);font-size:0.82rem;margin-bottom:0.5rem'>Try asking:</p>", unsafe_allow_html=True)
        prompts = [
            "📊 Where am I spending the most?",
            "💡 How can I save more money?",
            "📅 Compare my monthly expenses",
            "🎯 Suggest a savings plan",
        ]
        cols = st.columns(len(prompts))
        for i, (col, prompt) in enumerate(zip(cols, prompts)):
            with col:
                if st.button(prompt, key=f"suggest_{i}", use_container_width=True):
                    clean = prompt.split(" ",1)[1]
                    st.session_state.chat_history_dashboard.append({"role":"user","content":clean})
                    with st.spinner("Thinking..."):
                        resp, model = chat_with_agent(clean, st.session_state.chat_history_dashboard[:-1], st.session_state.transactions)
                    st.session_state.chat_history_dashboard.append({"role":"assistant","content":resp,"model":model})
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    render_chatbot("dashboard")


# ═════════════════════════════════════════════════════════════
#  CHATBOT RENDERER (shared component)
# ═════════════════════════════════════════════════════════════

def render_chatbot(context: str):
    hist_key = f"chat_history_{context}"

    # Display history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state[hist_key]:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                  <div class="bubble">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                model_tag = msg.get("model", "")
                st.markdown(f"""
                <div class="chat-ai">
                  <div class="avatar">💎</div>
                  <div>
                    <div class="bubble">{msg['content']}</div>
                    <div class="model-tag">via {model_tag}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

    # Input
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Ask about your finances... (Hindi/English/Hinglish)",
            label_visibility="collapsed",
            key=f"chat_input_{context}",
        )
    with col_btn:
        send = st.button("Send ➤", key=f"send_{context}", use_container_width=True)

    if send and user_input.strip():
        st.session_state[hist_key].append({"role": "user", "content": user_input.strip()})
        with st.spinner("SpendSage AI is thinking..."):
            resp, model = chat_with_agent(
                user_input.strip(),
                st.session_state[hist_key][:-1],
                st.session_state.transactions,
            )
        st.session_state[hist_key].append({"role": "assistant", "content": resp, "model": model})
        st.rerun()

    # Clear chat
    if st.session_state[hist_key]:
        if st.button("🗑️ Clear Chat", key=f"clear_chat_{context}"):
            st.session_state[hist_key] = []
            st.rerun()


# ═════════════════════════════════════════════════════════════
#  ROUTER
# ═════════════════════════════════════════════════════════════

p = st.session_state.page
if   p == "🏠 Dashboard":      page_dashboard()
elif p == "💳 Transactions":   page_transactions()
elif p == "📊 Analytics":      page_analytics()
elif p == "🤖 AI Assistant":   page_ai_assistant()
