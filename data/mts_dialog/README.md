# MTS-Dialog Dataset — HealthSphere

## Overview

This directory contains the **MTS-Dialog dataset** used by the HealthSphere AI Agent.

MTS-Dialog is a collection of approximately **1.7K short doctor-patient conversations** with corresponding clinical summaries and section headers.

The dataset is used in HealthSphere primarily to support:

- Conversation flow design
- Follow-up question strategies
- Clinical dialogue understanding
- Evaluation of conversational behavior
- Prompt engineering for the AI Agent

It is **not used to train the HealthSphere predictive ML model**.

---

## Purpose in HealthSphere

HealthSphere includes an AI-powered conversational assistant that should not immediately provide a conclusion when important information is missing.

For example:

```text
User:
"I have abdominal pain."

        ↓

HealthSphere AI Agent

        ↓

Missing information detected

        ↓

Follow-up questions:

- Where exactly is the pain?
- How long has it been present?
- How severe is it?
- Do you have nausea?
- Do you have fever?
- Are you taking any medication?
```

MTS-Dialog helps us understand realistic patterns of doctor-patient interaction and structure better follow-up conversations.

---

## Dataset Source

Original dataset:

**MTS-Dialog — Doctor-Patient Conversations and Clinical Summaries**

Original repository:

https://github.com/abachaa/MTS-Dialog

Dataset repository used for collection:

https://github.com/CG020/MTS-Dialog_Data

The dataset was introduced in:

**An Empirical Study of Clinical Note Generation from Doctor-Patient Encounters**

Authors:

- Asma Ben Abacha
- Wen-wai Yim
- Yadan Fan
- Thomas Lin

EACL 2023.

---

## Dataset Size

The main dataset contains approximately:

```text
Training set:   1,201 conversations
Validation set: 100 conversations
Test set 1:     200 conversations
Test set 2:     200 conversations
```

The dataset contains doctor-patient conversations associated with clinical summaries and normalized clinical sections.

---

## Clinical Sections

MTS-Dialog includes clinical sections such as:

```text
Family / Social History
History of Present Illness
Past Medical History
Chief Complaint
Past Surgical History
Allergies
Review of Systems
Medications
Assessment
Examination
Diagnosis
Disposition
Plan
Emergency Department Course
Immunizations
Imaging
Gynecologic History
Procedures
Other History
Labs
```

These sections make the dataset particularly useful for HealthSphere's conversational workflow.

---

## Directory Structure

```text
mts_dialog/
│
├── raw/
│   └── Main-Dataset/
│       ├── ...
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

contains the original collected MTS-Dialog files.

The raw files must remain unchanged.

Any transformation, cleaning, normalization or derived dataset must be generated under:

```text
processed/
```

---

## Planned Processing

The planned processing pipeline is:

```text
MTS-Dialog Raw Dataset
        ↓
Conversation Parsing
        ↓
Speaker Identification
        ↓
Clinical Section Extraction
        ↓
Conversation Pattern Analysis
        ↓
Follow-up Question Strategy
        ↓
Agent Evaluation Dataset
```

---

## Role in the AI Agent

MTS-Dialog is mainly used to improve the conversational behavior of the HealthSphere AI Agent.

Conceptually:

```text
User Message
     ↓
AI Agent
     ↓
Identify intent / symptom
     ↓
Identify missing information
     ↓
Select follow-up strategy
     ↓
Generate next question
```

MTS-Dialog can help us analyze patterns such as:

```text
Symptom
   ↓
Duration
   ↓
Severity
   ↓
Location
   ↓
Associated symptoms
   ↓
Medical history
   ↓
Medication
```

---

## MTS-Dialog vs MedQuAD

HealthSphere uses both datasets for different purposes.

### MedQuAD

```text
Medical Question
      ↓
RAG
      ↓
Medical Knowledge Retrieval
```

Main purpose:

- Medical knowledge
- Explanations
- Question answering
- RAG retrieval

### MTS-Dialog

```text
Patient Message
      ↓
Conversation Logic
      ↓
Follow-up Questions
```

Main purpose:

- Dialogue patterns
- Follow-up strategies
- Conversation evaluation
- Prompt design

---

## MTS-Dialog vs Predictive ML

MTS-Dialog is not used by the predictive ML service.

The HealthSphere architecture separates:

```text
healthsphere-ai
      ↓
Predictive Machine Learning

healthsphere-agent
      ↓
Conversational AI + RAG + LLM
```

The predictive ML component produces structured risk assessments.

The AI Agent is responsible for conversation, explanation and information retrieval.

---

## Current Status — Phase 0

- [x] Dataset identified
- [x] Dataset collected
- [x] Main dataset selected
- [x] Dataset source documented
- [x] License preserved
- [ ] Conversation analysis
- [ ] Dialogue preprocessing
- [ ] Follow-up pattern extraction
- [ ] Agent prompt design
- [ ] Conversation evaluation
- [ ] Integration with HealthSphere AI Agent

---

## Planned Next Steps

```text
1. Analyze MTS-Dialog structure
2. Inspect training / validation / test files
3. Identify useful conversation patterns
4. Extract follow-up question strategies
5. Define conversation state representation
6. Create agent prompts
7. Build evaluation scenarios
8. Integrate with HealthSphere AI Agent
9. Test conversation quality
```

---

## Important

The files under:

```text
raw/
```

must not be manually modified.

Processed or transformed files should be stored under:

```text
processed/
```

This helps preserve:

- Data provenance
- Reproducibility
- Traceability

---

## Medical Disclaimer

MTS-Dialog is used by HealthSphere as a research and development resource for conversational AI.

The HealthSphere AI Agent is intended for informational and educational purposes only.

It must not provide autonomous medical diagnosis or replace consultation with qualified healthcare professionals.