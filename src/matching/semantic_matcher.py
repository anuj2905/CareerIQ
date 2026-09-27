from typing import Any, Dict, List

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: Any) -> str:
    """
    Normalize arbitrary input into clean lowercase text.
    """

    if text is None:
        return ""

    if isinstance(text, str):
        value = text

    elif isinstance(text, (list, tuple, set)):
        value = " ".join(
            str(item)
            for item in text
            if item is not None
        )

    elif isinstance(text, dict):
        value = " ".join(
            str(item)
            for item in text.values()
            if item is not None
        )

    else:
        value = str(text)

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9+#.\-/ ]+",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


# ============================================================
# LIST NORMALIZATION
# ============================================================

def normalize_list(values: Any) -> List[str]:
    """
    Convert different input formats into a clean list of strings.
    """

    if values is None:
        return []

    if isinstance(values, str):
        value = values.strip()

        return [value] if value else []

    if isinstance(values, (list, tuple, set)):
        result = []

        for value in values:
            if value is None:
                continue

            cleaned = str(value).strip()

            if cleaned:
                result.append(cleaned)

        return result

    return [str(values).strip()]


# ============================================================
# TEXT COMBINATION
# ============================================================

def combine_text(values: Any) -> str:
    """
    Combine multiple text values into one normalized document.
    """

    items = normalize_list(values)

    cleaned_items = []

    for item in items:
        normalized = normalize_text(item)

        if normalized:
            cleaned_items.append(normalized)

    return " ".join(cleaned_items)


# ============================================================
# TF-IDF SEMANTIC SIMILARITY
# ============================================================

def calculate_text_similarity(
    resume_text: str,
    job_text: str
) -> float:
    """
    Calculate semantic-style text similarity using TF-IDF
    and cosine similarity.

    Returns:
        float: similarity between 0.0 and 1.0
    """

    resume_text = normalize_text(resume_text)
    job_text = normalize_text(job_text)

    if not resume_text or not job_text:
        return 0.0

    if resume_text == job_text:
        return 1.0

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=5000
        )

        vectors = vectorizer.fit_transform(
            [resume_text, job_text]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            max(0.0, min(float(similarity), 1.0)),
            4
        )

    except ValueError:
        return 0.0


# ============================================================
# POSITION SIMILARITY
# ============================================================

def calculate_position_similarity(
    resume_position: Any,
    job_position: Any
) -> float:
    """
    Compare the candidate's position/title with the job title.
    """

    resume_position = normalize_text(
        resume_position
    )

    job_position = normalize_text(
        job_position
    )

    if not resume_position or not job_position:
        return 0.0

    return calculate_text_similarity(
        resume_position,
        job_position
    )


# ============================================================
# RESPONSIBILITY SIMILARITY
# ============================================================

def calculate_responsibility_similarity(
    resume_responsibilities: Any,
    job_responsibilities: Any
) -> float:
    """
    Compare candidate responsibilities with job responsibilities.
    """

    resume_text = combine_text(
        resume_responsibilities
    )

    job_text = combine_text(
        job_responsibilities
    )

    return calculate_text_similarity(
        resume_text,
        job_text
    )


# ============================================================
# PROJECT SIMILARITY
# ============================================================

def calculate_project_similarity(
    projects: Any,
    job_requirements: Any
) -> float:
    """
    Compare candidate projects with job requirements.

    Projects can be:
        - list[str]
        - string
        - dictionaries
    """

    project_text = combine_text(projects)
    requirement_text = combine_text(
        job_requirements
    )

    return calculate_text_similarity(
        project_text,
        requirement_text
    )


# ============================================================
# EXPERIENCE RELEVANCE
# ============================================================

def calculate_experience_relevance(
    resume_position: Any,
    resume_responsibilities: Any,
    job_position: Any,
    job_responsibilities: Any
) -> Dict[str, float]:
    """
    Calculate semantic relevance between candidate experience
    and job experience requirements.

    Weighting:

        Position similarity       = 40%
        Responsibility similarity = 60%
    """

    position_similarity = calculate_position_similarity(
        resume_position=resume_position,
        job_position=job_position
    )

    responsibility_similarity = (
        calculate_responsibility_similarity(
            resume_responsibilities=resume_responsibilities,
            job_responsibilities=job_responsibilities
        )
    )

    experience_relevance = (
        position_similarity * 0.40
        + responsibility_similarity * 0.60
    )

    return {
        "position_similarity": round(
            position_similarity,
            4
        ),
        "responsibility_similarity": round(
            responsibility_similarity,
            4
        ),
        "experience_relevance": round(
            max(
                0.0,
                min(
                    experience_relevance,
                    1.0
                )
            ),
            4
        )
    }


# ============================================================
# GENERAL JOB SEMANTIC MATCH
# ============================================================

def calculate_job_semantic_similarity(
    resume_text: Any,
    job_text: Any
) -> float:
    """
    Calculate overall semantic similarity between a candidate
    profile and a job description.
    """

    resume_document = combine_text(
        resume_text
    )

    job_document = combine_text(
        job_text
    )

    return calculate_text_similarity(
        resume_document,
        job_document
    )


# ============================================================
# COMPLETE SEMANTIC ANALYSIS
# ============================================================

def analyze_semantic_job_match(
    resume_profile: Dict[str, Any],
    job: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Perform semantic analysis between a resume profile
    and a job.

    Expected resume_profile fields can include:

        skills
        projects
        experience
        experience_details
        education

    Expected job fields can include:

        title
        position
        description
        responsibilities
        required_skills
        skills_required
        requirements
    """

    if not isinstance(resume_profile, dict):
        raise TypeError(
            "resume_profile must be a dictionary."
        )

    if not isinstance(job, dict):
        raise TypeError(
            "job must be a dictionary."
        )

    # --------------------------------------------------------
    # Candidate information
    # --------------------------------------------------------

    skills = resume_profile.get(
        "skills",
        []
    )

    projects = resume_profile.get(
        "projects",
        []
    )

    experience = resume_profile.get(
        "experience",
        []
    )

    experience_details = resume_profile.get(
        "experience_details",
        []
    )

    education = resume_profile.get(
        "education",
        []
    )

    # --------------------------------------------------------
    # Job information
    # --------------------------------------------------------

    job_title = job.get(
        "title",
        job.get(
            "position",
            ""
        )
    )

    job_description = job.get(
        "description",
        ""
    )

    job_responsibilities = job.get(
        "responsibilities",
        []
    )

    required_skills = job.get(
        "required_skills",
        job.get(
            "skills_required",
            []
        )
    )

    job_requirements = job.get(
        "requirements",
        []
    )

    # --------------------------------------------------------
    # Candidate experience details
    # --------------------------------------------------------

    experience_positions = []
    experience_responsibilities = []

    for entry in normalize_list(
        experience_details
    ):

        if isinstance(entry, dict):

            position = entry.get(
                "job_title",
                ""
            )

            responsibilities = entry.get(
                "responsibilities",
                []
            )

            if position:
                experience_positions.append(
                    str(position)
                )

            experience_responsibilities.extend(
                normalize_list(
                    responsibilities
                )
            )

        else:

            experience_positions.append(
                str(entry)
            )

    # --------------------------------------------------------
    # Legacy experience fallback
    # --------------------------------------------------------

    if not experience_positions:

        experience_positions = normalize_list(
            experience
        )

    # --------------------------------------------------------
    # Position text
    # --------------------------------------------------------

    resume_position = combine_text(
        experience_positions
    )

    # --------------------------------------------------------
    # Resume responsibilities
    # --------------------------------------------------------

    resume_responsibilities = combine_text(
        experience_responsibilities
    )

    # --------------------------------------------------------
    # Job responsibility text
    # --------------------------------------------------------

    job_responsibility_text = combine_text(
        job_responsibilities
    )

    # --------------------------------------------------------
    # Experience relevance
    # --------------------------------------------------------

    experience_result = (
        calculate_experience_relevance(
            resume_position=resume_position,
            resume_responsibilities=(
                resume_responsibilities
            ),
            job_position=job_title,
            job_responsibilities=(
                job_responsibility_text
            )
        )
    )

    # --------------------------------------------------------
    # Project similarity
    # --------------------------------------------------------

    project_similarity = (
        calculate_project_similarity(
            projects=projects,
            job_requirements=[
                job_description,
                job_requirements,
                job_responsibilities
            ]
        )
    )

    # --------------------------------------------------------
    # Overall profile semantic similarity
    # --------------------------------------------------------

    resume_semantic_text = [
        skills,
        projects,
        experience,
        experience_details,
        education
    ]

    job_semantic_text = [
        job_title,
        job_description,
        job_responsibilities,
        required_skills,
        job_requirements
    ]

    overall_semantic_similarity = (
        calculate_job_semantic_similarity(
            resume_text=resume_semantic_text,
            job_text=job_semantic_text
        )
    )

    # --------------------------------------------------------
    # Final semantic relevance
    # --------------------------------------------------------

    semantic_relevance = (
        experience_result[
            "experience_relevance"
        ] * 0.45
        + project_similarity * 0.25
        + overall_semantic_similarity * 0.30
    )

    semantic_relevance = round(
        max(
            0.0,
            min(
                semantic_relevance,
                1.0
            )
        ),
        4
    )

    return {
        "position_similarity": (
            experience_result[
                "position_similarity"
            ]
        ),
        "responsibility_similarity": (
            experience_result[
                "responsibility_similarity"
            ]
        ),
        "experience_relevance": (
            experience_result[
                "experience_relevance"
            ]
        ),
        "project_similarity": round(
            project_similarity,
            4
        ),
        "overall_semantic_similarity": (
            overall_semantic_similarity
        ),
        "semantic_relevance": (
            semantic_relevance
        )
    }


# ============================================================
# SIMPLE PUBLIC FUNCTION
# ============================================================

def get_semantic_job_match(
    resume_profile: Dict[str, Any],
    job: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Public wrapper for semantic job matching.
    """

    return analyze_semantic_job_match(
        resume_profile=resume_profile,
        job=job
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_resume_profile = {

        "name": "Anuj",

        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL"
        ],

        "projects": [
            "AI Attendance System using Face Recognition",
            "Text Summarization using T5",
            "Resume Analysis using Machine Learning"
        ],

        "experience": [
            "Machine Learning Intern"
        ],

        "experience_details": [
            {
                "job_title": "Machine Learning Intern",
                "company": "AI Company",
                "responsibilities": [
                    "Built machine learning models",
                    "Preprocessed datasets",
                    "Evaluated model performance"
                ],
                "technologies": [
                    "Python",
                    "Pandas",
                    "Scikit-learn"
                ]
            }
        ],

        "education": [
            "B.E. Computer Engineering"
        ]
    }

    test_job = {

        "title": "Machine Learning Engineer",

        "description": (
            "We are looking for a Machine Learning Engineer "
            "to build and deploy machine learning solutions."
        ),

        "responsibilities": [
            "Develop machine learning models",
            "Preprocess and analyze datasets",
            "Evaluate model performance",
            "Build production machine learning systems"
        ],

        "required_skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL",
            "TensorFlow",
            "Docker"
        ],

        "requirements": [
            "Experience building machine learning models",
            "Strong Python programming skills",
            "Knowledge of machine learning algorithms"
        ]
    }

    result = get_semantic_job_match(
        resume_profile=test_resume_profile,
        job=test_job
    )

    print(
        "\n========== SEMANTIC JOB MATCH =========="
    )

    print(
        "\nPosition Similarity:",
        f'{result["position_similarity"] * 100:.1f}%'
    )

    print(
        "Responsibility Similarity:",
        f'{result["responsibility_similarity"] * 100:.1f}%'
    )

    print(
        "Experience Relevance:",
        f'{result["experience_relevance"] * 100:.1f}%'
    )

    print(
        "Project Similarity:",
        f'{result["project_similarity"] * 100:.1f}%'
    )

    print(
        "Overall Semantic Similarity:",
        f'{result["overall_semantic_similarity"] * 100:.1f}%'
    )

    print(
        "Semantic Relevance:",
        f'{result["semantic_relevance"] * 100:.1f}%'
    )

    print(
        "\n========================================"
    )