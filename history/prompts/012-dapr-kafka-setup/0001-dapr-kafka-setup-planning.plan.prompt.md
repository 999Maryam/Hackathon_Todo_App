---
id: 0001
title: "Dapr Kafka Setup Planning"
stage: plan
date_iso: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: dapr-kafka-setup
branch: 012-dapr-kafka-setup
user: maryam
command: "sp.plan Dapr + Kafka Setup on Minikube (Phase V – Spec 2)

Create:
- Dapr installation & verification on Minikube
- Redpanda single-container deployment in Minikube
- Dapr component YAMLs (pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes)
- Updated Helm charts with Dapr sidecar injection
- README section with setup & test commands

Decisions:
- Dapr version: latest stable (v1.13+)
- Redpanda: single-node Docker (no Zookeeper)
- Kafka topics: task-events, reminders, task-updates
- Dapr sidecar: injected via annotations in deployment.yaml
- State: postgresql (connect to Neon or local)
- Secrets: kubernetes secret store for OPENROUTER_API_KEY
- Bindings: cron for reminder checks (every 5 min)

Testing strategy:
- dapr init -k → dapr status -k (all components healthy)
- kubectl apply -f redpanda.yaml → kubectl get pods (redpanda running)
- kubectl apply -f dapr-components/ → dapr status -k
- Test Pub/Sub: dapr publish → dapr subscribe (event received)
- Test cron binding: wait 5 min → reminder event triggered
- Helm upgrade → pods show Dapr sidecar (2 containers)
- Verify app publishes event via Dapr API → Redpanda topic has message

Technical details & order:
1. minikube start (if not running)
2. dapr init -k (install Dapr on cluster)
3. Deploy Redpanda container (deployment + service YAML)
4. Create Dapr components YAML (pubsub, state, bindings, secrets)
5. Update Helm deployment.yaml (dapr.io/enabled: "true", dapr.io/app-id, etc.)
6. helm upgrade --install todo-backend charts/todo-backend-chart/
7. Test event flow (publish via curl to Dapr → check Redpanda)
8. Document in README: setup commands, verification, troubleshooting

Why critical:
- Enables event-driven architecture locally
- Prepares for cloud migration (Spec 3"
labels: ["plan", "dapr", "kafka", "minikube", "event-streaming", "pubsub"]
links:
  spec: "./spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/012-dapr-kafka-setup/plan.md"
  - "specs/012-dapr-kafka-setup/research.md"
  - "specs/012-dapr-kafka-setup/data-model.md"
  - "specs/012-dapr-kafka-setup/quickstart.md"
  - "specs/012-dapr-kafka-setup/contracts/dapr-pubsub-openapi.yaml"
  - "specs/012-dapr-kafka-setup/contracts/dapr-state-openapi.yaml"
  - "specs/012-dapr-kafka-setup/contracts/dapr-secrets-openapi.yaml"
tests_yaml:
  - "constitution check passed"
  - "research completed"
  - "data model defined"
  - "contracts created"
  - "quickstart guide written"
prompt_text: |
  Dapr + Kafka Setup on Minikube (Phase V – Spec 2)

  Create:
  - Dapr installation & verification on Minikube
  - Redpanda single-container deployment in Minikube
  - Dapr component YAMLs (pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes)
  - Updated Helm charts with Dapr sidecar injection
  - README section with setup & test commands

  Decisions:
  - Dapr version: latest stable (v1.13+)
  - Redpanda: single-node Docker (no Zookeeper)
  - Kafka topics: task-events, reminders, task-updates
  - Dapr sidecar: injected via annotations in deployment.yaml
  - State: postgresql (connect to Neon or local)
  - Secrets: kubernetes secret store for OPENROUTER_API_KEY
  - Bindings: cron for reminder checks (every 5 min)

  Testing strategy:
  - dapr init -k → dapr status -k (all components healthy)
  - kubectl apply -f redpanda.yaml → kubectl get pods (redpanda running)
  - kubectl apply -f dapr-components/ → dapr status -k
  - Test Pub/Sub: dapr publish → dapr subscribe (event received)
  - Test cron binding: wait 5 min → reminder event triggered
  - Helm upgrade → pods show Dapr sidecar (2 containers)
  - Verify app publishes event via Dapr API → Redpanda topic has message

  Technical details & order:
  1. minikube start (if not running)
  2. dapr init -k (install Dapr on cluster)
  3. Deploy Redpanda container (deployment + service YAML)
  4. Create Dapr components YAML (pubsub, state, bindings, secrets)
  5. Update Helm deployment.yaml (dapr.io/enabled: "true", dapr.io/app-id, etc.)
  6. helm upgrade --install todo-backend charts/todo-backend-chart/
  7. Test event flow (publish via curl to Dapr → check Redpanda)
  8. Document in README: setup commands, verification, troubleshooting

  Why critical:
  - Enables event-driven architecture locally
  - Prepares for cloud migration (Spec 3
response_text: |
  Completed comprehensive implementation plan for Dapr + Kafka Setup on Minikube, including:
  - Detailed implementation plan with technical context and constitution check
  - Research document covering all technical decisions and best practices
  - Data model defining entities and schemas for Dapr components
  - Quickstart guide with step-by-step setup instructions
  - API contracts for Dapr pubsub, state, and secrets building blocks
  - Agent context updated with new technologies
  All components align with the constitution and build on previous phases.
outcome: |
  Successfully created implementation plan for Dapr + Kafka setup on Minikube with all required artifacts: plan.md, research.md, data-model.md, quickstart.md, and API contracts for pubsub, state, and secrets building blocks.
evaluation: |
  The plan comprehensively covers all requirements from the spec, follows the constitution principles, and prepares for the next phase of implementation. All Dapr building blocks are properly defined with appropriate API contracts.
---