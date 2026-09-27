import html
import streamlit as st

from src.auth.auth_repository import get_user_company
from src.database.repositories import (
    get_company_jobs,
    get_job_applications,
    update_job_status,
    delete_job,
)


# ============================================================
# PREMIUM CAREERIQ JOB MANAGEMENT UI
# ============================================================

def style_job_management():
    st.html("""
    <style>
        .stApp {
            background:
                radial-gradient(circle at 7% 4%, rgba(99,102,241,.17), transparent 27%),
                radial-gradient(circle at 94% 12%, rgba(168,85,247,.13), transparent 30%),
                radial-gradient(circle at 48% 100%, rgba(14,165,233,.08), transparent 34%),
                linear-gradient(135deg,#070b17 0%,#0b1020 48%,#111827 100%);
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        .stButton > button {
            min-height: 43px;
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

        [data-testid="stMetric"] {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.075);
            border-radius: 17px;
            padding: 14px 16px;
        }

        hr {
            border-color: rgba(255,255,255,.08);
        }
    </style>
    """)


def safe_text(value):
    if value is None:
        return ""
    return html.escape(str(value))


# ============================================================
# STATUS
# ============================================================

def get_status_meta(status):
    status = str(status or "active").strip().lower()

    mapping = {
        "active": ("ACTIVE", "#4ade80", "rgba(34,197,94,.13)", "●"),
        "paused": ("PAUSED", "#fbbf24", "rgba(245,158,11,.13)", "Ⅱ"),
        "closed": ("CLOSED", "#94a3b8", "rgba(148,163,184,.13)", "■"),
        "draft": ("DRAFT", "#c4b5fd", "rgba(139,92,246,.13)", "✎"),
    }

    return mapping.get(
        status,
        (status.upper(), "#cbd5e1", "rgba(148,163,184,.13)", "●"),
    )


def get_status_badge(status):
    label, color, background, icon = get_status_meta(status)

    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding:7px 11px;
        border-radius:999px;
        background:{background};
        border:1px solid {color}45;
        color:{color};
        font-size:10px;
        font-weight:850;
        letter-spacing:.06em;
        white-space:nowrap;
    ">
        {icon} {label}
    </span>
    """


# ============================================================
# HERO
# ============================================================

def render_hero(company_name, total, active, applications):
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
            width:290px;
            height:290px;
            right:-100px;
            top:-150px;
            border-radius:50%;
            background:rgba(139,92,246,.17);
            filter:blur(52px);
        "></div>

        <div style="
            position:absolute;
            width:170px;
            height:170px;
            left:-90px;
            bottom:-110px;
            border-radius:50%;
            background:rgba(59,130,246,.10);
            filter:blur(45px);
        "></div>

        <div style="position:relative;z-index:2;">
            <div style="
                display:flex;
                align-items:flex-start;
                justify-content:space-between;
                gap:24px;
                flex-wrap:wrap;
            ">
                <div>
                    <div style="
                        display:inline-flex;
                        padding:7px 12px;
                        border-radius:999px;
                        background:rgba(255,255,255,.08);
                        border:1px solid rgba(255,255,255,.13);
                        color:#c4b5fd;
                        font-size:10px;
                        font-weight:850;
                        letter-spacing:.10em;
                    ">
                        JOB MANAGEMENT
                    </div>

                    <div style="
                        color:#fff;
                        font-size:36px;
                        line-height:1.12;
                        font-weight:850;
                        letter-spacing:-.025em;
                        margin-top:15px;
                    ">
                        Manage your jobs
                    </div>

                    <div style="
                        color:#cbd5e1;
                        font-size:15px;
                        line-height:1.7;
                        margin-top:9px;
                        max-width:690px;
                    ">
                        Create, monitor and manage opportunities published by
                        <strong>{company_name}</strong>.
                    </div>
                </div>

                <div style="
                    min-width:185px;
                    padding:18px;
                    border-radius:19px;
                    background:rgba(255,255,255,.045);
                    border:1px solid rgba(255,255,255,.08);
                    text-align:center;
                ">
                    <div style="
                        color:#64748b;
                        font-size:10px;
                        font-weight:800;
                        letter-spacing:.07em;
                    ">
                        CANDIDATE ACTIVITY
                    </div>
                    <div style="
                        color:#fff;
                        font-size:29px;
                        font-weight:850;
                        margin-top:4px;
                    ">
                        {applications}
                    </div>
                    <div style="color:#94a3b8;font-size:11px;">
                        total applications
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)


def render_html(content):
    st.html(content)


# ============================================================
# JOB CARD
# ============================================================

def render_job_card(
    job,
    company_name,
    application_count,
):
    title = safe_text(job.title or "Untitled Job")
    location = safe_text(job.location or "Location not specified")
    employment = safe_text(job.employment_type or "Not specified")
    education = safe_text(job.education_required or "Not specified")

    try:
        experience = float(job.experience_required or 0)
        experience_text = f"{experience:g}+ years"
    except (TypeError, ValueError):
        experience_text = "Not specified"

    status = str(job.status or "active").lower()
    status_badge = get_status_badge(status)

    salary = "Salary not specified"
    if job.salary_min is not None and job.salary_max is not None:
        salary = f"₹{job.salary_min:,.0f} – ₹{job.salary_max:,.0f}"
    elif job.salary_min is not None:
        salary = f"From ₹{job.salary_min:,.0f}"
    elif job.salary_max is not None:
        salary = f"Up to ₹{job.salary_max:,.0f}"

    salary = safe_text(salary)

    render_html(f"""
    <div style="
        position:relative;
        overflow:hidden;
        padding:23px;
        margin-top:14px;
        border-radius:21px;
        background:
            linear-gradient(145deg,
                rgba(15,23,42,.86),
                rgba(30,41,59,.62));
        border:1px solid rgba(255,255,255,.075);
        box-shadow:0 16px 42px rgba(0,0,0,.18);
    ">
        <div style="
            position:absolute;
            left:0;
            top:0;
            bottom:0;
            width:4px;
            background:linear-gradient(180deg,#6366f1,#a855f7);
        "></div>

        <div style="
            display:flex;
            align-items:flex-start;
            justify-content:space-between;
            gap:20px;
            flex-wrap:wrap;
        ">
            <div style="min-width:260px;flex:1;">
                <div style="
                    color:#fff;
                    font-size:21px;
                    font-weight:850;
                    letter-spacing:-.015em;
                ">
                    {title}
                </div>

                <div style="
                    color:#94a3b8;
                    font-size:13px;
                    margin-top:6px;
                ">
                    🏢 {company_name}
                </div>

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:7px;
                    margin-top:15px;
                ">
                    <span style="
                        padding:6px 10px;
                        border-radius:999px;
                        background:rgba(255,255,255,.055);
                        color:#cbd5e1;
                        font-size:11px;
                        font-weight:650;
                    ">📍 {location}</span>

                    <span style="
                        padding:6px 10px;
                        border-radius:999px;
                        background:rgba(255,255,255,.055);
                        color:#cbd5e1;
                        font-size:11px;
                        font-weight:650;
                    ">💼 {employment}</span>

                    <span style="
                        padding:6px 10px;
                        border-radius:999px;
                        background:rgba(255,255,255,.055);
                        color:#cbd5e1;
                        font-size:11px;
                        font-weight:650;
                    ">🎓 {education}</span>

                    <span style="
                        padding:6px 10px;
                        border-radius:999px;
                        background:rgba(255,255,255,.055);
                        color:#cbd5e1;
                        font-size:11px;
                        font-weight:650;
                    ">💻 {experience_text}</span>
                </div>
            </div>

            <div style="
                min-width:145px;
                text-align:right;
            ">
                {status_badge}

                <div style="
                    color:#cbd5e1;
                    font-size:14px;
                    font-weight:750;
                    margin-top:12px;
                ">
                    {salary}
                </div>
            </div>
        </div>

        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:15px;
            margin-top:19px;
            padding-top:16px;
            border-top:1px solid rgba(255,255,255,.065);
        ">
            <div style="
                color:#a5b4fc;
                font-size:13px;
                font-weight:750;
            ">
                👥 {application_count} application(s)
            </div>

            <div style="
                color:#64748b;
                font-size:11px;
            ">
                CareerIQ job
            </div>
        </div>
    </div>
    """)


# ============================================================
# MAIN PAGE
# ============================================================

def job_management_page():
    style_job_management()

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Please log in first.")
        st.session_state["page"] = "home"
        st.rerun()
        return

    company = get_user_company(user_id)

    if not company:
        render_html("""
        <div style="
            padding:50px 30px;
            text-align:center;
            border-radius:24px;
            background:rgba(15,23,42,.80);
            border:1px solid rgba(255,255,255,.08);
        ">
            <div style="font-size:48px;">🏢</div>
            <div style="
                color:#fff;
                font-size:24px;
                font-weight:850;
                margin-top:10px;
            ">
                Create your company profile
            </div>
            <div style="
                color:#94a3b8;
                font-size:14px;
                margin-top:8px;
            ">
                Your company profile is required before you can publish jobs.
            </div>
        </div>
        """)

        if st.button(
            "Create Company Profile",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["page"] = "company_profile"
            st.rerun()

        return

    company_id = company["id"]
    company_name = safe_text(
        company.get("company_name", "Your Company")
    )

    jobs = get_company_jobs(company_id)

    # --------------------------------------------------------
    # APPLICATION TOTAL
    # --------------------------------------------------------

    total_applications = 0
    application_counts = {}

    for job in jobs:
        try:
            count = len(get_job_applications(job.id))
        except Exception:
            count = 0

        application_counts[job.id] = count
        total_applications += count

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    total_jobs = len(jobs)
    active_jobs = sum(
        1 for job in jobs
        if str(job.status or "").lower() == "active"
    )
    paused_jobs = sum(
        1 for job in jobs
        if str(job.status or "").lower() == "paused"
    )
    closed_jobs = sum(
        1 for job in jobs
        if str(job.status or "").lower() == "closed"
    )

    render_hero(
        company_name,
        total_jobs,
        active_jobs,
        total_applications,
    )

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    cols = st.columns(4)

    metrics = [
        ("📋", total_jobs, "Total Jobs"),
        ("🟢", active_jobs, "Active Jobs"),
        ("🟡", paused_jobs, "Paused Jobs"),
        ("👥", total_applications, "Applications"),
    ]

    for col, (icon, value, label) in zip(cols, metrics):
        with col:
            render_html(f"""
            <div style="
                padding:18px;
                border-radius:17px;
                background:rgba(255,255,255,.035);
                border:1px solid rgba(255,255,255,.075);
            ">
                <div style="font-size:20px;">{icon}</div>
                <div style="
                    color:#fff;
                    font-size:27px;
                    font-weight:850;
                    margin-top:5px;
                ">
                    {value}
                </div>
                <div style="
                    color:#64748b;
                    font-size:11px;
                    font-weight:700;
                    margin-top:2px;
                ">
                    {label}
                </div>
            </div>
            """)

    # --------------------------------------------------------
    # TOOLBAR
    # --------------------------------------------------------

    st.html("""
    <div style="
        margin-top:30px;
        margin-bottom:8px;
        color:#fff;
        font-size:23px;
        font-weight:850;
    ">
        Your Jobs
    </div>
    """)

    toolbar1, toolbar2 = st.columns([3, 1])

    with toolbar1:
        st.html("""
        <div style="
            color:#64748b;
            font-size:13px;
            line-height:1.6;
            margin-top:3px;
        ">
            Manage published opportunities, monitor applications,
            and control job availability.
        </div>
        """)

    with toolbar2:
        if st.button(
            "＋ Create New Job",
            type="primary",
            use_container_width=True,
            key="create_new_job_management",
        ):
            st.session_state["page"] = "create_job"
            st.rerun()

    # --------------------------------------------------------
    # EMPTY
    # --------------------------------------------------------

    if not jobs:
        render_html("""
        <div style="
            margin-top:25px;
            padding:65px 30px;
            text-align:center;
            border-radius:24px;
            background:
                linear-gradient(145deg,
                    rgba(15,23,42,.84),
                    rgba(30,41,59,.62));
            border:1px solid rgba(255,255,255,.08);
            box-shadow:0 20px 55px rgba(0,0,0,.20);
        ">
            <div style="font-size:55px;">📋</div>

            <div style="
                color:#fff;
                font-size:26px;
                font-weight:850;
                margin-top:12px;
            ">
                No jobs published yet
            </div>

            <div style="
                max-width:600px;
                margin:9px auto 0;
                color:#94a3b8;
                font-size:14px;
                line-height:1.7;
            ">
                Create your first opportunity and start attracting
                qualified candidates through CareerIQ.
            </div>
        </div>
        """)

        if st.button(
            "🚀 Create Your First Job",
            type="primary",
            use_container_width=True,
            key="create_first_job",
        ):
            st.session_state["page"] = "create_job"
            st.rerun()

        return

    # --------------------------------------------------------
    # FILTER / SORT
    # --------------------------------------------------------

    filter_col, sort_col = st.columns(2)

    with filter_col:
        filter_status = st.selectbox(
            "Filter jobs",
            ["All", "Active", "Paused", "Closed", "Draft"],
            key="job_management_status_filter",
        )

    with sort_col:
        sort_by = st.selectbox(
            "Sort jobs",
            ["Newest / Database Order", "Title", "Applications"],
            key="job_management_sort",
        )

    visible_jobs = list(jobs)

    if filter_status != "All":
        visible_jobs = [
            job for job in visible_jobs
            if str(job.status or "").lower() == filter_status.lower()
        ]

    if sort_by == "Title":
        visible_jobs.sort(
            key=lambda job: (job.title or "").lower()
        )
    elif sort_by == "Applications":
        visible_jobs.sort(
            key=lambda job: application_counts.get(job.id, 0),
            reverse=True,
        )

    st.html(f"""
    <div style="
        margin-top:16px;
        color:#64748b;
        font-size:11px;
        font-weight:700;
    ">
        Showing {len(visible_jobs)} of {len(jobs)} jobs
    </div>
    """)

    # --------------------------------------------------------
    # JOBS
    # --------------------------------------------------------

    for job in visible_jobs:
        job_id = job.id
        application_count = application_counts.get(job_id, 0)

        render_job_card(
            job,
            company_name,
            application_count,
        )

        action1, action2, action3, action4 = st.columns(4)

        with action1:
            if st.button(
                "👁 View Details",
                key=f"view_job_{job_id}",
                use_container_width=True,
            ):
                st.session_state["selected_job_id"] = job_id
                st.session_state["page"] = "job_details"
                st.rerun()

        with action2:
            status = str(job.status or "active").lower()

            if status == "active":
                action_label = "⏸ Pause"
                next_status = "paused"
            else:
                action_label = "▶ Activate"
                next_status = "active"

            if st.button(
                action_label,
                key=f"toggle_job_{job_id}",
                use_container_width=True,
            ):
                update_job_status(job_id, next_status)
                st.rerun()

        with action3:
            if st.button(
                "👥 Applicants",
                key=f"applications_{job_id}",
                use_container_width=True,
            ):
                st.session_state["selected_job_id"] = job_id
                st.session_state["page"] = "job_applications"
                st.rerun()

        with action4:
            if st.button(
                "🗑 Delete",
                key=f"delete_job_{job_id}",
                use_container_width=True,
            ):
                st.session_state[f"confirm_delete_{job_id}"] = True
                st.rerun()

        # ----------------------------------------------------
        # DELETE CONFIRMATION
        # ----------------------------------------------------

        if st.session_state.get(
            f"confirm_delete_{job_id}",
            False,
        ):
            render_html(f"""
            <div style="
                margin-top:10px;
                padding:18px;
                border-radius:17px;
                background:rgba(239,68,68,.065);
                border:1px solid rgba(239,68,68,.16);
            ">
                <div style="
                    color:#fca5a5;
                    font-weight:800;
                    font-size:14px;
                ">
                    Delete “{safe_text(job.title)}”?
                </div>
                <div style="
                    color:#94a3b8;
                    font-size:12px;
                    margin-top:5px;
                ">
                    This action cannot be undone.
                </div>
            </div>
            """)

            confirm1, confirm2 = st.columns(2)

            with confirm1:
                if st.button(
                    "Yes, Delete Job",
                    type="primary",
                    use_container_width=True,
                    key=f"confirm_yes_{job_id}",
                ):
                    delete_job(job_id)
                    st.session_state.pop(
                        f"confirm_delete_{job_id}",
                        None,
                    )
                    st.rerun()

            with confirm2:
                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key=f"confirm_no_{job_id}",
                ):
                    st.session_state.pop(
                        f"confirm_delete_{job_id}",
                        None,
                    )
                    st.rerun()

        st.html('<div style="height:8px;"></div>')

    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    st.html('<div style="height:12px;"></div>')

    if st.button(
        "← Back to Company Dashboard",
        use_container_width=True,
        key="back_company_dashboard",
    ):
        st.session_state["page"] = "company_dashboard"
        st.rerun()


# ============================================================
# ENTRY POINT
# ============================================================

def job_management():
    job_management_page()
