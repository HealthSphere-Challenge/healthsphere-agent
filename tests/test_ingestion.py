from pathlib import Path

from app.rag.ingestion import (
    MedicalDocument,
    chunk_document,
    ingest_medquad,
    parse_medquad_file,
    safe_source_url,
)

XML = """<Document id="1" source="NHLBI" url="https://example.test"><Focus>Blood pressure</Focus><QAPairs><QAPair><Question qid="q1" qtype="information"> What is blood pressure? </Question><Answer> Pressure in the arteries. </Answer></QAPair><QAPair><Question qid="q2">Empty?</Question><Answer> </Answer></QAPair></QAPairs></Document>"""


def test_parser_preserves_sources_excludes_empty_and_is_stable(tmp_path: Path):
    raw = tmp_path / "raw"
    raw.mkdir()
    path = raw / "one.xml"
    path.write_text(XML)
    first, counts = parse_medquad_file(path, raw)
    second, _ = parse_medquad_file(path, raw)
    assert first == second and len(first) == 1
    assert first[0].source == "NHLBI" and first[0].source_url == "https://example.test"
    assert counts["empty_answer"] == 1


def test_ingestion_handles_malformed_and_duplicate_files(tmp_path: Path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "valid.xml").write_text(XML)
    (raw / "bad.xml").write_text("<broken")
    documents, counts = ingest_medquad(raw)
    assert len(documents) == 1 and counts["malformed"] == 1 and counts["empty_answer"] == 1


def test_chunking_is_deterministic_and_bounded():
    document = MedicalDocument(
        "medquad:x", "Question", "word " * 600, "Title", "topic", "source", None, "x.xml"
    )
    first = chunk_document(document, 300, 40)
    second = chunk_document(document, 300, 40)
    assert first == second and len(first) > 1
    assert all(
        len(chunk.text) <= 300 and chunk.document_id == document.document_id for chunk in first
    )
    assert len({chunk.chunk_id for chunk in first}) == len(first)


def test_only_http_source_urls_are_retained():
    assert safe_source_url("https://example.test/health") == "https://example.test/health"
    assert safe_source_url("file:///private/source") is None
    assert safe_source_url("not a url") is None
