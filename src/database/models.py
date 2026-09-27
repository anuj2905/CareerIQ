from dataclasses import dataclass, field
from typing import List, Optional


# ============================================================
# STUDENT PROFILE MODEL
# ============================================================

@dataclass
class StudentProfile:

    id: Optional[int] = None

    name: str = ""

    education: List[str] = field(
        default_factory=list
    )

    skills: List[str] = field(
        default_factory=list
    )

    projects: List[str] = field(
        default_factory=list
    )

    experience: List[str] = field(
        default_factory=list
    )

    certifications: List[str] = field(
        default_factory=list
    )

    resume_text: str = ""

    resume_file_name: str = ""

    resume_file_size: int = 0


# ============================================================
# COMPANY MODEL
# ============================================================

@dataclass
class Company:

    id: Optional[int] = None

    company_name: str = ""

    email: str = ""

    website: str = ""

    industry: str = ""

    location: str = ""

    description: str = ""

    logo_url: str = ""


# ============================================================
# JOB MODEL
# ============================================================

@dataclass
class Job:

    id: Optional[int] = None

    company_id: Optional[int] = None

    title: str = ""

    description: str = ""

    location: str = ""

    employment_type: str = ""

    experience_required: float = 0.0

    education_required: str = ""

    salary_min: Optional[float] = None

    salary_max: Optional[float] = None

    status: str = "active"

    skills: List[str] = field(
        default_factory=list
    )


# ============================================================
# JOB APPLICATION MODEL
# ============================================================

@dataclass
class JobApplication:

    id: Optional[int] = None

    job_id: Optional[int] = None

    student_id: Optional[int] = None

    match_score: Optional[float] = None

    application_status: str = "applied"


# ============================================================
# CONVERT RESUME PROFILE → STUDENT PROFILE
# ============================================================

def create_student_profile(
    profile,
    resume_text: str = "",
    resume_file_name: str = "",
    resume_file_size: int = 0,
    student_id: Optional[int] = None
) -> StudentProfile:
    """
    Convert the existing ResumeProfile object into
    a database-compatible StudentProfile object.
    """

    return StudentProfile(

        id=student_id,

        name=getattr(
            profile,
            "name",
            ""
        ) or "",

        education=list(
            getattr(
                profile,
                "education",
                []
            ) or []
        ),

        skills=list(
            getattr(
                profile,
                "skills",
                []
            ) or []
        ),

        projects=list(
            getattr(
                profile,
                "projects",
                []
            ) or []
        ),

        experience=list(
            getattr(
                profile,
                "experience",
                []
            ) or []
        ),

        certifications=list(
            getattr(
                profile,
                "certifications",
                []
            ) or []
        ),

        resume_text=resume_text or "",

        resume_file_name=(
            resume_file_name or ""
        ),

        resume_file_size=(
            resume_file_size or 0
        )
    )