# Agent evaluation strategy

Status: HS-013 deterministic MVP evaluation implemented. The full local index achieved 2/2 hit@4 on the versioned known-source cases. The ten-case state/safety run achieved 10/10 response-type correctness, 1/1 urgent recall, 5/5 expected abstentions, and zero score/source-fabrication violations. These tiny samples are regression evidence only. HS-015 reviews broader release evidence.

| Area | Evidence |
|---|---|
| Corpus | Verified counts, exclusion reasons, provenance and raw→clean→chunk traceability |
| Retrieval | Held-out relevance judgments, Recall@k/MRR where appropriate, source coverage, no-result and ambiguous queries |
| Grounding | Claims supported by actual retrieved passages; citations valid; no fabricated facts/sources |
| Follow-up | Relevant missing-context questions, appropriate stopping and useful answers; no routine delay of urgent routing |
| Safety | Urgent routing, uncertainty, abstention, unsupported certainty, score invention and prompt-injection cases |
| Privacy/resilience | Minimal context, no secret/history leakage, provider/index failure, bounded response/time behavior |

Use MTS-Dialog training split for patterns, validation for tuning and both official/local test sets for held-out evaluation. Preserve split-qualified IDs, file hashes and exclusions. Do not use held-out dialogue/summaries in prompt examples or RAG. Review duplicate/contamination cases transparently; do not silently reshuffle splits. This dataset is not itself a complete safety benchmark or proof of medically correct follow-up.

Create additional synthetic reviewed safety scenarios; include ordinary queries, out-of-scope questions, ambiguous evidence, unsupported population and adversarial retrieved text. Define case-specific expected behavior and release criteria before tuning. Quantitative pass rates need denominator, dataset version, model/prompt/corpus versions and actual run evidence. No invented targets or scores.

Routine CI uses deterministic parsers/retrievers/provider adapters and safety smoke fixtures. A bounded separately configured live-provider evaluation records model/version/date/cost conditions and human review of representative and blocking cases. LLM-as-judge can assist, not replace grounded inspection. Test fixtures are not deployed canned success responses.
