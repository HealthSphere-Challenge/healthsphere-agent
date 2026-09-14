import json
from pathlib import Path


def test_golden_evaluation_set_has_required_categories():
    cases = json.loads(Path("evaluation/cases-v1.json").read_text())
    categories = {case["category"] for case in cases}
    assert len(cases) == 10
    assert {
        "supported",
        "assessment",
        "unsupported",
        "follow_up",
        "urgent",
        "injection",
        "score_safety",
        "medication_safety",
        "diagnosis_safety",
        "grounding",
    } <= categories
    assert all("patient" not in case for case in cases)
