# HealthSphere — Conversational Agent and RAG

## Runtime status

HS-013 adds the internal FastAPI RAG and safety Agent MVP. MedQuAD supplies source-bearing retrieval knowledge; MTS-Dialog informs bounded follow-up/evaluation behavior. The Agent explains only supplied predictive assessments and never creates or changes a score.

Exactly four independent repositories: browser → frontend → backend → PostgreSQL; backend → AI and backend → Agent. Frontend never calls specialized services directly. Backend owns application data/access, while each repository owns its own architecture/governance. Cross-repository delivery belongs in GitHub Issues/Project after approval.

One account = one health profile; English MVP. Guardian/family/multi-profile access is excluded. ML is experimental and cannot claim clinical validity. Agent never creates predictive scores. See [AGENTS.md](AGENTS.md) before work.

## Documentation

- [Agent Architecture](docs/architecture/AGENT_ARCHITECTURE.md)
- [Adlc](docs/engineering/ADLC.md)
- [Evaluation Strategy](docs/evaluation/EVALUATION_STRATEGY.md)
- [Rag Pipeline](docs/rag/RAG_PIPELINE.md)
- [Healthcare Safety](docs/safety/HEALTHCARE_SAFETY.md)
- [Testing Strategy](docs/testing/TESTING_STRATEGY.md)
- [Proposed GitHub issues](docs/planning/PROPOSED_ISSUES.md)
- [HS-013 implementation and local run guide](docs/IMPLEMENTATION.md)
- [Dataset provenance](docs/DATA_PROVENANCE.md)

## Local configuration and delivery

Use Python 3.13.11 and `uv`. Run `uv sync --locked --dev`, build the ignored local index with `uv run healthsphere-build-index`, then configure `.env` and start `uv run uvicorn app.main:app --factory`. Run `uv run ruff format --check .`, `uv run ruff check .`, and `uv run pytest` before review. See the implementation guide for API, safety, evaluation, and provider configuration.

## Dataset responsibilities

- [MedQuAD](data/medquad/README.md): verified local 47,441 pairs; 16,407 nonempty answers; source knowledge for RAG.
- [MTS-Dialog](data/mts_dialog/README.md): 1,201/100/200/200 records in preserved training/validation/test splits; conversation patterns and evaluation.

Existing licenses and raw bytes are preserved. Data provenance and exclusions belong in dataset docs; this root README describes the service.
