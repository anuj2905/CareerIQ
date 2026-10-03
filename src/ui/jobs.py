import html
import re
from typing import Any, Dict, List

import streamlit as st

from src.database.repositories import (
    get_all_active_jobs,
    get_company,
    create_job_application,
    get_job_applications,
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
    st.markdown(
        """
        <style>
        .job-hero {
            padding: 28px 30px;
            border-radius: 18px;
            background:
                linear-gradient(
                    135deg,
                    #18243a 0%,
                    #111827 55%,
                    #0f172a 100%
                );
            border: 1px solid #26344d;
            margin-bottom: 22px;
        }

        .job-hero-title {
            font-size: 38px;
            font-weight: 800;
            margin: 0;
            color: #ffffff;
        }

        .job-hero-subtitle {
            margin-top: 8px;
            color: #aeb9cc;
            font-size: 16px;
        }

        .source-card {
            padding: 14px 18px;
            border-radius: 12px;
            background: #132b45;
            border: 1px solid #214363;
            color: #d9eaff;
            margin-bottom: 22px;
        }

        .search-card {
            padding: 22px;
            border-radius: 16px;
            background: #171a24;
            border: 1px solid #292d3a;
            margin-bottom: 22px;
        }

        .section-title {
            font-size: 25px;
            font-weight: 750;
            color: #ffffff;
            margin-bottom: 12px;
        }

        .job-card {
            padding: 22px;
            border-radius: 16px;
            background: #171a24;
            border: 1px solid #2b3040;
            margin-bottom: 16px;
        }

        .job-card:hover {
            border-color: #ff4f57;
        }

        .job-title {
            font-size: 21px;
            font-weight: 750;
            color: #ffffff;
            margin-bottom: 7px;
        }

        .job-company {
            color: #b8c2d4;
            font-size: 14px;
            margin-bottom: 12px;
        }

        .job-meta {
            color: #c6cfdd;
            font-size: 13px;
            margin-bottom: 12px;
        }

        .skill-pill {
            display: inline-block;
            padding: 5px 10px;
            margin: 3px 4px 3px 0;
            border-radius: 999px;
            background: #252a36;
            color: #dce4f1;
            border: 1px solid #363c4b;
            font-size: 12px;
        }

        .match-box {
            padding: 13px 16px;
            border-radius: 12px;
            background: #12281e;
            border: 1px solid #235638;
            text-align: center;
        }

        .match-number {
            font-size: 25px;
            font-weight: 800;
            color: #62e69a;
        }

        .match-label {
            font-size: 12px;
            color: #a9c3b3;
        }

        .empty-box {
            padding: 28px;
            border-radius: 15px;
            background: #162b43;
            border: 1px solid #214363;
            color: #d8eaff;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    """
    CareerIQ currently uses student ID 1 for the local
    single-student database setup.
    """
    value = st.session_state.get("student_id")

    try:
        return int(value) if value is not None else 1
    except (TypeError, ValueError):
        return 1


def _get_resume_skills() -> List[str]:
    profile = st.session_state.get("resume_profile")

    if profile is None:
        profile = st.session_state.get("profile")

    if profile is not None:
        skills = getattr(profile, "skills", []) or []

        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]

    return []


def _job_matches_filters(
    job: Dict[str, Any],
    target_role: str,
    location: str,
    work_mode: str,
) -> bool:

    searchable_text = _normalize(
        " ".join(
            [
                str(job.get("title", "")),
                str(job.get("description", "")),
                str(job.get("company", "")),
                str(job.get("location", "")),
                " ".join(
                    str(skill)
                    for skill in job.get("skills", [])
                ),
            ]
        )
    )

    target_role = _normalize(target_role)
    location = _normalize(location)
    work_mode = _normalize(work_mode)

    if target_role:
        role_terms = target_role.split()

        if not all(
            term in searchable_text
            for term in role_terms
        ):
            return False

    if location:
        if location not in searchable_text:
            return False

    if work_mode == "remote":
        if "remote" not in searchable_text:
            return False

    elif work_mode == "hybrid":
        if "hybrid" not in searchable_text:
            return False

    elif work_mode == "onsite":
        onsite_terms = [
            "onsite",
            "on-site",
            "office",
            "pune",
            "mumbai",
            "bangalore",
            "bengaluru",
            "delhi",
            "hyderabad",
        ]

        if not any(
            term in searchable_text
            for term in onsite_terms
        ):
            return False

    return True


def _convert_internal_job(
    job,
    company
) -> Dict[str, Any]:

    company_name = (
        company.company_name
        if company
        else "CareerIQ Company"
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
        "url": "",
        "date": "",
        "match_score": 0.0,
        "matched_skills": [],
        "missing_skills": [],
        "job_skills": list(job.skills or []),
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


# ============================================================
# LOAD INTERNAL CAREERIQ JOBS
# ============================================================

def _load_internal_jobs(
    target_role: str,
    location: str,
    work_mode: str,
    resume_skills: List[str],
) -> List[Dict[str, Any]]:

    jobs = get_all_active_jobs()
    results = []

    for job in jobs:
        company = get_company(job.company_id)

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
            item.get("match_score", 0.0) or 0.0
        ),
        reverse=True,
    )

    return results


# ============================================================
# LOAD EXTERNAL JOBS
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


def _format_salary(
    salary_min: Any,
    salary_max: Any,
) -> str:

    if salary_min is None and salary_max is None:
        return "Salary not specified"

    if salary_min is not None and salary_max is not None:
        return (
            f"₹{float(salary_min):,.0f}"
            f" – "
            f"₹{float(salary_max):,.0f}"
        )

    if salary_min is not None:
        return f"From ₹{float(salary_min):,.0f}"

    return f"Up to ₹{float(salary_max):,.0f}"


def _render_skill_pills(skills: List[str]):
    if not skills:
        st.caption("No required skills listed.")

        return

    pills = "".join(
        f'<span class="skill-pill">'
        f'{_safe_text(skill)}'
        f"</span>"
        for skill in skills
    )

    st.markdown(
        pills,
        unsafe_allow_html=True,
    )


def _already_applied(job_id: int) -> bool:
    student_id = _get_student_id()

    try:
        applications = get_job_applications_for_student(
            student_id
        )

        return any(
            application.job_id == job_id
            for application in applications
        )

    except Exception:
        return False


def get_job_applications_for_student(
    student_id: int
):
    """
    Retrieve the student's applications.

    This uses the existing repository database directly so
    Job Discovery does not need a second application store.
    """

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


# ============================================================
# JOB CARD
# ============================================================

def _render_job_card(
    job: Dict[str, Any],
    card_index: int,
):

    source = job.get(
        "source",
        "External",
    )

    title = job.get(
        "position",
        "Untitled Job",
    )

    company = job.get(
        "company",
        "Unknown Company",
    )

    location = job.get(
        "location",
        "Not specified",
    )

    employment_type = job.get(
        "employment_type",
        "",
    )

    description = str(
        job.get(
            "description",
            "",
        )
        or ""
    )

    description = re.sub(
        r"<[^>]+>",
        " ",
        description,
    )

    description = " ".join(
        description.split()
    )

    if len(description) > 320:
        description = (
            description[:320]
            + "..."
        )

    score = float(
        job.get(
            "match_score",
            0.0,
        )
        or 0.0
    )

    matched_skills = job.get(
        "matched_skills",
        [],
    ) or []

    missing_skills = job.get(
        "missing_skills",
        [],
    ) or []

    skills = job.get(
        "job_skills",
        job.get("tags", []),
    ) or []

    salary = _format_salary(
        job.get("salary_min"),
        job.get("salary_max"),
    )

    st.markdown(
        '<div class="job-card">',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [5, 1.35]
    )

    with left:

        st.markdown(
            f'<div class="job-title">'
            f'💼 {_safe_text(title)}'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="job-company">'
            f'🏢 {_safe_text(company)}'
            f" &nbsp; • &nbsp; "
            f'📌 {_safe_text(source)}'
            f"</div>",
            unsafe_allow_html=True,
        )

        meta = (
            f"📍 {location}"
        )

        if employment_type:
            meta += (
                f" &nbsp; • &nbsp; "
                f"💼 {employment_type}"
            )

        meta += (
            f" &nbsp; • &nbsp; 💰 {salary}"
        )

        st.markdown(
            f'<div class="job-meta">'
            f"{_safe_text(meta)}"
            f"</div>",
            unsafe_allow_html=True,
        )

        if description:
            st.write(description)

        st.caption("Required Skills")
        _render_skill_pills(skills)

        if matched_skills:
            st.success(
                "Matched: "
                + ", ".join(matched_skills)
            )

        if missing_skills:
            st.warning(
                "Missing: "
                + ", ".join(missing_skills)
            )

    with right:

        st.markdown(
            f"""
            <div class="match-box">
                <div class="match-number">
                    {score * 100:.0f}%
                </div>
                <div class="match-label">
                    Skill Match
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if job.get("internal"):

            if _already_applied(
                int(job["job_id"])
            ):

                st.button(
                    "✅ Applied",
                    key=(
                        f"applied_{job['job_id']}"
                    ),
                    use_container_width=True,
                    disabled=True,
                )

            else:

                if st.button(
                    "🚀 Apply Now",
                    key=(
                        f"apply_{job['job_id']}"
                    ),
                    type="primary",
                    use_container_width=True,
                ):

                    student_id = _get_student_id()

                    application = JobApplication(
                        job_id=int(
                            job["job_id"]
                        ),
                        student_id=student_id,
                        match_score=score,
                        application_status="applied",
                    )

                    try:

                        create_job_application(
                            application
                        )

                        st.success(
                            "Application submitted!"
                        )

                        st.rerun()

                    except Exception as e:

                        if "UNIQUE" in str(e).upper():

                            st.warning(
                                "You already applied "
                                "to this job."
                            )

                        else:

                            st.error(
                                "Could not submit "
                                f"application: {e}"
                            )

        else:

            url = job.get("url", "")

            if url:

                st.link_button(
                    "🔗 View & Apply",
                    url,
                    use_container_width=True,
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN PAGE
# ============================================================

def jobs_page():

    _inject_job_discovery_style()

    st.markdown(
        """
        <div class="job-hero">
            <div class="job-hero-title">
                🔎 Job Discovery
            </div>
            <div class="job-hero-subtitle">
                Discover CareerIQ company jobs and
                current remote opportunities matched
                with your resume.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="source-card">
            🏢 <b>CareerIQ Jobs</b> come directly from
            companies using the CareerIQ platform.
            🌐 <b>External Jobs</b> are fetched from
            Remote OK and link back to the original posting.
        </div>
        """,
        unsafe_allow_html=True,
    )

    resume_skills = _get_resume_skills()

    if not resume_skills:

        st.warning(
            "📄 Upload and analyze your resume first "
            "to calculate skill matches."
        )

    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">'
        '🔍 Search Jobs'
        '</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

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
                "Optional: Pune, Mumbai, "
                "India, Europe..."
            ),
        )

    col3, col4 = st.columns(2)

    with col3:

        work_mode = st.selectbox(
            "Work Mode",
            [
                "Remote",
                "Hybrid",
                "On-site",
                "All",
            ],
        )

    with col4:

        result_limit = st.selectbox(
            "Number of Results",
            [5, 10, 15, 20],
            index=1,
        )

    st.caption(
        "Your resume skills are automatically used "
        "to calculate the skill match percentage."
    )

    search_clicked = st.button(
        "🚀 Find Matching Jobs",
        type="primary",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # ========================================================
    # INITIAL INTERNAL JOB PREVIEW
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
    # SEARCH
    # ========================================================

    if search_clicked:

        st.session_state[
            "job_search_role"
        ] = target_role

        with st.spinner(
            "🔎 Finding matching jobs..."
        ):

            try:

                external_jobs = _load_external_jobs(
                    target_role=target_role,
                    location=location,
                    work_mode=work_mode,
                    resume_skills=resume_skills,
                    limit=result_limit,
                )

            except Exception as e:

                external_jobs = []

                st.warning(
                    "Remote OK jobs could not be loaded "
                    f"right now: {e}"
                )

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
            key=lambda item: item.get(
                "match_score",
                0.0,
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

    discovered_jobs = st.session_state.get(
        "discovered_jobs",
        [],
    )

    if discovered_jobs:

        st.markdown(
            '<div class="section-title">'
            '🎯 Matching Opportunities'
            '</div>',
            unsafe_allow_html=True,
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

    else:

        # Show active CareerIQ jobs even before
        # an external search has been performed.
        if internal_jobs:

            st.markdown(
                '<div class="section-title">'
                '🏢 CareerIQ Opportunities'
                '</div>',
                unsafe_allow_html=True,
            )

            st.info(
                "These active jobs are currently "
                "available on CareerIQ."
            )

            for index, job in enumerate(
                internal_jobs[:result_limit]
            ):
                _render_job_card(
                    job,
                    index,
                )

        else:

            st.markdown(
                """
                <div class="empty-box">
                    🔎 Enter a target role and click
                    <b>Find Matching Jobs</b> to discover
                    current opportunities.
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# COMPATIBILITY ALIAS
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
