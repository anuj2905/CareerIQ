import html
import re
import streamlit as st

from src.career.salary_predictor import (
    predict_salary,
    is_model_available,
)


# ============================================================
# DOMAIN → ROLE → REQUIRED SKILLS
# ============================================================

DOMAIN_ROLE_SKILLS = {
    "AI / Machine Learning": {
        "Machine Learning Engineer": [
            "Python",
            "SQL",
            "Machine Learning",
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "TensorFlow",
            "PyTorch",
            "Git",
            "Docker",
            "FastAPI",
            "MLflow",
        ],
        "AI Engineer": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "PyTorch",
            "TensorFlow",
            "NLP",
            "LLMs",
            "Generative AI",
            "RAG",
            "Git",
            "Docker",
            "FastAPI",
        ],
    },

    "Data Science": {
        "Data Scientist": [
            "Python",
            "SQL",
            "Statistics",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "Machine Learning",
            "Data Visualization",
            "Git",
        ],
    },

    "Software Development": {
        "Backend Developer": [
            "Python",
            "JavaScript",
            "Node.js",
            "Express.js",
            "SQL",
            "MongoDB",
            "REST API",
            "Git",
            "Docker",
        ],
        "Software Engineer": [
            "Python",
            "Java",
            "SQL",
            "Data Structures",
            "Algorithms",
            "Git",
            "REST API",
            "Docker",
        ],
    },

    "Web Development": {
        "Full Stack Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express.js",
            "SQL",
            "MongoDB",
            "Git",
        ],
        "Frontend Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "TypeScript",
            "Git",
        ],
    },

    "Cloud / DevOps": {
        "Cloud Engineer": [
            "AWS",
            "Azure",
            "Linux",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Git",
            "Python",
        ],
        "DevOps Engineer": [
            "Linux",
            "Docker",
            "Kubernetes",
            "CI/CD",
            "AWS",
            "Terraform",
            "Git",
            "Python",
        ],
    },

    "Data Engineering": {
        "Data Engineer": [
            "Python",
            "SQL",
            "ETL",
            "Pandas",
            "Spark",
            "Airflow",
            "Data Warehousing",
            "Git",
        ],
    },

    "Cybersecurity": {
        "Cybersecurity Analyst": [
            "Networking",
            "Linux",
            "Cybersecurity",
            "SIEM",
            "Python",
            "SQL",
            "Firewalls",
            "Git",
        ],
    },

    "QA / Testing": {
        "QA Engineer": [
            "Manual Testing",
            "Automation Testing",
            "Selenium",
            "Python",
            "SQL",
            "API Testing",
            "Git",
        ],
    },

    "Mobile Development": {
        "Mobile App Developer": [
            "Flutter",
            "Dart",
            "Android",
            "REST API",
            "Firebase",
            "Git",
        ],
    },

    "UI / UX": {
        "UI / UX Designer": [
            "Figma",
            "UI Design",
            "UX Design",
            "Wireframing",
            "Prototyping",
            "User Research",
        ],
    },

    "Product / Business Analytics": {
        "Business Analyst": [
            "SQL",
            "Excel",
            "Data Analysis",
            "Business Analysis",
            "Power BI",
            "Statistics",
        ],
        "Product Analyst": [
            "SQL",
            "Excel",
            "Data Analysis",
            "Statistics",
            "Product Analytics",
            "Power BI",
        ],
    },
}


# ============================================================
# RESUME SKILLS
# ============================================================

def _skills(profile):
    skills = getattr(profile, "skills", []) or []

    if isinstance(skills, str):
        skills = re.split(
            r"[,;\n|]+",
            skills,
        )

    return [
        str(x).strip()
        for x in skills
        if str(x).strip()
    ]


# ============================================================
# EXPERIENCE
# ============================================================

def _experience_years(profile):
    value = getattr(
        profile,
        "experience",
        [],
    ) or ""

    if isinstance(value, list):
        value = " ".join(
            str(x)
            for x in value
        )

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        str(value).lower(),
    )

    return max(
        (
            float(x)
            for x in matches
        ),
        default=0.0,
    )


# ============================================================
# SKILL MATCH
# ============================================================

def _match(
    student_skills,
    required,
):
    student = [
        re.sub(
            r"[^a-z0-9+#.]+",
            " ",
            x.lower(),
        ).strip()
        for x in student_skills
    ]

    matched = []
    missing = []

    for skill in required:

        target = re.sub(
            r"[^a-z0-9+#.]+",
            " ",
            skill.lower(),
        ).strip()

        if any(
            target == x
            or target in x
            or x in target
            for x in student
        ):
            matched.append(skill)

        else:
            missing.append(skill)

    pct = (
        len(matched) / len(required) * 100
        if required
        else 0.0
    )

    return pct, matched, missing


# ============================================================
# MONEY FORMAT
# ============================================================

def _money(value):
    return f"₹{float(value):,.0f}"


# ============================================================
# SALARY PREDICTION PAGE
# ============================================================

def salary_prediction_page():

    profile = st.session_state.get(
        "profile"
    )

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.html("""
    <div style="margin-bottom:28px;">

        <div style="
            font-size:12px;
            color:#ff5a36;
            font-weight:850;
            letter-spacing:1px;
        ">
            CAREERIQ / SALARY INTELLIGENCE
        </div>

        <div style="
            font-size:38px;
            font-weight:850;
            color:#073b5c;
            margin-top:7px;
        ">
            💰 Salary Prediction
        </div>

        <div style="
            color:#627586;
            margin-top:6px;
            font-size:14px;
        ">
            Estimate salary from your resume skills,
            target domain, role, location and experience.
        </div>

    </div>
    """)

    # --------------------------------------------------------
    # MODEL CHECK
    # --------------------------------------------------------

    if not is_model_available():

        st.error(
            "Salary prediction model is not available."
        )

        return

    # --------------------------------------------------------
    # PROFILE CHECK
    # --------------------------------------------------------

    if profile is None:

        st.warning(
            "Please upload and analyze your resume first."
        )

        if st.button(
            "📄 Upload & Analyze Resume",
            type="primary",
            use_container_width=True,
        ):

            st.session_state[
                "student_feature"
            ] = "📄 Resume Overview"

            st.session_state[
                "page"
            ] = "resume"

            st.rerun()

        return

    # --------------------------------------------------------
    # RESUME DATA
    # --------------------------------------------------------

    student_skills = _skills(
        profile
    )

    default_exp = min(
        _experience_years(profile),
        30.0,
    )

    # --------------------------------------------------------
    # INPUT SECTION
    # --------------------------------------------------------

    left, right = st.columns(
        [1, 1],
        gap="large",
    )

    with left:

        domain = st.selectbox(
            "Domain",
            list(DOMAIN_ROLE_SKILLS),
            key="salary_domain",
        )

        role = st.selectbox(
            "Role",
            list(
                DOMAIN_ROLE_SKILLS[domain]
            ),
            key="salary_role",
        )

        location = st.selectbox(
            "Location",
            [
                "Pune, Maharashtra",
                "Mumbai, Maharashtra",
                "Bengaluru, Karnataka",
                "Hyderabad, Telangana",
                "Chennai, Tamil Nadu",
                "Delhi NCR",
                "Other / India",
            ],
            key="salary_location",
        )

        experience_years = st.number_input(
            "Experience (years)",
            0.0,
            30.0,
            float(default_exp),
            0.5,
            key="salary_experience",
        )

    # --------------------------------------------------------
    # REQUIRED SKILLS
    # --------------------------------------------------------

    required = DOMAIN_ROLE_SKILLS[
        domain
    ][role]

    with right:

        st.subheader(
            "🎯 Required Skills"
        )

        cols = st.columns(3)

        for i, skill in enumerate(required):

            with cols[i % 3]:

                st.write(
                    f"• {skill}"
                )

    # --------------------------------------------------------
    # SKILL MATCH
    # --------------------------------------------------------

    pct, matched, missing = _match(
        student_skills,
        required,
    )

    st.divider()

    a, b, c = st.columns(3)

    a.metric(
        "Skill Match",
        f"{pct:.1f}%",
    )

    b.metric(
        "Matched Skills",
        len(matched),
    )

    c.metric(
        "Missing Skills",
        len(missing),
    )

    st.progress(
        max(
            0.0,
            min(
                pct / 100.0,
                1.0,
            ),
        )
    )

    x, y = st.columns(2)

    x.success(
        "Matched: "
        + (
            ", ".join(matched)
            or "None"
        )
    )

    y.warning(
        "Missing: "
        + (
            ", ".join(missing)
            or "None"
        )
    )

    # --------------------------------------------------------
    # PREDICT SALARY
    # --------------------------------------------------------

    if st.button(
        "💰 Predict Salary",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Predicting salary..."
        ):

            try:

                result = predict_salary(
                    domain=domain,
                    role=role,
                    location=location,
                    experience_years=experience_years,
                    student_skills=student_skills,
                    required_skills=required,
                )

                if not result.get(
                    "success",
                    False,
                ):

                    st.error(
                        result.get(
                            "error",
                            "Salary prediction failed.",
                        )
                    )

                else:

                    # Save complete backend result.
                    st.session_state[
                        "salary_prediction_result"
                    ] = result

            except Exception as exc:

                st.error(
                    f"Salary prediction failed: {exc}"
                )

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    result = st.session_state.get(
        "salary_prediction_result"
    )

    if not result:
        return

    # ========================================================
    # IMPORTANT:
    # salary_predictor.py returns nested dictionaries:
    #
    # result["salary_prediction"]
    # result["skill_match"]
    #
    # Therefore we must read those nested values.
    # ========================================================

    salary_data = result.get(
        "salary_prediction",
        {},
    )

    skill_data = result.get(
        "skill_match",
        {},
    )

    # --------------------------------------------------------
    # BACKEND SALARY VALUES
    # --------------------------------------------------------

    predicted = salary_data.get(
        "predicted_salary",
        result.get(
            "predicted_salary",
            0,
        ),
    )

    minimum = salary_data.get(
        "lower_salary",
        result.get(
            "salary_range_min",
            0,
        ),
    )

    maximum = salary_data.get(
        "upper_salary",
        result.get(
            "salary_range_max",
            0,
        ),
    )

    result_skill_match = skill_data.get(
        "percentage",
        result.get(
            "skill_match_percentage",
            pct,
        ),
    )

    # --------------------------------------------------------
    # RESULT SECTION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "📈 Salary Prediction Result"
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Predicted Salary",
        _money(predicted),
    )

    r2.metric(
        "Estimated Range",
        f"{_money(minimum)} – {_money(maximum)}",
    )

    r3.metric(
        "Skill Match",
        f"{float(result_skill_match):.1f}%",
    )

    # --------------------------------------------------------
    # RESULT CARD
    # --------------------------------------------------------

    st.html(
        f"""
        <div style="
            margin-top:14px;
            padding:22px;
            border-radius:18px;
            border:1px solid rgba(139,92,246,.16);
            background:rgba(255,255,255,.82);
        ">

            <div style="
                font-size:12px;
                font-weight:850;
                color:#8b5cf6;
            ">
                {html.escape(domain.upper())}
            </div>

            <div style="
                font-size:27px;
                font-weight:850;
                color:#073b5c;
                margin-top:5px;
            ">
                {html.escape(role)}
            </div>

            <div style="
                color:#627586;
                margin-top:6px;
                font-size:13px;
            ">
                {html.escape(location)}
                •
                {experience_years:.1f}
                years experience
            </div>

            <div style="
                color:#627586;
                margin-top:12px;
                font-size:12px;
                line-height:1.6;
            ">
                The displayed range is a presentation range
                around the model prediction, not a statistical
                confidence interval.
            </div>

        </div>
        """
    )