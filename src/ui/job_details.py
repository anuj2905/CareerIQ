import html
import streamlit as st

from src.auth.auth_repository import get_user_company
from src.database.repositories import (
    get_job,
    get_company,
    get_job_applications,
    update_job_status,
    delete_job,
)


# ============================================================
# PAGE STYLE
# ============================================================

def apply_job_details_style():
    st.html("""
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 4%, rgba(99,102,241,.17), transparent 28%),
                radial-gradient(circle at 92% 14%, rgba(168,85,247,.13), transparent 30%),
                radial-gradient(circle at 52% 100%, rgba(14,165,233,.08), transparent 32%),
                linear-gradient(135deg, #070b17 0%, #0b1020 48%, #111827 100%);
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .stButton > button {
            min-height: 44px;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,.10);
            background: rgba(255,255,255,.055);
            color: #f8fafc;
            font-weight: 650;
            transition: all .2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(139,92,246,.60);
            background: rgba(139,92,246,.15);
            box-shadow: 0 8px 24px rgba(0,0,0,.20);
        }

        .stSelectbox div[data-baseweb="select"] {
            background: rgba(255,255,255,.045) !important;
            border: 1px solid rgba(255,255,255,.10) !important;
            border-radius: 12px !important;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.075);
            border-radius: 16px;
            padding: 14px 16px;
        }

        hr {
            border-color: rgba(255,255,255,.08);
        }
    </style>
    """)


def render_html(content: str):
    st.html(content)


# ============================================================
# STATUS
# ============================================================

def get_job_status_meta(status):
    status = (status or "active").lower()

    mapping = {
        "active": ("ACTIVE", "#4ade80", "rgba(34,197,94,.13)", "●"),
        "paused": ("PAUSED", "#fbbf24", "rgba(245,158,11,.13)", "Ⅱ"),
        "draft": ("DRAFT", "#c4b5fd", "rgba(139,92,246,.13)", "✎"),
        "closed": ("CLOSED", "#94a3b8", "rgba(148,163,184,.13)", "■"),
    }

    return mapping.get(
        status,
        (status.upper(), "#cbd5e1", "rgba(148,163,184,.13)", "●"),
    )


# ============================================================
# HERO
# ============================================================

def render_hero(job, company):
    title = html.escape(job.title or "Untitled Job")
    company_name = html.escape(
        company.company_name if company else "Your Company"
    )
    location = html.escape(job.location or "Location not specified")
    employment = html.escape(
        job.employment_type or "Employment type not specified"
    )

    label, color, background, icon = get_job_status_meta(job.status)

    render_html(f"""
    <div style="
        position:relative;
        overflow:hidden;
        padding:34px;
        margin-bottom:22px;
        border-radius:27px;
        background:
            linear-gradient(135deg,
                rgba(99,102,241,.20),
                rgba(168,85,247,.11) 46%,
                rgba(15,23,42,.95));
        border:1px solid rgba(255,255,255,.095);
        box-shadow:0 28px 70px rgba(0,0,0,.30);
    ">
        <div style="
            position:absolute;
            width:280px;
            height:280px;
            right:-95px;
            top:-145px;
            border-radius:50%;
            background:rgba(139,92,246,.17);
            filter:blur(50px);
        "></div>

        <div style="
            position:absolute;
            width:170px;
            height:170px;
            left:-90px;
            bottom:-110px;
            border-radius:50%;
            background:rgba(59,130,246,.10);
            filter:blur(42px);
        "></div>

        <div style="position:relative;z-index:2;">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                gap:25px;
                flex-wrap:wrap;
            ">
                <div style="max-width:900px;">
                    <div style="
                        display:inline-flex;
                        align-items:center;
                        gap:7px;
                        padding:7px 12px;
                        border-radius:999px;
                        background:{background};
                        border:1px solid {color}45;
                        color:{color};
                        font-size:11px;
                        font-weight:800;
                        letter-spacing:.06em;
                        margin-bottom:15px;
                    ">
                        {icon} {label}
                    </div>

                    <div style="
                        color:#fff;
                        font-size:37px;
                        line-height:1.12;
                        font-weight:850;
                        letter-spacing:-.025em;
                    ">
                        {title}
                    </div>

                    <div style="
                        margin-top:9px;
                        color:#cbd5e1;
                        font-size:16px;
                    ">
                        {company_name}
                    </div>

                    <div style="
                        display:flex;
                        flex-wrap:wrap;
                        gap:9px;
                        margin-top:20px;
                    ">
                        <span style="
                            padding:9px 13px;
                            border-radius:11px;
                            background:rgba(255,255,255,.055);
                            border:1px solid rgba(255,255,255,.06);
                            color:#e2e8f0;
                            font-size:13px;
                        ">
                            📍 {location}
                        </span>

                        <span style="
                            padding:9px 13px;
                            border-radius:11px;
                            background:rgba(255,255,255,.055);
                            border:1px solid rgba(255,255,255,.06);
                            color:#e2e8f0;
                            font-size:13px;
                        ">
                            💼 {employment}
                        </span>
                    </div>
                </div>

                <div style="
                    min-width:165px;
                    padding:18px;
                    border-radius:18px;
                    background:rgba(255,255,255,.045);
                    border:1px solid rgba(255,255,255,.08);
                    text-align:center;
                ">
                    <div style="
                        color:#94a3b8;
                        font-size:10px;
                        font-weight:800;
                        letter-spacing:.07em;
                    ">
                        JOB STATUS
                    </div>

                    <div style="
                        color:{color};
                        font-size:22px;
                        font-weight:850;
                        margin-top:6px;
                    ">
                        {label}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)


# ============================================================
# JOB INFORMATION
# ============================================================

def render_job_information(job):
    description = html.escape(
        job.description or "No job description provided."
    )

    education = html.escape(
        job.education_required or "Not specified"
    )

    try:
        experience = float(job.experience_required or 0)
    except (TypeError, ValueError):
        experience = 0

    if job.salary_min is not None and job.salary_max is not None:
        salary_text = (
            f"₹{job.salary_min:,.0f} - "
            f"₹{job.salary_max:,.0f}"
        )
    elif job.salary_min is not None:
        salary_text = f"From ₹{job.salary_min:,.0f}"
    elif job.salary_max is not None:
        salary_text = f"Up to ₹{job.salary_max:,.0f}"
    else:
        salary_text = "Not specified"

    salary_text = html.escape(salary_text)

    render_html(f"""
    <div style="
        padding:27px;
        border-radius:21px;
        background:rgba(15,23,42,.72);
        border:1px solid rgba(255,255,255,.08);
        box-shadow:0 17px 45px rgba(0,0,0,.20);
    ">
        <div style="
            color:#fff;
            font-size:21px;
            font-weight:800;
            margin-bottom:17px;
        ">
            📋 Job Information
        </div>

        <div style="
            display:grid;
            grid-template-columns:repeat(3,minmax(0,1fr));
            gap:13px;
            margin-bottom:24px;
        ">
            <div style="
                padding:17px;
                border-radius:15px;
                background:rgba(255,255,255,.043);
                border:1px solid rgba(255,255,255,.045);
            ">
                <div style="color:#64748b;font-size:10px;font-weight:800;letter-spacing:.06em;">
                    EXPERIENCE
                </div>
                <div style="color:#fff;font-size:16px;font-weight:750;margin-top:7px;">
                    {experience:.1f} years
                </div>
            </div>

            <div style="
                padding:17px;
                border-radius:15px;
                background:rgba(255,255,255,.043);
                border:1px solid rgba(255,255,255,.045);
            ">
                <div style="color:#64748b;font-size:10px;font-weight:800;letter-spacing:.06em;">
                    EDUCATION
                </div>
                <div style="color:#fff;font-size:16px;font-weight:750;margin-top:7px;">
                    {education}
                </div>
            </div>

            <div style="
                padding:17px;
                border-radius:15px;
                background:rgba(255,255,255,.043);
                border:1px solid rgba(255,255,255,.045);
            ">
                <div style="color:#64748b;font-size:10px;font-weight:800;letter-spacing:.06em;">
                    SALARY
                </div>
                <div style="color:#fff;font-size:16px;font-weight:750;margin-top:7px;">
                    {salary_text}
                </div>
            </div>
        </div>

        <div style="
            color:#fff;
            font-size:16px;
            font-weight:750;
            margin-bottom:10px;
        ">
            Job Description
        </div>

        <div style="
            color:#cbd5e1;
            font-size:15px;
            line-height:1.8;
            white-space:pre-wrap;
        ">
            {description}
        </div>
    </div>
    """)


# ============================================================
# SKILLS
# ============================================================

def render_skills(job):
    skills = job.skills or []

    if not skills:
        render_html("""
        <div style="
            margin-top:20px;
            padding:24px;
            border-radius:20px;
            background:rgba(15,23,42,.72);
            border:1px solid rgba(255,255,255,.08);
            color:#94a3b8;
        ">
            🧠 No required skills have been added to this job.
        </div>
        """)
        return

    skills_html = ""

    for skill in skills:
        skill_text = html.escape(str(skill))
        skills_html += f"""
        <span style="
            display:inline-flex;
            padding:8px 13px;
            margin:4px;
            border-radius:999px;
            background:linear-gradient(
                135deg,
                rgba(99,102,241,.18),
                rgba(168,85,247,.15)
            );
            border:1px solid rgba(139,92,246,.25);
            color:#ddd6fe;
            font-size:13px;
            font-weight:650;
        ">
            {skill_text}
        </span>
        """

    render_html(f"""
    <div style="
        padding:27px;
        margin-top:20px;
        border-radius:21px;
        background:rgba(15,23,42,.72);
        border:1px solid rgba(255,255,255,.08);
        box-shadow:0 17px 45px rgba(0,0,0,.18);
    ">
        <div style="
            color:#fff;
            font-size:21px;
            font-weight:800;
            margin-bottom:13px;
        ">
            🧠 Required Skills
        </div>

        <div>{skills_html}</div>
    </div>
    """)


# ============================================================
# APPLICATION STATISTICS
# ============================================================

def render_application_stats(applications):
    total = len(applications)

    counts = {}
    for application in applications:
        key = (
            application.application_status or "applied"
        ).lower()
        counts[key] = counts.get(key, 0) + 1

    render_html("""
    <div style="
        margin-top:29px;
        margin-bottom:12px;
        color:#fff;
        font-size:21px;
        font-weight:800;
    ">
        👥 Applications
    </div>
    """)

    stats = [
        ("Total", total),
        ("Applied", counts.get("applied", 0)),
        ("Shortlisted", counts.get("shortlisted", 0)),
        ("Rejected", counts.get("rejected", 0)),
    ]

    columns = st.columns(4)

    for column, (label, value) in zip(columns, stats):
        with column:
            st.metric(label, value)


# ============================================================
# MAIN PAGE
# ============================================================

def job_details_page():
    apply_job_details_style()

    # --------------------------------------------------------
    # AUTH
    # --------------------------------------------------------

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please log in first.")
        st.session_state["page"] = "company"
        st.rerun()

    # --------------------------------------------------------
    # COMPANY
    # --------------------------------------------------------

    company = get_user_company(user_id)

    if not company:
        st.warning("No company is linked to your account.")
        st.session_state["page"] = "company_selector"
        st.rerun()

    # --------------------------------------------------------
    # JOB ID
    # --------------------------------------------------------

    job_id = st.session_state.get("selected_job_id")

    if not job_id:
        st.warning("No job selected.")
        st.session_state["page"] = "job_management"
        st.rerun()

    # --------------------------------------------------------
    # JOB
    # --------------------------------------------------------

    job = get_job(job_id)

    if not job:
        st.error("Job not found.")
        st.session_state["page"] = "job_management"
        st.rerun()

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    if job.company_id != company.id:
        st.error("You are not authorized to view this job.")

        if st.button(
            "← Back to Job Management",
            use_container_width=True,
        ):
            st.session_state["page"] = "job_management"
            st.rerun()

        return

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    render_hero(job, company)

    # --------------------------------------------------------
    # PRIMARY ACTIONS
    # --------------------------------------------------------

    action1, action2, action3, action4 = st.columns(4)

    with action1:
        if st.button(
            "← Back to Jobs",
            use_container_width=True,
            key="details_back_jobs",
        ):
            st.session_state["page"] = "job_management"
            st.rerun()

    with action2:
        if job.status == "active":
            if st.button(
                "⏸ Pause Job",
                use_container_width=True,
                key="details_pause_job",
            ):
                success = update_job_status(job.id, "paused")

                if success is not False:
                    st.success("Job paused successfully.")
                    st.rerun()

                st.error("Could not update job status.")
        else:
            if st.button(
                "▶ Activate Job",
                use_container_width=True,
                key="details_activate_job",
            ):
                success = update_job_status(job.id, "active")

                if success is not False:
                    st.success("Job activated successfully.")
                    st.rerun()

                st.error("Could not update job status.")

    with action3:
        if st.button(
            "👥 View Applicants",
            use_container_width=True,
            key="details_view_applicants",
        ):
            st.session_state["selected_job_id"] = job.id
            st.session_state["page"] = "job_applications"
            st.rerun()

    with action4:
        if st.button(
            "✏️ Edit Job",
            use_container_width=True,
            key="details_edit_job",
        ):
            st.session_state["editing_job_id"] = job.id
            st.session_state["page"] = "create_job"
            st.rerun()

    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    render_job_information(job)
    render_skills(job)

    applications = get_job_applications(job.id)
    render_application_stats(applications)

    # --------------------------------------------------------
    # QUICK APPLICATION INSIGHT
    # --------------------------------------------------------

    if applications:
        scores = [
            float(application.match_score)
            for application in applications
            if application.match_score is not None
        ]

        if scores:
            average_score = sum(scores) / len(scores) * 100
            highest_score = max(scores) * 100

            render_html(f"""
            <div style="
                display:grid;
                grid-template-columns:repeat(2,minmax(0,1fr));
                gap:14px;
                margin-top:17px;
            ">
                <div style="
                    padding:18px;
                    border-radius:17px;
                    background:rgba(255,255,255,.035);
                    border:1px solid rgba(255,255,255,.07);
                ">
                    <div style="color:#64748b;font-size:10px;font-weight:800;letter-spacing:.06em;">
                        AVERAGE AI MATCH
                    </div>
                    <div style="color:#a78bfa;font-size:25px;font-weight:850;margin-top:5px;">
                        {average_score:.1f}%
                    </div>
                </div>

                <div style="
                    padding:18px;
                    border-radius:17px;
                    background:rgba(255,255,255,.035);
                    border:1px solid rgba(255,255,255,.07);
                ">
                    <div style="color:#64748b;font-size:10px;font-weight:800;letter-spacing:.06em;">
                        HIGHEST MATCH
                    </div>
                    <div style="color:#4ade80;font-size:25px;font-weight:850;margin-top:5px;">
                        {highest_score:.1f}%
                    </div>
                </div>
            </div>
            """)

    # --------------------------------------------------------
    # DANGER ZONE
    # --------------------------------------------------------

    render_html("""
    <div style="
        margin-top:34px;
        margin-bottom:12px;
        color:#fca5a5;
        font-size:19px;
        font-weight:800;
    ">
        ⚠️ Danger Zone
    </div>
    """)

    delete_confirm_key = f"confirm_delete_job_{job.id}"

    if not st.session_state.get(delete_confirm_key, False):
        st.html("""
        <div style="
            padding:18px;
            margin-bottom:10px;
            border-radius:17px;
            background:rgba(239,68,68,.055);
            border:1px solid rgba(239,68,68,.14);
            color:#cbd5e1;
            font-size:13px;
        ">
            Deleting a job is permanent. Use this only when the job should
            no longer exist in your company workspace.
        </div>
        """)

        if st.button(
            "🗑️ Delete Job",
            key="delete_job_button",
        ):
            st.session_state[delete_confirm_key] = True
            st.rerun()

    else:
        st.warning(
            "Are you sure you want to delete this job? "
            "This action cannot be undone."
        )

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button(
                "Yes, Delete Job",
                use_container_width=True,
                key="confirm_delete_job_button",
            ):
                success = delete_job(job.id)

                if success is not False:
                    st.session_state.pop(delete_confirm_key, None)
                    st.session_state.pop("selected_job_id", None)
                    st.success("Job deleted successfully.")
                    st.session_state["page"] = "job_management"
                    st.rerun()

                st.error("Could not delete the job.")

        with cancel_col:
            if st.button(
                "Cancel",
                use_container_width=True,
                key="cancel_delete_job_button",
            ):
                st.session_state.pop(delete_confirm_key, None)
                st.rerun()


# ============================================================
# ENTRY POINT
# ============================================================

def job_details():
    job_details_page()
