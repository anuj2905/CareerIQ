
import streamlit as st
import html


# ==================================================
# IMPORTS
# ==================================================

from src.career.career_roadmap import (
    personalize_roadmap
)

from src.career.role_predictor import (
    ROLE_REQUIREMENTS,
    predict_career_roles
)

from src.career.career_recommender import (
    generate_career_recommendation
)

from src.resume.parser import (
    extract_text_from_file
)

from src.career.skill_gap_analyzer import (
    analyze_skill_gap
)

from src.resume.skill_extractor import (
    ResumeProfile,
    extract_resume_profile
)

from src.matching.job_matcher.skill_matcher import (
    calculate_skill_match
)

from src.matching.job_matcher.education_matcher import (
    calculate_education_match
)

from src.matching.job_matcher.experience_matcher import (
    calculate_final_experience_match
)

from src.ui.components.match_charts import (
    show_job_match_dashboard
)

# AI Career Assistant
from src.ui.assistant import (
    assistant_page
)

# DATABASE
from src.database.models import (
    create_student_profile
)

from src.database.repositories import (
    save_student_profile,
    get_student_profile
)

from src.database.repositories import (
    get_student_id_for_user,
    ensure_student_profile_for_user,
    save_student_profile,
    get_student_profile,
)

# JOB DISCOVERY
from src.job_discovery.job_fetcher import (
    fetch_remote_jobs
)



# ==================================================
# SKILL GAP ROLE REQUIREMENTS
# ==================================================

ROLE_REQUIRED_SKILLS = {
    role: data["skills"]
    for role, data in ROLE_REQUIREMENTS.items()
}

# ==================================================
# DATABASE PROFILE LOADER
# ==================================================

def _get_current_student_id() -> int | None:
    """
    Resolve the authenticated student's real profile ID.

    For a newly registered student, student_accounts.student_id may be NULL.
    In that case, create the initial student_profiles row and link it to the
    authenticated user through the repository layer.
    """
    user_id = st.session_state.get("user_id")
    user_role = st.session_state.get("user_role")

    if user_id is None or user_role != "student":
        return None

    try:
        user_id = int(user_id)

        student_id = get_student_id_for_user(user_id)

        if student_id is None:
            student_id = ensure_student_profile_for_user(user_id)

        if student_id is not None:
            st.session_state["student_id"] = student_id

        return student_id

    except (TypeError, ValueError, Exception) as exc:
        st.error(f"Unable to identify your student profile: {exc}")
        return None


def load_profile_from_database():
    """
    Load the authenticated student's profile from Supabase.
    If the account has no profile yet, create the initial profile mapping.
    """
    student_id = _get_current_student_id()

    if student_id is None:
        return None

    try:
        profile = get_student_profile(student_id=student_id)

        if profile is not None:
            st.session_state["profile"] = profile
            st.session_state["student_id"] = student_id

        return profile

    except Exception as exc:
        st.error(f"Unable to load your profile: {exc}")
        return None

def clear_resume_data():

    keys_to_remove = [

        "resume_profile",

        "profile",

        "student_profile",

        "resume_text",

        "resume_file_name",

        "resume_file_size",

        # Clear previous AI assistant conversation/result
        "assistant_answer",

        "assistant_question",

        # Clear dashboard results linked to the previous resume.
        "job_match_result",

        "skill_gap_result",

        "skill_gap_role",

        "career_roadmap",

        "discovered_jobs",

        "job_search_role",

        "career_role_predictions",
        "career_selected_role",
        "career_recommendation",
        "career_skill_gap",
        "career_insights_analyzed"

    ]

    for key in keys_to_remove:

        if key in st.session_state:

            del st.session_state[key]

    # Go back to resume overview after
    # uploading a new resume.

    st.session_state[
        "student_feature"
    ] = "📄 Resume Overview"



# ==================================================
# GLOBAL CAREERIQ UI
# ==================================================

def style_resume_workspace():
    """Apply the CareerIQ light documentation-style student workspace UI."""

    st.html("""
    <style>
        :root {
            --cq-ink: #123b59;
            --cq-ink-soft: #48647a;
            --cq-muted: #71859a;
            --cq-teal: #11a8a8;
            --cq-teal-dark: #087d8a;
            --cq-pink: #e64c91;
            --cq-orange: #ff6b35;
            --cq-cream: #f5f1df;
            --cq-paper: rgba(255,255,255,.72);
            --cq-border: rgba(18,59,89,.14);
        }

        /* Remove Streamlit's top Deploy/header area completely. */
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"] {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        .stAppViewContainer > .main {
            padding-top: 0 !important;
        }

        .block-container {
            padding-top: 2.0rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1480px !important;
        }

        /* Documentation-inspired dotted background. */
        .stApp,
        .stAppViewContainer,
        .main,
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 14% 18%, rgba(17,168,168,.13), transparent 27%),
                radial-gradient(circle at 78% 32%, rgba(230,76,145,.10), transparent 29%),
                radial-gradient(circle at 54% 85%, rgba(255,183,77,.09), transparent 30%),
                radial-gradient(rgba(18,59,89,.17) 1px, transparent 1px),
                linear-gradient(135deg, #f4f1df 0%, #eef5ee 43%, #fffaf2 68%, #f8eaf0 100%) !important;
            background-size: auto, auto, auto, 24px 24px, auto !important;
            color: var(--cq-ink) !important;
            min-height: 100vh !important;
        }

        /* Soft documentation-page overlay. */
        .main .block-container {
            position: relative;
            z-index: 1;
        }

        .main .block-container::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background:
                linear-gradient(90deg, rgba(255,255,255,.18), transparent 24%, transparent 76%, rgba(255,255,255,.16));
            z-index: -1;
        }

        /* Sidebar inspired by the reference screenshot. */
        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 10% 5%, rgba(17,168,168,.10), transparent 28%),
                linear-gradient(180deg, #f1eedc 0%, #eee9d5 100%) !important;
            border-right: 1px solid rgba(18,59,89,.14) !important;
            box-shadow: 8px 0 30px rgba(18,59,89,.06) !important;
        }

        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }

        section[data-testid="stSidebar"] * {
            color: #284b64;
        }

        section[data-testid="stSidebar"] small,
        section[data-testid="stSidebar"] .stCaption {
            color: #8192a0 !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(18,59,89,.13) !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 3px !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius: 11px !important;
            padding: 8px 9px !important;
            border: 1px solid transparent !important;
            transition: all .18s ease !important;
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(17,168,168,.09) !important;
            transform: translateX(2px);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(90deg, rgba(255,107,53,.12), rgba(17,168,168,.10)) !important;
            border: 1px solid rgba(255,107,53,.30) !important;
            box-shadow: 0 5px 16px rgba(18,59,89,.05) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 1.2rem !important;
        }

        /* Sidebar buttons. */
        section[data-testid="stSidebar"] .stButton > button {
            background: rgba(255,255,255,.58) !important;
            color: #164867 !important;
            border: 1px solid rgba(18,59,89,.14) !important;
            border-radius: 11px !important;
            min-height: 42px !important;
            font-weight: 650 !important;
            box-shadow: 0 4px 12px rgba(18,59,89,.04) !important;
        }

        section[data-testid="stSidebar"] .stButton > button:hover {
            background: #fffdf6 !important;
            border-color: rgba(17,168,168,.45) !important;
            color: #087d8a !important;
        }

        /* Main buttons. */
        .stButton > button {
            border-radius: 12px !important;
            border: 1px solid rgba(18,59,89,.16) !important;
            background: rgba(255,255,255,.72) !important;
            color: #123b59 !important;
            font-weight: 700 !important;
            min-height: 44px !important;
            transition: all .18s ease !important;
            box-shadow: 0 5px 16px rgba(18,59,89,.05) !important;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(17,168,168,.55) !important;
            box-shadow: 0 9px 24px rgba(18,59,89,.09) !important;
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0ba7a7, #087d8a) !important;
            color: white !important;
            border-color: transparent !important;
        }

        /* Text inputs / selects. */
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {
            background: rgba(255,255,255,.76) !important;
            border: 1px solid rgba(18,59,89,.15) !important;
            border-radius: 12px !important;
            color: #123b59 !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.7) !important;
        }

        input, textarea {
            color: #123b59 !important;
            caret-color: #0ba7a7 !important;
        }

        /* Selectbox text + dropdown options: always readable. */
        div[data-baseweb="select"] *,
        div[data-baseweb="input"] *,
        div[data-baseweb="textarea"] * {
            color: #123b59 !important;
        }

        div[data-baseweb="popover"] {
            background: #ffffff !important;
            color: #123b59 !important;
        }

        div[role="listbox"],
        div[role="option"] {
            background: #ffffff !important;
            color: #123b59 !important;
        }

        div[role="option"]:hover {
            background: #eef8f7 !important;
            color: #087d8a !important;
        }

        label,
        .stTextInput label,
        .stTextArea label,
        .stNumberInput label,
        .stSelectbox label,
        .stFileUploader label {
            color: #234d68 !important;
            font-weight: 650 !important;
        }

        /* File uploader: prominent and clickable. */
        div[data-testid="stFileUploader"] {
            background: rgba(255,255,255,.62) !important;
            border: 1px solid rgba(18,59,89,.12) !important;
            border-radius: 20px !important;
            padding: 10px !important;
            box-shadow: 0 14px 35px rgba(18,59,89,.07) !important;
        }

        div[data-testid="stFileUploaderDropzone"] {
            background:
                linear-gradient(135deg, rgba(17,168,168,.07), rgba(230,76,145,.06)),
                rgba(255,255,255,.84) !important;
            border: 2px dashed rgba(17,168,168,.42) !important;
            border-radius: 16px !important;
            min-height: 165px !important;
        }

        div[data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, #0ba7a7, #087d8a) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
        }

        div[data-testid="stFileUploaderDropzone"] small {
            color: #6b7f90 !important;
        }

        /* Typography. */
        h1, h2, h3, h4 {
            color: #103f5d !important;
            letter-spacing: -.025em !important;
        }

        p, li, .stMarkdown, .stCaption {
            color: #48647a;
        }

        hr {
            border-color: rgba(18,59,89,.12) !important;
        }

        /* Metrics / alerts / expanders. */
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,.68) !important;
            border: 1px solid var(--cq-border) !important;
            border-radius: 16px !important;
            padding: 16px !important;
            box-shadow: 0 8px 22px rgba(18,59,89,.05) !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #71859a !important;
        }

        div[data-testid="stMetricValue"] {
            color: #103f5d !important;
        }

        div[data-testid="stExpander"] {
            background: rgba(255,255,255,.58) !important;
            border: 1px solid var(--cq-border) !important;
            border-radius: 14px !important;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px !important;
        }

        /* Dropdown popovers. */
        div[data-baseweb="popover"] {
            border-radius: 12px !important;
        }

        /* Scrollbars. */
        ::-webkit-scrollbar {
            width: 9px;
            height: 9px;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(18,59,89,.22);
            border-radius: 999px;
        }
    </style>
    """)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

def show_student_sidebar():

    st.sidebar.title(
        "🎓 CareerIQ"
    )

    st.sidebar.caption(
        "Student Career Portal"
    )

    st.sidebar.divider()

    navigation_options = [
        "📄 Resume Overview",
        "🎯 Job Matching",
        "🧠 Career Insights",
        "📊 Skill Gap Analysis",
        "🤖 AI Career Assistant",
        "🔎 Job Discovery",
        "📈 Career Dashboard",
        "🗺️ Career Roadmap"
    ]

    current_feature = st.session_state.get(
        "student_feature",
        "📄 Resume Overview"
    )

    if current_feature not in navigation_options:
        current_feature = "📄 Resume Overview"

    selected_feature = st.sidebar.radio(
        "Navigation",
        navigation_options,
        index=navigation_options.index(current_feature)
    )

    st.session_state["student_feature"] = selected_feature

    st.sidebar.divider()

    if st.sidebar.button(
        "📤 Upload New Resume",
        use_container_width=True
    ):
        # Use a dedicated upload route instead of relying only on
        # a boolean flag. This prevents the database loader from
        # restoring the old profile on the next Streamlit rerun.
        st.session_state["student_feature"] = "📤 Upload New Resume"
        st.session_state["resume_upload_mode"] = True
        st.session_state["resume_upload_generation"] = (
            st.session_state.get("resume_upload_generation", 0) + 1
        )
        clear_resume_data()
        st.session_state["student_feature"] = "📤 Upload New Resume"
        st.session_state["resume_upload_mode"] = True
        st.rerun()

    if st.sidebar.button(
        "🏠 Back to Home",
        use_container_width=True
    ):
        st.session_state["page"] = "home"
        st.rerun()



# ==================================================
# RESUME UPLOAD AND ANALYSIS
# ==================================================

def upload_and_analyze_resume():

    st.html("""
    <div style="
        padding: 28px 30px;
        border: 1px solid rgba(18,59,89,.12);
        border-radius: 22px;
        background:
            linear-gradient(135deg, rgba(17,168,168,.10), rgba(230,76,145,.08)),
            rgba(255,255,255,.72);
        box-shadow: 0 14px 38px rgba(18,59,89,.08);
        margin-bottom: 22px;
    ">
        <div style="
            color:#0f4968;
            font-size:14px;
            font-weight:700;
            letter-spacing:.08em;
            text-transform:uppercase;
            margin-bottom:8px;
        ">CareerIQ • Resume Intelligence</div>
        <div style="
            color:#103f5d;
            font-size:38px;
            font-weight:800;
            line-height:1.08;
            margin-bottom:10px;
        ">Upload your new resume</div>
        <div style="
            color:#587084;
            font-size:16px;
            line-height:1.6;
            max-width:780px;
        ">
            Choose a PDF resume and CareerIQ will extract your profile,
            analyze your skills, and refresh your career intelligence.
        </div>
    </div>
    """)

    st.title(
        "📄 Resume Analysis"
    )

    st.write(
        "Upload your resume once. CareerIQ will use "
        "your resume data across all career features."
    )

    # ==============================================
    # FILE UPLOAD
    # ==============================================

    uploaded_file = st.file_uploader(

        "Upload your Resume (PDF)",

        type=["pdf"],

        key=f"resume_uploader_{st.session_state.get('resume_upload_generation', 0)}"

    )

    if uploaded_file is None:

        st.info(
            "Please upload your resume PDF to begin."
        )

        return False

    # ==============================================
    # FILE INFORMATION
    # ==============================================

    file_size_mb = (

        uploaded_file.size

        /

        (1024 * 1024)

    )

    st.caption(

        f"📁 File: {uploaded_file.name} | "
        f"Size: {file_size_mb:.2f} MB"

    )

    current_file_name = (
        uploaded_file.name
    )

    current_file_size = (
        uploaded_file.size
    )

    # ==============================================
    # CHECK IF SAME FILE ALREADY ANALYZED
    # ==============================================

    already_analyzed = (

        "resume_profile"

        in

        st.session_state

        and

        st.session_state.get(
            "resume_file_name"
        )

        ==

        current_file_name

        and

        st.session_state.get(
            "resume_file_size"
        )

        ==

        current_file_size

    )

    # ==============================================
    # ANALYZE RESUME
    # ==============================================

    if not already_analyzed:

        try:

            # ==========================================
            # STEP 1: EXTRACT TEXT
            # ==========================================

            with st.spinner(

                "📖 Reading your resume..."

            ):

                text = extract_text_from_file(
                    uploaded_file
                )

            # ==========================================
            # CHECK EXTRACTED TEXT
            # ==========================================

            if not text or not text.strip():

                st.error(

                    "No text could be extracted "
                    "from the resume."

                )

                return False

            # ==========================================
            # SHOW EXTRACTION SUCCESS
            # ==========================================

            st.success(

                f"Resume text extracted successfully "
                f"({len(text)} characters)."

            )

            # ==========================================
            # STEP 2: AI ANALYSIS
            # ==========================================

            with st.spinner(

                "🤖 Analyzing your resume with AI..."

            ):

                profile = extract_resume_profile(
                    text
                )

            # ==========================================
            # CHECK PROFILE
            # ==========================================

            if profile is None:

                st.error(

                    "Could not analyze the resume."

                )

                return False

            # ==========================================
            # STEP 3: CREATE DATABASE PROFILE
            # ==========================================

            student_profile = create_student_profile(

                profile=profile,

                resume_text=text,

                resume_file_name=current_file_name,

                resume_file_size=current_file_size

            )

            # ==========================================
            # STEP 4: SAVE TO DATABASE
            # ==========================================

            student_id = _get_current_student_id()

            if student_id is None:
                st.error(
                    "Your student account could not be identified. "
                    "Please log out and log in again."
                )
                return False

            save_student_profile(
                student_profile,
                student_id=student_id,
                user_id=int(st.session_state["user_id"])
            )

            st.session_state["student_id"] = int(student_id)

            # ==========================================
            # STEP 5: STORE RESUME DATA IN SESSION
            # ==========================================

            st.session_state[
                "resume_profile"
            ] = profile

            # Important:
            # AI Career Assistant uses "profile".

            st.session_state[
                "profile"
            ] = profile

            st.session_state[
                "student_profile"
            ] = student_profile

            st.session_state[
                "resume_text"
            ] = text

            st.session_state[
                "resume_file_name"
            ] = current_file_name

            st.session_state[
                "resume_file_size"
            ] = current_file_size

            # ==========================================
            # SUCCESS
            # ==========================================

            st.success(

                "🎉 Resume analyzed and saved successfully!"

            )

            st.info(
                "💾 Your resume profile has been saved "
                "to the CareerIQ database."
            )

            st.session_state["resume_upload_mode"] = False
            st.session_state["student_feature"] = "📄 Resume Overview"
            st.rerun()

        except Exception as e:

            st.error(

                f"Error while analyzing resume: {str(e)}"

            )

            return False

    else:

        st.success(

            "🎉 This resume is already analyzed."

        )

    return True


# ==================================================
# RESUME OVERVIEW PAGE
# ==================================================

def show_resume_overview():

    profile = st.session_state.get(
        "resume_profile"
    )

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    st.title(
        "📄 Resume Overview"
    )

    # ==============================================
    # PERSONAL INFORMATION
    # ==============================================

    st.subheader(
        "👤 Personal Information"
    )

    name = (

        profile.name

        if profile.name

        else "Not found"

    )

    st.info(
        f"**Name:** {name}"
    )

    # ==============================================
    # EDUCATION
    # ==============================================

    st.subheader(
        "🎓 Education"
    )

    if profile.education:

        for education in profile.education:

            st.write(
                f"• {education}"
            )

    else:

        st.info(
            "No education information found."
        )

    # ==============================================
    # SKILLS
    # ==============================================

    st.subheader(
        "💻 Skills"
    )

    if profile.skills:

        columns = st.columns(3)

        for index, skill in enumerate(
            profile.skills
        ):

            with columns[
                index % 3
            ]:

                st.markdown(
                    f"🔹 {skill}"
                )

    else:

        st.info(
            "No skills found."
        )

    # ==============================================
    # PROJECTS
    # ==============================================

    st.subheader(
        "🚀 Projects"
    )

    if profile.projects:

        for index, project in enumerate(

            profile.projects,

            start=1

        ):

            with st.expander(
                f"Project {index}"
            ):

                st.write(
                    project
                )

    else:

        st.info(
            "No project information found."
        )

    # ==============================================
    # EXPERIENCE
    # ==============================================

    st.subheader(
        "💼 Experience"
    )

    if profile.experience:

        for experience in profile.experience:

            st.write(
                f"• {experience}"
            )

    else:

        st.info(
            "No experience information found."
        )

    # ==============================================
    # CERTIFICATIONS
    # ==============================================

    st.subheader(
        "📜 Certifications"
    )

    if profile.certifications:

        for certification in profile.certifications:

            st.write(
                f"• {certification}"
            )

    else:

        st.info(
            "No certifications found."
        )

    # ==============================================
    # EXTRACTED TEXT
    # ==============================================

    st.divider()

    with st.expander(
        "🔍 View Extracted Resume Text"
    ):

        st.text(

            st.session_state.get(
                "resume_text",
                ""
            )

        )


# ==================================================
# JOB MATCHING PAGE
# ==================================================

def show_job_matching():

    profile = st.session_state.get(
        "resume_profile"
    )

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    st.title(
        "🎯 Job Matching"
    )

    st.write(
        "Enter the job requirements below to compare "
        "them with your uploaded resume."
    )

    # ==============================================
    # JOB POSITION
    # ==============================================

    job_position = st.text_input(

        "Job Position",

        placeholder=(
            "Example: Machine Learning Engineer"
        )

    )

    # ==============================================
    # REQUIRED SKILLS
    # ==============================================

    required_skills = st.text_area(

        "Required Skills",

        placeholder=(
            "Enter one skill per line.\n\n"
            "Example:\n"
            "Python\n"
            "SQL\n"
            "Machine Learning\n"
            "Scikit-learn"
        ),

        height=150

    )

    # ==============================================
    # REQUIRED EDUCATION
    # ==============================================

    required_education = st.text_input(

        "Required Education",

        placeholder=(
            "Example: Bachelor's degree in "
            "Computer Science or related field"
        )

    )

    # ==============================================
    # REQUIRED EXPERIENCE
    # ==============================================

    required_years = st.number_input(

        "Required Experience (Years)",

        min_value=0.0,

        max_value=50.0,

        value=0.0,

        step=0.5

    )

    # ==============================================
    # USER EXPERIENCE
    # ==============================================

    user_years = st.number_input(

        "Your Experience (Years)",

        min_value=0.0,

        max_value=50.0,

        value=0.0,

        step=0.5

    )

    # ==============================================
    # JOB RESPONSIBILITIES
    # ==============================================

    job_responsibilities = st.text_area(

        "Job Responsibilities",

        placeholder=(
            "Enter the main responsibilities.\n\n"
            "Example:\n"
            "Build machine learning models\n"
            "Analyze datasets\n"
            "Deploy AI solutions"
        ),

        height=150

    )

    # ==============================================
    # ANALYZE BUTTON
    # ==============================================

    analyze_match = st.button(

        "🚀 Analyze Job Match",

        use_container_width=True

    )

    # ==============================================
    # CALCULATE MATCH
    # ==============================================

    if analyze_match:

        # ==========================================
        # VALIDATION
        # ==========================================

        if not job_position.strip():

            st.warning(
                "Please enter the job position."
            )

            return

        if not required_skills.strip():

            st.warning(
                "Please enter the required skills."
            )

            return

        if not required_education.strip():

            st.warning(
                "Please enter the required education."
            )

            return

        # ==========================================
        # MATCHING PROCESS
        # ==========================================

        with st.spinner(

            "🔍 Calculating job match..."

        ):

            # --------------------------------------
            # SKILL MATCH
            # --------------------------------------

            skill_score = (

                calculate_skill_match(

                    profile.skills,

                    required_skills

                )

            )

            # --------------------------------------
            # EDUCATION MATCH
            # --------------------------------------

            resume_education = " ".join(
                profile.education
            )

            education_score = (

                calculate_education_match(

                    resume_degree=resume_education,

                    resume_field=resume_education,

                    required_education=required_education

                )

            )

            # --------------------------------------
            # EXPERIENCE MATCH
            # --------------------------------------

            resume_experience = " ".join(
                profile.experience
            )

            experience_result = (

                calculate_final_experience_match(

                    resume_position=resume_experience,

                    resume_responsibilities=resume_experience,

                    job_position=job_position,

                    job_responsibilities=job_responsibilities,

                    user_years=user_years,

                    required_years=required_years

                )

            )

            experience_score = (

                experience_result[
                    "final_experience_match"
                ]

            )

            # --------------------------------------
            # OVERALL MATCH
            # --------------------------------------

            overall_score = (

                skill_score * 0.50

                +

                education_score * 0.20

                +

                experience_score * 0.30

            )

            # Save the latest job-match result for the Career Dashboard.
            st.session_state["job_match_result"] = {
                "skill_score": skill_score,
                "education_score": education_score,
                "experience_score": experience_score,
                "overall_score": overall_score,
                "job_position": job_position,
            }

        # ==========================================
        # RESULTS
        # ==========================================

        st.divider()

        st.header(
            "📊 Job Match Results"
        )

        show_job_match_dashboard(

            skill_score=skill_score,

            education_score=education_score,

            experience_score=experience_score,

            overall_score=overall_score

        )

        # ==========================================
        # EXPERIENCE DETAILS
        # ==========================================

        st.divider()

        st.subheader(
            "💼 Experience Match Details"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Position Similarity",

                f"{experience_result['position_similarity'] * 100:.2f}%"

            )

            st.metric(

                "Experience Relevance",

                f"{experience_result['experience_relevance'] * 100:.2f}%"

            )

        with col2:

            st.metric(

                "Responsibility Similarity",

                f"{experience_result['responsibility_similarity'] * 100:.2f}%"

            )

            st.metric(

                "Years Match",

                f"{experience_result['years_match'] * 100:.2f}%"

            )

        # ==========================================
        # SCORE DETAILS
        # ==========================================

        st.divider()

        st.subheader(
            "📈 Score Details"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Skills",

                f"{skill_score * 100:.2f}%"

            )

        with col2:

            st.metric(

                "Education",

                f"{education_score * 100:.2f}%"

            )

        with col3:

            st.metric(

                "Experience",

                f"{experience_score * 100:.2f}%"

            )

        with col4:

            st.metric(

                "Overall Match",

                f"{overall_score * 100:.2f}%"

            )


# ==================================================
# CAREER INSIGHTS
# ==================================================

def show_career_insights():

    st.html("""
    <style>
    .career-header {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        margin-bottom: 24px;
    }
    .career-header h1 { margin: 0; font-size: 32px; }
    .career-header p { margin: 8px 0 0; color: #d1d5db; }
    .career-card {
        padding: 18px;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        background: white;
        min-height: 150px;
    }
    .role-card {
        padding: 16px;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        background: #f9fafb;
        margin-bottom: 10px;
    }
    .role-title { font-size: 18px; font-weight: 700; }
    .role-score { font-size: 26px; font-weight: 800; }
    .skill-pill {
        display: inline-block;
        padding: 6px 10px;
        margin: 4px;
        border-radius: 999px;
        background: #eef2ff;
        font-size: 13px;
    }
    </style>
    """)

    profile = st.session_state.get("profile")
    if profile is None:
        profile = st.session_state.get("resume_profile")

    if profile is None:
        st.info("Please upload and analyze your resume first.")
        return

    profile_data = profile.model_dump() if hasattr(profile, "model_dump") else dict(profile)

    st.html("""
    <div class="career-header">
        <h1>🧠 Career Insights</h1>
        <p>Understand your career direction, role suitability, skills, and next steps.</p>
    </div>
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Skills", len(profile_data.get("skills", [])))
    with col2:
        st.metric("Projects", len(profile_data.get("projects", [])))
    with col3:
        st.metric("Education", len(profile_data.get("education", [])))
    with col4:
        st.metric("Certifications", len(profile_data.get("certifications", [])))

    st.divider()

    if st.button("🔍 Analyze My Career", type="primary", use_container_width=True):
        with st.spinner("Analyzing your career profile..."):
            predictions = predict_career_roles(profile_data)
            st.session_state["career_role_predictions"] = predictions
            if predictions:
                st.session_state["career_selected_role"] = predictions[0]["role"]
            st.session_state["career_insights_analyzed"] = True
        st.rerun()

    predictions = st.session_state.get("career_role_predictions", [])

    if not predictions:
        st.info("Click **Analyze My Career** to generate personalized career insights.")
        return

    st.subheader("🎯 Career Role Recommendations")

    for prediction in predictions[:3]:
        role = prediction["role"]
        score = float(prediction.get("score", 0.0))
        matched = prediction.get("matched_skills", [])
        missing = prediction.get("missing_skills", [])
        st.html(f"""
        <div class="role-card">
            <div class="role-title">{html.escape(role)}</div>
            <div class="role-score">{score * 100:.1f}%</div>
            <div>Role suitability based on your current profile</div>
            <div style="margin-top:8px;">
                <b>Matched:</b> {len(matched)} &nbsp; | &nbsp;
                <b>Missing:</b> {len(missing)}
            </div>
        </div>
        """)

    st.divider()

    roles = [item["role"] for item in predictions]
    default_role = st.session_state.get("career_selected_role", roles[0])
    if default_role not in roles:
        default_role = roles[0]

    selected_role = st.selectbox(
        "Choose a role for detailed insights",
        roles,
        index=roles.index(default_role),
        key="career_role_selector"
    )

    selected_prediction = next(
        item for item in predictions if item["role"] == selected_role
    )

    recommendation = generate_career_recommendation(
        profile=profile_data,
        recommended_role=selected_role,
        required_skills=ROLE_REQUIRED_SKILLS.get(selected_role, []),
        role_score=selected_prediction.get("score", 0.0)
    )

    st.session_state["career_selected_role"] = selected_role
    st.session_state["career_recommendation"] = recommendation

    st.subheader(f"📌 {selected_role}")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Role Suitability", f'{recommendation["role_score"] * 100:.1f}%')
    with c2:
        st.metric("Skill Coverage", f'{recommendation["skill_coverage"] * 100:.1f}%')
    with c3:
        st.metric("Career Readiness", f'{recommendation["career_readiness"] * 100:.1f}%')

    left, right = st.columns(2)

    with left:
        st.markdown("### ✅ Matched Skills")
        matched = recommendation["matched_skills"]
        if matched:
            pills = "".join(
                f'<span class="skill-pill">{html.escape(str(skill))}</span>'
                for skill in matched
            )
            st.html(pills)
        else:
            st.info("No matching skills found yet.")

    with right:
        st.markdown("### 📚 Missing Skills")
        missing = recommendation["missing_skills"]
        if missing:
            pills = "".join(
                f'<span class="skill-pill">{html.escape(str(skill))}</span>'
                for skill in missing
            )
            st.html(pills)
        else:
            st.success("No major required skills are missing.")

    st.divider()

    st.subheader("🚀 Improvement Plan")
    for number, item in enumerate(recommendation["improvement_plan"], start=1):
        st.write(f"**{number}.** {item}")

    st.divider()

    st.subheader("🔎 Detailed Skill Gap")
    gap_result = analyze_skill_gap(
        user_skills=profile_data.get("skills", []),
        required_skills=ROLE_REQUIRED_SKILLS.get(selected_role, []),
        target_role=selected_role
    )
    st.session_state["career_skill_gap"] = gap_result

    gc1, gc2, gc3 = st.columns(3)
    with gc1:
        st.metric("Required Skills", gap_result.get("total_required_skills", 0))
    with gc2:
        st.metric("Matched Skills", gap_result.get("total_matched_skills", 0))
    with gc3:
        st.metric("Missing Skills", gap_result.get("total_missing_skills", 0))

    if st.button("📊 Open Skill Gap Analysis", use_container_width=True):
        st.session_state["student_feature"] = "📊 Skill Gap Analysis"
        st.rerun()

    if st.button("🗺️ Open Career Roadmap", use_container_width=True):
        st.session_state["student_feature"] = "🗺️ Career Roadmap"
        st.rerun()


# ==================================================
# SKILL GAP ANALYSIS
# ==================================================

def show_skill_gap_analysis():

    profile = st.session_state.get(
        "resume_profile"
    )

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    st.title(
        "📊 Skill Gap Analysis"
    )

    st.write(
        "Compare your current skills with the skills "
        "required for your target career."
    )

    # ==============================================
    # TARGET ROLE
    # ==============================================

    role_options = list(ROLE_REQUIRED_SKILLS.keys()) + [
        "Other / Custom Role"
    ]

    target_role = st.selectbox(
        "🎯 Target Role",
        role_options,
        key="skill_gap_target_role"
    )

    # ==============================================
    # REQUIRED SKILLS
    # ==============================================

    if target_role == "Other / Custom Role":

        custom_role = st.text_input(
            "Custom Target Role",
            placeholder="Example: MLOps Engineer",
            key="skill_gap_custom_role"
        )

        required_skills = st.text_area(
            "Required Skills",
            placeholder=(
                "Enter one skill per line.\n\n"
                "Example:\n"
                "Python\n"
                "Docker\n"
                "Kubernetes\n"
                "AWS"
            ),
            height=140,
            key="skill_gap_custom_skills"
        )

        actual_role = custom_role.strip()

    else:

        actual_role = target_role
        required_skills = ROLE_REQUIRED_SKILLS[target_role]

    # ==============================================
    # SHOW REQUIRED SKILLS
    # ==============================================

    st.subheader(
        "🎯 Skills Required for This Role"
    )

    if isinstance(required_skills, list):

        skill_columns = st.columns(3)

        for index, skill in enumerate(required_skills):

            with skill_columns[index % 3]:

                st.markdown(
                    f"🔹 {skill}"
                )

    elif required_skills.strip():

        for skill in required_skills.splitlines():

            skill = skill.strip()

            if skill:

                st.markdown(
                    f"🔹 {skill}"
                )

    else:

        st.info(
            "Enter the skills required for your custom role."
        )

    # ==============================================
    # ANALYZE BUTTON
    # ==============================================

    analyze_gap = st.button(
        "🔍 Analyze Skill Gap",
        use_container_width=True,
        type="primary"
    )

    if not analyze_gap:
        return

    # ==============================================
    # VALIDATION
    # ==============================================

    if not actual_role:

        st.warning(
            "Please enter a target role."
        )

        return

    if not required_skills:

        st.warning(
            "No required skills are available for this role."
        )

        return

    try:

        with st.spinner(
            "🧠 Analyzing your skill gap..."
        ):

            result = analyze_skill_gap(
                user_skills=profile.skills,
                required_skills=required_skills,
                target_role=actual_role
            )

            # Save the latest skill-gap result for the Career Dashboard.
            st.session_state["skill_gap_result"] = result
            st.session_state["skill_gap_role"] = actual_role

        # ==========================================
        # RESULT HEADER
        # ==========================================

        st.divider()

        st.subheader(
            "📋 Skill Gap Result"
        )

        st.caption(
            f"Target Role: {actual_role}"
        )

        # ==========================================
        # SCORE
        # ==========================================

        score = float(
            result.get(
                "skill_match_score",
                0.0
            )
        )

        percentage = score * 100

        st.metric(
            "Skill Match",
            f"{percentage:.1f}%"
        )

        st.progress(
            max(
                0.0,
                min(score, 1.0)
            )
        )

        # ==========================================
        # MATCHED / MISSING SKILLS
        # ==========================================

        matched_skills = result.get(
            "matched_skills",
            []
        )

        missing_skills = result.get(
            "missing_skills",
            []
        )

        extra_skills = result.get(
            "extra_skills",
            []
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "✅ Matched Skills"
            )

            if matched_skills:

                for skill in matched_skills:

                    st.success(
                        skill,
                        icon="✅"
                    )

            else:

                st.info(
                    "No required skills matched yet."
                )

        with col2:

            st.subheader(
                "❌ Missing Skills"
            )

            if missing_skills:

                for skill in missing_skills:

                    st.error(
                        skill,
                        icon="❌"
                    )

            else:

                st.success(
                    "No required skills are missing.",
                    icon="🎉"
                )

        # ==========================================
        # EXTRA SKILLS
        # ==========================================

        st.subheader(
            "💡 Additional Skills in Your Resume"
        )

        if extra_skills:

            st.write(
                ", ".join(extra_skills)
            )

        else:

            st.info(
                "No additional skills detected."
            )

        # ==========================================
        # PRIORITIES
        # ==========================================

        prioritized = result.get(
            "prioritized_missing_skills",
            []
        )

        if prioritized:

            st.subheader(
                "🎯 Learning Priorities"
            )

            for item in prioritized:

                skill = item.get(
                    "skill",
                    "Unknown skill"
                )

                priority = item.get(
                    "priority",
                    "Low"
                )

                st.write(
                    f"**{skill}** — {priority} Priority"
                )

        # ==========================================
        # LEARNING RECOMMENDATIONS
        # ==========================================

        recommendations = result.get(
            "learning_recommendations",
            []
        )

        if recommendations:

            st.subheader(
                "📚 Learning Recommendations"
            )

            for recommendation in recommendations:

                st.write(
                    f"• {recommendation}"
                )

        # ==========================================
        # SUMMARY
        # ==========================================

        st.divider()

        total_required = result.get(
            "total_required_skills",
            len(required_skills) if isinstance(required_skills, list) else 0
        )

        total_matched = result.get(
            "total_matched_skills",
            len(matched_skills)
        )

        total_missing = result.get(
            "total_missing_skills",
            len(missing_skills)
        )

        st.subheader(
            "📊 Gap Summary"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Required Skills",
                total_required
            )

        with col2:

            st.metric(
                "Matched",
                total_matched
            )

        with col3:

            st.metric(
                "Missing",
                total_missing
            )

    except Exception as e:

        st.error(
            f"Error while analyzing skill gap: {e}"
        )

# ==================================================
# AI CAREER ASSISTANT
# ==================================================

def show_ai_career_assistant():
    """
    Display the full AI Career Assistant interface.

    The dedicated assistant UI lives in src/ui/assistant.py.
    This function connects that UI to the Student workspace.
    """

    assistant_page()


# ==================================================
# JOB DISCOVERY
# ==================================================

def _format_salary(job):

    minimum = job.get("salary_min")
    maximum = job.get("salary_max")

    if minimum and maximum:
        return f"${minimum:,} - ${maximum:,}"

    if minimum:
        return f"From ${minimum:,}"

    if maximum:
        return f"Up to ${maximum:,}"

    return "Not specified"


def _clean_job_description(description):

    if not description:
        return "No description available."

    import re

    text = re.sub(r"<[^>]+>", " ", description)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > 500:
        text = text[:500].rsplit(" ", 1)[0] + "..."

    return text


def _show_job_card(job):

    match_score = job.get("match_score", 0.0)
    match_percentage = match_score * 100

    st.markdown("---")

    col1, col2 = st.columns([4, 1])

    with col1:

        st.subheader(
            f"💼 {job.get('position', 'Unknown Role')}"
        )

        st.write(
            f"**{job.get('company', 'Unknown Company')}**"
        )

        st.caption(
            f"📍 {job.get('location') or 'Remote'}  •  "
            f"🗓️ {job.get('date') or 'Date not available'}"
        )

    with col2:

        st.metric(
            "Resume Match",
            f"{match_percentage:.0f}%"
        )

    description = _clean_job_description(
        job.get("description", "")
    )

    st.write(description)

    tags = job.get("tags") or []

    if tags:
        visible_tags = tags[:10]
        st.caption(
            "🏷️ " + " • ".join(str(tag) for tag in visible_tags)
        )

    matched_skills = job.get("matched_skills") or []

    if matched_skills:
        st.success(
            "✅ Matching resume skills: "
            + ", ".join(matched_skills[:8])
        )
    else:
        st.warning(
            "No direct resume-skill matches were detected."
        )

    st.caption(
        f"💰 {_format_salary(job)}"
    )

    url = job.get("url")

    if url:
        st.link_button(
            "🔗 View & Apply",
            url,
            use_container_width=False
        )


def show_job_discovery():

    profile = st.session_state.get(
        "resume_profile"
    )

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    st.title(
        "🔎 Job Discovery"
    )

    st.write(
        "Find current remote jobs and compare them "
        "with the skills in your resume."
    )

    st.info(
        "CareerIQ currently uses Remote OK's public remote-job feed. "
        "Each result links to the original job posting."
    )

    # ==============================================
    # SEARCH CONTROLS
    # ==============================================

    st.subheader("🔍 Search Jobs")

    col1, col2 = st.columns(2)

    with col1:

        default_role = st.session_state.get(
            "job_search_role",
            "Machine Learning Engineer"
        )

        target_role = st.text_input(
            "Target Role",
            value=default_role,
            placeholder="Example: Machine Learning Engineer"
        )

    with col2:

        location = st.text_input(
            "Location",
            placeholder="Optional: India, Pune, Europe..."
        )

    col1, col2 = st.columns(2)

    with col1:

        work_mode = st.selectbox(
            "Work Mode",
            ["All", "Remote", "Hybrid", "On-site"],
            index=0,
            help="Choose the type of workplace you prefer."
        )

    with col2:

        result_limit = st.selectbox(
            "Number of Results",
            [5, 10, 15, 20],
            index=1
        )

    st.caption(
        "Your resume skills are automatically used to calculate "
        "the match percentage."
    )

    search_clicked = st.button(
        "🚀 Find Matching Jobs",
        use_container_width=True,
        type="primary"
    )

    if search_clicked:

        if not target_role.strip():
            st.warning("Please enter a target role.")
            return

        st.session_state["job_search_role"] = target_role.strip()

        try:

            with st.spinner(
                "🔎 Fetching current jobs and calculating matches..."
            ):

                jobs = fetch_remote_jobs(
                    keyword=target_role,
                    location=location,
                    work_mode=(
                        ""
                        if work_mode == "All"
                        else work_mode
                    ),
                    resume_skills=profile.skills,
                    limit=result_limit
                )

            st.session_state["discovered_jobs"] = jobs

        except Exception as error:

            st.error(
                "Could not fetch jobs right now. "
                "Please try again in a moment."
            )

            st.exception(error)
            return

    jobs = st.session_state.get(
        "discovered_jobs",
        []
    )

    if not jobs:

        st.info(
            "Enter a target role and click **Find Matching Jobs** "
            "to discover current openings."
        )

        return

    # ==============================================
    # RESULTS SUMMARY
    # ==============================================

    st.divider()

    st.subheader(
        f"💼 {len(jobs)} Jobs Found"
    )

    best_match = jobs[0].get("match_score", 0.0) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jobs Found",
            len(jobs)
        )

    with col2:
        st.metric(
            "Top Resume Match",
            f"{best_match:.0f}%"
        )

    with col3:
        st.metric(
            "Resume Skills",
            len(profile.skills)
        )

    # ==============================================
    # JOB RESULTS
    # ==============================================

    for job in jobs:
        _show_job_card(job)

# ==================================================
# CAREER DASHBOARD
# ==================================================

def show_career_dashboard():

    profile = st.session_state.get(
        "resume_profile"
    )

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        return

    st.title(
        "📈 Career Dashboard"
    )

    st.write(
        "View your career profile, skills, job matches, "
        "skill gaps, and career progress in one place."
    )

    # ==================================================
    # PROFILE SUMMARY
    # ==================================================

    st.subheader(
        "👤 Profile Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Skills",
            len(profile.skills)
        )

    with col2:
        st.metric(
            "Projects",
            len(profile.projects)
        )

    with col3:
        st.metric(
            "Experience",
            len(profile.experience)
        )

    with col4:
        st.metric(
            "Certifications",
            len(profile.certifications)
        )

    # ==================================================
    # PROFILE DETAILS
    # ==================================================

    st.divider()

    st.subheader(
        "👤 Profile Details"
    )

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.write(
            f"**Name:** {profile.name or 'Not found'}"
        )

        if profile.education:
            st.write(
                "**Education:** "
                + ", ".join(profile.education)
            )
        else:
            st.write(
                "**Education:** Not found"
            )

    with profile_col2:

        st.write(
            f"**Projects:** {len(profile.projects)}"
        )

        st.write(
            f"**Experience Entries:** {len(profile.experience)}"
        )

        st.write(
            f"**Certifications:** {len(profile.certifications)}"
        )

    # ==================================================
    # SKILLS
    # ==================================================

    st.divider()

    st.subheader(
        "💻 Skills"
    )

    if profile.skills:

        skill_columns = st.columns(3)

        for index, skill in enumerate(profile.skills):

            with skill_columns[index % 3]:

                st.markdown(
                    f"🔹 {skill}"
                )

    else:

        st.info(
            "No skills available."
        )

    # ==================================================
    # JOB MATCH SUMMARY
    # ==================================================

    st.divider()

    st.subheader(
        "🎯 Latest Job Match"
    )

    job_match = st.session_state.get(
        "job_match_result"
    )

    if job_match:

        job_title = job_match.get(
            "job_position",
            "Job"
        )

        st.caption(
            f"Latest analyzed position: **{job_title}**"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Skills",
                f"{job_match.get('skill_score', 0) * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Education",
                f"{job_match.get('education_score', 0) * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Experience",
                f"{job_match.get('experience_score', 0) * 100:.1f}%"
            )

        with col4:
            st.metric(
                "Overall Match",
                f"{job_match.get('overall_score', 0) * 100:.1f}%"
            )

    else:

        st.info(
            "No job match has been analyzed yet. "
            "Go to **🎯 Job Matching** to analyze a job."
        )

    # ==================================================
    # SKILL GAP SUMMARY
    # ==================================================

    st.divider()

    st.subheader(
        "📊 Skill Gap"
    )

    skill_gap = st.session_state.get(
        "skill_gap_result"
    )

    if skill_gap:

        gap_role = st.session_state.get(
            "skill_gap_role",
            "Selected Role"
        )

        skill_score = float(
            skill_gap.get(
                "skill_match_score",
                0.0
            )
        )

        matched_skills = skill_gap.get(
            "matched_skills",
            []
        )

        missing_skills = skill_gap.get(
            "missing_skills",
            []
        )

        st.caption(
            f"Target role: **{gap_role}**"
        )

        st.metric(
            "Skill Match",
            f"{skill_score * 100:.1f}%"
        )

        st.progress(
            max(
                0.0,
                min(skill_score, 1.0)
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### ✅ Matched"
            )

            if matched_skills:

                st.write(
                    ", ".join(matched_skills)
                )

            else:

                st.info(
                    "No matched skills yet."
                )

        with col2:

            st.markdown(
                "### 📚 Missing"
            )

            if missing_skills:

                st.write(
                    ", ".join(missing_skills)
                )

            else:

                st.success(
                    "No missing skills!"
                )

    else:

        st.info(
            "No skill-gap analysis has been completed yet. "
            "Go to **📊 Skill Gap Analysis** to analyze your skills."
        )

    # ==================================================
    # CAREER ROADMAP SUMMARY
    # ==================================================

    st.divider()

    st.subheader(
        "🗺️ Career Roadmap"
    )

    roadmap = st.session_state.get(
        "career_roadmap"
    )

    if roadmap:

        roadmap_role = roadmap.get(
            "target_role",
            "Selected Role"
        )

        roadmap_progress = float(
            roadmap.get(
                "overall_completion",
                0.0
            )
        )

        st.caption(
            f"Target role: **{roadmap_role}**"
        )

        st.metric(
            "Roadmap Progress",
            f"{roadmap_progress:.1f}%"
        )

        st.progress(
            max(
                0.0,
                min(roadmap_progress / 100, 1.0)
            )
        )

        phases = roadmap.get(
            "phases",
            []
        )

        if phases:

            phase_columns = st.columns(
                min(len(phases), 3)
            )

            for index, phase in enumerate(phases):

                with phase_columns[
                    index % len(phase_columns)
                ]:

                    st.markdown(
                        f"**Phase {phase.get('phase', index + 1)}**"
                    )

                    st.write(
                        phase.get(
                            "title",
                            "Career Phase"
                        )
                    )

                    st.caption(
                        f"{phase.get('completion_percentage', 0):.0f}% complete"
                    )

    else:

        st.info(
            "No career roadmap has been generated yet. "
            "Go to **🗺️ Career Roadmap** to create one."
        )

    # ==================================================
    # JOB DISCOVERY SUMMARY
    # ==================================================

    st.divider()

    st.subheader(
        "🔎 Job Discovery"
    )

    discovered_jobs = st.session_state.get(
        "discovered_jobs",
        []
    )

    if discovered_jobs:

        best_match = max(
            (
                float(job.get("match_score", 0.0))
                for job in discovered_jobs
            ),
            default=0.0
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Jobs Found",
                len(discovered_jobs)
            )

        with col2:
            st.metric(
                "Best Job Match",
                f"{best_match * 100:.0f}%"
            )

        with col3:
            st.metric(
                "Resume Skills",
                len(profile.skills)
            )

        st.write(
            "Latest discovered jobs:"
        )

        for job in discovered_jobs[:5]:

            position = job.get(
                "position",
                "Unknown Role"
            )

            company = job.get(
                "company",
                "Unknown Company"
            )

            match = float(
                job.get(
                    "match_score",
                    0.0
                )
            ) * 100

            st.write(
                f"💼 **{position}** — "
                f"{company} — "
                f"**{match:.0f}% match**"
            )

    else:

        st.info(
            "No jobs discovered yet. "
            "Go to **🔎 Job Discovery** to find current openings."
        )

    # ==================================================
    # CAREER OVERVIEW
    # ==================================================

    st.divider()

    st.subheader(
        "🚀 Career Overview"
    )

    overview_col1, overview_col2 = st.columns(2)

    with overview_col1:

        st.markdown(
            "### 📌 Current Profile"
        )

        st.write(
            f"• **{len(profile.skills)}** skills"
        )

        st.write(
            f"• **{len(profile.projects)}** projects"
        )

        st.write(
            f"• **{len(profile.experience)}** experience entries"
        )

        st.write(
            f"• **{len(profile.certifications)}** certifications"
        )

    with overview_col2:

        st.markdown(
            "### 🎯 Next Steps"
        )

        if skill_gap:

            missing_count = len(
                skill_gap.get(
                    "missing_skills",
                    []
                )
            )

            st.write(
                f"📚 Learn **{missing_count}** missing skills"
            )

        if roadmap:

            st.write(
                "🗺️ Continue your career roadmap"
            )

        if not job_match:

            st.write(
                "🎯 Analyze a target job"
            )

        if not discovered_jobs:

            st.write(
                "🔎 Discover current job openings"
            )

    st.success(
        "💡 Keep improving your skills, projects, "
        "and job-match score as you progress."
    )


# ==================================================
# CAREER ROADMAP
# ==================================================

def show_career_roadmap():
    st.header("🗺️ Career Roadmap")

    profile = st.session_state.get("resume_profile")

    if not profile:
        st.warning(
            "Please upload and analyze your resume first."
        )
        return

    st.write(
        "Build a personalized roadmap based on your "
        "current skills and target career."
    )

    target_role = st.selectbox(
        "🎯 Select Target Role",
        [
            "Machine Learning Engineer",
            "AI Engineer",
            "Data Scientist",
            "Backend Developer",
        ],
    )

    if st.button("🗺️ Generate My Roadmap", type="primary"):
        try:
            result = personalize_roadmap(
                target_role=target_role,
                user_skills=profile.skills,
            )

            st.session_state["career_roadmap"] = result

        except Exception as e:
            st.error(f"Could not generate roadmap: {e}")
            return

    roadmap = st.session_state.get("career_roadmap")

    if not roadmap:
        return

    st.divider()

    st.subheader(
        f"🎯 {roadmap['target_role']}"
    )

    st.write(roadmap["description"])

    st.metric(
        "Overall Roadmap Progress",
        f"{roadmap['overall_completion']:.1f}%",
    )

    st.progress(
        roadmap["overall_completion"] / 100
    )

    st.divider()

    for phase in roadmap["phases"]:

        st.subheader(
            f"Phase {phase['phase']}: {phase['title']}"
        )

        st.caption(
            f"⏱️ Estimated duration: {phase['duration']}"
        )

        completion = phase["completion_percentage"]

        st.write(
            f"Progress: **{completion:.1f}%**"
        )

        st.progress(completion / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Already Have")

            if phase["completed_skills"]:
                for skill in phase["completed_skills"]:
                    st.write(f"✅ {skill}")
            else:
                st.write("No matching skills yet.")

        with col2:
            st.markdown("### 📚 Need to Learn")

            if phase["missing_skills"]:
                for skill in phase["missing_skills"]:
                    st.write(f"📚 {skill}")
            else:
                st.write("🎉 All skills completed!")

        st.markdown("### 🚀 Recommended Projects")

        for project in phase["projects"]:
            st.write(f"🔹 {project}")

        st.divider()


# ==================================================
# MAIN RESUME PAGE
# ==================================================

def resume_page():

    # ==============================================
    # GLOBAL CAREERIQ STYLING
    # ==============================================

    style_resume_workspace()

    # ==============================================
    # SHOW SIDEBAR
    # ==============================================

    show_student_sidebar()

    # ==============================================
    # EXPLICIT NEW-RESUME UPLOAD MODE
    # ==============================================

    if (
        st.session_state.get("resume_upload_mode", False)
        or st.session_state.get("student_feature") == "📤 Upload New Resume"
    ):
        upload_and_analyze_resume()
        return

    # ==============================================
    # LOAD PROFILE FROM DATABASE
    # ==============================================

    if "resume_profile" not in st.session_state:

        stored_profile = load_profile_from_database()

        if stored_profile is None:

            upload_and_analyze_resume()

            return

    # ==============================================
    # GET SELECTED FEATURE
    # ==============================================

    selected_feature = (

        st.session_state.get(

            "student_feature",

            "📄 Resume Overview"

        )

    )

    # ==============================================
    # RESUME OVERVIEW
    # ==============================================

    if selected_feature == (
        "📄 Resume Overview"
    ):

        show_resume_overview()

    # ==============================================
    # JOB MATCHING
    # ==============================================

    elif selected_feature == (
        "🎯 Job Matching"
    ):

        show_job_matching()

    # ==============================================
    # CAREER INSIGHTS
    # ==============================================

    elif selected_feature == (
        "🧠 Career Insights"
    ):

        show_career_insights()

    # ==============================================
    # SKILL GAP ANALYSIS
    # ==============================================

    elif selected_feature == (
        "📊 Skill Gap Analysis"
    ):

        show_skill_gap_analysis()

    # ==============================================
    # AI CAREER ASSISTANT
    # ==============================================

    elif selected_feature == (
        "🤖 AI Career Assistant"
    ):

        show_ai_career_assistant()

    # ==============================================
    # JOB DISCOVERY
    # ==============================================

    elif selected_feature == (
        "🔎 Job Discovery"
    ):

        show_job_discovery()

    # ==============================================
    # CAREER DASHBOARD
    # ==============================================

    elif selected_feature == (
        "📈 Career Dashboard"
    ):

        show_career_dashboard()

    # ==============================================
    # CAREER ROADMAP
    # ==============================================

    elif selected_feature == (
        "🗺️ Career Roadmap"
    ):

        show_career_roadmap()