# Data Model: Helm Charts for Todo AI Chatbot

**Feature**: 009-helm-charts
**Date**: 2026-01-21
**Phase**: 1 (Design)

## Overview

This document defines the data structures and configuration entities for the Helm charts. Unlike traditional database data models, Helm charts deal with Kubernetes resource definitions and configuration values.

---

## Entity: Helm Chart (Backend)

### Chart Metadata (Chart.yaml)

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| apiVersion | string | Helm API version | Must be "v2" |
| name | string | Chart name | "todo-backend-chart" |
| version | string | Chart version | Semver format (0.1.0) |
| appVersion | string | App version | "1.0.0" |
| description | string | Chart description | Non-empty |
| type | string | Chart type | "application" |

### Configuration Values (values.yaml)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| replicaCount | integer | 1 | Number of pod replicas |
| image.repository | string | "todo-backend" | Docker image name |
| image.tag | string | "latest" | Image tag |
| image.pullPolicy | string | "IfNotPresent" | Kubernetes pull policy |
| service.type | string | "ClusterIP" | Service type |
| service.port | integer | 8000 | Service port |
| service.nodePort | integer | null | NodePort (optional) |
| resources.requests.memory | string | "128Mi" | Memory request |
| resources.requests.cpu | string | "100m" | CPU request |
| resources.limits.memory | string | "512Mi" | Memory limit |
| resources.limits.cpu | string | "500m" | CPU limit |
| env.DATABASE_URL | string | "" | Database connection string |
| env.ENVIRONMENT | string | "production" | Environment name |
| secrets.openRouterApiKey.secretName | string | "todo-backend-secrets" | K8s secret name |
| secrets.openRouterApiKey.secretKey | string | "OPENROUTER_API_KEY" | Key in secret |
| probes.liveness.path | string | "/health" | Liveness probe path |
| probes.liveness.port | integer | 8000 | Liveness probe port |
| probes.readiness.path | string | "/health" | Readiness probe path |
| probes.readiness.port | integer | 8000 | Readiness probe port |

---

## Entity: Helm Chart (Frontend)

### Chart Metadata (Chart.yaml)

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| apiVersion | string | Helm API version | Must be "v2" |
| name | string | Chart name | "todo-frontend-chart" |
| version | string | Chart version | Semver format (0.1.0) |
| appVersion | string | App version | "1.0.0" |
| description | string | Chart description | Non-empty |
| type | string | Chart type | "application" |

### Configuration Values (values.yaml)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| replicaCount | integer | 1 | Number of pod replicas |
| image.repository | string | "todo-frontend" | Docker image name |
| image.tag | string | "latest" | Image tag |
| image.pullPolicy | string | "IfNotPresent" | Kubernetes pull policy |
| service.type | string | "ClusterIP" | Service type |
| service.port | integer | 3000 | Service port |
| service.nodePort | integer | null | NodePort (optional) |
| resources.requests.memory | string | "128Mi" | Memory request |
| resources.requests.cpu | string | "100m" | CPU request |
| resources.limits.memory | string | "256Mi" | Memory limit |
| resources.limits.cpu | string | "300m" | CPU limit |
| env.NEXT_PUBLIC_API_URL | string | "http://todo-backend:8000" | Backend API URL |
| probes.liveness.path | string | "/" | Liveness probe path |
| probes.liveness.port | integer | 3000 | Liveness probe port |
| probes.readiness.port | integer | 3000 | Readiness probe port (TCP) |

---

## Entity: Kubernetes Deployment

### Backend Deployment Resource

| Field | K8s Path | Source | Description |
|-------|----------|--------|-------------|
| name | metadata.name | Release name | Deployment identifier |
| namespace | metadata.namespace | Release namespace | K8s namespace |
| replicas | spec.replicas | values.replicaCount | Pod replicas |
| image | spec.template.spec.containers[0].image | values.image | Container image |
| containerPort | spec.template.spec.containers[0].ports[0] | 8000 | App port |
| env | spec.template.spec.containers[0].env | values.env + secrets | Environment vars |
| resources | spec.template.spec.containers[0].resources | values.resources | Resource limits |
| livenessProbe | spec.template.spec.containers[0].livenessProbe | values.probes | Health check |
| readinessProbe | spec.template.spec.containers[0].readinessProbe | values.probes | Ready check |

### Frontend Deployment Resource

| Field | K8s Path | Source | Description |
|-------|----------|--------|-------------|
| name | metadata.name | Release name | Deployment identifier |
| namespace | metadata.namespace | Release namespace | K8s namespace |
| replicas | spec.replicas | values.replicaCount | Pod replicas |
| image | spec.template.spec.containers[0].image | values.image | Container image |
| containerPort | spec.template.spec.containers[0].ports[0] | 3000 | App port |
| env | spec.template.spec.containers[0].env | values.env | Environment vars |
| resources | spec.template.spec.containers[0].resources | values.resources | Resource limits |
| livenessProbe | spec.template.spec.containers[0].livenessProbe | values.probes | Health check |
| readinessProbe | spec.template.spec.containers[0].readinessProbe | values.probes | Ready check |

---

## Entity: Kubernetes Service

### Service Resource (Both Charts)

| Field | K8s Path | Source | Description |
|-------|----------|--------|-------------|
| name | metadata.name | Release name | Service identifier |
| type | spec.type | values.service.type | ClusterIP or NodePort |
| port | spec.ports[0].port | values.service.port | Service port |
| targetPort | spec.ports[0].targetPort | Container port | Pod port |
| nodePort | spec.ports[0].nodePort | values.service.nodePort | Node port (optional) |
| selector | spec.selector | App labels | Pod selector |

---

## Entity: Kubernetes Secret (External)

The secret is created externally (not by Helm chart). Chart references it.

| Field | Description | Example |
|-------|-------------|---------|
| metadata.name | Secret name | "todo-backend-secrets" |
| type | Secret type | Opaque |
| data.OPENROUTER_API_KEY | API key (base64) | Provided by user |

### Creation Command
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-api-key>
```

---

## Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                          │
│                                                                 │
│  ┌─────────────────────┐       ┌─────────────────────┐         │
│  │  todo-backend       │       │  todo-frontend      │         │
│  │  (Helm Release)     │       │  (Helm Release)     │         │
│  │                     │       │                     │         │
│  │  ┌───────────────┐  │       │  ┌───────────────┐  │         │
│  │  │  Deployment   │  │       │  │  Deployment   │  │         │
│  │  │  - Pod(s)     │  │◄──────│  │  - Pod(s)     │  │         │
│  │  └───────────────┘  │  API  │  └───────────────┘  │         │
│  │         ▲           │  Call │         ▲           │         │
│  │         │           │       │         │           │         │
│  │  ┌───────────────┐  │       │  ┌───────────────┐  │         │
│  │  │   Service     │  │       │  │   Service     │  │         │
│  │  │ :8000         │  │       │  │ :3000         │  │         │
│  │  └───────────────┘  │       │  └───────────────┘  │         │
│  └─────────────────────┘       └─────────────────────┘         │
│           ▲                                                     │
│           │                                                     │
│  ┌───────────────────┐                                         │
│  │   Secret          │                                         │
│  │ todo-backend-     │                                         │
│  │ secrets           │                                         │
│  └───────────────────┘                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                    │                    │
                    ▼                    ▼
              kubectl port-forward  kubectl port-forward
              svc/todo-backend      svc/todo-frontend
              8000:8000             3000:3000
                    │                    │
                    ▼                    ▼
              localhost:8000       localhost:3000
```

---

## State Transitions

Helm charts don't have traditional state, but Helm releases do:

| State | Description | Transition |
|-------|-------------|------------|
| Not Installed | Chart exists, no release | `helm install` → Deployed |
| Deployed | Release active, pods running | `helm upgrade` → Deployed |
| Failed | Install/upgrade failed | Fix issue → retry install/upgrade |
| Superseded | Old release replaced | Automatic on upgrade |
| Uninstalled | Release removed | `helm uninstall` from Deployed |

---

## Validation Rules

### Chart.yaml
- `apiVersion` must be "v2" (Helm 3)
- `version` must be valid semver
- `name` must match directory name
- `type` should be "application"

### values.yaml
- `replicaCount` must be positive integer
- `image.repository` must be non-empty
- `service.port` must be 1-65535
- `service.type` must be "ClusterIP" or "NodePort"
- `resources.requests` must not exceed `resources.limits`

### Templates
- Must pass `helm lint`
- Must render valid YAML via `helm template`
- Must reference existing values correctly
