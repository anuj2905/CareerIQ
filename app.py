import streamlit as st

from dotenv import load_dotenv

from src.ui.home import (
    home_page,
    style_home_page,
    student_page,
    student_feature_page,
)

from src.ui.job_management import (
    job_management,
)

from src.ui.job_applications import (
    job_applications,
)

from src.ui.job_details import (
    job_details,
)

from src.ui.jobs import (
    jobs_page,
)

from src.ui.resume import (
    resume_page,
)

from src.ui.assistant import (
    assistant_page,
)

from src.ui.auth import (
    auth_page,
)

from src.ui.company_selector import (
    company_selector,
)

from src.ui.company_profile import (
    company_profile_page,
)

from src.ui.company_dashboard import (
    company_dashboard,
)

from src.ui.create_job import (
    create_job,
)


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
)


# ============================================================
# GLOBAL STYLE
# ============================================================

style_home_page()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state["page"] = "home"


if "logged_in" not in st.session_state:

    st.session_state["logged_in"] = False


if "user_id" not in st.session_state:

    st.session_state["user_id"] = None


if "user_email" not in st.session_state:

    st.session_state["user_email"] = None


if "user_role" not in st.session_state:

    st.session_state["user_role"] = None


if "profile" not in st.session_state:

    st.session_state["profile"] = None


if "student_feature" not in st.session_state:

    st.session_state[
        "student_feature"
    ] = "📄 Resume Overview"


if "company_id" not in st.session_state:

    st.session_state["company_id"] = None


if "company_profile" not in st.session_state:

    st.session_state["company_profile"] = None


if "company_saved" not in st.session_state:

    st.session_state["company_saved"] = False


if "last_created_job_id" not in st.session_state:

    st.session_state["last_created_job_id"] = None


if "student_id" not in st.session_state:

    st.session_state["student_id"] = 1


if "discovered_jobs" not in st.session_state:

    st.session_state["discovered_jobs"] = []


if "job_search_role" not in st.session_state:

    st.session_state["job_search_role"] = ""


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state["page"]


# ============================================================
# HOME
# ============================================================

if page == "home":

    home_page()


# ============================================================
# AUTHENTICATION
# ============================================================

elif page == "student_auth":

    auth_page("student")


elif page == "company_auth":

    auth_page("company")


# ============================================================
# COMPANY / APPLICATION PAGES
# ============================================================

elif page == "job_applications":

    job_applications()


elif page == "job_management":

    job_management()


elif page == "job_details":

    job_details()


# ============================================================
# STUDENT
# ============================================================

elif page == "student":

    student_page()


elif page == "resume":

    resume_page()


elif page == "assistant":

    assistant_page()


elif page == "jobs":

    jobs_page()


elif page == "student_feature":

    student_feature_page()


# ============================================================
# COMPANY
# ============================================================

elif page == "company_selector":

    company_selector()


elif page == "company_profile":

    company_profile_page()


elif page == "company_dashboard":

    company_dashboard()


elif page == "create_job":

    create_job()


# ============================================================
# SAFETY FALLBACK
# ============================================================

else:

    st.session_state["page"] = "home"
