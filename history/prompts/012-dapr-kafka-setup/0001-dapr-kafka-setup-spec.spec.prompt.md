---
id: 0001
title: "Dapr Kafka Setup Spec Creation"
stage: spec
date_iso: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: dapr-kafka-setup
branch: 012-dapr-kafka-setup
user: maryam
command: "sp.specify Dapr + Kafka Setup on Minikube (Phase V – Spec 2)"
labels: ["spec", "dapr", "kafka", "minikube", "event-streaming"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/012-dapr-kafka-setup/spec.md"
  - "specs/012-dapr-kafka-setup/checklists/requirements.md"
tests_yaml:
  - "spec quality checklist validated"
prompt_text: |
  Dapr + Kafka Setup on Minikube (Phase V – Spec 2)

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
  - Troubleshooting notes (Dapr sidecar crash, Kafka connection fail)
response_text: |
  Created comprehensive specification for Dapr + Kafka setup on Minikube, including:
  - User stories covering Dapr installation, event streaming infrastructure, Dapr-Kafka integration, sidecar injection, and additional components
  - Functional requirements (FR-001 to FR-014) detailing all necessary capabilities
  - Key entities definition for Dapr Runtime, Redpanda, Event Topics, Application Pods, and Dapr Components
  - Success criteria (SC-001 to SC-008) with measurable outcomes for deployment, connectivity, and functionality
  - Quality checklist to validate specification completeness
outcome: |
  Successfully created feature specification for Dapr + Kafka setup on Minikube in branch 012-dapr-kafka-setup with complete user scenarios, requirements, and success criteria.
evaluation: |
  The specification is comprehensive and ready for the planning phase (/sp.plan). All user requirements have been translated into testable functional requirements with clear acceptance scenarios.
---
