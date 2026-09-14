# Dataset provenance

## MedQuAD

- **Role:** sole medical-knowledge retrieval corpus.
- **Source:** Asma Ben Abacha and Dina Demner-Fushman, [MedQuAD](https://github.com/abachaa/MedQuAD), collected from the named US medical-information sources retained in each XML document.
- **License:** the repository-local `data/medquad/LICENSE.txt` is preserved. Individual upstream source terms may differ and require release review.
- **Local version:** raw fingerprint `sha256:0c998a31f0c13ac9886d6d963a055602c59f663115542a00c6bf2c1b98f3978f`, inventoried 2026-09-13.
- **Processing:** safe XML parsing, whitespace normalization, empty question/answer exclusion, stable SHA-256 document IDs, deterministic QA-aware chunking, and hashing TF vectors. Medical wording is not paraphrased.
- **Limitations:** static content can be incomplete or outdated; source quality varies; inclusion is not clinical validation or a current-guideline claim.

## MTS-Dialog

- **Role:** conversation-shape analysis and versioned follow-up/evaluation cases only. It is not indexed and does not supply live medical answers.
- **Source:** Asma Ben Abacha et al., [MTS-Dialog](https://github.com/abachaa/MTS-Dialog), with the collected data repository documented in `data/mts_dialog/README.md`.
- **License:** `data/mts_dialog/LICENSE.txt` is preserved.
- **Local version:** training 1,201, validation 100, test-1 200, and test-2 200 records, inventoried 2026-09-13.
- **Processing:** raw splits remain unchanged. The MVP's bounded follow-up shape was informed by training-set dialogue structure; deterministic synthetic evaluation cases are stored in `evaluation/cases-v1.json`. Held-out dialogue and summaries are not embedded, copied into prompts, or used as live medical truth.
- **Limitations:** clinical-dialogue form does not establish answer correctness or comprehensive conversational safety.
