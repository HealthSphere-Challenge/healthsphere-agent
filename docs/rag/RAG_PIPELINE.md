# RAG pipeline and corpus provenance

Status: implemented by HS-013. [Verified MedQuAD inventory](../../data/medquad/README.md) is authoritative: 47,441 pairs, 16,407 indexed nonempty answers and 31,034 excluded empty answers.

## Source and cleaning

Parse raw XML without modifying it. Disable external entity/network resolution in the chosen parser. Keep collection, original path, document/question identifiers, source URL where present, question type, answer and provenance. Missing source metadata must be explicit; do not invent URLs or imply a retrieval date establishes medical freshness.

Normalize whitespace/markup while preserving medical wording, units and qualifiers. Exclude empty question/answer, invalid records, unsupported sources and unusable content with reason counts. Deduplicate while retaining all applicable source references. Do not synthesize missing answers. Preserve license files and source attribution; collection suitability/redistribution and freshness require review before inclusion, not inference from a top-level license alone.

## Chunking and retrieval

The versioned configuration keeps QA pairs intact up to 1,200 characters, then splits at word boundaries with 150-character overlap. It uses 16,384-dimensional sparse hashing TF vectors, cosine similarity, top-k 4, and minimum score 0.20. Source identifiers and chunk boundaries remain attached.

Retrieve only approved corpus content; patient conversation history is not automatically added to the knowledge index. Retrieved instructions cannot override system/task/safety boundaries. When no relevant evidence exists, abstain or ask a useful follow-up; do not force a confident answer.

## Corpus version and artifact record

Index metadata binds raw fingerprint, parser/cleaning version, exclusions and counts, chunk rules, embedding version/dimension, index settings and generation time. Generated artifacts remain ignored under `artifacts/`; the build command never runs during requests.

Evaluate retrieval with held-out queries, relevance judgments, source coverage and no-result scenarios. Measure Recall@k/MRR or another justified measure and report sample size; choose retrieval settings on development evaluation only. Response grounding needs separate Agent evaluation. No claimed retrieval score exists today.
