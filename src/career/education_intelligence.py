from typing import Any
import re

from pydantic import BaseModel, Field


# ============================================================
# EDUCATION STRUCTURE
# ============================================================

class EducationEntry(BaseModel):
    """
    Structured representation of one education entry.
    """

    degree: str = ""

    field_of_study: str = ""

    institution: str = ""

    education_level: str = ""

    graduation_year: str = ""

    education_text: str = ""


# ============================================================
# TEXT CLEANING
# ============================================================

def _clean_text(
    value: Any
) -> str:
    """
    Clean a text value safely.
    """

    if value is None:
        return ""

    text = str(value)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# CLEAN LIST
# ============================================================

def _clean_list(
    values: Any
) -> list[str]:
    """
    Clean and deduplicate a list of education entries.
    """

    if not values:
        return []

    if isinstance(
        values,
        str
    ):
        values = [values]

    if not isinstance(
        values,
        (list, tuple, set)
    ):
        values = [values]

    cleaned = []

    seen = set()

    for value in values:

        text = _clean_text(
            value
        )

        if not text:
            continue

        key = text.lower()

        if key in seen:
            continue

        seen.add(key)

        cleaned.append(
            text
        )

    return cleaned


# ============================================================
# DETECT EDUCATION LEVEL
# ============================================================

def detect_education_level(
    education_text: str
) -> str:
    """
    Detect the general education level.
    """

    text = _clean_text(
        education_text
    ).lower()

    if not text:
        return ""

    patterns = [

        (
            "doctorate",
            [
                r"\bph\.?d\b",
                r"\bdoctorate\b",
                r"\bdoctoral\b"
            ]
        ),

        (
            "master",
            [
                r"\bm\.?e\b",
                r"\bm\.?tech\b",
                r"\bm\.?sc\b",
                r"\bmca\b",
                r"\bmba\b",
                r"\bmaster\b",
                r"\bmasters\b",
                r"\bpostgraduate\b",
                r"\bpost graduate\b"
            ]
        ),

        (
            "bachelor",
            [
                r"\bb\.?e\b",
                r"\bb\.?tech\b",
                r"\bb\.?sc\b",
                r"\bbca\b",
                r"\bbba\b",
                r"\bbachelor\b",
                r"\bbachelors\b",
                r"\bundergraduate\b"
            ]
        ),

        (
            "diploma",
            [
                r"\bdiploma\b",
                r"\bpolytechnic\b"
            ]
        ),

        (
            "higher_secondary",
            [
                r"\b12th\b",
                r"\bhsc\b",
                r"\bhigher secondary\b",
                r"\bclass 12\b",
                r"\b12th standard\b"
            ]
        ),

        (
            "secondary",
            [
                r"\b10th\b",
                r"\bssc\b",
                r"\bsecondary school\b",
                r"\bclass 10\b",
                r"\b10th standard\b"
            ]
        )
    ]

    for level, level_patterns in patterns:

        for pattern in level_patterns:

            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            ):

                return level

    return ""


# ============================================================
# EXTRACT DEGREE
# ============================================================

def extract_degree(
    education_text: str
) -> str:
    """
    Extract the degree from an education entry.
    """

    text = _clean_text(
        education_text
    )

    if not text:
        return ""

    degree_patterns = [

        (
            r"\b(B\.?\s*E\.?)\b",
            "B.E."
        ),

        (
            r"\b(B\.?\s*Tech\.?)\b",
            "B.Tech"
        ),

        (
            r"\b(B\.?\s*Sc\.?)\b",
            "B.Sc"
        ),

        (
            r"\b(B\.?\s*CA)\b",
            "BCA"
        ),

        (
            r"\b(B\.?\s*BA)\b",
            "B.A."
        ),

        (
            r"\b(B\.?\s*Com)\b",
            "B.Com"
        ),

        (
            r"\b(B\.?\s*BA)\b",
            "BBA"
        ),

        (
            r"\b(M\.?\s*E\.?)\b",
            "M.E."
        ),

        (
            r"\b(M\.?\s*Tech\.?)\b",
            "M.Tech"
        ),

        (
            r"\b(M\.?\s*Sc\.?)\b",
            "M.Sc"
        ),

        (
            r"\b(M\.?\s*CA)\b",
            "MCA"
        ),

        (
            r"\b(M\.?\s*BA)\b",
            "MBA"
        ),

        (
            r"\b(Ph\.?\s*D\.?)\b",
            "Ph.D."
        ),

        (
            r"\b(Diploma)\b",
            "Diploma"
        )
    ]

    for pattern, degree in degree_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            return degree

    # Full degree names
    full_degree_patterns = [
        (
            r"\bBachelor of Engineering\b",
            "Bachelor of Engineering"
        ),
        (
            r"\bBachelor of Technology\b",
            "Bachelor of Technology"
        ),
        (
            r"\bMaster of Engineering\b",
            "Master of Engineering"
        ),
        (
            r"\bMaster of Technology\b",
            "Master of Technology"
        ),
        (
            r"\bBachelor of Science\b",
            "Bachelor of Science"
        ),
        (
            r"\bMaster of Science\b",
            "Master of Science"
        ),
        (
            r"\bMaster of Computer Applications\b",
            "Master of Computer Applications"
        )
    ]

    for pattern, degree in full_degree_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            return degree

    return ""


# ============================================================
# EXTRACT FIELD OF STUDY
# ============================================================

def extract_field_of_study(
    education_text: str
) -> str:
    """
    Extract the field or branch of study.
    """

    text = _clean_text(
        education_text
    )

    if not text:
        return ""

    # --------------------------------------------------------
    # Common "in" format
    #
    # B.E. in Computer Engineering
    # --------------------------------------------------------

    match = re.search(
        r"\b(?:in|of)\s+"
        r"([A-Za-z][A-Za-z &/\-]+?)"
        r"(?:,| at | from | \(|$)",
        text,
        flags=re.IGNORECASE
    )

    if match:

        field = _clean_text(
            match.group(1)
        )

        if field:
            return field

    # --------------------------------------------------------
    # Common engineering branches
    # --------------------------------------------------------

    fields = [
        "Computer Engineering",
        "Computer Science",
        "Information Technology",
        "Artificial Intelligence",
        "Machine Learning",
        "Data Science",
        "Electronics and Telecommunication",
        "Electronics and Communication",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Biomedical Engineering",
        "Software Engineering",
        "Information Science"
    ]

    for field in fields:

        if re.search(
            re.escape(field),
            text,
            flags=re.IGNORECASE
        ):

            return field

    return ""


# ============================================================
# EXTRACT INSTITUTION
# ============================================================

def extract_institution(
    education_text: str
) -> str:
    """
    Attempt to extract an institution name.

    This is intentionally conservative.
    """

    text = _clean_text(
        education_text
    )

    if not text:
        return ""

    # --------------------------------------------------------
    # "at Institution"
    # --------------------------------------------------------

    match = re.search(
        r"\bat\s+"
        r"(.+?)(?:,|\s+\d{4}\b|$)",
        text,
        flags=re.IGNORECASE
    )

    if match:

        institution = _clean_text(
            match.group(1)
        )

        if institution:
            return institution

    # --------------------------------------------------------
    # "from Institution"
    # --------------------------------------------------------

    match = re.search(
        r"\bfrom\s+"
        r"(.+?)(?:,|\s+\d{4}\b|$)",
        text,
        flags=re.IGNORECASE
    )

    if match:

        institution = _clean_text(
            match.group(1)
        )

        if institution:
            return institution

    # --------------------------------------------------------
    # Common institution keywords
    # --------------------------------------------------------

    institution_match = re.search(
        r"([A-Z][A-Za-z0-9&.,' \-]+"
        r"(?:University|College|Institute|School)"
        r"(?:[A-Za-z0-9&.,' \-]*)?)",
        text
    )

    if institution_match:

        institution = _clean_text(
            institution_match.group(1)
        )

        if institution:
            return institution

    return ""


# ============================================================
# EXTRACT GRADUATION YEAR
# ============================================================

def extract_graduation_year(
    education_text: str
) -> str:
    """
    Extract a four-digit education/graduation year.

    Only extracts a year when it is explicitly present.
    """

    text = _clean_text(
        education_text
    )

    if not text:
        return ""

    years = re.findall(
        r"\b(19\d{2}|20\d{2})\b",
        text
    )

    if not years:
        return ""

    # Return the last explicitly mentioned year.
    return years[-1]


# ============================================================
# ANALYZE ONE EDUCATION ENTRY
# ============================================================

def analyze_education_entry(
    education_text: str
) -> EducationEntry:
    """
    Analyze one raw education entry.
    """

    text = _clean_text(
        education_text
    )

    if not text:
        return EducationEntry()

    degree = extract_degree(
        text
    )

    field_of_study = extract_field_of_study(
        text
    )

    institution = extract_institution(
        text
    )

    education_level = detect_education_level(
        text
    )

    graduation_year = extract_graduation_year(
        text
    )

    return EducationEntry(

        degree=degree,

        field_of_study=field_of_study,

        institution=institution,

        education_level=education_level,

        graduation_year=graduation_year,

        education_text=text
    )


# ============================================================
# ANALYZE ALL EDUCATION
# ============================================================

def analyze_education(
    education: list[Any]
) -> list[EducationEntry]:
    """
    Analyze all education entries.
    """

    normalized_education = _clean_list(
        education
    )

    analyzed_entries = []

    for education_text in normalized_education:

        entry = analyze_education_entry(
            education_text
        )

        if (
            entry.education_text
            or entry.degree
            or entry.field_of_study
            or entry.institution
        ):

            analyzed_entries.append(
                entry
            )

    return analyzed_entries


# ============================================================
# EDUCATION LEVEL SCORE
# ============================================================

def education_level_score(
    education_level: str
) -> int:
    """
    Convert education level into a hierarchy score.

    Higher number = higher academic level.

    This is NOT a candidate score.
    It is only an internal ordering used by CareerIQ.
    """

    levels = {

        "secondary": 1,

        "higher_secondary": 2,

        "diploma": 3,

        "bachelor": 4,

        "master": 5,

        "doctorate": 6
    }

    return levels.get(
        education_level,
        0
    )


# ============================================================
# FIND HIGHEST EDUCATION LEVEL
# ============================================================

def get_highest_education(
    education_entries: list[EducationEntry]
) -> EducationEntry | None:
    """
    Return the highest education entry based on
    academic level.
    """

    if not education_entries:
        return None

    return max(
        education_entries,
        key=lambda entry: education_level_score(
            entry.education_level
        )
    )


# ============================================================
# EDUCATION SUMMARY
# ============================================================

def build_education_summary(
    education_entries: list[EducationEntry]
) -> dict:
    """
    Build a high-level education summary.
    """

    highest = get_highest_education(
        education_entries
    )

    degrees = []

    fields = []

    institutions = []

    levels = []

    graduation_years = []

    for entry in education_entries:

        if entry.degree:
            degrees.append(
                entry.degree
            )

        if entry.field_of_study:
            fields.append(
                entry.field_of_study
            )

        if entry.institution:
            institutions.append(
                entry.institution
            )

        if entry.education_level:
            levels.append(
                entry.education_level
            )

        if entry.graduation_year:
            graduation_years.append(
                entry.graduation_year
            )

    return {

        "education_count":
            len(education_entries),

        "degrees":
            list(dict.fromkeys(degrees)),

        "fields_of_study":
            list(dict.fromkeys(fields)),

        "institutions":
            list(dict.fromkeys(institutions)),

        "education_levels":
            list(dict.fromkeys(levels)),

        "graduation_years":
            list(dict.fromkeys(graduation_years)),

        "highest_education":
            (
                highest.model_dump()
                if highest
                else None
            )
    }


# ============================================================
# COMPLETE EDUCATION ANALYSIS
# ============================================================

def analyze_profile_education(
    education: list[Any]
) -> dict:
    """
    Complete CareerIQ education analysis.
    """

    entries = analyze_education(
        education
    )

    summary = build_education_summary(
        entries
    )

    return {

        "entries": [
            entry.model_dump()
            for entry in entries
        ],

        "summary": summary
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_education = [

        (
            "B.E. in Computer Engineering, "
            "Atharva College of Engineering, "
            "2027"
        ),

        (
            "HSC, Maharashtra State Board, "
            "2023"
        )

    ]

    print()

    print(
        "=" * 60
    )

    print(
        "       CAREERIQ EDUCATION INTELLIGENCE"
    )

    print(
        "=" * 60
    )

    result = analyze_profile_education(
        test_education
    )

    print()

    print(
        "Education Entries:"
    )

    for index, entry in enumerate(
        result["entries"],
        start=1
    ):

        print()

        print(
            f"  Education {index}:"
        )

        print(
            f"    Degree: "
            f"{entry['degree']}"
        )

        print(
            f"    Field of Study: "
            f"{entry['field_of_study']}"
        )

        print(
            f"    Institution: "
            f"{entry['institution']}"
        )

        print(
            f"    Education Level: "
            f"{entry['education_level']}"
        )

        print(
            f"    Graduation Year: "
            f"{entry['graduation_year']}"
        )

        print(
            f"    Original Text: "
            f"{entry['education_text']}"
        )

    print()

    print(
        "Education Summary:"
    )

    print(
        result["summary"]
    )

    print()

    print(
        "=" * 60
    )