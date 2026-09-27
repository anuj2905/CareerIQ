from pathlib import Path

import chromadb

from .document_loader import load_and_split_documents
from .embeddings import create_embeddings


# ============================================================
# CONFIGURATION
# ============================================================

KNOWLEDGE_BASE_PATH = Path(
    "data/career_knowledge"
)

VECTOR_DB_PATH = Path(
    "data/chroma_db"
)

COLLECTION_NAME = (
    "career_knowledge"
)


# ============================================================
# CHROMADB CLIENT
# ============================================================

def get_chroma_client():
    """
    Create or load the persistent ChromaDB client.

    The database will be stored locally inside:
    data/chroma_db/
    """

    VECTOR_DB_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_PATH)
    )

    return client


# ============================================================
# GET COLLECTION
# ============================================================

def get_collection():
    """
    Get the CareerIQ career knowledge collection.

    If the collection does not exist,
    ChromaDB will create it.
    """

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


# ============================================================
# ADD DOCUMENTS
# ============================================================

def add_documents(
    documents
):
    """
    Add document chunks and their embeddings
    into ChromaDB.
    """

    if not documents:

        print(
            "No documents found."
        )

        return

    collection = get_collection()

    texts = [
        document["text"]
        for document in documents
    ]

    print(
        f"Creating embeddings for "
        f"{len(texts)} document chunks..."
    )

    embeddings = create_embeddings(
        texts
    )

    ids = [
        f"{document['source']}_{document['chunk_id']}"
        for document in documents
    ]

    metadatas = [
        {
            "source": document["source"],
            "chunk_id": document["chunk_id"]
        }
        for document in documents
    ]

    print(
        "Adding documents to ChromaDB..."
    )

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(
        f"Added {len(texts)} document chunks "
        f"to ChromaDB."
    )


# ============================================================
# SEARCH DOCUMENTS
# ============================================================

def search_documents(
    query: str,
    n_results: int = 5
):
    """
    Search the vector database using
    semantic similarity.
    """

    if not query or not query.strip():

        raise ValueError(
            "Query cannot be empty."
        )

    collection = get_collection()

    query_embedding = create_embeddings(
        [query]
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results


# ============================================================
# BUILD VECTOR DATABASE
# ============================================================

def build_vector_database():
    """
    Load career knowledge documents,
    split them into chunks,
    create embeddings,
    and store them in ChromaDB.
    """

    print()
    print(
        "=========================================="
    )
    print(
        "      CareerIQ Vector Database Builder"
    )
    print(
        "=========================================="
    )

    print()
    print(
        "Knowledge base:",
        KNOWLEDGE_BASE_PATH
    )

    print(
        "Vector database:",
        VECTOR_DB_PATH
    )

    # --------------------------------------------------------
    # Check knowledge base
    # --------------------------------------------------------

    if not KNOWLEDGE_BASE_PATH.exists():

        raise FileNotFoundError(
            f"Knowledge base not found: "
            f"{KNOWLEDGE_BASE_PATH}"
        )

    # --------------------------------------------------------
    # Load and split documents
    # --------------------------------------------------------

    print()
    print(
        "Loading knowledge documents..."
    )

    documents = load_and_split_documents(
        KNOWLEDGE_BASE_PATH
    )

    print(
        f"Loaded {len(documents)} document chunks."
    )

    if not documents:

        raise ValueError(
            "No documents were found in "
            "the knowledge base."
        )

    # --------------------------------------------------------
    # Add documents to ChromaDB
    # --------------------------------------------------------

    print()

    add_documents(
        documents
    )

    # --------------------------------------------------------
    # Verify database
    # --------------------------------------------------------

    collection = get_collection()

    document_count = collection.count()

    print()
    print(
        "=========================================="
    )
    print(
        "Vector database built successfully."
    )
    print(
        f"Total stored chunks: {document_count}"
    )
    print(
        f"Database location: {VECTOR_DB_PATH}"
    )
    print(
        "=========================================="
    )
    print()


# ============================================================
# TEST SEARCH
# ============================================================

def test_search():
    """
    Test whether semantic search is working.
    """

    print()
    print(
        "Testing vector search..."
    )

    query = (
        "What skills are required "
        "to become a machine learning engineer?"
    )

    results = search_documents(
        query,
        n_results=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    print()
    print(
        "Search query:",
        query
    )

    print()
    print(
        "Top results:"
    )

    for index, document in enumerate(
        documents,
        start=1
    ):

        print()
        print(
            f"--- Result {index} ---"
        )

        print(
            document[:500]
        )

        if index <= len(metadatas):

            print(
                "Source:",
                metadatas[index - 1].get(
                    "source",
                    "Unknown"
                )
            )

    print()
    print(
        "Vector search test completed."
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    build_vector_database()

    test_search()