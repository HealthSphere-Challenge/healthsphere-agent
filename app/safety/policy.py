import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    response_type: str
    content: str
    reason: str


URGENT_PATTERNS = [
    (re.compile(r"\b(severe|crushing) chest pain\b", re.I), "severe_chest_pain"),
    (
        re.compile(r"\b(can'?t breathe|cannot breathe|severe difficulty breathing)\b", re.I),
        "severe_breathing_difficulty",
    ),
    (
        re.compile(r"\b(unconscious|loss of consciousness|passed out and won'?t wake)\b", re.I),
        "loss_of_consciousness",
    ),
    (
        re.compile(r"\b(face droop|slurred speech|sudden one-sided weakness)\b", re.I),
        "possible_stroke_signs",
    ),
    (
        re.compile(r"\b(kill myself|suicide|immediate self-harm)\b", re.I),
        "immediate_self_harm_danger",
    ),
]


def precheck(message: str) -> SafetyDecision | None:
    for pattern, reason in URGENT_PATTERNS:
        if pattern.search(message):
            return SafetyDecision(
                "urgent",
                "Seek immediate emergency help now. Contact local emergency services or go to the nearest emergency department. Do not wait for this assistant.",
                reason,
            )
    lower = message.lower()
    if any(
        phrase in lower
        for phrase in ("stop my medicine", "stop my medication", "change my dose", "should i stop")
    ):
        return SafetyDecision(
            "abstention",
            "Do not stop or change prescribed medication based on this assistant. Contact the prescribing healthcare professional or a pharmacist for guidance.",
            "medication_change_request",
        )
    if "hidden prompt" in lower or "system instructions" in lower:
        return SafetyDecision(
            "abstention",
            "I cannot provide private system instructions. I can help with a health-information question using the available medical sources.",
            "prompt_exfiltration",
        )
    if any(
        phrase in lower
        for phrase in (
            "invent a diagnosis",
            "invent a risk score",
            "change my score",
            "recalculate my score",
        )
    ):
        return SafetyDecision(
            "abstention",
            "I cannot invent a diagnosis or create, change, or recalculate a health risk score.",
            "score_or_diagnosis_manipulation",
        )
    if re.search(r"\binvent\b.*\brisk score\b", lower):
        return SafetyDecision(
            "abstention",
            "I cannot invent a diagnosis or create, change, or recalculate a health risk score.",
            "score_or_diagnosis_manipulation",
        )
    if re.search(r"\b(do i have|diagnose me|am i diagnosed)\b", lower):
        return SafetyDecision(
            "abstention",
            "I cannot diagnose a medical condition. A qualified healthcare professional can evaluate symptoms, measurements, and appropriate tests.",
            "diagnosis_request",
        )
    return None


def unsafe_generated_answer(content: str, supplied_score: float | None) -> bool:
    lower = content.lower()
    if any(
        phrase in lower
        for phrase in (
            "you are diagnosed",
            "you definitely have",
            "stop taking",
            "change your dose",
            "hidden system prompt",
        )
    ):
        return True
    if supplied_score is not None and re.search(
        r"\b\d+(?:\.\d+)?%\s+(?:chance|risk|probability)", lower
    ):
        return True
    if re.search(r"\b(?:your|the)\s+(?:risk|score|probability)\s+(?:is|=)\s+\d", lower):
        return True
    return False


def fabricates_source(content: str, allowed_source_ids: set[str]) -> bool:
    claimed = set(re.findall(r"medquad:[a-f0-9]+(?::chunk:\d+)?", content.lower()))
    return bool(claimed - allowed_source_ids)
