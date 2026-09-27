import html
import streamlit as st

from src.database.repositories import (
    get_company,
    get_company_jobs,
    get_job_applications,
)


# ============================================================
# PAGE STYLING
# ============================================================

def style_company_dashboard():
    """
    CareerIQ company recruitment dashboard styling.

    Custom HTML/CSS is rendered with st.html().
    """

    st.html(
        """
        <style>

        /* ==================================================
           GLOBAL
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
                    rgba(108,99,255,.08),
                    transparent 25%
                ),
                linear-gradient(
                    180deg,
                    #faf9f2 0%,
                    #f5f7f7 100%
                );
        }

        .block-container {
            max-width: 1200px;
            padding-top: 1.6rem;
            padding-bottom: 3.5rem;
        }

        /* ==================================================
           HERO
           ================================================== */

        .company-hero {
            position: relative;
            overflow: hidden;

            padding: 32px 36px;

            border-radius: 28px;

            background:
                radial-gradient(
                    circle at 92% 8%,
                    rgba(17,169,181,.20),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 6% 95%,
                    rgba(108,99,255,.13),
                    transparent 30%
                ),
                #ffffff;

            border: 1px solid rgba(7,59,92,.10);

            box-shadow:
                0 18px 55px rgba(7,59,92,.08);
        }

        .hero-badge {
            display: inline-flex;

            padding: 7px 12px;

            border-radius: 999px;

            background: rgba(17,169,181,.09);

            border: 1px solid rgba(17,169,181,.15);

            color: #087789;

            font-size: 10px;

            font-weight: 850;

            letter-spacing: .7px;

            text-transform: uppercase;
        }

        .hero-title {
            margin-top: 15px;

            color: #073b5c;

            font-size: 35px;

            line-height: 1.08;

            font-weight: 900;

            letter-spacing: -1.3px;
        }

        .hero-subtitle {
            margin-top: 8px;

            color: #627586;

            font-size: 12px;

            line-height: 1.7;
        }

        .hero-location {
            margin-top: 17px;

            color: #557080;

            font-size: 11px;

            font-weight: 650;
        }

        /* ==================================================
           SECTION HEADERS
           ================================================== */

        .section-title {
            margin-top: 29px;

            color: #073b5c;

            font-size: 21px;

            font-weight: 850;

            letter-spacing: -.35px;
        }

        .section-subtitle {
            margin-top: 4px;

            color: #718096;

            font-size: 11px;

            line-height: 1.6;
        }

        /* ==================================================
           STAT CARDS
           ================================================== */

        .stat-card {
            min-height: 125px;

            padding: 19px;

            border-radius: 18px;

            background: rgba(255,255,255,.92);

            border: 1px solid rgba(7,59,92,.09);

            box-shadow:
                0 8px 28px rgba(7,59,92,.05);
        }

        .stat-icon {
            width: 35px;
            height: 35px;

            display: flex;

            align-items: center;
            justify-content: center;

            border-radius: 10px;

            background: #f1f8f8;

            font-size: 16px;
        }

        .stat-label {
            margin-top: 12px;

            color: #718096;

            font-size: 10px;

            font-weight: 750;

            text-transform: uppercase;

            letter-spacing: .6px;
        }

        .stat-value {
            margin-top: 4px;

            color: #073b5c;

            font-size: 27px;

            font-weight: 900;

            letter-spacing: -1px;
        }

        /* ==================================================
           QUICK ACTION CARD
           ================================================== */

        .action-card {
            min-height: 105px;

            padding: 18px;

            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    rgba(17,169,181,.07),
                    rgba(108,99,255,.05)
                );

            border: 1px solid rgba(17,169,181,.12);
        }

        .action-icon {
            font-size: 21px;
        }

        .action-title {
            margin-top: 8px;

            color: #073b5c;

            font-size: 13px;

            font-weight: 820;
        }

        .action-text {
            margin-top: 4px;

            color: #718096;

            font-size: 10px;

            line-height: 1.5;
        }

        /* ==================================================
           JOB CARD
           ================================================== */

        .job-card {
            padding: 19px;

            margin-bottom: 11px;

            border-radius: 18px;

            background: rgba(255,255,255,.93);

            border: 1px solid rgba(7,59,92,.09);

            box-shadow:
                0 7px 25px rgba(7,59,92,.045);
        }

        .job-header {
            display: flex;

            align-items: flex-start;

            justify-content: space-between;

            gap: 15px;
        }

        .job-title {
            color: #073b5c;

            font-size: 15px;

            font-weight: 850;
        }

        .job-meta {
            margin-top: 8px;

            color: #718096;

            font-size: 10px;

            line-height: 1.7;
        }

        .job-status {
            padding: 5px 9px;

            border-radius: 999px;

            font-size: 9px;

            font-weight: 850;

            text-transform: uppercase;
        }

        .status-active {
            color: #087b61;

            background: rgba(16,185,129,.10);
        }

        .status-draft {
            color: #a26700;

            background: rgba(245,158,11,.11);
        }

        .status-closed {
            color: #c23c3c;

            background: rgba(239,68,68,.10);
        }

        /* ==================================================
           APPLICATION CARD
           ================================================== */

        .application-card {
            padding: 16px 18px;

            margin-bottom: 9px;

            border-radius: 16px;

            background: rgba(255,255,255,.91);

            border: 1px solid rgba(7,59,92,.08);
        }

        .application-name {
            color: #073b5c;

            font-size: 13px;

            font-weight: 820;
        }

        .application-meta {
            margin-top: 5px;

            color: #718096;

            font-size: 10px;
        }

        .match-pill {
            padding: 6px 10px;

            border-radius: 999px;

            color: #087789;

            background: rgba(17,169,181,.09);

            font-size: 10px;

            font-weight: 850;
        }

        /* ==================================================
           COMPANY INFO
           ================================================== */

        .company-info-card {
            min-height: 145px;

            padding: 19px;

            border-radius: 18px;

            background: rgba(255,255,255,.92);

            border: 1px solid rgba(7,59,92,.09);

            box-shadow:
                0 7px 25px rgba(7,59,92,.045);
        }

        .info-label {
            color: #718096;

            font-size: 9px;

            font-weight: 750;

            text-transform: uppercase;

            letter-spacing: .6px;
        }

        .info-value {
            margin-top: 4px;

            color: #073b5c;

            font-size: 13px;

            font-weight: 780;

            word-break: break-word;
        }

        /* ==================================================
           EMPTY STATE
           ================================================== */

        .empty-card {
            padding: 35px 20px;

            border-radius: 20px;

            background: rgba(255,255,255,.88);

            border: 1px dashed rgba(7,59,92,.16);

            text-align: center;
        }

        .empty-icon {
            font-size: 38px;
        }

        .empty-title {
            margin-top: 10px;

            color: #073b5c;

            font-size: 17px;

            font-weight: 850;
        }

        .empty-text {
            margin-top: 5px;

            color: #718096;

            font-size: 11px;
        }

        /* ==================================================
           FOOTER
           ================================================== */

        .dashboard-footer {
            margin-top: 34px;

            padding-bottom: 10px;

            text-align: center;

            color: #9aa7b2;

            font-size: 10px;
        }

        .stButton > button {
            min-height: 43px;

            border-radius: 12px;

            font-weight: 760;
        }

        </style>
        """
    )


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    """
    Safely convert a value into HTML-safe text.
    """

    if value is None:
        return "Not specified"

    value = str(value).strip()

    if not value:
        return "Not specified"

    return html.escape(value)


def render_html(content):
    """
    Render custom HTML using Streamlit's native HTML renderer.
    """

    st.html(content)


def get_status_counts(jobs):
    """
    Count jobs by status.
    """

    active = 0
    draft = 0
    closed = 0

    for job in jobs:

        status = str(
            getattr(job, "status", "")
        ).lower()

        if status == "active":
            active += 1

        elif status == "draft":
            draft += 1

        elif status == "closed":
            closed += 1

    return active, draft, closed


def calculate_average_match(applications):
    """
    Calculate average application match score.
    """

    scores = []

    for application in applications:

        score = getattr(
            application,
            "match_score",
            None
        )

        if score is not None:

            try:
                scores.append(
                    float(score)
                )

            except (TypeError, ValueError):
                pass

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def get_status_class(status):
    """
    Return the CSS class for a job status.
    """

    status = str(status).lower()

    if status == "active":
        return "status-active"

    if status == "draft":
        return "status-draft"

    if status == "closed":
        return "status-closed"

    return "status-draft"


# ============================================================
# STAT CARD
# ============================================================

def show_stat_card(
    column,
    icon,
    label,
    value
):
    """
    Render one dashboard statistic.
    """

    with column:

        render_html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    {icon}
                </div>

                <div class="stat-label">
                    {label}
                </div>

                <div class="stat-value">
                    {value}
                </div>

            </div>
            """
        )


# ============================================================
# COMPANY DASHBOARD
# ============================================================

def company_dashboard():
    """
    Main CareerIQ company recruitment dashboard.
    """

    style_company_dashboard()

    # ========================================================
    # COMPANY
    # ========================================================

    company_id = st.session_state.get(
        "company_id"
    )

    if not company_id:

        render_html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    🏢
                </div>

                <div class="empty-title">
                    No Company Selected
                </div>

                <div class="empty-text">
                    Select your company profile to open
                    the recruitment dashboard.
                </div>

            </div>
            """
        )

        if st.button(
            "🏢 Select Company",
            use_container_width=True,
            type="primary"
        ):

            st.session_state["page"] = (
                "company_selector"
            )

            st.rerun()

        return

    company = get_company(
        company_id
    )

    if company is None:

        st.error(
            "Company information could not be found."
        )

        if st.button(
            "🏠 Back to Home",
            use_container_width=True
        ):

            st.session_state["page"] = "home"

            st.rerun()

        return

    # ========================================================
    # JOBS
    # ========================================================

    jobs = get_company_jobs(
        company_id
    )

    # ========================================================
    # APPLICATIONS
    # ========================================================

    all_applications = []

    for job in jobs:

        job_id = getattr(
            job,
            "id",
            None
        )

        if job_id:

            applications = get_job_applications(
                job_id
            )

            all_applications.extend(
                applications
            )

    # ========================================================
    # STATISTICS
    # ========================================================

    total_jobs = len(jobs)

    active_jobs, draft_jobs, closed_jobs = (
        get_status_counts(jobs)
    )

    total_applications = len(
        all_applications
    )

    average_match = calculate_average_match(
        all_applications
    )

    # ========================================================
    # HERO
    # ========================================================

    company_name = safe_text(
        company.company_name
    )

    company_location = safe_text(
        company.location
    )

    render_html(
        f"""
        <div class="company-hero">

            <div class="hero-badge">
                🏢 Company Workspace
            </div>

            <div class="hero-title">
                {company_name}
            </div>

            <div class="hero-subtitle">
                Recruitment intelligence dashboard for
                managing opportunities and reviewing candidates.
            </div>

            <div class="hero-location">
                📍 {company_location}
            </div>

        </div>
        """
    )

    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    render_html(
        """
        <div class="section-title">
            ⚡ Quick Actions
        </div>

        <div class="section-subtitle">
            Manage your recruitment workflow from one place.
        </div>
        """
    )

    action1, action2, action3 = st.columns(
        3,
        gap="medium"
    )

    with action1:

        render_html(
            """
            <div class="action-card">

                <div class="action-icon">
                    ➕
                </div>

                <div class="action-title">
                    Create New Job
                </div>

                <div class="action-text">
                    Publish a new opportunity and define
                    your candidate requirements.
                </div>

            </div>
            """
        )

        if st.button(
            "Create Job →",
            use_container_width=True,
            type="primary",
            key="dashboard_create_job"
        ):

            st.session_state["page"] = (
                "create_job"
            )

            st.rerun()

    with action2:

        render_html(
            """
            <div class="action-card">

                <div class="action-icon">
                    💼
                </div>

                <div class="action-title">
                    Manage Jobs
                </div>

                <div class="action-text">
                    Review, edit, close, and manage
                    your published opportunities.
                </div>

            </div>
            """
        )

        if st.button(
            "Manage Jobs →",
            use_container_width=True,
            key="dashboard_manage_jobs"
        ):

            st.session_state["page"] = (
                "job_management"
            )

            st.rerun()

    with action3:

        render_html(
            """
            <div class="action-card">

                <div class="action-icon">
                    🏢
                </div>

                <div class="action-title">
                    Company Profile
                </div>

                <div class="action-text">
                    Update your company information and
                    recruitment profile.
                </div>

            </div>
            """
        )

        if st.button(
            "Open Profile →",
            use_container_width=True,
            key="dashboard_company_profile"
        ):

            st.session_state["page"] = (
                "company_profile"
            )

            st.rerun()

    # ========================================================
    # RECRUITMENT OVERVIEW
    # ========================================================

    render_html(
        """
        <div class="section-title">
            📊 Recruitment Overview
        </div>

        <div class="section-subtitle">
            A live summary of your jobs and candidate activity.
        </div>
        """
    )

    col1, col2, col3, col4 = st.columns(
        4,
        gap="medium"
    )

    show_stat_card(
        col1,
        "💼",
        "Total Jobs",
        total_jobs
    )

    show_stat_card(
        col2,
        "🟢",
        "Active Jobs",
        active_jobs
    )

    show_stat_card(
        col3,
        "👥",
        "Applications",
        total_applications
    )

    show_stat_card(
        col4,
        "🎯",
        "Average Match",
        f"{average_match * 100:.1f}%"
    )

    # ========================================================
    # JOB STATUS
    # ========================================================

    render_html(
        """
        <div class="section-title">
            📌 Job Status
        </div>

        <div class="section-subtitle">
            Current state of your recruitment opportunities.
        </div>
        """
    )

    status1, status2, status3 = st.columns(
        3,
        gap="medium"
    )

    with status1:

        render_html(
            f"""
            <div class="stat-card">

                <div class="stat-label">
                    🟢 Active
                </div>

                <div class="stat-value">
                    {active_jobs}
                </div>

            </div>
            """
        )

    with status2:

        render_html(
            f"""
            <div class="stat-card">

                <div class="stat-label">
                    🟡 Draft
                </div>

                <div class="stat-value">
                    {draft_jobs}
                </div>

            </div>
            """
        )

    with status3:

        render_html(
            f"""
            <div class="stat-card">

                <div class="stat-label">
                    🔴 Closed
                </div>

                <div class="stat-value">
                    {closed_jobs}
                </div>

            </div>
            """
        )

    # ========================================================
    # YOUR JOBS
    # ========================================================

    render_html(
        """
        <div class="section-title">
            💼 Your Jobs
        </div>

        <div class="section-subtitle">
            Opportunities currently connected to your company.
        </div>
        """
    )

    if not jobs:

        render_html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    💼
                </div>

                <div class="empty-title">
                    No jobs created yet
                </div>

                <div class="empty-text">
                    Create your first opportunity to start
                    receiving relevant candidates.
                </div>

            </div>
            """
        )

        if st.button(
            "➕ Create Your First Job",
            use_container_width=True,
            type="primary",
            key="dashboard_first_job"
        ):

            st.session_state["page"] = (
                "create_job"
            )

            st.rerun()

    else:

        for job in jobs:

            title = safe_text(
                getattr(
                    job,
                    "title",
                    None
                )
            )

            location = safe_text(
                getattr(
                    job,
                    "location",
                    None
                )
            )

            employment_type = safe_text(
                getattr(
                    job,
                    "employment_type",
                    None
                )
            )

            status = safe_text(
                getattr(
                    job,
                    "status",
                    None
                )
            )

            experience = getattr(
                job,
                "experience_required",
                0
            )

            status_class = get_status_class(
                status
            )

            render_html(
                f"""
                <div class="job-card">

                    <div class="job-header">

                        <div>

                            <div class="job-title">
                                {title}
                            </div>

                            <div class="job-meta">
                                📍 {location}
                                &nbsp; • &nbsp;
                                💼 {employment_type}
                                &nbsp; • &nbsp;
                                🎯 {experience} years experience
                            </div>

                        </div>

                        <div class="job-status {status_class}">
                            {status}
                        </div>

                    </div>

                </div>
                """
            )

    # ========================================================
    # COMPANY OVERVIEW
    # ========================================================

    render_html(
        """
        <div class="section-title">
            🏢 Company Overview
        </div>

        <div class="section-subtitle">
            Key information connected to your company profile.
        </div>
        """
    )

    overview1, overview2 = st.columns(
        2,
        gap="medium"
    )

    with overview1:

        industry = safe_text(
            getattr(
                company,
                "industry",
                None
            )
        )

        location = safe_text(
            getattr(
                company,
                "location",
                None
            )
        )

        render_html(
            f"""
            <div class="company-info-card">

                <div class="info-label">
                    Industry
                </div>

                <div class="info-value">
                    {industry}
                </div>

                <div style="height:20px;"></div>

                <div class="info-label">
                    Location
                </div>

                <div class="info-value">
                    {location}
                </div>

            </div>
            """
        )

    with overview2:

        website = safe_text(
            getattr(
                company,
                "website",
                None
            )
        )

        email = safe_text(
            getattr(
                company,
                "email",
                None
            )
        )

        render_html(
            f"""
            <div class="company-info-card">

                <div class="info-label">
                    Website
                </div>

                <div class="info-value">
                    {website}
                </div>

                <div style="height:20px;"></div>

                <div class="info-label">
                    Recruitment Email
                </div>

                <div class="info-value">
                    {email}
                </div>

            </div>
            """
        )

    # ========================================================
    # RECENT APPLICATIONS
    # ========================================================

    render_html(
        """
        <div class="section-title">
            👥 Recent Applications
        </div>

        <div class="section-subtitle">
            Latest candidates who applied to your opportunities.
        </div>
        """
    )

    if not all_applications:

        render_html(
            """
            <div class="empty-card">

                <div class="empty-icon">
                    👥
                </div>

                <div class="empty-title">
                    No applications yet
                </div>

                <div class="empty-text">
                    Applications will appear here when students
                    apply to your active jobs.
                </div>

            </div>
            """
        )

    else:

        for index, application in enumerate(
            all_applications[:10]
        ):

            student_id = getattr(
                application,
                "student_id",
                "Unknown"
            )

            match_score = getattr(
                application,
                "match_score",
                None
            )

            status = getattr(
                application,
                "application_status",
                "applied"
            )

            if match_score is not None:

                try:

                    match_text = (
                        f"{float(match_score) * 100:.1f}%"
                    )

                except (TypeError, ValueError):

                    match_text = "Not calculated"

            else:

                match_text = "Not calculated"

            render_html(
                f"""
                <div class="application-card">

                    <div class="job-header">

                        <div>

                            <div class="application-name">
                                👤 Student #{safe_text(student_id)}
                            </div>

                            <div class="application-meta">
                                📌 Status:
                                {safe_text(status)}
                            </div>

                        </div>

                        <div class="match-pill">
                            🎯 {match_text} Match
                        </div>

                    </div>

                </div>
                """
            )

    # ========================================================
    # FOOTER ACTIONS
    # ========================================================

    st.divider()

    col1, col2 = st.columns(
        2,
        gap="medium"
    )

    with col1:

        if st.button(
            "💼 Manage Jobs",
            use_container_width=True,
            key="dashboard_footer_manage"
        ):

            st.session_state["page"] = (
                "job_management"
            )

            st.rerun()

    with col2:

        if st.button(
            "🏠 Back to Home",
            use_container_width=True,
            key="dashboard_footer_home"
        ):

            st.session_state["page"] = "home"

            st.rerun()

    render_html(
        """
        <div class="dashboard-footer">
            CareerIQ • AI-powered recruitment intelligence
        </div>
        """
    )
