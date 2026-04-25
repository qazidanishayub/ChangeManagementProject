import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CM Hub — Change Management",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── API Setup ─────────────────────────────────────────────────────────────────
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    try:
        if "gemini_api_key" in st.secrets:
            api_key = st.secrets["gemini_api_key"]
        elif "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
            api_key = st.secrets["gemini"]["api_key"]
    except Exception:
        pass

if not api_key:
    st.warning("⚠️ **API Key Missing**: Please set `GEMINI_API_KEY` in your environment variables or Streamlit secrets to use this application.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-flash-latest")

# ── Session State Init ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "run_count" not in st.session_state:
    st.session_state.run_count = 0
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── Assessment Categories ─────────────────────────────────────────────────────
CATEGORIES = {
    "Strategy": [
        "Change vision/case for change",
        "Change approach/strategy",
        "Change impact assessment",
        "Benefits/Adoption KPIs",
    ],
    "Stakeholders": [
        "Stakeholder assessment/map",
        "ADKAR assessment",
        "Key messages by stakeholder group",
        "Briefing messages",
    ],
    "Planning": [
        "Communications plan",
        "Engagement plan",
        "Training plan",
        "Training assessment",
    ],
    "Measurement": [
        "Readiness assessment",
        "Health check",
        "Change KPIs/user adoption statistics",
    ],
    "Content": [
        "What's changing and what is not summary",
        "Communications messages",
        "FAQs",
    ],
    "Surveys": [
        "Champions survey",
        "Users survey",
        "Training feedback survey",
    ],
}
ALL_ASSESSMENTS = [item for items in CATEGORIES.values() for item in items]

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }

.main { background: #080C14 !important; }
.main .block-container {
    background: #080C14 !important;
    padding: 1.5rem 2.5rem 2rem;
    max-width: 100% !important;
}
[data-testid="stSidebar"] {
    background: #0C1120 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

h1, h2, h3, h4 { font-family: 'Outfit', sans-serif !important; color: #E2EFFF !important; }
p, li, label, .stMarkdown { color: #8B9FBD !important; font-size: 0.92rem !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown { color: #9EB3D0 !important; }

[data-testid="metric-container"] {
    background: #0E1626 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}
[data-testid="stMetricValue"] {
    color: #D4E8FF !important;
    font-weight: 600 !important;
    font-size: 1.8rem !important;
}
[data-testid="stMetricLabel"] {
    color: #5B7A9E !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetricDelta"] { color: #4ADE80 !important; font-size: 0.75rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #1C6FFF 0%, #6D3AE8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(28, 111, 255, 0.4) !important;
    filter: brightness(1.08) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

[data-baseweb="select"] > div {
    background: #0E1626 !important;
    border-color: rgba(255,255,255,0.09) !important;
    border-radius: 9px !important;
    color: #C0D8F5 !important;
}
[data-baseweb="tag"] {
    background: rgba(28, 111, 255, 0.18) !important;
    border-color: rgba(28, 111, 255, 0.35) !important;
    border-radius: 6px !important;
    color: #7ABCFF !important;
}

[data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    gap: 2px !important;
}
[data-baseweb="tab"] {
    color: #5B7A9E !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    border-radius: 7px !important;
    padding: 0.38rem 0.95rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: rgba(28, 111, 255, 0.18) !important;
    color: #7ABCFF !important;
    border: 1px solid rgba(28, 111, 255, 0.28) !important;
}
.stTabs [data-testid="stTabsContent"] { padding-top: 1.25rem; }

[data-testid="stRadio"] label div p { color: #9EB3D0 !important; font-size: 0.88rem !important; }

[data-testid="stCheckbox"] label { color: #9EB3D0 !important; font-size: 0.88rem !important; }

[data-testid="stTextInput"] input {
    background: #0E1626 !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #C0D8F5 !important;
    border-radius: 9px !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: rgba(28,111,255,0.5) !important;
    box-shadow: 0 0 0 2px rgba(28,111,255,0.12) !important;
}
[data-testid="stTextInput"] input[type="password"] {
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stExpander"] {
    background: #0E1626 !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    margin-bottom: 6px !important;
}
[data-testid="stExpander"] summary { color: #AABFD8 !important; font-weight: 500 !important; }

[data-testid="stForm"] {
    background: #0E1626;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.5rem 1.5rem 1rem;
}

hr { border-color: rgba(255,255,255,0.05) !important; }

[data-testid="stProgress"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 4px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #1C6FFF, #6D3AE8) !important;
    border-radius: 4px !important;
}

code {
    background: rgba(28,111,255,0.12) !important;
    color: #7ABCFF !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.18); }

.cm-header-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 0 1.25rem; border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.5rem;
}
.cm-logo-block { display: flex; align-items: center; gap: 12px; }
.cm-logo-icon {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, rgba(28,111,255,0.15), rgba(109,58,232,0.15));
    border: 1px solid rgba(28,111,255,0.3);
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.cm-title { font-size: 1.35rem; font-weight: 700; color: #E2EFFF !important; letter-spacing: -0.02em; margin: 0; }
.cm-sub { font-size: 0.78rem; color: #5B7A9E !important; margin: 0; }
.cm-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.25);
    color: #4ADE80; border-radius: 99px; padding: 3px 10px;
    font-size: 0.72rem; font-weight: 500;
}
.cm-dot { width: 6px; height: 6px; border-radius: 50%; background: #4ADE80; }
.cm-response-card {
    background: linear-gradient(145deg, #0E1A30 0%, #0B1525 100%);
    border: 1px solid rgba(28,111,255,0.18); border-radius: 14px;
    padding: 1.5rem 1.75rem; margin-top: 1rem; position: relative; overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.cm-response-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(28, 111, 255, 0.2);
}
.cm-response-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #1C6FFF, #6D3AE8);
}
.cm-response-label {
    font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.1em;
    text-transform: uppercase; color: #4A8FFF !important; margin-bottom: 0.75rem;
}
.cm-response-body {
    color: #BDD4F5; font-size: 0.92rem; line-height: 1.75; white-space: pre-wrap;
    font-family: 'Outfit', sans-serif;
}
.cm-cat-header {
    font-size: 0.68rem !important; font-weight: 600 !important; letter-spacing: 0.08em;
    text-transform: uppercase; color: #3D5F8A !important; margin: 1rem 0 0.4rem;
    border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px;
}
.sb-brand {
    background: linear-gradient(145deg, #0E1A30, #0B1525);
    border: 1px solid rgba(28,111,255,0.15); border-radius: 12px;
    padding: 1rem 1.1rem; margin-bottom: 1.25rem; text-align: center;
}
.sb-brand-name { font-size: 1.05rem !important; font-weight: 700 !important; color: #D4E8FF !important; }
.sb-brand-tag { font-size: 0.72rem !important; color: #3D5F8A !important; }
.coverage-ring {
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; padding: 0.75rem 0;
}
.coverage-pct { font-size: 1.6rem !important; font-weight: 700 !important; color: #D4E8FF !important; }
.coverage-lbl { font-size: 0.72rem !important; color: #3D5F8A !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div style="font-size:1.6rem;margin-bottom:4px;">⬡</div>
      <div class="sb-brand-name">CM Hub</div>
      <div class="sb-brand-tag">Change Management Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cm-cat-header">Detail Level</div>', unsafe_allow_html=True)
    detail_level = st.radio(
        "detail",
        ("Basic", "Intermediate", "Advanced"),
        index=1,
        label_visibility="collapsed"
    )

    st.markdown('<div class="cm-cat-header" style="margin-top:1.25rem;">Select Assessments</div>',
                unsafe_allow_html=True)
    selected_assessments = []
    for cat, items in CATEGORIES.items():
        with st.expander(cat, expanded=False):
            for item in items:
                if st.checkbox(item, key=f"cb_{item}"):
                    selected_assessments.append(item)

    total = len(ALL_ASSESSMENTS)
    count = len(selected_assessments)
    pct = int(count / total * 100) if total else 0

    st.markdown('<div class="cm-cat-header" style="margin-top:1rem;">Coverage</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="coverage-ring">
      <div class="coverage-pct">{pct}%</div>
      <div class="coverage-lbl">{count} of {total} areas</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(pct / 100)

    def select_all():
        for item in ALL_ASSESSMENTS:
            st.session_state[f"cb_{item}"] = True

    def clear_all():
        for item in ALL_ASSESSMENTS:
            st.session_state[f"cb_{item}"] = False

    st.button("Select All", use_container_width=True, on_click=select_all)
    st.button("Clear All", use_container_width=True, on_click=clear_all)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cm-header-bar">
  <div class="cm-logo-block">
    <div class="cm-logo-icon">
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
        <rect x="1" y="1" width="7" height="7" rx="2" fill="#4A8FFF"/>
        <rect x="10" y="1" width="7" height="7" rx="2" fill="#4A8FFF" opacity=".4"/>
        <rect x="1" y="10" width="7" height="7" rx="2" fill="#4A8FFF" opacity=".4"/>
        <rect x="10" y="10" width="7" height="7" rx="2" fill="#4A8FFF"/>
      </svg>
    </div>
    <div>
      <div class="cm-title">Change Management Hub</div>
      <div class="cm-sub">AI-powered assessments for organisational transformation</div>
    </div>
  </div>
  <div class="cm-badge"><div class="cm-dot"></div>Gemini Flash</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Assessment Builder", "Dashboard", "History", "Settings"
])

# ══ TAB 1: ASSESSMENT BUILDER ════════════════════════════════════════════════
with tab1:
    if not selected_assessments:
        st.info("Select assessments from the sidebar to get started. "
                "Use **Select All** for a full audit, or choose specific areas.")
    else:
        chip_html = "".join([
            f'<span style="display:inline-flex;align-items:center;'
            f'background:rgba(28,111,255,0.14);border:1px solid rgba(28,111,255,0.3);'
            f'color:#7ABCFF;border-radius:6px;padding:3px 9px;'
            f'font-size:0.8rem;margin:2px;">{a}</span>'
            for a in selected_assessments
        ])
        st.markdown(f"""
        <div style="margin-bottom:1.25rem;">
          <div class="cm-response-label">Selected assessments ({len(selected_assessments)})</div>
          <div style="display:flex;flex-wrap:wrap;gap:2px;">{chip_html}</div>
        </div>
        """, unsafe_allow_html=True)

        col_gen, col_exp = st.columns([3, 1])
        with col_gen:
            generate_btn = st.button(
                f"Generate {detail_level} Assessment  →",
                use_container_width=True
            )
        with col_exp:
            export_btn = st.button("Export Last", use_container_width=True)

        if export_btn and st.session_state.history:
            last = st.session_state.history[-1]
            export_text = (
                f"CHANGE MANAGEMENT ASSESSMENT REPORT\n"
                f"Generated: {last['timestamp']}\n"
                f"Detail Level: {last['level']}\n"
                f"Areas: {', '.join(last['items'])}\n\n"
                f"{'=' * 60}\n\n{last['response']}"
            )
            st.download_button(
                "Download .txt", export_text,
                file_name=f"cm_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain", use_container_width=True
            )

        level_instructions = {
            "Basic": (
                "Provide a concise, easy-to-read overview with bullet points. "
                "Use simple language — 3 to 5 bullets per topic, no jargon."
            ),
            "Intermediate": (
                "Provide structured sections with clear headings, key actions, and practical "
                "guidance. Include indicative timelines and ownership hints."
            ),
            "Advanced": (
                "Provide a comprehensive, consultant-grade framework with methodology references "
                "(ADKAR, Kotter, Prosci), risk analysis, phased approach, success metrics, "
                "and a detailed implementation roadmap."
            ),
        }

        if generate_btn:
            prompt = (
                f"You are a senior change management consultant. "
                f"Generate a {detail_level} level change management assessment report "
                f"for the following selected areas: {', '.join(selected_assessments)}.\n\n"
                f"Instructions: {level_instructions[detail_level]}\n"
                f"Format with clear section headings. Be practical, specific, and actionable."
            )

            with st.spinner("Generating your assessment with Gemini 1.5 Flash..."):
                try:
                    response = model.generate_content(prompt)
                    result_text = response.text
                    st.toast("Assessment generated successfully!", icon="✨")
                except Exception as e:
                    st.error(f"Error generating assessment: {e}")
                    st.stop()

            st.session_state.run_count += 1
            st.session_state.history.append({
                "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
                "items": selected_assessments.copy(),
                "level": detail_level,
                "response": result_text,
                "run_id": st.session_state.run_count,
            })

            st.markdown(f"""
            <div class="cm-response-card">
              <div class="cm-response-label">
                AI Assessment · {detail_level} · {len(selected_assessments)} areas
              </div>
              <div class="cm-response-body">{result_text}</div>
            </div>
            """, unsafe_allow_html=True)

        elif st.session_state.history:
            last = st.session_state.history[-1]
            st.markdown(f"""
            <div class="cm-response-card">
              <div class="cm-response-label">Last response · {last['level']} · {last['timestamp']}</div>
              <div class="cm-response-body">{last['response']}</div>
            </div>
            """, unsafe_allow_html=True)

# ══ TAB 2: DASHBOARD ═════════════════════════════════════════════════════════
with tab2:
    runs_total = st.session_state.run_count
    avg_sel = (
        sum(len(h["items"]) for h in st.session_state.history) / len(st.session_state.history)
        if st.session_state.history else 0
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Selected Now", count, f"+{count} active")
    m2.metric("Reports Generated", runs_total)
    m3.metric("Coverage", f"{pct}%", f"{count}/{total} areas")
    m4.metric("Avg. Areas / Report", f"{avg_sel:.1f}" if avg_sel else "—")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="cm-cat-header">Coverage by category</div>', unsafe_allow_html=True)

    for cat, items in CATEGORIES.items():
        in_cat = [i for i in items if i in selected_assessments]
        cat_pct = int(len(in_cat) / len(items) * 100) if items else 0
        col_l, col_r = st.columns([4, 1])
        with col_l:
            st.markdown(
                f'<div style="font-size:0.85rem;color:#9EB3D0;margin-bottom:2px;">{cat}</div>',
                unsafe_allow_html=True
            )
            st.progress(cat_pct / 100)
        with col_r:
            st.markdown(
                f'<div style="font-size:0.85rem;color:#5B7A9E;text-align:right;padding-top:4px;">'
                f'{len(in_cat)}/{len(items)}</div>',
                unsafe_allow_html=True
            )

    if not selected_assessments:
        st.markdown(
            '<div style="text-align:center;color:#3D5F8A;padding:2rem;font-size:0.9rem;">'
            'Select assessments from the sidebar to see coverage data.</div>',
            unsafe_allow_html=True
        )

# ══ TAB 3: HISTORY ═══════════════════════════════════════════════════════════
with tab3:
    if not st.session_state.history:
        st.markdown(
            '<div style="text-align:center;color:#3D5F8A;padding:3rem;font-size:0.9rem;">'
            'No reports generated yet. Head to Assessment Builder to get started.</div>',
            unsafe_allow_html=True
        )
    else:
        for h in reversed(st.session_state.history):
            with st.expander(
                f"#{h['run_id']}  ·  {h['level']}  ·  {h['timestamp']}  "
                f"·  {len(h['items'])} areas"
            ):
                chips = "".join([
                    f'<span style="display:inline-flex;align-items:center;'
                    f'background:rgba(28,111,255,0.14);border:1px solid rgba(28,111,255,0.3);'
                    f'color:#7ABCFF;border-radius:6px;padding:2px 8px;'
                    f'font-size:0.75rem;margin:2px;">{a}</span>'
                    for a in h["items"]
                ])
                st.markdown(
                    f'<div style="margin-bottom:0.75rem;">{chips}</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div style="color:#9EB3D0;font-size:0.88rem;'
                    f'white-space:pre-wrap;line-height:1.7;">{h["response"]}</div>',
                    unsafe_allow_html=True
                )

        if st.button("Clear All History"):
            st.session_state.history = []
            st.session_state.run_count = 0
            st.rerun()

# ══ TAB 4: SETTINGS ══════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="cm-cat-header">Account</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown(
            '<div style="font-size:0.9rem;color:#AABFD8;font-weight:500;'
            'margin-bottom:0.5rem;">Sign in</div>',
            unsafe_allow_html=True
        )
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_btn = st.form_submit_button("Sign In")

    if login_btn:
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.success(f"Signed in as {username}")
        else:
            st.error("Invalid credentials. Use admin / admin123 for the demo account.")

    if st.session_state.authenticated:
        st.markdown(
            '<span style="display:inline-flex;align-items:center;gap:5px;'
            'background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.25);'
            'color:#4ADE80;border-radius:99px;padding:3px 10px;font-size:0.72rem;">'
            'Account active</span>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="cm-cat-header" style="margin-top:1.5rem;">Model</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Model", "Gemini Flash")
    c2.metric("Provider", "Google AI")
