import streamlit as st
import html


# ============================================================
# CAREER BACKEND IMPORTS
# ============================================================

from src.career.career_recommender import (
    generate_career_recommendation,
)

from src.career.career_roadmap import (
    personalize_roadmap,
)

from src.career.role_predictor import (
    ROLE_REQUIREMENTS,
    predict_career_roles,
)

from src.career.skill_gap_analyzer import (
    analyze_skill_gap,
)


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
            radial-gradient(
                circle at 8% 8%,
                rgba(17,169,181,.10),
                transparent 24%
            ),
            radial-gradient(
                circle at 92% 14%,
                rgba(139,92,246,.08),
                transparent 24%
            ),
            linear-gradient(
                180deg,
                #faf9f2 0%,
                #f7f6ef 100%
            );
        color:var(--cq-ink);
    }

    [data-testid="stHeader"] {
        background:rgba(250,249,242,.82);
    }

    .block-container {
        max-width:1420px;
        padding-top:2rem;
        padding-bottom:3.5rem;
        background-image:
            radial-gradient(
                rgba(7,59,92,.12) .7px,
                transparent .7px
            );
        background-size:26px 26px;
    }

    h1,h2,h3,h4,p,li {
        color:var(--cq-ink);
    }

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
        background:
            linear-gradient(
                90deg,
                var(--cq-cyan),
                #159aa8
            );
        font-size:12px;
        font-weight:800;
        box-shadow:
            0 8px 24px
            rgba(17,169,181,.20);
    }

    .cq-hero {
        padding:48px 42px 42px;
        border:1px solid var(--cq-border);
        border-radius:26px;
        background:
            radial-gradient(
                circle at 86% 12%,
                rgba(17,169,181,.15),
                transparent 24%
            ),
            radial-gradient(
                circle at 68% 100%,
                rgba(139,92,246,.10),
                transparent 28%
            ),
            rgba(255,255,255,.68);
        box-shadow:
            0 18px 55px
            rgba(7,59,92,.07);
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
        background:
            linear-gradient(
                90deg,
                var(--cq-cyan),
                var(--cq-purple),
                var(--cq-coral)
            );
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .cq-gradient-line {
        height:3px;
        width:100%;
        margin:20px 0 18px;
        border-radius:999px;
        background:
            linear-gradient(
                90deg,
                var(--cq-cyan),
                var(--cq-purple),
                var(--cq-coral)
            );
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
        box-shadow:
            0 10px 32px
            rgba(7,59,92,.055);
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

    .cq-platform-icon {
        font-size:28px;
        margin-bottom:7px;
    }

    .cq-platform-name {
        color:var(--cq-ink);
        font-size:13px;
        font-weight:780;
    }

    .cq-platform-text {
        color:var(--cq-muted);
        font-size:11px;
        line-height:1.5;
        margin-top:5px;
    }

    .cq-footer {
        text-align:center;
        color:#72818d;
        font-size:11px;
        margin-top:48px;
        padding-top:20px;
        border-top:1px solid var(--cq-border);
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #eeebda 0%,
                #e8e6d8 100%
            );
        border-right:1px solid var(--cq-border);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color:var(--cq-ink) !important;
    }

    section[data-testid="stSidebar"] p {
        color:var(--cq-muted);
    }

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

    .cq-metric-card {
        padding:20px;
        border-radius:18px;
        border:1px solid var(--cq-border);
        background:rgba(255,255,255,.82);
        box-shadow:
            0 8px 25px
            rgba(7,59,92,.05);
        min-height:120px;
    }

    .cq-metric-label {
        color:var(--cq-muted);
        font-size:12px;
        font-weight:700;
    }

    .cq-metric-value {
        color:var(--cq-ink);
        font-size:29px;
        font-weight:850;
        margin-top:8px;
    }

    .cq-progress-card {
        padding:24px;
        border-radius:20px;
        border:1px solid var(--cq-border);
        background:rgba(255,255,255,.82);
        margin-bottom:18px;
    }

    .cq-phase-card {
        padding:22px;
        border-radius:18px;
        border:1px solid var(--cq-border);
        background:rgba(255,255,255,.82);
        margin-bottom:15px;
    }

    .cq-phase-title {
        color:var(--cq-ink);
        font-size:18px;
        font-weight:800;
    }

    .cq-small {
        color:var(--cq-muted);
        font-size:12px;
        line-height:1.6;
    }

    .skill-pill {
        display:inline-block;
        padding:6px 10px;
        margin:3px;
        border-radius:999px;
        background:#f0f7f8;
        border:1px solid rgba(17,169,181,.15);
        color:#225d73;
        font-size:11px;
        font-weight:700;
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
            <div class="cq-brand-sub">
                AI Career Intelligence Platform
            </div>
        </div>

        <div class="cq-top-pill">
            AI-Powered Career Intelligence
        </div>
    </div>

    <div class="cq-hero">
        <div class="cq-kicker">
            CAREERIQ / INTELLIGENCE PLATFORM
        </div>

        <div class="cq-title">
            Build Your <span>Career</span><br>
            With Intelligence
        </div>

        <div class="cq-gradient-line"></div>

        <div class="cq-subtitle">
            CareerIQ analyzes resumes, skills, experience and
            opportunities to help students understand their
            career profile and help companies discover
            relevant talent.
        </div>
    </div>

    <div class="cq-section-title">
        Choose your workspace
    </div>

    <div class="cq-section-subtitle">
        Select how you want to use CareerIQ
    </div>
    """)

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.html("""
        <div class="cq-workspace">
            <div class="cq-icon">🎓</div>

            <div class="cq-card-title">
                Student Workspace
            </div>

            <div class="cq-card-text">
                Analyze your resume, discover relevant jobs,
                identify skill gaps and build a personalized
                career roadmap.
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

            <div class="cq-card-title">
                Company Workspace
            </div>

            <div class="cq-card-text">
                Create jobs, define hiring requirements and
                review candidates using CareerIQ's matching
                and recruitment intelligence.
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
        (
            "📄",
            "Resume Intelligence",
            "Extract and understand your career profile.",
        ),
        (
            "🎯",
            "AI Job Matching",
            "Compare your profile with relevant opportunities.",
        ),
        (
            "📊",
            "Skill Intelligence",
            "Find missing skills and prioritize what to learn.",
        ),
        (
            "🤖",
            "AI Career Assistant",
            "Get personalized career guidance from your profile.",
        ),
    ]

    feature_cols = st.columns(4, gap="medium")

    for column, (icon, name, description) in zip(
        feature_cols,
        features,
    ):
        with column:

            st.html(
                f"""
                <div class="cq-platform-card">
                    <div class="cq-platform-icon">
                        {icon}
                    </div>

                    <div class="cq-platform-name">
                        {html.escape(name)}
                    </div>

                    <div class="cq-platform-text">
                        {html.escape(description)}
                    </div>
                </div>
                """
            )

    st.html("""
    <div class="cq-footer">
        CareerIQ • AI-powered career intelligence platform
    </div>
    """)


# ============================================================
# STUDENT WORKSPACE
# ============================================================

def student_page():
    """Main Student workspace."""

    profile = st.session_state.get("profile")

    st.html("""
    <div style="margin-bottom:28px;">

        <div style="
            font-size:12px;
            color:#ff5a36;
            font-weight:850;
            letter-spacing:1px;
        ">
            CAREERIQ / STUDENT
        </div>

        <div style="
            font-size:38px;
            font-weight:850;
            color:#073b5c;
            letter-spacing:-1px;
            margin-top:7px;
        ">
            🎓 Student Workspace
        </div>

        <div style="
            color:#627586;
            margin-top:6px;
            font-size:14px;
        ">
            Your AI-powered career intelligence workspace.
        </div>

    </div>
    """)

    if profile is None:

        st.html("""
        <div class="cq-workspace" style="margin-top:25px;">

            <div class="cq-icon">
                📄
            </div>

            <div class="cq-card-title">
                Start with your resume
            </div>

            <div class="cq-card-text" style="max-width:760px;">
                Upload your resume and let CareerIQ build
                your personalized career profile. Your
                profile powers job matching, skill
                intelligence, career insights and the
                AI career assistant.
            </div>

        </div>
        """)

        st.write("")

        if st.button(
            "📄 Upload & Analyze Resume",
            type="primary",
            use_container_width=True,
        ):

            st.session_state[
                "student_feature"
            ] = "📄 Resume Overview"

            st.session_state[
                "page"
            ] = "resume"

            st.rerun()

        return

    name = getattr(
        profile,
        "name",
        "",
    ) or "Student"

    display_name = html.escape(
        str(name)
    )

    st.html(
        f"""
        <div class="cq-workspace" style="margin-top:20px;">

            <div style="
                font-size:11px;
                font-weight:800;
                color:#0f9f9a;
                letter-spacing:.7px;
            ">
                PROFILE CONNECTED
            </div>

            <div style="
                font-size:25px;
                font-weight:820;
                color:#073b5c;
                margin-top:7px;
            ">
                Welcome back, {display_name} 👋
            </div>

            <div style="
                color:#627586;
                margin-top:6px;
                font-size:13px;
            ">
                Your resume profile is ready. Choose a
                feature from the sidebar to continue.
            </div>

        </div>
        """
    )

    st.html("""
    <div class="cq-platform-title"
         style="text-align:left;margin-top:34px;">
        What can you do?
    </div>
    """)

    quick_features = [
        ("🎯", "Job Matching"),
        ("🧠", "Career Insights"),
        ("📊", "Skill Gap"),
        ("🔎", "Job Discovery"),
    ]

    feature_cols = st.columns(
        4,
        gap="medium",
    )

    for column, (icon, title) in zip(
        feature_cols,
        quick_features,
    ):

        with column:

            st.html(
                f"""
                <div class="cq-platform-card"
                     style="min-height:105px;">

                    <div class="cq-platform-icon">
                        {icon}
                    </div>

                    <div class="cq-platform-name">
                        {html.escape(title)}
                    </div>

                </div>
                """
            )


# ============================================================
# COMPANY WORKSPACE
# ============================================================

def company_page():
    """Company workspace landing page."""

    st.html("""
    <div style="margin-bottom:26px;">

        <div style="
            font-size:12px;
            color:#ff5a36;
            font-weight:850;
            letter-spacing:1px;
        ">
            CAREERIQ / COMPANY
        </div>

        <div style="
            font-size:38px;
            font-weight:850;
            color:#073b5c;
            letter-spacing:-1px;
            margin-top:7px;
        ">
            🏢 Company Workspace
        </div>

        <div style="
            color:#627586;
            margin-top:6px;
            font-size:14px;
        ">
            Recruitment intelligence for discovering
            relevant talent.
        </div>

    </div>

    <div class="cq-workspace">

        <div class="cq-card-title">
            Recruitment Intelligence
        </div>

        <div class="cq-card-text">
            Build job requirements, discover relevant
            candidates and manage applications through
            CareerIQ.
        </div>

        <div class="cq-pills">
            <span class="cq-pill">
                Job Requirements
            </span>

            <span class="cq-pill">
                Candidate Search
            </span>

            <span class="cq-pill">
                AI Matching
            </span>

            <span class="cq-pill">
                Recruitment Dashboard
            </span>
        </div>

    </div>

    <div class="cq-platform-title"
         style="text-align:left;">
        Planned Company Features
    </div>

    <div class="cq-workspace">

        <div class="cq-card-text"
             style="font-size:14px;line-height:2.1;">

            📋 Upload Job Requirements<br>
            👥 Candidate Search<br>
            🎯 Candidate Matching<br>
            📊 Candidate Ranking<br>
            🔎 Skill-Based Filtering<br>
            📈 Recruitment Dashboard

        </div>

    </div>
    """)

    if st.button(
        "🏠 Back to Home",
        use_container_width=True,
    ):

        st.session_state["page"] = "home"
        st.rerun()


# ============================================================
# PROFILE → DICTIONARY
# ============================================================

def _profile_to_dict(profile):
    """
    Convert ResumeProfile / object / dictionary into
    the dictionary format expected by career backends.
    """

    if profile is None:
        return {}

    if isinstance(profile, dict):
        return profile

    return {
        "name": getattr(
            profile,
            "name",
            "",
        ),
        "education": getattr(
            profile,
            "education",
            [],
        ) or [],
        "skills": getattr(
            profile,
            "skills",
            [],
        ) or [],
        "projects": getattr(
            profile,
            "projects",
            [],
        ) or [],
        "experience": getattr(
            profile,
            "experience",
            [],
        ) or [],
        "certifications": getattr(
            profile,
            "certifications",
            [],
        ) or [],
    }


# ============================================================
# CAREER ROLE REQUIREMENTS
# ============================================================

ROLE_REQUIRED_SKILLS = {
    role: data.get(
        "skills",
        [],
    )
    for role, data in ROLE_REQUIREMENTS.items()
}


# ============================================================
# CAREER DASHBOARD
# ============================================================

def _render_career_dashboard(profile):
    """
    Render the Career Dashboard using the existing
    CareerIQ career intelligence backend.
    """

    profile_data = _profile_to_dict(profile)

    if not profile_data:
        st.warning(
            "Please upload and analyze your resume first."
        )
        return

    skills = profile_data.get(
        "skills",
        [],
    ) or []

    projects = profile_data.get(
        "projects",
        [],
    ) or []

    education = profile_data.get(
        "education",
        [],
    ) or []

    experience = profile_data.get(
        "experience",
        [],
    ) or []

    certifications = profile_data.get(
        "certifications",
        [],
    ) or []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html("""
    <div style="margin-bottom:26px;">

        <div style="
            font-size:12px;
            color:#ff5a36;
            font-weight:850;
            letter-spacing:1px;
        ">
            CAREERIQ / INTELLIGENCE
        </div>

        <div style="
            font-size:38px;
            font-weight:850;
            color:#073b5c;
            margin-top:7px;
        ">
            📈 Career Dashboard
        </div>

        <div style="
            color:#627586;
            margin-top:6px;
            font-size:14px;
        ">
            A consolidated view of your career profile,
            skills and career readiness.
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------------

    st.subheader("👤 Profile Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Skills",
            len(skills),
        )

    with col2:
        st.metric(
            "Projects",
            len(projects),
        )

    with col3:
        st.metric(
            "Education",
            len(education),
        )

    with col4:
        st.metric(
            "Certifications",
            len(certifications),
        )

    # --------------------------------------------------------
    # CAREER ANALYSIS
    # --------------------------------------------------------

    if not skills:

        st.warning(
            "No skills were found in your resume. "
            "Career intelligence requires resume skills."
        )

        return

    if st.button(
        "🔍 Analyze My Career",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Analyzing your career profile..."
        ):

            try:

                predictions = predict_career_roles(
                    profile,
                    top_k=4,
                )

                st.session_state[
                    "career_role_predictions"
                ] = predictions

                if predictions:

                    st.session_state[
                        "career_selected_role"
                    ] = predictions[0]["role"]

                st.session_state[
                    "career_insights_analyzed"
                ] = True

            except Exception as exc:

                st.error(
                    f"Career analysis failed: {exc}"
                )

        st.rerun()

    predictions = st.session_state.get(
        "career_role_predictions",
        [],
    )

    # --------------------------------------------------------
    # NO ANALYSIS YET
    # --------------------------------------------------------

    if not predictions:

        st.info(
            "Click **Analyze My Career** to generate "
            "your personalized career insights."
        )

        return

    # --------------------------------------------------------
    # ROLE RECOMMENDATIONS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🎯 Career Role Recommendations"
    )

    for prediction in predictions[:3]:

        role = str(
            prediction.get(
                "role",
                "Unknown Role",
            )
        )

        score = float(
            prediction.get(
                "score",
                0.0,
            ) or 0.0
        )

        matched = prediction.get(
            "matched_skills",
            [],
        ) or []

        missing = prediction.get(
            "missing_skills",
            [],
        ) or []

        st.html(
            f"""
            <div class="cq-progress-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                ">

                    <div style="
                        font-size:20px;
                        font-weight:820;
                        color:#073b5c;
                    ">
                        {html.escape(role)}
                    </div>

                    <div style="
                        font-size:24px;
                        font-weight:850;
                        color:#0f9f9a;
                    ">
                        {score * 100:.1f}%
                    </div>

                </div>

                <div class="cq-small"
                     style="margin-top:8px;">
                    Role suitability based on your
                    current profile.
                </div>

                <div class="cq-small"
                     style="margin-top:10px;">

                    <b>Matched:</b> {len(matched)}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    <b>Missing:</b> {len(missing)}

                </div>

            </div>
            """
        )

    # --------------------------------------------------------
    # SELECT ROLE
    # --------------------------------------------------------

    roles = [
        item["role"]
        for item in predictions
        if item.get("role")
    ]

    if not roles:
        st.warning(
            "No career roles could be generated."
        )
        return

    default_role = st.session_state.get(
        "career_selected_role",
        roles[0],
    )

    if default_role not in roles:
        default_role = roles[0]

    selected_role = st.selectbox(
        "Choose a role for detailed insights",
        roles,
        index=roles.index(default_role),
        key="career_role_selector",
    )

    selected_prediction = next(
        (
            item
            for item in predictions
            if item["role"] == selected_role
        ),
        None,
    )

    if selected_prediction is None:
        return

    # --------------------------------------------------------
    # CAREER RECOMMENDATION
    # --------------------------------------------------------

    try:

        recommendation = (
            generate_career_recommendation(
                profile=profile_data,
                recommended_role=selected_role,
                required_skills=ROLE_REQUIRED_SKILLS.get(
                    selected_role,
                    [],
                ),
                role_score=selected_prediction.get(
                    "score",
                    0.0,
                ),
            )
        )

        st.session_state[
            "career_selected_role"
        ] = selected_role

        st.session_state[
            "career_recommendation"
        ] = recommendation

    except Exception as exc:

        st.error(
            f"Unable to generate career recommendation: {exc}"
        )
        return

    # --------------------------------------------------------
    # CAREER METRICS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        f"📌 {selected_role}"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Role Suitability",
            f'{recommendation.get("role_score", 0) * 100:.1f}%',
        )

    with c2:
        st.metric(
            "Skill Coverage",
            f'{recommendation.get("skill_coverage", 0) * 100:.1f}%',
        )

    with c3:
        st.metric(
            "Career Readiness",
            f'{recommendation.get("career_readiness", 0) * 100:.1f}%',
        )

    # --------------------------------------------------------
    # READINESS LEVEL
    # --------------------------------------------------------

    readiness_level = recommendation.get(
        "readiness_level",
        "Needs Improvement",
    )

    st.info(
        f"Career Readiness Level: **{readiness_level}**"
    )

    # --------------------------------------------------------
    # MATCHED / MISSING SKILLS
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### ✅ Matched Skills"
        )

        matched = recommendation.get(
            "matched_skills",
            [],
        ) or []

        if matched:

            pills = "".join(
                f"""
                <span class="skill-pill">
                    {html.escape(str(skill))}
                </span>
                """
                for skill in matched
            )

            st.html(
                f'<div>{pills}</div>'
            )

        else:

            st.info(
                "No matching skills found yet."
            )

    with right:

        st.markdown(
            "### 📚 Missing Skills"
        )

        missing = recommendation.get(
            "missing_skills",
            [],
        ) or []

        if missing:

            pills = "".join(
                f"""
                <span class="skill-pill">
                    {html.escape(str(skill))}
                </span>
                """
                for skill in missing
            )

            st.html(
                f'<div>{pills}</div>'
            )

        else:

            st.success(
                "No major required skills are missing."
            )

    # --------------------------------------------------------
    # IMPROVEMENT PLAN
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🚀 Improvement Plan"
    )

    improvement_plan = recommendation.get(
        "improvement_plan",
        [],
    ) or []

    if improvement_plan:

        for number, item in enumerate(
            improvement_plan,
            start=1,
        ):

            st.write(
                f"**{number}.** {item}"
            )

    else:

        st.info(
            "No improvement recommendations available."
        )

    # --------------------------------------------------------
    # DETAILED SKILL GAP
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔎 Detailed Skill Gap"
    )

    required_skills = ROLE_REQUIRED_SKILLS.get(
        selected_role,
        [],
    )

    try:

        gap_result = analyze_skill_gap(
            user_skills=skills,
            required_skills=required_skills,
            target_role=selected_role,
        )

        st.session_state[
            "career_skill_gap"
        ] = gap_result

    except Exception as exc:

        st.warning(
            f"Skill gap analysis could not be loaded: {exc}"
        )

        gap_result = {}

    gc1, gc2, gc3 = st.columns(3)

    with gc1:
        st.metric(
            "Required Skills",
            gap_result.get(
                "total_required_skills",
                len(required_skills),
            ),
        )

    with gc2:
        st.metric(
            "Matched Skills",
            gap_result.get(
                "total_matched_skills",
                len(
                    recommendation.get(
                        "matched_skills",
                        [],
                    )
                ),
            ),
        )

    with gc3:
        st.metric(
            "Missing Skills",
            gap_result.get(
                "total_missing_skills",
                len(
                    recommendation.get(
                        "missing_skills",
                        [],
                    )
                ),
            ),
        )

    # --------------------------------------------------------
    # ROADMAP BUTTON
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "🗺️ Open Career Roadmap",
        use_container_width=True,
    ):

        st.session_state[
            "student_feature"
        ] = "🗺️ Career Roadmap"

        st.session_state[
            "page"
        ] = "student_feature"

        st.rerun()


# ============================================================
# CAREER ROADMAP
# ============================================================

def _render_career_roadmap(profile):
    """
    Render a personalized career roadmap using the
    existing CareerIQ career roadmap backend.
    """

    profile_data = _profile_to_dict(
        profile
    )

    if not profile_data:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    skills = profile_data.get(
        "skills",
        [],
    ) or []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.html("""
    <div style="margin-bottom:26px;">

        <div style="
            font-size:12px;
            color:#ff5a36;
            font-weight:850;
            letter-spacing:1px;
        ">
            CAREERIQ / CAREER PLANNING
        </div>

        <div style="
            font-size:38px;
            font-weight:850;
            color:#073b5c;
            margin-top:7px;
        ">
            🗺️ Career Roadmap
        </div>

        <div style="
            color:#627586;
            margin-top:6px;
            font-size:14px;
        ">
            A personalized learning path based on your
            current skills and target career role.
        </div>

    </div>
    """)

    if not skills:

        st.warning(
            "Your resume does not contain any skills yet. "
            "Upload a resume with skills to build a roadmap."
        )

        return

    # --------------------------------------------------------
    # GET EXISTING ROLE PREDICTIONS
    # --------------------------------------------------------

    predictions = st.session_state.get(
        "career_role_predictions",
        [],
    )

    if not predictions:

        with st.spinner(
            "Finding suitable career roles..."
        ):

            try:

                predictions = predict_career_roles(
                    profile,
                    top_k=4,
                )

                st.session_state[
                    "career_role_predictions"
                ] = predictions

            except Exception as exc:

                st.error(
                    f"Unable to determine career roles: {exc}"
                )

                return

    if not predictions:

        st.warning(
            "No suitable career role could be identified "
            "from your current resume."
        )

        return

    roles = [
        item["role"]
        for item in predictions
        if item.get("role")
    ]

    if not roles:

        st.warning(
            "No roadmap role is available."
        )

        return

    # --------------------------------------------------------
    # ROLE SELECTION
    # --------------------------------------------------------

    default_role = st.session_state.get(
        "career_selected_role",
        roles[0],
    )

    if default_role not in roles:
        default_role = roles[0]

    selected_role = st.selectbox(
        "Choose your target role",
        roles,
        index=roles.index(default_role),
        key="roadmap_role_selector",
    )

    st.session_state[
        "career_selected_role"
    ] = selected_role

    # --------------------------------------------------------
    # GENERATE PERSONALIZED ROADMAP
    # --------------------------------------------------------

    try:

        roadmap = personalize_roadmap(
            target_role=selected_role,
            user_skills=skills,
        )

        st.session_state[
            "career_roadmap"
        ] = roadmap

    except ValueError as exc:

        st.error(
            str(exc)
        )

        return

    except Exception as exc:

        st.error(
            f"Unable to generate career roadmap: {exc}"
        )

        return

    # --------------------------------------------------------
    # ROADMAP SUMMARY
    # --------------------------------------------------------

    target_role = roadmap.get(
        "target_role",
        selected_role,
    )

    description = roadmap.get(
        "description",
        "",
    )

    overall_completion = float(
        roadmap.get(
            "overall_completion",
            0.0,
        ) or 0.0
    )

    st.html(
        f"""
        <div class="cq-progress-card">

            <div style="
                font-size:12px;
                color:#ff5a36;
                font-weight:850;
                letter-spacing:1px;
            ">
                TARGET ROLE
            </div>

            <div style="
                font-size:26px;
                font-weight:850;
                color:#073b5c;
                margin-top:6px;
            ">
                {html.escape(str(target_role))}
            </div>

            <div class="cq-small"
                 style="margin-top:8px;">
                {html.escape(str(description))}
            </div>

        </div>
        """
    )

    st.subheader(
        "📊 Overall Roadmap Progress"
    )

    st.progress(
        max(
            0.0,
            min(
                overall_completion / 100.0,
                1.0,
            ),
        )
    )

    st.metric(
        "Overall Completion",
        f"{overall_completion:.1f}%",
    )

    # --------------------------------------------------------
    # PHASES
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🧭 Learning Phases"
    )

    phases = roadmap.get(
        "phases",
        [],
    ) or []

    for phase in phases:

        phase_number = phase.get(
            "phase",
            "",
        )

        phase_title = phase.get(
            "title",
            "Career Phase",
        )

        duration = phase.get(
            "duration",
            "",
        )

        completion = float(
            phase.get(
                "completion_percentage",
                0.0,
            ) or 0.0
        )

        completed_skills = phase.get(
            "completed_skills",
            [],
        ) or []

        missing_skills = phase.get(
            "missing_skills",
            [],
        ) or []

        projects = phase.get(
            "projects",
            [],
        ) or []

        st.html(
            f"""
            <div class="cq-phase-card">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:20px;
                ">

                    <div class="cq-phase-title">
                        Phase {phase_number} —
                        {html.escape(str(phase_title))}
                    </div>

                    <div style="
                        font-size:13px;
                        font-weight:800;
                        color:#0f9f9a;
                    ">
                        {completion:.1f}%
                    </div>

                </div>

                <div class="cq-small"
                     style="margin-top:7px;">
                    Duration: {html.escape(str(duration))}
                </div>

            </div>
            """
        )

        st.progress(
            max(
                0.0,
                min(
                    completion / 100.0,
                    1.0,
                ),
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "#### ✅ Skills You Have"
            )

            if completed_skills:

                pills = "".join(
                    f"""
                    <span class="skill-pill">
                        {html.escape(str(skill))}
                    </span>
                    """
                    for skill in completed_skills
                )

                st.html(
                    f"<div>{pills}</div>"
                )

            else:

                st.info(
                    "No skills from this phase "
                    "are currently detected."
                )

        with col2:

            st.markdown(
                "#### 📚 Skills to Learn"
            )

            if missing_skills:

                pills = "".join(
                    f"""
                    <span class="skill-pill">
                        {html.escape(str(skill))}
                    </span>
                    """
                    for skill in missing_skills
                )

                st.html(
                    f"<div>{pills}</div>"
                )

            else:

                st.success(
                    "You currently cover all skills "
                    "in this phase."
                )

        if projects:

            st.markdown(
                "#### 🛠️ Recommended Projects"
            )

            for project in projects:

                st.write(
                    f"• {project}"
                )

        st.divider()


# ============================================================
# STUDENT FEATURE ROUTER
# ============================================================

def student_feature_page():
    """
    Route student career features to their real
    implementations.

    Other dedicated features remain handled by
    their existing pages.
    """

    feature = st.session_state.get(
        "student_feature",
        "📄 Resume Overview",
    )

    profile = st.session_state.get(
        "profile"
    )

    # --------------------------------------------------------
    # CAREER DASHBOARD
    # --------------------------------------------------------

    if feature == "📈 Career Dashboard":

        _render_career_dashboard(
            profile
        )

        return

    # --------------------------------------------------------
    # CAREER ROADMAP
    # --------------------------------------------------------

    if feature == "🗺️ Career Roadmap":

        _render_career_roadmap(
            profile
        )

        return

    # --------------------------------------------------------
    # OTHER FEATURES
    # --------------------------------------------------------

    st.html(
        f"""
        <div style="margin-bottom:25px;">

            <div style="
                font-size:12px;
                color:#ff5a36;
                font-weight:850;
                letter-spacing:1px;
            ">
                CAREERIQ / STUDENT
            </div>

            <div style="
                font-size:38px;
                font-weight:850;
                color:#073b5c;
                margin-top:7px;
            ">
                {html.escape(str(feature))}
            </div>

        </div>

        <div class="cq-workspace">

            <div class="cq-card-title">
                🚧 {html.escape(str(feature))}
            </div>

            <div class="cq-card-text">
                This feature is handled by its
                dedicated CareerIQ module.
            </div>

        </div>
        """
    )

    if st.button(
        "🏠 Back to Student Workspace",
        use_container_width=True,
    ):

        st.session_state[
            "page"
        ] = "student"

        st.rerun()