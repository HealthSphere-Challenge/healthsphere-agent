# Proposed GitHub issues — healthsphere-agent

Status: approved issue-body record, delivered to GitHub on 2026-09-13. The table retains stable project IDs; actual GitHub issue numbers are repository-local. Live issue bodies contain actual dependency and coordination links. Refresh GitHub before creating future issues.

Cross-repository coordination will live in approved GitHub Issues/Project. This file contains only issues proposed for this repository, not a project-wide governance authority. Dependency IDs include their repository below; actual issue links are added only after approved creation. Child membership is not a prerequisite cycle: HS-001 children may start after proposal approval; the coordinator closes after their review/merge evidence. HS-016 preparation may overlap QA, but actual deployment waits for HS-015 and hosting approval.

Labels below already exist; no new labels are proposed. Priority P0 applies to all immediate roadmap items; sizes S/M/L are relative, not delivery-date promises. P1/deferred: medical documents, advanced 7/30-day trend screens, recommendations/progress/timeline expansion, Women's Health, guardian/multi-profile accounts and extended preferences. Guardian/multi-profile remains excluded from MVP and requires a future explicit architecture decision.

| ID | Title | Kind | Dependencies | Labels | Size |
|---|---|---|---|---|---|
| [HS-001-AG](#hs-001-ag) | Repository foundation: agent | implementation | Stage 2 approval | documentation | M |
| [HS-013](#hs-013) | MedQuAD RAG + Safety Agent MVP | implementation | HS-001-AG, HS-002 | enhancement | L |
| [HS-016-AG](#hs-016-ag) | Deployment readiness: agent | implementation | HS-013 | enhancement | M |

# HS-001-AG

Proposed title: **[HS-001-AG] Repository foundation: agent**

Repository: `HealthSphere-Challenge/healthsphere-agent` · Priority: P0 · Size: M · Labels: `documentation`

## Context

Stage 2 approved the local documentation, skills and support files. Stage 3 created this live issue and authorized the foundation PR; product implementation and PR merge remain outside this stage.

## Objective

Review and deliver the approved Stage 2 foundation in this repository.

## User / Business Value

Keeps approved decisions discoverable and prevents architecture, UX or safety drift.

## Technical Scope

AGENTS, local ADLC, RAG/Agent/safety/evaluation/testing docs; three skills; verified dataset README corrections and service README/support files.

## Out of Scope

Product runtime/dependencies/endpoints/tables/training/indexing.

## Acceptance Criteria

- [ ] All required repository docs and specialized skills exist with working references.
- [ ] Approved versus proposed/unresolved choices are distinguished; current implementation status is accurate.
- [ ] Existing raw data/design assets preserved byte-for-byte; examples contain no real credentials.
- [ ] Local Stage 2 work is reviewed and merged only through an authorized PR targeting main.

## Testing Requirements

Markdown link audit, skill-creator metadata validation, git diff/whitespace review, ignore/template checks and original-asset checksum preservation.

## Dependencies

- Created under the explicit Stage 3 issue-delivery approval; product implementation still requires a later execution authorization.
- Coordination membership: [HS-001](https://github.com/HealthSphere-Challenge/healthsphere-frontend/issues/2); not a blocking dependency on coordinator closure.

## ADLC Gates

Discovery → Brainstorm → Architecture Check → Plan → Ticket → Development → Unit Tests → Integration / Contract Tests → Self Review → QA → Security / Healthcare Safety → Visual QA when UI → E2E when applicable → PR → CI → Merge decision. Record nonapplicable gates with reasons. Coordination issues gather linked child evidence; they do not duplicate implementation PRs. Documentation-only HS-001 work uses document/skill/hygiene validation rather than nonexistent runtime tests.

## Definition of Done

Acceptance criteria and required checks pass; architecture, scope, documentation and compatibility are reviewed; residual risks are recorded. Applicable lint/typecheck/build and CI pass. Implementation PR targets main and is merged only after an authorized decision. A coordination issue closes only when its linked implementation/release evidence is complete; it needs no artificial code PR. No failing or unrun required check is reported as passed.

# HS-013

Proposed title: **[HS-013] MedQuAD RAG + Safety Agent MVP**

Repository: `HealthSphere-Challenge/healthsphere-agent` · Priority: P0 · Size: L · Labels: `enhancement`

## Context

Stage 1 found no executable product, tests or CI; Stage 2 authorizes foundation/governance only. This future ticket is not implementation approval.

## Objective

Build a grounded, bounded conversational service with evaluated safety behavior.

## User / Business Value

Users can ask questions and receive useful follow-up without unsupported medical certainty.

## Technical Scope

Python/testing/CI foundation; verified corpus cleaning/exclusion/versioning; approved embeddings/vector/provider choice; retrieval; MTS-Dialog-informed follow-up with preserved splits; urgent/abstention/output checks; Agent API/provenance/contracts.

## Out of Scope

Fine-tuning requirements, clinical diagnosis, indexing empty answers, raw user data in knowledge corpus.

## Acceptance Criteria

- [ ] Empty-answer entries excluded, source traceability and corpus/index versions recorded.
- [ ] Provider/data handling and retrieval decisions justified before use.
- [ ] Grounded answers, follow-up, abstention, urgent and outage states meet reviewed case expectations.
- [ ] No invented predictive scores; deterministic CI and bounded measured retrieval/Agent evaluation recorded.

## Testing Requirements

Parser/chunk/exclusion unit tests, retrieval/source integration, held-out MTS split integrity, grounding/injection/urgency/uncertainty cases, backend contracts and configured live-provider evaluation.

## Dependencies

- `HS-001-AG` — healthsphere-agent
- `HS-002` — healthsphere-backend

## ADLC Gates

Discovery → Brainstorm → Architecture Check → Plan → Ticket → Development → Unit Tests → Integration / Contract Tests → Self Review → QA → Security / Healthcare Safety → Visual QA when UI → E2E when applicable → PR → CI → Merge decision. Record nonapplicable gates with reasons. Coordination issues gather linked child evidence; they do not duplicate implementation PRs. Documentation-only HS-001 work uses document/skill/hygiene validation rather than nonexistent runtime tests.

## Definition of Done

Acceptance criteria and required checks pass; architecture, scope, documentation and compatibility are reviewed; residual risks are recorded. Applicable lint/typecheck/build and CI pass. Implementation PR targets main and is merged only after an authorized decision. A coordination issue closes only when its linked implementation/release evidence is complete; it needs no artificial code PR. No failing or unrun required check is reported as passed.

# HS-016-AG

Proposed title: **[HS-016-AG] Deployment readiness: agent**

Repository: `HealthSphere-Challenge/healthsphere-agent` · Priority: P0 · Size: M · Labels: `enhancement`

## Context

Stage 1 found no executable product, tests or CI; Stage 2 authorizes foundation/governance only. This future ticket is not implementation approval.

## Objective

Prepare this service for the approved integrated prototype release.

## User / Business Value

The service can be deployed and recovered consistently within its existing boundary.

## Technical Scope

Agent packaging/deployment, approved provider secrets/data-use settings, corpus/index distribution and version compatibility, internal access and rollback notes. Configuration preparation can precede HS-015; actual publication requires passing HS-015 and an explicitly approved hosting/deployment plan.

## Out of Scope

Unapproved publication/spend, new service boundaries or product features.

## Acceptance Criteria

- [ ] Deployed Agent uses approved corpus/provider configuration, preserves safety behavior and has no public browser bypass.
- [ ] Document verified run/configuration/health/rollback steps with release revisions.
- [ ] Use synthetic demo data and an approved secrets mechanism; no production claims.

## Testing Requirements

Source/corpus compatibility, backend conversation smoke, provider failure/urgent path and secret/rollback review.

## Dependencies

- `HS-013` — healthsphere-agent
- HS-015 (frontend) and approved hosting/publication plan gate actual deployment; configuration preparation may proceed earlier.

## ADLC Gates

Discovery → Brainstorm → Architecture Check → Plan → Ticket → Development → Unit Tests → Integration / Contract Tests → Self Review → QA → Security / Healthcare Safety → Visual QA when UI → E2E when applicable → PR → CI → Merge decision. Record nonapplicable gates with reasons. Coordination issues gather linked child evidence; they do not duplicate implementation PRs. Documentation-only HS-001 work uses document/skill/hygiene validation rather than nonexistent runtime tests.

## Definition of Done

Acceptance criteria and required checks pass; architecture, scope, documentation and compatibility are reviewed; residual risks are recorded. Applicable lint/typecheck/build and CI pass. Implementation PR targets main and is merged only after an authorized decision. A coordination issue closes only when its linked implementation/release evidence is complete; it needs no artificial code PR. No failing or unrun required check is reported as passed.
