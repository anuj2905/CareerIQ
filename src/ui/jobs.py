
import re
from typing import Any, Dict, List
import html

import streamlit as st

from src.database.repositories import (
    get_all_active_jobs,
    get_company,
    create_job_application,
)
from src.database.models import JobApplication

from src.job_discovery.job_fetcher import (
    fetch_remote_jobs,
    calculate_job_match,
)


# ============================================================
# PAGE STYLE
# ============================================================

def _inject_job_discovery_style():
    st.html("""
    <style>
    :root {
        --cq-bg:#f7f6ef; --cq-ink:#073b5c; --cq-muted:#627586;
        --cq-border:rgba(7,59,92,.13); --cq-cyan:#11a9b5;
        --cq-purple:#8b5cf6; --cq-coral:#ff5a36;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 15%, rgba(17,169,181,.10), transparent 24%),
            radial-gradient(circle at 90% 20%, rgba(139,92,246,.08), transparent 25%),
            linear-gradient(180deg,#faf9f2 0%,#f7f6ef 100%);
        color:var(--cq-ink);
    }

    [data-testid="stHeader"] { background:rgba(250,249,242,.78); }
    .block-container {
        max-width:1420px;
        padding-top:2.1rem;
        padding-bottom:4rem;
        background-image:radial-gradient(rgba(7,59,92,.13) .7px,transparent .7px);
        background-size:26px 26px;
    }

    section[data-testid="stSidebar"] {
        background:linear-gradient(180deg,#eeebda 0%,#e8e6d8 100%);
        border-right:1px solid rgba(7,59,92,.12);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color:#35556c; font-weight:650;
    }
    section[data-testid="stSidebar"] .stButton button {
        border-radius:12px;
        border:1px solid rgba(7,59,92,.14);
        background:rgba(255,255,255,.58);
        color:#0a4566; font-weight:700;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background:rgba(255,255,255,.96) !important;
        border-color:rgba(7,59,92,.15) !important;
        border-radius:12px !important;
        color:#073b5c !important;
    }
    div[data-baseweb="input"] input,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] [role="combobox"],
    div[data-baseweb="select"] [data-baseweb="select-value"],
    div[data-baseweb="select"] span {
        color:#073b5c !important;
        -webkit-text-fill-color:#073b5c !important;
    }
    div[data-baseweb="select"] svg {
        fill:#073b5c !important;
    }
    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background:#ffffff !important;
        color:#073b5c !important;
    }
    [data-baseweb="menu"] [role="option"] {
        color:#073b5c !important;
        background:#ffffff !important;
    }
    [data-baseweb="menu"] [role="option"]:hover {
        background:#eef8fa !important;
        color:#073b5c !important;
    }
    label { color:#36546a !important; font-weight:700 !important; }
    .stButton > button { border-radius:12px; font-weight:750; }

    .cq-hero {
        padding:34px 38px 36px;
        border:1px solid var(--cq-border);
        border-radius:24px;
        background:
            radial-gradient(circle at 88% 12%,rgba(17,169,181,.16),transparent 24%),
            radial-gradient(circle at 72% 100%,rgba(139,92,246,.10),transparent 28%),
            rgba(255,255,255,.72);
        box-shadow:0 18px 55px rgba(7,59,92,.08);
        margin-bottom:18px;
    }
    .cq-kicker {
        color:var(--cq-coral); font-size:12px; font-weight:850;
        letter-spacing:1.2px; text-transform:uppercase; margin-bottom:10px;
    }
    .cq-title {
        color:var(--cq-ink); font-size:clamp(38px,5vw,62px);
        line-height:1.02; font-weight:850; letter-spacing:-1.8px; margin:0;
    }
    .cq-gradient-line {
        height:3px; width:100%; margin:18px 0;
        border-radius:999px;
        background:linear-gradient(90deg,#11a9b5,#8b5cf6,#ff5a36);
    }
    .cq-subtitle {
        max-width:850px; color:#536a7c; font-size:15px; line-height:1.75;
    }
    .cq-source {
        padding:14px 18px; border-radius:14px;
        background:rgba(255,255,255,.75);
        border:1px solid var(--cq-border); color:#506779;
        line-height:1.65; margin-bottom:22px;
    }
    .cq-search {
        padding:22px 24px 8px; border-radius:20px;
        background:rgba(255,255,255,.8);
        border:1px solid var(--cq-border);
        box-shadow:0 10px 35px rgba(7,59,92,.055);
        margin-bottom:22px;
    }
    .cq-section {
        color:var(--cq-ink); font-size:24px; font-weight:820;
        letter-spacing:-.4px; margin:18px 0 12px;
    }

    .cq-job {
        padding:24px 26px 20px; margin-bottom:0;
        border-radius:20px; background:rgba(255,255,255,.9);
        border:1px solid var(--cq-border);
        box-shadow:0 10px 30px rgba(7,59,92,.055);
    }
    .cq-job.internal {
        border-color:rgba(17,169,181,.28);
        background:linear-gradient(135deg,rgba(236,253,250,.84),rgba(255,255,255,.94) 55%);
    }
    .cq-badge {
        display:inline-block; padding:5px 9px; border-radius:999px;
        font-size:10px; font-weight:850; letter-spacing:.45px;
        color:#12657b; background:rgba(17,169,181,.10);
        border:1px solid rgba(17,169,181,.20); margin-bottom:9px;
    }
    .cq-job-title {
        color:var(--cq-ink); font-size:22px; line-height:1.2;
        font-weight:820; margin-bottom:6px;
    }
    .cq-company { color:#49657a; font-size:14px; font-weight:650; margin-bottom:12px; }
    .cq-meta { color:#687b8b; font-size:13px; line-height:1.7; margin-bottom:12px; }
    .cq-description { color:#607485; font-size:13px; line-height:1.7; margin-bottom:10px; }

    .cq-pill {
        display:inline-block; padding:5px 10px; margin:3px 4px 3px 0;
        border-radius:999px; background:#f0f7f8; color:#225d73;
        border:1px solid rgba(17,169,181,.16); font-size:11px; font-weight:650;
    }
    .cq-match {
        padding:15px 10px; border-radius:16px; text-align:center;
        background:linear-gradient(145deg,rgba(17,169,181,.10),rgba(139,92,246,.08));
        border:1px solid rgba(17,169,181,.18);
    }
    .cq-match-number { font-size:29px; line-height:1; font-weight:880; color:#087e91; }
    .cq-match-label {
        margin-top:5px; font-size:10px; color:#607a89;
        font-weight:750; text-transform:uppercase; letter-spacing:.55px;
    }
    .cq-empty {
        padding:42px 28px; border-radius:20px; text-align:center;
        background:rgba(255,255,255,.72);
        border:1px dashed rgba(7,59,92,.20);
    }
    .cq-cq-empty-icon { font-size:38px; margin-bottom:8px; }
    .cq-cq-empty-title { color:var(--cq-ink); font-size:20px; font-weight:800; }
    .cq-cq-empty-text { color:#687b8b; font-size:13px; line-height:1.65; margin-top:8px; }
    [data-testid="stMetric"] {
        background:rgba(255,255,255,.75);
        border:1px solid rgba(7,59,92,.10);
        border-radius:14px; padding:12px 14px;
    }
    [data-testid="stMetricValue"] { color:var(--cq-ink) !important; }
    </style>
    """)


# ============================================================
# HELPERS
# ============================================================

def _normalize(value: Any) -> str:
    return " ".join(
        str(value or "").lower().strip().split()
    )


def _safe_text(value: Any) -> str:
    return html.escape(str(value or ""))


def _get_student_id() -> int:
    value = st.session_state.get("student_id")

    try:
        return int(value) if value is not None else 1
    except (TypeError, ValueError):
        return 1


def _get_resume_skills() -> List[str]:
    profile = st.session_state.get("resume_profile")

    if profile is None:
        profile = st.session_state.get("profile")

    if profile is None:
        return []

    skills = getattr(profile, "skills", []) or []

    return [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]


# ============================================================
# ROLE MATCHING
# ============================================================

ROLE_ALIASES = {
    "ml": {
        "ml",
        "machine learning",
        "machine learning engineer",
        "ml engineer",
    },
    "ai": {
        "ai",
        "artificial intelligence",
        "ai engineer",
        "artificial intelligence engineer",
    },
    "data scientist": {
        "data scientist",
        "data science",
        "data scientist intern",
    },
    "data analyst": {
        "data analyst",
        "data analytics",
        "data analysis",
    },
    "backend": {
        "backend",
        "backend developer",
        "backend engineer",
        "software engineer backend",
    },
    "frontend": {
        "frontend",
        "frontend developer",
        "frontend engineer",
    },
    "full stack": {
        "full stack",
        "fullstack",
        "full stack developer",
        "full stack engineer",
    },
    "python": {
        "python",
        "python developer",
        "python engineer",
    },
}


def _role_tokens(value: str) -> set:
    normalized = _normalize(value)

    if not normalized:
        return set()

    tokens = set(normalized.split())

    for canonical, aliases in ROLE_ALIASES.items():

        if normalized == canonical:
            tokens.update(
                " ".join(alias.split())
                for alias in aliases
            )

        if normalized in aliases:
            tokens.update(
                " ".join(alias.split())
                for alias in aliases
            )

    return tokens


def _role_matches(
    job: Dict[str, Any],
    target_role: str,
) -> bool:

    target_role = _normalize(target_role)

    if not target_role:
        return True

    searchable_text = _normalize(
        " ".join(
            [
                str(job.get("title", "")),
                str(job.get("position", "")),
                str(job.get("description", "")),
                str(job.get("company", "")),
                " ".join(
                    str(skill)
                    for skill in job.get("skills", [])
                ),
            ]
        )
    )

    # Exact phrase match.
    if target_role in searchable_text:
        return True

    # Alias-aware matching.
    for alias_group in ROLE_ALIASES.values():

        if target_role in alias_group:

            if any(
                alias in searchable_text
                for alias in alias_group
            ):
                return True

    # Token overlap.
    target_tokens = set(target_role.split())

    if not target_tokens:
        return True

    job_tokens = set(searchable_text.split())

    overlap = target_tokens.intersection(job_tokens)

    return len(overlap) >= max(
        1,
        len(target_tokens) // 2
    )


# ============================================================
# FILTERING
# ============================================================

def _work_mode_matches(
    job: Dict[str, Any],
    work_mode: str,
) -> bool:

    work_mode = _normalize(work_mode)

    if not work_mode or work_mode == "all":
        return True

    searchable_text = _normalize(
        " ".join(
            [
                str(job.get("location", "")),
                str(job.get("description", "")),
                str(job.get("employment_type", "")),
                str(job.get("work_mode", "")),
            ]
        )
    )

    if work_mode == "remote":
        return "remote" in searchable_text

    if work_mode == "hybrid":
        return "hybrid" in searchable_text

    if work_mode == "on-site":
        onsite_terms = {
            "onsite",
            "on-site",
            "office",
            "pune",
            "mumbai",
            "bangalore",
            "bengaluru",
            "delhi",
            "hyderabad",
        }

        return any(
            term in searchable_text
            for term in onsite_terms
        )

    return True


def _job_matches_filters(
    job: Dict[str, Any],
    target_role: str,
    location: str,
    work_mode: str,
) -> bool:

    if not _role_matches(
        job,
        target_role,
    ):
        return False

    location = _normalize(location)

    if location:

        job_location = _normalize(
            job.get("location", "")
        )

        company_location = _normalize(
            job.get("company_location", "")
        )

        combined_location = (
            f"{job_location} {company_location}"
        )

        if location not in combined_location:
            return False

    if not _work_mode_matches(
        job,
        work_mode,
    ):
        return False

    return True


# ============================================================
# INTERNAL CAREERIQ JOBS
# ============================================================

def _convert_internal_job(
    job,
    company,
) -> Dict[str, Any]:

    company_name = (
        company.company_name
        if company
        else "CareerIQ Company"
    )

    company_location = (
        company.location
        if company
        else ""
    )

    return {
        "source": "CareerIQ",
        "internal": True,
        "id": job.id,
        "job_id": job.id,
        "position": job.title,
        "title": job.title,
        "company": company_name,
        "company_id": job.company_id,
        "company_location": company_location,
        "location": job.location,
        "description": job.description,
        "employment_type": job.employment_type,
        "experience_required": job.experience_required,
        "education_required": job.education_required,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "status": job.status,
        "skills": list(job.skills or []),
        "tags": list(job.skills or []),
        "job_skills": list(job.skills or []),
        "url": "",
        "date": "",
        "match_score": 0.0,
        "matched_skills": [],
        "missing_skills": [],
    }


def _calculate_internal_match(
    job: Dict[str, Any],
    resume_skills: List[str],
) -> Dict[str, Any]:

    job_for_match = {
        "position": job.get("position", ""),
        "description": job.get("description", ""),
        "tags": job.get("skills", []),
    }

    return calculate_job_match(
        job_for_match,
        resume_skills,
    )


def _load_internal_jobs(
    target_role: str,
    location: str,
    work_mode: str,
    resume_skills: List[str],
) -> List[Dict[str, Any]]:

    jobs = get_all_active_jobs()

    results = []

    for job in jobs:

        company = get_company(
            job.company_id
        )

        item = _convert_internal_job(
            job,
            company,
        )

        if not _job_matches_filters(
            item,
            target_role,
            location,
            work_mode,
        ):
            continue

        match = _calculate_internal_match(
            item,
            resume_skills,
        )

        item.update(match)

        results.append(item)

    results.sort(
        key=lambda item: float(
            item.get("match_score", 0.0)
            or 0.0
        ),
        reverse=True,
    )

    return results


# ============================================================
# EXTERNAL JOBS
# ============================================================

def _load_external_jobs(
    target_role: str,
    location: str,
    work_mode: str,
    resume_skills: List[str],
    limit: int,
) -> List[Dict[str, Any]]:

    if not target_role.strip():
        return []

    if work_mode == "On-site":
        return []

    return fetch_remote_jobs(
        keyword=target_role,
        location=location,
        work_mode=work_mode,
        resume_skills=resume_skills,
        limit=limit,
    )


# ============================================================
# APPLICATION HELPERS
# ============================================================

def _get_student_applications():
    student_id = _get_student_id()

    from src.database.database import get_connection

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                job_id,
                student_id,
                match_score,
                application_status
            FROM job_applications
            WHERE student_id = ?
            """,
            (student_id,),
        )

        rows = cursor.fetchall()

        return [
            JobApplication(
                id=row["id"],
                job_id=row["job_id"],
                student_id=row["student_id"],
                match_score=row["match_score"],
                application_status=(
                    row["application_status"]
                    or "applied"
                ),
            )
            for row in rows
        ]

    finally:
        connection.close()


def _already_applied(job_id: int) -> bool:

    try:

        applications = _get_student_applications()

        return any(
            application.job_id == job_id
            for application in applications
        )

    except Exception:

        return False


# ============================================================
# SKILLS
# ============================================================

def _render_skill_pills(
    skills: List[str],
):

    if not skills:

        st.caption(
            "No required skills listed."
        )

        return

    pills = "".join(
        f"""
        <span class="skill-pill">
            {_safe_text(skill)}
        </span>
        """
        for skill in skills
    )

    st.html(pills)


# ============================================================
# SIDEBAR
# ============================================================

def _show_sidebar():
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
        <div style="font-size:26px;font-weight:850;letter-spacing:-.8px;">🧠 CareerIQ</div>
        <div style="margin-top:4px;font-size:12px;color:#637789;font-weight:650;">
            AI Career Intelligence Platform
        </div>
    </div>
    """)

    st.sidebar.divider()

    navigation_options = [
        "📄 Resume Overview",
        "🎯 Job Matching",
        "🧠 Career Insights",
        "📊 Skill Gap Analysis",
        "🤖 AI Career Assistant",
        "🔎 Job Discovery",
        "📈 Career Dashboard",
        "🗺️ Career Roadmap",
    ]

    current = st.session_state.get("student_feature", "🔎 Job Discovery")
    if current not in navigation_options:
        current = "🔎 Job Discovery"

    selected = st.sidebar.radio(
        "Workspace",
        navigation_options,
        index=navigation_options.index(current),
    )

    st.session_state["student_feature"] = selected

    if selected != "🔎 Job Discovery":
        st.session_state["page"] = "student_feature"
        st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("QUICK ACTIONS")

    if st.sidebar.button("📄 Upload New Resume", use_container_width=True):
        st.session_state["student_feature"] = "📄 Resume Overview"
        st.session_state["page"] = "student_feature"
        st.rerun()

    if st.sidebar.button("🏠 Back to Home", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()


# ============================================================
# JOB CARD
# ============================================================

def _render_job_card(
    job: Dict[str, Any],
    card_index: int,
):
    title = job.get("position", "Untitled Job")
    company = job.get("company", "Unknown Company")
    location = job.get("location", "Not specified")
    employment_type = job.get("employment_type", "")

    description = str(job.get("description", "") or "")
    description = re.sub(r"<[^>]+>", " ", description)
    description = " ".join(description.split())
    if len(description) > 320:
        description = description[:320] + "..."

    score = float(job.get("match_score", 0.0) or 0.0)
    matched_skills = job.get("matched_skills", []) or []
    missing_skills = job.get("missing_skills", []) or []
    skills = job.get("job_skills", job.get("tags", [])) or []

    salary_min = job.get("salary_min")
    salary_max = job.get("salary_max")
    if salary_min is None and salary_max is None:
        salary = "Salary not specified"
    elif salary_min is not None and salary_max is not None:
        salary = f"₹{float(salary_min):,.0f} – ₹{float(salary_max):,.0f}"
    elif salary_min is not None:
        salary = f"From ₹{float(salary_min):,.0f}"
    else:
        salary = f"Up to ₹{float(salary_max):,.0f}"

    card_class = "cq-job internal" if job.get("internal") else "cq-job"

    st.html(f"""
    <div class="{card_class}">
        <div class="cq-badge">
            {"🏢 CAREERIQ COMPANY JOB" if job.get("internal") else "🌐 EXTERNAL JOB"}
        </div>
        <div class="cq-job-title">💼 {_safe_text(title)}</div>
        <div class="cq-company">🏢 {_safe_text(company)}</div>
        <div class="cq-meta">
            📍 {_safe_text(location)}
            &nbsp; • &nbsp; 💼 {_safe_text(employment_type or "Not specified")}
            &nbsp; • &nbsp; 💰 {_safe_text(salary)}
        </div>
        {
            f'<div class="cq-description">{_safe_text(description)}</div>'
            if description else ""
        }
    </div>
    """)

    left, right = st.columns([5, 1.25], gap="large")

    with left:
        st.caption("REQUIRED SKILLS")
        _render_skill_pills(skills)

        if matched_skills:
            st.success("Matched: " + ", ".join(matched_skills))
        if missing_skills:
            st.warning("Missing: " + ", ".join(missing_skills))

    with right:
        st.html(f"""
        <div class="cq-match">
            <div class="cq-match-number">{score * 100:.0f}%</div>
            <div class="cq-match-label">AI Skill Match</div>
        </div>
        """)
        st.write("")

        if job.get("internal"):
            job_id = int(job["job_id"])

            if _already_applied(job_id):
                st.button(
                    "✅ Applied",
                    key=f"applied_{job_id}",
                    use_container_width=True,
                    disabled=True,
                )
            elif st.button(
                "🚀 Apply Now",
                key=f"apply_{job_id}",
                type="primary",
                use_container_width=True,
            ):
                application = JobApplication(
                    job_id=job_id,
                    student_id=_get_student_id(),
                    match_score=score,
                    application_status="applied",
                )
                try:
                    create_job_application(application)
                    st.success("Application submitted!")
                    st.rerun()
                except Exception as e:
                    if "UNIQUE" in str(e).upper():
                        st.warning("You already applied to this job.")
                    else:
                        st.error(f"Could not submit application: {e}")
        else:
            url = job.get("url", "")
            if url:
                st.link_button("🔗 View & Apply", url, use_container_width=True)

    st.write("")


# ============================================================
# MAIN PAGE
# ============================================================

def jobs_page():

    _inject_job_discovery_style()

    _show_sidebar()

    st.html(
        """
        <div class="cq-hero">

            <div class="cq-kicker">
                CAREERIQ / OPPORTUNITIES
            </div>

            <div class="cq-hero-title">
                🔎 Job Discovery
            </div>

            <div class="cq-hero-subtitle">
                Discover jobs posted by CareerIQ companies
                and external remote opportunities. Compare
                each opportunity with the skills in your resume.
            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="cq-source">
            🏢 <b>CareerIQ Jobs</b> are posted directly by
            companies using the platform.
            &nbsp;&nbsp;
            🌐 <b>External Jobs</b> come from Remote OK and
            link back to the original posting.
        </div>
        """
    )

    resume_skills = _get_resume_skills()

    if not resume_skills:

        st.warning(
            "📄 Upload and analyze your resume first "
            "to calculate skill matches."
        )

    # ========================================================
    # SEARCH PANEL
    # ========================================================

    st.html(
        """
        <div class="cq-search">
            <div class="cq-section">
                🔍 Search Opportunities
            </div>
        </div>
        """
    )

    col1, col2 = st.columns(
        2,
        gap="large",
    )

    with col1:

        target_role = st.text_input(
            "Target Role",
            value=st.session_state.get(
                "job_search_role",
                "",
            ),
            placeholder=(
                "e.g. ML Engineer, "
                "AI Engineer, Backend Developer"
            ),
        )

    with col2:

        location = st.text_input(
            "Location",
            placeholder=(
                "Optional: Pune, Mumbai, India..."
            ),
        )

    col3, col4 = st.columns(
        2,
        gap="large",
    )

    with col3:

        work_mode = st.selectbox(
            "Work Mode",
            [
                "All",
                "Remote",
                "Hybrid",
                "On-site",
            ],
        )

    with col4:

        result_limit = st.selectbox(
            "Number of Results",
            [5, 10, 15, 20],
            index=1,
        )

    st.caption(
        "Your resume skills are used to calculate "
        "the skill match percentage."
    )

    search_clicked = st.button(
        "🚀 Find Matching Jobs",
        type="primary",
        use_container_width=True,
    )

    # ========================================================
    # LOAD INTERNAL CAREERIQ JOBS
    # ========================================================

    try:

        internal_jobs = _load_internal_jobs(
            target_role=target_role,
            location=location,
            work_mode=(
                ""
                if work_mode == "All"
                else work_mode
            ),
            resume_skills=resume_skills,
        )

    except Exception as e:

        internal_jobs = []

        st.error(
            "Could not load CareerIQ jobs: "
            f"{e}"
        )

    # ========================================================
    # SEARCH EXTERNAL JOBS
    # ========================================================

    if search_clicked:

        st.session_state[
            "job_search_role"
        ] = target_role

        with st.spinner(
            "🔎 Finding matching jobs..."
        ):

            try:

                external_jobs = (
                    _load_external_jobs(
                        target_role=target_role,
                        location=location,
                        work_mode=work_mode,
                        resume_skills=resume_skills,
                        limit=result_limit,
                    )
                )

            except Exception as e:

                external_jobs = []

                st.warning(
                    "Remote OK jobs could not be "
                    f"loaded right now: {e}"
                )

        # Reload internal jobs after search.
        internal_jobs = _load_internal_jobs(
            target_role=target_role,
            location=location,
            work_mode=(
                ""
                if work_mode == "All"
                else work_mode
            ),
            resume_skills=resume_skills,
        )

        for job in external_jobs:

            job["source"] = "Remote OK"
            job["internal"] = False

        combined_jobs = (
            internal_jobs
            + external_jobs
        )

        combined_jobs.sort(
            key=lambda item: float(
                item.get(
                    "match_score",
                    0.0,
                )
                or 0.0
            ),
            reverse=True,
        )

        st.session_state[
            "discovered_jobs"
        ] = combined_jobs[
            :result_limit
        ]

    # ========================================================
    # RESULTS
    # ========================================================

    discovered_jobs = (
        st.session_state.get(
            "discovered_jobs",
            [],
        )
    )

    if discovered_jobs:

        st.html(
            """
            <div class="cq-section">
                🎯 Matching Opportunities
            </div>
            """
        )

        careeriq_count = sum(
            1
            for job in discovered_jobs
            if job.get("internal")
        )

        external_count = (
            len(discovered_jobs)
            - careeriq_count
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Total Jobs",
            len(discovered_jobs),
        )

        c2.metric(
            "CareerIQ Jobs",
            careeriq_count,
        )

        c3.metric(
            "External Jobs",
            external_count,
        )

        for index, job in enumerate(
            discovered_jobs
        ):

            _render_job_card(
                job,
                index,
            )

    elif internal_jobs:

        st.html(
            """
            <div class="cq-section">
                🏢 CareerIQ Opportunities
            </div>
            """
        )

        st.info(
            "These active company jobs are currently "
            "available on CareerIQ."
        )

        for index, job in enumerate(
            internal_jobs[
                :result_limit
            ]
        ):

            _render_job_card(
                job,
                index,
            )

    else:

        st.html(
            """
            <div class="cq-empty">

                <div class="cq-empty-icon">
                    🔎
                </div>

                <div class="cq-empty-title">
                    No matching opportunities found
                </div>

                <div class="cq-empty-text">
                    Try a broader target role, remove
                    the location filter, or choose
                    <b>All</b> work modes.
                </div>

            </div>
            """
        )


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def job_discovery_page():
    jobs_page()


def jobs():
    jobs_page()


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":
    jobs_page()
