from pathlib import Path

import pytest

from app.rag import MedicalRetriever, SparseVectorIndex


def test_known_query_retrieves_expected_source_with_metadata(index):
    results = MedicalRetriever(index, top_k=1, minimum_score=0.01).retrieve(
        "What is hypertension blood pressure?"
    )
    assert len(results) == 1 and results[0].chunk.document_id == "medquad:hypertension"
    assert results[0].chunk.source == "NHLBI" and results[0].chunk.source_url


def test_top_k_is_bounded_and_unsupported_query_has_no_evidence(index):
    retriever = MedicalRetriever(index, top_k=1, minimum_score=0.1)
    assert len(retriever.retrieve("sleep routines")) <= 1
    assert retriever.retrieve("quantum spaceship taxation") == []
    with pytest.raises(ValueError):
        MedicalRetriever(index, top_k=9)


def test_index_round_trip_and_incompatible_metadata(index, tmp_path: Path):
    path = tmp_path / "index.json"
    index.save(path)
    loaded = SparseVectorIndex.load(path)
    assert loaded.metadata == index.metadata and loaded.chunks == index.chunks
    path.write_text(
        path.read_text().replace('"embedding_dimension":16384', '"embedding_dimension":12')
    )
    with pytest.raises(ValueError, match="incompatible"):
        SparseVectorIndex.load(path)
