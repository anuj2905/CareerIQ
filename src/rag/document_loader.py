from pathlib import Path
from typing import List, Dict


# ============================================================
# LOAD TEXT DOCUMENTS
# ============================================================

def load_documents(
    knowledge_base_path: str
) -> List[Dict[str, str]]:
    """
    Load all .txt documents from the knowledge base.

    Each document contains:
        - text
        - source
    """

    knowledge_base = Path(
        knowledge_base_path
    )

    if not knowledge_base.exists():

        raise FileNotFoundError(
            f"Knowledge base not found: "
            f"{knowledge_base}"
        )

    documents = []

    # --------------------------------------------------------
    # Find all TXT files
    # --------------------------------------------------------

    txt_files = knowledge_base.rglob(
        "*.txt"
    )

    for file_path in txt_files:

        try:

            text = file_path.read_text(
                encoding="utf-8"
            ).strip()

            if not text:
                continue

            documents.append(
                {
                    "text": text,
                    "source": str(file_path)
                }
            )

        except Exception as e:

            print(
                f"Could not read "
                f"{file_path}: {e}"
            )

    return documents


# ============================================================
# SPLIT DOCUMENT INTO CHUNKS
# ============================================================

def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[str]:
    """
    Split a document into overlapping chunks.

    Example:

        Document
            ↓
        Chunk 1
        Chunk 2
        Chunk 3
    """

    if not text or not text.strip():

        return []

    text = text.strip()

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        if end >= text_length:

            break

        start = (
            end
            - chunk_overlap
        )

    return chunks


# ============================================================
# LOAD AND CHUNK DOCUMENTS
# ============================================================

def load_and_split_documents(
    knowledge_base_path: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[Dict[str, str]]:
    """
    Load all documents and split them into chunks.

    Returns:

        [
            {
                "text": "...",
                "source": "...",
                "chunk_id": 0
            }
        ]
    """

    documents = load_documents(
        knowledge_base_path
    )

    chunks = []

    for document in documents:

        document_chunks = split_text(
            document["text"],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        for chunk_id, chunk in enumerate(
            document_chunks
        ):

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "chunk_id": chunk_id
                }
            )

    return chunks


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    documents = load_and_split_documents(
        "data/career_knowledge"
    )

    print(
        f"Loaded {len(documents)} chunks."
    )

    for document in documents[:5]:

        print(
            "\nSource:",
            document["source"]
        )

        print(
            "Chunk:",
            document["chunk_id"]
        )

        print(
            "Text:",
            document["text"][:200]
        )