# HS-013 RAG and safety Agent MVP

## Runtime architecture

The backend alone calls `POST /internal/v1/agent/responses`. FastAPI validates the frozen schema, Bearer service credential, UUIDv4 request correlation, bounded six-turn history, and bounded minimum health context. The Agent does not persist conversations and does not access the application database, browser, predictive model, or frontend.

The turn pipeline is: validation → deterministic urgent/scope safety precheck → assessment explanation or follow-up decision → MedQuAD retrieval → bounded grounded prompt → provider-neutral LLM → post-generation safety check → structured response. Urgent handling bypasses retrieval and generation. Provider failure returns the canonical `dependency_unavailable` envelope; insufficient retrieval returns `abstention`.

## Corpus and retrieval

Run:

```bash
uv sync --locked --dev
uv run healthsphere-build-index
uv run healthsphere-evaluate-retrieval --index artifacts/medquad-index-v1/index.json
uv run healthsphere-evaluate-agent --index artifacts/medquad-index-v1/index.json
```

`medquad-parser-v1` excludes empty answers and preserves source path, source name, URL, topic, title, and stable document ID. `qa-char-1200-overlap-150-v1` keeps small QA pairs intact and splits long answers at word boundaries with 150-character overlap. `healthsphere-hashing-tf-v1` maps normalized tokens deterministically into 16,384 sparse dimensions. The local JSON index uses cosine similarity, top-k 4, and minimum score 0.20 under `medquad-sparse-cosine-v1`. Artifacts are ignored and never rebuilt during requests or ordinary startup.

Index metadata binds the corpus/index/parser/chunking/embedding versions, vector dimension, counts, generation time, and raw fingerprint. Runtime fails closed for missing or incompatible metadata. This lightweight index avoids hosted infrastructure and model downloads, but lexical hashing has weaker semantic recall than a trained biomedical embedding model.

## LLM and prompt configuration

`LLMClient` isolates generation. The MVP adapter uses an OpenAI-compatible server configured only through server environment variables, temperature 0, 500 output tokens, and a timeout below the 30-second service budget. Clients cannot supply a URL, provider, model, prompt, corpus, or index path. CI uses deterministic fakes; live-provider access is optional and never required by tests.

The reviewable `app/prompts/system-v1.txt` requires evidence-only answers, treats retrieved text as data, forbids diagnosis/prescribing/score manipulation/secrets, and requires abstention. Responses include corpus, retrieval, prompt, provider, model, and generation-time provenance.

## Safety and response behavior

- `answer`: grounded in retrieved chunks with exact machine-readable source IDs, or explains the exact backend-supplied assessment provenance.
- `follow_up`: a single bounded clarification for a very short ambiguous symptom/term request.
- `abstention`: insufficient evidence, diagnosis/medication/score manipulation, prompt exfiltration, or unsafe generated content.
- `urgent`: explicit high-recall, reviewable emergency phrases are handled before retrieval with short immediate-care language and no diagnosis.

Assessment explanation repeats only the supplied score, calls it experimental and uncalibrated, and explains its five-year horizon and synthetic-data limitation. It never calculates inputs, changes the score, creates categories, or presents a clinical percentage. Logs contain request ID, response type, and retrieval count only; they exclude message, conversation reference, context, score, token, evidence, and provider body.

## Local service

Copy `.env.example` to ignored `.env`, set a long random internal token and provider key, build the index, then run:

```bash
uv run uvicorn app.main:create_app --factory
```

`GET /health` is a public liveness probe. Authenticated `GET /ready` confirms compatible index and configured provider metadata without exposing secrets. A local provider smoke test should exercise one grounded question, one unsupported question, one urgent phrase, and an assessment explanation. It must be reviewed manually; deterministic CI does not establish clinical safety.

## Evaluation limits

`evaluation/cases-v1.json` fixes ten synthetic cases across retrieval, attribution, follow-up, abstention, urgency, injection, diagnosis, medication, and score safety. The full-index run reports 2/2 hit@4, 10/10 response-type correctness, 1/1 urgent recall, 5/5 expected abstentions, and zero score/source-fabrication violations. These small fixtures demonstrate contract and regression behavior only; they do not establish broad retrieval quality, medical correctness, clinical validation, or safety certification. English is the only evaluated language.
