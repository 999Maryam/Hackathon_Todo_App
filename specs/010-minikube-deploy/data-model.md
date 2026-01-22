# Data Model: Minikube Deployment Kubernetes Resources

**Feature**: 010-minikube-deploy
**Date**: 2026-01-22
**Purpose**: Document Kubernetes resource relationships for local deployment

---

## Overview

This feature doesn't introduce new database entities. Instead, it documents the Kubernetes resources and their relationships for deploying the Todo AI Chatbot to Minikube.

---

## Kubernetes Resource Model

### Resource Hierarchy

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Minikube Cluster                             │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                     default namespace                          │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │                    Deployments                           │  │ │
│  │  │  ┌─────────────────────┐  ┌─────────────────────┐       │  │ │
│  │  │  │ todo-backend        │  │ todo-frontend       │       │  │ │
│  │  │  │ replicas: 1         │  │ replicas: 1         │       │  │ │
│  │  │  │ image: todo-backend │  │ image: todo-frontend│       │  │ │
│  │  │  └─────────┬───────────┘  └─────────┬───────────┘       │  │ │
│  │  └────────────┼────────────────────────┼───────────────────┘  │ │
│  │               │                        │                       │ │
│  │  ┌────────────▼────────────────────────▼───────────────────┐  │ │
│  │  │                       Pods                               │  │ │
│  │  │  ┌─────────────────────┐  ┌─────────────────────┐       │  │ │
│  │  │  │ todo-backend-xxxxx  │  │ todo-frontend-xxxxx │       │  │ │
│  │  │  │ port: 8000          │  │ port: 3000          │       │  │ │
│  │  │  │ env: from Secret    │  │ env: from values    │       │  │ │
│  │  │  └─────────────────────┘  └─────────────────────┘       │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │                      Services                            │  │ │
│  │  │  ┌─────────────────────┐  ┌─────────────────────┐       │  │ │
│  │  │  │ todo-backend        │  │ todo-frontend       │       │  │ │
│  │  │  │ type: ClusterIP     │  │ type: ClusterIP     │       │  │ │
│  │  │  │ port: 8000          │  │ port: 3000          │       │  │ │
│  │  │  └─────────────────────┘  └─────────────────────┘       │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  │                                                                │ │
│  │  ┌─────────────────────────────────────────────────────────┐  │ │
│  │  │                      Secrets                             │  │ │
│  │  │  ┌─────────────────────────────────────────────┐        │  │ │
│  │  │  │ todo-backend-secrets                         │        │  │ │
│  │  │  │ keys:                                        │        │  │ │
│  │  │  │   - OPENROUTER_API_KEY                       │        │  │ │
│  │  │  │   - DATABASE_URL                             │        │  │ │
│  │  │  │   - BETTER_AUTH_SECRET                       │        │  │ │
│  │  │  └─────────────────────────────────────────────┘        │  │ │
│  │  └─────────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Resource Specifications

### 1. Deployment: todo-backend

**Source**: `charts/todo-backend-chart/templates/deployment.yaml`

| Property | Value | Source |
|----------|-------|--------|
| Name | todo-backend | Chart.yaml |
| Replicas | 1 | values.yaml |
| Image | todo-backend:latest | values.yaml |
| Container Port | 8000 | values.yaml |
| CPU Request | 100m | values.yaml |
| CPU Limit | 500m | values.yaml |
| Memory Request | 128Mi | values.yaml |
| Memory Limit | 512Mi | values.yaml |

**Environment Variables**:
| Variable | Source |
|----------|--------|
| DATABASE_URL | values.yaml.env |
| ENVIRONMENT | values.yaml.env |
| BETTER_AUTH_SECRET | values.yaml.env |
| OPENROUTER_API_KEY | Secret (todo-backend-secrets) |

**Health Probes**:
| Probe | Path | Port | Initial Delay | Period |
|-------|------|------|---------------|--------|
| Liveness | /health | 8000 | 5s | 30s |
| Readiness | /health | 8000 | 5s | 10s |

---

### 2. Deployment: todo-frontend

**Source**: `charts/todo-frontend-chart/templates/deployment.yaml`

| Property | Value | Source |
|----------|-------|--------|
| Name | todo-frontend | Chart.yaml |
| Replicas | 1 | values.yaml |
| Image | todo-frontend:latest | values.yaml |
| Container Port | 3000 | values.yaml |
| CPU Request | 100m | values.yaml |
| CPU Limit | 300m | values.yaml |
| Memory Request | 128Mi | values.yaml |
| Memory Limit | 256Mi | values.yaml |

**Environment Variables**:
| Variable | Value |
|----------|-------|
| NEXT_PUBLIC_API_URL | http://todo-backend:8000 |
| NODE_ENV | production |
| HOSTNAME | 0.0.0.0 |

**Health Probes**:
| Probe | Path | Port | Initial Delay | Period |
|-------|------|------|---------------|--------|
| Liveness | / | 3000 | 10s | 30s |
| Readiness | (TCP) | 3000 | 5s | 10s |

---

### 3. Service: todo-backend

**Source**: `charts/todo-backend-chart/templates/service.yaml`

| Property | Value |
|----------|-------|
| Name | todo-backend |
| Type | ClusterIP |
| Port | 8000 |
| Target Port | 8000 |
| Protocol | TCP |

**Selector**: Matches pods with label `app.kubernetes.io/name: todo-backend`

---

### 4. Service: todo-frontend

**Source**: `charts/todo-frontend-chart/templates/service.yaml`

| Property | Value |
|----------|-------|
| Name | todo-frontend |
| Type | ClusterIP |
| Port | 3000 |
| Target Port | 3000 |
| Protocol | TCP |

**Selector**: Matches pods with label `app.kubernetes.io/name: todo-frontend`

---

### 5. Secret: todo-backend-secrets

**Created Manually** (not via Helm)

| Key | Description |
|-----|-------------|
| OPENROUTER_API_KEY | API key for OpenRouter LLM service |
| DATABASE_URL | Neon PostgreSQL connection string |
| BETTER_AUTH_SECRET | JWT signing secret for authentication |

**Creation Command**:
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<key> \
  --from-literal=DATABASE_URL=<url> \
  --from-literal=BETTER_AUTH_SECRET=<secret>
```

---

## Resource Relationships

```
┌──────────────────┐     ┌──────────────────┐
│   Helm Release   │     │   Helm Release   │
│  todo-backend    │     │  todo-frontend   │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
    creates                  creates
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐
│   Deployment     │     │   Deployment     │
│  todo-backend    │     │  todo-frontend   │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
    manages                  manages
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐
│      Pod         │     │      Pod         │
│ todo-backend-xxx │     │todo-frontend-xxx │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
    references                connects to
         │                        │
         ▼                        ▼
┌──────────────────┐     ┌──────────────────┐
│     Secret       │     │    Service       │
│todo-backend-     │     │  todo-backend    │
│     secrets      │     │   :8000          │
└──────────────────┘     └──────────────────┘
```

---

## External Dependencies

### Neon PostgreSQL Database

| Property | Value |
|----------|-------|
| Type | External (not in cluster) |
| Connection | Via DATABASE_URL environment variable |
| Protocol | PostgreSQL (port 5432) |
| Network | Internet-accessible from Minikube |

**Connection Flow**:
```
Pod (todo-backend)
    → DATABASE_URL from Secret
    → External Neon PostgreSQL
    → Internet
```

---

## Label Strategy

All resources use Kubernetes recommended labels:

| Label | Value | Purpose |
|-------|-------|---------|
| app.kubernetes.io/name | todo-backend / todo-frontend | Resource identification |
| app.kubernetes.io/instance | {{ .Release.Name }} | Helm release tracking |
| app.kubernetes.io/version | {{ .Chart.AppVersion }} | Version tracking |
| app.kubernetes.io/managed-by | Helm | Tool identification |

---

## Resource Verification Commands

```bash
# List all deployments
kubectl get deployments

# List all pods
kubectl get pods

# List all services
kubectl get services

# List all secrets
kubectl get secrets

# Describe specific resource
kubectl describe deployment todo-backend
kubectl describe pod <pod-name>
kubectl describe service todo-frontend
kubectl describe secret todo-backend-secrets
```
