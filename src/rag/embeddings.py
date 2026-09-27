from typing import List

from sentence_transformers import (
    SentenceTransformer
)


# ============================================================
# EMBEDDING MODEL
# ============================================================

MODEL_NAME = (
    "all-MiniLM-L6-v2"
)


# ============================================================
# LOAD MODEL
# ============================================================

_model = None


def get_embedding_model():
    """
    Load the embedding model only once.

    The model converts text into numerical vectors.
    """

    global _model

    if _model is None:

        print(
            "Loading embedding model..."
        )

        _model = SentenceTransformer(
            MODEL_NAME
        )

        print(
            "Embedding model loaded."
        )

    return _model


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(
    texts: List[str]
):
    """
    Convert a list of text chunks into embeddings.
    """

    if not texts:

        return []

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


# ============================================================
# CREATE SINGLE EMBEDDING
# ============================================================

def create_embedding(
    text: str
):
    """
    Convert one text into an embedding.
    """

    if not text or not text.strip():

        raise ValueError(
            "Text cannot be empty."
        )

    model = get_embedding_model()

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    text = (
        "Machine learning engineers "
        "build and deploy machine learning models."
    )

    embedding = create_embedding(
        text
    )

    print(
        "Embedding dimension:",
        len(embedding)
    )