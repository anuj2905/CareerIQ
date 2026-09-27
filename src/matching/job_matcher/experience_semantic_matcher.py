from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. Load embedding model
# ==========================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# 2. Clean dataset text
# ==========================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    # Replace formatting characters
    text = text.replace("\n", " ")
    text = text.replace(",", " ")

    return text.strip()


# ==========================================
# 3. Calculate semantic similarity
# ==========================================

def calculate_semantic_similarity(
    resume_text,
    job_text
):

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    if not resume_text or not job_text:
        return 0.0

    # Create embeddings
    embeddings = model.encode(
        [resume_text, job_text]
    )

    # Calculate cosine similarity
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)


# ==========================================
# 4. Position similarity
# ==========================================

def calculate_position_similarity(
    resume_position,
    job_position
):

    return calculate_semantic_similarity(
        resume_position,
        job_position
    )


# ==========================================
# 5. Responsibility similarity
# ==========================================

def calculate_responsibility_similarity(
    resume_responsibilities,
    job_responsibilities
):

    return calculate_semantic_similarity(
        resume_responsibilities,
        job_responsibilities
    )


# ==========================================
# 6. Final experience relevance
# ==========================================

def calculate_experience_relevance(
    resume_position,
    resume_responsibilities,
    job_position,
    job_responsibilities
):

    position_similarity = (
        calculate_position_similarity(
            resume_position,
            job_position
        )
    )

    responsibility_similarity = (
        calculate_responsibility_similarity(
            resume_responsibilities,
            job_responsibilities
        )
    )

    # Final weighted score
    experience_relevance = (
        position_similarity * 0.4
        + responsibility_similarity * 0.6
    )

    return {
        "position_similarity": round(
            position_similarity,
            4
        ),

        "responsibility_similarity": round(
            responsibility_similarity,
            4
        ),

        "experience_relevance": round(
            experience_relevance,
            4
        )
    }


# ==========================================
# 7. Test
# ==========================================

if __name__ == "__main__":

    resume_position = (
        "Software Developer "
        "(Machine Learning Engineer)"
    )

    resume_responsibilities = """
    Machine Learning Design
    Data Analysis
    Model Training
    AI Integration
    Model Deployment
    """

    job_position = (
        "Machine Learning (ML) Engineer"
    )

    job_responsibilities = """
    Machine Learning Leadership
    ML System Design
    Algorithm Research
    Model Training
    AI Integration
    Model Deployment
    """

    result = calculate_experience_relevance(
        resume_position,
        resume_responsibilities,
        job_position,
        job_responsibilities
    )

    print("\nPosition Similarity:")
    print(result["position_similarity"])

    print("\nResponsibility Similarity:")
    print(result["responsibility_similarity"])

    print("\nFinal Experience Relevance:")
    print(result["experience_relevance"])

    print("\nExperience Relevance %:")
    print(
        result["experience_relevance"] * 100
    )