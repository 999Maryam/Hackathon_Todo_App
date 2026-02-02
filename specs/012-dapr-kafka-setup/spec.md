# Feature Specification: Dapr + Kafka Setup on Minikube

**Feature Branch**: `012-dapr-kafka-setup`
**Created**: 2026-01-30
**Status**: Draft
**Input**: User description: " Dapr + Kafka Setup on Minikube (Phase V – Spec 2)

Target audience: Developers adding distributed runtime and event-driven architecture locally

Focus:
- Install and configure Dapr on Minikube with full building blocks
- Deploy Redpanda (Kafka-compatible) as a container inside Minikube
- Bridge Kafka events with Dapr Pub/Sub for seamless integration

Success criteria:
- Dapr sidecars injected in all pods (deployment/service level)
- Dapr components deployed and healthy:
  - pubsub.kafka (connected to Redpanda)
  - state.postgresql (Neon DB or local Postgres)
  - bindings.cron (scheduled reminders)
  - secretstores.kubernetes (OPENROUTER_API_KEY)
  - service-invocation enabled
- Redpanda running in Minikube with topics: task-events, reminders, task-updates
- App publishes/receives events via Dapr HTTP API (no direct Kafka client)
- Local verification: publish test event → consumer receives it

Constraints:
- Local Minikube only (no cloud yet)
- Reuse Phase IV Helm charts (add Dapr annotations/sidecar)
- Redpanda single-node Docker container (no Zookeeper)
- No production hardening (security, HA) – focus on functionality
- Use OPENROUTER_API_KEY via Dapr secret store

Deliverables:
- Dapr installation commands (`dapr init -k`)
- Redpanda deployment YAML (deployment + service)
- Dapr component YAML files (pubsub, state, bindings, secrets)
- Updated Helm deployment.yaml (Dapr sidecar injection)
- Verification commands (dapr status, publish/subscribe test)
- README update: Minikube + Dapr + Redpanda setup guide
- Troubleshooting notes (Dapr sidecar crash, Kafka connection fail)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dapr Runtime Installation (Priority: P1)

As a developer, I want to install and configure Dapr on my local Minikube cluster so that I can leverage distributed runtime capabilities for my applications.

**Why this priority**: This is foundational - without Dapr installed and configured, none of the other features can work. It provides the core infrastructure needed for all other distributed capabilities.

**Independent Test**: Can be fully tested by verifying Dapr control plane components are running and healthy in the cluster, delivering distributed runtime capabilities without requiring Kafka or other components.

**Acceptance Scenarios**:

1. **Given** a local Minikube cluster is running, **When** I run Dapr installation commands, **Then** Dapr control plane components (daprd, placement, operator) are deployed and operational in the cluster
2. **Given** Dapr is installed, **When** I check Dapr status, **Then** all Dapr components show as healthy and ready

---

### User Story 2 - Event Streaming Infrastructure (Priority: P1)

As a developer, I want to deploy a Kafka-compatible event streaming platform (Redpanda) within my Minikube cluster so that I can handle asynchronous events and messaging between services.

**Why this priority**: This is the core messaging infrastructure that enables event-driven architecture. Without this, the pub/sub functionality cannot work.

**Independent Test**: Can be fully tested by creating topics and publishing/consuming messages directly through Redpanda, delivering event streaming capabilities without Dapr integration initially.

**Acceptance Scenarios**:

1. **Given** Minikube cluster is running, **When** I deploy Redpanda, **Then** Redpanda pods are operational and accessible within the cluster
2. **Given** Redpanda is deployed, **When** I create event topics (task-events, reminders, task-updates), **Then** topics are successfully created and ready for use
3. **Given** topics exist, **When** I publish a test message to a topic, **Then** consumers can successfully read the message

---

### User Story 3 - Dapr-Kafka Integration (Priority: P1)

As a developer, I want to configure Dapr's pub/sub component to connect to Redpanda so that my applications can publish and subscribe to events through Dapr's standardized API without direct Kafka client dependencies.

**Why this priority**: This bridges the gap between Dapr's abstractions and the underlying Kafka infrastructure, providing the primary value proposition of simplified event-driven development.

**Independent Test**: Can be fully tested by configuring the Dapr pub/sub component and using Dapr's HTTP API to publish and consume messages, delivering standardized event handling without requiring other Dapr components.

**Acceptance Scenarios**:

1. **Given** Dapr and Redpanda are running, **When** I configure the pubsub.kafka component, **Then** Dapr can successfully connect to Redpanda and create the required topics
2. **Given** pubsub component is configured, **When** I publish an event via Dapr HTTP API, **Then** the event appears in the appropriate Redpanda topic
3. **Given** events exist in topics, **When** I subscribe to events via Dapr HTTP API, **Then** I receive the published events without direct Kafka client usage

---

### User Story 4 - Application Sidecar Injection (Priority: P2)

As a developer, I want Dapr sidecars automatically injected into my application pods so that my applications can seamlessly integrate with Dapr's building blocks without code changes.

**Why this priority**: This enables existing applications to leverage Dapr capabilities with minimal changes, providing practical value for integrating with legacy or existing services.

**Independent Test**: Can be fully tested by deploying applications with Dapr annotations and verifying sidecar injection occurs, delivering transparent integration with Dapr services.

**Acceptance Scenarios**:

1. **Given** Dapr is installed with sidecar injector enabled, **When** I deploy an application with Dapr annotations, **Then** the daprd sidecar is automatically injected into the pod
2. **Given** application with sidecar is running, **When** I check pod status, **Then** both application container and Dapr sidecar are operational

---

### User Story 5 - Additional Dapr Components (Priority: P2)

As a developer, I want to configure additional Dapr components (state store, cron bindings, secret store) so that my applications can leverage multiple Dapr building blocks for a complete microservices solution.

**Why this priority**: These components provide essential infrastructure for state management, scheduled tasks, and secure secret handling, enhancing the overall distributed system capabilities.

**Independent Test**: Can be fully tested by configuring each component separately and using their respective APIs, delivering individual building block functionality without requiring others.

**Acceptance Scenarios**:

1. **Given** PostgreSQL is available, **When** I configure the state.postgresql component, **Then** Dapr can store and retrieve state using PostgreSQL
2. **Given** OPENROUTER_API_KEY exists, **When** I configure the secretstore component, **Then** Dapr can securely retrieve the API key through its secret API
3. **Given** cron binding is configured, **When** I set up scheduled tasks, **Then** tasks execute according to the defined schedule

---

### User Story 6 - End-to-End Verification (Priority: P3)

As a developer, I want to verify the complete Dapr + Kafka setup works end-to-end so that I can confirm the integrated system functions as expected for real-world scenarios.

**Why this priority**: This validates that all components work together as intended, ensuring the complete solution delivers the promised value.

**Independent Test**: Can be fully tested by running a complete publish-subscribe workflow with real events, delivering confidence in the integrated system.

**Acceptance Scenarios**:

1. **Given** complete setup is configured, **When** I publish a test event through Dapr API, **Then** a consumer application receives and processes the event successfully
2. **Given** test event is processed, **When** I verify the complete workflow, **Then** all components (app → Dapr → Kafka → Dapr → consumer app) function correctly

---

### Edge Cases

- What happens when Redpanda becomes temporarily unavailable during event publishing?
- How does the system handle high-volume event publishing that might overwhelm the Kafka broker?
- What occurs when Dapr sidecar fails to inject into an application pod?
- How does the system behave when network partitions occur between Dapr sidecars and the control plane?
- What happens when the configured event topics already exist with different configurations?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST install Dapr runtime components in Minikube cluster using `dapr init -k` command
- **FR-002**: System MUST deploy Redpanda as a single-node container within the Minikube cluster
- **FR-003**: System MUST create three Kafka topics: task-events, reminders, and task-updates
- **FR-004**: System MUST configure Dapr pubsub.kafka component to connect to the deployed Redpanda instance
- **FR-005**: Applications MUST be able to publish events to Kafka topics using Dapr HTTP API without direct Kafka client dependencies
- **FR-006**: Applications MUST be able to subscribe to events from Kafka topics using Dapr HTTP API
- **FR-007**: System MUST support automatic Dapr sidecar injection in application pods via Helm chart annotations
- **FR-008**: System MUST configure state.postgresql component connected to Neon DB or local Postgres
- **FR-009**: System MUST configure bindings.cron component for scheduled reminders functionality
- **FR-010**: System MUST configure secretstores.kubernetes component to securely access OPENROUTER_API_KEY
- **FR-011**: System MUST enable Dapr service invocation between applications in the cluster
- **FR-012**: System MUST provide verification commands to test the complete publish/subscribe workflow
- **FR-013**: System MUST update documentation with setup instructions for Minikube + Dapr + Redpanda
- **FR-014**: System MUST include troubleshooting notes for common issues (sidecar crashes, Kafka connection failures)

### Key Entities

- **Dapr Runtime**: Distributed application runtime that provides building blocks for microservices, deployed as control plane components and application sidecars
- **Redpanda**: Kafka-compatible event streaming platform deployed as a container in the cluster to handle pub/sub messaging
- **Event Topics**: Named channels (task-events, reminders, task-updates) where applications publish and subscribe to events
- **Application Pods**: Containerized applications that integrate with Dapr through sidecar injection and HTTP API usage
- **Dapr Components**: Configurable building blocks (pubsub, state store, bindings, secrets) that extend application capabilities

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dapr control plane components are successfully deployed and operational in Minikube within 5 minutes of running installation commands
- **SC-002**: Redpanda single-node deployment becomes ready and available within 3 minutes of deployment
- **SC-003**: All three required Kafka topics (task-events, reminders, task-updates) are created and accessible within 1 minute of Redpanda becoming ready
- **SC-004**: Dapr pubsub.kafka component successfully connects to Redpanda and can publish/subscribe to events within 2 minutes of configuration
- **SC-005**: Application pods with Dapr annotations successfully receive automatically injected sidecars with 100% success rate
- **SC-006**: End-to-end publish/subscribe test completes successfully with 95% success rate over 10 consecutive tests
- **SC-007**: Developers can complete the entire setup process following documentation within 30 minutes
- **SC-008**: All configured Dapr components (pubsub, state, bindings, secrets) show as healthy in Dapr status checks