# Tasks: Dapr + Kafka Setup on Minikube

## Feature Overview
Implementation of Dapr (Distributed Application Runtime) with Redpanda (Kafka-compatible) on Minikube to enable event-driven architecture. This includes installing Dapr runtime, deploying Redpanda as a single-node container, configuring Dapr components (pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes), updating Helm charts with Dapr sidecar injection, and creating documentation for local setup and verification.

## Dependencies & Execution Order
1. **Phase 1 (Setup)**: Project initialization and environment preparation
2. **Phase 2 (Foundational)**: Install Dapr and Redpanda infrastructure
3. **Phase 3 (US1)**: Dapr Runtime Installation and verification
4. **Phase 4 (US2)**: Event Streaming Infrastructure (Redpanda deployment)
5. **Phase 5 (US3)**: Dapr-Kafka Integration (pubsub component)
6. **Phase 6 (US4)**: Application Sidecar Injection
7. **Phase 7 (US5)**: Additional Dapr Components (state, bindings, secrets)
8. **Phase 8 (US6)**: End-to-End Verification
9. **Phase 9 (Polish)**: Documentation and troubleshooting notes

## Parallel Execution Opportunities
- **US2 (Redpanda)** can run in parallel with Dapr installation preparation
- **US5 (Additional Components)** can run in parallel with US3 (pubsub) and US4 (sidecar injection)
- **Documentation tasks** can run in parallel with infrastructure setup

**MVP Scope (Core Deliverable)**  
Phase 1–5 (T001–T031): Dapr runtime + Redpanda + pub/sub integration  
→ Enables basic event-driven flow locally on Minikube

---

## Phase 1: Setup

### Goal
Initialize project structure and prepare environment for Dapr + Kafka setup.

- [X] T001 Create infrastructure directory structure at `.infrastructure/dapr/components/`, `.infrastructure/redpanda/`, and `.infrastructure/helm/todo-backend-chart/templates/`
- [X] T002 Verify prerequisites: Minikube, kubectl, Dapr CLI, Helm 3+ are installed and accessible
- [ ] T002 Note: Use minikube start --memory=2048 --cpus=2 (2GB RAM is sufficient for Phase IV/V)
- [X] T003 [P] Create placeholder files for all required Dapr component configurations

---

## Phase 2: Foundational

### Goal
Install and verify Dapr runtime and Redpanda infrastructure.

- [X] T004 Start Minikube cluster if not already running
- [X] T005 Install Dapr on Minikube using `dapr init -k` command
- [X] T006 Verify Dapr installation with `dapr status -k` command
- [X] T007 [P] Create Redpanda deployment YAML file at `.infrastructure/redpanda/deployment.yaml`
- [X] T008 [P] Create Redpanda service YAML file at `.infrastructure/redpanda/service.yaml`
- [X] T009 Deploy Redpanda to Minikube cluster
- [X] T010 Wait for Redpanda pods to be ready and operational

---

## Phase 3: [US1] Dapr Runtime Installation

### Goal
Complete Dapr runtime installation and verify all control plane components are healthy.

### Independent Test Criteria
Dapr control plane components are running and healthy in the cluster without requiring Kafka or other components.

- [X] T011 [US1] Verify Dapr control plane components (operator, placement, sentry, dashboard) are deployed
- [X] T012 [US1] Check that all Dapr components show as HEALTHY using `dapr status -k`
- [X] T013 [US1] Verify Dapr dashboard is accessible
- [X] T014 [US1] Test basic Dapr functionality with `dapr list` command
- [X] T015 [US1] Document Dapr installation verification process

---

## Phase 4: [US2] Event Streaming Infrastructure

### Goal
Deploy Redpanda as a Kafka-compatible event streaming platform and verify it's operational.

### Independent Test Criteria
Create topics and publish/consume messages directly through Redpanda, delivering event streaming capabilities without Dapr integration initially.

- [X] T016 [US2] Deploy Redpanda deployment to Minikube cluster
- [X] T017 [US2] Deploy Redpanda service to expose broker port 9092
- [X] T018 [US2] Verify Redpanda pods are operational and accessible within the cluster
- [X] T019 [US2] Test direct connection to Redpanda broker from within cluster
- [X] T020 [US2] Create initial Kafka topics: task-events, reminders, task-updates
- [X] T021 [US2] Verify topics are successfully created and ready for use
- [X] T022 [US2] Test publish and consume messages directly to Redpanda topics
- [X] T023 [US2] Verify consumers can successfully read messages from topics

---

## Phase 5: [US3] Dapr-Kafka Integration

### Goal
Configure Dapr's pub/sub component to connect to Redpanda for standardized event handling.

### Independent Test Criteria
Configure the Dapr pub/sub component and use Dapr's HTTP API to publish and consume messages, delivering standardized event handling without requiring other Dapr components.

- [X] T024 [US3] Create pubsub Kafka component configuration at `.infrastructure/dapr/components/pubsub-kafka.yaml`
- [X] T025 [US3] Apply pubsub Kafka component configuration to cluster
- [X] T026 [US3] Verify pubsub component connects to Redpanda and creates required topics
- [X] T027 [US3] Test event publishing via Dapr HTTP API to Redpanda topic
- [X] T028 [US3] Verify event appears in appropriate Redpanda topic
- [X] T029 [US3] Test event subscription via Dapr HTTP API from Redpanda topic
- [X] T030 [US3] Confirm events received without direct Kafka client usage
- [X] T031 [US3] Validate event schemas match defined formats

---

## Phase 6: [US4] Application Sidecar Injection

### Goal
Enable automatic Dapr sidecar injection in application pods for transparent integration.

### Independent Test Criteria
Deploy applications with Dapr annotations and verify sidecar injection occurs, delivering transparent integration with Dapr services.

- [X] T032 [US4] Locate existing Phase IV Helm charts for todo-backend
- [X] T033 [US4] Update Helm deployment template with Dapr annotations
- [X] T034 [US4] Add `dapr.io/enabled: "true"` annotation to deployment
- [X] T035 [US4] Add `dapr.io/app-id: "todo-backend"` annotation to deployment
- [X] T036 [US4] Add `dapr.io/app-port: "8000"` annotation to deployment
- [X] T037 [US4] Deploy updated application with Dapr annotations
- [X] T038 [US4] Verify daprd sidecar is automatically injected into pod
- [X] T039 [US4] Confirm both application container and Dapr sidecar are operational
- [X] T040 [US4] Test Dapr sidecar communication with application

---

## Phase 7: [US5] Additional Dapr Components

### Goal
Configure additional Dapr building blocks (state store, cron bindings, secret store) for complete solution.

### Independent Test Criteria
Configure each component separately and use their respective APIs, delivering individual building block functionality without requiring others.

- [X] T041 [US5] Create PostgreSQL state component configuration at `.infrastructure/dapr/components/state-postgresql.yaml`
- [X] T042 [US5] Apply state PostgreSQL component configuration to cluster
- [X] T043 [US5] Test Dapr state management using PostgreSQL backend
- [X] T044 [US5] Verify Dapr can store and retrieve state using PostgreSQL
- [X] T045 [US5] Create cron binding component configuration at `.infrastructure/dapr/components/bindings-cron.yaml`
- [X] T046 [US5] Apply cron binding component configuration to cluster
- [X] T047 [US5] Test scheduled task execution via cron binding
- [X] T048 [US5] Verify tasks execute according to defined schedule
- [X] T049 [US5] Create Kubernetes secret store component configuration at `.infrastructure/dapr/components/secretstores-kubernetes.yaml`
- [X] T050 [US5] Apply secret store component configuration to cluster
- [X] T051 [US5] Store OPENROUTER_API_KEY in Kubernetes secret
- [ ] T051 Note: Store OPENROUTER_API_KEY in Kubernetes secret and access via Dapr secret store – no hard-coding
- [X] T052 [US5] Test Dapr secret retrieval via secret API
- [X] T053 [US5] Verify Dapr can securely retrieve API key through secret API
- [X] T054 [US5] Enable Dapr service invocation between applications
- [X] T055 [US5] Verify all configured Dapr components show as healthy in status checks

---

## Phase 8: [US6] End-to-End Verification

### Goal
Verify the complete Dapr + Kafka setup works end-to-end for integrated system validation.

### Independent Test Criteria
Run a complete publish-subscribe workflow with real events, delivering confidence in the integrated system.

- [X] T056 [US6] Create test event with proper schema for task-events topic
- [X] T057 [US6] Publish test event through Dapr API to task-events topic
- [X] T058 [US6] Verify consumer application receives and processes the event
- [X] T059 [US6] Test complete workflow: app → Dapr → Kafka → Dapr → consumer app
- [X] T060 [US6] Run 10 consecutive publish/subscribe tests to verify reliability
- [X] T061 [US6] Verify 95% success rate over the 10 consecutive tests
- [X] T062 [US6] Test all three Kafka topics (task-events, reminders, task-updates) with sample events
- [X] T063 [US6] Verify all Dapr building blocks work together cohesively
- [X] T064 [US6] Document end-to-end verification results and metrics
- [X] T064 Note: Verify Dapr metrics endpoint<a href="http://localhost:3500/metrics" target="_blank" rel="noopener noreferrer nofollow"></a> returns data

---

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Complete documentation and add troubleshooting capabilities for production readiness.

- [X] T065 Update README with comprehensive setup instructions for Minikube + Dapr + Redpanda
- [X] T066 Add verification commands section to documentation (dapr status, publish/subscribe test)
- [X] T067 Create troubleshooting notes for common issues (sidecar crashes, Kafka connection failures)
- [X] T068 Document expected timeframes: Dapr installation (5 min), Redpanda startup (3 min), topic creation (1 min)
- [X] T069 Create quick reference guide for common Dapr and Redpanda operations
- [X] T070 Verify all deliverables from requirements are completed and documented
- [X] T071 Perform final verification that setup can be completed within 30 minutes as specified
- [X] T072 Create backup and recovery procedures for Dapr + Redpanda setup
- [X] T073 Document security considerations for Dapr secret management and service communication

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)
Focus on User Story 1 (Dapr Runtime Installation) and User Story 2 (Event Streaming Infrastructure) as the core foundation. This delivers the essential infrastructure for event-driven architecture.

### Incremental Delivery
1. **Phase 1-3**: Dapr runtime installation and verification
2. **Phase 4**: Redpanda deployment and basic Kafka functionality
3. **Phase 5**: Dapr-Kafka integration
4. **Phase 6-9**: Complete the remaining user stories with additional components and verification

### Success Metrics
- All Dapr control plane components operational within 5 minutes (SC-001)
- Redpanda single-node deployment ready within 3 minutes (SC-002)
- All 3 Kafka topics created within 1 minute of Redpanda readiness (SC-003)
- Dapr pubsub connects to Redpanda within 2 minutes of configuration (SC-004)
- 100% success rate for Dapr sidecar injection (SC-005)
- 95% success rate for publish/subscribe tests (SC-006)
- Setup completed within 30 minutes (SC-007)
- All Dapr components show as healthy (SC-008)