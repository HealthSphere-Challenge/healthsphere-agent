from pathlib import Path

from app.agent.mts_patterns import analyze_split


def test_mts_analysis_preserves_split_qualified_stable_ids(tmp_path: Path):
    path = tmp_path / "dialogue.csv"
    path.write_text(
        'ID,section_header,section_text,dialogue\n1,HPI,summary,"Doctor: How long?\nPatient: Two days."\n'
    )
    first = analyze_split(path, "training")
    assert first == analyze_split(path, "training")
    assert first[0].record_id.startswith("mts:training:") and first[0].question_turns == 1
    assert analyze_split(path, "validation")[0].record_id != first[0].record_id
