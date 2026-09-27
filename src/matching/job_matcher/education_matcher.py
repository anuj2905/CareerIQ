import ast
import re


# ==========================================
# 1. EDUCATION FIELD GROUPS
# ==========================================

EDUCATION_GROUPS = {

    "computer_science": {
        "computer science",
        "computer engineering",
        "computer applications",
        "computer application",
        "information technology",
        "it",
        "information systems",
        "software engineering",
        "software development",
        "data science",
        "artificial intelligence",
        "machine learning",
        "cyber security",
        "cybersecurity",
        "computers"
    },

    "electronics": {
        "electronics",
        "electronics engineering",
        "electronics and communication",
        "electronics and communication engineering",
        "electronics and telecommunication",
        "electronics and telecommunication engineering",
        "electronics telecommunication",
        "communication engineering",
        "ece"
    },

    "electrical": {
        "electrical",
        "electrical engineering",
        "power engineering",
        "eee"
    },

    "mechanical": {
        "mechanical",
        "mechanical engineering",
        "automobile engineering",
        "automotive engineering",
        "production engineering"
    },

    "civil": {
        "civil",
        "civil engineering",
        "construction engineering"
    },

    "chemical": {
        "chemical",
        "chemical engineering"
    },

    "business": {
        "business administration",
        "business management",
        "management",
        "marketing",
        "finance",
        "financial management",
        "human resources",
        "accounting",
        "commerce"
    },

    "mathematics": {
        "mathematics",
        "maths",
        "applied mathematics",
        "statistics",
        "applied statistics"
    },

    "physics": {
        "physics",
        "applied physics"
    },

    "biology": {
        "biology",
        "biotechnology",
        "microbiology",
        "biomedical science",
        "biomedical engineering"
    }
}


# ==========================================
# 2. DEGREE LEVELS
# ==========================================

DEGREE_LEVELS = {

    "diploma": {
        "diploma",
        "polytechnic",
        "associate degree",
        "associate"
    },

    "bachelor": {
        "b.e",
        "be",
        "b.tech",
        "btech",
        "b.sc",
        "bsc",
        "bca",
        "bba",

        "bachelor",
        "bachelor's",
        "bachelors",
        "bachelor degree",
        "bachelor's degree",

        "bachelor of engineering",
        "bachelor of technology",
        "bachelor of science",
        "bachelor of computer applications",
        "bachelor of business administration",

        "honors",
        "honours"
    },

    "master": {
        "m.e",
        "me",
        "m.tech",
        "mtech",
        "m.sc",
        "msc",
        "mca",
        "mba",

        "master",
        "master's",
        "masters",
        "master degree",
        "master's degree",

        "master of engineering",
        "master of technology",
        "master of science",
        "master of computer applications",
        "master of business administration"
    },

    "phd": {
        "phd",
        "ph.d",
        "ph.d.",
        "doctorate",
        "doctoral",
        "doctor of philosophy"
    }
}


# ==========================================
# 3. NORMALIZE TEXT
# ==========================================

def normalize_text(text):
    """
    Convert text into a normalized format.
    """

    if text is None:
        return ""

    text = str(text).lower().strip()

    # Convert common separators into spaces
    text = text.replace("/", " ")
    text = text.replace("&", " and ")
    text = text.replace("-", " ")

    # Remove unnecessary punctuation
    text = re.sub(r"[^a-z0-9.\s']", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 4. CONVERT DATA INTO CLEAN TEXT
# ==========================================

def clean_data(education):
    """
    Convert dataset values into a clean normalized string.

    Supports:
    - Python lists
    - String representations of lists
    - Normal text
    - Comma-separated text
    """

    if not education:
        return ""

    # Already a Python list
    if isinstance(education, list):
        return " ".join(
            normalize_text(item)
            for item in education
            if str(item).strip()
        )

    education = str(education).strip()

    # Dataset format:
    # "['B.Tech', 'Computer Engineering']"
    if education.startswith("[") and education.endswith("]"):

        try:
            parsed_data = ast.literal_eval(education)

            if isinstance(parsed_data, list):
                return " ".join(
                    normalize_text(item)
                    for item in parsed_data
                    if str(item).strip()
                )

        except (ValueError, SyntaxError):
            pass

    return normalize_text(education)


# ==========================================
# 5. CHECK IF PHRASE EXISTS
# ==========================================

def contains_phrase(text, phrase):
    """
    Check whether a phrase exists in text.

    Uses word boundaries to avoid false matches.
    """

    text = normalize_text(text)
    phrase = normalize_text(phrase)

    if not text or not phrase:
        return False

    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"

    return bool(
        re.search(pattern, text)
    )


# ==========================================
# 6. FIND DEGREE LEVEL
# ==========================================

def get_degree_level(education):
    """
    Detect diploma / bachelor / master / phd
    from education text.
    """

    education_text = clean_data(education)

    if not education_text:
        return None

    # Check longer phrases first
    for level, degrees in DEGREE_LEVELS.items():

        sorted_degrees = sorted(
            degrees,
            key=len,
            reverse=True
        )

        for degree in sorted_degrees:

            if contains_phrase(
                education_text,
                degree
            ):
                return level

    return None


# ==========================================
# 7. FIND EDUCATION FIELD GROUP
# ==========================================

def get_education_group(education):
    """
    Detect the education field group
    from education text.
    """

    education_text = clean_data(education)

    if not education_text:
        return None

    # Check longer phrases first
    for group, fields in EDUCATION_GROUPS.items():

        sorted_fields = sorted(
            fields,
            key=len,
            reverse=True
        )

        for field in sorted_fields:

            if contains_phrase(
                education_text,
                field
            ):
                return group

    return None


# ==========================================
# 8. CALCULATE DEGREE MATCH
# ==========================================

def calculate_degree_match(
    resume_degree,
    required_education
):

    resume_level = get_degree_level(
        resume_degree
    )

    required_level = get_degree_level(
        required_education
    )

    if not resume_level:
        return 0.0

    # If job requirement does not clearly specify
    # a degree level, do not penalize the candidate.
    if not required_level:
        return 1.0

    degree_order = {
        "diploma": 1,
        "bachelor": 2,
        "master": 3,
        "phd": 4
    }

    # Candidate qualification is equal
    # or higher than required qualification
    if (
        degree_order[resume_level]
        >=
        degree_order[required_level]
    ):
        return 1.0

    return 0.0


# ==========================================
# 9. CALCULATE FIELD MATCH
# ==========================================

def calculate_field_match(
    resume_field,
    required_education
):

    resume_group = get_education_group(
        resume_field
    )

    required_group = get_education_group(
        required_education
    )

    # Resume field cannot be identified
    if not resume_group:
        return 0.0

    # Job does not specify a clear field.
    # We should not penalize the candidate.
    if not required_group:
        return 1.0

    # Same field group
    if resume_group == required_group:
        return 1.0

    return 0.0


# ==========================================
# 10. FINAL EDUCATION MATCH
# ==========================================

def calculate_education_match(
    resume_degree,
    resume_field,
    required_education
):
    """
    Calculate final education match.

    Degree = 50%
    Field  = 50%
    """

    if not required_education:
        return 0.0

    degree_match = calculate_degree_match(
        resume_degree,
        required_education
    )

    field_match = calculate_field_match(
        resume_field,
        required_education
    )

    education_score = (
        degree_match * 0.5
        +
        field_match * 0.5
    )

    return round(
        education_score,
        4
    )


# ==========================================
# 11. TEST
# ==========================================

if __name__ == "__main__":

    resume_degree = "B.Tech"

    resume_field = "Computer Engineering"

    required_education = (
        "Bachelor's degree in Computer Science "
        "or related field"
    )


    print("\nEDUCATION ANALYSIS")
    print("=" * 50)

    print(
        "Resume Degree:",
        resume_degree
    )

    print(
        "Detected Resume Degree:",
        get_degree_level(resume_degree)
    )

    print(
        "Resume Field:",
        resume_field
    )

    print(
        "Detected Resume Field:",
        get_education_group(resume_field)
    )

    print(
        "\nRequired Education:",
        required_education
    )

    print(
        "Detected Required Degree:",
        get_degree_level(required_education)
    )

    print(
        "Detected Required Field:",
        get_education_group(required_education)
    )


    degree_match = calculate_degree_match(
        resume_degree,
        required_education
    )

    field_match = calculate_field_match(
        resume_field,
        required_education
    )

    score = calculate_education_match(
        resume_degree,
        resume_field,
        required_education
    )


    print("\nRESULT")
    print("=" * 50)

    print(
        "Degree Match:",
        degree_match * 100,
        "%"
    )

    print(
        "Field Match:",
        field_match * 100,
        "%"
    )

    print(
        "Education Match:",
        score
    )

    print(
        "Education Match %:",
        score * 100
    )