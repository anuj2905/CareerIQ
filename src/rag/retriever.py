from typing import List, Dict

from .vector_store import (
    search_documents
)


# ============================================================
# RETRIEVE RELEVANT DOCUMENTS
# ============================================================

def retrieve_documents(
    query: str,
    n_results: int = 5
) -> List[Dict]:
    """
    Retrieve the most relevant knowledge chunks
    for a user query.
    """

    results = search_documents(
        query=query,
        n_results=n_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    retrieved_documents = []

    for index, document in enumerate(
        documents
    ):

        metadata = {}

        if index < len(metadatas):

            metadata = (
                metadatas[index]
            )

        distance = None

        if index < len(distances):

            distance = distances[
                index
            ]

        retrieved_documents.append(
            {
                "text": document,

                "source":
                    metadata.get(
                        "source",
                        "unknown"
                    ),

                "chunk_id":
                    metadata.get(
                        "chunk_id"
                    ),

                "distance":
                    distance
            }
        )

    return retrieved_documents


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(
    documents: List[Dict]
) -> str:
    """
    Combine retrieved documents into
    one context string for the LLM.
    """

    if not documents:

        return ""

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}
Source: {document["source"]}

{document["text"]}
"""
        )

    return "\n".join(
        context_parts
    ).strip()


# ============================================================
# RETRIEVE CONTEXT
# ============================================================

def retrieve_context(
    query: str,
    n_results: int = 5
) -> str:
    """
    Retrieve relevant documents and
    return them as LLM-ready context.
    """

    documents = retrieve_documents(
        query=query,
        n_results=n_results
    )

    return build_context(
        documents
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    query = (
        "What skills should I learn "
        "to become a Machine Learning Engineer?"
    )

    documents = retrieve_documents(
        query,
        n_results=3
    )

    print(
        "\n========== RETRIEVED DOCUMENTS =========="
    )

    for document in documents:

        print(
            "\nSource:",
            document["source"]
        )

        print(
            "Distance:",
            document["distance"]
        )

        print(
            "Text:",
            document["text"]
        )

    print(
        "\n=========================================="
    )