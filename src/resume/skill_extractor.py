from dotenv import load_dotenv

load_dotenv()


import json
import os
from typing import Any

from agno.agent import Agent

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

from agno.models.openai import OpenAIResponses

from src.career.skill_intelligence import (
    normalize_skills
)


# ============================================================
# EXPERIENCE STRUCTURE
# ============================================================

class ExperienceDetails(BaseModel):
    """
    Structured representation of one professional experience.
    """

    model_config = ConfigDict(
        extra="ignore"
    )

    job_title: str = ""

    company: str = ""

    employment_type: str = ""

    location: str = ""

    start_date: str = ""

    end_date: str = ""

    duration: str = ""

    responsibilities: list[str] = Field(
        default_factory=list
    )

    technologies: list[str] = Field(
        default_factory=list
    )


# ============================================================
# RESUME PROFILE STRUCTURE
# ============================================================

class ResumeProfile(BaseModel):
    """
    Structured representation of a student's resume.

    The existing fields are preserved for compatibility
    with the current CareerIQ application.
    """

    model_config = ConfigDict(
        extra="ignore"
    )

    name: str = ""

    education: list[str] = Field(
        default_factory=list
    )

    skills: list[str] = Field(
        default_factory=list
    )

    projects: list[str] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Existing experience field
    # --------------------------------------------------------

    experience: list[str] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # New structured experience field
    # --------------------------------------------------------

    experience_details: list[ExperienceDetails] = Field(
        default_factory=list
    )

    certifications: list[str] = Field(
        default_factory=list
    )


# ============================================================
# PROFILE CLEANING
# ============================================================

def _clean_text(
    value: Any
) -> str:
    """
    Clean a single text value.
    """

    if value is None:
        return ""

    return " ".join(
        str(value)
        .strip()
        .split()
    )


# ============================================================
# CLEAN LIST
# ============================================================

def _clean_list(
    values: Any
) -> list[str]:
    """
    Clean a list of extracted values.

    Removes:
        - None
        - empty strings
        - unnecessary whitespace
        - duplicate entries
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

        comparison_key = text.lower()

        if comparison_key in seen:
            continue

        seen.add(
            comparison_key
        )

        cleaned.append(
            text
        )

    return cleaned


# ============================================================
# CLEAN EXPERIENCE DETAILS
# ============================================================

def _clean_experience_details(
    experiences: Any
) -> list[ExperienceDetails]:
    """
    Clean and validate structured experience entries.
    """

    if not experiences:
        return []

    cleaned_entries = []

    for experience in experiences:

        try:

            if isinstance(
                experience,
                ExperienceDetails
            ):
                entry = experience

            elif isinstance(
                experience,
                dict
            ):
                entry = ExperienceDetails.model_validate(
                    experience
                )

            else:
                continue

        except Exception:
            continue

        entry = ExperienceDetails(

            job_title=_clean_text(
                entry.job_title
            ),

            company=_clean_text(
                entry.company
            ),

            employment_type=_clean_text(
                entry.employment_type
            ),

            location=_clean_text(
                entry.location
            ),

            start_date=_clean_text(
                entry.start_date
            ),

            end_date=_clean_text(
                entry.end_date
            ),

            duration=_clean_text(
                entry.duration
            ),

            responsibilities=_clean_list(
                entry.responsibilities
            ),

            technologies=normalize_profile_skills(
                entry.technologies
            )
        )

        cleaned_entries.append(
            entry
        )

    return cleaned_entries


# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_profile_skills(
    skills: Any
) -> list[str]:
    """
    Normalize extracted skills using the centralized
    CareerIQ Skill Intelligence Engine.
    """

    if not skills:
        return []

    return normalize_skills(
        skills
    )


# ============================================================
# PROFILE NORMALIZATION
# ============================================================

def normalize_resume_profile(
    profile: ResumeProfile
) -> ResumeProfile:
    """
    Clean and normalize an extracted ResumeProfile.

    The LLM extracts information.

    This function validates and normalizes that information.
    """

    if not isinstance(
        profile,
        ResumeProfile
    ):

        raise TypeError(
            "profile must be a ResumeProfile."
        )

    cleaned_experience_details = (
        _clean_experience_details(
            profile.experience_details
        )
    )

    # --------------------------------------------------------
    # If structured experience exists but legacy experience
    # is empty, create compatible experience strings.
    # --------------------------------------------------------

    experience = _clean_list(
        profile.experience
    )

    if not experience:

        for entry in cleaned_experience_details:

            parts = []

            if entry.job_title:
                parts.append(
                    entry.job_title
                )

            if entry.company:
                parts.append(
                    f"at {entry.company}"
                )

            if entry.duration:
                parts.append(
                    f"({entry.duration})"
                )

            if parts:

                experience.append(
                    " ".join(parts)
                )

    return ResumeProfile(

        name=_clean_text(
            profile.name
        ),

        education=_clean_list(
            profile.education
        ),

        skills=normalize_profile_skills(
            profile.skills
        ),

        projects=_clean_list(
            profile.projects
        ),

        experience=experience,

        experience_details=(
            cleaned_experience_details
        ),

        certifications=_clean_list(
            profile.certifications
        )
    )


# ============================================================
# CREATE RESUME EXTRACTION AGENT
# ============================================================

def create_resume_extraction_agent() -> Agent:
    """
    Create the AI agent used for resume extraction.
    """

    if not os.getenv(
        "OPENAI_API_KEY"
    ):

        raise RuntimeError(
            "OPENAI_API_KEY was not found. "
            "Make sure your .env file exists in "
            "the CareerIQ project root."
        )

    return Agent(

        model=OpenAIResponses(
            id="gpt-5.6"
        ),

        output_schema=ResumeProfile,

        structured_outputs=True
    )


# ============================================================
# BUILD EXTRACTION PROMPT
# ============================================================

def build_extraction_prompt(
    resume_text: str
) -> str:
    """
    Build the structured resume extraction prompt.
    """

    return f"""
You are CareerIQ's professional resume extraction engine.

Your task is to analyze the provided resume and extract
ONLY information that is explicitly present in the resume.

Return ONLY the required structured output.

Do NOT invent information.

Do NOT infer missing information.

Do NOT guess skills.

Do NOT guess employment dates.

Do NOT guess companies.

Do NOT create projects that are not present.

Do NOT add explanations outside the structured output.


============================================================
1. CANDIDATE NAME
============================================================

Extract the candidate's full name.

If the name is not clearly available,
return an empty string.


============================================================
2. EDUCATION
============================================================

Extract every education entry explicitly present.

Include useful information such as:

- Degree
- Branch / field of study
- College / university
- Institution
- Graduation year when explicitly available
- Other relevant education details

Keep each education entry separate.

Do not invent missing details.


============================================================
3. SKILLS
============================================================

Extract technical and professional skills explicitly
mentioned in the resume.

Include:

- Programming languages
- Frameworks
- Libraries
- Databases
- Cloud technologies
- AI / ML technologies
- Data technologies
- Development tools
- DevOps technologies
- Other clearly stated professional skills

Return each skill separately.

IMPORTANT:

Extract the skill as written in the resume.

For example:

If the resume says:

"ML"

return:

"ML"

Do NOT automatically change it to:

"Machine Learning"

CareerIQ will normalize skills separately.


============================================================
4. PROJECTS
============================================================

Extract projects explicitly mentioned.

For each project:

- Include project name.
- Include concise description when available.
- Include important technologies when clearly mentioned.

Keep each project separate.

Do not invent project descriptions.


============================================================
5. EXPERIENCE
============================================================

Extract professional experience explicitly mentioned.

IMPORTANT:

Professional experience includes:

- Internships
- Full-time employment
- Part-time employment
- Contract work
- Freelance work
- Other clearly identified professional roles

Do NOT convert projects into work experience.

Do NOT convert coursework into work experience.


For every experience entry, extract structured information:

JOB TITLE
- Extract the exact job title when available.

COMPANY
- Extract the company or organization name when available.

EMPLOYMENT TYPE
- Examples:
  Internship
  Full-time
  Part-time
  Contract
  Freelance
- Only include it when explicitly stated or clearly identified.

LOCATION
- Extract location when explicitly available.

START DATE
- Extract only when explicitly available.

END DATE
- Extract only when explicitly available.

DURATION
- Extract duration when explicitly available.
- Examples:
  "6 months"
  "1 year"
  "Jan 2025 - Jun 2025"

RESPONSIBILITIES
- Extract important responsibilities and work performed.
- Keep each responsibility as a separate item.

TECHNOLOGIES
- Extract technologies explicitly associated with
  that particular experience.
- Do NOT add technologies merely because they appear
  elsewhere in the resume.

If a field is not available, return an empty string
or an empty list.

Do not guess.


============================================================
6. CERTIFICATIONS
============================================================

Extract certifications explicitly mentioned.

Include:

- Certification name
- Issuing organization/provider
- Year when explicitly available

Keep each certification separate.

Do not invent certifications.


============================================================
IMPORTANT EXTRACTION RULES
============================================================

1. Extract only information present in the resume.

2. Never fabricate information.

3. Never infer missing information as fact.

4. Never add skills simply because they are related
   to another skill.

5. Never convert projects into experience.

6. Never convert coursework into professional experience.

7. Preserve useful technical details.

8. Remove obvious duplication.

9. If a section is absent, return an empty list.

10. If the candidate name is unavailable, return "".

11. For missing experience fields, return empty values.

12. Keep experience entries separate.

13. Keep responsibilities separate.

14. Keep technologies separate.

15. Return ONLY the structured ResumeProfile output.

16. Do not include explanations.

17. Do not include Markdown.

18. Do not include commentary.

19. Do not include confidence scores.

20. Do not create information that is not explicitly
    supported by the resume.


============================================================
RESUME TEXT
============================================================

{resume_text}
"""


# ============================================================
# CONVERT RESPONSE TO PROFILE
# ============================================================

def _convert_response_to_profile(
    extracted_profile: Any
) -> ResumeProfile:
    """
    Convert different possible AI response formats
    into ResumeProfile.

    Supports:

        ResumeProfile
        dict
        JSON string
    """

    if isinstance(
        extracted_profile,
        ResumeProfile
    ):

        return extracted_profile

    if isinstance(
        extracted_profile,
        dict
    ):

        try:

            return ResumeProfile.model_validate(
                extracted_profile
            )

        except Exception as exc:

            raise RuntimeError(
                "The AI returned invalid "
                "resume profile data."
            ) from exc

    # --------------------------------------------------------
    # Some Agno/OpenAI configurations can return structured
    # content as a JSON string.
    # --------------------------------------------------------

    if isinstance(
        extracted_profile,
        str
    ):

        text = extracted_profile.strip()

        if not text:

            raise RuntimeError(
                "The AI returned an empty response."
            )

        try:

            parsed = json.loads(
                text
            )

        except json.JSONDecodeError as exc:

            raise RuntimeError(
                "The AI returned text instead of "
                "valid structured resume data."
            ) from exc

        try:

            return ResumeProfile.model_validate(
                parsed
            )

        except Exception as exc:

            raise RuntimeError(
                "The AI returned invalid "
                "resume profile data."
            ) from exc

    raise RuntimeError(
        "Unexpected AI response type: "
        f"{type(extracted_profile).__name__}"
    )


# ============================================================
# EXTRACT RESUME PROFILE
# ============================================================

def extract_resume_profile(
    resume_text: str
) -> ResumeProfile:
    """
    Extract a structured ResumeProfile from resume text.

    Pipeline:

        Resume Text
            ↓
        GPT-5.6
            ↓
        Structured ResumeProfile
            ↓
        Validation
            ↓
        Normalization
            ↓
        Final ResumeProfile
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not isinstance(
        resume_text,
        str
    ):

        raise TypeError(
            "resume_text must be a string."
        )

    resume_text = resume_text.strip()

    if not resume_text:

        raise ValueError(
            "Resume text is empty."
        )

    # --------------------------------------------------------
    # Create agent
    # --------------------------------------------------------

    agent = create_resume_extraction_agent()

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = build_extraction_prompt(
        resume_text
    )

    # --------------------------------------------------------
    # Run AI extraction
    # --------------------------------------------------------

    try:

        response = agent.run(
            prompt
        )

    except Exception as exc:

        raise RuntimeError(
            "Resume extraction failed: "
            f"{str(exc)}"
        ) from exc

    # --------------------------------------------------------
    # Validate AI response
    # --------------------------------------------------------

    if response is None:

        raise RuntimeError(
            "The resume extraction agent "
            "returned no response."
        )

    extracted_profile = getattr(
        response,
        "content",
        None
    )

    if extracted_profile is None:

        raise RuntimeError(
            "The AI response did not contain "
            "structured resume data."
        )

    # --------------------------------------------------------
    # Convert response
    # --------------------------------------------------------

    profile = _convert_response_to_profile(
        extracted_profile
    )

    # --------------------------------------------------------
    # Normalize final profile
    # --------------------------------------------------------

    profile = normalize_resume_profile(
        profile
    )

    # --------------------------------------------------------
    # Debug output
    # --------------------------------------------------------

    print(
        "\n========== RESUME PROFILE EXTRACTION =========="
    )

    print(
        "\nName:",
        profile.name
    )

    print(
        "\nEducation:"
    )

    for item in profile.education:

        print(
            f"  • {item}"
        )

    print(
        "\nSkills:"
    )

    for skill in profile.skills:

        print(
            f"  • {skill}"
        )

    print(
        "\nProjects:"
    )

    for project in profile.projects:

        print(
            f"  • {project}"
        )

    print(
        "\nExperience:"
    )

    for experience in profile.experience:

        print(
            f"  • {experience}"
        )

    print(
        "\nStructured Experience:"
    )

    for index, experience in enumerate(
        profile.experience_details,
        start=1
    ):

        print(
            f"\n  Experience {index}:"
        )

        print(
            f"    Job Title: "
            f"{experience.job_title}"
        )

        print(
            f"    Company: "
            f"{experience.company}"
        )

        print(
            f"    Employment Type: "
            f"{experience.employment_type}"
        )

        print(
            f"    Location: "
            f"{experience.location}"
        )

        print(
            f"    Start Date: "
            f"{experience.start_date}"
        )

        print(
            f"    End Date: "
            f"{experience.end_date}"
        )

        print(
            f"    Duration: "
            f"{experience.duration}"
        )

        print(
            f"    Technologies: "
            f"{experience.technologies}"
        )

        print(
            f"    Responsibilities: "
            f"{experience.responsibilities}"
        )

    print(
        "\nCertifications:"
    )

    for certification in profile.certifications:

        print(
            f"  • {certification}"
        )

    print(
        "\n==============================================="
    )

    return profile


# ============================================================
# PROFILE TO DICTIONARY
# ============================================================

def profile_to_dict(
    profile: ResumeProfile
) -> dict:
    """
    Convert ResumeProfile into a normal dictionary.

    Useful for:

        - Database storage
        - APIs
        - Matching engines
        - Streamlit session state
        - JSON serialization
    """

    if not isinstance(
        profile,
        ResumeProfile
    ):

        raise TypeError(
            "profile must be a ResumeProfile."
        )

    return profile.model_dump()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_resume = """

Anuj Patil

Education:
B.E. in Computer Engineering

Skills:
Python, SQL, ML, Pandas, NumPy, sklearn, FastAPI

Projects:
CareerIQ - AI Resume Analyzer
AI Attendance System using Python and OpenCV

Experience:
Machine Learning Intern at ABC Technologies
Internship
January 2026 - June 2026
Worked on machine learning models and data preprocessing.
Used Python, Pandas, NumPy, Scikit-learn and OpenCV.

Certifications:
Python for Data Science

"""

    try:

        profile = extract_resume_profile(
            test_resume
        )

        print(
            "\n\nFINAL PROFILE"
        )

        print(
            "=" * 60
        )

        print(
            profile.model_dump()
        )

        print(
            "\nProfile Dictionary:"
        )

        print(
            profile_to_dict(
                profile
            )
        )

        print(
            "\n" + "=" * 60
        )

    except Exception as exc:

        print(
            "\nERROR:"
        )

        print(
            str(exc)
        )