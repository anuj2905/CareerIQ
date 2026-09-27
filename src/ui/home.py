import streamlit as st
import html


# ============================================================
# GLOBAL PAGE STYLING
# ============================================================

def style_home_page():
    """CareerIQ global visual system — clean AI-product style."""
    st.html("""
    <style>
    :root {
        --cq-bg:#f7f6ef;
        --cq-paper:rgba(255,255,255,.78);
        --cq-ink:#073b5c;
        --cq-muted:#627586;
        --cq-border:rgba(7,59,92,.13);
        --cq-cyan:#11a9b5;
        --cq-purple:#8b5cf6;
        --cq-coral:#ff5a36;
        --cq-teal:#0f9f9a;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 8%, rgba(17,169,181,.10), transparent 24%),
            radial-gradient(circle at 92% 14%, rgba(139,92,246,.08), transparent 24%),
            linear-gradient(180deg,#faf9f2 0%,#f7f6ef 100%);
        color:var(--cq-ink);
    }

    [data-testid="stHeader"] {
        background:rgba(250,249,242,.82);
    }

    .block-container {
        max-width:1420px;
        padding-top:2rem;
        padding-bottom:3.5rem;
        background-image:radial-gradient(rgba(7,59,92,.12) .7px,transparent .7px);
        background-size:26px 26px;
    }

    h1,h2,h3,h4,p,li { color:var(--cq-ink); }

    .cq-topbar {
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:5px 0 20px;
        margin-bottom:8px;
        border-bottom:1px solid var(--cq-border);
    }
    .cq-brand {
        font-size:17px;
        font-weight:850;
        letter-spacing:-.3px;
    }
    .cq-brand-sub {
        color:var(--cq-muted);
        font-size:11px;
        margin-top:2px;
        font-weight:650;
    }
    .cq-top-pill {
        padding:9px 16px;
        border-radius:999px;
        color:#fff;
        background:linear-gradient(90deg,var(--cq-cyan),#159aa8);
        font-size:12px;
        font-weight:800;
        box-shadow:0 8px 24px rgba(17,169,181,.20);
    }

    .cq-hero {
        padding:48px 42px 42px;
        border:1px solid var(--cq-border);
        border-radius:26px;
        background:
            radial-gradient(circle at 86% 12%,rgba(17,169,181,.15),transparent 24%),
            radial-gradient(circle at 68% 100%,rgba(139,92,246,.10),transparent 28%),
            rgba(255,255,255,.68);
        box-shadow:0 18px 55px rgba(7,59,92,.07);
        margin:30px auto 28px;
        max-width:1120px;
        text-align:left;
    }
    .cq-kicker {
        color:var(--cq-coral);
        font-size:12px;
        font-weight:850;
        letter-spacing:1.3px;
        margin-bottom:13px;
    }
    .cq-title {
        color:var(--cq-ink);
        font-size:clamp(42px,6vw,68px);
        line-height:1.01;
        font-weight:880;
        letter-spacing:-2.5px;
        margin:0;
    }
    .cq-title span {
        background:linear-gradient(90deg,var(--cq-cyan),var(--cq-purple),var(--cq-coral));
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }
    .cq-gradient-line {
        height:3px;
        width:100%;
        margin:20px 0 18px;
        border-radius:999px;
        background:linear-gradient(90deg,var(--cq-cyan),var(--cq-purple),var(--cq-coral));
    }
    .cq-subtitle {
        max-width:850px;
        color:#536a7c;
        font-size:16px;
        line-height:1.8;
        margin:0;
    }

    .cq-section-title {
        color:var(--cq-ink);
        font-size:25px;
        font-weight:830;
        letter-spacing:-.5px;
        margin:20px 0 5px;
        text-align:center;
    }
    .cq-section-subtitle {
        color:var(--cq-muted);
        text-align:center;
        font-size:13px;
        margin-bottom:20px;
    }

    .cq-workspace {
        padding:28px 26px;
        min-height:245px;
        border:1px solid var(--cq-border);
        border-radius:20px;
        background:rgba(255,255,255,.80);
        box-shadow:0 10px 32px rgba(7,59,92,.055);
    }
    .cq-workspace:hover {
        border-color:rgba(17,169,181,.30);
    }
    .cq-icon {
        font-size:39px;
        margin-bottom:10px;
    }
    .cq-card-title {
        color:var(--cq-ink);
        font-size:22px;
        font-weight:820;
    }
    .cq-card-text {
        color:#607485;
        font-size:13px;
        line-height:1.7;
        margin-top:8px;
        min-height:68px;
    }
    .cq-pills {
        display:flex;
        flex-wrap:wrap;
        gap:7px;
        margin-top:16px;
    }
    .cq-pill {
        padding:5px 9px;
        border-radius:999px;
        background:#f0f7f8;
        border:1px solid rgba(17,169,181,.15);
        color:#225d73;
        font-size:10px;
        font-weight:700;
    }

    .cq-platform-title {
        color:var(--cq-ink);
        font-size:22px;
        font-weight:820;
        text-align:center;
        margin:44px 0 18px;
    }
    .cq-platform-card {
        min-height:145px;
        padding:20px 16px;
        border-radius:17px;
        border:1px solid var(--cq-border);
        background:rgba(255,255,255,.72);
        text-align:center;
    }
    .cq-platform-icon { font-size:28px; margin-bottom:7px; }
    .cq-platform-name { color:var(--cq-ink); font-size:13px; font-weight:780; }
    .cq-platform-text { color:var(--cq-muted); font-size:11px; line-height:1.5; margin-top:5px; }

    .cq-footer {
        text-align:center;
        color:#72818d;
        font-size:11px;
        margin-top:48px;
        padding-top:20px;
        border-top:1px solid var(--cq-border);
    }

    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#eeebda 0%,#e8e6d8 100%);
        border-right:1px solid var(--cq-border);
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color:var(--cq-ink) !important;
    }
    section[data-testid="stSidebar"] p { color:var(--cq-muted); }
    section[data-testid="stSidebar"] .stButton > button {
        border-radius:11px;
        border:1px solid rgba(7,59,92,.12);
        background:rgba(255,255,255,.55);
        color:#174c68;
        font-weight:700;
    }

    .stButton > button {
        border-radius:12px;
        min-height:44px;
        font-weight:750;
    }
    </style>
    """)

    st.html("""
    <style>
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background:rgba(255,255,255,.90) !important;
        border-color:rgba(7,59,92,.14) !important;
        border-radius:12px !important;
    }
    </style>
    """)


# ============================================================
# HOME PAGE
# ============================================================

def home_page():
    """Main CareerIQ landing page."""

    st.html("""
    <div class="cq-topbar">
        <div>
            <div class="cq-brand">🧠 CareerIQ</div>
            <div class="cq-brand-sub">AI Career Intelligence Platform</div>
        </div>
        <div class="cq-top-pill">AI-Powered Career Intelligence</div>
    </div>

    <div class="cq-hero">
        <div class="cq-kicker">CAREERIQ / INTELLIGENCE PLATFORM</div>
        <div class="cq-title">
            Build Your <span>Career</span><br>
            With Intelligence
        </div>
        <div class="cq-gradient-line"></div>
        <div class="cq-subtitle">
            CareerIQ analyzes resumes, skills, experience and opportunities
            to help students understand their career profile and help
            companies discover relevant talent.
        </div>
    </div>

    <div class="cq-section-title">Choose your workspace</div>
    <div class="cq-section-subtitle">
        Select how you want to use CareerIQ
    </div>
    """)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.html("""
        <div class="cq-workspace">
            <div class="cq-icon">🎓</div>
            <div class="cq-card-title">Student Workspace</div>
            <div class="cq-card-text">
                Analyze your resume, discover relevant jobs, identify
                skill gaps and build a personalized career roadmap.
            </div>
            <div class="cq-pills">
                <span class="cq-pill">Resume AI</span>
                <span class="cq-pill">Job Matching</span>
                <span class="cq-pill">Skill Gap</span>
                <span class="cq-pill">Career Roadmap</span>
            </div>
        </div>
        """)

        st.write("")
        if st.button(
            "🎓 Enter Student Workspace",
            use_container_width=True,
            type="primary",
        ):
            st.session_state["page"] = "student_auth"
            st.rerun()

    with col2:
        st.html("""
        <div class="cq-workspace">
            <div class="cq-icon">🏢</div>
            <div class="cq-card-title">Company Workspace</div>
            <div class="cq-card-text">
                Create jobs, define hiring requirements and review
                candidates using CareerIQ's matching and recruitment
                intelligence.
            </div>
            <div class="cq-pills">
                <span class="cq-pill">Create Jobs</span>
                <span class="cq-pill">Candidate Matching</span>
                <span class="cq-pill">Applications</span>
                <span class="cq-pill">Recruitment</span>
            </div>
        </div>
        """)

        st.write("")
        if st.button(
            "🏢 Enter Company Workspace",
            use_container_width=True,
        ):
            st.session_state["page"] = "company_auth"
            st.rerun()

    st.html("""
    <div class="cq-platform-title">
        One Platform. Complete Career Intelligence.
    </div>
    """)

    features = [
        ("📄", "Resume Intelligence", "Extract and understand your career profile."),
        ("🎯", "AI Job Matching", "Compare your profile with relevant opportunities."),
        ("📊", "Skill Intelligence", "Find missing skills and prioritize what to learn."),
        ("🤖", "AI Career Assistant", "Get personalized career guidance from your profile."),
    ]

    feature_cols = st.columns(4, gap="medium")
    for column, (icon, name, description) in zip(feature_cols, features):
        with column:
            st.html(f"""
            <div class="cq-platform-card">
                <div class="cq-platform-icon">{icon}</div>
                <div class="cq-platform-name">{html.escape(name)}</div>
                <div class="cq-platform-text">{html.escape(description)}</div>
            </div>
            """)

    st.html("""
    <div class="cq-footer">
        CareerIQ • AI-powered career intelligence platform
    </div>
    """)


# ============================================================
# STUDENT SIDEBAR
# ============================================================

def show_student_sidebar():
    """Sidebar shown inside the Student workspace."""

    st.html("""
    <style>
    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#eeebda 0%,#e8e6d8 100%);
        border-right:1px solid rgba(7,59,92,.12);
    }
    </style>
    """)

    st.sidebar.html("""
    <div style="padding:8px 4px 14px;color:#073b5c;">
        <div style="font-size:24px;font-weight:850;">🧠 CareerIQ</div>
        <div style="font-size:11px;color:#627586;margin-top:3px;font-weight:650;">
            Student Workspace
        </div>
    </div>
    """)

    st.sidebar.divider()

    st.sidebar.subheader("📄 Resume")

    if st.sidebar.button("📄 Resume Overview", use_container_width=True):
        st.session_state["student_feature"] = "📄 Resume Overview"
        st.session_state["page"] = "resume"
        st.rerun()

    if st.sidebar.button("🔄 Upload New Resume", use_container_width=True):
        st.session_state["student_feature"] = "🔄 Upload New Resume"
        st.session_state["page"] = "resume"
        st.rerun()

    st.sidebar.subheader("🧠 Career Intelligence")

    if st.sidebar.button("🎯 Job Matching", use_container_width=True):
        st.session_state["student_feature"] = "🎯 Job Matching"
        st.session_state["page"] = "resume"
        st.rerun()

    if st.sidebar.button("🧠 Career Insights", use_container_width=True):
        st.session_state["student_feature"] = "🧠 Career Insights"
        st.session_state["page"] = "resume"
        st.rerun()

    if st.sidebar.button("📊 Skill Gap Analysis", use_container_width=True):
        st.session_state["student_feature"] = "📊 Skill Gap Analysis"
        st.session_state["page"] = "resume"
        st.rerun()

    st.sidebar.subheader("🤖 AI")

    if st.sidebar.button("🤖 AI Career Assistant", use_container_width=True):
        st.session_state["student_feature"] = "🤖 AI Career Assistant"
        st.session_state["page"] = "assistant"
        st.rerun()

    st.sidebar.subheader("🔎 Opportunities")

    if st.sidebar.button("🔎 Job Discovery", use_container_width=True):
        st.session_state["student_feature"] = "🔎 Job Discovery"
        st.session_state["page"] = "jobs"
        st.rerun()

    st.sidebar.subheader("📈 Career Planning")

    if st.sidebar.button("📈 Career Dashboard", use_container_width=True):
        st.session_state["student_feature"] = "📈 Career Dashboard"
        st.session_state["page"] = "student_feature"
        st.rerun()

    if st.sidebar.button("🗺️ Career Roadmap", use_container_width=True):
        st.session_state["student_feature"] = "🗺️ Career Roadmap"
        st.session_state["page"] = "student_feature"
        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("🏠 Back to Home", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()


# ============================================================
# STUDENT WORKSPACE
# ============================================================

def student_page():
    """Main Student workspace."""

    show_student_sidebar()
    profile = st.session_state.get("profile")

    st.html("""
    <div style="margin-bottom:28px;">
        <div style="font-size:12px;color:#ff5a36;font-weight:850;letter-spacing:1px;">
            CAREERIQ / STUDENT
        </div>
        <div style="font-size:38px;font-weight:850;color:#073b5c;letter-spacing:-1px;margin-top:7px;">
            🎓 Student Workspace
        </div>
        <div style="color:#627586;margin-top:6px;font-size:14px;">
            Your AI-powered career intelligence workspace.
        </div>
    </div>
    """)

    if profile is None:
        st.html("""
        <div class="cq-workspace" style="margin-top:25px;">
            <div class="cq-icon">📄</div>
            <div class="cq-card-title">Start with your resume</div>
            <div class="cq-card-text" style="max-width:760px;">
                Upload your resume and let CareerIQ build your personalized
                career profile. Your profile powers job matching, skill
                intelligence, career insights and the AI career assistant.
            </div>
        </div>
        """)

        st.write("")
        if st.button(
            "📄 Upload & Analyze Resume",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["student_feature"] = "📄 Resume Overview"
            st.session_state["page"] = "resume"
            st.rerun()
        return

    name = getattr(profile, "name", "") or "Student"
    display_name = html.escape(str(name))

    st.html(f"""
    <div class="cq-workspace" style="margin-top:20px;">
        <div style="font-size:11px;font-weight:800;color:#0f9f9a;letter-spacing:.7px;">
            PROFILE CONNECTED
        </div>
        <div style="font-size:25px;font-weight:820;color:#073b5c;margin-top:7px;">
            Welcome back, {display_name} 👋
        </div>
        <div style="color:#627586;margin-top:6px;font-size:13px;">
            Your resume profile is ready. Choose a feature from the sidebar to continue.
        </div>
    </div>
    """)

    st.html("""
    <div class="cq-platform-title" style="text-align:left;margin-top:34px;">
        What can you do?
    </div>
    """)

    quick_features = [
        ("🎯", "Job Matching"),
        ("🧠", "Career Insights"),
        ("📊", "Skill Gap"),
        ("🔎", "Job Discovery"),
    ]

    feature_cols = st.columns(4, gap="medium")
    for column, (icon, title) in zip(feature_cols, quick_features):
        with column:
            st.html(f"""
            <div class="cq-platform-card" style="min-height:105px;">
                <div class="cq-platform-icon">{icon}</div>
                <div class="cq-platform-name">{html.escape(title)}</div>
            </div>
            """)


# ============================================================
# COMPANY WORKSPACE
# ============================================================

def company_page():
    """Company workspace landing page."""

    st.html("""
    <div style="margin-bottom:26px;">
        <div style="font-size:12px;color:#ff5a36;font-weight:850;letter-spacing:1px;">
            CAREERIQ / COMPANY
        </div>
        <div style="font-size:38px;font-weight:850;color:#073b5c;letter-spacing:-1px;margin-top:7px;">
            🏢 Company Workspace
        </div>
        <div style="color:#627586;margin-top:6px;font-size:14px;">
            Recruitment intelligence for discovering relevant talent.
        </div>
    </div>

    <div class="cq-workspace">
        <div class="cq-card-title">Recruitment Intelligence</div>
        <div class="cq-card-text">
            Build job requirements, discover relevant candidates and
            manage applications through CareerIQ.
        </div>
        <div class="cq-pills">
            <span class="cq-pill">Job Requirements</span>
            <span class="cq-pill">Candidate Search</span>
            <span class="cq-pill">AI Matching</span>
            <span class="cq-pill">Recruitment Dashboard</span>
        </div>
    </div>

    <div class="cq-platform-title" style="text-align:left;">
        Planned Company Features
    </div>

    <div class="cq-workspace">
        <div class="cq-card-text" style="font-size:14px;line-height:2.1;">
            📋 Upload Job Requirements<br>
            👥 Candidate Search<br>
            🎯 Candidate Matching<br>
            📊 Candidate Ranking<br>
            🔎 Skill-Based Filtering<br>
            📈 Recruitment Dashboard
        </div>
    </div>
    """)

    if st.button("🏠 Back to Home", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()


# ============================================================
# TEMPORARY STUDENT FEATURE PAGE
# ============================================================

def student_feature_page():
    """Temporary student feature page."""

    show_student_sidebar()

    feature = st.session_state.get("student_feature", "Career Feature")
    safe_feature = html.escape(str(feature))

    st.html(f"""
    <div style="margin-bottom:25px;">
        <div style="font-size:12px;color:#ff5a36;font-weight:850;letter-spacing:1px;">
            CAREERIQ / STUDENT
        </div>
        <div style="font-size:38px;font-weight:850;color:#073b5c;margin-top:7px;">
            {safe_feature}
        </div>
    </div>

    <div class="cq-workspace">
        <div class="cq-card-title">🚧 {safe_feature}</div>
        <div class="cq-card-text">
            This module is being connected to the CareerIQ intelligence backend.
        </div>
    </div>
    """)

    if st.button("🏠 Back to Student Workspace", use_container_width=True):
        st.session_state["page"] = "student"
        st.rerun()