# Research: Dapr + Kafka Setup on Minikube

## Overview
This research document addresses all technical decisions and unknowns required for implementing the Dapr + Kafka setup on Minikube feature. It consolidates findings from various sources and best practices to guide the implementation.

## Decision Log

### 1. Dapr Installation Method
- **Decision**: Use `dapr init -k` for cluster-wide installation
- **Rationale**: This is the official Dapr CLI command for installing Dapr on Kubernetes clusters. It handles all control plane components (operator, placement, sentry, dashboard) automatically.
- **Alternatives considered**:
  - Manual YAML deployment - more complex and error-prone
  - Helm chart installation - also valid but CLI method is simpler for dev environments

### 2. Redpanda Deployment Strategy
- **Decision**: Deploy Redpanda as a single-node container in Minikube
- **Rationale**: Aligns with constraints (single-node, no Zookeeper) and serves as a Kafka-compatible event streaming platform for local development
- **Alternatives considered**:
  - Full Kafka with Zookeeper - more complex setup, violates constraint
  - Cloud Kafka service - violates "local Minikube only" constraint

### 3. Kafka Topics Configuration
- **Decision**: Create three topics: task-events, reminders, task-updates
- **Rationale**: Matches requirements from spec and constitution for Phase V event-driven architecture
- **Topic details**:
  - task-events: For task lifecycle events (CRUD operations)
  - reminders: For scheduled reminder events
  - task-updates: For real-time task change notifications

### 4. Dapr Component Types
- **Decision**: Implement four core Dapr building blocks:
  - pubsub.kafka: Connect to Redpanda for event streaming
  - state.postgresql: Connect to Neon DB for state management
  - bindings.cron: For scheduled reminder checks
  - secretstores.kubernetes: For OPENROUTER_API_KEY access
- **Rationale**: These components fulfill all requirements from the spec and align with constitution's Dapr building blocks section

### 5. Helm Chart Modification Approach
- **Decision**: Update existing Phase IV Helm charts with Dapr annotations
- **Rationale**: Follows progressive evolution principle (builds on Phase IV) and maintains backward compatibility
- **Annotations to add**:
  - `dapr.io/enabled: "true"`
  - `dapr.io/app-id: "todo-backend"`
  - `dapr.io/app-port: "8000"` (assuming FastAPI backend port)

### 6. Service Discovery and Communication
- **Decision**: Use Dapr service invocation for inter-service communication
- **Rationale**: Constitution specifies service invocation should be enabled, and it provides built-in features like mTLS, retries, and circuit breakers

### 7. Secret Management
- **Decision**: Store OPENROUTER_API_KEY in Kubernetes secret and access via Dapr secret store
- **Rationale**: Follows security best practices and aligns with constitution's secret management requirements

### 8. Cron Binding Schedule
- **Decision**: Configure cron binding to trigger every 5 minutes (`*/5 * * * *`)
- **Rationale**: Matches requirements in spec for scheduled reminder checks
- **Alternative considered**: Different intervals - 5 minutes balances timely reminders with resource usage

## Technical Architecture

### Dapr Control Plane Components
- **Operator**: Manages Dapr runtime lifecycle
- **Placement**: Handles actor placement (if actors are used)
- **Sentry**: Handles mTLS certificate rotation
- **Dashboard**: Web UI for Dapr observability

### Redpanda Configuration
- **Broker Port**: 9092 (standard Kafka port)
- **Single-node**: Simplified for local development
- **Topics**: Created automatically by Dapr pubsub component

### Integration Points
1. Application publishes events via Dapr HTTP API
2. Dapr pubsub component forwards to Redpanda
3. Consumers receive events via Dapr HTTP API from Redpanda
4. State stored/retrieved via Dapr state management
5. Secrets accessed via Dapr secret store
6. Scheduled tasks handled via Dapr cron bindings

## Implementation Order
1. Install Dapr on Minikube (`dapr init -k`)
2. Deploy Redpanda container (deployment + service)
3. Create Dapr component configurations
4. Update Helm charts with Dapr annotations
5. Deploy updated application
6. Test event flow and verify all components

## Security Considerations
- Use Dapr's built-in mTLS for service-to-service communication
- Store secrets in Kubernetes and access via Dapr secret store
- Maintain JWT-based authentication for user requests
- Ensure proper namespace isolation in Minikube

## Dependencies
- Dapr CLI (latest stable version)
- kubectl
- Minikube
- Helm (for chart updates)
- Existing Phase IV Helm charts