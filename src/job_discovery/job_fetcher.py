from typing import Any, Dict, List

import re
import requests


# ============================================================
# CONFIGURATION
# ============================================================

REMOTE_OK_API = "https://remoteok.com/api"
REQUEST_TIMEOUT = 15


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "python": {
        "python",
    },
    "java": {
        "java",
    },
    "javascript": {
        "javascript",
        "js",
    },
    "typescript": {
        "typescript",
        "ts",
    },
    "node.js": {
        "node.js",
        "nodejs",
        "node js",
    },
    "express.js": {
        "express.js",
        "expressjs",
        "express js",
    },
    "sql": {
        "sql",
        "structured query language",
    },
    "mongodb": {
        "mongodb",
        "mongo db",
        "mongo",
    },
    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
    },
    "fastapi": {
        "fastapi",
        "fast api",
    },
    "flask": {
        "flask",
    },
    "django": {
        "django",
    },
    "git": {
        "git",
    },
    "github": {
        "github",
        "git hub",
    },
    "docker": {
        "docker",
        "dockerized",
        "docker container",
        "docker containers",
    },
    "kubernetes": {
        "kubernetes",
        "k8s",
    },
    "machine learning": {
        "machine learning",
        "machine-learning",
        "ml",
    },
    "deep learning": {
        "deep learning",
        "deep-learning",
        "dl",
    },
    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn",
    },
    "tensorflow": {
        "tensorflow",
        "tensorflow keras",
        "tf",
    },
    "pytorch": {
        "pytorch",
        "torch",
    },
    "numpy": {
        "numpy",
    },
    "pandas": {
        "pandas",
    },
    "opencv": {
        "opencv",
        "open cv",
    },
    "computer vision": {
        "computer vision",
        "computer-vision",
    },
    "nlp": {
        "nlp",
        "natural language processing",
    },
    "llms": {
        "llm",
        "llms",
        "large language model",
        "large language models",
    },
    "generative ai": {
        "generative ai",
        "gen ai",
        "genai",
        "generative artificial intelligence",
    },
    "rag": {
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
    },
    "langchain": {
        "langchain",
    },
    "vector databases": {
        "vector database",
        "vector databases",
        "vector db",
        "vector dbs",
    },
    "embeddings": {
        "embedding",
        "embeddings",
        "vector embeddings",
    },
    "ai agents": {
        "ai agent",
        "ai agents",
        "agentic ai",
    },
    "streamlit": {
        "streamlit",
    },
    "react": {
        "react",
        "react.js",
        "reactjs",
    },
    "html": {
        "html",
        "html5",
    },
    "css": {
        "css",
        "css3",
    },
    "bootstrap": {
        "bootstrap",
    },
    "cloud": {
        "cloud",
        "cloud computing",
        "cloud infrastructure",
    },
    "aws": {
        "aws",
        "amazon web services",
    },
    "azure": {
        "azure",
        "microsoft azure",
    },
    "gcp": {
        "gcp",
        "google cloud",
        "google cloud platform",
    },
    "linux": {
        "linux",
    },
    "terraform": {
        "terraform",
    },
    "jenkins": {
        "jenkins",
    },
    "mlflow": {
        "mlflow",
        "ml flow",
    },
    "dsa": {
        "dsa",
        "data structures and algorithms",
        "data structures & algorithms",
    },
    "system design": {
        "system design",
        "system architecture",
    },
    "statistics": {
        "statistics",
        "statistical analysis",
    },
}


# ============================================================
# ROLE ALIASES
# ============================================================

ROLE_ALIASES = {
    "machine learning engineer": [
        "machine learning engineer",
        "ml engineer",
        "machine learning developer",
        "ml developer",
        "applied machine learning engineer",
        "applied ml engineer",
    ],
    "ai engineer": [
        "ai engineer",
        "artificial intelligence engineer",
        "ai developer",
        "artificial intelligence developer",
    ],
    "data scientist": [
        "data scientist",
        "data science",
        "data science engineer",
    ],
    "backend developer": [
        "backend developer",
        "backend engineer",
        "back-end developer",
        "back-end engineer",
        "software backend engineer",
    ],
}


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize(value: Any) -> str:
    """
    Normalize text for comparison.
    """

    return " ".join(
        str(value or "")
        .lower()
        .strip()
        .split()
    )


def _normalize_skill(skill: str) -> str:
    """
    Normalize a skill name.
    """

    return _normalize(skill)


# ============================================================
# CANONICAL SKILL
# ============================================================

def _canonical_skill(skill: str) -> str:
    """
    Convert a skill alias into its canonical skill name.
    """

    normalized = _normalize_skill(skill)

    if not normalized:
        return ""

    for canonical, aliases in SKILL_ALIASES.items():

        normalized_aliases = {
            _normalize_skill(alias)
            for alias in aliases
        }

        if normalized in normalized_aliases:
            return canonical

    return normalized


# ============================================================
# JOB TEXT
# ============================================================

def _job_text(job: Dict[str, Any]) -> str:
    """
    Combine important job fields into searchable text.
    """

    tags = job.get("tags") or []

    if not isinstance(tags, list):
        tags = [tags]

    return _normalize(
        " ".join(
            [
                str(job.get("position") or ""),
                str(job.get("description") or ""),
                " ".join(
                    str(tag)
                    for tag in tags
                ),
            ]
        )
    )


# ============================================================
# TEXT SKILL MATCHING
# ============================================================

def _contains_skill(
    job_text: str,
    skill: str
) -> bool:
    """
    Check whether a skill appears in the job text.

    Uses aliases and word-boundary matching to reduce
    accidental matches.
    """

    canonical = _canonical_skill(skill)

    if not canonical:
        return False

    aliases = SKILL_ALIASES.get(
        canonical,
        {canonical}
    )

    for alias in aliases:

        normalized_alias = _normalize_skill(
            alias
        )

        if not normalized_alias:
            continue

        escaped_alias = re.escape(
            normalized_alias
        )

        pattern = (
            rf"(?<!\w)"
            rf"{escaped_alias}"
            rf"(?!\w)"
        )

        if re.search(
            pattern,
            job_text,
            flags=re.IGNORECASE
        ):
            return True

    return False


# ============================================================
# ROLE MATCHING
# ============================================================

def _role_matches(
    job_position: str,
    keyword: str
) -> bool:
    """
    Check whether a job title matches the requested role.

    Supports role aliases such as:

        Machine Learning Engineer
        ML Engineer
        ML Developer
    """

    requested_role = _normalize(keyword)
    job_title = _normalize(job_position)

    if not requested_role:
        return True

    # --------------------------------------------------------
    # If we know aliases for this role
    # --------------------------------------------------------

    aliases = ROLE_ALIASES.get(
        requested_role
    )

    if aliases:

        return any(
            _normalize(alias) in job_title
            for alias in aliases
        )

    # --------------------------------------------------------
    # Generic keyword matching
    # --------------------------------------------------------

    requested_terms = requested_role.split()

    return all(
        term in job_title
        for term in requested_terms
    )


# ============================================================
# DETECT JOB SKILLS
# ============================================================

def _extract_job_skills(
    job: Dict[str, Any]
) -> List[str]:
    """
    Detect known technical skills from the job.

    Skills are detected from the job title,
    description, and tags.
    """

    job_text = _job_text(job)

    detected_skills = []

    for canonical_skill in SKILL_ALIASES:

        if _contains_skill(
            job_text,
            canonical_skill
        ):
            detected_skills.append(
                canonical_skill
            )

    return detected_skills


# ============================================================
# CALCULATE JOB MATCH
# ============================================================

def calculate_job_match(
    job: Dict[str, Any],
    resume_skills: List[str]
) -> Dict[str, Any]:
    """
    Calculate resume-to-job skill coverage.

    Main score:

        matched required skills
        -----------------------
        detected job skills

    This is different from the old approach,
    which divided matched resume skills by
    all resume skills.
    """

    resume_skills = [
        str(skill).strip()
        for skill in (resume_skills or [])
        if str(skill).strip()
    ]

    # --------------------------------------------------------
    # Convert resume skills to canonical skills
    # --------------------------------------------------------

    canonical_resume_skills = set()

    for skill in resume_skills:

        canonical = _canonical_skill(
            skill
        )

        if canonical:
            canonical_resume_skills.add(
                canonical
            )

    # --------------------------------------------------------
    # Detect skills required/mentioned by job
    # --------------------------------------------------------

    job_skills = _extract_job_skills(
        job
    )

    # --------------------------------------------------------
    # Find matching skills
    # --------------------------------------------------------

    matched_skills = [
        skill
        for skill in job_skills
        if skill in canonical_resume_skills
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill not in canonical_resume_skills
    ]

    # --------------------------------------------------------
    # Calculate match score
    # --------------------------------------------------------

    if job_skills:

        match_score = (
            len(matched_skills)
            / len(job_skills)
        )

    else:

        match_score = 0.0

    # --------------------------------------------------------
    # Match tags separately
    # --------------------------------------------------------

    tags = job.get("tags") or []

    if not isinstance(tags, list):
        tags = [str(tags)]

    matched_tags = []

    for tag in tags:

        canonical_tag = _canonical_skill(
            str(tag)
        )

        if (
            canonical_tag
            and canonical_tag
            in canonical_resume_skills
        ):
            matched_tags.append(
                str(tag)
            )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "match_score": round(
            match_score,
            4
        ),

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "matched_skill_count": len(
            matched_skills
        ),

        "job_skill_count": len(
            job_skills
        ),

        "resume_skill_count": len(
            resume_skills
        ),

        "job_skills": job_skills,

        "job_tags": tags,

        "matched_tags": matched_tags,
    }


# ============================================================
# FETCH REMOTE JOBS
# ============================================================

def fetch_remote_jobs(
    keyword: str = "",
    location: str = "",
    work_mode: str = "Remote",
    resume_skills: List[str] | None = None,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """
    Fetch current remote jobs from Remote OK's public JSON feed.

    Remote OK documents this public feed at /api and asks
    aggregators to link users back to the original job post.
    """

    response = requests.get(
        REMOTE_OK_API,
        headers={
            "User-Agent": "CareerIQ/1.0"
        },
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, list):

        raise ValueError(
            "Unexpected response format "
            "from the job source."
        )

    keyword = _normalize(keyword)
    location = _normalize(location)
    work_mode = _normalize(work_mode)

    resume_skills = resume_skills or []

    jobs: List[Dict[str, Any]] = []

    # ========================================================
    # PROCESS JOBS
    # ========================================================

    for item in payload:

        if (
            not isinstance(item, dict)
            or not item.get("position")
        ):
            continue

        job = {
            "id": item.get("id"),

            "position": item.get(
                "position",
                "Unknown role"
            ),

            "company": item.get(
                "company",
                "Unknown company"
            ),

            "location": item.get(
                "location",
                "Remote"
            ),

            "description": item.get(
                "description",
                ""
            ),

            "tags": item.get(
                "tags"
            ) or [],

            "url": (
                item.get("url")
                or item.get("apply_url")
                or ""
            ),

            "date": item.get(
                "date",
                ""
            ),

            "salary_min": item.get(
                "salary_min"
            ),

            "salary_max": item.get(
                "salary_max"
            ),
        }

        # ====================================================
        # ROLE FILTER
        # ====================================================

        if keyword:

            if not _role_matches(
                job["position"],
                keyword
            ):
                continue

        # ====================================================
        # LOCATION FILTER
        # ====================================================

        job_text = _job_text(job)

        if location:

            if location not in job_text:
                continue

        # ====================================================
        # WORK MODE FILTER
        # ====================================================

        if work_mode == "remote":

            if "remote" not in job_text:

                # Remote OK is already a remote-job feed,
                # but keep this defensive check.
                continue

        # ====================================================
        # CALCULATE MATCH
        # ====================================================

        match = calculate_job_match(
            job,
            resume_skills
        )

        job.update(match)

        jobs.append(job)

    # ========================================================
    # SORT RESULTS
    # ========================================================

    jobs.sort(
        key=lambda job: (
            job.get(
                "match_score",
                0.0
            ),

            job.get(
                "date",
                ""
            ),
        ),
        reverse=True,
    )

    # ========================================================
    # RETURN LIMITED RESULTS
    # ========================================================

    return jobs[
        : max(
            1,
            int(limit)
        )
    ]