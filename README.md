# HealthSphere — Conversational Agent and RAG

## Current status — Stage 3

Foundation/governance only, delivered for review on 2026-09-13. MedQuAD and MTS-Dialog raw datasets, their READMEs/licenses, and placeholder app directories exist. No parser pipeline, embeddings, index, LLM integration, runtime, tests or CI exists yet. Documentation, repo-local skills and support templates describe future approved work; there are no application install/run commands to execute yet.

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

## Local configuration and delivery

`.env.example` documents placeholders only; `.env` is ignored and must never be committed. Runtime tickets must validate required configuration before startup. Use short-lived branches → PR → main, no develop; no silent merge. The approved roadmap exists as live GitHub issues; issues coordinate work but do not by themselves authorize implementation.

## Dataset responsibilities

- [MedQuAD](data/medquad/README.md): verified local 47,441 pairs; 16,407 nonempty answers; source knowledge for RAG.
- [MTS-Dialog](data/mts_dialog/README.md): 1,201/100/200/200 records in preserved training/validation/test splits; conversation patterns and evaluation.

Existing licenses and raw bytes are preserved. Data provenance and exclusions belong in dataset docs; this root README describes the service.
