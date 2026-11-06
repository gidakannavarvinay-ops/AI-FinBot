"""
FinBot - AI Financial Assistant
Powered by Streamlit + Google Gemini API | Indian personal finance (INR ₹)
"""

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FinBot – AI Financial Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()
SERVER_API_KEY = (os.getenv("GEMINI_API_KEY") or "").strip()
DEFAULT_MODEL  = "gemini-2.5-flash"

# ─────────────────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Page background ── */
.stApp { background: #060b18; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.4rem !important; padding-bottom: 2rem !important; }

/* ════════════════════════════════
   HERO HEADER
════════════════════════════════ */
.hero {
    background: linear-gradient(130deg, #0f2460 0%, #1a4f6e 40%, #0d5c45 100%);
    border-radius: 20px;
    padding: 2rem 2.4rem 1.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.07);
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 80% 20%, rgba(56,189,248,.15) 0%, transparent 60%),
                radial-gradient(ellipse at 20% 80%, rgba(52,211,153,.12) 0%, transparent 55%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem; font-weight: 800;
    background: linear-gradient(90deg, #f8fafc, #7dd3fc, #6ee7b7);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 .4rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    font-size: .97rem; color: #94a3b8; margin: 0;
    display: flex; align-items: center; gap: .5rem;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: .35rem;
    background: rgba(52,211,153,.15);
    border: 1px solid rgba(52,211,153,.35);
    border-radius: 20px;
    padding: .22rem .7rem;
    font-size: .78rem; font-weight: 600; color: #34d399;
    margin-left: .6rem;
}

/* ════════════════════════════════
   QUICK-PROMPT CHIPS
════════════════════════════════ */
.chip-row {
    display: flex; flex-wrap: wrap; gap: .55rem;
    margin-bottom: 1.2rem;
}
.chip {
    display: inline-flex; align-items: center; gap: .4rem;
    background: rgba(30,41,59,.8);
    border: 1px solid rgba(99,102,241,.35);
    border-radius: 24px;
    padding: .4rem 1rem;
    font-size: .82rem; font-weight: 500; color: #cbd5e1;
    cursor: pointer;
    transition: all .2s ease;
    text-decoration: none;
    white-space: nowrap;
}
.chip:hover {
    background: rgba(99,102,241,.25);
    border-color: #818cf8;
    color: #e0e7ff;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99,102,241,.3);
}

/* ════════════════════════════════
   CHAT BUBBLES  (override Streamlit defaults)
════════════════════════════════ */
div[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
}
/* User bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
    border: 1px solid rgba(99,102,241,.4);
    border-radius: 18px 18px 4px 18px;
    padding: .9rem 1.2rem;
    color: #e0e7ff;
    box-shadow: 0 4px 16px rgba(30,58,138,.35);
}
/* Bot bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: rgba(15,23,42,.85);
    border: 1px solid rgba(52,211,153,.2);
    border-radius: 18px 18px 18px 4px;
    padding: .9rem 1.2rem;
    color: #e2e8f0;
    box-shadow: 0 4px 16px rgba(0,0,0,.35);
    backdrop-filter: blur(8px);
}

/* ════════════════════════════════
   CHAT INPUT BAR
════════════════════════════════ */
div[data-testid="stChatInput"] textarea {
    background: rgba(15,23,42,.9) !important;
    border: 1.5px solid rgba(99,102,241,.45) !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-size: .93rem !important;
    padding: .8rem 1rem !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.2) !important;
}

/* ════════════════════════════════
   EMI CALCULATOR CARD
════════════════════════════════ */
.emi-card {
    background: linear-gradient(135deg, rgba(15,36,96,.7) 0%, rgba(13,92,69,.5) 100%);
    border: 1px solid rgba(99,102,241,.3);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(6px);
}
.emi-title {
    font-size: 1rem; font-weight: 700; color: #7dd3fc;
    margin: 0 0 1rem; display: flex; align-items: center; gap: .5rem;
}
.emi-result-row {
    display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1rem;
}
.emi-result-box {
    flex: 1; min-width: 110px;
    background: rgba(0,0,0,.35);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px;
    padding: .7rem 1rem;
    text-align: center;
}
.emi-result-label {
    font-size: .72rem; color: #64748b;
    text-transform: uppercase; letter-spacing: .06em;
    margin-bottom: .3rem;
}
.emi-result-value {
    font-size: 1.1rem; font-weight: 700; color: #34d399;
}

/* ════════════════════════════════
   SIDEBAR
════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080e1f 0%, #0b1628 100%);
    border-right: 1px solid rgba(255,255,255,.06);
}
.sb-logo {
    display: flex; align-items: center; gap: .7rem;
    padding: .6rem 0 1rem;
    border-bottom: 1px solid rgba(255,255,255,.07);
    margin-bottom: 1rem;
}
.sb-logo-text { font-size: 1.15rem; font-weight: 800; color: #f1f5f9; }
.sb-logo-sub  { font-size: .73rem; color: #475569; margin-top: -.1rem; }

.sb-section-title {
    font-size: .72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .1em;
    color: #475569; margin: 1.1rem 0 .6rem;
}

.stat-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 12px;
    padding: .75rem 1rem;
    margin-bottom: .6rem;
}
.stat-label { font-size: .72rem; color: #64748b; text-transform: uppercase; letter-spacing:.06em; }
.stat-value { font-size: 1.25rem; font-weight: 700; color: #f1f5f9; }
.stat-sub   { font-size: .72rem; color: #475569; margin-top: .1rem; }

.pill {
    display: inline-block; padding: .18rem .55rem;
    border-radius: 20px; font-size: .72rem; font-weight: 600;
}
.pill-green  { background: rgba(16,185,129,.15); color:#34d399; border:1px solid rgba(16,185,129,.35); }
.pill-yellow { background: rgba(245,158,11,.15);  color:#fbbf24; border:1px solid rgba(245,158,11,.35); }
.pill-red    { background: rgba(239,68,68,.15);   color:#f87171; border:1px solid rgba(239,68,68,.35); }

.api-ok  { background:rgba(52,211,153,.12); border:1px solid rgba(52,211,153,.35);
           border-radius:10px; padding:.5rem .9rem; font-size:.82rem; color:#34d399;
           display:flex; align-items:center; gap:.45rem; }
.api-err { background:rgba(239,68,68,.12); border:1px solid rgba(239,68,68,.35);
           border-radius:10px; padding:.5rem .9rem; font-size:.82rem; color:#f87171;
           display:flex; align-items:center; gap:.45rem; }

/* sidebar Streamlit widgets */
section[data-testid="stSidebar"] label { color: #94a3b8 !important; font-size:.82rem !important; }
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] select {
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    color: #f1f5f9 !important; border-radius: 8px !important;
    font-size: .84rem !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.05) !important;
    border-color: rgba(255,255,255,.1) !important;
    color: #f1f5f9 !important;
}

/* General buttons */
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    border: 1px solid rgba(99,102,241,.4) !important;
    background: rgba(99,102,241,.12) !important;
    color: #c7d2fe !important;
    font-size: .83rem !important;
    font-weight: 500 !important;
    transition: all .2s !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(99,102,241,.3) !important;
    border-color: #818cf8 !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
}

/* Streamlit metrics */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 12px; padding: .7rem 1rem;
}
div[data-testid="stMetricLabel"] { color:#64748b !important; font-size:.75rem !important; }
div[data-testid="stMetricValue"] { color:#34d399 !important; font-size:1.1rem !important; font-weight:700 !important; }

/* Disclaimer */
.disclaimer {
    background: rgba(56,189,248,.06);
    border-left: 3px solid #38bdf8;
    border-radius: 8px; padding: .7rem 1rem;
    font-size: .78rem; color: #64748b;
    margin-top: 1.5rem;
}

/* Expander */
div[data-testid="stExpander"] {
    background: rgba(255,255,255,.03) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    border-radius: 12px !important;
}

/* Progress bars */
.stProgress > div > div { background: linear-gradient(90deg,#6366f1,#34d399) !important; border-radius:4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# EMI Calculator (also used as Gemini tool)
# ─────────────────────────────────────────────────────────
def calculate_emi(loan_amount: float, annual_rate: float, tenure_years: float) -> dict:
    """
    Calculate monthly EMI, total interest, and total payment for a loan in ₹.

    Args:
        loan_amount:   Principal amount in ₹ (e.g. 500000 for ₹5 Lakh).
        annual_rate:   Annual interest rate in % (e.g. 10.5 for 10.5% p.a.).
        tenure_years:  Repayment tenure in years (e.g. 3, or 0.5 for 6 months).

    Returns:
        dict with monthly_emi, total_interest, total_payment, and formatted strings.
    """
    try:
        p, r_a, t = float(loan_amount), float(annual_rate), float(tenure_years)
        n = int(round(t * 12))
        if n <= 0 or p <= 0:
            return {"error": "Loan amount and tenure must be > 0."}
        r = (r_a / 12) / 100
        emi = p / n if r == 0 else (p * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        total = emi * n
        interest = total - p
        return {
            "principal": round(p, 2),          "principal_formatted": f"₹{p:,.0f}",
            "annual_rate_percent": r_a,
            "tenure_years": t,                  "tenure_months": n,
            "monthly_emi": round(emi, 2),       "monthly_emi_formatted": f"₹{emi:,.2f}",
            "total_interest": round(interest,2),"total_interest_formatted": f"₹{interest:,.2f}",
            "total_payment": round(total, 2),   "total_payment_formatted": f"₹{total:,.2f}",
            "interest_share_percent": round(interest / total * 100, 1) if total else 0,
        }
    except Exception as exc:
        return {"error": str(exc)}


# ─────────────────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────────────────
def build_system_prompt(income, expenses, surplus, savings_rate,
                        savings_goal, risk_appetite, investment_horizon) -> str:
    return f"""You are "FinBot", an expert, empathetic AI Financial Assistant for India.

SCOPE – answer ONLY questions about:
  Budgeting, savings, emergency funds, loans/EMI, mutual funds/SIP, PPF/EPF/NPS, FDs,
  stocks, insurance (term vs ULIP), tax planning (80C/80D, old vs new regime).

GUARDRAILS:
- Politely refuse ANY non-finance question. Say:
  "I'm FinBot, your dedicated finance assistant. I only help with money matters! 💰"
- Always use ₹, Lakhs, Crores (Indian conventions).
- Use the calculate_emi tool whenever a loan/EMI calculation is needed.
- End EVERY response with:
  "📌 *Educational note: This is for informational purposes only — not SEBI-registered advice. Consult a certified financial planner for major decisions.*"

USER PROFILE (tailor all advice to this):
  Monthly Income   : ₹{income:,.0f}
  Monthly Expenses : ₹{expenses:,.0f}
  Monthly Surplus  : ₹{surplus:,.0f}  ({savings_rate:.1f}% savings rate)
  Goals            : {savings_goal}
  Risk Profile     : {risk_appetite}
  Horizon          : {investment_horizon}
"""


# ─────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sb-logo">
        <span style="font-size:2rem">💰</span>
        <div>
            <div class="sb-logo-text">FinBot</div>
            <div class="sb-logo-sub">AI Financial Assistant · India</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # API Status
    if not SERVER_API_KEY:
        st.markdown('<div class="api-err">⚠️ API key not configured</div>', unsafe_allow_html=True)
        fallback_key = st.text_input("Gemini API Key", type="password", value="",
                                     placeholder="Paste key here…",
                                     help="Set GEMINI_API_KEY in .env to avoid this.")
    else:
        st.markdown('<div class="api-ok">✅ &nbsp;Gemini API Connected</div>', unsafe_allow_html=True)
        fallback_key = ""

    # Model picker
    with st.expander("🤖 Model", expanded=False):
        selected_model = st.selectbox(
            "Gemini Model",
            ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.5-flash-lite"],
            index=0,
        )

    # ── Financial Profile ──
    st.markdown('<div class="sb-section-title">👤 Your Financial Profile</div>', unsafe_allow_html=True)

    monthly_income   = st.number_input("Monthly Income (₹)",   min_value=0.0, value=75000.0, step=5000.0, format="%.0f")
    monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=45000.0, step=2000.0, format="%.0f")
    savings_goal     = st.text_area("Goals",
                                    value="Build ₹3,00,000 Emergency Fund · Start ₹10,000/mo SIP",
                                    height=68)
    risk_appetite      = st.selectbox("Risk Profile",
                                      ["Moderate (Balanced)", "Conservative (FD/PPF/Debt)", "Aggressive (Equity/Small-cap)"])
    investment_horizon = st.selectbox("Horizon",
                                      ["Medium (3–5 yrs)", "Short (< 3 yrs)", "Long (5–15+ yrs)"])

    # ── Live Snapshot ──
    surplus      = monthly_income - monthly_expenses
    savings_rate = (surplus / monthly_income * 100) if monthly_income > 0 else 0.0

    st.markdown('<div class="sb-section-title">📊 Live Snapshot</div>', unsafe_allow_html=True)

    surplus_color = "#34d399" if surplus >= 0 else "#f87171"
    st.markdown(f"""
    <div class="stat-card">
      <div class="stat-label">Monthly Surplus</div>
      <div class="stat-value" style="color:{surplus_color}">₹{surplus:,.0f}</div>
      <div class="stat-sub">Income − Expenses</div>
    </div>""", unsafe_allow_html=True)

    if savings_rate >= 30:
        pill = '<span class="pill pill-green">Healthy ≥ 30%</span>'
    elif savings_rate >= 15:
        pill = '<span class="pill pill-yellow">Moderate 15–30%</span>'
    else:
        pill = '<span class="pill pill-red">Needs Boost &lt;15%</span>'

    st.markdown(f"""
    <div class="stat-card">
      <div class="stat-label">Savings Rate &nbsp;{pill}</div>
      <div class="stat-value">{savings_rate:.1f}%</div>
      <div class="stat-sub">% of income saved</div>
    </div>""", unsafe_allow_html=True)

    # Progress bar toward 30% target
    pct = min(savings_rate / 30, 1.0)
    st.progress(pct, text=f"Target 30% — {savings_rate:.0f}% achieved")

    with st.expander("📌 50/30/20 Rule Targets"):
        st.markdown(f"""
| Category | Target | Amount |
|---|---|---|
| 🏠 Needs | 50% | ₹{monthly_income*.5:,.0f} |
| 🛍️ Wants | 30% | ₹{monthly_income*.3:,.0f} |
| 💰 Savings | 20% | ₹{monthly_income*.2:,.0f} |
""")

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ─────────────────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">💰 FinBot — AI Financial Assistant</div>
  <p class="hero-sub">
    Your intelligent guide for budgeting, investments, loans &amp; wealth building in India 🇮🇳
    <span class="hero-badge">✦ Gemini 2.5 Flash</span>
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Inline EMI Calculator
# ─────────────────────────────────────────────────────────
with st.expander("🧮 EMI Calculator", expanded=False):
    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        c_loan = st.number_input("Loan Amount (₹)", 10_000.0, 10_000_000.0, 500_000.0, 25_000.0, key="c_loan")
    with ec2:
        c_rate = st.number_input("Interest Rate (% p.a.)", 1.0, 36.0, 10.0, 0.25, key="c_rate")
    with ec3:
        c_tenure = st.number_input("Tenure (Years)", 0.5, 30.0, 3.0, 0.5, key="c_tenure")

    er = calculate_emi(c_loan, c_rate, c_tenure)
    if "error" not in er:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Monthly EMI",    er["monthly_emi_formatted"])
        m2.metric("Total Interest", er["total_interest_formatted"])
        m3.metric("Total Payment",  er["total_payment_formatted"])
        m4.metric("Interest Share", f"{er['interest_share_percent']}%")

        if st.button("💬 Analyze this loan with FinBot", key="emi_to_chat"):
            st.session_state.pending_prompt = (
                f"I'm considering a loan of {er['principal_formatted']} at {c_rate}% p.a. for {c_tenure} years. "
                f"EMI comes to {er['monthly_emi_formatted']}. Given my income of ₹{monthly_income:,.0f} and "
                f"expenses of ₹{monthly_expenses:,.0f}, is this affordable? What repayment tips do you suggest?"
            )
            st.rerun()


# ─────────────────────────────────────────────────────────
# Quick-Prompt Chips  (HTML buttons → st.session_state trick)
# ─────────────────────────────────────────────────────────
QUICK_PROMPTS = [
    ("💡", "Emergency Fund",    "How do I build a ₹3–6 month emergency fund based on my income & expenses? Where should I park it?"),
    ("📈", "Start SIP",         "How much SIP should I start to build ₹50 Lakh in 10 years? Suggest fund categories."),
    ("🏦", "EMI for ₹5L @10%", "Calculate EMI for a ₹5 Lakh loan at 10% interest for 3 years and advise on affordability."),
    ("⚖️", "PPF vs MF",        "Compare PPF vs Equity Mutual Funds for long-term wealth — returns, liquidity, and tax angle."),
    ("🛡️", "Term vs ULIP",    "Explain the difference between Term Insurance and ULIP. Which is better for pure protection?"),
    ("📊", "50/30/20 Rule",     "Break down the 50/30/20 budgeting rule for my specific income and suggest improvements."),
]

st.markdown("**⚡ Quick Questions**")
cols = st.columns(len(QUICK_PROMPTS))
for i, (icon, label, prompt) in enumerate(QUICK_PROMPTS):
    with cols[i]:
        if st.button(f"{icon} {label}", use_container_width=True, key=f"qp_{i}"):
            st.session_state.pending_prompt = prompt
            st.rerun()


# ─────────────────────────────────────────────────────────
# Chat Session State Init
# ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Namaste! 🙏 I'm **FinBot**, your personal AI Finance Assistant for India.\n\n"
                f"Your profile shows a monthly surplus of **₹{surplus:,.0f}** "
                f"({savings_rate:.1f}% savings rate). "
                f"{'That\'s a healthy rate — let\'s make it work harder! 💪' if savings_rate >= 20 else 'Let\'s build a stronger savings habit together! 💪'}\n\n"
                f"Ask me anything about budgeting, SIPs, loans, or investments — or tap a quick button above!"
            ),
        }
    ]


# ─────────────────────────────────────────────────────────
# Chat Display
# ─────────────────────────────────────────────────────────
st.markdown('<div style="height:.3rem"></div>', unsafe_allow_html=True)
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "💰"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ─────────────────────────────────────────────────────────
# Chat Input + Response
# ─────────────────────────────────────────────────────────
user_input = st.chat_input("Ask a finance question… e.g. 'What SIP gives ₹1 Cr in 15 years?'")

if not user_input and st.session_state.get("pending_prompt"):
    user_input = st.session_state.pop("pending_prompt")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    active_key = SERVER_API_KEY or fallback_key.strip()

    if not active_key:
        err = "⚠️ **API key not configured.** Add `GEMINI_API_KEY` to your `.env` file and restart the app."
        st.session_state.messages.append({"role": "assistant", "content": err})
        with st.chat_message("assistant", avatar="💰"):
            st.markdown(err)
    else:
        with st.chat_message("assistant", avatar="💰"):
            with st.spinner("FinBot is thinking…"):
                try:
                    genai.configure(api_key=active_key)

                    model = genai.GenerativeModel(
                        model_name=selected_model or DEFAULT_MODEL,
                        system_instruction=build_system_prompt(
                            monthly_income, monthly_expenses, surplus, savings_rate,
                            savings_goal, risk_appetite, investment_horizon
                        ),
                        tools=[calculate_emi],
                    )

                    history = []
                    for m in st.session_state.messages[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history.append({"role": role, "parts": [m["content"]]})

                    chat = model.start_chat(history=history, enable_automatic_function_calling=True)
                    response = chat.send_message(user_input)
                    reply = response.text

                    # Safety net: ensure disclaimer is present
                    if "educational note" not in reply.lower():
                        reply += (
                            "\n\n---\n"
                            "📌 *Educational note: This is for informational purposes only — "
                            "not SEBI-registered advice. Consult a certified financial planner for major decisions.*"
                        )

                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                except Exception as exc:
                    e = str(exc)
                    if "API_KEY_INVALID" in e or "invalid api key" in e.lower():
                        msg = "❌ **Invalid API key.** Check `GEMINI_API_KEY` in your `.env` file."
                    elif "404" in e or "not found" in e.lower():
                        msg = f"❌ **Model not found.** Try switching to `{DEFAULT_MODEL}` in the sidebar."
                    elif "RESOURCE_EXHAUSTED" in e or "quota" in e.lower():
                        msg = "⏳ **Quota exceeded.** Wait a moment, then retry."
                    else:
                        msg = f"⚠️ **Something went wrong:** {e}"
                    st.markdown(msg)
                    st.session_state.messages.append({"role": "assistant", "content": msg})


# ─────────────────────────────────────────────────────────
# Footer Disclaimer
# ─────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
  🛡️ <strong>Disclaimer:</strong> FinBot is an AI-powered educational tool for financial literacy in India.
  It is not a SEBI-registered investment adviser and does not provide certified financial planning services.
  Always verify with a licensed financial professional before making significant financial decisions.
</div>
""", unsafe_allow_html=True)
