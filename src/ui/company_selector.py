
import html
import streamlit as st

from src.auth.auth_repository import get_user_company

from src.database.repositories import (
    get_company_jobs,
    get_job_applications,
)


# ============================================================
# CAREERIQ — COMPANY SELECTOR
# Premium production UI
# ============================================================

def style_company_selector():
    st.html(
        """
        <style>

        /* ========================================================
           GLOBAL
        ======================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at 5% 0%,
                    rgba(34, 211, 238, 0.08),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 95% 5%,
                    rgba(99, 102, 241, 0.09),
                    transparent 30%
                ),
                #f7f9fc;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.6rem;
            padding-bottom: 3.5rem;
        }

        /* ========================================================
           HERO
        ======================================================== */

        .ciq-hero {
            position: relative;
            overflow: hidden;
            padding: 42px 44px;
            margin-bottom: 26px;
            border-radius: 28px;

            background:
                linear-gradient(
                    135deg,
                    #07111f 0%,
                    #101d3d 48%,
                    #30276b 100%
                );

            box-shadow:
                0 26px 70px rgba(15, 23, 42, 0.20);
        }

        .ciq-hero::before {
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -120px;
            top: -190px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle,
                    rgba(34, 211, 238, 0.30),
                    transparent 68%
                );
        }

        .ciq-hero::after {
            content: "";
            position: absolute;
            width: 290px;
            height: 290px;
            left: -150px;
            bottom: -210px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle,
                    rgba(129, 140, 248, 0.28),
                    transparent 70%
                );
        }

        .ciq-hero-content {
            position: relative;
            z-index: 2;
        }

        .ciq-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            padding: 7px 12px;
            border-radius: 999px;

            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.13);

            color: #a5f3fc;
            font-size: 10px;
            font-weight: 850;
            letter-spacing: .09em;
        }

        .ciq-title {
            margin-top: 16px;
            color: #fff;
            font-size: 40px;
            line-height: 1.08;
            font-weight: 850;
            letter-spacing: -.035em;
        }

        .ciq-subtitle {
            max-width: 720px;
            margin-top: 11px;
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.72;
        }

        .ciq-account {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            padding: 8px 12px;
            border-radius: 11px;

            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.10);

            color: #bfdbfe;
            font-size: 11px;
            font-weight: 700;
        }

        /* ========================================================
           SECTION
        ======================================================== */

        .ciq-section-title {
            color: #0f172a;
            font-size: 21px;
            font-weight: 850;
            letter-spacing: -.02em;
        }

        .ciq-section-subtitle {
            margin-top: 4px;
            margin-bottom: 18px;
            color: #64748b;
            font-size: 12px;
            line-height: 1.6;
        }

        /* ========================================================
           COMPANY CARD
        ======================================================== */

        .ciq-company-card {
            position: relative;
            overflow: hidden;
            padding: 24px;
            min-height: 225px;
            border-radius: 23px;

            background: rgba(255,255,255,.94);
            border: 1px solid #e2e8f0;

            box-shadow:
                0 14px 42px rgba(15,23,42,.07);
        }

        .ciq-company-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;

            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #7c3aed,
                    #06b6d4
                );
        }

        .ciq-logo {
            width: 62px;
            height: 62px;
            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 17px;

            background:
                linear-gradient(
                    135deg,
                    #eff6ff,
                    #eef2ff
                );

            border: 1px solid #dbeafe;
            font-size: 29px;
        }

        .ciq-company-name {
            margin-top: 15px;
            color: #0f172a;
            font-size: 22px;
            font-weight: 850;
            letter-spacing: -.025em;
        }

        .ciq-company-meta {
            margin-top: 8px;
            color: #64748b;
            font-size: 12px;
            line-height: 1.75;
        }

        .ciq-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 15px;
            padding: 6px 10px;
            border-radius: 999px;

            background: #ecfdf5;
            border: 1px solid #bbf7d0;
            color: #047857;

            font-size: 10px;
            font-weight: 850;
        }

        /* ========================================================
           STAT CARDS
        ======================================================== */

        .ciq-stat {
            padding: 17px 18px;
            border-radius: 17px;

            background: rgba(255,255,255,.90);
            border: 1px solid #e5e7eb;

            box-shadow:
                0 8px 24px rgba(15,23,42,.045);
        }

        .ciq-stat-icon {
            font-size: 17px;
        }

        .ciq-stat-value {
            margin-top: 8px;
            color: #0f172a;
            font-size: 25px;
            font-weight: 850;
            line-height: 1;
        }

        .ciq-stat-label {
            margin-top: 6px;
            color: #64748b;
            font-size: 10px;
            font-weight: 700;
        }

        /* ========================================================
           RIGHT SIDE INFO
        ======================================================== */

        .ciq-info-card {
            padding: 21px;
            border-radius: 20px;

            background: #fff;
            border: 1px solid #e2e8f0;

            box-shadow:
                0 10px 30px rgba(15,23,42,.05);
        }

        .ciq-info-title {
            color: #0f172a;
            font-size: 14px;
            font-weight: 850;
        }

        .ciq-info-text {
            margin-top: 7px;
            color: #64748b;
            font-size: 11px;
            line-height: 1.7;
        }

        .ciq-feature {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-top: 14px;
        }

        .ciq-feature-icon {
            flex: 0 0 auto;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 9px;

            background: #f1f5f9;
            color: #334155;
            font-size: 14px;
        }

        .ciq-feature-text {
            color: #475569;
            font-size: 11px;
            line-height: 1.5;
        }

        /* ========================================================
           EMPTY STATE
        ======================================================== */

        .ciq-empty {
            text-align: center;
            padding: 54px 28px;
            border-radius: 25px;

            background: rgba(255,255,255,.92);
            border: 1px solid #e2e8f0;

            box-shadow:
                0 16px 45px rgba(15,23,42,.07);
        }

        .ciq-empty-icon {
            font-size: 48px;
        }

        .ciq-empty-title {
            margin-top: 12px;
            color: #0f172a;
            font-size: 25px;
            font-weight: 850;
        }

        .ciq-empty-text {
            max-width: 600px;
            margin: 9px auto 0;
            color: #64748b;
            font-size: 12px;
            line-height: 1.7;
        }

        /* ========================================================
           SECURITY
        ======================================================== */

        .ciq-security {
            display: flex;
            gap: 11px;
            padding: 15px 17px;
            margin-top: 23px;
            border-radius: 17px;

            background:
                linear-gradient(
                    135deg,
                    #ecfdf5,
                    #f0fdf4
                );

            border: 1px solid #bbf7d0;
        }

        .ciq-security-title {
            color: #166534;
            font-size: 11px;
            font-weight: 850;
        }

        .ciq-security-text {
            margin-top: 3px;
            color: #15803d;
            font-size: 10px;
            line-height: 1.55;
        }

        /* ========================================================
           BUTTONS
        ======================================================== */

        div.stButton > button {
            min-height: 45px;
            border-radius: 12px !important;
            font-size: 12px !important;
            font-weight: 750 !important;
        }

        /* ========================================================
           RESPONSIVE
        ======================================================== */

        @media (max-width: 768px) {
            .ciq-hero {
                padding: 29px 24px;
                border-radius: 22px;
            }

            .ciq-title {
                font-size: 30px;
            }
        }

        </style>
        """
    )


# ============================================================
# LOGOUT
# ============================================================

def logout_user():

    keys = [
        "logged_in",
        "user_id",
        "user_email",
        "user_role",
        "company_id",
        "company_profile",
        "company_saved",
        "last_created_job_id",
    ]

    for key in keys:
        st.session_state.pop(key, None)

    st.session_state["page"] = "home"
    st.rerun()


# ============================================================
# HERO
# ============================================================

def _hero(email):

    safe_email = html.escape(
        email or "Authenticated company account"
    )

    st.html(
        f"""
        <div class="ciq-hero">
            <div class="ciq-hero-content">

                <div class="ciq-eyebrow">
                    🏢 CAREERIQ • COMPANY WORKSPACE
                </div>

                <div class="ciq-title">
                    Welcome back 👋
                </div>

                <div class="ciq-subtitle">
                    Manage your company, publish opportunities,
                    discover qualified candidates and run your
                    hiring workflow from one intelligent workspace.
                </div>

                <div class="ciq-account">
                    🔐 {safe_email}
                </div>

            </div>
        </div>
        """
    )


# ============================================================
# COMPANY CARD
# ============================================================

def _company_card(company):

    name = html.escape(
        company.get("company_name", "Your Company")
    )

    location = html.escape(
        company.get("location", "Location not specified")
    )

    industry = html.escape(
        company.get("industry", "Industry not specified")
    )

    st.html(
        f"""
        <div class="ciq-company-card">

            <div class="ciq-logo">
                🏢
            </div>

            <div class="ciq-company-name">
                {name}
            </div>

            <div class="ciq-company-meta">
                📍 {location}<br>
                💼 {industry}
            </div>

            <div class="ciq-status">
                ✓ REGISTERED & CONNECTED
            </div>

        </div>
        """
    )


# ============================================================
# STAT CARD
# ============================================================

def _stat_card(icon, value, label):

    st.html(
        f"""
        <div class="ciq-stat">

            <div class="ciq-stat-icon">
                {icon}
            </div>

            <div class="ciq-stat-value">
                {value}
            </div>

            <div class="ciq-stat-label">
                {label}
            </div>

        </div>
        """
    )


# ============================================================
# INFORMATION CARD
# ============================================================

def _info_card():

    st.html(
        """
        <div class="ciq-info-card">

            <div class="ciq-info-title">
                🚀 Your company workspace
            </div>

            <div class="ciq-info-text">
                Everything you need to move from a company
                profile to an active hiring workflow.
            </div>

            <div class="ciq-feature">
                <div class="ciq-feature-icon">📋</div>
                <div class="ciq-feature-text">
                    Publish and manage job opportunities.
                </div>
            </div>

            <div class="ciq-feature">
                <div class="ciq-feature-icon">🎯</div>
                <div class="ciq-feature-text">
                    Review AI-powered candidate matching.
                </div>
            </div>

            <div class="ciq-feature">
                <div class="ciq-feature-icon">👥</div>
                <div class="ciq-feature-text">
                    Track applications and hiring progress.
                </div>
            </div>

            <div class="ciq-feature">
                <div class="ciq-feature-icon">📊</div>
                <div class="ciq-feature-text">
                    Monitor jobs and recruitment activity.
                </div>
            </div>

        </div>
        """
    )


# ============================================================
# SECURITY CARD
# ============================================================

def _security_card():

    st.html(
        """
        <div class="ciq-security">

            <div style="font-size:17px;">
                🔒
            </div>

            <div>

                <div class="ciq-security-title">
                    Company account protected
                </div>

                <div class="ciq-security-text">
                    This account is connected to one company.
                    Your jobs, candidates and applications remain
                    associated with the correct organization.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# EMPTY STATE
# ============================================================

def _empty_state():

    st.html(
        """
        <div class="ciq-empty">

            <div class="ciq-empty-icon">
                🏢
            </div>

            <div class="ciq-empty-title">
                Create your company workspace
            </div>

            <div class="ciq-empty-text">
                Your company account is ready. Create your company
                profile to publish jobs, discover candidates and
                start managing your hiring pipeline with CareerIQ.
            </div>

        </div>
        """
    )


# ============================================================
# COMPANY SELECTOR PAGE
# ============================================================

def company_selector_page():

    style_company_selector()

    user_id = st.session_state.get("user_id")

    # ========================================================
    # AUTH CHECK
    # ========================================================

    if not user_id:

        st.error("Please login first.")

        st.session_state["page"] = "home"
        st.rerun()

        return

    email = st.session_state.get(
        "user_email",
        ""
    )

    # ========================================================
    # LOAD COMPANY
    # ========================================================

    company = get_user_company(user_id)

    # ========================================================
    # HERO
    # ========================================================

    _hero(email)

    # ========================================================
    # EXISTING COMPANY
    # ========================================================

    if company:

        st.html(
            """
            <div class="ciq-section-title">
                🏢 Your Company
            </div>

            <div class="ciq-section-subtitle">
                Your company is already registered and connected
                to this account.
            </div>
            """
        )

        left, right = st.columns(
            [1.45, 1],
            gap="large"
        )

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        with left:

            _company_card(company)

            # ------------------------------------------------
            # LOAD STATISTICS
            # ------------------------------------------------

            try:

                company_id = company["id"]

                jobs = get_company_jobs(
                    company_id
                )

                total_jobs = len(jobs)

                active_jobs = len(
                    [
                        job
                        for job in jobs
                        if str(
                            getattr(
                                job,
                                "status",
                                ""
                            )
                        ).lower()
                        == "active"
                    ]
                )

                applications = 0

                for job in jobs:

                    try:

                        job_apps = get_job_applications(
                            job.id
                        )

                        applications += len(
                            job_apps
                        )

                    except Exception:
                        continue

            except Exception:

                total_jobs = 0
                active_jobs = 0
                applications = 0

            st.write("")

            stat1, stat2, stat3 = st.columns(
                3,
                gap="medium"
            )

            with stat1:
                _stat_card(
                    "📋",
                    total_jobs,
                    "TOTAL JOBS"
                )

            with stat2:
                _stat_card(
                    "🟢",
                    active_jobs,
                    "ACTIVE JOBS"
                )

            with stat3:
                _stat_card(
                    "👥",
                    applications,
                    "APPLICATIONS"
                )

        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        with right:

            _info_card()

            _security_card()

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        st.write("")
        st.write("")

        if st.button(
            "🚀 Open Company Dashboard",
            type="primary",
            use_container_width=True,
            key="open_company_dashboard"
        ):

            st.session_state[
                "company_id"
            ] = company["id"]

            st.session_state[
                "company_saved"
            ] = True

            st.session_state[
                "page"
            ] = "company_dashboard"

            st.rerun()

    # ========================================================
    # NO COMPANY
    # ========================================================

    else:

        _empty_state()

        st.write("")

        col1, col2 = st.columns(
            [2, 1],
            gap="medium"
        )

        with col1:

            if st.button(
                "✨ Create Your Company",
                type="primary",
                use_container_width=True,
                key="create_company"
            ):

                st.session_state[
                    "page"
                ] = "company_profile"

                st.rerun()

        with col2:

            if st.button(
                "🚪 Logout",
                use_container_width=True,
                key="empty_logout"
            ):

                logout_user()

    # ========================================================
    # FOOTER / LOGOUT
    # ========================================================

    st.html(
        """
        <div style="
            margin-top:38px;
            padding-top:17px;
            border-top:1px solid #e2e8f0;
            text-align:center;
            color:#94a3b8;
            font-size:10px;
        ">
            CareerIQ • AI-Powered Career Intelligence & Job Matching Platform
        </div>
        """
    )

    # Existing-company logout is intentionally kept below
    # the main workflow so it does not compete with the CTA.
    if company:

        st.write("")

        if st.button(
            "🚪 Logout",
            use_container_width=True,
            key="company_logout"
        ):

            logout_user()


# ============================================================
# ENTRY POINT
# ============================================================

def company_selector():
    company_selector_page()
