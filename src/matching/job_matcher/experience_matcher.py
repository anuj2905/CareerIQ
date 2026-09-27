from .experience_semantic_matcher import (
    calculate_experience_relevance
)

from .calculate_experience import (
    calculate_experience_match
)


# ==================================================
# FINAL EXPERIENCE MATCH
# ==================================================

def calculate_final_experience_match(
    resume_position,
    resume_responsibilities,
    job_position,
    job_responsibilities,
    user_years,
    required_years
):

    # ==============================================
    # 1. SEMANTIC EXPERIENCE RELEVANCE
    # ==============================================

    semantic_result = (
        calculate_experience_relevance(
            resume_position,
            resume_responsibilities,
            job_position,
            job_responsibilities
        )
    )


    experience_relevance = (
        semantic_result[
            "experience_relevance"
        ]
    )


    # ==============================================
    # 2. EXPERIENCE YEARS MATCH
    # ==============================================

    years_match = (
        calculate_experience_match(
            user_years,
            required_years
        )
    )


    # ==============================================
    # 3. COMBINE BOTH SCORES
    # ==============================================

    final_experience_match = (

        experience_relevance * 0.6

        +

        years_match * 0.4
    )


    # ==============================================
    # RETURN RESULTS
    # ==============================================

    return {

        "position_similarity":
            semantic_result[
                "position_similarity"
            ],

        "responsibility_similarity":
            semantic_result[
                "responsibility_similarity"
            ],

        "experience_relevance":
            experience_relevance,

        "years_match":
            round(
                years_match,
                4
            ),

        "final_experience_match":
            round(
                final_experience_match,
                4
            )
    }