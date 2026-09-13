# Agent testing strategy

Status: planned tooling in HS-013; no runner, CI or runtime yet.

- pytest unit: XML/CSV parsing, empty-answer exclusion, cleaning, chunk metadata, bounded context, safety routing and provider error mapping.
- Integration: clean/chunk/index round-trip on a small approved corpus fixture, embedding/index compatibility and source traceability; provider adapter simulated deterministically.
- Contract: Agent owns Pydantic producer/consumer schemas and backend checks synthetic consumer fixtures. Cover schema version, UUID/request correlation, response/source/provenance shape, null/empty/omitted behavior, answer/follow-up/abstention/urgent, malformed response, timeout, and canonical dependency errors. No fifth contract repository.
- Safety: urgent path precedes routine retrieval/follow-up; no invented scores/citations, no unsupported certainty, no data leakage or obedience to retrieved instructions.
- Evaluation: [evaluation strategy](../evaluation/EVALUATION_STRATEGY.md) plus preserved MTS-Dialog splits; held-out tests never tune prompts or populate retrieval.
- Security: safe parsing, bounded inputs, service authentication when selected, controlled tool access and dependency/secret scanning.

CI minimum: reproducible Python 3.13 install with `uv`, lint, pytest and deterministic retrieval/safety smoke tests. Record exact dependency/workflow versions and commands in HS-013. Do not require paid provider calls for every PR; use separately approved live evaluations for release evidence. Synthetic fixture answers cannot substitute for a live assistant in showcase claims.

Stage 2 checks documentation links, skill metadata, accurate inventories and raw-data preservation only. No indexing or training runs are authorized now.
