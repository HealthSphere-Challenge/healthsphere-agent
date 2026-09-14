import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from .ingestion import MedicalChunk

TOKEN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "do",
    "does",
    "for",
    "how",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "which",
    "with",
}
EMBEDDING_MODEL = "healthsphere-hashing-tf-v1"
EMBEDDING_DIMENSION = 16384
INDEX_VERSION = "medquad-sparse-cosine-v1"
RETRIEVAL_VERSION = "hashing-cosine-top4-min0.20-v1"


def embed(text: str) -> dict[int, float]:
    tokens = (token for token in TOKEN.findall(text.lower()) if token not in STOP_WORDS)
    counts = Counter(
        int.from_bytes(hashlib.sha256(token.encode()).digest()[:4]) % EMBEDDING_DIMENSION
        for token in tokens
    )
    norm = math.sqrt(sum(value * value for value in counts.values())) or 1
    return {key: value / norm for key, value in counts.items()}


def similarity(left: dict[int, float], right: dict[int, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(key, 0) for key, value in left.items())


@dataclass(frozen=True)
class RetrievalResult:
    chunk: MedicalChunk
    score: float


class SparseVectorIndex:
    def __init__(self, chunks: list[MedicalChunk], metadata: dict[str, object]):
        self.chunks = chunks
        self.metadata = metadata
        self.vectors = [embed(chunk.text) for chunk in chunks]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"metadata": self.metadata, "chunks": [chunk.to_dict() for chunk in self.chunks]}
        path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))

    @classmethod
    def load(cls, path: Path) -> "SparseVectorIndex":
        payload = json.loads(path.read_text())
        metadata = payload["metadata"]
        if (
            metadata.get("index_version") != INDEX_VERSION
            or metadata.get("embedding_model") != EMBEDDING_MODEL
            or metadata.get("embedding_dimension") != EMBEDDING_DIMENSION
        ):
            raise ValueError("incompatible index metadata")
        return cls([MedicalChunk(**item) for item in payload["chunks"]], metadata)


class MedicalRetriever:
    def __init__(self, index: SparseVectorIndex, top_k: int = 4, minimum_score: float = 0.20):
        if not 1 <= top_k <= 8:
            raise ValueError("top_k must be between 1 and 8")
        self.index, self.top_k, self.minimum_score = index, top_k, minimum_score

    def retrieve(self, query: str) -> list[RetrievalResult]:
        query_vector = embed(query)
        ranked = sorted(
            (
                RetrievalResult(chunk, similarity(query_vector, vector))
                for chunk, vector in zip(self.index.chunks, self.index.vectors, strict=True)
            ),
            key=lambda item: (-item.score, item.chunk.chunk_id),
        )
        return [result for result in ranked[: self.top_k] if result.score >= self.minimum_score]
