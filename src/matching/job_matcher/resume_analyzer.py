# ==========================================
# IMPORT MATCHERS
# ==========================================

from skill_matcher import calculate_skill_match

from education_matcher import calculate_education_match

from experience_matcher import calculate_final_experience_match


# ==========================================
# MAIN RESUME ANALYZER
# ==========================================

def analyze_resume(
    # Skills
    resume_skills,
    required_skills,

    # Education
    resume_degree,
    resume_field,
    required_education,

    # Experience
    resume_position,
    resume_responsibilities,
    job_position,
    job_responsibilities,
    start_dates,
    end_dates,
    experience_requirement
):

    # ==========================================
    # 1. SKILL MATCH
    # ==========================================

    skill_match = calculate_skill_match(
        resume_skills,
        required_skills
    )


    # ==========================================
    # 2. EDUCATION MATCH
    # ==========================================

    education_match = calculate_education_match(
        resume_degree,
        resume_field,
        required_education
    )


    # ==========================================
    # 3. EXPERIENCE MATCH
    # ==========================================

    experience_result = calculate_final_experience_match(

        resume_position=resume_position,

        resume_responsibilities=resume_responsibilities,

        job_position=job_position,

        job_responsibilities=job_responsibilities,

        start_dates=start_dates,

        end_dates=end_dates,

        experience_requirement=experience_requirement
    )


    # ==========================================
    # RETURN ALL RESULTS
    # ==========================================

    return {

        "skill_match": round(
            skill_match,
            4
        ),

        "education_match": round(
            education_match,
            4
        ),

        "experience_result":
            experience_result
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    result = analyze_resume(

        # ----------------------------------
        # SKILLS
        # ----------------------------------

        resume_skills="""
        Python
        SQL
        Machine Learning
        Java
        """,

        required_skills="""
        Python
        SQL
        Machine Learning
        AWS
        """,


        # ----------------------------------
        # EDUCATION
        # ----------------------------------

        resume_degree="B.Tech",

        resume_field="Computer Engineering",

        required_education="""
        Bachelor's degree in
        Computer Science or related field
        """,


        # ----------------------------------
        # EXPERIENCE
        # ----------------------------------

        resume_position="Software Developer",

        resume_responsibilities="""
        Developed Python applications.
        Built REST APIs.
        Worked with databases.
        """,

        job_position="Machine Learning Engineer",

        job_responsibilities="""
        Develop machine learning models.
        Build AI applications.
        Train and deploy models.
        """,

        start_dates="['2021-01-01']",

        end_dates="['2024-01-01']",

        experience_requirement="""
        Minimum 5 years of experience
        """
    )


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    print("\nRESUME ANALYSIS RESULT")
    print("=" * 50)


    print("\nSKILL MATCH")
    print(
        f"{result['skill_match'] * 100:.2f}%"
    )


    print("\nEDUCATION MATCH")
    print(
        f"{result['education_match'] * 100:.2f}%"
    )


    print("\nEXPERIENCE MATCH")

    experience = result["experience_result"]

    print(
        f"User Experience: "
        f"{experience['user_years']} years"
    )

    print(
        f"Required Experience: "
        f"{experience['required_years']} years"
    )

    print(
        f"Position Similarity: "
        f"{experience['position_similarity'] * 100:.2f}%"
    )

    print(
        f"Responsibility Similarity: "
        f"{experience['responsibility_similarity'] * 100:.2f}%"
    )

    print(
        f"Experience Relevance: "
        f"{experience['experience_relevance'] * 100:.2f}%"
    )

    print(
        f"Years Match: "
        f"{experience['years_match'] * 100:.2f}%"
    )

    print(
        f"Final Experience Match: "
        f"{experience['final_experience_match'] * 100:.2f}%"
    )