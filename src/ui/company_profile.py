import html
import re
import streamlit as st

from src.auth.auth_repository import (
    get_user_company,
    link_company_to_user,
)

from src.database.models import Company

from src.database.repositories import (
    create_company,
)


# ============================================================
# PAGE CONFIG / THEME
# ============================================================

def style_company_profile():
    """
    Premium CareerIQ company profile styling.

    Important:
    - Custom HTML/CSS is rendered using st.html()
    - No st.markdown() is used for custom HTML/CSS
    """

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
                    rgba(99, 102, 241, 0.08),
                    transparent 30%
                ),
                #f7f9fc;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.8rem;
            padding-bottom: 4rem;
        }

        /* ========================================================
           REMOVE EXTRA STREAMLIT SPACING
        ======================================================== */

        div[data-testid="stVerticalBlock"] {
            gap: 0.6rem;
        }

        /* ========================================================
           HERO
        ======================================================== */

        .ciq-hero {
            position: relative;
            overflow: hidden;
            padding: 42px 44px;
            margin-bottom: 24px;
            border-radius: 28px;

            background:
                linear-gradient(
                    135deg,
                    #0b1220 0%,
                    #111c35 45%,
                    #243b76 100%
                );

            box-shadow:
                0 24px 70px rgba(15, 23, 42, 0.18);
        }

        .ciq-hero::before {
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -130px;
            top: -180px;
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
            width: 260px;
            height: 260px;
            left: 50%;
            bottom: -220px;
            border-radius: 50%;

            background:
                radial-gradient(
                    circle,
                    rgba(99, 102, 241, 0.24),
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

            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.13);

            color: #a5f3fc;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
        }

        .ciq-hero-title {
            margin-top: 16px;

            color: #ffffff;
            font-size: 39px;
            line-height: 1.12;
            font-weight: 850;
            letter-spacing: -0.035em;
        }

        .ciq-hero-subtitle {
            max-width: 720px;
            margin-top: 12px;

            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.75;
        }

        .ciq-hero-points {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
            margin-top: 22px;
        }

        .ciq-hero-point {
            padding: 7px 11px;
            border-radius: 10px;

            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.10);

            color: #e2e8f0;
            font-size: 11px;
            font-weight: 650;
        }

        /* ========================================================
           SECTION
        ======================================================== */

        .ciq-section {
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .ciq-section-title {
            color: #0f172a;
            font-size: 20px;
            font-weight: 850;
            letter-spacing: -0.02em;
        }

        .ciq-section-subtitle {
            margin-top: 4px;
            color: #64748b;
            font-size: 12px;
            line-height: 1.6;
        }

        /* ========================================================
           ACCOUNT CARD
        ======================================================== */

        .ciq-account {
            display: flex;
            align-items: center;
            gap: 14px;

            padding: 16px 18px;
            margin-bottom: 18px;

            border-radius: 18px;

            background:
                linear-gradient(
                    135deg,
                    #eff6ff,
                    #eef2ff
                );

            border: 1px solid #dbe4ff;
        }

        .ciq-account-icon {
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background: #ffffff;
            border: 1px solid #dbe4ff;

            font-size: 19px;

            box-shadow:
                0 6px 18px rgba(37, 99, 235, 0.08);
        }

        .ciq-account-label {
            color: #4f46e5;
            font-size: 10px;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .ciq-account-email {
            margin-top: 3px;
            color: #1e3a8a;
            font-size: 13px;
            font-weight: 700;
        }

        /* ========================================================
           FORM CARD
        ======================================================== */

        .ciq-form-card {
            padding: 24px;
            border-radius: 22px;

            background: rgba(255, 255, 255, 0.92);

            border: 1px solid #e5eaf2;

            box-shadow:
                0 12px 38px rgba(15, 23, 42, 0.055);
        }

        .ciq-form-heading {
            display: flex;
            align-items: center;
            gap: 12px;

            margin-bottom: 20px;
        }

        .ciq-form-icon {
            width: 44px;
            height: 44px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background:
                linear-gradient(
                    135deg,
                    #ecfeff,
                    #eef2ff
                );

            border: 1px solid #dbeafe;

            font-size: 21px;
        }

        .ciq-form-title {
            color: #0f172a;
            font-size: 19px;
            font-weight: 850;
        }

        .ciq-form-description {
            margin-top: 3px;
            color: #64748b;
            font-size: 12px;
        }

        /* ========================================================
           FIELD LABEL
        ======================================================== */

        .ciq-field-label {
            margin-top: 8px;
            margin-bottom: 5px;

            color: #334155;
            font-size: 12px;
            font-weight: 750;
        }

        .ciq-required {
            color: #ef4444;
        }

        /* ========================================================
           SECURITY CARD
        ======================================================== */

        .ciq-security {
            display: flex;
            gap: 13px;

            margin-top: 22px;
            padding: 16px 18px;

            border-radius: 17px;

            background:
                linear-gradient(
                    135deg,
                    #ecfdf5,
                    #f0fdf4
                );

            border: 1px solid #bbf7d0;
        }

        .ciq-security-icon {
            font-size: 18px;
        }

        .ciq-security-title {
            color: #166534;
            font-size: 12px;
            font-weight: 850;
        }

        .ciq-security-text {
            margin-top: 3px;
            color: #15803d;
            font-size: 11px;
            line-height: 1.55;
        }

        /* ========================================================
           PREVIEW CARD
        ======================================================== */

        .ciq-preview {
            padding: 21px;
            border-radius: 20px;

            background: #ffffff;
            border: 1px solid #e5e7eb;

            box-shadow:
                0 10px 30px rgba(15, 23, 42, 0.05);
        }

        .ciq-preview-title {
            color: #0f172a;
            font-size: 15px;
            font-weight: 850;
        }

        .ciq-preview-subtitle {
            margin-top: 4px;
            margin-bottom: 16px;

            color: #64748b;
            font-size: 11px;
            line-height: 1.55;
        }

        .ciq-preview-logo {
            width: 76px;
            height: 76px;

            display: flex;
            align-items: center;
            justify-content: center;

            margin-bottom: 13px;

            border-radius: 20px;

            background:
                linear-gradient(
                    135deg,
                    #eff6ff,
                    #eef2ff
                );

            border: 1px solid #dbeafe;

            font-size: 32px;
            overflow: hidden;
        }

        .ciq-preview-logo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .ciq-preview-name {
            color: #0f172a;
            font-size: 18px;
            font-weight: 850;
        }

        .ciq-preview-meta {
            margin-top: 5px;
            color: #64748b;
            font-size: 11px;
        }

        /* ========================================================
           EXISTING COMPANY
        ======================================================== */

        .ciq-existing {
            padding: 24px;
            margin-bottom: 18px;

            border-radius: 22px;

            background: #ffffff;
            border: 1px solid #e5e7eb;

            box-shadow:
                0 12px 36px rgba(15, 23, 42, 0.06);
        }

        .ciq-existing-badge {
            display: inline-block;

            padding: 6px 10px;
            border-radius: 999px;

            background: #eff6ff;
            color: #2563eb;

            font-size: 10px;
            font-weight: 850;
            letter-spacing: 0.06em;
        }

        .ciq-existing-name {
            margin-top: 14px;

            color: #0f172a;
            font-size: 27px;
            font-weight: 850;
            letter-spacing: -0.025em;
        }

        .ciq-existing-text {
            margin-top: 7px;

            color: #64748b;
            font-size: 12px;
            line-height: 1.65;
        }

        /* ========================================================
           FOOTER
        ======================================================== */

        .ciq-footer {
            margin-top: 30px;
            padding-top: 18px;

            border-top: 1px solid #e2e8f0;

            color: #94a3b8;
            font-size: 10px;
            text-align: center;
        }

        /* ========================================================
           STREAMLIT INPUTS
        ======================================================== */

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div {
            border-radius: 12px !important;
            border-color: #dbe2ea !important;
            background: #ffffff !important;
        }

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow:
                0 0 0 3px rgba(99, 102, 241, 0.10) !important;
        }

        input,
        textarea {
            font-size: 13px !important;
        }

        /* ========================================================
           BUTTONS
        ======================================================== */

        div.stButton > button {
            min-height: 45px;

            border-radius: 12px !important;

            font-weight: 750 !important;
            font-size: 13px !important;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-1px);
        }

        /* ========================================================
           RESPONSIVE
        ======================================================== */

        @media (max-width: 768px) {

            .ciq-hero {
                padding: 28px 24px;
                border-radius: 22px;
            }

            .ciq-hero-title {
                font-size: 30px;
            }

            .ciq-form-card {
                padding: 18px;
            }

        }

        </style>
        """
    )


# ============================================================
# HELPERS
# ============================================================

def _safe_text(value, fallback=""):
    """Safely escape text for HTML rendering."""
    return html.escape(str(value or fallback))


def _valid_url(url):
    """Basic website/logo URL validation."""
    if not url:
        return True

    return bool(
        re.match(
            r"^https?://.+",
            url.strip(),
            re.IGNORECASE
        )
    )


def _show_logo_preview(logo_url):
    """Render a logo preview if a valid URL is provided."""

    if not logo_url or not _valid_url(logo_url):
        return

    safe_url = html.escape(logo_url.strip(), quote=True)

    st.html(
        f"""
        <div style="
            margin-top:10px;
            padding:12px;
            border:1px solid #e2e8f0;
            border-radius:14px;
            background:#f8fafc;
        ">
            <div style="
                font-size:10px;
                font-weight:800;
                color:#64748b;
                margin-bottom:8px;
                text-transform:uppercase;
                letter-spacing:.06em;
            ">
                Logo Preview
            </div>

            <img
                src="{safe_url}"
                style="
                    width:72px;
                    height:72px;
                    object-fit:contain;
                    border-radius:14px;
                    background:white;
                    border:1px solid #e2e8f0;
                    padding:8px;
                "
            >
        </div>
        """
    )


# ============================================================
# HERO
# ============================================================

def _show_hero():

    st.html(
        """
        <div class="ciq-hero">

            <div class="ciq-hero-content">

                <div class="ciq-eyebrow">
                    🏢 CAREERIQ • COMPANY PORTAL
                </div>

                <div class="ciq-hero-title">
                    Build your company presence.
                </div>

                <div class="ciq-hero-subtitle">
                    Create a professional company profile to publish
                    opportunities, discover qualified candidates and
                    manage your hiring pipeline with CareerIQ's
                    AI-powered recruitment platform.
                </div>

                <div class="ciq-hero-points">

                    <div class="ciq-hero-point">
                        ✨ Professional Company Profile
                    </div>

                    <div class="ciq-hero-point">
                        🎯 AI Candidate Matching
                    </div>

                    <div class="ciq-hero-point">
                        📊 Hiring Intelligence
                    </div>

                </div>

            </div>

        </div>
        """
    )


# ============================================================
# ACCOUNT CARD
# ============================================================

def _show_account_card(user_email):

    safe_email = _safe_text(
        user_email,
        "Authenticated account"
    )

    st.html(
        f"""
        <div class="ciq-account">

            <div class="ciq-account-icon">
                🔐
            </div>

            <div>

                <div class="ciq-account-label">
                    COMPANY ACCOUNT
                </div>

                <div class="ciq-account-email">
                    {safe_email}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# FORM HEADER
# ============================================================

def _show_form_header():

    st.html(
        """
        <div class="ciq-form-heading">

            <div class="ciq-form-icon">
                🏢
            </div>

            <div>

                <div class="ciq-form-title">
                    Company Information
                </div>

                <div class="ciq-form-description">
                    Tell candidates what your organization does
                    and why they should consider working with you.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# SECURITY
# ============================================================

def _show_security():

    st.html(
        """
        <div class="ciq-security">

            <div class="ciq-security-icon">
                🔒
            </div>

            <div>

                <div class="ciq-security-title">
                    Account protection
                </div>

                <div class="ciq-security-text">
                    One company can be connected to this account.
                    This prevents duplicate company profiles and
                    keeps your jobs and applications connected
                    to the correct organization.
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# COMPANY PREVIEW
# ============================================================

def _show_preview(
    company_name,
    industry,
    location,
    logo_url
):

    safe_name = _safe_text(
        company_name,
        "Your Company"
    )

    safe_industry = _safe_text(
        industry,
        "Industry"
    )

    safe_location = _safe_text(
        location,
        "Location"
    )

    logo_html = "🏢"

    if logo_url and _valid_url(logo_url):
        safe_logo = html.escape(
            logo_url.strip(),
            quote=True
        )

        logo_html = (
            f'<img src="{safe_logo}" '
            f'alt="Company logo">'
        )

    st.html(
        f"""
        <div class="ciq-preview">

            <div class="ciq-preview-title">
                Profile Preview
            </div>

            <div class="ciq-preview-subtitle">
                This is how your company information
                will begin to appear inside CareerIQ.
            </div>

            <div class="ciq-preview-logo">
                {logo_html}
            </div>

            <div class="ciq-preview-name">
                {safe_name}
            </div>

            <div class="ciq-preview-meta">
                {safe_industry}
                &nbsp; • &nbsp;
                {safe_location}
            </div>

        </div>
        """
    )


# ============================================================
# EXISTING COMPANY
# ============================================================

def _show_existing_company(existing_company):

    company_name = _safe_text(
        existing_company.get(
            "company_name",
            "Your Company"
        )
    )

    industry = _safe_text(
        existing_company.get(
            "industry",
            ""
        )
    )

    location = _safe_text(
        existing_company.get(
            "location",
            ""
        )
    )

    st.html(
        f"""
        <div class="ciq-existing">

            <div class="ciq-existing-badge">
                ✓ REGISTERED COMPANY
            </div>

            <div class="ciq-existing-name">
                🏢 {company_name}
            </div>

            <div class="ciq-existing-text">
                This account is already connected to a company.
                You can continue directly to your company
                dashboard to manage jobs and candidates.
            </div>

            <div style="
                display:flex;
                flex-wrap:wrap;
                gap:8px;
                margin-top:15px;
            ">

                <span style="
                    padding:6px 9px;
                    border-radius:8px;
                    background:#f1f5f9;
                    color:#475569;
                    font-size:10px;
                    font-weight:700;
                ">
                    🏷️ {industry or "Industry not specified"}
                </span>

                <span style="
                    padding:6px 9px;
                    border-radius:8px;
                    background:#f1f5f9;
                    color:#475569;
                    font-size:10px;
                    font-weight:700;
                ">
                    📍 {location or "Location not specified"}
                </span>

            </div>

        </div>
        """
    )


# ============================================================
# COMPANY PROFILE PAGE
# ============================================================

def company_profile_page():

    style_company_profile()

    user_id = st.session_state.get(
        "user_id"
    )

    # ========================================================
    # AUTH CHECK
    # ========================================================

    if not user_id:

        st.error(
            "Please login first."
        )

        st.session_state["page"] = "home"
        st.rerun()

        return

    # ========================================================
    # USER ACCOUNT
    # ========================================================

    user_email = st.session_state.get(
        "user_email",
        ""
    )

    # ========================================================
    # CHECK EXISTING COMPANY
    # ========================================================

    existing_company = get_user_company(
        user_id
    )

    # ========================================================
    # EXISTING COMPANY FLOW
    # ========================================================

    if existing_company:

        _show_hero()

        _show_existing_company(
            existing_company
        )

        st.info(
            "This account already has a company profile. "
            "A second company cannot be created."
        )

        st.write("")

        col1, col2 = st.columns(
            [2, 1],
            gap="medium"
        )

        with col1:

            if st.button(
                "🚀 Open Company Dashboard",
                type="primary",
                use_container_width=True,
                key="open_company_dashboard"
            ):

                st.session_state[
                    "company_id"
                ] = existing_company["id"]

                st.session_state[
                    "company_saved"
                ] = True

                st.session_state[
                    "page"
                ] = "company_dashboard"

                st.rerun()

        with col2:

            if st.button(
                "← Back",
                use_container_width=True,
                key="existing_company_back"
            ):

                st.session_state[
                    "page"
                ] = "company_selector"

                st.rerun()

        st.html(
            """
            <div class="ciq-footer">
                CareerIQ • Company Recruitment Intelligence Platform
            </div>
            """
        )

        return

    # ========================================================
    # HERO
    # ========================================================

    _show_hero()

    # ========================================================
    # ACCOUNT
    # ========================================================

    _show_account_card(
        user_email
    )

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    left, right = st.columns(
        [1.75, 1],
        gap="large"
    )

    # ========================================================
    # LEFT — FORM
    # ========================================================

    with left:

        st.html(
            '<div class="ciq-form-card">'
        )

        _show_form_header()

        # ----------------------------------------------------
        # COMPANY NAME
        # ----------------------------------------------------

        st.html(
            """
            <div class="ciq-field-label">
                Company Name <span class="ciq-required">*</span>
            </div>
            """
        )

        company_name = st.text_input(
            "Company Name",
            placeholder="e.g. TechNova Solutions",
            key="new_company_name",
            label_visibility="collapsed"
        )

        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        st.html(
            """
            <div class="ciq-field-label">
                Company Email
            </div>
            """
        )

        st.text_input(
            "Company Email",
            value=user_email,
            disabled=True,
            key="company_account_email",
            label_visibility="collapsed"
        )

        # ----------------------------------------------------
        # WEBSITE
        # ----------------------------------------------------

        st.html(
            """
            <div class="ciq-field-label">
                Website
            </div>
            """
        )

        website = st.text_input(
            "Website",
            placeholder="https://yourcompany.com",
            key="new_company_website",
            label_visibility="collapsed"
        )

        # ----------------------------------------------------
        # INDUSTRY + LOCATION
        # ----------------------------------------------------

        col1, col2 = st.columns(
            2,
            gap="medium"
        )

        with col1:

            st.html(
                """
                <div class="ciq-field-label">
                    Industry
                </div>
                """
            )

            industry = st.text_input(
                "Industry",
                placeholder="e.g. Artificial Intelligence",
                key="new_company_industry",
                label_visibility="collapsed"
            )

        with col2:

            st.html(
                """
                <div class="ciq-field-label">
                    Location
                </div>
                """
            )

            location = st.text_input(
                "Location",
                placeholder="e.g. Pune, Maharashtra",
                key="new_company_location",
                label_visibility="collapsed"
            )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        st.html(
            """
            <div class="ciq-field-label">
                Company Description
            </div>
            """
        )

        description = st.text_area(
            "Company Description",
            placeholder=(
                "Tell candidates about your company, "
                "products, technology, culture, mission "
                "and what makes your organization unique..."
            ),
            height=165,
            key="new_company_description",
            label_visibility="collapsed"
        )

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        st.html(
            """
            <div class="ciq-field-label">
                Company Logo URL
            </div>
            """
        )

        logo_url = st.text_input(
            "Company Logo URL",
            placeholder="https://example.com/logo.png",
            key="new_company_logo",
            label_visibility="collapsed"
        )

        if logo_url:

            if _valid_url(logo_url):

                _show_logo_preview(
                    logo_url
                )

            else:

                st.warning(
                    "Logo URL should start with http:// or https://."
                )

        # ----------------------------------------------------
        # SECURITY
        # ----------------------------------------------------

        _show_security()

        st.html(
            "</div>"
        )

    # ========================================================
    # RIGHT — PREVIEW + GUIDANCE
    # ========================================================

    with right:

        _show_preview(
            company_name,
            industry,
            location,
            logo_url
        )

        st.write("")

        st.html(
            """
            <div style="
                padding:20px;
                border-radius:20px;
                background:
                    linear-gradient(
                        135deg,
                        #f8fafc,
                        #eef2ff
                    );
                border:1px solid #e2e8f0;
            ">

                <div style="
                    color:#0f172a;
                    font-size:14px;
                    font-weight:850;
                ">
                    💡 Profile tips
                </div>

                <div style="
                    margin-top:12px;
                    color:#64748b;
                    font-size:11px;
                    line-height:1.75;
                ">

                    <div>✓ Use your official company name</div>

                    <div>
                        ✓ Add your website for credibility
                    </div>

                    <div>
                        ✓ Describe your products and technology
                    </div>

                    <div>
                        ✓ Mention your company location
                    </div>

                    <div>
                        ✓ Use a professional company logo
                    </div>

                </div>

            </div>
            """
        )

        st.write("")

        st.html(
            """
            <div style="
                padding:18px;
                border-radius:18px;
                background:#ffffff;
                border:1px solid #e5e7eb;
            ">

                <div style="
                    color:#334155;
                    font-size:12px;
                    font-weight:800;
                ">
                    🎯 What's next?
                </div>

                <div style="
                    margin-top:7px;
                    color:#64748b;
                    font-size:11px;
                    line-height:1.65;
                ">
                    After creating your company profile,
                    you'll be able to publish jobs and
                    start discovering candidates through
                    CareerIQ.
                </div>

            </div>
            """
        )

    # ========================================================
    # ACTION BAR
    # ========================================================

    st.write("")
    st.write("")

    col1, col2 = st.columns(
        [2, 1],
        gap="medium"
    )

    with col1:

        save_clicked = st.button(
            "🚀 Create Company Profile",
            type="primary",
            use_container_width=True,
            key="create_company_profile"
        )

    with col2:

        cancel_clicked = st.button(
            "← Back",
            use_container_width=True,
            key="company_profile_back"
        )

    # ========================================================
    # CANCEL
    # ========================================================

    if cancel_clicked:

        st.session_state[
            "page"
        ] = "company_selector"

        st.rerun()

    # ========================================================
    # SAVE
    # ========================================================

    if save_clicked:

        # ----------------------------------------------------
        # FINAL DUPLICATE CHECK
        # ----------------------------------------------------

        existing_company = get_user_company(
            user_id
        )

        if existing_company:

            st.error(
                "This account already has a registered company. "
                "A second company cannot be created."
            )

            return

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not company_name.strip():

            st.error(
                "Please enter your company name."
            )

            return

        if website.strip() and not _valid_url(
            website
        ):

            st.error(
                "Please enter a valid website URL "
                "starting with http:// or https://."
            )

            return

        if logo_url.strip() and not _valid_url(
            logo_url
        ):

            st.error(
                "Please enter a valid logo URL "
                "starting with http:// or https://."
            )

            return

        # ----------------------------------------------------
        # CREATE COMPANY OBJECT
        # ----------------------------------------------------

        company = Company(
            company_name=company_name.strip(),
            email=user_email.strip(),
            website=website.strip(),
            industry=industry.strip(),
            location=location.strip(),
            description=description.strip(),
            logo_url=logo_url.strip()
        )

        try:

            # ------------------------------------------------
            # CREATE COMPANY
            # ------------------------------------------------

            company_id = create_company(
                company
            )

            # ------------------------------------------------
            # LINK COMPANY TO USER
            # ------------------------------------------------

            try:

                link_company_to_user(
                    user_id,
                    company_id
                )

            except Exception:

                # --------------------------------------------
                # CLEAN UP ORPHAN COMPANY
                # --------------------------------------------

                from src.database.repositories import (
                    delete_company,
                )

                try:

                    delete_company(
                        company_id
                    )

                except Exception:
                    pass

                raise

            # ------------------------------------------------
            # SAVE SESSION
            # ------------------------------------------------

            st.session_state[
                "company_id"
            ] = company_id

            st.session_state[
                "company_saved"
            ] = True

            st.session_state[
                "page"
            ] = "company_dashboard"

            st.success(
                "Company profile created successfully!"
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"Could not create company profile: {error}"
            )

    # ========================================================
    # FOOTER
    # ========================================================

    st.html(
        """
        <div class="ciq-footer">
            CareerIQ • AI-Powered Career Intelligence & Job Matching Platform
        </div>
        """
    )


# ============================================================
# COMPATIBILITY ENTRY POINT
# ============================================================

def company_profile():
    company_profile_page()