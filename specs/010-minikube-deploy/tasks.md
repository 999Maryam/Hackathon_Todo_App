# Tasks: Minikube Deployment & AI-Assisted K8s Operations

**Input**: Design documents from `/specs/010-minikube-deploy/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md

**Tests**: Not required - this is a documentation-focused feature with manual verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation files**: `README.md`, `docs/troubleshooting/minikube.md`
- **Reference files (no modification)**: `charts/`, `backend/Dockerfile`, `frontend/Dockerfile`

**MVP Scope (Core Deliverable)**  
Phase 1–5 (T001–T026): Minikube cluster start + Helm deploy + port-forward access  
→ Enables full local K8s deployment of the chatbot

---

## Phase 1: Setup (Directory Structure)

**Purpose**: Create documentation directory structure

- [x] T001 Create `docs/troubleshooting/` directory structure
- [x] T002 [P] Review existing README.md structure for integration point

---

## Phase 2: Foundational (Prerequisites Documentation)

**Purpose**: Document prerequisites that MUST be in place before any deployment

**⚠️ CRITICAL**: This documentation must be complete before user story tasks

- [x] T003 Document Minikube prerequisites section in README.md (minimum versions, resources)
- [x] T004 [P] Document Docker prerequisites and `eval $(minikube docker-env)` setup in README.md
- [x] T005 [P] Document Helm prerequisites (version 3.x) in README.md
- [x] T006 Document kubectl-ai/kagent installation instructions (optional) in README.md
- [x] T006 Note: kubectl-ai/kagent is optional – document installation link in README.md (e.g., https://github.com/...)

**Checkpoint**: Prerequisites documentation complete - user story documentation can now begin

---

## Phase 3: User Story 1 - Start and Verify Minikube Cluster (Priority: P1) 🎯 MVP

**Goal**: Developers can start Minikube and verify cluster health with documented commands

**Independent Test**: Run `minikube start` and `kubectl get nodes` following README instructions → node shows `Ready` status

### Implementation for User Story 1

- [x] T007 [US1] Document `minikube start --driver=docker --memory=4096 --cpus=2` command in README.md
- [x] T008 [US1] Document `minikube status` verification command with expected output in README.md
- [x] T009 [P] [US1] Document `kubectl get nodes` verification command with expected output in README.md
- [x] T010 [P] [US1] Document `kubectl cluster-info` command for control plane verification in README.md
- [x] T011 [US1] Add troubleshooting note for Minikube startup failures in docs/troubleshooting/minikube.md

**Checkpoint**: User Story 1 complete - developer can start and verify Minikube cluster

---

## Phase 4: User Story 2 - Deploy Backend and Frontend via Helm Charts (Priority: P1)

**Goal**: Developers can deploy both applications using Helm and verify pods are running

**Independent Test**: Run `helm install` commands following README → `kubectl get pods` shows both pods `Running`

### Implementation for User Story 2

- [x] T012 [US2] Document secret creation command `kubectl create secret generic todo-backend-secrets` in README.md
- [x] T013 [US2] Document Docker image build commands with Minikube context in README.md
- [x] T014 [P] [US2] Document `helm install todo-backend ./charts/todo-backend-chart` command in README.md
- [x] T015 [P] [US2] Document `helm install todo-frontend ./charts/todo-frontend-chart` command in README.md
- [x] T016 [US2] Document `kubectl get pods` verification command with expected output in README.md
- [x] T016 Note: Use Kubernetes Secret 'todo-secrets' for OPENROUTER_API_KEY (already created in Spec 2)
- [x] T017 [US2] Document `kubectl get services` verification command in README.md
- [x] T018 [P] [US2] Add troubleshooting note for ImagePullBackOff errors in docs/troubleshooting/minikube.md
- [x] T019 [P] [US2] Add troubleshooting note for CrashLoopBackOff errors in docs/troubleshooting/minikube.md
- [x] T020 [P] [US2] Add troubleshooting note for missing secrets in docs/troubleshooting/minikube.md

**Checkpoint**: User Story 2 complete - developer can deploy both applications via Helm

---

## Phase 5: User Story 3 - Access Chatbot via Port Forwarding (Priority: P1)

**Goal**: Developers can access the deployed chatbot at localhost:3000 and verify backend health

**Independent Test**: Run port-forward commands → `curl localhost:8000/health` returns `{"status":"ok"}` and browser shows UI at localhost:3000

### Implementation for User Story 3

- [x] T021 [US3] Document `kubectl port-forward svc/todo-backend 8000:8000` command in README.md
- [x] T022 [P] [US3] Document `kubectl port-forward svc/todo-frontend 3000:3000` command in README.md
- [x] T023 [US3] Document `curl http://localhost:8000/health` verification with expected response in README.md
- [x] T024 [US3] Document browser access to `http://localhost:3000` in README.md
- [x] T025 [P] [US3] Add troubleshooting note for "address already in use" errors in docs/troubleshooting/minikube.md
- [x] T026 [P] [US3] Add troubleshooting note for service not accessible in docs/troubleshooting/minikube.md

**Checkpoint**: User Story 3 complete - developer can access chatbot UI and verify backend health

---

## Phase 6: User Story 4 - AI-Assisted Operations with kubectl-ai/kagent (Priority: P2)

**Goal**: Developers can use AI-assisted tools for Kubernetes operations

**Independent Test**: Run kubectl-ai command → translates natural language to kubectl command and displays output

### Implementation for User Story 4

- [x] T027 [US4] Document kubectl-ai "show me all pods and their status" example with output in README.md
- [x] T028 [P] [US4] Document kubectl-ai "why is my backend pod failing" example in README.md
- [x] T029 [P] [US4] Document kubectl-ai "scale backend to 2 replicas" example in README.md
- [x] T030 [US4] Add note that kubectl-ai/kagent is optional (manual commands always available) in README.md

**Checkpoint**: User Story 4 complete - developer has AI-assisted operation examples

---

## Phase 7: User Story 5 - Perform Dry-Run Helm Install (Priority: P2)

**Goal**: Developers can validate Helm charts before deployment using dry-run

**Independent Test**: Run `helm install --dry-run` → outputs valid YAML without creating resources

### Implementation for User Story 5

- [x] T031 [US5] Document `helm install todo-backend ./charts/todo-backend-chart --dry-run` command in README.md
- [x] T032 [P] [US5] Document `helm install todo-frontend ./charts/todo-frontend-chart --dry-run` command in README.md
- [x] T033 [US5] Document how to validate dry-run YAML output in README.md

**Checkpoint**: User Story 5 complete - developer can validate Helm charts with dry-run

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final README structure, cleanup commands, and validation

- [x] T034 [P] Organize README.md Minikube section with clear step-by-step numbering
- [x] T035 [P] Add cleanup commands section in README.md (helm uninstall, kubectl delete secret, minikube stop/delete)
- [x] T036 Create troubleshooting summary table in docs/troubleshooting/minikube.md (Issue | Symptom | Solution)
- [x] T037 Add resource requirements note in README.md (4GB RAM, 2 CPU minimum)
- [x] T038 Add link from README.md to troubleshooting guide docs/troubleshooting/minikube.md
- [x] T039 Validate complete workflow by following quickstart.md instructions
- [x] T040 Review all documentation for spec compliance (FR-001 through FR-012)
- [x] T041 Verify complete workflow by following README steps end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1, US2, US3 are P1 priority - complete first
  - US4, US5 are P2 priority - complete after P1 stories
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Cluster) | Foundational | Phase 2 |
| US2 (Helm Deploy) | US1 (cluster must be running) | T011 |
| US3 (Port Forward) | US2 (apps must be deployed) | T020 |
| US4 (AI Ops) | US2 (apps must be deployed for demos) | T020 |
| US5 (Dry Run) | Foundational (no deployed apps needed) | Phase 2 |

### Within Each User Story

- Documentation tasks can often be parallelized (different sections)
- Troubleshooting notes can be written in parallel with main documentation
- Verification commands depend on core commands being documented

### Parallel Opportunities

- All tasks marked [P] can run in parallel within their phase
- Troubleshooting tasks (T018, T019, T020, T025, T026) can run in parallel
- US4 and US5 can run in parallel after US2 completes

---

## Parallel Example: User Story 2

```bash
# Launch all parallelizable tasks for User Story 2 together:
Task: "Document `helm install todo-backend` command" (T014)
Task: "Document `helm install todo-frontend` command" (T015)
Task: "Add troubleshooting note for ImagePullBackOff" (T018)
Task: "Add troubleshooting note for CrashLoopBackOff" (T019)
Task: "Add troubleshooting note for missing secrets" (T020)
```

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US1 - Minikube Cluster
4. Complete Phase 4: US2 - Helm Deploy
5. Complete Phase 5: US3 - Port Forward
6. **STOP and VALIDATE**: Test complete deployment workflow
7. Demo if ready - full local K8s deployment working

### Incremental Delivery

1. Setup + Foundational → Prerequisites documented
2. Add US1 → Cluster can be started → Demo
3. Add US2 → Apps can be deployed → Demo
4. Add US3 → Apps can be accessed → Demo (MVP Complete!)
5. Add US4 → AI-assisted operations → Demo
6. Add US5 → Dry-run validation → Demo
7. Polish → Final documentation quality

### Recommended Single-Developer Order

Execute tasks in numerical order (T001 → T040) for optimal flow.

---

## Summary

| Phase | Task Count | Parallel Tasks |
|-------|------------|----------------|
| Phase 1: Setup | 2 | 1 |
| Phase 2: Foundational | 4 | 2 |
| Phase 3: US1 | 5 | 2 |
| Phase 4: US2 | 9 | 5 |
| Phase 5: US3 | 6 | 3 |
| Phase 6: US4 | 4 | 2 |
| Phase 7: US5 | 3 | 1 |
| Phase 8: Polish | 7 | 2 |
| **Total** | **40** | **18 (45%)** |

---

## Notes

- [P] tasks = different files/sections, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This is documentation-only - no code changes required
- Verification is manual (kubectl commands, curl, browser)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
