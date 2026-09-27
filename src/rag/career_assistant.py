from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv

from .retriever import retrieve_context


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# OPENAI CLIENT
# ============================================================

client = OpenAI()


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gpt-5.6"


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are CareerIQ, an AI-powered career assistant.

Your job is to help students with career planning,
skills, learning paths, projects, job preparation,
and career-related questions.

Use the provided career knowledge as your primary
source of factual information.

You also receive the student's resume profile.
Use it to personalize your answer.

Important rules:

1. Give practical and clear answers.
2. Personalize recommendations according to the
   student's current skills, education, projects,
   and experience when that information is available.
3. Do not invent information about the student's
   background.
4. If the retrieved knowledge does not contain enough
   information to answer a factual question, clearly
   say that the available knowledge base does not
   contain enough information.
5. Separate the student's current skills from skills
   they still need to learn.
6. When suggesting a learning path, keep it realistic
   and structured.
7. Prefer concise explanations with useful bullet points.
8. Do not mention internal RAG, embeddings, ChromaDB,
   vector databases, prompts, or implementation details
   unless the user specifically asks about them.
"""


# ============================================================
# RESUME PROFILE FORMATTER
# ============================================================

def format_resume_profile(
    profile: Optional[object]
) -> str:
    """
    Convert the student's ResumeProfile into
    readable text for the LLM.
    """

    if profile is None:
        return (
            "No student resume profile is currently available."
        )

    name = getattr(
        profile,
        "name",
        ""
    )

    education = getattr(
        profile,
        "education",
        []
    )

    skills = getattr(
        profile,
        "skills",
        []
    )

    projects = getattr(
        profile,
        "projects",
        []
    )

    experience = getattr(
        profile,
        "experience",
        []
    )

    certifications = getattr(
        profile,
        "certifications",
        []
    )

    return f"""
Student Name:
{name}

Education:
{format_list(education)}

Skills:
{format_list(skills)}

Projects:
{format_list(projects)}

Experience:
{format_list(experience)}

Certifications:
{format_list(certifications)}
""".strip()


# ============================================================
# LIST FORMATTER
# ============================================================

def format_list(
    items
) -> str:
    """
    Convert a list into readable bullet points.
    """

    if not items:
        return "Not available"

    if isinstance(items, str):
        return f"- {items}"

    return "\n".join(
        f"- {str(item).strip()}"
        for item in items
        if str(item).strip()
    )


# ============================================================
# BUILD USER PROMPT
# ============================================================

def build_user_prompt(
    question: str,
    context: str,
    profile: Optional[object] = None
) -> str:
    """
    Build the final prompt containing:

    - Student question
    - Resume profile
    - Retrieved career knowledge
    """

    resume_information = format_resume_profile(
        profile
    )

    return f"""
STUDENT RESUME PROFILE
======================

{resume_information}


RETRIEVED CAREER KNOWLEDGE
==========================

{context}


STUDENT QUESTION
================

{question}


INSTRUCTIONS
============

Answer the student's question using the retrieved
career knowledge and the student's resume profile.

Personalize the answer where possible.

If the student asks what they should learn next,
identify relevant skills based on their current
profile and the retrieved knowledge.

Do not claim that the student has a skill unless
that skill appears in the resume profile.

Give a clear, practical answer.
""".strip()


# ============================================================
# GENERATE CAREER ANSWER
# ============================================================

def generate_career_answer(
    question: str,
    profile: Optional[object] = None,
    n_results: int = 5
) -> str:
    """
    Generate a personalized career answer using:

    1. ChromaDB retrieval
    2. Student resume profile
    3. GPT-5.6
    """

    if not question or not question.strip():
        raise ValueError(
            "Question cannot be empty."
        )

    question = question.strip()

    # --------------------------------------------------------
    # Retrieve relevant knowledge
    # --------------------------------------------------------

    context = retrieve_context(
        question,
        n_results=n_results
    )

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    user_prompt = build_user_prompt(
        question=question,
        context=context,
        profile=profile
    )

    # --------------------------------------------------------
    # Call GPT-5.6
    # --------------------------------------------------------

    response = client.responses.create(
        model=MODEL_NAME,
        instructions=SYSTEM_PROMPT,
        input=user_prompt
    )

    # --------------------------------------------------------
    # Extract answer
    # --------------------------------------------------------

    answer = response.output_text

    if not answer or not answer.strip():
        raise ValueError(
            "The AI returned an empty response."
        )

    return answer.strip()


# ============================================================
# SIMPLE QUESTION FUNCTION
# ============================================================

def ask_career_assistant(
    question: str,
    profile: Optional[object] = None
) -> str:
    """
    Simple public function for the Streamlit UI.

    Example:

        answer = ask_career_assistant(
            "What should I learn to become an ML Engineer?",
            profile
        )
    """

    return generate_career_answer(
        question=question,
        profile=profile
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "=========================================="
    )
    print(
        "       CareerIQ AI Career Assistant"
    )
    print(
        "=========================================="
    )

    question = (
        "What skills are required "
        "to become a Machine Learning Engineer?"
    )

    print()
    print(
        "Question:",
        question
    )

    print()
    print(
        "Generating answer..."
    )

    answer = ask_career_assistant(
        question
    )

    print()
    print(
        "=========================================="
    )
    print(
        "AI Career Assistant Answer"
    )
    print(
        "=========================================="
    )

    print()
    print(answer)

    print()
    print(
        "=========================================="
    )