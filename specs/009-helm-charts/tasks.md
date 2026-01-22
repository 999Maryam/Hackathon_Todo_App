# Tasks: Helm Charts for Todo AI Chatbot

**Input**: Design documents from `/specs/009-helm-charts/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No test tasks included - spec does not request TDD approach. Validation via helm lint/template is included in implementation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Helm charts**: `charts/todo-backend-chart/`, `charts/todo-frontend-chart/`
- **Documentation**: `README.md` at repository root

**MVP Scope (Core Deliverable)**  
Phase 1–2 (T001–T007): Backend Helm chart + validation  
→ Enables first Helm-deployed service on Minikube

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory structure for Helm charts

- [x] T001 Create charts directory structure at charts/todo-backend-chart/templates/ and charts/todo-frontend-chart/templates/

---

## Phase 2: User Story 1 - Deploy Backend to Local Kubernetes (Priority: P1) 🎯 MVP

**Goal**: Package and deploy FastAPI backend to Minikube using Helm with configurable settings

**Independent Test**: Run `helm install todo-backend ./charts/todo-backend-chart` on Minikube, verify pods running, access via port-forward on port 8000

### Implementation for User Story 1

- [x] T002 [US1] Create Chart.yaml with metadata (name: todo-backend-chart, version: 0.1.0, appVersion: 1.0.0) in charts/todo-backend-chart/Chart.yaml
- [x] T003 [US1] Create values.yaml with image, service, resources, env, secrets, and probes configuration in charts/todo-backend-chart/values.yaml
- [x] T004 [US1] Create deployment.yaml template with container spec, env vars, resource limits, liveness/readiness probes in charts/todo-backend-chart/templates/deployment.yaml
- [x] T005 [US1] Create service.yaml template with ClusterIP/NodePort support on port 8000 in charts/todo-backend-chart/templates/service.yaml
- [ ] T006 [US1] Validate backend chart with helm lint ./charts/todo-backend-chart (requires Helm CLI)
- [ ] T007 [US1] Verify backend chart renders valid YAML with helm template test ./charts/todo-backend-chart (requires Helm CLI)

**Checkpoint**: Backend chart should pass helm lint and be installable on Minikube

---

## Phase 3: User Story 2 - Deploy Frontend to Local Kubernetes (Priority: P1)

**Goal**: Package and deploy Next.js frontend to Minikube using Helm, configured to communicate with backend

**Independent Test**: Run `helm install todo-frontend ./charts/todo-frontend-chart` on Minikube, verify pods running, access via port-forward on port 3000

### Implementation for User Story 2

- [x] T008 [US2] Create Chart.yaml with metadata (name: todo-frontend-chart, version: 0.1.0, appVersion: 1.0.0) in charts/todo-frontend-chart/Chart.yaml
- [x] T009 [US2] Create values.yaml with image, service, resources, env (NEXT_PUBLIC_API_URL), and probes configuration in charts/todo-frontend-chart/values.yaml
- [x] T010 [US2] Create deployment.yaml template with container spec, env vars, resource limits, liveness/readiness probes in charts/todo-frontend-chart/templates/deployment.yaml
- [x] T011 [US2] Create service.yaml template with ClusterIP/NodePort support on port 3000 in charts/todo-frontend-chart/templates/service.yaml
- [ ] T012 [US2] Validate frontend chart with helm lint ./charts/todo-frontend-chart (requires Helm CLI)
- [ ] T013 [US2] Verify frontend chart renders valid YAML with helm template test ./charts/todo-frontend-chart (requires Helm CLI)

**Checkpoint**: Frontend chart should pass helm lint and be installable on Minikube

---

## Phase 4: User Story 3 - Configure Application via Helm Values (Priority: P2)

**Goal**: Enable configuration customization (replicas, image tags, env vars) without template modification

**Independent Test**: Modify values.yaml, run `helm upgrade`, verify configuration changes applied

### Implementation for User Story 3

- [x] T014 [US3] Verify backend values.yaml supports replicaCount override in charts/todo-backend-chart/values.yaml
- [x] T015 [US3] Verify backend values.yaml supports image.tag override in charts/todo-backend-chart/values.yaml
- [x] T016 [US3] Verify backend deployment template correctly references secretKeyRef for OPENROUTER_API_KEY in charts/todo-backend-chart/templates/deployment.yaml
- [x] T017 [US3] Verify frontend values.yaml supports replicaCount and image.tag overrides in charts/todo-frontend-chart/values.yaml
- [ ] T018 [US3] Test configuration override with helm template --set replicaCount=2 ./charts/todo-backend-chart (requires Helm CLI)

**Checkpoint**: Both charts should support all configurable parameters from values.yaml

---

## Phase 5: User Story 4 - Upgrade and Rollback Deployments (Priority: P3)

**Goal**: Enable Helm release lifecycle management with upgrade and rollback capabilities

**Independent Test**: Run `helm upgrade` with new values, then `helm rollback` to previous revision

### Implementation for User Story 4

- [x] T019 [US4] Document helm upgrade command syntax in specs/009-helm-charts/quickstart.md
- [x] T020 [US4] Document helm rollback command syntax in specs/009-helm-charts/quickstart.md
- [ ] T021 [US4] Verify helm history command shows release revisions (requires Helm CLI + running cluster)

**Checkpoint**: Upgrade and rollback workflow documented and functional

---

## Phase 6: Polish & Documentation

**Purpose**: Documentation updates for deployment workflow

- [x] T022 [P] Update README.md with Helm deployment section including prerequisites, install, upgrade, uninstall commands
- [x] T023 [P] Document Minikube Docker environment setup (eval $(minikube docker-env)) in README.md
- [x] T024 [P] Document Kubernetes secret creation for OPENROUTER_API_KEY in README.md
- [x] T025 [P] Document port-forward commands for accessing services in README.md
- [x] T026 Add troubleshooting section to README.md for common issues (image not found, secret missing, port conflict)
- [ ] T027 Run quickstart.md validation to ensure all commands work (requires Helm CLI + Minikube)
- [x] T028 Add Minikube Docker environment setup to README: `eval $(minikube docker-env)` so images are available locally
- [ ] T029 Verify Helm charts pass `helm lint` with no warnings (requires Helm CLI)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup (T001) completion
- **User Story 2 (Phase 3)**: Depends on Setup (T001) completion - CAN run parallel with US1
- **User Story 3 (Phase 4)**: Depends on US1 and US2 (T002-T013) completion
- **User Story 4 (Phase 5)**: Depends on US1 and US2 completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Backend chart - No dependencies on other stories
- **User Story 2 (P1)**: Frontend chart - No dependencies on other stories (can parallel with US1)
- **User Story 3 (P2)**: Configuration - Depends on US1 and US2 charts existing
- **User Story 4 (P3)**: Lifecycle - Depends on US1 and US2 charts being installable

### Within Each User Story

- Chart.yaml before values.yaml
- values.yaml before templates
- deployment.yaml before service.yaml (convention, can be parallel)
- Templates before lint validation
- Lint before template validation

### Parallel Opportunities

- **US1 and US2 can run in parallel**: Different chart directories, no dependencies
- **T022-T025**: All documentation tasks can run in parallel (different sections)
- **T004 and T005**: Backend templates can be created in parallel
- **T010 and T011**: Frontend templates can be created in parallel

---

## Parallel Example: User Stories 1 & 2 (Backend and Frontend Charts)

```bash
# These two user stories can be implemented in parallel:

# Developer A - User Story 1 (Backend Chart):
Task: "Create Chart.yaml in charts/todo-backend-chart/Chart.yaml"
Task: "Create values.yaml in charts/todo-backend-chart/values.yaml"
Task: "Create deployment.yaml in charts/todo-backend-chart/templates/deployment.yaml"
Task: "Create service.yaml in charts/todo-backend-chart/templates/service.yaml"

# Developer B - User Story 2 (Frontend Chart) - AT THE SAME TIME:
Task: "Create Chart.yaml in charts/todo-frontend-chart/Chart.yaml"
Task: "Create values.yaml in charts/todo-frontend-chart/values.yaml"
Task: "Create deployment.yaml in charts/todo-frontend-chart/templates/deployment.yaml"
Task: "Create service.yaml in charts/todo-frontend-chart/templates/service.yaml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: User Story 1 - Backend Chart (T002-T007)
3. **STOP and VALIDATE**: Run `helm lint` and `helm install --dry-run`
4. Test on Minikube with `helm install todo-backend ./charts/todo-backend-chart`

### Incremental Delivery

1. Complete Setup → Directory structure ready
2. Add User Story 1 (Backend Chart) → Validate with lint → Install on Minikube (MVP!)
3. Add User Story 2 (Frontend Chart) → Validate with lint → Install on Minikube
4. Add User Story 3 (Configuration) → Test with --set overrides
5. Add User Story 4 (Lifecycle) → Document upgrade/rollback
6. Add Documentation → README update

### Parallel Team Strategy

With two developers:

1. Team completes Setup (T001) together
2. Once Setup is done:
   - Developer A: User Story 1 (Backend Chart) - T002-T007
   - Developer B: User Story 2 (Frontend Chart) - T008-T013
3. Both charts complete → Continue with US3, US4, and Polish

---

## Summary

| Phase | User Story | Tasks | Parallel | Files |
|-------|------------|-------|----------|-------|
| 1 | Setup | 1 | - | charts/ directories |
| 2 | US1 - Backend | 6 | Some | 4 chart files |
| 3 | US2 - Frontend | 6 | Some | 4 chart files |
| 4 | US3 - Config | 5 | Some | Verify existing |
| 5 | US4 - Lifecycle | 3 | - | Documentation |
| 6 | Polish | 6 | Most | README.md |

**Total Tasks**: 27
**MVP Tasks** (US1 only): 7 (T001-T007)
**Parallel Opportunities**: US1/US2 can run together, documentation tasks parallel

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Validate charts with `helm lint` before proceeding to next phase
- Stop at any checkpoint to validate story independently
