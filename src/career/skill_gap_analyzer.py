from typing import Any, Dict, List


# ============================================================
# 1. NORMALIZE SKILLS
# ============================================================

def normalize_skill(skill: str) -> str:
    """
    Normalize a single skill for comparison.

    Example:
        " Python " -> "python"
        "Machine Learning" -> "machine learning"
    """

    return " ".join(
        str(skill).strip().lower().split()
    )


# ============================================================
# 2. CLEAN SKILL LIST
# ============================================================

def clean_skills(skills) -> List[str]:
    """
    Convert different skill formats into a clean list.

    Supported examples:

        ["Python", "SQL"]

        "Python, SQL"

        "Python\nSQL"

    Returns:
        Clean list of skills.
    """

    if not skills:
        return []

    # --------------------------------------------------------
    # Already a list
    # --------------------------------------------------------

    if isinstance(skills, list):

        cleaned_skills = []

        for skill in skills:

            skill = str(skill).strip()

            if skill:
                cleaned_skills.append(skill)

        return cleaned_skills

    # --------------------------------------------------------
    # Convert other values to string
    # --------------------------------------------------------

    skills = str(skills).strip()

    if not skills:
        return []

    # --------------------------------------------------------
    # Handle comma-separated skills
    # --------------------------------------------------------

    if "," in skills:

        skills = skills.replace(
            ",",
            "\n"
        )

    # --------------------------------------------------------
    # Split by lines
    # --------------------------------------------------------

    skill_list = skills.splitlines()

    cleaned_skills = []

    for skill in skill_list:

        skill = skill.strip()

        if skill:
            cleaned_skills.append(skill)

    return cleaned_skills


# ============================================================
# 3. REMOVE DUPLICATE SKILLS
# ============================================================

def remove_duplicate_skills(
    skills: List[str]
) -> List[str]:
    """
    Remove duplicate skills while preserving
    the original order.
    """

    unique_skills = []

    seen = set()

    for skill in skills:

        normalized = normalize_skill(
            skill
        )

        if normalized not in seen:

            seen.add(normalized)

            unique_skills.append(
                skill
            )

    return unique_skills


# ============================================================
# 4. COMPARE USER SKILLS WITH REQUIRED SKILLS
# ============================================================

def calculate_skill_gap(
    user_skills,
    required_skills
) -> Dict[str, Any]:
    """
    Compare the student's current skills
    with the skills required for a target role.

    Returns:

        matched_skills
        missing_skills
        extra_skills
        skill_match_score
        total_required_skills
        total_matched_skills
        total_missing_skills
    """

    # --------------------------------------------------------
    # Clean input
    # --------------------------------------------------------

    user_skills = clean_skills(
        user_skills
    )

    required_skills = clean_skills(
        required_skills
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    user_skills = remove_duplicate_skills(
        user_skills
    )

    required_skills = remove_duplicate_skills(
        required_skills
    )

    # --------------------------------------------------------
    # Create normalized sets
    # --------------------------------------------------------

    user_skill_map = {
        normalize_skill(skill): skill
        for skill in user_skills
    }

    required_skill_map = {
        normalize_skill(skill): skill
        for skill in required_skills
    }

    user_skill_set = set(
        user_skill_map.keys()
    )

    required_skill_set = set(
        required_skill_map.keys()
    )

    # --------------------------------------------------------
    # Matched skills
    # --------------------------------------------------------

    matched_normalized = (
        user_skill_set
        .intersection(
            required_skill_set
        )
    )

    matched_skills = [
        user_skill_map[skill]
        for skill in user_skill_set
        if skill in matched_normalized
    ]

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing_normalized = (
        required_skill_set
        - user_skill_set
    )

    missing_skills = [
        required_skill_map[skill]
        for skill in required_skill_set
        if skill in missing_normalized
    ]

    # --------------------------------------------------------
    # Extra skills
    #
    # Skills the user has but the target role
    # does not explicitly require.
    # --------------------------------------------------------

    extra_normalized = (
        user_skill_set
        - required_skill_set
    )

    extra_skills = [
        user_skill_map[skill]
        for skill in user_skill_set
        if skill in extra_normalized
    ]

    # --------------------------------------------------------
    # Calculate match score
    # --------------------------------------------------------

    total_required = len(
        required_skill_set
    )

    total_matched = len(
        matched_normalized
    )

    total_missing = len(
        missing_normalized
    )

    if total_required == 0:

        skill_match_score = 0.0

    else:

        skill_match_score = (
            total_matched
            / total_required
        )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "extra_skills": extra_skills,

        "skill_match_score": round(
            skill_match_score,
            4
        ),

        "total_required_skills":
            total_required,

        "total_matched_skills":
            total_matched,

        "total_missing_skills":
            total_missing
    }


# ============================================================
# 5. PRIORITIZE MISSING SKILLS
# ============================================================

def prioritize_missing_skills(
    missing_skills: List[str]
) -> List[Dict[str, str]]:
    """
    Assign a simple learning priority
    to missing skills.

    The first few missing skills are treated
    as high priority.

    This can later be replaced with an
    ML/LLM-based priority system.
    """

    prioritized_skills = []

    for index, skill in enumerate(
        missing_skills
    ):

        if index < 3:

            priority = "High"

        elif index < 6:

            priority = "Medium"

        else:

            priority = "Low"

        prioritized_skills.append(
            {
                "skill": skill,
                "priority": priority
            }
        )

    return prioritized_skills


# ============================================================
# 6. GENERATE LEARNING RECOMMENDATIONS
# ============================================================

def generate_learning_recommendations(
    missing_skills: List[str]
) -> List[str]:
    """
    Generate basic learning recommendations
    for missing skills.
    """

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Learn and practice {skill}."
        )

    return recommendations


# ============================================================
# 7. COMPLETE SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    user_skills,
    required_skills,
    target_role: str = ""
) -> Dict[str, Any]:
    """
    Perform a complete skill-gap analysis.

    Parameters
    ----------
    user_skills:
        Skills extracted from the student's resume.

    required_skills:
        Skills required for the target career role.

    target_role:
        Career role selected for analysis.

    Returns
    -------
    Dictionary containing:

        target_role
        matched_skills
        missing_skills
        extra_skills
        prioritized_missing_skills
        skill_match_score
        skill_match_percentage
        learning_recommendations
    """

    # --------------------------------------------------------
    # Compare skills
    # --------------------------------------------------------

    result = calculate_skill_gap(
        user_skills=user_skills,
        required_skills=required_skills
    )

    # --------------------------------------------------------
    # Prioritize missing skills
    # --------------------------------------------------------

    prioritized_missing_skills = (
        prioritize_missing_skills(
            result["missing_skills"]
        )
    )

    # --------------------------------------------------------
    # Learning recommendations
    # --------------------------------------------------------

    learning_recommendations = (
        generate_learning_recommendations(
            result["missing_skills"]
        )
    )

    # --------------------------------------------------------
    # Convert score to percentage
    # --------------------------------------------------------

    skill_match_percentage = (
        result["skill_match_score"] * 100
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    return {

        "target_role": target_role,

        "matched_skills":
            result["matched_skills"],

        "missing_skills":
            result["missing_skills"],

        "extra_skills":
            result["extra_skills"],

        "prioritized_missing_skills":
            prioritized_missing_skills,

        "skill_match_score":
            result["skill_match_score"],

        "skill_match_percentage":
            round(
                skill_match_percentage,
                2
            ),

        "total_required_skills":
            result[
                "total_required_skills"
            ],

        "total_matched_skills":
            result[
                "total_matched_skills"
            ],

        "total_missing_skills":
            result[
                "total_missing_skills"
            ],

        "learning_recommendations":
            learning_recommendations
    }


# ============================================================
# 8. PROFILE-BASED SKILL GAP ANALYSIS
# ============================================================

def analyze_profile_skill_gap(
    profile: Dict[str, Any],
    required_skills,
    target_role: str = ""
) -> Dict[str, Any]:
    """
    Analyze the skill gap directly from a ResumeProfile
    dictionary.

    Example profile:

        {
            "name": "Anuj",
            "skills": [
                "Python",
                "Machine Learning",
                "SQL"
            ]
        }
    """

    if not isinstance(
        profile,
        dict
    ):

        raise TypeError(
            "profile must be a dictionary."
        )

    user_skills = profile.get(
        "skills",
        []
    )

    return analyze_skill_gap(
        user_skills=user_skills,
        required_skills=required_skills,
        target_role=target_role
    )


# ============================================================
# 9. TEST
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Example student profile
    # --------------------------------------------------------

    test_profile = {

        "name": "Anuj Patil",

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

    # --------------------------------------------------------
    # Example Machine Learning Engineer requirements
    # --------------------------------------------------------

    required_skills = [

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

    # --------------------------------------------------------
    # Run analysis
    # --------------------------------------------------------

    result = analyze_profile_skill_gap(
        profile=test_profile,
        required_skills=required_skills,
        target_role="Machine Learning Engineer"
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print(
        "\n=========================================="
    )

    print(
        "        SKILL GAP ANALYSIS"
    )

    print(
        "=========================================="
    )

    print(
        "\nTarget Role:"
    )

    print(
        result["target_role"]
    )

    print(
        "\nSkill Match:"
    )

    print(
        f'{result["skill_match_percentage"]}%'
    )

    print(
        "\nMatched Skills:"
    )

    for skill in result[
        "matched_skills"
    ]:

        print(
            f"  ✓ {skill}"
        )

    print(
        "\nMissing Skills:"
    )

    for skill in result[
        "missing_skills"
    ]:

        print(
            f"  ✗ {skill}"
        )

    print(
        "\nExtra Skills:"
    )

    for skill in result[
        "extra_skills"
    ]:

        print(
            f"  + {skill}"
        )

    print(
        "\nLearning Priority:"
    )

    for item in result[
        "prioritized_missing_skills"
    ]:

        print(
            f'  {item["priority"]}: '
            f'{item["skill"]}'
        )

    print(
        "\nLearning Recommendations:"
    )

    for recommendation in result[
        "learning_recommendations"
    ]:

        print(
            f"  → {recommendation}"
        )

    print(
        "\n=========================================="
    )   