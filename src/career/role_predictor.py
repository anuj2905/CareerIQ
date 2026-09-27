from typing import Any, Dict, List, Optional


# ============================================================
# CAREER ROLE REQUIREMENTS
# ============================================================

ROLE_REQUIREMENTS = {

    "Machine Learning Engineer": {

        "description": (
            "Build, train, evaluate, and deploy machine learning "
            "models and intelligent systems."
        ),

        "skills": [
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

        "keywords": [
            "machine learning",
            "ml model",
            "prediction",
            "classification",
            "regression",
            "model training",
            "model deployment",
            "machine learning model",
        ],
    },

    "AI Engineer": {

        "description": (
            "Build AI applications using machine learning, "
            "deep learning, LLMs, Generative AI, RAG, "
            "and AI agents."
        ),

        "skills": [
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

        "keywords": [
            "artificial intelligence",
            "ai application",
            "generative ai",
            "large language model",
            "llm",
            "rag",
            "chatbot",
            "ai assistant",
            "ai agent",
            "natural language processing",
        ],
    },

    "Data Scientist": {

        "description": (
            "Analyze data and build statistical and machine "
            "learning solutions to solve business problems."
        ),

        "skills": [
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

        "keywords": [
            "data analysis",
            "data science",
            "statistical analysis",
            "exploratory data analysis",
            "eda",
            "data visualization",
            "prediction",
            "analytics",
        ],
    },

    "Backend Developer": {

        "description": (
            "Build scalable backend systems, APIs, databases, "
            "authentication systems, and server-side applications."
        ),

        "skills": [
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

        "keywords": [
            "backend",
            "backend development",
            "api",
            "rest api",
            "server",
            "server-side",
            "database",
            "authentication",
            "web application",
        ],
    },
}


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "python": {
        "python",
    },

    "sql": {
        "sql",
        "structured query language",
    },

    "machine learning": {
        "machine learning",
        "ml",
        "machine-learning",
    },

    "deep learning": {
        "deep learning",
        "dl",
        "deep-learning",
    },

    "numpy": {
        "numpy",
    },

    "pandas": {
        "pandas",
    },

    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn",
        "scikit",
    },

    "tensorflow": {
        "tensorflow",
        "tensorflow keras",
        "tf",
    },

    "pytorch": {
        "pytorch",
        "torch",
    },

    "javascript": {
        "javascript",
        "js",
    },

    "node.js": {
        "node.js",
        "nodejs",
        "node js",
    },

    "express.js": {
        "express.js",
        "expressjs",
        "express js",
    },

    "mongodb": {
        "mongodb",
        "mongo db",
        "mongo",
    },

    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "restful services",
    },

    "fastapi": {
        "fastapi",
        "fast api",
    },

    "docker": {
        "docker",
        "docker containers",
        "containerization",
    },

    "git": {
        "git",
    },

    "llms": {
        "llm",
        "llms",
        "large language model",
        "large language models",
    },

    "generative ai": {
        "generative ai",
        "gen ai",
        "genai",
        "generative artificial intelligence",
    },

    "rag": {
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
    },

    "nlp": {
        "nlp",
        "natural language processing",
    },

    "data visualization": {
        "data visualization",
        "data visualisation",
    },

    "statistics": {
        "statistics",
        "statistical analysis",
        "statistical methods",
    },
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(
    value: Any
) -> str:
    """
    Normalize text for comparison.
    """

    if value is None:
        return ""

    return " ".join(
        str(value)
        .lower()
        .strip()
        .split()
    )


def get_canonical_skill(
    skill: str
) -> str:
    """
    Convert aliases into canonical skill names.
    """

    normalized = normalize_text(
        skill
    )

    if not normalized:
        return ""

    for canonical, aliases in SKILL_ALIASES.items():

        normalized_aliases = {
            normalize_text(alias)
            for alias in aliases
        }

        if normalized in normalized_aliases:
            return canonical

    return normalized


# ============================================================
# PROFILE HELPERS
# ============================================================

def get_profile_value(
    profile: Any,
    field_name: str,
    default=None
):
    """
    Read a field from:

        1. Pydantic model
        2. Dictionary
    """

    if profile is None:
        return default

    if isinstance(
        profile,
        dict
    ):

        return profile.get(
            field_name,
            default
        )

    return getattr(
        profile,
        field_name,
        default
    )


def normalize_list(
    values
) -> List[str]:
    """
    Convert different input formats into a clean list.
    """

    if not values:
        return []

    if isinstance(
        values,
        str
    ):

        return (
            [values.strip()]
            if values.strip()
            else []
        )

    if isinstance(
        values,
        (list, tuple, set)
    ):

        return [
            str(value).strip()
            for value in values
            if str(value).strip()
        ]

    return [
        str(values).strip()
    ]


# ============================================================
# PROFILE TEXT
# ============================================================

def build_profile_text(
    profile: Any
) -> str:
    """
    Build searchable profile text.

    Includes:

        Education
        Projects
        Experience
        Certifications
        Structured experience
    """

    sections = []

    fields = [
        "education",
        "projects",
        "experience",
        "certifications",
    ]

    for field in fields:

        values = get_profile_value(
            profile,
            field,
            []
        )

        values = normalize_list(
            values
        )

        if values:
            sections.extend(
                values
            )

    # --------------------------------------------------------
    # Structured experience
    # --------------------------------------------------------

    experience_details = get_profile_value(
        profile,
        "experience_details",
        []
    )

    if experience_details:

        for experience in experience_details:

            if isinstance(
                experience,
                dict
            ):

                values = [
                    experience.get(
                        "job_title",
                        ""
                    ),

                    experience.get(
                        "company",
                        ""
                    ),

                    experience.get(
                        "employment_type",
                        ""
                    ),

                    experience.get(
                        "responsibilities",
                        []
                    ),

                    experience.get(
                        "technologies",
                        []
                    ),
                ]

            else:

                values = [
                    getattr(
                        experience,
                        "job_title",
                        ""
                    ),

                    getattr(
                        experience,
                        "company",
                        ""
                    ),

                    getattr(
                        experience,
                        "employment_type",
                        ""
                    ),

                    getattr(
                        experience,
                        "responsibilities",
                        []
                    ),

                    getattr(
                        experience,
                        "technologies",
                        []
                    ),
                ]

            for value in values:

                if isinstance(
                    value,
                    (list, tuple, set)
                ):

                    sections.extend(
                        normalize_list(
                            value
                        )
                    )

                elif value:

                    sections.append(
                        str(value)
                    )

    return normalize_text(
        " ".join(
            sections
        )
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(
    user_skills,
    required_skills
) -> Dict[str, Any]:
    """
    Calculate skill coverage for a role.
    """

    user_skills = normalize_list(
        user_skills
    )

    required_skills = normalize_list(
        required_skills
    )

    user_skill_map = {}

    for skill in user_skills:

        canonical = get_canonical_skill(
            skill
        )

        if canonical:

            user_skill_map[
                canonical
            ] = skill

    required_skill_map = {}

    for skill in required_skills:

        canonical = get_canonical_skill(
            skill
        )

        if canonical:

            required_skill_map[
                canonical
            ] = skill

    if not required_skill_map:

        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched_skills = []

    missing_skills = []

    for canonical, original_skill in (
        required_skill_map.items()
    ):

        if canonical in user_skill_map:

            matched_skills.append(
                original_skill
            )

        else:

            missing_skills.append(
                original_skill
            )

    score = (
        len(matched_skills)
        / len(required_skill_map)
    )

    return {

        "score": round(
            score,
            4
        ),

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,
    }


# ============================================================
# KEYWORD EVIDENCE
# ============================================================

def calculate_keyword_score(
    profile: Any,
    keywords: List[str]
) -> Dict[str, Any]:
    """
    Calculate role-related textual evidence.
    """

    profile_text = build_profile_text(
        profile
    )

    if (
        not profile_text
        or not keywords
    ):

        return {
            "score": 0.0,
            "matched_keywords": [],
        }

    matched_keywords = []

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if (
            normalized_keyword
            and normalized_keyword in profile_text
        ):

            matched_keywords.append(
                keyword
            )

    score = (
        len(matched_keywords)
        / len(keywords)
    )

    return {

        "score": round(
            min(
                score,
                1.0
            ),
            4
        ),

        "matched_keywords":
            matched_keywords,
    }


# ============================================================
# PROJECT EVIDENCE
# ============================================================

def calculate_project_evidence(
    profile: Any,
    keywords: List[str]
) -> Dict[str, Any]:
    """
    Analyze project descriptions separately.

    This prevents project evidence from being hidden
    inside the general profile score.
    """

    projects = get_profile_value(
        profile,
        "projects",
        []
    )

    projects = normalize_list(
        projects
    )

    if not projects:

        return {
            "score": 0.0,
            "matched_keywords": [],
        }

    project_text = normalize_text(
        " ".join(projects)
    )

    matched_keywords = []

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if (
            normalized_keyword
            and normalized_keyword in project_text
        ):

            matched_keywords.append(
                keyword
            )

    score = (
        len(matched_keywords)
        / len(keywords)
        if keywords
        else 0.0
    )

    return {

        "score": round(
            min(
                score,
                1.0
            ),
            4
        ),

        "matched_keywords":
            matched_keywords,
    }


# ============================================================
# EXPERIENCE EVIDENCE
# ============================================================

def calculate_experience_evidence(
    profile: Any,
    keywords: List[str]
) -> Dict[str, Any]:
    """
    Analyze structured and legacy experience
    for role-related evidence.
    """

    experience_parts = []

    experience = get_profile_value(
        profile,
        "experience",
        []
    )

    experience_parts.extend(
        normalize_list(
            experience
        )
    )

    experience_details = get_profile_value(
        profile,
        "experience_details",
        []
    )

    for entry in experience_details:

        if isinstance(
            entry,
            dict
        ):

            values = [

                entry.get(
                    "job_title",
                    ""
                ),

                entry.get(
                    "company",
                    ""
                ),

                entry.get(
                    "employment_type",
                    ""
                ),

                entry.get(
                    "responsibilities",
                    []
                ),

                entry.get(
                    "technologies",
                    []
                ),
            ]

        else:

            values = [

                getattr(
                    entry,
                    "job_title",
                    ""
                ),

                getattr(
                    entry,
                    "company",
                    ""
                ),

                getattr(
                    entry,
                    "employment_type",
                    ""
                ),

                getattr(
                    entry,
                    "responsibilities",
                    []
                ),

                getattr(
                    entry,
                    "technologies",
                    []
                ),
            ]

        for value in values:

            if isinstance(
                value,
                (list, tuple, set)
            ):

                experience_parts.extend(
                    normalize_list(
                        value
                    )
                )

            elif value:

                experience_parts.append(
                    str(value)
                )

    experience_text = normalize_text(
        " ".join(
            experience_parts
        )
    )

    if not experience_text:

        return {
            "score": 0.0,
            "matched_keywords": [],
        }

    matched_keywords = []

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if (
            normalized_keyword
            and normalized_keyword in experience_text
        ):

            matched_keywords.append(
                keyword
            )

    score = (
        len(matched_keywords)
        / len(keywords)
        if keywords
        else 0.0
    )

    return {

        "score": round(
            min(
                score,
                1.0
            ),
            4
        ),

        "matched_keywords":
            matched_keywords,
    }


# ============================================================
# EDUCATION EVIDENCE
# ============================================================

def calculate_education_evidence(
    profile: Any,
    keywords: List[str]
) -> Dict[str, Any]:
    """
    Analyze education-related evidence.
    """

    education = get_profile_value(
        profile,
        "education",
        []
    )

    education = normalize_list(
        education
    )

    if not education:

        return {
            "score": 0.0,
            "matched_keywords": [],
        }

    education_text = normalize_text(
        " ".join(
            education
        )
    )

    matched_keywords = []

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if (
            normalized_keyword
            and normalized_keyword in education_text
        ):

            matched_keywords.append(
                keyword
            )

    score = (
        len(matched_keywords)
        / len(keywords)
        if keywords
        else 0.0
    )

    return {

        "score": round(
            min(
                score,
                1.0
            ),
            4
        ),

        "matched_keywords":
            matched_keywords,
    }


# ============================================================
# ROLE SCORE
# ============================================================

def calculate_role_score(
    profile: Any,
    role_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate role-fit score.

    Current weighting:

        Skills              = 60%
        Project Evidence    = 15%
        Experience Evidence = 15%
        Education Evidence  = 10%

    This keeps technical skills as the strongest signal
    while allowing the rest of the resume to contribute.
    """

    user_skills = get_profile_value(
        profile,
        "skills",
        []
    )

    skill_result = calculate_skill_match(
        user_skills=user_skills,
        required_skills=role_data[
            "skills"
        ]
    )

    keyword_result = calculate_keyword_score(
        profile=profile,
        keywords=role_data[
            "keywords"
        ]
    )

    project_result = calculate_project_evidence(
        profile=profile,
        keywords=role_data[
            "keywords"
        ]
    )

    experience_result = calculate_experience_evidence(
        profile=profile,
        keywords=role_data[
            "keywords"
        ]
    )

    education_result = calculate_education_evidence(
        profile=profile,
        keywords=role_data[
            "keywords"
        ]
    )

    skill_score = skill_result[
        "score"
    ]

    project_score = project_result[
        "score"
    ]

    experience_score = experience_result[
        "score"
    ]

    education_score = education_result[
        "score"
    ]

    overall_score = (

        skill_score * 0.60

        + project_score * 0.15

        + experience_score * 0.15

        + education_score * 0.10
    )

    # --------------------------------------------------------
    # Combined evidence for compatibility with existing UI
    # --------------------------------------------------------

    evidence_score = (

        project_score * 0.375

        + experience_score * 0.375

        + education_score * 0.25
    )

    matched_keywords = list(
        dict.fromkeys(

            project_result[
                "matched_keywords"
            ]

            + experience_result[
                "matched_keywords"
            ]

            + education_result[
                "matched_keywords"
            ]
        )
    )

    return {

        "score": round(
            overall_score,
            4
        ),

        "skill_match": round(
            skill_score,
            4
        ),

        "evidence_score": round(
            evidence_score,
            4
        ),

        "project_evidence": round(
            project_score,
            4
        ),

        "experience_evidence": round(
            experience_score,
            4
        ),

        "education_evidence": round(
            education_score,
            4
        ),

        "matched_skills":
            skill_result[
                "matched_skills"
            ],

        "missing_skills":
            skill_result[
                "missing_skills"
            ],

        "matched_keywords":
            matched_keywords,
    }


# ============================================================
# CAREER ROLE PREDICTION
# ============================================================

def predict_career_roles(
    profile: Any,
    top_k: int = 4
) -> List[Dict[str, Any]]:
    """
    Predict career roles from the student's profile.

    Returns roles sorted by role-fit score.
    """

    if profile is None:

        raise ValueError(
            "Resume profile is required."
        )

    user_skills = get_profile_value(
        profile,
        "skills",
        []
    )

    user_skills = normalize_list(
        user_skills
    )

    if not user_skills:

        return []

    predictions = []

    for role_name, role_data in (
        ROLE_REQUIREMENTS.items()
    ):

        result = calculate_role_score(
            profile=profile,
            role_data=role_data
        )

        predictions.append({

            "role":
                role_name,

            "score":
                result["score"],

            "skill_match":
                result["skill_match"],

            "evidence_score":
                result["evidence_score"],

            "project_evidence":
                result["project_evidence"],

            "experience_evidence":
                result["experience_evidence"],

            "education_evidence":
                result["education_evidence"],

            "description":
                role_data["description"],

            "required_skills":
                role_data["skills"],

            "matched_skills":
                result["matched_skills"],

            "missing_skills":
                result["missing_skills"],

            "matched_keywords":
                result["matched_keywords"],
        })

    predictions.sort(
        key=lambda item: item[
            "score"
        ],
        reverse=True
    )

    return predictions[
        :max(1, top_k)
    ]


# ============================================================
# GET TOP CAREER ROLE
# ============================================================

def get_top_career_role(
    profile: Any
) -> Optional[Dict[str, Any]]:
    """
    Return the highest-scoring role.
    """

    predictions = predict_career_roles(
        profile=profile,
        top_k=1
    )

    if not predictions:

        return None

    return predictions[0]


# ============================================================
# FORMAT SCORE
# ============================================================

def format_role_score(
    score: float
) -> str:
    """
    Convert a 0-1 score into percentage text.
    """

    score = max(
        0.0,
        min(
            float(score),
            1.0
        )
    )

    return (
        f"{score * 100:.1f}%"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_profile = {

        "name":
            "Anuj Patil",

        "education": [

            "B.E. in Computer Engineering, "
            "Atharva College of Engineering"
        ],

        "skills": [

            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "FastAPI",
            "Git",
            "OpenCV",
            "Streamlit"
        ],

        "projects": [

            "AI Attendance System using Python "
            "and OpenCV",

            "Text Summarization using "
            "Hugging Face T5",

            "CareerIQ AI Resume Analyzer"
        ],

        "experience": [

            "Machine Learning Intern"
        ],

        "experience_details": [

            {
                "job_title":
                    "Machine Learning Intern",

                "company":
                    "ABC Technologies",

                "employment_type":
                    "Internship",

                "location":
                    "Pune, India",

                "start_date":
                    "January 2026",

                "end_date":
                    "June 2026",

                "duration":
                    "6 months",

                "responsibilities": [

                    "Built machine learning models.",

                    "Performed data preprocessing."
                ],

                "technologies": [

                    "Python",
                    "Pandas",
                    "NumPy",
                    "Scikit-learn",
                    "OpenCV"
                ]
            }
        ],

        "certifications": [

            "Machine Learning Certification",

            "Python Certification"
        ],
    }

    predictions = predict_career_roles(
        profile=test_profile,
        top_k=4
    )

    print()

    print(
        "=" * 65
    )

    print(
        "          CAREERIQ CAREER ROLE PREDICTION"
    )

    print(
        "=" * 65
    )

    for index, prediction in enumerate(
        predictions,
        start=1
    ):

        print()

        print(
            f"{index}. "
            f"{prediction['role']}"
        )

        print(
            "   Role Fit: ",
            format_role_score(
                prediction["score"]
            )
        )

        print(
            "   Skill Match: ",
            format_role_score(
                prediction["skill_match"]
            )
        )

        print(
            "   Project Evidence: ",
            format_role_score(
                prediction["project_evidence"]
            )
        )

        print(
            "   Experience Evidence: ",
            format_role_score(
                prediction["experience_evidence"]
            )
        )

        print(
            "   Education Evidence: ",
            format_role_score(
                prediction["education_evidence"]
            )
        )

        print(
            "   Matched Skills: ",
            ", ".join(
                prediction[
                    "matched_skills"
                ]
            )
        )

        print(
            "   Missing Skills: ",
            ", ".join(
                prediction[
                    "missing_skills"
                ]
            )
        )

        print(
            "   Matched Keywords: ",
            ", ".join(
                prediction[
                    "matched_keywords"
                ]
            )
        )

    print()

    print(
        "=" * 65
    )