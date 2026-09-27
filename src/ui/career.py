import streamlit as st

from src.career.career_recommender import (
    get_career_recommendation,
)


# ============================================================
# CAREER PAGE STATE
# ============================================================

if "career_selected_role" not in st.session_state:
    st.session_state["career_selected_role"] = None


# ============================================================
# PAGE STYLING
# ============================================================

def style_career_page():
    """
    CareerIQ Career Intelligence page styling.

    Custom HTML/CSS is rendered through st.html().
    """

    st.html(
        """
        <style>

        /* ==================================================
           CAREERIQ BACKGROUND
           ================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 7% 5%,
                    rgba(17,169,181,.10),
                    transparent 25%
                ),
                radial-gradient(
                    circle at 93% 8%,
                    rgba(108,99,255,.09),
                    transparent 25%
                ),
                linear-gradient(
                    180deg,
                    #faf9f2 0%,
                    #f6f7f4 100%
                );
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.7rem;
            padding-bottom: 3.5rem;
        }

        /* ==================================================
           HERO
           ================================================== */

        .career-hero {
            position: relative;
            overflow: hidden;

            padding: 34px 38px;

            border-radius: 28px;

            background:
                radial-gradient(
                    circle at 92% 8%,
                    rgba(17,169,181,.18),
                    transparent 27%
                ),
                radial-gradient(
                    circle at 7% 95%,
                    rgba(108,99,255,.12),
                    transparent 30%
                ),
                rgba(255,255,255,.90);

            border: 1px solid rgba(7,59,92,.10);

            box-shadow:
                0 18px 55px rgba(7,59,92,.08);
        }

        .career-badge {
            display: inline-flex;

            padding: 7px 12px;

            border-radius: 999px;

            background: rgba(17,169,181,.09);

            border: 1px solid rgba(17,169,181,.15);

            color: #087789;

            font-size: 10px;

            font-weight: 850;

            letter-spacing: .6px;

            text-transform: uppercase;
        }

        .career-title {
            margin-top: 15px;

            color: #073b5c;

            font-size: 38px;

            line-height: 1.08;

            font-weight: 900;

            letter-spacing: -1.5px;
        }

        .career-title span {
            background:
                linear-gradient(
                    90deg,
                    #073b5c,
                    #11a9b5,
                    #6c63ff
                );

            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .career-subtitle {
            max-width: 780px;

            margin-top: 10px;

            color: #627586;

            font-size: 13px;

            line-height: 1.75;
        }

        /* ==================================================
           SECTION HEADERS
           ================================================== */

        .section-title {
            margin-top: 30px;

            color: #073b5c;

            font-size: 21px;

            font-weight: 850;

            letter-spacing: -.4px;
        }

        .section-subtitle {
            margin-top: 4px;

            color: #718096;

            font-size: 11px;

            line-height: 1.6;
        }

        /* ==================================================
           PROFILE STATUS
           ================================================== */

        .profile-card {
            margin-top: 20px;

            padding: 16px 18px;

            border-radius: 17px;

            background:
                linear-gradient(
                    135deg,
                    rgba(17,169,181,.08),
                    rgba(108,99,255,.06)
                );

            border: 1px solid rgba(17,169,181,.14);
        }

        .profile-label {
            color: #718096;

            font-size: 10px;

            font-weight: 750;

            text-transform: uppercase;

            letter-spacing: .7px;
        }

        .profile-name {
            margin-top: 4px;

            color: #073b5c;

            font-size: 15px;

            font-weight: 850;
        }

        /* ==================================================
           ROLE CARD
           ================================================== */

        .role-card {
            min-height: 185px;

            padding: 21px;

            border-radius: 20px;

            background: rgba(255,255,255,.92);

            border: 1px solid rgba(7,59,92,.09);

            box-shadow:
                0 9px 30px rgba(7,59,92,.055);
        }

        .role-icon {
            width: 44px;
            height: 44px;

            display: flex;

            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background: #f1f8f8;

            font-size: 21px;
        }

        .role-name {
            margin-top: 13px;

            color: #073b5c;

            font-size: 15px;

            font-weight: 850;
        }

        .role-description {
            margin-top: 5px;

            color: #718096;

            font-size: 11px;

            line-height: 1.55;
        }

        /* ==================================================
           METRIC CARDS
           ================================================== */

        .metric-card {
            padding: 20px;

            border-radius: 18px;

            background: rgba(255,255,255,.92);

            border: 1px solid rgba(7,59,92,.09);

            box-shadow:
                0 8px 26px rgba(7,59,92,.05);
        }

        .metric-label {
            color: #718096;

            font-size: 10px;

            font-weight: 750;

            text-transform: uppercase;

            letter-spacing: .6px;
        }

        .metric-value {
            margin-top: 7px;

            color: #073b5c;

            font-size: 27px;

            font-weight: 900;

            letter-spacing: -1px;
        }

        .metric-description {
            margin-top: 3px;

            color: #8a98a5;

            font-size: 10px;
        }

        /* ==================================================
           SKILL CARD
           ================================================== */

        .skill-card {
            padding: 18px;

            border-radius: 17px;

            background: rgba(255,255,255,.90);

            border: 1px solid rgba(7,59,92,.08);

            margin-bottom: 10px;
        }

        .skill-header {
            display: flex;

            align-items: center;

            justify-content: space-between;
        }

        .skill-name {
            color: #073b5c;

            font-size: 12px;

            font-weight: 780;
        }

        .skill-status {
            font-size: 10px;

            font-weight: 800;
        }

        .skill-bar {
            width: 100%;

            height: 7px;

            margin-top: 10px;

            border-radius: 999px;

            background: #e8edf2;

            overflow: hidden;
        }

        .skill-fill {
            height: 100%;

            border-radius: 999px;

            background:
                linear-gradient(
                    90deg,
                    #11a9b5,
                    #6c63ff
                );
        }

        /* ==================================================
           IMPROVEMENT CARD
           ================================================== */

        .improvement-card {
            padding: 18px 20px;

            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    rgba(255,255,255,.96),
                    rgba(247,249,251,.96)
                );

            border: 1px solid rgba(7,59,92,.09);

            margin-bottom: 10px;
        }

        .improvement-number {
            width: 27px;
            height: 27px;

            display: inline-flex;

            align-items: center;
            justify-content: center;

            border-radius: 9px;

            background: rgba(17,169,181,.10);

            color: #087789;

            font-size: 11px;

            font-weight: 850;
        }

        .improvement-text {
            display: inline;

            margin-left: 9px;

            color: #49657a;

            font-size: 12px;

            line-height: 1.55;
        }

        /* ==================================================
           FOOTER
           ================================================== */

        .career-footer {
            margin-top: 35px;

            padding-bottom: 10px;

            text-align: center;

            color: #9aa7b2;

            font-size: 10px;
        }

        /* ==================================================
           STREAMLIT BUTTONS
           ================================================== */

        .stButton > button {
            min-height: 43px;

            border-radius: 12px;

            font-weight: 760;
        }

        </style>
        """
    )


# ============================================================
# HERO
# ============================================================

def show_hero():
    """
    Show Career Intelligence hero section.
    """

    st.html(
        """
        <div class="career-hero">

            <div class="career-badge">
                🧭 Career Intelligence
            </div>

            <div class="career-title">
                Discover Your <span>Career Path</span>
            </div>

            <div class="career-subtitle">
                CareerIQ analyzes your skills, education, experience,
                and profile information to help you understand
                your career readiness and identify practical
                next steps.
            </div>

        </div>
        """
    )


# ============================================================
# PROFILE STATUS
# ============================================================

def show_profile_status(profile):
    """
    Show the connected resume profile.
    """

    if profile is None:

        st.warning(
            "📄 No resume profile is available yet. "
            "Upload and analyze your resume first."
        )

        return False

    name = getattr(
        profile,
        "name",
        ""
    )

    if not name:
        name = "Resume Profile"

    st.html(
        f"""
        <div class="profile-card">

            <div class="profile-label">
                Career Analysis Profile
            </div>

            <div class="profile-name">
                👤 {name}
            </div>

        </div>
        """
    )

    return True


# ============================================================
# PROFILE CONVERSION
# ============================================================

def _profile_to_dict(profile):
    """
    Convert supported profile objects into a dictionary.

    The existing career recommender expects a dictionary.
    """

    if isinstance(profile, dict):
        return profile

    if hasattr(profile, "model_dump"):
        return profile.model_dump()

    if hasattr(profile, "dict"):
        return profile.dict()

    if hasattr(profile, "__dict__"):
        return vars(profile)

    return {}


# ============================================================
# DEFAULT ROLE REQUIREMENTS
# ============================================================

def _default_role_requirements():
    """
    Career role requirements used by the existing recommender.

    These are kept local to the UI because the current
    recommender requires required_skills as an input.
    """

    return {
        "Machine Learning Engineer": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "TensorFlow",
            "PyTorch",
            "Docker",
            "MLOps",
        ],

        "Data Scientist": [
            "Python",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "Data Visualization",
            "Feature Engineering",
        ],

        "AI Engineer": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "LLMs",
            "PyTorch",
            "TensorFlow",
            "FastAPI",
            "Docker",
            "RAG",
        ],

        "Data Analyst": [
            "Python",
            "SQL",
            "Excel",
            "Pandas",
            "Statistics",
            "Data Visualization",
            "Power BI",
            "Tableau",
        ],

        "Backend Developer": [
            "Python",
            "Java",
            "Node.js",
            "SQL",
            "REST API",
            "FastAPI",
            "Flask",
            "Git",
            "Docker",
        ],

        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express.js",
            "SQL",
            "MongoDB",
            "Git",
        ],
    }


# ============================================================
# ROLE ICONS
# ============================================================

def _role_icon(role):
    """
    Return an icon for a career role.
    """

    icons = {
        "Machine Learning Engineer": "🤖",
        "Data Scientist": "📊",
        "AI Engineer": "🧠",
        "Data Analyst": "📈",
        "Backend Developer": "⚙️",
        "Full Stack Developer": "🌐",
    }

    return icons.get(
        role,
        "🎯"
    )


# ============================================================
# ROLE RECOMMENDATION
# ============================================================

def _calculate_role_recommendations(profile_dict):
    """
    Generate recommendations using the existing career
    recommender.

    The existing recommender calculates skill coverage and
    career readiness for the selected role.
    """

    role_requirements = (
        _default_role_requirements()
    )

    recommendations = []

    for role, required_skills in role_requirements.items():

        try:

            result = get_career_recommendation(
                profile=profile_dict,
                recommended_role=role,
                required_skills=required_skills,
            )

            recommendations.append(
                result
            )

        except Exception:
            continue

    recommendations.sort(
        key=lambda item: (
            item.get(
                "career_readiness",
                0.0
            ),
            item.get(
                "skill_coverage",
                0.0
            ),
            item.get(
                "role_score",
                0.0
            ),
        ),
        reverse=True,
    )

    return recommendations


# ============================================================
# ROLE CARD
# ============================================================

def _show_role_card(result):
    """
    Display a career recommendation card.
    """

    role = result.get(
        "recommended_role",
        "Career Role"
    )

    readiness = float(
        result.get(
            "career_readiness",
            0.0
        )
    )

    skill_coverage = float(
        result.get(
            "skill_coverage",
            0.0
        )
    )

    status = result.get(
        "readiness_level",
        "Moderate"
    )

    icon = _role_icon(role)

    st.html(
        f"""
        <div class="role-card">

            <div class="role-icon">
                {icon}
            </div>

            <div class="role-name">
                {role}
            </div>

            <div class="role-description">
                Career readiness:
                <strong>{readiness * 100:.0f}%</strong>
                · Skill coverage:
                <strong>{skill_coverage * 100:.0f}%</strong>
                · {status}
            </div>

        </div>
        """
    )


# ============================================================
# RECOMMENDATION METRICS
# ============================================================

def show_recommendation_metrics(result):
    """
    Show high-level recommendation metrics.
    """

    readiness = float(
        result.get(
            "career_readiness",
            0.0
        )
    )

    coverage = float(
        result.get(
            "skill_coverage",
            0.0
        )
    )

    role_score = float(
        result.get(
            "role_score",
            0.0
        )
    )

    missing = result.get(
        "missing_skills",
        []
    )

    matched = result.get(
        "matched_skills",
        []
    )

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium"
    )

    metrics = [
        (
            col1,
            "Career Readiness",
            readiness,
            "Overall preparation"
        ),
        (
            col2,
            "Skill Coverage",
            coverage,
            "Required skills matched"
        ),
        (
            col3,
            "Role Score",
            role_score,
            "Role suitability"
        ),
        (
            col4,
            "Skills Matched",
            len(matched),
            "Required skills found"
        ),
    ]

    for column, label, value, description in metrics:

        with column:

            if label == "Skills Matched":

                value_text = str(
                    int(value)
                )

            else:

                value_text = (
                    f"{float(value) * 100:.0f}%"
                )

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        {label}
                    </div>

                    <div class="metric-value">
                        {value_text}
                    </div>

                    <div class="metric-description">
                        {description}
                    </div>

                </div>
                """
            )


# ============================================================
# SKILL ANALYSIS
# ============================================================

def show_skill_analysis(result):
    """
    Show matched and missing skills.
    """

    matched = result.get(
        "matched_skills",
        []
    )

    missing = result.get(
        "missing_skills",
        []
    )

    st.html(
        """
        <div class="section-title">
            🧠 Skill Analysis
        </div>

        <div class="section-subtitle">
            See which skills are already covered and which
            skills need further development.
        </div>
        """
    )

    col1, col2 = st.columns(
        2,
        gap="medium"
    )

    with col1:

        st.html(
            """
            <div class="section-title"
                 style="font-size:16px;margin-top:18px;">
                ✅ Matched Skills
            </div>
            """
        )

        if not matched:

            st.info(
                "No matching skills were detected."
            )

        else:

            for skill in matched:

                st.html(
                    f"""
                    <div class="skill-card">

                        <div class="skill-header">

                            <div class="skill-name">
                                {skill}
                            </div>

                            <div class="skill-status"
                                 style="color:#0b9b78;">
                                MATCHED
                            </div>

                        </div>

                        <div class="skill-bar">

                            <div class="skill-fill"
                                 style="
                                    width:100%;
                                    background:#11A9B5;
                                 ">
                            </div>

                        </div>

                    </div>
                    """
                )

    with col2:

        st.html(
            """
            <div class="section-title"
                 style="font-size:16px;margin-top:18px;">
                ⚠️ Skills to Develop
            </div>
            """
        )

        if not missing:

            st.success(
                "No missing skills detected for this role."
            )

        else:

            for skill in missing:

                st.html(
                    f"""
                    <div class="skill-card">

                        <div class="skill-header">

                            <div class="skill-name">
                                {skill}
                            </div>

                            <div class="skill-status"
                                 style="color:#e88900;">
                                DEVELOP
                            </div>

                        </div>

                        <div class="skill-bar">

                            <div class="skill-fill"
                                 style="
                                    width:35%;
                                    background:#f59e0b;
                                 ">
                            </div>

                        </div>

                    </div>
                    """
                )


# ============================================================
# IMPROVEMENT PLAN
# ============================================================

def show_improvement_plan(result):
    """
    Display the existing improvement recommendations.
    """

    recommendations = result.get(
        "improvement_plan",
        []
    )

    st.html(
        """
        <div class="section-title">
            🚀 Recommended Next Steps
        </div>

        <div class="section-subtitle">
            Practical actions generated from the current
            career recommendation.
        </div>
        """
    )

    if not recommendations:

        st.info(
            "No improvement recommendations are available."
        )

        return

    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.html(
            f"""
            <div class="improvement-card">

                <span class="improvement-number">
                    {index}
                </span>

                <span class="improvement-text">
                    {recommendation}
                </span>

            </div>
            """
        )


# ============================================================
# MAIN CAREER PAGE
# ============================================================

def career_page():
    """
    Main Career Intelligence page.
    """

    style_career_page()

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    show_hero()

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    profile = st.session_state.get(
        "profile"
    )

    if not show_profile_status(
        profile
    ):

        st.html(
            """
            <div class="career-footer">
                CareerIQ • AI-powered career intelligence
            </div>
            """
        )

        return

    # --------------------------------------------------------
    # CONVERT PROFILE
    # --------------------------------------------------------

    profile_dict = _profile_to_dict(
        profile
    )

    # --------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # --------------------------------------------------------

    with st.spinner(
        "🧠 Analyzing your career profile..."
    ):

        recommendations = (
            _calculate_role_recommendations(
                profile_dict
            )
        )

    if not recommendations:

        st.error(
            "Career recommendations could not be generated "
            "from the current profile."
        )

        return

    # --------------------------------------------------------
    # TOP RECOMMENDATIONS
    # --------------------------------------------------------

    st.html(
        """
        <div class="section-title">
            🎯 Career Paths For You
        </div>

        <div class="section-subtitle">
            These roles are analyzed using the career
            recommendation engine currently connected
            to CareerIQ.
        </div>
        """
    )

    top_results = recommendations[:3]

    columns = st.columns(
        len(top_results),
        gap="medium"
    )

    for column, result in zip(
        columns,
        top_results
    ):

        with column:

            _show_role_card(
                result
            )

    # --------------------------------------------------------
    # ROLE SELECTION
    # --------------------------------------------------------

    role_names = [
        result.get(
            "recommended_role",
            "Career Role"
        )
        for result in recommendations
    ]

    selected_role = st.selectbox(
        "Analyze a career path",
        role_names,
        key="career_selected_role"
    )

    selected_result = next(
        (
            result
            for result in recommendations
            if result.get(
                "recommended_role"
            ) == selected_role
        ),
        recommendations[0]
    )

    # --------------------------------------------------------
    # SELECTED ROLE HEADER
    # --------------------------------------------------------

    st.html(
        f"""
        <div class="section-title">
            { _role_icon(selected_role) }
            {selected_role}
        </div>

        <div class="section-subtitle">
            Detailed CareerIQ analysis for this career path.
        </div>
        """
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    show_recommendation_metrics(
        selected_result
    )

    # --------------------------------------------------------
    # SKILL ANALYSIS
    # --------------------------------------------------------

    show_skill_analysis(
        selected_result
    )

    # --------------------------------------------------------
    # IMPROVEMENT PLAN
    # --------------------------------------------------------

    show_improvement_plan(
        selected_result
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.html(
        """
        <div class="career-footer">
            CareerIQ • AI-powered career intelligence
        </div>
        """
    )


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def career():
    """
    Compatibility wrapper.

    Existing code can call career() without breaking.
    """

    career_page()
