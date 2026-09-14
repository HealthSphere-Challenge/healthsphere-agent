import argparse
import hashlib
from datetime import UTC, datetime
from pathlib import Path

from app.rag.index import EMBEDDING_DIMENSION, EMBEDDING_MODEL, INDEX_VERSION, SparseVectorIndex
from app.rag.ingestion import CHUNKING_VERSION, PARSER_VERSION, chunk_document, ingest_medquad


def raw_fingerprint(root: Path) -> str:
    manifest = "".join(
        f"{path.relative_to(root).as_posix()}\t{hashlib.sha256(path.read_bytes()).hexdigest()}\n"
        for path in sorted(root.rglob("*.xml"))
    )
    return hashlib.sha256(manifest.encode()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, default=Path("data/medquad/raw"))
    parser.add_argument(
        "--output", type=Path, default=Path("artifacts/medquad-index-v1/index.json")
    )
    args = parser.parse_args()
    documents, counts = ingest_medquad(args.raw)
    chunks = [chunk for document in documents for chunk in chunk_document(document)]
    metadata = {
        "index_version": INDEX_VERSION,
        "corpus_version": "medquad-clean-v1",
        "parser_version": PARSER_VERSION,
        "chunking_version": CHUNKING_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dimension": EMBEDDING_DIMENSION,
        "chunk_count": len(chunks),
        "source_document_count": len(documents),
        "generated_at": datetime.now(UTC).isoformat(),
        "raw_fingerprint": raw_fingerprint(args.raw),
        "counts": counts,
    }
    SparseVectorIndex(chunks, metadata).save(args.output)
    print(f"Built {len(chunks)} chunks from {len(documents)} documents at {args.output}")


if __name__ == "__main__":
    main()
