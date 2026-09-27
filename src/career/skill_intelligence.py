from typing import Any, Dict, Iterable, List, Set


# ============================================================
# SKILL INTELLIGENCE ENGINE
# ============================================================
#
# Central skill-processing module for CareerIQ.
#
# Used by:
#   - Resume Analysis
#   - Career Prediction
#   - Career Recommendation
#   - Skill Gap Analysis
#   - Job Matching
#   - Company Candidate Matching
#
# Main responsibilities:
#   1. Normalize skill names
#   2. Resolve skill aliases
#   3. Compare skills
#   4. Calculate skill coverage
#   5. Identify missing skills
#   6. Provide reusable skill intelligence
#
# Scores are always returned in the range 0.0 - 1.0.
# UI can convert them to percentages.
# ============================================================


# ============================================================
# CANONICAL SKILLS
# ============================================================

SKILL_ALIASES: Dict[str, Set[str]] = {

    "python": {
        "python",
        "python3",
        "python 3",
    },

    "java": {
        "java",
    },

    "javascript": {
        "javascript",
        "js",
        "ecmascript",
    },

    "typescript": {
        "typescript",
        "ts",
    },

    "c++": {
        "c++",
        "cpp",
    },

    "c#": {
        "c#",
        "c sharp",
    },

    "sql": {
        "sql",
        "structured query language",
    },

    "html": {
        "html",
        "html5",
    },

    "css": {
        "css",
        "css3",
    },

    "react": {
        "react",
        "react.js",
        "reactjs",
    },

    "node.js": {
        "node",
        "node.js",
        "nodejs",
        "node js",
    },

    "express.js": {
        "express",
        "express.js",
        "expressjs",
        "express js",
    },

    "mongodb": {
        "mongodb",
        "mongo db",
        "mongo",
    },

    "mysql": {
        "mysql",
        "my sql",
    },

    "postgresql": {
        "postgresql",
        "postgres",
        "postgre sql",
    },

    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest api development",
    },

    "graphql": {
        "graphql",
        "graph ql",
    },

    "git": {
        "git",
        "git scm",
    },

    "github": {
        "github",
        "git hub",
    },

    "docker": {
        "docker",
        "docker container",
        "docker containers",
        "containerization",
    },

    "kubernetes": {
        "kubernetes",
        "k8s",
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

    "machine learning": {
        "machine learning",
        "machine-learning",
        "ml",
        "machine learning algorithms",
    },

    "deep learning": {
        "deep learning",
        "deep-learning",
        "dl",
    },

    "artificial intelligence": {
        "artificial intelligence",
        "artificial intelligence ai",
        "ai",
        "artificial-intelligence",
    },

    "data science": {
        "data science",
        "data-science",
        "data scientist",
    },

    "data analysis": {
        "data analysis",
        "data analytics",
        "data analyst",
    },

    "statistics": {
        "statistics",
        "statistical analysis",
        "statistical methods",
    },

    "numpy": {
        "numpy",
    },

    "pandas": {
        "pandas",
    },

    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn",
        "scikit",
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

    "keras": {
        "keras",
    },

    "opencv": {
        "opencv",
        "open cv",
        "opencv-python",
    },

    "nlp": {
        "nlp",
        "natural language processing",
    },

    "computer vision": {
        "computer vision",
        "cv",
    },

    "llms": {
        "llm",
        "llms",
        "large language model",
        "large language models",
    },

    "generative ai": {
        "generative ai",
        "generative artificial intelligence",
        "gen ai",
        "genai",
    },

    "rag": {
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "retrieval augmented generation systems",
    },

    "langchain": {
        "langchain",
    },

    "vector database": {
        "vector database",
        "vector databases",
        "vector db",
        "vector dbs",
    },

    "mlops": {
        "mlops",
        "ml ops",
        "machine learning operations",
    },

    "mlflow": {
        "mlflow",
        "ml flow",
    },

    "data visualization": {
        "data visualization",
        "data visualisation",
    },

    "power bi": {
        "power bi",
        "powerbi",
    },

    "tableau": {
        "tableau",
    },

    "streamlit": {
        "streamlit",
    },

    "flutter": {
        "flutter",
    },

    "dart": {
        "dart",
    },
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value: Any) -> str:
    """
    Normalize arbitrary text for comparison.

    Example:
        "  Machine-Learning  "
        -> "machine learning"
    """

    if value is None:
        return ""

    text = str(value).lower().strip()

    replacements = {
        "_": " ",
        "-": " ",
        "/": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return " ".join(text.split())


# ============================================================
# ALIAS INDEX
# ============================================================

def _build_alias_index() -> Dict[str, str]:
    """
    Build an alias -> canonical skill lookup table.
    """

    alias_index: Dict[str, str] = {}

    for canonical_skill, aliases in SKILL_ALIASES.items():

        canonical = normalize_text(
            canonical_skill
        )

        alias_index[canonical] = canonical

        for alias in aliases:

            normalized_alias = normalize_text(
                alias
            )

            if normalized_alias:
                alias_index[
                    normalized_alias
                ] = canonical

    return alias_index


_ALIAS_INDEX = _build_alias_index()


# ============================================================
# CANONICAL SKILL
# ============================================================

def canonicalize_skill(skill: Any) -> str:
    """
    Convert a skill into its canonical representation.

    Examples:

        ML
        -> machine learning

        sklearn
        -> scikit learn

        NodeJS
        -> node.js
    """

    normalized = normalize_text(skill)

    if not normalized:
        return ""

    return _ALIAS_INDEX.get(
        normalized,
        normalized
    )


# ============================================================
# CLEAN SKILL LIST
# ============================================================

def normalize_skills(
    skills: Any
) -> List[str]:
    """
    Convert different skill formats into
    a clean canonical skill list.
    """

    if skills is None:
        return []

    if isinstance(skills, str):

        values = [
            item.strip()
            for item in skills.replace(
                ",",
                "\n"
            ).splitlines()
            if item.strip()
        ]

    elif isinstance(
        skills,
        (list, tuple, set)
    ):

        values = [
            str(item).strip()
            for item in skills
            if str(item).strip()
        ]

    else:

        values = [
            str(skills).strip()
        ]

    canonical_skills = []

    for skill in values:

        canonical = canonicalize_skill(
            skill
        )

        if canonical:
            canonical_skills.append(
                canonical
            )

    # Remove duplicates while preserving order
    return list(
        dict.fromkeys(
            canonical_skills
        )
    )


# ============================================================
# SKILL SET
# ============================================================

def skill_set(
    skills: Any
) -> Set[str]:
    """
    Return normalized skills as a set.
    """

    return set(
        normalize_skills(skills)
    )


# ============================================================
# SKILL MATCH
# ============================================================

def calculate_skill_match(
    user_skills: Any,
    required_skills: Any
) -> Dict[str, Any]:
    """
    Compare user skills against required skills.

    Returns:

        score
        matched_skills
        missing_skills
        extra_skills
    """

    user_set = skill_set(
        user_skills
    )

    required_set = skill_set(
        required_skills
    )

    if not required_set:

        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": sorted(
                user_set
            ),
        }

    matched = user_set.intersection(
        required_set
    )

    missing = required_set.difference(
        user_set
    )

    extra = user_set.difference(
        required_set
    )

    score = (
        len(matched)
        / len(required_set)
    )

    return {
        "score": round(
            score,
            4
        ),
        "matched_skills": sorted(
            matched
        ),
        "missing_skills": sorted(
            missing
        ),
        "extra_skills": sorted(
            extra
        ),
    }


# ============================================================
# SKILL COVERAGE
# ============================================================

def calculate_skill_coverage(
    user_skills: Any,
    required_skills: Any
) -> float:
    """
    Return only the skill coverage score.
    """

    result = calculate_skill_match(
        user_skills=user_skills,
        required_skills=required_skills
    )

    return result["score"]


# ============================================================
# MISSING SKILLS
# ============================================================

def get_missing_skills(
    user_skills: Any,
    required_skills: Any
) -> List[str]:
    """
    Return skills required by the target
    but missing from the user profile.
    """

    result = calculate_skill_match(
        user_skills=user_skills,
        required_skills=required_skills
    )

    return result["missing_skills"]


# ============================================================
# MATCHED SKILLS
# ============================================================

def get_matched_skills(
    user_skills: Any,
    required_skills: Any
) -> List[str]:
    """
    Return skills present in both sets.
    """

    result = calculate_skill_match(
        user_skills=user_skills,
        required_skills=required_skills
    )

    return result["matched_skills"]


# ============================================================
# SKILL DIFFERENCE
# ============================================================

def compare_skill_sets(
    first_skills: Any,
    second_skills: Any
) -> Dict[str, Any]:
    """
    Compare two skill sets.

    Useful for:
        Resume vs Job
        Resume vs Career Role
        Student vs Company Requirements
    """

    first = skill_set(
        first_skills
    )

    second = skill_set(
        second_skills
    )

    common = first.intersection(
        second
    )

    only_first = first.difference(
        second
    )

    only_second = second.difference(
        first
    )

    return {
        "common_skills": sorted(
            common
        ),
        "only_first": sorted(
            only_first
        ),
        "only_second": sorted(
            only_second
        ),
    }


# ============================================================
# SKILL SIMILARITY
# ============================================================

def calculate_skill_similarity(
    first_skills: Any,
    second_skills: Any
) -> float:
    """
    Calculate symmetric skill similarity.

    Uses the Jaccard similarity:

        intersection / union

    This is different from job skill coverage.

    Job coverage:
        matched / required

    Similarity:
        matched / union
    """

    first = skill_set(
        first_skills
    )

    second = skill_set(
        second_skills
    )

    if not first and not second:
        return 1.0

    if not first or not second:
        return 0.0

    intersection = len(
        first.intersection(
            second
        )
    )

    union = len(
        first.union(
            second
        )
    )

    if union == 0:
        return 0.0

    return round(
        intersection / union,
        4
    )


# ============================================================
# SKILL GROUPS
# ============================================================

SKILL_GROUPS = {

    "programming": {
        "python",
        "java",
        "javascript",
        "typescript",
        "c++",
        "c#",
    },

    "data": {
        "sql",
        "numpy",
        "pandas",
        "statistics",
        "data analysis",
        "data science",
        "data visualization",
        "power bi",
        "tableau",
    },

    "machine_learning": {
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "keras",
        "mlflow",
        "mlops",
    },

    "ai": {
        "artificial intelligence",
        "deep learning",
        "nlp",
        "computer vision",
        "llms",
        "generative ai",
        "rag",
        "langchain",
    },

    "backend": {
        "python",
        "node.js",
        "express.js",
        "fastapi",
        "flask",
        "django",
        "sql",
        "mongodb",
        "mysql",
        "postgresql",
        "rest api",
        "graphql",
    },

    "devops": {
        "git",
        "github",
        "docker",
        "kubernetes",
        "mlops",
        "mlflow",
    },

    "frontend": {
        "html",
        "css",
        "javascript",
        "typescript",
        "react",
    },

    "mobile": {
        "flutter",
        "dart",
    },
}


# ============================================================
# SKILL CATEGORY ANALYSIS
# ============================================================

def analyze_skill_categories(
    skills: Any
) -> Dict[str, List[str]]:
    """
    Determine which technical categories
    are represented in a skill set.
    """

    user_skills = skill_set(
        skills
    )

    result: Dict[str, List[str]] = {}

    for category, category_skills in (
        SKILL_GROUPS.items()
    ):

        matched = user_skills.intersection(
            category_skills
        )

        if matched:

            result[category] = sorted(
                matched
            )

    return result


# ============================================================
# SKILL PRIORITY
# ============================================================

def prioritize_missing_skills(
    missing_skills: Any,
    required_skills: Any
) -> List[Dict[str, Any]]:
    """
    Give missing skills a basic priority.

    Priority is determined by how important
    the skill is within the required skill set.

    This is intentionally deterministic.
    A future ML/LLM layer can improve this
    using job-market and role-specific data.
    """

    missing = normalize_skills(
        missing_skills
    )

    required = normalize_skills(
        required_skills
    )

    if not missing:
        return []

    required_count = len(
        required
    )

    results = []

    for skill in missing:

        # Default priority
        priority = "Medium"

        # Core skills receive higher priority
        if skill in {
            "python",
            "java",
            "javascript",
            "machine learning",
            "deep learning",
            "sql",
            "scikit-learn",
            "tensorflow",
            "pytorch",
        }:
            priority = "High"

        elif skill in {
            "docker",
            "mlops",
            "mlflow",
            "fastapi",
            "rest api",
            "git",
        }:
            priority = "Medium"

        results.append({
            "skill": skill,
            "priority": priority,
            "required": skill in required,
            "required_skill_count": required_count,
        })

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    results.sort(
        key=lambda item: (
            priority_order[
                item["priority"]
            ],
            item["skill"]
        )
    )

    return results


# ============================================================
# PROFILE SKILL SUMMARY
# ============================================================

def build_skill_summary(
    skills: Any
) -> Dict[str, Any]:
    """
    Build a reusable summary of a student's skills.
    """

    normalized = normalize_skills(
        skills
    )

    categories = analyze_skill_categories(
        normalized
    )

    return {
        "total_skills": len(
            normalized
        ),
        "skills": normalized,
        "categories": categories,
    }


# ============================================================
# FULL SKILL INTELLIGENCE
# ============================================================

def analyze_skills(
    user_skills: Any,
    target_skills: Any = None
) -> Dict[str, Any]:
    """
    Main public function.

    If target_skills are supplied, it additionally
    calculates matching and skill gaps.
    """

    summary = build_skill_summary(
        user_skills
    )

    result = {
        "skills": summary["skills"],
        "total_skills": summary[
            "total_skills"
        ],
        "categories": summary[
            "categories"
        ],
    }

    if target_skills is not None:

        match = calculate_skill_match(
            user_skills=user_skills,
            required_skills=target_skills
        )

        result.update({
            "match_score": match[
                "score"
            ],
            "matched_skills": match[
                "matched_skills"
            ],
            "missing_skills": match[
                "missing_skills"
            ],
            "extra_skills": match[
                "extra_skills"
            ],
        })

        result[
            "prioritized_missing_skills"
        ] = prioritize_missing_skills(
            match["missing_skills"],
            target_skills
        )

    return result


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    user_skills = [
        "Python",
        "ML",
        "Pandas",
        "NumPy",
        "sklearn",
        "SQL",
        "FastAPI",
        "NodeJS",
        "Mongo",
        "Docker",
    ]

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
        "MLOps",
    ]

    print(
        "\n=========================================="
    )

    print(
        "       CAREERIQ SKILL INTELLIGENCE"
    )

    print(
        "=========================================="
    )

    result = analyze_skills(
        user_skills=user_skills,
        target_skills=required_skills
    )

    print(
        "\nNormalized Skills:"
    )

    for skill in result["skills"]:
        print(
            f"  ✓ {skill}"
        )

    print(
        "\nSkill Match:",
        f'{result["match_score"] * 100:.1f}%'
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
        "\nPrioritized Missing Skills:"
    )

    for item in result[
        "prioritized_missing_skills"
    ]:

        print(
            f'  {item["priority"]}: '
            f'{item["skill"]}'
        )

    print(
        "\nSkill Categories:"
    )

    for category, skills in result[
        "categories"
    ].items():

        print(
            f"  {category}: "
            f"{', '.join(skills)}"
        )

    print(
        "\n=========================================="
    )