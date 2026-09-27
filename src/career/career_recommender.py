from typing import Any, Dict, List


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def _normalize_list(values) -> List[str]:
    """
    Convert different input formats into a clean list of strings.
    """

    if not values:
        return []

    if isinstance(values, str):
        return [values.strip()] if values.strip() else []

    if isinstance(values, (list, tuple, set)):
        return [
            str(value).strip()
            for value in values
            if str(value).strip()
        ]

    return [str(values).strip()]


def _normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """

    return " ".join(
        str(skill)
        .lower()
        .strip()
        .split()
    )


# ============================================================
# SKILL COVERAGE
# ============================================================

def calculate_skill_coverage(
    user_skills,
    required_skills
) -> Dict[str, Any]:
    """
    Compare the user's skills with the skills
    required for a target career role.
    """

    user_skills = _normalize_list(user_skills)
    required_skills = _normalize_list(required_skills)

    user_skill_map = {
        _normalize_skill(skill): skill
        for skill in user_skills
    }

    required_skill_map = {
        _normalize_skill(skill): skill
        for skill in required_skills
    }

    if not required_skill_map:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "skill_coverage": 0.0
        }

    matched_skills = []
    missing_skills = []

    for normalized_skill, original_skill in (
        required_skill_map.items()
    ):

        if normalized_skill in user_skill_map:

            matched_skills.append(
                original_skill
            )

        else:

            missing_skills.append(
                original_skill
            )

    coverage = (
        len(matched_skills)
        / len(required_skill_map)
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round(
            coverage,
            4
        )
    }


# ============================================================
# CAREER READINESS
# ============================================================

def calculate_career_readiness(
    skill_coverage: float,
    experience_score: float = 0.0,
    education_score: float = 0.0
) -> float:
    """
    Calculate overall career readiness.

    Weighting:

    Skills      = 60%
    Experience  = 25%
    Education   = 15%
    """

    skill_coverage = max(
        0.0,
        min(float(skill_coverage), 1.0)
    )

    experience_score = max(
        0.0,
        min(float(experience_score), 1.0)
    )

    education_score = max(
        0.0,
        min(float(education_score), 1.0)
    )

    readiness = (
        skill_coverage * 0.60
        + experience_score * 0.25
        + education_score * 0.15
    )

    return round(
        readiness,
        4
    )


# ============================================================
# IMPROVEMENT PLAN
# ============================================================

def generate_improvement_plan(
    missing_skills,
    matched_skills,
    recommended_role: str
) -> List[str]:
    """
    Generate practical recommendations based
    on the user's current skills.
    """

    missing_skills = _normalize_list(
        missing_skills
    )

    matched_skills = _normalize_list(
        matched_skills
    )

    recommendations = []

    # Missing skills
    if missing_skills:

        for skill in missing_skills[:5]:

            recommendations.append(
                f"Improve your knowledge of {skill}."
            )

    # No matching skills
    if not matched_skills:

        recommendations.append(
            f"Build foundational skills required "
            f"for {recommended_role}."
        )

    # Project recommendation
    if len(matched_skills) >= 3:

        recommendations.append(
            f"Build a project that demonstrates "
            f"your existing skills for "
            f"{recommended_role}."
        )

    # Interview preparation
    recommendations.append(
        "Practice interview questions related to "
        f"{recommended_role}."
    )

    return recommendations


# ============================================================
# MAIN CAREER RECOMMENDATION
# ============================================================

def generate_career_recommendation(
    profile: Dict[str, Any],
    recommended_role: str,
    required_skills,
    role_score: float = 0.0,
    experience_score: float = 0.0,
    education_score: float = 0.0
) -> Dict[str, Any]:
    """
    Generate a complete career recommendation
    for a student profile.
    """

    if not isinstance(profile, dict):

        raise TypeError(
            "profile must be a dictionary."
        )

    # --------------------------------------------------------
    # User skills
    # --------------------------------------------------------

    user_skills = profile.get(
        "skills",
        []
    )

    # --------------------------------------------------------
    # Skill coverage
    # --------------------------------------------------------

    skill_result = calculate_skill_coverage(
        user_skills=user_skills,
        required_skills=required_skills
    )

    skill_coverage = skill_result[
        "skill_coverage"
    ]

    # --------------------------------------------------------
    # Career readiness
    # --------------------------------------------------------

    career_readiness = calculate_career_readiness(
        skill_coverage=skill_coverage,
        experience_score=experience_score,
        education_score=education_score
    )

    # --------------------------------------------------------
    # Improvement plan
    # --------------------------------------------------------

    improvement_plan = generate_improvement_plan(
        missing_skills=skill_result[
            "missing_skills"
        ],
        matched_skills=skill_result[
            "matched_skills"
        ],
        recommended_role=recommended_role
    )

    # --------------------------------------------------------
    # Readiness level
    # --------------------------------------------------------

    if career_readiness >= 0.80:

        readiness_level = "Excellent"

    elif career_readiness >= 0.65:

        readiness_level = "Good"

    elif career_readiness >= 0.50:

        readiness_level = "Moderate"

    else:

        readiness_level = "Needs Improvement"

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "recommended_role": recommended_role,

        "role_score": round(
            float(role_score),
            4
        ),

        "matched_skills": skill_result[
            "matched_skills"
        ],

        "missing_skills": skill_result[
            "missing_skills"
        ],

        "skill_coverage": skill_coverage,

        "experience_score": round(
            float(experience_score),
            4
        ),

        "education_score": round(
            float(education_score),
            4
        ),

        "career_readiness": career_readiness,

        "readiness_level": readiness_level,

        "improvement_plan": improvement_plan
    }


# ============================================================
# SIMPLE PUBLIC FUNCTION
# ============================================================

def get_career_recommendation(
    profile: Dict[str, Any],
    recommended_role: str,
    required_skills
) -> Dict[str, Any]:
    """
    Simplified wrapper for career recommendation.
    """

    return generate_career_recommendation(
        profile=profile,
        recommended_role=recommended_role,
        required_skills=required_skills
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_profile = {

        "name": "Anuj",

        "education": [
            "B.E. Computer Engineering"
        ],

        "skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn",
            "SQL"
        ],

        "projects": [
            "AI Attendance System",
            "Text Summarization"
        ],

        "experience": [],

        "certifications": []
    }

    ml_engineer_skills = [

        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "SQL",
        "TensorFlow",
        "PyTorch",
        "Docker",
        "MLOps"
    ]

    result = get_career_recommendation(

        profile=test_profile,

        recommended_role=(
            "Machine Learning Engineer"
        ),

        required_skills=ml_engineer_skills
    )

    print(
        "\n========== CAREER RECOMMENDATION =========="
    )

    print(
        "\nRecommended Role:",
        result["recommended_role"]
    )

    print(
        "\nRole Score:",
        f'{result["role_score"] * 100:.1f}%'
    )

    print("\nMatched Skills:")

    for skill in result[
        "matched_skills"
    ]:

        print(
            f"  ✓ {skill}"
        )

    print("\nMissing Skills:")

    for skill in result[
        "missing_skills"
    ]:

        print(
            f"  ✗ {skill}"
        )

    print(
        "\nSkill Coverage:",
        f'{result["skill_coverage"] * 100:.1f}%'
    )

    print(
        "\nCareer Readiness:",
        f'{result["career_readiness"] * 100:.1f}%'
    )

    print(
        "\nReadiness Level:",
        result["readiness_level"]
    )

    print("\nImprovement Plan:")

    for number, recommendation in enumerate(
        result["improvement_plan"],
        start=1
    ):

        print(
            f"  {number}. {recommendation}"
        )

    print(
        "\n============================================"
    )