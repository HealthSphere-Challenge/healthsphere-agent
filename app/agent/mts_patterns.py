import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DialogueRecord:
    record_id: str
    split: str
    section_header: str
    question_turns: int


def analyze_split(path: Path, split: str) -> list[DialogueRecord]:
    records = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            raw_id = (row.get("ID") or "").strip()
            dialogue = row.get("dialogue") or ""
            if not raw_id or not dialogue.strip():
                continue
            identity = hashlib.sha256(f"{split}:{raw_id}".encode()).hexdigest()[:16]
            records.append(
                DialogueRecord(
                    f"mts:{split}:{identity}",
                    split,
                    (row.get("section_header") or "unknown").strip(),
                    sum(line.strip().endswith("?") for line in dialogue.splitlines()),
                )
            )
    return records
