import ast


# ==========================================
# Clean Skills
# ==========================================

def clean_skills(skills):
    """
    Convert different skill formats into a clean set.
    """

    if not skills:
        return set()

    # Handle Python list directly
    if isinstance(skills, list):
        return {
            str(skill).strip().lower()
            for skill in skills
            if str(skill).strip()
        }

    skills = str(skills).strip()

    # Handle dataset format:
    # "['Python', 'SQL', 'Machine Learning']"
    if skills.startswith("[") and skills.endswith("]"):

        try:
            skills = ast.literal_eval(skills)

        except (ValueError, SyntaxError):
            skills = []

        if isinstance(skills, list):
            return {
                str(skill).strip().lower()
                for skill in skills
                if str(skill).strip()
            }

    # Handle comma/newline separated text
    return {
        skill.strip().lower()
        for skill in skills.replace(",", "\n").splitlines()
        if skill.strip()
    }


# ==========================================
# Calculate Skill Match
# ==========================================

def calculate_skill_match(
    resume_skills,
    required_skills
):
    """
    Calculate the percentage of required
    skills available in the resume.

    Returns:
        float: Score between 0.0 and 1.0
    """

    resume_set = clean_skills(resume_skills)
    required_set = clean_skills(required_skills)

    # No required skills available
    if not required_set:
        return 0.0

    # Find matching skills
    matched_skills = (
        resume_set.intersection(required_set)
    )

    # Calculate score
    match_score = (
        len(matched_skills)
        / len(required_set)
    )

    return round(match_score, 4)


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    resume = (
        "['Python', 'SQL', "
        "'Machine Learning', 'Java']"
    )

    job = """
    Python
    SQL
    Machine Learning
    AWS
    """

    score = calculate_skill_match(
        resume,
        job
    )

    print("Skill Match:", score)
    print("Skill Match %:", score * 100)