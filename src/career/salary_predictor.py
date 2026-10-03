# ============================================================
# CareerIQ
# Salary Prediction Backend
# ============================================================
#
# This module:
# 1. Loads the trained XGBoost salary model
# 2. Calculates student skill match percentage
# 3. Validates whether the student has relevant skills
# 4. Prepares input for the trained model
# 5. Predicts estimated salary in INR
# 6. Returns an estimated salary range
#
# IMPORTANT:
# Salary prediction is NOT performed when the student has
# zero matching skills for the selected role.
#
# ============================================================

from __future__ import annotations

import math
import os
import pickle
import re
from typing import Any, Dict, List


# ============================================================
# PATH CONFIGURATION
# ============================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        "..",
        "..",
    )
)

MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "models",
    "salary_prediction",
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "salary_prediction_model.pkl",
)

MODEL_INFO_PATH = os.path.join(
    MODEL_DIR,
    "model_info.pkl",
)


# ============================================================
# MODEL CACHE
# ============================================================

_MODEL = None
_MODEL_INFO = None


# ============================================================
# MODEL LOADING
# ============================================================

def load_salary_model():
    """
    Load the trained salary prediction model.

    Returns
    -------
    object
        Trained scikit-learn/XGBoost model or pipeline.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist.
    """

    global _MODEL

    if _MODEL is not None:
        return _MODEL

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Salary prediction model not found.\n\n"
            f"Expected location:\n{MODEL_PATH}\n\n"
            "Please make sure the trained model exists."
        )

    with open(
        MODEL_PATH,
        "rb",
    ) as file:

        _MODEL = pickle.load(file)

    return _MODEL


def load_model_info() -> Dict[str, Any]:
    """
    Load saved model information and metrics.

    Returns
    -------
    dict
        Model metadata.
    """

    global _MODEL_INFO

    if _MODEL_INFO is not None:
        return _MODEL_INFO

    if not os.path.exists(
        MODEL_INFO_PATH
    ):
        return {}

    with open(
        MODEL_INFO_PATH,
        "rb",
    ) as file:

        _MODEL_INFO = pickle.load(file)

    return _MODEL_INFO


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(
    value: Any,
) -> str:
    """
    Normalize text for model input and skill comparison.
    """

    if value is None:
        return ""

    text = str(value).lower()

    text = text.replace(
        "&",
        " and ",
    )

    text = re.sub(
        r"[\r\n\t]+",
        " ",
        text,
    )

    text = re.sub(
        r"[^a-z0-9+#.\-/ ]+",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ============================================================
# SKILL CANONICALIZATION
# ============================================================

def canonicalize_skill(
    skill: Any,
) -> str:
    """
    Convert a skill into a consistent comparison format.

    Examples
    --------
    Node.js       -> nodejs
    Node JS       -> nodejs
    Scikit-learn  -> scikit learn
    scikit learn  -> scikit learn
    """

    text = normalize_text(
        skill
    )

    if not text:
        return ""

    # Common equivalent forms.
    aliases = {
        "node.js": "nodejs",
        "node js": "nodejs",
        "node-js": "nodejs",

        "react.js": "react",
        "react js": "react",

        "next.js": "nextjs",
        "next js": "nextjs",

        "vue.js": "vue",
        "vue js": "vue",

        "express": "expressjs",
        "express js": "expressjs",
        "express.js": "expressjs",

        "scikit-learn": "scikit learn",
        "scikit learn": "scikit learn",
        "sklearn": "scikit learn",

        "machine-learning": "machine learning",
        "machinelearning": "machine learning",

        "deep-learning": "deep learning",
        "deeplearning": "deep learning",

        "data-science": "data science",
        "datascience": "data science",

        "data-analysis": "data analysis",
        "dataanalysis": "data analysis",

        "rest-api": "rest api",
        "restapi": "rest api",

        "ui/ux": "ui ux",
        "ui ux design": "ui ux",

        "power-bi": "power bi",
        "powerbi": "power bi",

        "ci/cd": "ci cd",
        "cicd": "ci cd",
    }

    return aliases.get(
        text,
        text,
    )


# ============================================================
# SKILL PARSING
# ============================================================

def parse_skills(
    skills: Any,
) -> List[str]:
    """
    Convert skills into a normalized unique list.

    Supports:
    - list
    - tuple
    - set
    - comma-separated string
    - semicolon-separated string
    - pipe-separated string
    - newline-separated string
    """

    if skills is None:
        return []

    if isinstance(
        skills,
        (list, tuple, set),
    ):

        raw_skills = list(
            skills
        )

    else:

        text = str(skills)

        raw_skills = re.split(
            r"[,;|\n]+",
            text,
        )

    cleaned_skills = []

    for skill in raw_skills:

        skill = canonicalize_skill(
            skill
        )

        if not skill:
            continue

        cleaned_skills.append(
            skill
        )

    # Remove duplicates while preserving order.
    unique_skills = []

    seen = set()

    for skill in cleaned_skills:

        if skill not in seen:

            unique_skills.append(
                skill
            )

            seen.add(
                skill
            )

    return unique_skills


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(
    student_skills: Any,
    required_skills: Any,
) -> Dict[str, Any]:
    """
    Compare student skills against required role skills.

    Returns
    -------
    dict
        Match percentage, matched skills and missing skills.
    """

    student = parse_skills(
        student_skills
    )

    required = parse_skills(
        required_skills
    )

    if not required:

        return {
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "student_skills": student,
            "required_skills": required,
            "matched_count": 0,
            "required_count": 0,
        }

    student_set = set(
        student
    )

    matched = []
    missing = []

    for skill in required:

        if skill in student_set:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    percentage = (
        len(matched)
        /
        len(required)
    ) * 100

    return {
        "match_percentage": round(
            percentage,
            2,
        ),
        "matched_skills": matched,
        "missing_skills": missing,
        "student_skills": student,
        "required_skills": required,
        "matched_count": len(
            matched
        ),
        "required_count": len(
            required
        ),
    }


# ============================================================
# EXPERIENCE NORMALIZATION
# ============================================================

def normalize_experience(
    experience: Any,
) -> float:
    """
    Convert experience input to years.

    Examples
    --------
    2              -> 2.0
    "2 years"      -> 2.0
    "2-4 years"    -> 3.0
    "Fresher"      -> 0.0
    """

    if experience is None:
        return 0.0

    if isinstance(
        experience,
        (int, float),
    ):

        value = float(
            experience
        )

        if not math.isfinite(
            value
        ):
            return 0.0

        return max(
            0.0,
            min(
                value,
                50.0,
            ),
        )

    text = normalize_text(
        experience
    )

    if not text:
        return 0.0

    if (
        "fresher" in text
        or "entry level" in text
        or "no experience" in text
    ):

        return 0.0

    numbers = re.findall(
        r"\d+(?:\.\d+)?",
        text,
    )

    if not numbers:
        return 0.0

    values = [
        float(number)
        for number in numbers
    ]

    if len(values) >= 2:

        value = (
            values[0]
            + values[1]
        ) / 2

    else:

        value = values[0]

    return max(
        0.0,
        min(
            value,
            50.0,
        ),
    )


# ============================================================
# SKILL TEXT CREATION
# ============================================================

def build_skills_text(
    student_skills: Any,
    domain: str = "",
    role: str = "",
) -> str:
    """
    Create the skills_text feature used by the trained model.
    """

    skills = parse_skills(
        student_skills
    )

    skills_text = " ".join(
        skills
    )

    domain_text = normalize_text(
        domain
    )

    role_text = normalize_text(
        role
    )

    return (
        f"{skills_text} "
        f"{domain_text} "
        f"{role_text}"
    ).strip()


# ============================================================
# JOB TEXT CREATION
# ============================================================

def build_job_text(
    role: str,
    student_skills: Any,
    domain: str = "",
    required_skills: Any = None,
    job_description: str = "",
) -> str:
    """
    Create the job_text feature used during training.

    The trained model uses information equivalent to:
        title_clean
        skills_clean
        description_clean

    For student prediction we construct a corresponding
    representation from the selected role, domain and skills.
    """

    role_text = normalize_text(
        role
    )

    domain_text = normalize_text(
        domain
    )

    student_skill_text = " ".join(
        parse_skills(
            student_skills
        )
    )

    required_skill_text = " ".join(
        parse_skills(
            required_skills
        )
    )

    description_text = normalize_text(
        job_description
    )

    return (
        f"{role_text} "
        f"{domain_text} "
        f"{student_skill_text} "
        f"{required_skill_text} "
        f"{description_text}"
    ).strip()


# ============================================================
# SALARY RANGE
# ============================================================

def create_salary_range(
    predicted_salary: float,
) -> Dict[str, float]:
    """
    Create a presentation range around the prediction.

    IMPORTANT:
    This is NOT a statistical confidence interval.
    """

    predicted_salary = max(
        0.0,
        float(
            predicted_salary
        ),
    )

    lower = (
        predicted_salary
        * 0.85
    )

    upper = (
        predicted_salary
        * 1.15
    )

    return {
        "lower": round(
            lower,
            0,
        ),
        "predicted": round(
            predicted_salary,
            0,
        ),
        "upper": round(
            upper,
            0,
        ),
    }


# ============================================================
# SALARY FORMATTING
# ============================================================

def format_inr(
    amount: float,
) -> str:
    """
    Format amount as Indian Rupees.

    Example:
        711170 -> ₹7,11,170
    """

    amount = int(
        round(
            float(amount)
        )
    )

    negative = (
        amount < 0
    )

    amount = abs(
        amount
    )

    text = str(
        amount
    )

    if len(text) <= 3:

        formatted = text

    else:

        last_three = text[-3:]

        remaining = text[:-3]

        groups = []

        while len(
            remaining
        ) > 2:

            groups.insert(
                0,
                remaining[-2:],
            )

            remaining = (
                remaining[:-2]
            )

        if remaining:

            groups.insert(
                0,
                remaining,
            )

        formatted = (
            ",".join(
                groups
            )
            + ","
            + last_three
        )

    if negative:

        return f"-₹{formatted}"

    return f"₹{formatted}"


# ============================================================
# SALARY PREDICTION
# ============================================================

def predict_salary(
    student_skills: Any,
    domain: str,
    role: str,
    experience_years: Any = 0,
    location: str = "",
    required_skills: Any = None,
    job_description: str = "",
) -> Dict[str, Any]:
    """
    Predict salary for a student.

    Prediction uses:
    - Student skills
    - Selected domain
    - Selected role
    - Experience
    - Location
    - Required skills

    IMPORTANT VALIDATION:
    If the student has ZERO matching skills for the selected
    role, salary prediction is stopped.

    This prevents CareerIQ from showing a salary estimate
    for a role that has no skill overlap with the resume.
    """

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    domain = str(
        domain or ""
    ).strip()

    role = str(
        role or ""
    ).strip()

    location = str(
        location or ""
    ).strip()

    if not domain:

        return {
            "success": False,
            "error": "Domain is required.",
        }

    if not role:

        return {
            "success": False,
            "error": "Role is required.",
        }

    # ========================================================
    # NORMALIZE EXPERIENCE
    # ========================================================

    experience = normalize_experience(
        experience_years
    )

    # ========================================================
    # PARSE STUDENT SKILLS
    # ========================================================

    normalized_student_skills = parse_skills(
        student_skills
    )

    # ========================================================
    # CALCULATE SKILL MATCH
    # ========================================================

    skill_match = calculate_skill_match(
        normalized_student_skills,
        required_skills,
    )

    matched_count = skill_match[
        "matched_count"
    ]

    required_count = skill_match[
        "required_count"
    ]

    match_percentage = skill_match[
        "match_percentage"
    ]

    # ========================================================
    # IMPORTANT:
    # ZERO MATCH = NO SALARY PREDICTION
    # ========================================================

    if matched_count == 0:

        return {
            "success": False,

            "error": (
                "Salary prediction is unavailable "
                "because your resume has no matching "
                "skills for the selected role."
            ),

            "reason": "zero_skill_match",

            "domain": domain,

            "role": role,

            "location": location,

            "experience_years": experience,

            "student_skills":
                normalized_student_skills,

            "skill_match": {
                "percentage":
                    match_percentage,

                "matched_skills":
                    skill_match[
                        "matched_skills"
                    ],

                "missing_skills":
                    skill_match[
                        "missing_skills"
                    ],

                "matched_count":
                    matched_count,

                "required_count":
                    required_count,
            },

            "salary_prediction": None,
        }

    # ========================================================
    # LOAD MODEL
    # ========================================================

    try:

        model = load_salary_model()

    except Exception as exc:

        return {
            "success": False,
            "error": str(exc),
        }

    # ========================================================
    # BUILD MODEL FEATURES
    # ========================================================

    skills_text = build_skills_text(
        normalized_student_skills,
        domain,
        role,
    )

    job_text = build_job_text(
        role=role,
        student_skills=normalized_student_skills,
        domain=domain,
        required_skills=required_skills,
        job_description=job_description,
    )

    skill_count = len(
        normalized_student_skills
    )

    # ========================================================
    # CREATE PREDICTION DATAFRAME
    # ========================================================

    try:

        import pandas as pd

        prediction_input = pd.DataFrame(
            [
                {
                    "skills_text":
                        skills_text,

                    "job_text":
                        job_text,

                    "location":
                        location,

                    "experience_years":
                        experience,

                    "skill_count":
                        skill_count,
                }
            ]
        )

    except Exception as exc:

        return {
            "success": False,
            "error":
                f"Failed to prepare prediction input: {exc}",
        }

    # ========================================================
    # MODEL PREDICTION
    # ========================================================

    try:

        predicted_log_salary = model.predict(
            prediction_input
        )[0]

    except Exception as exc:

        return {
            "success": False,
            "error":
                f"Salary model prediction failed: {exc}",
        }

    # ========================================================
    # CONVERT LOG SALARY → INR
    # ========================================================

    try:

        import numpy as np

        predicted_salary = float(
            np.expm1(
                predicted_log_salary
            )
        )

    except Exception as exc:

        return {
            "success": False,
            "error":
                f"Failed to convert salary prediction: {exc}",
        }

    # ========================================================
    # VALIDATE PREDICTION
    # ========================================================

    if not math.isfinite(
        predicted_salary
    ):

        return {
            "success": False,
            "error":
                "The salary model returned an invalid prediction.",
        }

    predicted_salary = max(
        0.0,
        predicted_salary,
    )

    # A valid model prediction should be greater than zero.
    if predicted_salary <= 0:

        return {
            "success": False,
            "error":
                "The salary model returned a zero salary prediction.",
        }

    # ========================================================
    # CREATE SALARY RANGE
    # ========================================================

    salary_range = create_salary_range(
        predicted_salary
    )

    # ========================================================
    # LOAD MODEL INFORMATION
    # ========================================================

    model_info = load_model_info()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "success": True,

        "domain":
            domain,

        "role":
            role,

        "location":
            location,

        "experience_years":
            experience,

        # ----------------------------------------------------
        # SALARY
        # ----------------------------------------------------

        "salary_prediction": {

            "predicted_salary":
                round(
                    predicted_salary,
                    0,
                ),

            "predicted_salary_formatted":
                format_inr(
                    predicted_salary
                ),

            "lower_salary":
                salary_range[
                    "lower"
                ],

            "upper_salary":
                salary_range[
                    "upper"
                ],

            "salary_range_formatted":
                (
                    f"{format_inr(salary_range['lower'])}"
                    f" - "
                    f"{format_inr(salary_range['upper'])}"
                ),
        },

        # ----------------------------------------------------
        # SKILL MATCH
        # ----------------------------------------------------

        "skill_match": {

            "percentage":
                skill_match[
                    "match_percentage"
                ],

            "matched_skills":
                skill_match[
                    "matched_skills"
                ],

            "missing_skills":
                skill_match[
                    "missing_skills"
                ],

            "matched_count":
                skill_match[
                    "matched_count"
                ],

            "required_count":
                skill_match[
                    "required_count"
                ],
        },

        # ----------------------------------------------------
        # STUDENT SKILLS
        # ----------------------------------------------------

        "student_skills":
            normalized_student_skills,

        # ----------------------------------------------------
        # MODEL INFORMATION
        # ----------------------------------------------------

        "model": {

            "name":
                model_info.get(
                    "model",
                    "Improved XGBoost",
                ),

            "r2":
                model_info.get(
                    "r2"
                ),

            "mae":
                model_info.get(
                    "mae"
                ),

            "rmse":
                model_info.get(
                    "rmse"
                ),

            "currency":
                model_info.get(
                    "currency",
                    "INR",
                ),
        },
    }


# ============================================================
# SIMPLE PREDICTION HELPER
# ============================================================

def get_salary_prediction(
    student_skills: Any,
    domain: str,
    role: str,
    experience_years: Any = 0,
    location: str = "",
    required_skills: Any = None,
    job_description: str = "",
) -> Dict[str, Any]:
    """
    Wrapper around predict_salary().
    """

    return predict_salary(
        student_skills=student_skills,
        domain=domain,
        role=role,
        experience_years=experience_years,
        location=location,
        required_skills=required_skills,
        job_description=job_description,
    )


# ============================================================
# MODEL INFORMATION HELPER
# ============================================================

def get_model_metrics() -> Dict[str, Any]:
    """
    Return saved model evaluation metrics.
    """

    info = load_model_info()

    return {
        "model":
            info.get(
                "model",
                "Improved XGBoost",
            ),

        "mae":
            info.get(
                "mae"
            ),

        "rmse":
            info.get(
                "rmse"
            ),

        "r2":
            info.get(
                "r2"
            ),

        "currency":
            info.get(
                "currency",
                "INR",
            ),

        "training_rows":
            info.get(
                "training_rows"
            ),

        "testing_rows":
            info.get(
                "testing_rows"
            ),
    }


# ============================================================
# MODEL STATUS
# ============================================================

def is_model_available() -> bool:
    """
    Check whether the trained salary model exists.
    """

    return os.path.exists(
        MODEL_PATH
    )


# ============================================================
# TEST / DEMO
# ============================================================

if __name__ == "__main__":

    print(
        "========================================"
    )

    print(
        "CareerIQ Salary Predictor"
    )

    print(
        "========================================"
    )

    print(
        "\nModel path:"
    )

    print(
        MODEL_PATH
    )

    print(
        "\nModel available:"
    )

    print(
        is_model_available()
    )

    if is_model_available():

        # ----------------------------------------------------
        # MODEL METRICS
        # ----------------------------------------------------

        print(
            "\nModel metrics:"
        )

        print(
            get_model_metrics()
        )

        # ----------------------------------------------------
        # DEMO 1
        # Valid skill match
        # ----------------------------------------------------

        demo_result = predict_salary(

            student_skills=[
                "Python",
                "Machine Learning",
                "Pandas",
                "NumPy",
                "Scikit-learn",
                "TensorFlow",
            ],

            domain=
                "AI / Machine Learning",

            role=
                "Machine Learning Engineer",

            experience_years=1,

            location="Pune",

            required_skills=[
                "Python",
                "Machine Learning",
                "Pandas",
                "NumPy",
                "Scikit-learn",
                "TensorFlow",
                "SQL",
            ],
        )

        print(
            "\n========================================"
        )

        print(
            "DEMO 1 - VALID SKILL MATCH"
        )

        print(
            "========================================"
        )

        print(
            "Success:",
            demo_result[
                "success"
            ],
        )

        print(
            "Domain:",
            demo_result.get(
                "domain"
            ),
        )

        print(
            "Role:",
            demo_result.get(
                "role"
            ),
        )

        print(
            "Skill Match:",
            demo_result.get(
                "skill_match",
                {}
            ).get(
                "percentage"
            ),
        )

        print(
            "Matched Skills:",
            demo_result.get(
                "skill_match",
                {}
            ).get(
                "matched_skills"
            ),
        )

        print(
            "Missing Skills:",
            demo_result.get(
                "skill_match",
                {}
            ).get(
                "missing_skills"
            ),
        )

        if demo_result.get(
            "success"
        ):

            print(
                "Predicted Salary:",
                demo_result[
                    "salary_prediction"
                ][
                    "predicted_salary_formatted"
                ],
            )

            print(
                "Estimated Range:",
                demo_result[
                    "salary_prediction"
                ][
                    "salary_range_formatted"
                ],
            )

        # ----------------------------------------------------
        # DEMO 2
        # ZERO SKILL MATCH
        # ----------------------------------------------------

        zero_skill_result = predict_salary(

            student_skills=[],

            domain=
                "UI / UX",

            role=
                "UI / UX Designer",

            experience_years=0,

            location="Pune",

            required_skills=[
                "Figma",
                "UI Design",
                "UX Design",
                "Wireframing",
                "Prototyping",
                "User Research",
            ],
        )

        print(
            "\n========================================"
        )

        print(
            "DEMO 2 - ZERO SKILL MATCH"
        )

        print(
            "========================================"
        )

        print(
            "Success:",
            zero_skill_result[
                "success"
            ],
        )

        print(
            "Error:",
            zero_skill_result.get(
                "error"
            ),
        )

        print(
            "Skill Match:",
            zero_skill_result.get(
                "skill_match",
                {}
            ).get(
                "percentage"
            ),
        )

        print(
            "Matched Skills:",
            zero_skill_result.get(
                "skill_match",
                {}
            ).get(
                "matched_skills"
            ),
        )

        print(
            "Missing Skills:",
            zero_skill_result.get(
                "skill_match",
                {}
            ).get(
                "missing_skills"
            ),
        )

    else:

        print(
            "\nSalary model is not available."
        )

        print(
            "Make sure salary_prediction_model.pkl "
            "exists in the models/salary_prediction folder."
        )