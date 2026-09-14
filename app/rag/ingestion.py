import hashlib
import re
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlparse

WHITESPACE = re.compile(r"\s+")
PARSER_VERSION = "medquad-parser-v1"
CHUNKING_VERSION = "qa-char-1200-overlap-150-v1"


@dataclass(frozen=True)
class MedicalDocument:
    document_id: str
    question: str
    answer: str
    title: str
    topic: str | None
    source: str
    source_url: str | None
    source_path: str


@dataclass(frozen=True)
class MedicalChunk:
    chunk_id: str
    document_id: str
    text: str
    title: str
    topic: str | None
    source: str
    source_url: str | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def clean_text(value: str | None) -> str:
    return WHITESPACE.sub(" ", value or "").strip()


def safe_source_url(value: str | None) -> str | None:
    cleaned = clean_text(value)
    parsed = urlparse(cleaned)
    return cleaned if parsed.scheme in {"http", "https"} and parsed.netloc else None


def parse_medquad_file(path: Path, raw_root: Path) -> tuple[list[MedicalDocument], dict[str, int]]:
    root = ET.parse(path).getroot()  # noqa: S314 - stdlib parser does not resolve external entities
    relative = path.relative_to(raw_root).as_posix()
    source = clean_text(root.attrib.get("source")) or relative.split("/", 1)[0]
    url = safe_source_url(root.attrib.get("url"))
    focus = clean_text(root.findtext("Focus"))
    documents: list[MedicalDocument] = []
    counts = {"empty_question": 0, "empty_answer": 0, "duplicate": 0}
    seen: set[str] = set()
    for position, pair in enumerate(root.findall(".//QAPair")):
        question_node, answer_node = pair.find("Question"), pair.find("Answer")
        question = clean_text(
            "".join(question_node.itertext()) if question_node is not None else ""
        )
        answer = clean_text("".join(answer_node.itertext()) if answer_node is not None else "")
        if not question:
            counts["empty_question"] += 1
            continue
        if not answer:
            counts["empty_answer"] += 1
            continue
        qid = clean_text(question_node.attrib.get("qid")) if question_node is not None else ""
        identity = f"{relative}\n{qid or position}\n{question}"
        document_id = "medquad:" + hashlib.sha256(identity.encode()).hexdigest()[:24]
        if document_id in seen:
            counts["duplicate"] += 1
            continue
        seen.add(document_id)
        documents.append(
            MedicalDocument(
                document_id,
                question,
                answer,
                focus or question,
                clean_text(question_node.attrib.get("qtype")) or None,
                source,
                url,
                relative,
            )
        )
    return documents, counts


def ingest_medquad(raw_root: Path) -> tuple[list[MedicalDocument], dict[str, int]]:
    documents: list[MedicalDocument] = []
    totals = {
        "xml_files": 0,
        "included": 0,
        "empty_question": 0,
        "empty_answer": 0,
        "duplicate": 0,
        "malformed": 0,
    }
    seen: set[str] = set()
    for path in sorted(raw_root.rglob("*.xml")):
        totals["xml_files"] += 1
        try:
            parsed, counts = parse_medquad_file(path, raw_root)
        except ET.ParseError:
            totals["malformed"] += 1
            continue
        for key, value in counts.items():
            totals[key] += value
        for document in parsed:
            if document.document_id in seen:
                totals["duplicate"] += 1
            else:
                seen.add(document.document_id)
                documents.append(document)
    totals["included"] = len(documents)
    return documents, totals


def chunk_document(
    document: MedicalDocument, max_chars: int = 1200, overlap_chars: int = 150
) -> list[MedicalChunk]:
    if max_chars < 200 or overlap_chars < 0 or overlap_chars >= max_chars:
        raise ValueError("invalid chunk configuration")
    text = f"Question: {document.question}\nAnswer: {document.answer}"
    if len(text) <= max_chars:
        parts = [text]
    else:
        parts, start = [], 0
        while start < len(text):
            end = min(len(text), start + max_chars)
            if end < len(text):
                boundary = text.rfind(" ", start + max_chars // 2, end)
                if boundary > start:
                    end = boundary
            parts.append(text[start:end].strip())
            if end == len(text):
                break
            start = end - overlap_chars
    return [
        MedicalChunk(
            f"{document.document_id}:chunk:{index:03d}",
            document.document_id,
            part,
            document.title,
            document.topic,
            document.source,
            document.source_url,
        )
        for index, part in enumerate(parts)
    ]
