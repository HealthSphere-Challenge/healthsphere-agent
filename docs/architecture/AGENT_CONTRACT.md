# Backend–Agent contract

Status: stable transport is the **APPROVED IMPLEMENTED CONTRACT**. HS-013 defines the retrieval, safety, prompt, context-limit, and response behavior below.

Contract revision: `phase1-hs002-2026-09-13`. Agent owns Pydantic producer/consumer schemas for this boundary; the backend contract is the application-level companion.

## Request — APPROVED CONTRACT

The backend alone calls `POST /internal/v1/agent/responses` using a service-specific opaque bearer credential and `X-Request-ID`. IDs are UUIDv4, JSON uses `snake_case`, and timestamps use RFC 3339 UTC with milliseconds. Connect timeout is 2 seconds and total timeout is 30 seconds. There are no automatic application retries initially.

```json
{
  "schema_version": "1.0",
  "request_id": "c4a760a8-7d0b-4f98-9652-244be1ebcc2e",
  "conversation_ref": "7a19544c-e55f-4ea8-96b9-557575027fb4",
  "user_message": "What can affect sleep duration?",
  "recent_turns": [{"role": "assistant", "content": "Which part of sleep would you like to discuss?"}],
  "health_context": {"profile": null, "measurements": [], "assessment": null}
}
```

`conversation_ref` is pseudonymous and not the application user ID. The backend sends only the minimum authorized context needed for this turn. User messages and turn content are capped at 2,000 characters, recent history at 6 turns, and measurements at 20 items. Omitted context was not supplied, null means unavailable/unknown, and an empty array means no items. Assessment context, when present, is immutable provenance-bearing output from AI; Agent cannot create or change its score.

## Response — APPROVED CONTRACT

Agent returns exactly one `response_type`: `answer`, `follow_up`, `abstention`, or `urgent`. Backend and frontend preserve the state rather than converting it into generic success.

```json
{
  "schema_version": "1.0",
  "request_id": "c4a760a8-7d0b-4f98-9652-244be1ebcc2e",
  "response_type": "answer",
  "content": "Several habits and health factors can affect sleep duration.",
  "sources": [{"source_id": "medquad:synthetic-example", "title": "Sleep information", "url": null}],
  "safety": {"urgent": false, "reason": null},
  "uncertainty": "General information only; this does not determine the cause for an individual.",
  "provenance": {
    "corpus_version": "pending_hs_013",
    "retrieval_version": "pending_hs_013",
    "prompt_version": "pending_hs_013",
    "model_provider": "pending_hs_013",
    "model_name": "pending_hs_013",
    "generated_at": "2026-09-13T09:06:08.000Z"
  }
}
```

The example is synthetic and establishes shape. HS-013 requires `content` for every state, exact retrieved chunk or supplied-assessment source identifiers for answers, and versioned provenance. An `abstention` represents insufficient evidence or a safety boundary. An `urgent` response routes to immediate-care guidance. Neither is an inferred diagnosis.

Canonical failures use:

```json
{
  "error": {
    "code": "dependency_unavailable",
    "message": "The assistant is temporarily unavailable.",
    "details": null,
    "request_id": "c4a760a8-7d0b-4f98-9652-244be1ebcc2e",
    "retry_after_seconds": null
  }
}
```

Errors never include prompts, retrieved passages, conversation text, credentials, or provider bodies. Retrieved content is untrusted data. Empty-answer MedQuAD entries remain excluded and source metadata remains attached.

## Conversation handling

The backend owns conversation authorization and persistence. Prototype retention is 30 days from conversation creation; users must be able to delete their conversations. Operational deletion and backup behavior are **PENDING HS-013/HS-016**. Agent receives no browser cookie and has no application-database access.

## Compatibility and tests

Agent owns Pydantic request and response schemas; backend validates responses as consumer. Future fixture-based contract tests use synthetic answer, follow-up, abstention, urgent, no-source, malformed, provider-failure, and timeout cases. Tests assert that provenance/sources remain attached, untrusted retrieved instructions cannot override system safety, and absent assessment data cannot become an invented score. Compatible additions remain optional; changes to types, enum meaning, nullability, or safety semantics require a schema-version change and linked producer/consumer PR evidence. Python 3.13 with `uv` is the approved baseline; exact dependency versions are selected and tested in HS-013.
