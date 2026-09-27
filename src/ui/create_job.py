import html

import streamlit as st

from src.database.models import Job
from src.database.repositories import create_job as save_job, get_company


# ============================================================
# PAGE STYLING
# ============================================================

def style_create_job_page():

    st.markdown(
        """
        <style>

        /* ====================================================
           GLOBAL
        ==================================================== */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        /* ====================================================
           HERO
        ==================================================== */

        .job-hero {
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 85% 15%,
                    rgba(59, 130, 246, 0.30),
                    transparent 35%
                ),
                radial-gradient(
                    circle at 10% 90%,
                    rgba(139, 92, 246, 0.22),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #0f172a,
                    #111827 55%,
                    #1e293b
                );

            padding: 38px 42px;
            border-radius: 26px;
            margin-bottom: 30px;
            color: white;

            border: 1px solid rgba(255,255,255,0.10);

            box-shadow:
                0 25px 50px rgba(15,23,42,0.20),
                inset 0 1px 0 rgba(255,255,255,0.08);
        }

        .job-hero::before {
            content: "";
            position: absolute;

            width: 180px;
            height: 180px;

            right: -50px;
            top: -70px;

            border-radius: 50%;

            background: rgba(255,255,255,0.05);

            filter: blur(2px);
        }

        .job-hero::after {
            content: "";
            position: absolute;

            width: 120px;
            height: 120px;

            left: 45%;
            bottom: -80px;

            border-radius: 50%;

            background: rgba(59,130,246,0.10);
        }

        .step-badge {
            display: inline-flex;
            align-items: center;

            padding: 8px 15px;

            border-radius: 999px;

            background: rgba(255,255,255,0.10);

            border: 1px solid rgba(255,255,255,0.12);

            color: #dbeafe;

            font-size: 12px;
            font-weight: 700;

            letter-spacing: 0.05em;

            margin-bottom: 18px;

            backdrop-filter: blur(12px);
        }

        .job-hero-title {
            font-size: 38px;
            font-weight: 850;

            letter-spacing: -0.02em;

            margin-bottom: 10px;
        }

        .job-hero-subtitle {
            max-width: 760px;

            font-size: 15px;

            color: #cbd5e1;

            line-height: 1.7;
        }

        /* ====================================================
           SECTION CARDS
        ==================================================== */

        .section-card {
            position: relative;

            background:
                linear-gradient(
                    145deg,
                    rgba(255,255,255,0.98),
                    rgba(248,250,252,0.96)
                );

            border: 1px solid #e2e8f0;

            border-radius: 22px;

            padding: 25px;

            margin-bottom: 20px;

            box-shadow:
                0 12px 30px rgba(15,23,42,0.07),
                0 2px 5px rgba(15,23,42,0.03);

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        .section-card:hover {
            transform: translateY(-2px);

            box-shadow:
                0 18px 40px rgba(15,23,42,0.10),
                0 3px 8px rgba(15,23,42,0.04);
        }

        .section-icon {
            width: 42px;
            height: 42px;

            display: flex;
            align-items: center;
            justify-content: center;

            border-radius: 13px;

            background:
                linear-gradient(
                    145deg,
                    #eff6ff,
                    #dbeafe
                );

            box-shadow:
                0 6px 12px rgba(59,130,246,0.12);

            font-size: 20px;

            margin-bottom: 13px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 800;

            color: #0f172a;

            margin-bottom: 5px;
        }

        .section-description {
            color: #64748b;

            font-size: 13px;

            line-height: 1.6;

            margin-bottom: 18px;
        }

        /* ====================================================
           PREVIEW
        ==================================================== */

        .preview-wrapper {
            position: sticky;
            top: 20px;
        }

        .preview-card {
            position: relative;
            overflow: hidden;

            background:
                radial-gradient(
                    circle at 100% 0%,
                    rgba(59,130,246,0.12),
                    transparent 30%
                ),
                linear-gradient(
                    145deg,
                    #ffffff,
                    #f8fafc
                );

            border: 1px solid #dbe3ee;

            border-radius: 24px;

            padding: 28px;

            box-shadow:
                0 25px 50px rgba(15,23,42,0.12),
                0 5px 12px rgba(15,23,42,0.05);
        }

        .preview-top {
            display: flex;

            align-items: center;

            justify-content: space-between;

            margin-bottom: 22px;
        }

        .preview-label {
            color: #64748b;

            font-size: 11px;

            font-weight: 800;

            text-transform: uppercase;

            letter-spacing: 0.10em;
        }

        .preview-live {
            padding: 5px 10px;

            border-radius: 999px;

            background: #ecfdf5;

            color: #15803d;

            font-size: 11px;

            font-weight: 700;

            border: 1px solid #bbf7d0;
        }

        .preview-title {
            font-size: 27px;

            font-weight: 850;

            color: #0f172a;

            line-height: 1.2;

            margin-bottom: 9px;
        }

        .preview-company {
            font-size: 14px;

            color: #475569;

            font-weight: 650;

            margin-bottom: 22px;
        }

        /* ====================================================
           PREVIEW META
        ==================================================== */

        .preview-meta {
            display: flex;

            flex-direction: column;

            gap: 11px;

            margin-bottom: 22px;
        }

        .preview-meta-item {
            display: flex;

            align-items: center;

            gap: 12px;

            color: #334155;

            font-size: 13px;

            padding: 8px 0;
        }

        .preview-meta-icon {
            width: 34px;
            height: 34px;

            border-radius: 10px;

            display: flex;

            align-items: center;

            justify-content: center;

            background:
                linear-gradient(
                    145deg,
                    #f1f5f9,
                    #e2e8f0
                );

            box-shadow:
                0 4px 8px rgba(15,23,42,0.06);

            flex-shrink: 0;

            font-size: 15px;
        }

        /* ====================================================
           SKILLS
        ==================================================== */

        .skill-tag {
            display: inline-block;

            padding: 7px 11px;

            margin: 4px 4px 4px 0;

            border-radius: 999px;

            background:
                linear-gradient(
                    145deg,
                    #eff6ff,
                    #dbeafe
                );

            color: #1d4ed8;

            border: 1px solid #bfdbfe;

            font-size: 11px;

            font-weight: 700;

            box-shadow:
                0 3px 7px rgba(37,99,235,0.08);
        }

        .preview-description {
            color: #475569;

            font-size: 13px;

            line-height: 1.75;

            white-space: pre-wrap;
        }

        .preview-section-title {
            font-size: 14px;

            font-weight: 800;

            color: #0f172a;

            margin-bottom: 10px;
        }

        /* ====================================================
           INPUTS
        ==================================================== */

        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] {
            border-radius: 12px !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        /* ====================================================
           BUTTONS
        ==================================================== */

        .stButton > button {
            border-radius: 12px;

            min-height: 46px;

            font-weight: 700;

            transition:
                transform 0.15s ease,
                box-shadow 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);

            box-shadow:
                0 8px 18px rgba(15,23,42,0.10);
        }

        /* ====================================================
           SKILL INFO
        ==================================================== */

        .skill-counter {
            display: inline-block;

            margin-top: 8px;

            padding: 5px 10px;

            border-radius: 999px;

            background: #f1f5f9;

            color: #475569;

            font-size: 11px;

            font-weight: 700;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# HELPERS
# ============================================================

def parse_skills(raw_skills: str):
    """
    Convert comma-separated skills into a clean unique list.
    """

    if not raw_skills:
        return []

    skills = []

    for skill in raw_skills.split(","):

        skill = skill.strip()

        if (
            skill
            and skill.lower()
            not in {
                existing.lower()
                for existing in skills
            }
        ):
            skills.append(skill)

    return skills


def format_salary(min_salary, max_salary):
    """
    Format salary for preview.
    """

    if min_salary and max_salary:
        return (
            f"₹{min_salary:,.0f} – "
            f"₹{max_salary:,.0f}"
        )

    if min_salary:
        return f"₹{min_salary:,.0f}+"

    if max_salary:
        return f"Up to ₹{max_salary:,.0f}"

    return "Not disclosed"


def render_html(content):
    """
    Render custom HTML safely through Streamlit.
    """

    st.html(content)


# ============================================================
# PREVIEW
# ============================================================

def render_job_preview(
    company,
    title,
    location,
    employment_type,
    experience,
    education,
    salary_min,
    salary_max,
    description,
    skills,
):

    safe_company = html.escape(
        company or "Your Company"
    )

    safe_title = html.escape(
        title or "Your Job Title"
    )

    safe_location = html.escape(
        location or "Location"
    )

    safe_employment = html.escape(
        employment_type or "Employment Type"
    )

    safe_education = html.escape(
        education or "Education requirement"
    )

    safe_description = html.escape(
        description
        or "Your job description will appear here."
    )

    skill_html = ""

    if skills:

        skill_html = "".join(
            f'<span class="skill-tag">'
            f'{html.escape(skill)}'
            f'</span>'
            for skill in skills
        )

    else:

        skill_html = (
            '<span style="'
            'color:#94a3b8;'
            'font-size:12px;'
            '">'
            "No skills added yet"
            "</span>"
        )

    salary = html.escape(
        format_salary(
            salary_min,
            salary_max
        )
    )

    render_html(
        f"""
        <div class="preview-card">

            <div class="preview-top">

                <div class="preview-label">
                    Job Preview
                </div>

                <div class="preview-live">
                    ● Live Preview
                </div>

            </div>

            <div class="preview-title">
                {safe_title}
            </div>

            <div class="preview-company">
                🏢 {safe_company}
            </div>

            <div class="preview-meta">

                <div class="preview-meta-item">

                    <div class="preview-meta-icon">
                        📍
                    </div>

                    <span>
                        {safe_location}
                    </span>

                </div>

                <div class="preview-meta-item">

                    <div class="preview-meta-icon">
                        💼
                    </div>

                    <span>
                        {safe_employment}
                    </span>

                </div>

                <div class="preview-meta-item">

                    <div class="preview-meta-icon">
                        ⏱️
                    </div>

                    <span>
                        {experience:g} years experience
                    </span>

                </div>

                <div class="preview-meta-item">

                    <div class="preview-meta-icon">
                        🎓
                    </div>

                    <span>
                        {safe_education}
                    </span>

                </div>

                <div class="preview-meta-item">

                    <div class="preview-meta-icon">
                        💰
                    </div>

                    <span>
                        {salary}
                    </span>

                </div>

            </div>

            <hr style="
                border:none;
                border-top:1px solid #e2e8f0;
                margin:20px 0;
            ">

            <div class="preview-section-title">
                Required Skills
            </div>

            <div style="
                margin-bottom:24px;
            ">
                {skill_html}
            </div>

            <div class="preview-section-title">
                About the Role
            </div>

            <div class="preview-description">
                {safe_description}
            </div>

        </div>
        """
    )


# ============================================================
# MAIN PAGE
# ============================================================

def create_job_page():

    company_id = st.session_state.get(
        "company_id"
    )

    # --------------------------------------------------------
    # COMPANY CHECK
    # --------------------------------------------------------

    if not company_id:

        st.error(
            "No company profile found. "
            "Please select a company first."
        )

        if st.button(
            "🏢 Select Company",
            use_container_width=True
        ):

            st.session_state["page"] = (
                "company_selector"
            )

            st.rerun()

        return

    company = get_company(
        company_id
    )

    if not company:

        st.error(
            "Company profile could not be found."
        )

        if st.button(
            "🏠 Back to Home",
            use_container_width=True
        ):

            st.session_state["page"] = "home"

            st.rerun()

        return

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    render_html(
        """
        <div class="job-hero">

            <div class="step-badge">
                🏢 COMPANY WORKSPACE
                &nbsp; • &nbsp;
                JOB CREATION
            </div>

            <div class="job-hero-title">
                Create a New Job
            </div>

            <div class="job-hero-subtitle">
                Publish a structured opportunity and let
                CareerIQ help you discover candidates whose
                skills, education and experience match the role.
            </div>

        </div>
        """
    )

    # --------------------------------------------------------
    # MAIN LAYOUT
    # --------------------------------------------------------

    left_col, right_col = st.columns(
        [1.55, 1],
        gap="large"
    )

    # ========================================================
    # LEFT — FORM
    # ========================================================

    with left_col:

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        render_html(
            """
            <div class="section-card">

                <div class="section-icon">
                    📋
                </div>

                <div class="section-title">
                    Basic Information
                </div>

                <div class="section-description">
                    Add the core information candidates
                    will see first.
                </div>

            </div>
            """
        )

        job_title = st.text_input(
            "Job Title *",
            placeholder=(
                "e.g. Machine Learning Engineer"
            ),
            key="create_job_title",
        )

        location = st.text_input(
            "Location *",
            placeholder=(
                "e.g. Pune, Maharashtra / Remote"
            ),
            key="create_job_location",
        )

        employment_type = st.selectbox(
            "Employment Type *",
            [
                "Full-time",
                "Part-time",
                "Internship",
                "Contract",
                "Freelance",
            ],
            key="create_job_employment_type",
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                margin-top:28px;
                margin-bottom:12px;
            ">

                <div class="section-icon">
                    📝
                </div>

                <div class="section-title">
                    Job Description
                </div>

                <div class="section-description">
                    Clearly explain the role, responsibilities
                    and expectations.
                </div>

            </div>
            """
        )

        description = st.text_area(
            "Description *",
            placeholder=(
                "Describe the role, responsibilities, "
                "technologies and expectations..."
            ),
            height=220,
            key="create_job_description",
        )

        # ----------------------------------------------------
        # REQUIREMENTS
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                margin-top:28px;
                margin-bottom:12px;
            ">

                <div class="section-icon">
                    🎯
                </div>

                <div class="section-title">
                    Candidate Requirements
                </div>

                <div class="section-description">
                    Define the experience, education and
                    technical skills required.
                </div>

            </div>
            """
        )

        experience_required = st.number_input(
            "Experience Required (years)",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=0.5,
            key="create_job_experience",
        )

        education_required = st.selectbox(
            "Minimum Education",
            [
                "Any",
                "Diploma",
                "Bachelor's Degree",
                "Master's Degree",
                "PhD",
            ],
            key="create_job_education",
        )

        required_skills_text = st.text_input(
            "Required Skills *",
            placeholder=(
                "Python, Machine Learning, SQL, "
                "TensorFlow, Docker"
            ),
            key="create_job_skills",
        )

        st.caption(
            "Enter skills separated by commas."
        )

        skills = parse_skills(
            required_skills_text
        )

        if skills:

            st.markdown(
                "**Selected Skills**"
            )

            skill_columns = st.columns(
                min(len(skills), 4)
            )

            for index, skill in enumerate(skills):

                with skill_columns[
                    index % len(skill_columns)
                ]:

                    st.success(skill)

            st.markdown(
                f"""
                <span class="skill-counter">
                    {len(skills)} skills added
                </span>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # COMPENSATION
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                margin-top:30px;
                margin-bottom:12px;
            ">

                <div class="section-icon">
                    💰
                </div>

                <div class="section-title">
                    Compensation
                </div>

                <div class="section-description">
                    Salary information is optional and
                    can be hidden from candidates.
                </div>

            </div>
            """
        )

        salary_col1, salary_col2 = st.columns(2)

        with salary_col1:

            salary_min = st.number_input(
                "Minimum Salary (₹ / year)",
                min_value=0.0,
                max_value=100000000.0,
                value=0.0,
                step=50000.0,
                key="create_job_salary_min",
            )

        with salary_col2:

            salary_max = st.number_input(
                "Maximum Salary (₹ / year)",
                min_value=0.0,
                max_value=100000000.0,
                value=0.0,
                step=50000.0,
                key="create_job_salary_max",
            )

        # ----------------------------------------------------
        # PUBLISHING
        # ----------------------------------------------------

        render_html(
            """
            <div style="
                margin-top:30px;
                margin-bottom:12px;
            ">

                <div class="section-icon">
                    🚦
                </div>

                <div class="section-title">
                    Publishing
                </div>

                <div class="section-description">
                    Choose whether candidates can see
                    this job immediately.
                </div>

            </div>
            """
        )

        status = st.radio(
            "Job Status",
            [
                "Active",
                "Draft",
            ],
            horizontal=True,
            key="create_job_status",
        )

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )

        save_col, cancel_col = st.columns(2)

        with save_col:

            save_clicked = st.button(
                "🚀 Create Job",
                type="primary",
                use_container_width=True,
            )

        with cancel_col:

            cancel_clicked = st.button(
                "← Back to Dashboard",
                use_container_width=True,
            )

        if cancel_clicked:

            st.session_state["page"] = (
                "company_dashboard"
            )

            st.rerun()

        # ----------------------------------------------------
        # SAVE JOB
        # ----------------------------------------------------

        if save_clicked:

            errors = []

            if not job_title.strip():

                errors.append(
                    "Job title is required."
                )

            if not location.strip():

                errors.append(
                    "Location is required."
                )

            if not description.strip():

                errors.append(
                    "Job description is required."
                )

            if not skills:

                errors.append(
                    "Please add at least one required skill."
                )

            if (
                salary_min > 0
                and salary_max > 0
                and salary_min > salary_max
            ):

                errors.append(
                    "Minimum salary cannot be greater "
                    "than maximum salary."
                )

            if errors:

                for error in errors:

                    st.error(error)

            else:

                education_value = (
                    ""
                    if education_required == "Any"
                    else education_required
                )

                job = Job(
                    company_id=company_id,
                    title=job_title.strip(),
                    description=description.strip(),
                    location=location.strip(),
                    employment_type=employment_type,
                    experience_required=float(
                        experience_required
                    ),
                    education_required=education_value,
                    salary_min=(
                        float(salary_min)
                        if salary_min > 0
                        else None
                    ),
                    salary_max=(
                        float(salary_max)
                        if salary_max > 0
                        else None
                    ),
                    status=status.lower(),
                    skills=skills,
                )

                try:

                    job_id = save_job(
                        job
                    )

                    st.session_state[
                        "last_created_job_id"
                    ] = job_id

                    st.session_state[
                        "job_created"
                    ] = True

                    st.success(
                        f"Job created successfully! "
                        f"Job ID: {job_id}"
                    )

                    st.session_state[
                        "page"
                    ] = "company_dashboard"

                    st.rerun()

                except Exception as error:

                    st.error(
                        f"Could not create job: {error}"
                    )

    # ========================================================
    # RIGHT — LIVE PREVIEW
    # ========================================================

    with right_col:

        render_html(
            """
            <div style="
                font-size:20px;
                font-weight:800;
                color:#0f172a;
                margin-bottom:7px;
            ">
                👀 Live Preview
            </div>

            <div style="
                color:#64748b;
                font-size:13px;
                line-height:1.6;
                margin-bottom:18px;
            ">
                See how candidates will view your job
                while you create it.
            </div>
            """
        )

        render_job_preview(
            company=company.company_name,
            title=job_title,
            location=location,
            employment_type=employment_type,
            experience=experience_required,
            education=education_required,
            salary_min=salary_min,
            salary_max=salary_max,
            description=description,
            skills=skills,
        )


# ============================================================
# ENTRY POINT
# ============================================================

def create_job():

    style_create_job_page()

    create_job_page()