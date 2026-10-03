import streamlit as st
from dotenv import load_dotenv

from src.ui.home import (
    home_page,
    style_home_page,
    student_page,
    student_feature_page,
)

from src.ui.job_management import job_management
from src.ui.job_applications import job_applications
from src.ui.job_details import job_details
from src.ui.jobs import jobs_page
from src.ui.resume import resume_page
from src.ui.assistant import assistant_page
from src.ui.auth import auth_page
from src.ui.company_selector import company_selector
from src.ui.company_profile import company_profile_page
from src.ui.company_dashboard import company_dashboard
from src.ui.create_job import create_job
from src.ui.salary_prediction import salary_prediction_page

from src.ui.student_sidebar import show_student_sidebar


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CareerIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

style_home_page()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

DEFAULT_SESSION_STATE = {
    "page": "home",
    "logged_in": False,
    "user_id": None,
    "user_email": None,
    "user_role": None,
    "profile": None,
    "student_feature": "📄 Resume Overview",
    "company_id": None,
    "company_profile": None,
    "company_saved": False,
    "last_created_job_id": None,
    "student_id": None,
    "discovered_jobs": [],
    "job_search_role": "",
    "resume_upload_mode": False,
    "resume_upload_generation": 0,
}


for key, default_value in DEFAULT_SESSION_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = default_value


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.get(
    "page",
    "home",
)


# ============================================================
# CURRENT USER ROLE
# ============================================================

user_role = str(
    st.session_state.get(
        "user_role",
        "",
    )
    or ""
).strip().lower()


logged_in = bool(
    st.session_state.get(
        "logged_in",
        False,
    )
)


# ============================================================
# STUDENT SIDEBAR
# ============================================================
#
# IMPORTANT:
# The sidebar is rendered ONLY here.
#
# resume.py
# jobs.py
# salary_prediction.py
# assistant.py
# student_feature.py
#
# DO NOT create another sidebar inside those files.
#
# ============================================================

student_pages = {
    "student",
    "resume",
    "assistant",
    "jobs",
    "salary_prediction",
    "student_feature",
    "job_details",
    "job_applications",
}


should_show_student_sidebar = (
    logged_in
    and user_role == "student"
    and page in student_pages
)


if should_show_student_sidebar:

    show_student_sidebar()


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "home":

    home_page()


# ------------------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------------------

elif page == "student_auth":

    auth_page("student")


elif page == "company_auth":

    auth_page("company")


# ------------------------------------------------------------
# STUDENT PAGES
# ------------------------------------------------------------

elif page == "student":

    student_page()


elif page == "resume":

    resume_page()


elif page == "assistant":

    assistant_page()


elif page == "jobs":

    jobs_page()


elif page == "salary_prediction":

    salary_prediction_page()


elif page == "student_feature":

    student_feature_page()


elif page == "job_details":

    job_details()


elif page == "job_applications":

    job_applications()


# ------------------------------------------------------------
# COMPANY PAGES
# ------------------------------------------------------------

elif page == "company_selector":

    company_selector()


elif page == "company_profile":

    company_profile_page()


elif page == "company_dashboard":

    company_dashboard()


elif page == "create_job":

    create_job()


elif page == "job_management":

    job_management()


# ============================================================
# UNKNOWN PAGE
# ============================================================

else:

    st.session_state["page"] = "home"

    st.rerun()