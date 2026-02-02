# Implementation Plan: Dapr + Kafka Setup on Minikube

**Branch**: `012-dapr-kafka-setup` | **Date**: 2026-01-30 | **Spec**: [Dapr + Kafka Setup on Minikube](./spec.md)
**Input**: Feature specification from `/specs/012-dapr-kafka-setup/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of Dapr (Distributed Application Runtime) with Redpanda (Kafka-compatible) on Minikube to enable event-driven architecture. This includes installing Dapr runtime, deploying Redpanda as a single-node container, configuring Dapr components (pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes), updating Helm charts with Dapr sidecar injection, and creating documentation for local setup and verification.

## Technical Context

**Language/Version**: N/A (Infrastructure/Deployment Configuration)
**Primary Dependencies**: Dapr (v1.13+), Redpanda (single-node Docker), Kafka protocol, Helm charts, Minikube
**Storage**: Neon Serverless PostgreSQL (external) accessed via Dapr state management
**Testing**: kubectl commands, dapr CLI verification, publish/subscribe tests, pod status checks
**Target Platform**: Minikube (local Kubernetes), Kubernetes cluster
**Project Type**: Infrastructure/Deployment
**Performance Goals**: Dapr control plane components operational within 5 minutes, Redpanda ready within 3 minutes, all 3 Kafka topics created within 1 minute, 95% success rate for publish/subscribe tests
**Constraints**: Local Minikube only (no cloud yet), single-node Redpanda (no Zookeeper), no production hardening (focus on functionality), reuse Phase IV Helm charts with Dapr annotations
**Scale/Scope**: Single developer environment, 3 Kafka topics (task-events, reminders, task-updates), Dapr sidecar injection for all application pods

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

1. **SDD Compliance (Core Principle I)**: ✓ Plan implements SDD workflow from spec to tasks to implementation
2. **Progressive Evolution (Core Principle II)**: ✓ Builds on Phase IV Helm charts and extends to event-driven architecture
3. **Security First (Core Principle IV)**: ✓ Uses Dapr secret stores for OPENROUTER_API_KEY, maintains JWT authentication
4. **Stateless Design (Core Principle V)**: ✓ Dapr state management with PostgreSQL, no in-memory state
5. **Cloud-Native (Core Principle VI)**: ✓ Kubernetes-native Dapr deployment, Helm chart updates
6. **Technology Stack Compliance**: ✓ Uses Dapr + Redpanda as specified in constitution for Phase V
7. **Event Topics Compliance**: ✓ Creates required topics: task-events, reminders, task-updates
8. **Dapr Building Blocks**: ✓ Implements pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes

## Project Structure

### Documentation (this feature)

```text
specs/012-dapr-kafka-setup/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Infrastructure/Deployment Structure
.infrastructure/
├── dapr/
│   ├── components/
│   │   ├── pubsub-kafka.yaml
│   │   ├── state-postgresql.yaml
│   │   ├── bindings-cron.yaml
│   │   └── secretstores-kubernetes.yaml
│   └── config/
│       └── config.yaml
├── redpanda/
│   ├── deployment.yaml
│   └── service.yaml
└── helm/
    └── todo-backend-chart/
        └── templates/
            └── deployment.yaml  # Updated with Dapr annotations

# Existing application code remains unchanged
backend/
├── src/
└── tests/

frontend/
├── src/
└── tests/
```

**Structure Decision**: Infrastructure/deployment configuration for Dapr + Redpanda on Minikube. New configuration files added to implement event-driven architecture while maintaining compatibility with existing application structure. Dapr annotations added to existing Helm charts to enable sidecar injection.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
