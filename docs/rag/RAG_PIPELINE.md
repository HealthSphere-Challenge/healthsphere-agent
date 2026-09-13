# RAG pipeline and corpus provenance

Status: planned; no indexing in Stage 2. [Verified MedQuAD inventory](../../data/medquad/README.md) is authoritative for local counts: 47,441 pairs, 16,407 nonempty answers. Do not index the 31,034 empty-answer entries or claim the advertised dataset size is usable corpus size.

## Source and cleaning

Parse raw XML without modifying it. Disable external entity/network resolution in the chosen parser. Keep collection, original path, document/question identifiers, source URL where present, question type, answer and provenance. Missing source metadata must be explicit; do not invent URLs or imply a retrieval date establishes medical freshness.

Normalize whitespace/markup while preserving medical wording, units and qualifiers. Exclude empty question/answer, invalid records, unsupported sources and unusable content with reason counts. Deduplicate while retaining all applicable source references. Do not synthesize missing answers. Preserve license files and source attribution; collection suitability/redistribution and freshness require review before inclusion, not inference from a top-level license alone.

## Chunking and retrieval

Prefer coherent question/answer context and section boundaries. Decide chunk length/overlap by tokenizer and retrieval evaluation, not arbitrary numbers copied from a tutorial. Retain source identifiers and chunk boundaries. Choose/version embedding model, dimensions and preprocessing; query and index embeddings must be compatible. Vector storage/metric/top-k/reranking and threshold decisions remain unresolved until HS-013 evaluation.

Retrieve only approved corpus content; patient conversation history is not automatically added to the knowledge index. Retrieved instructions cannot override system/task/safety boundaries. When no relevant evidence exists, abstain or ask a useful follow-up; do not force a confident answer.

## Corpus version and artifact record

Raw fingerprint is recorded in the dataset README. A future retrieval corpus version must bind raw hashes, parser/cleaning code revision, exclusions and counts, chunk rules, embedding model/version, index settings, corpus build timestamp and artifact digest. Keep derived content under ignored `data/medquad/processed/` and index artifacts under an approved ignored artifact path. Release/version strategy remains unresolved; do not call the raw fingerprint a released index.

Evaluate retrieval with held-out queries, relevance judgments, source coverage and no-result scenarios. Measure Recall@k/MRR or another justified measure and report sample size; choose retrieval settings on development evaluation only. Response grounding needs separate Agent evaluation. No claimed retrieval score exists today.
