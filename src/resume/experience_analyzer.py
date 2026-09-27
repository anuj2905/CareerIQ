import re
from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# EXPERIENCE STRUCTURE
# ============================================================

class ExperienceEntry(BaseModel):
    """
    Structured representation of one work experience entry.
    """

    job_title: str = ""

    company: str = ""

    employment_type: str = ""

    location: str = ""

    start_date: str = ""

    end_date: str = ""

    duration: str = ""

    duration_months: float = 0.0

    responsibilities: list[str] = Field(
        default_factory=list
    )

    technologies: list[str] = Field(
        default_factory=list
    )


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
    Clean a list of values.

    Removes:
        - None
        - empty strings
        - unnecessary whitespace
        - duplicates
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
# NORMALIZE EXPERIENCE LIST
# ============================================================

def normalize_experience_list(
    experience: list[Any]
) -> list[str]:
    """
    Clean and normalize legacy raw experience entries.
    """

    return _clean_list(
        experience
    )


# ============================================================
# EXTRACT JOB TITLE FROM RAW TEXT
# ============================================================

def extract_job_title(
    experience_text: str
) -> str:
    """
    Extract a job title from legacy raw experience text.

    This is used only when structured experience data
    is not available.
    """

    text = _clean_text(
        experience_text
    )

    if not text:
        return ""

    patterns = [
        r"\b(machine learning engineer)\b",
        r"\b(machine learning intern)\b",
        r"\b(ai engineer)\b",
        r"\b(ai/ml engineer)\b",
        r"\b(artificial intelligence engineer)\b",
        r"\b(software engineer)\b",
        r"\b(software developer)\b",
        r"\b(full stack developer)\b",
        r"\b(full-stack developer)\b",
        r"\b(backend developer)\b",
        r"\b(frontend developer)\b",
        r"\b(data scientist)\b",
        r"\b(data analyst)\b",
        r"\b(ml engineer)\b",
        r"\b(intern)\b",
        r"\b(developer)\b",
        r"\b(engineer)\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return ""


# ============================================================
# EXTRACT DURATION FROM RAW TEXT
# ============================================================

def extract_duration_months(
    experience_text: str
) -> float:
    """
    Extract approximate duration from raw text.

    Examples:

        6 months -> 6
        1 year -> 12
        2 years -> 24
        1.5 years -> 18
    """

    text = _clean_text(
        experience_text
    ).lower()

    if not text:
        return 0.0

    # --------------------------------------------------------
    # Years
    # --------------------------------------------------------

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text
    )

    if year_match:

        years = float(
            year_match.group(1)
        )

        return round(
            years * 12,
            2
        )

    # --------------------------------------------------------
    # Months
    # --------------------------------------------------------

    month_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)",
        text
    )

    if month_match:

        months = float(
            month_match.group(1)
        )

        return round(
            months,
            2
        )

    return 0.0


# ============================================================
# EXTRACT TECHNOLOGIES FROM RAW TEXT
# ============================================================

def extract_experience_technologies(
    experience_text: str
) -> list[str]:
    """
    Extract commonly mentioned technologies from raw
    experience text.

    Used only as a fallback when structured technologies
    are unavailable.
    """

    text = _clean_text(
        experience_text
    ).lower()

    if not text:
        return []

    technology_patterns = {

        "python": r"\bpython\b",

        "java": r"\bjava\b",

        "javascript": r"\bjavascript\b",

        "typescript": r"\btypescript\b",

        "sql": r"\bsql\b",

        "mongodb": r"\bmongodb\b",

        "mysql": r"\bmysql\b",

        "postgresql": r"\bpostgres(?:ql)?\b",

        "react": r"\breact(?:\.js)?\b",

        "node.js": r"\bnode(?:\.js)?\b",

        "express.js": r"\bexpress(?:\.js)?\b",

        "fastapi": r"\bfastapi\b",

        "flask": r"\bflask\b",

        "django": r"\bdjango\b",

        "pandas": r"\bpandas\b",

        "numpy": r"\bnumpy\b",

        "scikit-learn": r"\bscikit[- ]learn\b",

        "tensorflow": r"\btensorflow\b",

        "pytorch": r"\bpytorch\b",

        "keras": r"\bkeras\b",

        "opencv": r"\bopencv\b",

        "docker": r"\bdocker\b",

        "git": r"\bgit\b",

        "github": r"\bgithub\b",

        "aws": r"\baws\b",

        "azure": r"\bazure\b",

        "gcp": r"\bgcp\b",

        "streamlit": r"\bstreamlit\b",

        "langchain": r"\blangchain\b",
    }

    technologies = []

    for technology, pattern in (
        technology_patterns.items()
    ):

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            technologies.append(
                technology
            )

    return technologies


# ============================================================
# CONVERT YEARS / MONTHS
# ============================================================

def _duration_to_months(
    duration: str
) -> float:
    """
    Convert a structured duration string into months.

    Examples:

        "6 months" -> 6
        "1 year" -> 12
        "1.5 years" -> 18
    """

    text = _clean_text(
        duration
    ).lower()

    if not text:
        return 0.0

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
        text
    )

    if year_match:

        years = float(
            year_match.group(1)
        )

        return round(
            years * 12,
            2
        )

    month_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:months?|mos?)",
        text
    )

    if month_match:

        months = float(
            month_match.group(1)
        )

        return round(
            months,
            2
        )

    return 0.0


# ============================================================
# ANALYZE STRUCTURED EXPERIENCE
# ============================================================

def analyze_structured_experience(
    experience: Any
) -> ExperienceEntry:
    """
    Analyze an experience entry produced by the AI
    resume extractor.

    Expected fields:

        job_title
        company
        employment_type
        location
        start_date
        end_date
        duration
        responsibilities
        technologies
    """

    if isinstance(
        experience,
        ExperienceEntry
    ):

        source = experience

    elif isinstance(
        experience,
        dict
    ):

        source = ExperienceEntry.model_validate(
            experience
        )

    else:

        raise TypeError(
            "Structured experience must be "
            "an ExperienceEntry or dictionary."
        )

    duration = _clean_text(
        source.duration
    )

    duration_months = _duration_to_months(
        duration
    )

    return ExperienceEntry(

        job_title=_clean_text(
            source.job_title
        ),

        company=_clean_text(
            source.company
        ),

        employment_type=_clean_text(
            source.employment_type
        ),

        location=_clean_text(
            source.location
        ),

        start_date=_clean_text(
            source.start_date
        ),

        end_date=_clean_text(
            source.end_date
        ),

        duration=duration,

        duration_months=duration_months,

        responsibilities=_clean_list(
            source.responsibilities
        ),

        technologies=_clean_list(
            source.technologies
        )
    )


# ============================================================
# ANALYZE RAW EXPERIENCE
# ============================================================

def analyze_experience_entry(
    experience_text: str
) -> ExperienceEntry:
    """
    Analyze one legacy raw experience string.

    This is the fallback path.
    """

    text = _clean_text(
        experience_text
    )

    if not text:
        return ExperienceEntry()

    job_title = extract_job_title(
        text
    )

    duration_months = extract_duration_months(
        text
    )

    technologies = extract_experience_technologies(
        text
    )

    return ExperienceEntry(

        job_title=job_title,

        duration_months=duration_months,

        responsibilities=[
            text
        ],

        technologies=technologies
    )


# ============================================================
# ANALYZE ALL EXPERIENCE
# ============================================================

def analyze_experience(
    experience: list[Any] | None = None,
    experience_details: list[Any] | None = None
) -> list[ExperienceEntry]:
    """
    Analyze resume experience.

    Priority:

        1. Structured experience_details
        2. Legacy experience strings

    This allows CareerIQ to support both the new
    AI extraction system and older profile data.
    """

    analyzed_experience = []

    # --------------------------------------------------------
    # Preferred path: structured AI experience
    # --------------------------------------------------------

    if experience_details:

        for item in experience_details:

            try:

                entry = analyze_structured_experience(
                    item
                )

                if (
                    entry.job_title
                    or entry.company
                    or entry.responsibilities
                    or entry.technologies
                ):

                    analyzed_experience.append(
                        entry
                    )

            except Exception:
                continue

        if analyzed_experience:

            return analyzed_experience

    # --------------------------------------------------------
    # Fallback path: legacy experience strings
    # --------------------------------------------------------

    normalized_experience = (
        normalize_experience_list(
            experience or []
        )
    )

    for experience_text in normalized_experience:

        entry = analyze_experience_entry(
            experience_text
        )

        if (
            entry.job_title
            or entry.responsibilities
            or entry.technologies
        ):

            analyzed_experience.append(
                entry
            )

    return analyzed_experience


# ============================================================
# TOTAL EXPERIENCE
# ============================================================

def calculate_total_experience_months(
    experience_entries: list[ExperienceEntry]
) -> float:
    """
    Calculate total known experience in months.
    """

    if not experience_entries:
        return 0.0

    total_months = sum(
        entry.duration_months
        for entry in experience_entries
    )

    return round(
        total_months,
        2
    )


# ============================================================
# TOTAL EXPERIENCE IN YEARS
# ============================================================

def calculate_total_experience_years(
    experience_entries: list[ExperienceEntry]
) -> float:
    """
    Calculate total known experience in years.
    """

    total_months = (
        calculate_total_experience_months(
            experience_entries
        )
    )

    return round(
        total_months / 12,
        2
    )


# ============================================================
# COLLECT UNIQUE VALUES
# ============================================================

def _unique_values(
    values: list[str]
) -> list[str]:
    """
    Return unique non-empty values while preserving order.
    """

    result = []

    seen = set()

    for value in values:

        value = _clean_text(
            value
        )

        if not value:
            continue

        key = value.lower()

        if key in seen:
            continue

        seen.add(
            key
        )

        result.append(
            value
        )

    return result


# ============================================================
# EXPERIENCE SUMMARY
# ============================================================

def build_experience_summary(
    experience_entries: list[ExperienceEntry]
) -> dict:
    """
    Build a high-level experience summary.
    """

    total_months = (
        calculate_total_experience_months(
            experience_entries
        )
    )

    total_years = (
        calculate_total_experience_years(
            experience_entries
        )
    )

    job_titles = _unique_values(
        [
            entry.job_title
            for entry in experience_entries
        ]
    )

    companies = _unique_values(
        [
            entry.company
            for entry in experience_entries
        ]
    )

    technologies = _unique_values(
        [
            technology
            for entry in experience_entries
            for technology in entry.technologies
        ]
    )

    employment_types = _unique_values(
        [
            entry.employment_type
            for entry in experience_entries
        ]
    )

    return {

        "total_experience_months":
            total_months,

        "total_experience_years":
            total_years,

        "job_titles":
            job_titles,

        "companies":
            companies,

        "technologies":
            technologies,

        "employment_types":
            employment_types,

        "experience_count":
            len(experience_entries)
    }


# ============================================================
# COMPLETE EXPERIENCE ANALYSIS
# ============================================================

def analyze_profile_experience(
    experience: list[Any] | None = None,
    experience_details: list[Any] | None = None
) -> dict:
    """
    Complete CareerIQ experience analysis.

    Preferred input:

        experience_details

    Fallback:

        experience
    """

    entries = analyze_experience(
        experience=experience,
        experience_details=experience_details
    )

    summary = build_experience_summary(
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

    test_experience_details = [

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
                "Developed machine learning models.",
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
    ]

    print()

    print(
        "=" * 60
    )

    print(
        "       CAREERIQ EXPERIENCE INTELLIGENCE"
    )

    print(
        "=" * 60
    )

    result = analyze_profile_experience(
        experience_details=
            test_experience_details
    )

    print()

    print(
        "Experience Entries:"
    )

    for index, entry in enumerate(
        result["entries"],
        start=1
    ):

        print()

        print(
            f"  Experience {index}:"
        )

        print(
            f"    Job Title: "
            f"{entry['job_title']}"
        )

        print(
            f"    Company: "
            f"{entry['company']}"
        )

        print(
            f"    Employment Type: "
            f"{entry['employment_type']}"
        )

        print(
            f"    Location: "
            f"{entry['location']}"
        )

        print(
            f"    Start Date: "
            f"{entry['start_date']}"
        )

        print(
            f"    End Date: "
            f"{entry['end_date']}"
        )

        print(
            f"    Duration: "
            f"{entry['duration']}"
        )

        print(
            f"    Duration Months: "
            f"{entry['duration_months']}"
        )

        print(
            f"    Technologies: "
            f"{entry['technologies']}"
        )

        print(
            f"    Responsibilities: "
            f"{entry['responsibilities']}"
        )

    print()

    print(
        "Experience Summary:"
    )

    print(
        result["summary"]
    )

    print()

    print(
        "=" * 60
    )