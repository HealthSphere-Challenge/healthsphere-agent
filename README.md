# MedQuAD Dataset — HealthSphere

## Overview

This directory contains the **MedQuAD (Medical Question Answering Dataset)** used by the HealthSphere AI Agent.

MedQuAD is a medical question-answering dataset containing **47,457 medical question-answer pairs** collected from multiple trusted NIH-related health information sources.

In HealthSphere, MedQuAD is primarily used as a **medical knowledge source for the Retrieval-Augmented Generation (RAG) pipeline**.

It is **not used to train the HealthSphere predictive ML model**.

---

## Purpose in HealthSphere

MedQuAD provides medical knowledge that can be retrieved when a user asks a health-related question.

For example:

```text
User
"What is hypertension?"
        ↓
HealthSphere AI Agent
        ↓
RAG Retriever
        ↓
MedQuAD Knowledge Base
        ↓
Relevant medical information
        ↓
LLM
        ↓
Simple and contextualized explanation
```

This architecture allows the AI assistant to retrieve relevant medical information before generating its response.

---

## Dataset Source

Original dataset:

**MedQuAD — Medical Question Answering Dataset**

GitHub repository:

https://github.com/abachaa/MedQuAD

The dataset contains medical question-answer pairs collected from multiple NIH websites and health information resources.

---

## License

MedQuAD is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

The original license file is preserved in:

```text
data/medquad/LICENSE.txt
```

The original authors and dataset source must be properly attributed when using or redistributing the dataset.

Please refer to the original MedQuAD repository and `LICENSE.txt` for complete licensing information.

---

## Directory Structure

```text
medquad/
│
├── raw/
│   ├── 1_CancerGov_QA/
│   ├── 2_GARD_QA/
│   ├── 3_GHR_QA/
│   ├── 4_MPlus_Health_Topics_QA/
│   ├── 5_NIDDK_QA/
│   ├── 6_NINDS_QA/
│   ├── 7_SeniorHealth_QA/
│   ├── 8_NHLBI_QA_XML/
│   ├── 9_CDC_QA/
│   ├── 10_MPlus_ADAM_QA/
│   ├── 11_MPlusDrugs_QA/
│   └── 12_MPlusHerbsSupplements_QA/
│
├── processed/
│   └── .gitkeep
│
├── LICENSE.txt
└── README.md
```

---

## Raw Data

The directory:

```text
raw/
```

contains the original MedQuAD data collected for HealthSphere.

The raw dataset must remain **unchanged**.

Any cleaning, parsing, transformation or normalization must generate new files under:

```text
processed/
```

This ensures that the original dataset remains available and that the data-processing pipeline is reproducible.

---

## Dataset Collections

The raw dataset is divided into multiple medical Q&A collections:

| Collection | Description |
|---|---|
| `1_CancerGov_QA` | Cancer-related medical questions |
| `2_GARD_QA` | Genetic and rare disease information |
| `3_GHR_QA` | Genetics-related health information |
| `4_MPlus_Health_Topics_QA` | General health topics |
| `5_NIDDK_QA` | Diabetes, digestive and kidney disease information |
| `6_NINDS_QA` | Neurological disorder information |
| `7_SeniorHealth_QA` | Health information related to older adults |
| `8_NHLBI_QA_XML` | Heart, lung and blood-related information |
| `9_CDC_QA` | Public health information |
| `10_MPlus_ADAM_QA` | General medical information |
| `11_MPlusDrugs_QA` | Drug-related information |
| `12_MPlusHerbsSupplements_QA` | Herbs and supplement information |

Not every collection must necessarily be used by the final HealthSphere RAG system.

Relevant collections will be selected and evaluated during development.

---

## Data Processing

The planned processing pipeline is:

```text
MedQuAD Raw Data
       ↓
XML / Data Parsing
       ↓
Data Cleaning
       ↓
Question / Answer Extraction
       ↓
Metadata Extraction
       ↓
Normalized Dataset
       ↓
data/medquad/processed/
```

A processed record may conceptually contain:

```json
{
  "question": "What is hypertension?",
  "answer": "Hypertension is...",
  "category": "cardiovascular",
  "source": "NHLBI"
}
```

The exact processed schema may evolve during development.

---

## RAG Pipeline

After preprocessing, MedQuAD will be integrated into the HealthSphere RAG pipeline.

```text
MedQuAD
   ↓
Cleaning
   ↓
Chunking
   ↓
Embedding Model
   ↓
Vector Embeddings
   ↓
Vector Database
   ↓
Retriever
```

When a user asks a question:

```text
User Question
      ↓
Embedding Model
      ↓
Question Vector
      ↓
Vector Similarity Search
      ↓
Relevant MedQuAD Chunks
      ↓
AI Agent
      ↓
LLM
      ↓
HealthSphere Response
```

---

## Why Embeddings Are Used

Traditional keyword search may fail when two sentences have similar meanings but use different words.

An embedding model transforms text into numerical vectors.

For example:

```text
"What are the symptoms of diabetes?"

            ↓

       Embedding Model

            ↓

[0.21, -0.43, 0.76, ...]
```

Documents with similar meanings should have nearby vector representations.

This allows HealthSphere to perform **semantic medical knowledge retrieval**.

---

## Role of the LLM

MedQuAD itself does not generate the final chatbot response.

Instead:

```text
MedQuAD
   ↓
provides knowledge

RAG
   ↓
retrieves relevant knowledge

LLM
   ↓
generates the natural-language response

AI Agent
   ↓
orchestrates the process
```

The LLM receives the user's question together with relevant retrieved context and generates a simplified response.

---

## MedQuAD vs Predictive ML

HealthSphere intentionally separates these two AI components.

### Predictive ML

Located in:

```text
healthsphere-ai
```

Its responsibility is:

```text
Structured Patient Data
        ↓
ML Model
        ↓
Risk Assessment
```

### MedQuAD / RAG

Located in:

```text
healthsphere-agent
```

Its responsibility is:

```text
Medical Question
       ↓
Knowledge Retrieval
       ↓
LLM Explanation
```

Therefore:

```text
MedQuAD → RAG / Medical Knowledge

Synthea → Structured health data / ML experimentation
```

MedQuAD is **not used to generate the `health_risk_pipeline.joblib` model**.

---

## Current Status — Phase 0

During Phase 0:

- [x] MedQuAD identified
- [x] Dataset source documented
- [x] Raw dataset collected
- [x] Dataset integrated into repository structure
- [x] License preserved
- [ ] Data parsing
- [ ] Data cleaning
- [ ] Dataset normalization
- [ ] Chunking strategy
- [ ] Embedding generation
- [ ] Vector database integration
- [ ] RAG retriever implementation
- [ ] RAG evaluation

---

## Planned Next Steps

```text
1. Analyze MedQuAD structure
2. Parse the original dataset
3. Extract questions, answers and metadata
4. Clean and normalize the data
5. Generate a processed dataset
6. Define chunking strategy
7. Select an embedding model
8. Generate embeddings
9. Store embeddings in a vector database
10. Implement semantic retrieval
11. Connect the retriever to the HealthSphere AI Agent
12. Evaluate retrieval quality
```

---

## Important

The files under:

```text
raw/
```

must not be manually modified.

All generated or transformed data should be stored under:

```text
processed/
```

This convention helps maintain **data provenance, reproducibility and traceability**.

---

## Medical Disclaimer

MedQuAD is used by HealthSphere as a medical information resource.

Information retrieved from this dataset and responses generated by the HealthSphere AI Agent are intended for **informational and educational purposes only**.

They do not constitute a medical diagnosis and should not replace consultation with qualified healthcare professionals.