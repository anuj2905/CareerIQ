import streamlit as st


# ============================================================
# CareerIQ - Shared Student Sidebar
# ============================================================

STUDENT_PAGES = {
    "student",
    "resume",
    "assistant",
    "jobs",
    "salary_prediction",
    "student_feature",
    "job_details",
    "job_applications",
}


def _go_to(page, feature=None, upload=False):
    """Update student navigation state and rerun the app."""

    if feature is not None:
        st.session_state["student_feature"] = feature

    st.session_state["page"] = page

    if upload:
        st.session_state["resume_upload_mode"] = True
        st.session_state["resume_upload_generation"] = (
            st.session_state.get("resume_upload_generation", 0) + 1
        )
    else:
        if page != "resume":
            st.session_state["resume_upload_mode"] = False

    st.rerun()


def show_student_sidebar():
    """
    Render the single shared Student Workspace sidebar.

    This function is called once from app.py.
    Other student pages do not create their own sidebar.
    """

    current_page = st.session_state.get("page", "student")
    current_feature = st.session_state.get(
        "student_feature",
        "📄 Resume Overview",
    )

    # ========================================================
    # SIDEBAR STYLING
    # ========================================================

    st.html("""
    <style>

    /* ------------------------------------------------------
       CareerIQ Sidebar
       ------------------------------------------------------ */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #eeebda 0%,
            #e8e6d8 100%
        );

        border-right: 1px solid rgba(7, 59, 92, 0.12);
    }

    /* Keep Streamlit's sidebar collapse/expand control visible */
    section[data-testid="stSidebar"] button[kind="header"] {
        visibility: visible !important;
        display: flex !important;
    }

    /* Sidebar navigation buttons */
    section[data-testid="stSidebar"] .stButton > button {
        border-radius: 11px;
        min-height: 42px;
        font-weight: 700;
    }

    </style>
    """)

    # ========================================================
    # HEADER
    # ========================================================

    st.sidebar.html("""
    <div style="
        padding:8px 4px 14px;
        color:#073b5c;
    ">
        <div style="
            font-size:24px;
            font-weight:850;
            letter-spacing:-.5px;
        ">
            🧠 CareerIQ
        </div>

        <div style="
            font-size:11px;
            color:#627586;
            margin-top:3px;
            font-weight:650;
        ">
            Student Workspace
        </div>
    </div>
    """)

    st.sidebar.divider()

    # ========================================================
    # RESUME
    # ========================================================

    st.sidebar.subheader("📄 Resume")

    if st.sidebar.button(
        "📄 Resume Overview",
        use_container_width=True,
        key="student_nav_resume_overview",
    ):
        _go_to(
            "resume",
            "📄 Resume Overview",
        )

    if st.sidebar.button(
        "🔄 Upload New Resume",
        use_container_width=True,
        key="student_nav_upload_resume",
    ):
        _go_to(
            "resume",
            "📤 Upload New Resume",
            upload=True,
        )

    # ========================================================
    # CAREER INTELLIGENCE
    # ========================================================

    st.sidebar.subheader("🧠 Career Intelligence")

    if st.sidebar.button(
        "🎯 Job Matching",
        use_container_width=True,
        key="student_nav_job_matching",
    ):
        _go_to(
            "resume",
            "🎯 Job Matching",
        )

    if st.sidebar.button(
        "🧠 Career Insights",
        use_container_width=True,
        key="student_nav_career_insights",
    ):
        _go_to(
            "resume",
            "🧠 Career Insights",
        )

    if st.sidebar.button(
        "📊 Skill Gap Analysis",
        use_container_width=True,
        key="student_nav_skill_gap",
    ):
        _go_to(
            "resume",
            "📊 Skill Gap Analysis",
        )

    # ========================================================
    # AI
    # ========================================================

    st.sidebar.subheader("🤖 AI")

    if st.sidebar.button(
        "🤖 AI Career Assistant",
        use_container_width=True,
        key="student_nav_assistant",
    ):
        _go_to(
            "assistant",
            "🤖 AI Career Assistant",
        )

    # ========================================================
    # OPPORTUNITIES
    # ========================================================

    st.sidebar.subheader("🔎 Opportunities")

    if st.sidebar.button(
        "🔎 Job Discovery",
        use_container_width=True,
        key="student_nav_jobs",
    ):
        _go_to(
            "jobs",
            "🔎 Job Discovery",
        )

    # ========================================================
    # SALARY INTELLIGENCE
    # ========================================================

    st.sidebar.subheader("💰 Salary Intelligence")

    if st.sidebar.button(
        "💰 Salary Prediction",
        use_container_width=True,
        key="student_nav_salary_prediction",
    ):
        _go_to(
            "salary_prediction",
            "💰 Salary Prediction",
        )

    # ========================================================
    # CAREER PLANNING
    # ========================================================

    st.sidebar.subheader("📈 Career Planning")

    if st.sidebar.button(
        "📈 Career Dashboard",
        use_container_width=True,
        key="student_nav_dashboard",
    ):
        _go_to(
            "student_feature",
            "📈 Career Dashboard",
        )

    if st.sidebar.button(
        "🗺️ Career Roadmap",
        use_container_width=True,
        key="student_nav_roadmap",
    ):
        _go_to(
            "student_feature",
            "🗺️ Career Roadmap",
        )

    # ========================================================
    # HOME
    # ========================================================

    st.sidebar.divider()

    if st.sidebar.button(
        "🏠 Back to Home",
        use_container_width=True,
        key="student_nav_home",
    ):
        st.session_state["page"] = "home"
        st.session_state["student_feature"] = "📄 Resume Overview"
        st.session_state["resume_upload_mode"] = False
        st.rerun()