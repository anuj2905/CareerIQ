
import html
import re
import streamlit as st

from src.database.models import Company
from src.database.repositories import (
    create_company,
    get_company,
)

# ============================================================
# CAREERIQ — COMPANY PROFILE
# Premium production UI
# ============================================================

INDUSTRIES = [
    "Select industry",
    "Information Technology",
    "Artificial Intelligence",
    "Software Development",
    "FinTech",
    "Healthcare",
    "Education",
    "E-Commerce",
    "Consulting",
    "Banking & Finance",
    "Manufacturing",
    "Other",
]


def _safe(value, fallback=""):
    return html.escape(str(value or fallback), quote=True)


def _valid_url(value):
    if not value.strip():
        return True
    return bool(re.match(r"^https?://.+", value.strip(), re.I))


def style_company_profile():
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
                    rgba(34,211,238,.08),
                    transparent 28%
                ),
                radial-gradient(
                    circle at 96% 4%,
                    rgba(99,102,241,.09),
                    transparent 30%
                ),
                #f7f9fc;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        /* ========================================================
           HERO
        ======================================================== */

        .hero {
            position: relative;
            overflow: hidden;
            padding: 40px 44px;
            border-radius: 28px;
            margin-bottom: 22px;

            background:
                linear-gradient(
                    135deg,
                    #07111f 0%,
                    #101d3d 50%,
                    #33256f 100%
                );

            box-shadow:
                0 25px 70px rgba(15,23,42,.19);
        }

        .hero:before {
            content: "";
            position: absolute;
            width: 390px;
            height: 390px;
            right: -150px;
            top: -205px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle,
                    rgba(34,211,238,.31),
                    transparent 69%
                );
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            left: -140px;
            bottom: -180px;
            border-radius: 50%;
            background:
                radial-gradient(
                    circle,
                    rgba(129,140,248,.25),
                    transparent 70%
                );
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.13);
            color: #a5f3fc;
            font-size: 10px;
            font-weight: 850;
            letter-spacing: .09em;
        }

        .hero-title {
            margin-top: 15px;
            color: #fff;
            font-size: 38px;
            line-height: 1.1;
            font-weight: 850;
            letter-spacing: -.035em;
        }

        .hero-text {
            max-width: 710px;
            margin-top: 10px;
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.7;
        }

        .hero-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 19px;
        }

        .flow-item {
            padding: 7px 10px;
            border-radius: 9px;
            background: rgba(255,255,255,.07);
            border: 1px solid rgba(255,255,255,.10);
            color: #e2e8f0;
            font-size: 10px;
            font-weight: 700;
        }

        /* ========================================================
           PROGRESS
        ======================================================== */

        .progress-card {
            padding: 17px 20px;
            border-radius: 18px;
            background: rgba(255,255,255,.94);
            border: 1px solid #e2e8f0;
            box-shadow: 0 8px 26px rgba(15,23,42,.045);
            margin-bottom: 24px;
        }

        .progress-head {
            display: flex;
            justify-content: space-between;
            color: #334155;
            font-size: 11px;
            font-weight: 800;
        }

        .progress-track {
            height: 7px;
            margin-top: 10px;
            border-radius: 999px;
            background: #e2e8f0;
            overflow: hidden;
        }

        .progress-fill {
            width: 33.33%;
            height: 100%;
            border-radius: 999px;
            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #7c3aed
                );
        }

        .progress-text {
            margin-top: 8px;
            color: #64748b;
            font-size: 10px;
        }

        /* ========================================================
           SECTION
        ======================================================== */

        .section {
            margin-bottom: 11px;
        }

        .section-title {
            color: #0f172a;
            font-size: 20px;
            font-weight: 850;
            letter-spacing: -.02em;
        }

        .section-text {
            margin-top: 3px;
            color: #64748b;
            font-size: 11px;
            line-height: 1.6;
        }

        /* ========================================================
           FORM
        ======================================================== */

        .form-card {
            padding: 25px;
            border-radius: 22px;
            background: rgba(255,255,255,.95);
            border: 1px solid #e2e8f0;
            box-shadow: 0 12px 38px rgba(15,23,42,.055);
        }

        .form-heading {
            display: flex;
            align-items: center;
            gap: 11px;
            margin-bottom: 19px;
        }

        .form-icon {
            width: 43px;
            height: 43px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 13px;
            background: linear-gradient(135deg,#eff6ff,#eef2ff);
            border: 1px solid #dbeafe;
            font-size: 20px;
        }

        .field-label {
            margin-top: 5px;
            margin-bottom: 5px;
            color: #334155;
            font-size: 11px;
            font-weight: 750;
        }

        .required {
            color: #ef4444;
        }

        /* ========================================================
           PREVIEW
        ======================================================== */

        .preview-card {
            padding: 23px;
            border-radius: 22px;
            background: #fff;
            border: 1px solid #e2e8f0;
            box-shadow: 0 12px 36px rgba(15,23,42,.055);
        }

        .preview-label {
            color: #64748b;
            font-size: 10px;
            font-weight: 850;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .preview-logo {
            width: 72px;
            height: 72px;
            margin-top: 17px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            background: linear-gradient(135deg,#eff6ff,#eef2ff);
            border: 1px solid #dbeafe;
            font-size: 31px;
        }

        .preview-logo img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .preview-name {
            margin-top: 14px;
            color: #0f172a;
            font-size: 22px;
            font-weight: 850;
            letter-spacing: -.025em;
        }

        .preview-industry {
            display: inline-block;
            margin-top: 8px;
            padding: 5px 9px;
            border-radius: 999px;
            background: #f1f5f9;
            color: #475569;
            font-size: 10px;
            font-weight: 750;
        }

        .preview-location {
            margin-top: 11px;
            color: #64748b;
            font-size: 11px;
        }

        .preview-divider {
            height: 1px;
            margin: 18px 0;
            background: #e2e8f0;
        }

        .preview-description {
            color: #475569;
            font-size: 11px;
            line-height: 1.7;
        }

        .preview-website {
            margin-top: 15px;
            padding: 10px 11px;
            border-radius: 10px;
            background: #f8fafc;
            color: #475569;
            font-size: 10px;
            word-break: break-word;
        }

        /* ========================================================
           NEXT STEPS
        ======================================================== */

        .next-card {
            margin-top: 17px;
            padding: 21px;
            border-radius: 20px;
            background: #0f172a;
            color: #fff;
        }

        .next-title {
            color: #fff;
            font-size: 14px;
            font-weight: 850;
        }

        .step {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }

        .step-num {
            width: 27px;
            height: 27px;
            flex: 0 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: #334155;
            color: #cbd5e1;
            font-size: 10px;
            font-weight: 800;
        }

        .step-num.active {
            background: #fff;
            color: #0f172a;
        }

        .step-title {
            color: #f8fafc;
            font-size: 11px;
            font-weight: 800;
        }

        .step-text {
            margin-top: 2px;
            color: #94a3b8;
            font-size: 10px;
        }

        /* ========================================================
           SAVED STATE
        ======================================================== */

        .saved-card {
            display: flex;
            gap: 11px;
            align-items: center;
            margin-top: 17px;
            padding: 14px;
            border-radius: 15px;
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
        }

        .saved-icon {
            width: 34px;
            height: 34px;
            flex: 0 0 auto;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: #16a34a;
            color: #fff;
            font-weight: 850;
        }

        .saved-title {
            color: #166534;
            font-size: 11px;
            font-weight: 850;
        }

        .saved-text {
            margin-top: 2px;
            color: #15803d;
            font-size: 10px;
        }

        /* ========================================================
           INPUTS
        ======================================================== */

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {
            border-radius: 11px !important;
            border-color: #dbe2ea !important;
            background: #fff !important;
        }

        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,.09) !important;
        }

        input,
        textarea {
            font-size: 12px !important;
        }

        .stButton > button {
            min-height: 44px;
            border-radius: 11px !important;
            font-size: 12px !important;
            font-weight: 750 !important;
        }

        /* ========================================================
           RESPONSIVE
        ======================================================== */

        @media (max-width: 768px) {
            .hero {
                padding: 28px 23px;
                border-radius: 22px;
            }

            .hero-title {
                font-size: 30px;
            }

            .form-card,
            .preview-card {
                padding: 18px;
            }
        }

        </style>
        """
    )


def _hero():
    st.html(
        """
        <div class="hero">
            <div class="hero-content">

                <div class="badge">
                    🏢 CAREERIQ • COMPANY WORKSPACE
                </div>

                <div class="hero-title">
                    Build your company presence.
                </div>

                <div class="hero-text">
                    Create a professional company profile to publish
                    opportunities, attract qualified candidates and
                    power CareerIQ's intelligent matching workflow.
                </div>

                <div class="hero-flow">
                    <div class="flow-item">✨ Company Profile</div>
                    <div class="flow-item">📋 Create Jobs</div>
                    <div class="flow-item">🎯 Find Candidates</div>
                </div>

            </div>
        </div>
        """
    )


def _progress():
    st.html(
        """
        <div class="progress-card">

            <div class="progress-head">
                <span>Profile setup</span>
                <span>Step 1 of 3</span>
            </div>

            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>

            <div class="progress-text">
                Company Profile &nbsp; → &nbsp;
                Create Jobs &nbsp; → &nbsp;
                Find Candidates
            </div>

        </div>
        """
    )


def _preview(
    name,
    industry,
    location,
    description,
    website,
    logo_url,
):
    safe_name = _safe(name, "Your Company")
    safe_industry = _safe(
        industry if industry != "Select industry"
        else "Your Industry"
    )
    safe_location = _safe(location, "Your Location")
    safe_description = _safe(
        description,
        "Your company description will appear here once you enter it.",
    )
    safe_website = _safe(
        website,
        "Company website",
    )

    if logo_url.strip() and _valid_url(logo_url):
        logo = (
            f'<img src="{_safe(logo_url)}" '
            f'alt="Company logo">'
        )
    else:
        logo = "🏢"

    st.html(
        f"""
        <div class="preview-card">

            <div class="preview-label">
                PROFILE PREVIEW
            </div>

            <div class="preview-logo">
                {logo}
            </div>

            <div class="preview-name">
                {safe_name}
            </div>

            <div class="preview-industry">
                {safe_industry}
            </div>

            <div class="preview-location">
                📍 {safe_location}
            </div>

            <div class="preview-divider"></div>

            <div class="preview-description">
                {safe_description}
            </div>

            <div class="preview-website">
                🌐 {safe_website}
            </div>

        </div>
        """
    )


def _next_steps():
    st.html(
        """
        <div class="next-card">

            <div class="next-title">
                🚀 What's next?
            </div>

            <div class="step">
                <div class="step-num active">1</div>
                <div>
                    <div class="step-title">Company Profile</div>
                    <div class="step-text">
                        Introduce your organization.
                    </div>
                </div>
            </div>

            <div class="step">
                <div class="step-num">2</div>
                <div>
                    <div class="step-title">Create Jobs</div>
                    <div class="step-text">
                        Publish your open positions.
                    </div>
                </div>
            </div>

            <div class="step">
                <div class="step-num">3</div>
                <div>
                    <div class="step-title">Find Candidates</div>
                    <div class="step-text">
                        Discover matching students.
                    </div>
                </div>
            </div>

        </div>
        """
    )


def company_profile_page():
    """
    CareerIQ company profile creation / update page.
    """

    style_company_profile()
    _hero()
    _progress()

    company_id = st.session_state.get("company_id")
    existing_company = None

    if company_id:
        try:
            existing_company = get_company(company_id)
        except Exception as error:
            st.error(
                f"Unable to load company profile: {error}"
            )

    # ========================================================
    # DEFAULTS
    # ========================================================

    if existing_company:
        default_name = existing_company.company_name or ""
        default_email = existing_company.email or ""
        default_website = existing_company.website or ""
        default_industry = existing_company.industry or "Select industry"
        default_location = existing_company.location or ""
        default_description = existing_company.description or ""
        default_logo = existing_company.logo_url or ""
    else:
        default_name = ""
        default_email = st.session_state.get("user_email", "")
        default_website = ""
        default_industry = "Select industry"
        default_location = ""
        default_description = ""
        default_logo = ""

    # ========================================================
    # MAIN
    # ========================================================

    left, right = st.columns(
        [1.65, 1],
        gap="large",
    )

    # ========================================================
    # FORM
    # ========================================================

    with left:

        st.html(
            """
            <div class="section">
                <div class="section-title">
                    🏢 Company Information
                </div>
                <div class="section-text">
                    Tell candidates about your organization.
                </div>
            </div>

            <div class="form-card">
            """
        )

        company_name = st.text_input(
            "Company Name *",
            value=default_name,
            placeholder="e.g. Microsoft",
            key="company_name",
        )

        c1, c2 = st.columns(2, gap="medium")

        with c1:
            email = st.text_input(
                "Company Email *",
                value=default_email,
                placeholder="hr@company.com",
                key="company_email",
            )

        with c2:
            website = st.text_input(
                "Website",
                value=default_website,
                placeholder="https://company.com",
                key="company_website",
            )

        c3, c4 = st.columns(2, gap="medium")

        if default_industry in INDUSTRIES:
            industry_index = INDUSTRIES.index(
                default_industry
            )
        else:
            industry_index = 0

        with c3:
            industry = st.selectbox(
                "Industry *",
                INDUSTRIES,
                index=industry_index,
                key="company_industry",
            )

        with c4:
            location = st.text_input(
                "Location *",
                value=default_location,
                placeholder="e.g. Pune, Maharashtra",
                key="company_location",
            )

        description = st.text_area(
            "Company Description *",
            value=default_description,
            placeholder=(
                "Describe your company, products, culture, "
                "technology and what makes your organization unique..."
            ),
            height=170,
            key="company_description",
        )

        logo_url = st.text_input(
            "Company Logo URL",
            value=default_logo,
            placeholder="https://example.com/logo.png",
            key="company_logo_url",
        )

        st.html("</div>")

        st.write("")

        save_col, clear_col = st.columns(
            [3, 1],
            gap="medium",
        )

        with save_col:
            save_clicked = st.button(
                "🚀 Save Company Profile",
                type="primary",
                use_container_width=True,
                key="save_company_profile",
            )

        with clear_col:
            clear_clicked = st.button(
                "Clear",
                use_container_width=True,
                key="clear_company_profile",
            )

        if clear_clicked:
            for key in [
                "company_name",
                "company_email",
                "company_website",
                "company_industry",
                "company_location",
                "company_description",
                "company_logo_url",
            ]:
                st.session_state.pop(key, None)

            st.rerun()

        # ====================================================
        # SAVE
        # ====================================================

        if save_clicked:

            if not company_name.strip():
                st.error("Please enter the company name.")

            elif not email.strip():
                st.error("Please enter the company email.")

            elif "@" not in email:
                st.error("Please enter a valid company email.")

            elif industry == "Select industry":
                st.error("Please select an industry.")

            elif not location.strip():
                st.error("Please enter the company location.")

            elif not description.strip():
                st.error("Please enter a company description.")

            elif website.strip() and not _valid_url(website):
                st.error(
                    "Website URL should start with http:// or https://."
                )

            elif logo_url.strip() and not _valid_url(logo_url):
                st.error(
                    "Logo URL should start with http:// or https://."
                )

            else:
                try:
                    company = Company(
                        id=company_id,
                        company_name=company_name.strip(),
                        email=email.strip(),
                        website=website.strip(),
                        industry=industry,
                        location=location.strip(),
                        description=description.strip(),
                        logo_url=logo_url.strip(),
                    )

                    if company_id is None:

                        new_company_id = create_company(
                            company
                        )

                        st.session_state[
                            "company_id"
                        ] = new_company_id

                        st.session_state[
                            "company_profile"
                        ] = company

                        st.session_state[
                            "company_saved"
                        ] = True

                        st.success(
                            "🎉 Company profile created successfully!"
                        )

                    else:

                        from src.database.repositories import (
                            update_company,
                        )

                        update_company(company)

                        st.session_state[
                            "company_profile"
                        ] = company

                        st.session_state[
                            "company_saved"
                        ] = True

                        st.success(
                            "✅ Company profile updated successfully!"
                        )

                except Exception as error:
                    st.error(
                        f"Unable to save company profile: {error}"
                    )

    # ========================================================
    # PREVIEW
    # ========================================================

    with right:

        st.html(
            """
            <div class="section">
                <div class="section-title">
                    👁️ Profile Preview
                </div>
                <div class="section-text">
                    See how your company information will look.
                </div>
            </div>
            """
        )

        _preview(
            company_name,
            industry,
            location,
            description,
            website,
            logo_url,
        )

        if st.session_state.get(
            "company_saved",
            False,
        ):
            st.html(
                """
                <div class="saved-card">

                    <div class="saved-icon">
                        ✓
                    </div>

                    <div>
                        <div class="saved-title">
                            Profile saved
                        </div>
                        <div class="saved-text">
                            Your company information is stored in CareerIQ.
                        </div>
                    </div>

                </div>
                """
            )

        _next_steps()

    # ========================================================
    # BACK
    # ========================================================

    st.write("")
    st.write("")

    if st.button(
        "← Back",
        use_container_width=True,
        key="company_profile_back",
    ):
        st.session_state["page"] = "company_selector"
        st.rerun()


# ============================================================
# COMPATIBILITY ENTRY POINT
# ============================================================

def company_profile():
    company_profile_page()
