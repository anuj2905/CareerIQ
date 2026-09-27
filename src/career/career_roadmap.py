from typing import Any, Dict, List


# ============================================================
# CAREER ROADMAPS
# ============================================================

CAREER_ROADMAPS = {
    "Machine Learning Engineer": {
        "description": (
            "Build strong foundations in Python, data handling, "
            "machine learning, deep learning, and ML deployment."
        ),
        "phases": [
            {
                "phase": 1,
                "title": "Python & Data Foundations",
                "duration": "3–4 weeks",
                "skills": [
                    "Python",
                    "NumPy",
                    "Pandas",
                    "SQL",
                    "Git",
                ],
                "projects": [
                    "Data Analysis Project",
                    "Exploratory Data Analysis Project",
                ],
            },
            {
                "phase": 2,
                "title": "Machine Learning",
                "duration": "4–6 weeks",
                "skills": [
                    "Machine Learning",
                    "Scikit-learn",
                    "Statistics",
                    "Feature Engineering",
                    "Model Evaluation",
                ],
                "projects": [
                    "House Price Prediction",
                    "Customer Churn Prediction",
                ],
            },
            {
                "phase": 3,
                "title": "Deep Learning",
                "duration": "4–6 weeks",
                "skills": [
                    "Deep Learning",
                    "TensorFlow",
                    "PyTorch",
                    "Neural Networks",
                    "CNN",
                    "RNN",
                ],
                "projects": [
                    "Image Classification",
                    "Deep Learning Prediction System",
                ],
            },
            {
                "phase": 4,
                "title": "ML Deployment",
                "duration": "3–4 weeks",
                "skills": [
                    "FastAPI",
                    "Docker",
                    "MLflow",
                    "REST API",
                    "Cloud Deployment",
                ],
                "projects": [
                    "Deploy an ML Model with FastAPI",
                    "Dockerized ML Application",
                ],
            },
            {
                "phase": 5,
                "title": "Interview & Job Preparation",
                "duration": "3–4 weeks",
                "skills": [
                    "DSA",
                    "SQL",
                    "Machine Learning Interview",
                    "System Design",
                    "Resume",
                    "GitHub",
                ],
                "projects": [
                    "Build 2–3 strong portfolio projects",
                    "Practice ML interview questions",
                ],
            },
        ],
    },

    "AI Engineer": {
        "description": (
            "Build skills in machine learning, deep learning, LLMs, "
            "Generative AI, RAG, and AI application deployment."
        ),
        "phases": [
            {
                "phase": 1,
                "title": "Programming & ML Foundations",
                "duration": "4–5 weeks",
                "skills": [
                    "Python",
                    "NumPy",
                    "Pandas",
                    "SQL",
                    "Machine Learning",
                ],
                "projects": [
                    "ML Prediction Project",
                    "Data Analysis Project",
                ],
            },
            {
                "phase": 2,
                "title": "Deep Learning",
                "duration": "4–6 weeks",
                "skills": [
                    "Deep Learning",
                    "Neural Networks",
                    "TensorFlow",
                    "PyTorch",
                    "CNN",
                    "RNN",
                ],
                "projects": [
                    "Image Classification",
                    "Neural Network Application",
                ],
            },
            {
                "phase": 3,
                "title": "Generative AI",
                "duration": "4–6 weeks",
                "skills": [
                    "LLMs",
                    "Generative AI",
                    "Prompt Engineering",
                    "LangChain",
                    "Embeddings",
                    "Vector Databases",
                ],
                "projects": [
                    "LLM Chatbot",
                    "Document Question Answering System",
                ],
            },
            {
                "phase": 4,
                "title": "RAG & AI Applications",
                "duration": "4–5 weeks",
                "skills": [
                    "RAG",
                    "Vector Databases",
                    "FastAPI",
                    "Streamlit",
                    "AI Agents",
                ],
                "projects": [
                    "RAG Career Assistant",
                    "AI Agent Application",
                ],
            },
            {
                "phase": 5,
                "title": "Deployment & Interview",
                "duration": "3–4 weeks",
                "skills": [
                    "Docker",
                    "Cloud Deployment",
                    "Git",
                    "DSA",
                    "System Design",
                ],
                "projects": [
                    "Deploy an AI Application",
                    "Build a production-ready AI project",
                ],
            },
        ],
    },

    "Data Scientist": {
        "description": (
            "Develop skills in statistics, data analysis, machine learning, "
            "visualization, and business-oriented problem solving."
        ),
        "phases": [
            {
                "phase": 1,
                "title": "Data Foundations",
                "duration": "3–4 weeks",
                "skills": [
                    "Python",
                    "NumPy",
                    "Pandas",
                    "SQL",
                    "Statistics",
                ],
                "projects": [
                    "Exploratory Data Analysis",
                    "SQL Data Analysis Project",
                ],
            },
            {
                "phase": 2,
                "title": "Data Visualization",
                "duration": "2–3 weeks",
                "skills": [
                    "Matplotlib",
                    "Seaborn",
                    "Data Visualization",
                    "Power BI",
                ],
                "projects": [
                    "Business Analytics Dashboard",
                ],
            },
            {
                "phase": 3,
                "title": "Machine Learning",
                "duration": "4–6 weeks",
                "skills": [
                    "Machine Learning",
                    "Scikit-learn",
                    "Feature Engineering",
                    "Model Evaluation",
                ],
                "projects": [
                    "Customer Churn Prediction",
                    "Sales Prediction",
                ],
            },
            {
                "phase": 4,
                "title": "Advanced Data Science",
                "duration": "3–4 weeks",
                "skills": [
                    "Feature Selection",
                    "Model Optimization",
                    "Time Series",
                    "Experimentation",
                ],
                "projects": [
                    "Time Series Forecasting",
                ],
            },
            {
                "phase": 5,
                "title": "Interview & Portfolio",
                "duration": "3–4 weeks",
                "skills": [
                    "SQL Interview",
                    "Statistics Interview",
                    "ML Interview",
                    "DSA",
                    "Resume",
                ],
                "projects": [
                    "Build a complete end-to-end Data Science project",
                ],
            },
        ],
    },

    "Backend Developer": {
        "description": (
            "Develop strong backend engineering skills using APIs, "
            "databases, authentication, testing, and deployment."
        ),
        "phases": [
            {
                "phase": 1,
                "title": "Programming Foundations",
                "duration": "3–4 weeks",
                "skills": [
                    "Python",
                    "JavaScript",
                    "TypeScript",
                    "Git",
                    "DSA",
                ],
                "projects": [
                    "REST API Project",
                ],
            },
            {
                "phase": 2,
                "title": "Backend Development",
                "duration": "4–6 weeks",
                "skills": [
                    "Node.js",
                    "Express.js",
                    "FastAPI",
                    "REST API",
                ],
                "projects": [
                    "Backend API",
                    "Authentication API",
                ],
            },
            {
                "phase": 3,
                "title": "Databases",
                "duration": "3–4 weeks",
                "skills": [
                    "SQL",
                    "MongoDB",
                    "Database Design",
                    "Query Optimization",
                ],
                "projects": [
                    "Database-driven Web Application",
                ],
            },
            {
                "phase": 4,
                "title": "Production Backend",
                "duration": "4–5 weeks",
                "skills": [
                    "Docker",
                    "Testing",
                    "Authentication",
                    "Caching",
                    "Cloud Deployment",
                ],
                "projects": [
                    "Production-ready REST API",
                ],
            },
            {
                "phase": 5,
                "title": "Interview Preparation",
                "duration": "3–4 weeks",
                "skills": [
                    "DSA",
                    "SQL",
                    "System Design",
                    "Backend Interview",
                ],
                "projects": [
                    "Build a scalable backend project",
                ],
            },
        ],
    },
}


# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_skill(skill: str) -> str:
    """
    Normalize a skill name for comparison.

    Example:
        "  Python  " -> "python"
        "Machine   Learning" -> "machine learning"
    """

    return " ".join(
        str(skill).lower().strip().split()
    )


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    # --------------------------------------------------------
    # Programming / Data
    # --------------------------------------------------------

    "python": {
        "python",
    },

    "javascript": {
        "javascript",
        "js",
    },

    "typescript": {
        "typescript",
        "ts",
    },

    "numpy": {
        "numpy",
    },

    "pandas": {
        "pandas",
    },

    "sql": {
        "sql",
        "structured query language",
    },

    "git": {
        "git",
    },

    "github": {
        "github",
        "git hub",
    },

    # --------------------------------------------------------
    # Machine Learning
    # --------------------------------------------------------

    "machine learning": {
        "machine learning",
        "ml",
        "machine-learning",
    },

    "scikit-learn": {
        "scikit-learn",
        "scikit learn",
        "sklearn",
        "scikit",
    },

    "statistics": {
        "statistics",
        "statistical analysis",
        "statistical methods",
    },

    "feature engineering": {
        "feature engineering",
        "feature extraction",
        "feature creation",
    },

    "model evaluation": {
        "model evaluation",
        "model validation",
        "model assessment",
    },

    # --------------------------------------------------------
    # Deep Learning
    # --------------------------------------------------------

    "deep learning": {
        "deep learning",
        "dl",
        "deep-learning",
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

    "neural networks": {
        "neural networks",
        "neural network",
        "ann",
        "artificial neural network",
        "artificial neural networks",
    },

    "cnn": {
        "cnn",
        "convolutional neural network",
        "convolutional neural networks",
    },

    "rnn": {
        "rnn",
        "recurrent neural network",
        "recurrent neural networks",
    },

    # --------------------------------------------------------
    # AI / Generative AI
    # --------------------------------------------------------

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

    "prompt engineering": {
        "prompt engineering",
        "prompt design",
    },

    "langchain": {
        "langchain",
    },

    "embeddings": {
        "embedding",
        "embeddings",
        "vector embeddings",
    },

    "vector databases": {
        "vector database",
        "vector databases",
        "vector db",
        "vector dbs",
        "vectordb",
    },

    "rag": {
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "retrieval augmented generative ai",
    },

    "ai agents": {
        "ai agent",
        "ai agents",
        "agentic ai",
        "agentic artificial intelligence",
        "ai agentic systems",
    },

    # --------------------------------------------------------
    # Backend / APIs
    # --------------------------------------------------------

    "fastapi": {
        "fastapi",
        "fast api",
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

    "rest api": {
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "restful services",
    },

    "mongodb": {
        "mongodb",
        "mongo db",
        "mongo",
    },

    # --------------------------------------------------------
    # Deployment
    # --------------------------------------------------------

    "docker": {
        "docker",
        "docker containers",
        "containerization",
    },

    "mlflow": {
        "mlflow",
        "ml flow",
    },

    "cloud deployment": {
        "cloud deployment",
        "cloud deployments",
        "cloud computing",
        "cloud",
    },

    # --------------------------------------------------------
    # Other technical skills
    # --------------------------------------------------------

    "dsa": {
        "dsa",
        "data structures and algorithms",
        "data structures & algorithms",
        "data structures algorithms",
        "data structures",
        "algorithms",
    },

    "system design": {
        "system design",
        "software architecture",
        "system architecture",
    },

    "matplotlib": {
        "matplotlib",
    },

    "seaborn": {
        "seaborn",
    },

    "data visualization": {
        "data visualization",
        "data visualisation",
        "data analysis visualization",
    },

    "power bi": {
        "power bi",
        "powerbi",
    },

    "database design": {
        "database design",
        "database architecture",
    },

    "query optimization": {
        "query optimization",
        "sql optimization",
        "database query optimization",
    },

    "testing": {
        "testing",
        "software testing",
        "unit testing",
        "integration testing",
    },

    "authentication": {
        "authentication",
        "user authentication",
        "api authentication",
    },

    "caching": {
        "caching",
        "cache",
    },

    "resume": {
        "resume",
        "cv",
        "curriculum vitae",
    },
}


# ============================================================
# BUILD REVERSE ALIAS LOOKUP
# ============================================================

def build_skill_alias_lookup() -> Dict[str, str]:
    """
    Build a lookup where every known alias points to the
    canonical roadmap skill.
    """

    lookup: Dict[str, str] = {}

    for canonical_skill, aliases in SKILL_ALIASES.items():

        canonical_normalized = normalize_skill(
            canonical_skill
        )

        lookup[canonical_normalized] = canonical_normalized

        for alias in aliases:

            normalized_alias = normalize_skill(alias)

            lookup[normalized_alias] = canonical_normalized

    return lookup


SKILL_ALIAS_LOOKUP = build_skill_alias_lookup()


# ============================================================
# CANONICAL SKILL
# ============================================================

def get_canonical_skill(skill: str) -> str:
    """
    Convert a skill into its canonical skill name.

    Example:

        ML
        ↓
        machine learning

        sklearn
        ↓
        scikit-learn
    """

    normalized = normalize_skill(skill)

    if not normalized:
        return ""

    return SKILL_ALIAS_LOOKUP.get(
        normalized,
        normalized
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def skills_match(
    roadmap_skill: str,
    user_skill: str
) -> bool:
    """
    Check whether a roadmap skill matches a user's skill.

    Matching uses canonical skill names and aliases.
    """

    roadmap_canonical = get_canonical_skill(
        roadmap_skill
    )

    user_canonical = get_canonical_skill(
        user_skill
    )

    return (
        roadmap_canonical
        and user_canonical
        and roadmap_canonical == user_canonical
    )


# ============================================================
# CHECK USER HAS SKILL
# ============================================================

def user_has_skill(
    roadmap_skill: str,
    user_skills: List[str]
) -> bool:
    """
    Check whether the user has a roadmap skill.
    """

    for user_skill in user_skills or []:

        if skills_match(
            roadmap_skill,
            user_skill
        ):
            return True

    return False


# ============================================================
# GET CAREER ROADMAP
# ============================================================

def get_career_roadmap(
    target_role: str
) -> Dict[str, Any]:
    """
    Return the roadmap for a selected career role.
    """

    if not target_role:
        raise ValueError(
            "Target role is required."
        )

    roadmap = CAREER_ROADMAPS.get(
        target_role
    )

    if roadmap is None:

        raise ValueError(
            f"No roadmap available for '{target_role}'."
        )

    return {
        "target_role": target_role,
        "description": roadmap["description"],
        "phases": roadmap["phases"],
    }


# ============================================================
# PERSONALIZE ROADMAP
# ============================================================

def personalize_roadmap(
    target_role: str,
    user_skills: List[str],
) -> Dict[str, Any]:
    """
    Personalize a roadmap by identifying:

    - Skills the user already has
    - Skills the user still needs to learn
    - Completion percentage for each phase
    - Overall roadmap completion
    """

    roadmap = get_career_roadmap(
        target_role
    )

    user_skills = user_skills or []

    personalized_phases = []

    # --------------------------------------------------------
    # Process every phase
    # --------------------------------------------------------

    for phase in roadmap["phases"]:

        completed_skills = []
        missing_skills = []

        for roadmap_skill in phase["skills"]:

            if user_has_skill(
                roadmap_skill,
                user_skills
            ):

                completed_skills.append(
                    roadmap_skill
                )

            else:

                missing_skills.append(
                    roadmap_skill
                )

        # ----------------------------------------------------
        # Calculate phase completion
        # ----------------------------------------------------

        total_phase_skills = len(
            phase["skills"]
        )

        completed_phase_skills = len(
            completed_skills
        )

        if total_phase_skills:

            completion_percentage = round(
                (
                    completed_phase_skills
                    / total_phase_skills
                ) * 100,
                1
            )

        else:

            completion_percentage = 0.0

        personalized_phases.append(
            {
                **phase,
                "completed_skills": completed_skills,
                "missing_skills": missing_skills,
                "completion_percentage": (
                    completion_percentage
                ),
            }
        )

    # ========================================================
    # OVERALL ROADMAP PROGRESS
    # ========================================================

    total_skills = sum(
        len(phase["skills"])
        for phase in roadmap["phases"]
    )

    completed_total = sum(
        len(phase["completed_skills"])
        for phase in personalized_phases
    )

    if total_skills:

        overall_completion = round(
            (
                completed_total
                / total_skills
            ) * 100,
            1
        )

    else:

        overall_completion = 0.0

    # ========================================================
    # RETURN PERSONALIZED ROADMAP
    # ========================================================

    return {
        "target_role": roadmap["target_role"],
        "description": roadmap["description"],
        "phases": personalized_phases,
        "overall_completion": overall_completion,
    }