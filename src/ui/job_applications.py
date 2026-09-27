
import streamlit as st

from src.auth.auth_repository import get_user_company
from src.database.repositories import (
    get_job,
    get_job_applications,
    update_application_status,
)


# ============================================================
# GLOBAL UI
# ============================================================

def apply_applications_style():
    st.html("""
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 5%, rgba(99,102,241,.16), transparent 28%),
                radial-gradient(circle at 92% 12%, rgba(168,85,247,.13), transparent 30%),
                radial-gradient(circle at 50% 100%, rgba(14,165,233,.08), transparent 32%),
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
            transition: .2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            border-color: rgba(139,92,246,.55);
            background: rgba(139,92,246,.15);
        }

        .stSelectbox div[data-baseweb="select"] {
            background: rgba(255,255,255,.045) !important;
            border: 1px solid rgba(255,255,255,.10) !important;
            border-radius: 12px !important;
        }

        hr {
            border-color: rgba(255,255,255,.08);
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.075);
            border-radius: 16px;
            padding: 14px 16px;
        }
    </style>
    """)


def render_html(content: str):
    st.html(content)


# ============================================================
# HELPERS
# ============================================================

def status_meta(status):
    status = (status or "applied").strip().lower()

    mapping = {
        "applied": ("APPLIED", "#60a5fa", "rgba(59,130,246,.14)", "●"),
        "under review": ("UNDER REVIEW", "#c4b5fd", "rgba(139,92,246,.14)", "◉"),
        "shortlisted": ("SHORTLISTED", "#86efac", "rgba(34,197,94,.14)", "✓"),
        "interview": ("INTERVIEW", "#fde68a", "rgba(245,158,11,.14)", "◆"),
        "selected": ("SELECTED", "#67e8f9", "rgba(6,182,212,.14)", "★"),
        "rejected": ("REJECTED", "#fca5a5", "rgba(239,68,68,.14)", "✕"),
        "withdrawn": ("WITHDRAWN", "#cbd5e1", "rgba(148,163,184,.14)", "↩"),
    }

    return mapping.get(
        status,
        (status.upper(), "#cbd5e1", "rgba(148,163,184,.14)", "●"),
    )


def get_status_badge(status):
    label, color, background, icon = status_meta(status)

    return f"""
    <span style="
        display:inline-flex;
        align-items:center;
        gap:7px;
        padding:7px 11px;
        border-radius:999px;
        background:{background};
        border:1px solid {color}38;
        color:{color};
        font-size:11px;
        font-weight:800;
        letter-spacing:.04em;
        white-space:nowrap;
    ">
        <span>{icon}</span>{html.escape(label)}
    </span>
    """


def score_meta(match_score):
    if match_score is None:
        return "Not calculated", "#94a3b8", 0

    try:
        percentage = float(match_score) * 100
    except (TypeError, ValueError):
        return "Not calculated", "#94a3b8", 0

    percentage = max(0, min(100, percentage))

    if percentage >= 80:
        color = "#4ade80"
    elif percentage >= 60:
        color = "#fbbf24"
    else:
        color = "#94a3b8"

    return f"{percentage:.1f}%", color, percentage


# ============================================================
# HERO
# ============================================================

def render_hero(job, total):
    title = html.escape(job.title or "Job")
    status = (job.status or "active").lower()

    if status == "active":
        status_color = "#4ade80"
        status_bg = "rgba(34,197,94,.13)"
    elif status == "paused":
        status_color = "#fbbf24"
        status_bg = "rgba(245,158,11,.13)"
    else:
        status_color = "#94a3b8"
        status_bg = "rgba(148,163,184,.13)"

    render_html(f"""
    <div style="
        position:relative;
        overflow:hidden;
        padding:34px;
        margin-bottom:22px;
        border-radius:26px;
        background:
            linear-gradient(135deg,
                rgba(99,102,241,.20),
                rgba(168,85,247,.11) 48%,
                rgba(15,23,42,.94));
        border:1px solid rgba(255,255,255,.095);
        box-shadow:0 28px 70px rgba(0,0,0,.30);
    ">
        <div style="
            position:absolute;
            width:260px;
            height:260px;
            right:-90px;
            top:-130px;
            border-radius:50%;
            background:rgba(139,92,246,.17);
            filter:blur(45px);
        "></div>

        <div style="position:relative;z-index:2;">
            <div style="
                display:flex;
                align-items:flex-start;
                justify-content:space-between;
                gap:20px;
                flex-wrap:wrap;
            ">
                <div>
                    <div style="
                        display:inline-flex;
                        align-items:center;
                        gap:7px;
                        padding:7px 12px;
                        border-radius:999px;
                        background:{status_bg};
                        border:1px solid {status_color}45;
                        color:{status_color};
                        font-size:11px;
                        font-weight:800;
                        letter-spacing:.05em;
                        margin-bottom:14px;
                    ">
                        ● {html.escape(status.upper())}
                    </div>

                    <div style="
                        color:#fff;
                        font-size:34px;
                        line-height:1.15;
                        font-weight:850;
                        letter-spacing:-.02em;
                    ">
                        Candidate Applications
                    </div>

                    <div style="
                        margin-top:9px;
                        color:#cbd5e1;
                        font-size:16px;
                    ">
                        {title}
                    </div>
                </div>

                <div style="
                    min-width:150px;
                    padding:17px 20px;
                    border-radius:18px;
                    background:rgba(255,255,255,.045);
                    border:1px solid rgba(255,255,255,.08);
                    text-align:center;
                ">
                    <div style="
                        color:#94a3b8;
                        font-size:11px;
                        font-weight:700;
                        letter-spacing:.06em;
                    ">
                        TOTAL APPLICANTS
                    </div>
                    <div style="
                        margin-top:5px;
                        color:#fff;
                        font-size:30px;
                        font-weight:850;
                    ">
                        {total}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)


# ============================================================
# APPLICATION CARD
# ============================================================

def render_application_card(application, index):
    student_id = html.escape(str(application.student_id))
    status = application.application_status or "applied"

    score_text, score_color, percentage = score_meta(application.match_score)

    if percentage >= 80:
        score_label = "Strong match"
    elif percentage >= 60:
        score_label = "Moderate match"
    elif application.match_score is None:
        score_label = "Awaiting analysis"
    else:
        score_label = "Needs review"

    status_badge = get_status_badge(status)

    render_html(f"""
    <div style="
        padding:22px;
        margin:0 0 12px 0;
        border-radius:20px;
        background:
            linear-gradient(145deg,
                rgba(15,23,42,.86),
                rgba(30,41,59,.62));
        border:1px solid rgba(255,255,255,.075);
        box-shadow:0 16px 42px rgba(0,0,0,.17);
    ">
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:22px;
            flex-wrap:wrap;
        ">
            <div style="min-width:240px;">
                <div style="
                    color:#64748b;
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:.08em;
                    margin-bottom:8px;
                ">
                    APPLICANT #{index}
                </div>

                <div style="
                    color:#fff;
                    font-size:19px;
                    font-weight:800;
                    margin-bottom:10px;
                ">
                    Student ID: {student_id}
                </div>

                {status_badge}
            </div>

            <div style="
                width:155px;
                padding:15px 14px;
                border-radius:16px;
                background:rgba(255,255,255,.04);
                border:1px solid rgba(255,255,255,.07);
                text-align:center;
            ">
                <div style="
                    color:#94a3b8;
                    font-size:10px;
                    font-weight:800;
                    letter-spacing:.06em;
                ">
                    AI MATCH SCORE
                </div>

                <div style="
                    color:{score_color};
                    font-size:25px;
                    font-weight:850;
                    margin-top:3px;
                ">
                    {html.escape(score_text)}
                </div>

                <div style="
                    color:#64748b;
                    font-size:10px;
                    margin-top:2px;
                ">
                    {html.escape(score_label)}
                </div>
            </div>
        </div>
    </div>
    """)


# ============================================================
# MAIN PAGE
# ============================================================

def job_applications_page():
    apply_applications_style()

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
    # JOB
    # --------------------------------------------------------

    job_id = st.session_state.get("selected_job_id")

    if not job_id:
        st.warning("No job selected.")
        st.session_state["page"] = "job_management"
        st.rerun()

    job = get_job(job_id)

    if not job:
        st.error("Job not found.")
        st.session_state["page"] = "job_management"
        st.rerun()

    # --------------------------------------------------------
    # SECURITY
    # --------------------------------------------------------

    if job.company_id != company.id:
        st.error("You are not authorized to view these applications.")

        if st.button("← Back to Job Management", use_container_width=True):
            st.session_state["page"] = "job_management"
            st.rerun()

        return

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------

    applications = get_job_applications(job.id)

    total = len(applications)

    counts = {}
    for application in applications:
        key = (application.application_status or "applied").lower()
        counts[key] = counts.get(key, 0) + 1

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    render_hero(job, total)

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    nav1, nav2 = st.columns(2)

    with nav1:
        if st.button(
            "← Back to Job Details",
            use_container_width=True,
            key="back_job_details",
        ):
            st.session_state["selected_job_id"] = job.id
            st.session_state["page"] = "job_details"
            st.rerun()

    with nav2:
        if st.button(
            "📋 Back to Job Management",
            use_container_width=True,
            key="back_job_management",
        ):
            st.session_state["page"] = "job_management"
            st.rerun()

    # --------------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------------

    if not applications:
        render_html("""
        <div style="
            margin-top:25px;
            padding:65px 30px;
            text-align:center;
            border-radius:24px;
            background:
                linear-gradient(145deg,
                    rgba(15,23,42,.82),
                    rgba(30,41,59,.58));
            border:1px solid rgba(255,255,255,.075);
            box-shadow:0 20px 55px rgba(0,0,0,.20);
        ">
            <div style="font-size:54px;margin-bottom:14px;">📭</div>

            <div style="
                color:#fff;
                font-size:25px;
                font-weight:850;
                margin-bottom:9px;
            ">
                No Applications Yet
            </div>

            <div style="
                color:#94a3b8;
                font-size:15px;
            ">
                Candidate applications for this job will appear here.
            </div>
        </div>
        """)
        return

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    st.html("""
    <div style="
        margin-top:28px;
        margin-bottom:14px;
        color:#fff;
        font-size:22px;
        font-weight:800;
    ">
        Application Overview
    </div>
    """)

    overview = [
        ("Total", total),
        ("Applied", counts.get("applied", 0)),
        ("Shortlisted", counts.get("shortlisted", 0)),
        ("Rejected", counts.get("rejected", 0)),
    ]

    cols = st.columns(4)

    for col, (label, value) in zip(cols, overview):
        with col:
            st.metric(label, value)

    # --------------------------------------------------------
    # FILTER / SORT
    # --------------------------------------------------------

    st.html("""
    <div style="
        margin-top:28px;
        margin-bottom:8px;
        color:#fff;
        font-size:22px;
        font-weight:800;
    ">
        Candidates
    </div>
    """)

    filter_col, sort_col = st.columns([1, 1])

    status_options = [
        "All",
        "Applied",
        "Under Review",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected",
        "Withdrawn",
    ]

    with filter_col:
        filter_status = st.selectbox(
            "Filter applications",
            status_options,
            key=f"application_filter_{job.id}",
        )

    with sort_col:
        sort_by = st.selectbox(
            "Sort candidates",
            ["Match Score", "Newest / Database Order", "Status"],
            key=f"application_sort_{job.id}",
        )

    filtered_applications = list(applications)

    if filter_status != "All":
        filtered_applications = [
            application
            for application in filtered_applications
            if (application.application_status or "applied").lower()
            == filter_status.lower()
        ]

    if sort_by == "Match Score":
        filtered_applications.sort(
            key=lambda application: (
                -1 if application.match_score is None
                else float(application.match_score)
            ),
            reverse=True,
        )
    elif sort_by == "Status":
        filtered_applications.sort(
            key=lambda application: (
                application.application_status or "applied"
            ).lower()
        )

    st.html(f"""
    <div style="
        margin:18px 0 12px 0;
        color:#64748b;
        font-size:12px;
        font-weight:700;
    ">
        Showing {len(filtered_applications)} of {total} applications
    </div>
    """)

    # --------------------------------------------------------
    # CANDIDATES
    # --------------------------------------------------------

    if not filtered_applications:
        st.info("No applications match the selected filter.")
        return

    for index, application in enumerate(filtered_applications, start=1):
        render_application_card(application, index)

        current_status = (
            application.application_status or "applied"
        ).lower()

        status_options_for_update = [
            "Applied",
            "Under Review",
            "Shortlisted",
            "Interview",
            "Selected",
            "Rejected",
            "Withdrawn",
        ]

        current_display = current_status.title()

        if current_display not in status_options_for_update:
            current_display = "Applied"

        action_col, save_col = st.columns([3, 1])

        with action_col:
            selected_status = st.selectbox(
                "Application status",
                status_options_for_update,
                index=status_options_for_update.index(current_display),
                key=f"status_{application.id}",
                label_visibility="collapsed",
            )

        with save_col:
            if st.button(
                "Save Status",
                key=f"update_status_{application.id}",
                use_container_width=True,
                disabled=selected_status.lower() == current_status,
            ):
                success = update_application_status(
                    application.id,
                    selected_status.lower(),
                )

                if success:
                    st.success("Application status updated.")
                    st.rerun()
                else:
                    st.error("Could not update application status.")

        st.html('<div style="height:10px;"></div>')


# ============================================================
# ENTRY POINT
# ============================================================

def job_applications():
    job_applications_page()
