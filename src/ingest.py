# """
# Used for adding NEW documents to the existing Faiss vector store.

# Supported file types:
# - PDF
# - TXT
# - CSV
# - Excel (.xlsx)
# - Word (.docx)
# - JSON

# Workflow:
# 1. Read indexed_files.json
# 2. Find newly added files in the data directory
# 3. Load only new files
# 4. Chunk them
# 5. Generate embeddings
# 6. Append to existing Faiss index
# 7. Update indexed_files.json
# """

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_single_file
from src.embedding import EmbeddingPipeline
from src.vectorstore import FaissVectorStore

INDEX_FILE = PROJECT_ROOT / "faiss_store" / "indexed_files.json"
DATA_FOLDER = PROJECT_ROOT / "data"

SUPPORTED_EXTENSIONS = [
    "*.pdf",
    "*.txt",
    "*.csv",
    "*.xlsx",
    "*.docx",
    "*.json",
]


def load_indexed_files():
    """Load already indexed files."""

    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r") as f:
            return json.load(f)
        return [Path(path).as_posix() for path in indexed]

    return []


def save_indexed_files(indexed):
    """Save indexed file list."""

    with open(INDEX_FILE, "w") as f:
        json.dump(indexed, f, indent=4)


def ingest():

    indexed = load_indexed_files()

    # -------------------------------------------------------
    # Find all supported files
    # -------------------------------------------------------

    all_files = []

    for ext in SUPPORTED_EXTENSIONS:
        all_files.extend(DATA_FOLDER.rglob(ext))

    # -------------------------------------------------------
    # Find only NEW files
    # -------------------------------------------------------

    new_files = [
        file
        for file in all_files
        if file.relative_to(DATA_FOLDER).as_posix() not in indexed
    ]

    if not new_files:
        print("\n[INFO] No new documents found.")
        return

    print("\n[INFO] New documents detected:\n")

    for file in new_files:
        print(f"   {file.relative_to(DATA_FOLDER)}")

    # -------------------------------------------------------
    # Load existing vector store
    # -------------------------------------------------------

    store = FaissVectorStore("faiss_store")
    store.load()

    emb_pipe = EmbeddingPipeline()

    # -------------------------------------------------------
    # Process every new file
    # -------------------------------------------------------

    for file in new_files:

        print(f"\n{'='*60}")
        print(f"[INFO] Processing: {file.name}")
        print("=" * 60)

        docs = load_single_file(file)

        if not docs:
            print(f"[WARNING] Skipping {file.name}")
            continue

        chunks = emb_pipe.chunk_documents(docs)

        embeddings = emb_pipe.embed_chunks(chunks)

        metadata = [
            {
                "text": chunk.page_content,
                "source": chunk.metadata.get("source"),
                "page": chunk.metadata.get("page"),
            }
            for chunk in chunks
        ]

        store.add_embeddings(
            embeddings.astype("float32"),
            metadata,
        )

        indexed.append(
            file.relative_to(DATA_FOLDER).as_posix()
        )

    # -------------------------------------------------------
    # Save updated vector store
    # -------------------------------------------------------

    store.save()

    save_indexed_files(indexed)

    print("\n" + "=" * 60)
    print("[INFO] Ingestion Complete!")
    print(f"[INFO] Total vectors in Faiss : {store.index.ntotal}")
    print(f"[INFO] Indexed files          : {len(indexed)}")
    print("=" * 60)


if __name__ == "__main__":
    ingest()