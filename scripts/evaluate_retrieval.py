import argparse
import json
from pathlib import Path

from app.rag import MedicalRetriever, SparseVectorIndex


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--cases", type=Path, default=Path("evaluation/cases-v1.json"))
    args = parser.parse_args()
    retriever = MedicalRetriever(SparseVectorIndex.load(args.index))
    cases = json.loads(args.cases.read_text())
    retrieval_cases = [case for case in cases if case.get("expected_document")]
    hits = 0
    for case in retrieval_cases:
        results = retriever.retrieve(case["query"])
        hits += any(result.chunk.document_id == case["expected_document"] for result in results)
    print(
        json.dumps(
            {
                "metric": "hit_at_4",
                "hits": hits,
                "total": len(retrieval_cases),
                "rate": hits / len(retrieval_cases) if retrieval_cases else None,
            }
        )
    )


if __name__ == "__main__":
    main()
