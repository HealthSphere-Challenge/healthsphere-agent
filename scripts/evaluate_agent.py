import argparse
import asyncio
import json
from pathlib import Path
from uuid import UUID

from app.agent import AgentService
from app.rag import MedicalRetriever, SparseVectorIndex
from app.schemas import AgentRequest


class EvaluationLLM:
    provider_name = "deterministic-evaluation"
    model_name = "fixture-v1"

    async def generate(self, _system: str, _user: str) -> str:
        return "The retrieved medical information provides a general educational explanation."


ASSESSMENT = {
    "target_id": "incident_essential_hypertension_5y_v1",
    "score": 0.42,
    "score_type": "uncalibrated_experimental_probability_estimate",
    "calibrated": False,
    "model_version": "hypertension_5y_v1.0.0",
    "prediction_horizon_days": 1825,
}


async def evaluate(index_path: Path, cases_path: Path) -> dict[str, object]:
    index = SparseVectorIndex.load(index_path)
    service = AgentService(
        MedicalRetriever(index), EvaluationLLM(), str(index.metadata["corpus_version"])
    )
    cases = json.loads(cases_path.read_text())
    correct = urgent_total = urgent_correct = abstention_total = abstention_correct = 0
    score_violations = source_violations = 0
    for offset, case in enumerate(cases):
        request = AgentRequest(
            schema_version="1.0",
            request_id=UUID(int=(1 << 76) | offset),
            conversation_ref=UUID(int=(1 << 76) | 100 + offset),
            user_message=case["query"],
            recent_turns=[],
            health_context={
                "profile": None,
                "measurements": [],
                "assessment": ASSESSMENT if case["category"] == "assessment" else None,
            },
        )
        response = await service.respond(request)
        correct += response.response_type == case["expected"]
        if case["expected"] == "urgent":
            urgent_total += 1
            urgent_correct += response.response_type == "urgent"
        if case["expected"] == "abstention":
            abstention_total += 1
            abstention_correct += response.response_type == "abstention"
        score_violations += "42%" in response.content or "0.91" in response.content
        known = {chunk.chunk_id for chunk in index.chunks} | {
            f"healthsphere-assessment:{ASSESSMENT['model_version']}"
        }
        source_violations += any(str(source.source_id) not in known for source in response.sources)
    return {
        "cases": len(cases),
        "response_type_correct": correct,
        "urgent_recall": f"{urgent_correct}/{urgent_total}",
        "abstention_correct": f"{abstention_correct}/{abstention_total}",
        "score_fabrication_violations": score_violations,
        "source_fabrication_violations": source_violations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--cases", type=Path, default=Path("evaluation/cases-v1.json"))
    args = parser.parse_args()
    print(json.dumps(asyncio.run(evaluate(args.index, args.cases))))


if __name__ == "__main__":
    main()
