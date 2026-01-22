# Research: Helm Charts for Todo AI Chatbot

**Feature**: 009-helm-charts
**Date**: 2026-01-21
**Phase**: 0 (Research)

## Research Summary

This document captures research findings and decisions for implementing Helm charts for the Todo AI Chatbot application.

---

## R1: Helm Chart Structure Best Practices

### Decision
Use minimal Helm chart structure with only essential files: Chart.yaml, values.yaml, templates/deployment.yaml, templates/service.yaml.

### Rationale
- Spec explicitly states "Charts must be minimal & valid"
- No Helm hooks or CRDs required
- Keeps charts simple and maintainable for local Minikube deployment
- Easier to understand for developers new to Helm

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Full chart with helpers, NOTES.txt, tests | Over-engineering for local dev; adds maintenance burden |
| Umbrella chart combining both services | Increases coupling; spec requires separate charts |
| Include ingress.yaml | Explicitly out of scope (Phase V) |

---

## R2: Docker Image References

### Decision
Reference local images built via Minikube's Docker environment:
- Backend: `todo-backend:latest`
- Frontend: `todo-frontend:latest`

### Rationale
- Existing Dockerfiles from Spec 1 (008-docker-containerization) already define image builds
- Using Minikube's Docker daemon avoids need for remote registry
- `latest` tag acceptable for local development; configurable via values.yaml

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Use Docker Hub public images | Requires registry push; adds complexity for local dev |
| Use ghcr.io images | Requires GitHub Container Registry setup |
| Hardcode specific tags | Less flexible; values.yaml should allow overrides |

---

## R3: Service Type Configuration

### Decision
Default to ClusterIP with optional NodePort support via values.yaml.

### Rationale
- ClusterIP is standard for internal cluster communication
- Port-forward works with ClusterIP (kubectl port-forward)
- NodePort available for direct Minikube access if needed
- No LoadBalancer (requires cloud provider)

### Configuration

```yaml
# values.yaml
service:
  type: ClusterIP  # or NodePort
  port: 8000       # backend
  nodePort: null   # Optional, only for NodePort type
```

---

## R4: Secret Management for OPENROUTER_API_KEY

### Decision
Reference external Kubernetes Secret; do not include secret values in Helm chart.

### Rationale
- Spec states "OPENROUTER_API_KEY as secret"
- Secrets should never be committed to Git
- Users create secret manually or via kubectl before helm install
- Chart references secretKeyRef in deployment

### Implementation Pattern

```yaml
# values.yaml
secrets:
  openRouterApiKey:
    secretName: "todo-backend-secrets"
    secretKey: "OPENROUTER_API_KEY"

# templates/deployment.yaml
env:
  - name: OPENROUTER_API_KEY
    valueFrom:
      secretKeyRef:
        name: {{ .Values.secrets.openRouterApiKey.secretName }}
        key: {{ .Values.secrets.openRouterApiKey.secretKey }}
```

### Secret Creation Command
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-api-key>
```

---

## R5: Environment Variable Injection

### Decision
Support two patterns: direct values and secretKeyRef.

### Rationale
- Non-sensitive vars (DATABASE_URL, ports) can be in values.yaml
- Sensitive vars (API keys) reference Kubernetes Secrets
- Flexible configuration for different environments

### Implementation

```yaml
# values.yaml
env:
  DATABASE_URL: "postgresql://..."  # Direct value
  ENVIRONMENT: "production"

# Secrets handled via secretKeyRef pattern (see R4)
```

---

## R6: Health Probes Configuration

### Decision
Configure readiness and liveness probes matching existing Docker health checks.

### Rationale
- Backend already has `/health` endpoint (from Dockerfile)
- Frontend uses Node.js server on port 3000
- Probes ensure pods are only scheduled when ready
- Constitution requires "Readiness and liveness probes configured"

### Backend Probes
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

### Frontend Probes
```yaml
livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 30

readinessProbe:
  tcpSocket:
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

## R7: Resource Limits

### Decision
Define conservative resource limits suitable for Minikube.

### Rationale
- Minikube typically has limited resources (4GB RAM, 2 CPUs)
- Constitution requires "Resource limits and requests defined"
- Prevents resource contention during local development

### Configuration
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

---

## R8: Chart Versioning

### Decision
Use semantic versioning starting at 0.1.0.

### Rationale
- User specified "Chart version: 0.1.0"
- Pre-1.0 indicates initial development phase
- appVersion matches Docker image version concept

### Chart.yaml Pattern
```yaml
apiVersion: v2
name: todo-backend-chart
version: 0.1.0
appVersion: "1.0.0"
```

---

## R9: Directory Structure

### Decision
Place charts under `charts/` directory at repository root.

### Rationale
- User specified: `charts/todo-backend-chart/` and `charts/todo-frontend-chart/`
- Consistent with common Helm repository patterns
- Separate from existing `helm/` structure in constitution (allows flexibility)

### Structure
```
charts/
├── todo-backend-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       └── service.yaml
└── todo-frontend-chart/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        └── service.yaml
```

---

## R10: Frontend-Backend Communication

### Decision
Frontend references backend via Kubernetes service DNS name.

### Rationale
- Within cluster: `http://todo-backend:8000`
- Standard Kubernetes service discovery
- No need for external URLs in cluster-internal communication

### Configuration
```yaml
# frontend values.yaml
env:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
```

---

## Research Complete

All NEEDS CLARIFICATION items resolved. Ready to proceed to Phase 1 (Design & Contracts).
