# Agent architecture

Status: approved service responsibility; current app directories are placeholders. Python 3.13 with `uv` is the approved baseline; exact dependencies remain pending HS-013. No LLM integration, corpus/index, RAG or API is implemented. See the [Agent contract](AGENT_CONTRACT.md).

Browser → frontend → backend → Agent. Backend owns application users, profile, authorized conversation access and persistence. Agent owns retrieval, prompt/conversation orchestration, LLM adapter and safety behavior. No direct browser access or application PostgreSQL access. Agent never invents a predictive score or substitutes for the AI service; backend may supply immutable model-provenance-bearing assessment context for explanation.

## Planned module boundaries

Existing `app/agent/` coordinates turns; `app/rag/` manages retrieval; `app/llm/` encapsulates provider calls; `app/tools/` holds explicit bounded capabilities; `app/safety/` routes urgency and validates responses. API schemas/transport and tests will be added in HS-013. Avoid granting tools arbitrary code execution, external writes or access to whole user profiles.

MedQuAD supplies source-bearing medical Q&A; MTS-Dialog supplies conversation patterns/evaluation, not predictive labels. Cleaned text and retrieved chunks are untrusted data, never higher-priority instructions. No model training or fine-tuning is required for the Agent MVP.

## Planned turn flow

Validate request and permitted context → check urgent/safety signals before routine follow-up/retrieval → determine missing context → retrieve relevant approved sources where needed → assemble bounded prompt → call provider → check grounding/safety → return structured response through backend. An urgent path must not wait for an ordinary conversation to complete. Provider/retrieval failure yields an explicit unavailable/abstention state, not a medical conclusion.

Conversation persistence and ownership stay in backend; Agent receives only bounded context necessary for the turn. Prototype retention is 30 days from conversation creation and user deletion is required. Exact history/context caps, streaming behavior, deletion mechanics, and backup behavior remain pending HS-013/016.

## Producer contract responsibilities

Agent and backend co-review input limits, safety state enums, follow-up representation, citation format, provider errors, provenance and versioning. Approved response types distinguish `answer`, `follow_up`, `abstention`, and `urgent`; dependency failure uses the canonical error contract. The service endpoint is `/internal/v1/agent/responses`. Preserve source/corpus/prompt/model version metadata as applicable; avoid exposing private prompts or unnecessary context.

Provider/model, embedding model, vector storage, chunk sizes, retrieval parameters and provider data handling remain unresolved. Backend requests use an opaque bearer credential with a 2-second connect and 30-second total timeout; credential provisioning remains pending deployment. Remaining decisions must be justified against local corpus size, evaluation, cost/privacy and deployment requirements rather than introduced as dependencies silently.

See [RAG](../rag/RAG_PIPELINE.md), [safety](../safety/HEALTHCARE_SAFETY.md), [evaluation](../evaluation/EVALUATION_STRATEGY.md) and [testing](../testing/TESTING_STRATEGY.md).
