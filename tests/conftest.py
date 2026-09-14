from pathlib import Path

import pytest

from app.agent import AgentService
from app.rag import MedicalRetriever, SparseVectorIndex
from app.rag.index import EMBEDDING_DIMENSION, EMBEDDING_MODEL, INDEX_VERSION
from app.rag.ingestion import MedicalDocument, chunk_document


class FakeLLM:
    provider_name = "fake"
    model_name = "deterministic-v1"

    def __init__(
        self,
        answer: str = "Hypertension means blood pressure remains higher than recommended over time.",
        fail: bool = False,
    ):
        self.answer, self.fail, self.calls = answer, fail, []

    async def generate(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        if self.fail:
            raise RuntimeError("secret provider failure")
        return self.answer


@pytest.fixture
def chunks():
    documents = [
        MedicalDocument(
            "medquad:hypertension",
            "What is hypertension?",
            "Hypertension is persistently elevated blood pressure. A healthcare professional confirms it using appropriate measurements.",
            "Hypertension",
            "information",
            "NHLBI",
            "https://example.test/hypertension",
            "fixture/1.xml",
        ),
        MedicalDocument(
            "medquad:sleep",
            "What affects sleep?",
            "Sleep duration can be affected by routines, environment, health conditions, and medicines.",
            "Sleep information",
            "information",
            "MedlinePlus",
            "https://example.test/sleep",
            "fixture/2.xml",
        ),
    ]
    return [chunk for document in documents for chunk in chunk_document(document)]


@pytest.fixture
def index(chunks):
    return SparseVectorIndex(
        chunks,
        {
            "index_version": INDEX_VERSION,
            "corpus_version": "fixture-v1",
            "embedding_model": EMBEDDING_MODEL,
            "embedding_dimension": EMBEDDING_DIMENSION,
            "chunk_count": len(chunks),
            "source_document_count": 2,
        },
    )


@pytest.fixture
def service(index):
    return AgentService(
        MedicalRetriever(index, minimum_score=0.1),
        FakeLLM(),
        "fixture-v1",
        Path("app/prompts/system-v1.txt"),
    )
