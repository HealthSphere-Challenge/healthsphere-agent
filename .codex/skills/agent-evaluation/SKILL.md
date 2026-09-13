---
name: agent-evaluation
description: "Evaluate HealthSphere retrieval, grounded dialogue and follow-up behavior without contaminating held-out data."
---

# Agent Evaluation

Read the active approved ticket and relevant repository instructions first. This skill does not expand authorization.

- [Evaluation Strategy](../../../docs/evaluation/EVALUATION_STRATEGY.md)
- [Testing Strategy](../../../docs/testing/TESTING_STRATEGY.md)
- [Readme](../../../data/mts_dialog/README.md)

## Workflow

Preserve split-qualified MTS-Dialog IDs and official/local train/validation/test assignments. Keep test dialogue and summaries out of prompts and retrieval. Version cases and expected behavior before tuning; report retrieval and response-grounding results separately. Run deterministic safety/adapter tests and any configured bounded live-provider evaluation, recording model/prompt/corpus versions and sample sizes. Review blocking failures directly instead of relying only on an LLM judge. Distinguish fixture success from live-service evidence.
