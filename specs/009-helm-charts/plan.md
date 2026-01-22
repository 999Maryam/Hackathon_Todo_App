# Implementation Plan: Helm Charts for Todo AI Chatbot

**Branch**: `009-helm-charts` | **Date**: 2026-01-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-helm-charts/spec.md`

## Summary

Create two minimal Helm charts (todo-backend-chart and todo-frontend-chart) to package the Todo AI Chatbot Phase III applications for local Kubernetes deployment on Minikube. Charts will be configurable via values.yaml and support ClusterIP/NodePort services with health probes.

## Technical Context

**Language/Version**: YAML (Helm templates), Kubernetes API v1/apps/v1
**Primary Dependencies**: Helm 3.x, kubectl, Minikube, Docker
**Storage**: N/A (charts deploy to existing Neon PostgreSQL via env vars)
**Testing**: helm lint, helm template, helm install --dry-run
**Target Platform**: Local Minikube cluster (Docker driver)
**Project Type**: Infrastructure-as-Code (Helm charts)
**Performance Goals**: Pods reach Running state within 120 seconds
**Constraints**: No cloud-specific settings, no Ingress, no Helm hooks, no CRDs
**Scale/Scope**: 2 charts, ~4 files each, local development target

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Following /specify → /plan → /tasks → /implement workflow |
| II. Progressive Evolution | ✅ PASS | Builds on Phase III app (008-docker-containerization) |
| III. Reusable Intelligence | ✅ PASS | Charts are parameterized for reuse via values.yaml |
| IV. Security First | ✅ PASS | Secrets handled via K8s Secret reference, not in values |
| V. Stateless & Resilient | ✅ PASS | Charts deploy stateless containers, DB external |
| VI. Cloud-Native Mindset | ✅ PASS | Helm charts, health probes, resource limits defined |
| VII. AI-Native Focus | N/A | Not applicable to Helm charts |
| VIII. Maintainability | ✅ PASS | Task IDs will be added to chart files |

### Phase IV Specific Checks

| Requirement | Status | Notes |
|-------------|--------|-------|
| Helm Charts | ✅ PASS | Creating todo-backend-chart and todo-frontend-chart |
| Parameterized values.yaml | ✅ PASS | Full configuration externalization |
| ConfigMaps | ⚠️ OPTIONAL | Using env vars in values.yaml (simpler approach) |
| Secrets reference | ✅ PASS | secretKeyRef for OPENROUTER_API_KEY |
| Resource limits | ✅ PASS | Defined in values.yaml |
| Readiness/liveness probes | ✅ PASS | Configured for both charts |
| Helm lint passes | ✅ PASS | Validation requirement met |

## Project Structure

### Documentation (this feature)

```text
specs/009-helm-charts/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # Configuration entities
├── quickstart.md        # Deployment guide
├── contracts/           # Chart contracts
│   ├── backend-chart.yaml
│   └── frontend-chart.yaml
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
charts/
├── todo-backend-chart/
│   ├── Chart.yaml           # Chart metadata
│   ├── values.yaml          # Default configuration
│   └── templates/
│       ├── deployment.yaml  # Kubernetes Deployment
│       └── service.yaml     # Kubernetes Service
└── todo-frontend-chart/
    ├── Chart.yaml           # Chart metadata
    ├── values.yaml          # Default configuration
    └── templates/
        ├── deployment.yaml  # Kubernetes Deployment
        └── service.yaml     # Kubernetes Service
```

**Structure Decision**: Using dedicated `charts/` directory at repository root as specified in requirements. This separates Helm charts from application code while keeping them in the same repository.

## Complexity Tracking

No constitutional violations requiring justification. Implementation follows minimal chart approach as specified.

---

## Implementation Phases

### Phase 1: Backend Chart Creation

**Tasks**:
1. Create `charts/todo-backend-chart/` directory structure
2. Write `Chart.yaml` with metadata (name, version 0.1.0, appVersion 1.0.0)
3. Write `values.yaml` with all configurable parameters
4. Write `templates/deployment.yaml` with pod spec, env vars, probes
5. Write `templates/service.yaml` with ClusterIP/NodePort support
6. Validate with `helm lint`

**Acceptance Criteria**:
- `helm lint ./charts/todo-backend-chart` passes
- `helm template test ./charts/todo-backend-chart` renders valid YAML
- Deployment includes health probes, resource limits, env vars
- Service exposes port 8000

### Phase 2: Frontend Chart Creation

**Tasks**:
1. Create `charts/todo-frontend-chart/` directory structure
2. Write `Chart.yaml` with metadata
3. Write `values.yaml` with frontend-specific parameters
4. Write `templates/deployment.yaml` with frontend pod spec
5. Write `templates/service.yaml`
6. Validate with `helm lint`

**Acceptance Criteria**:
- `helm lint ./charts/todo-frontend-chart` passes
- `helm template test ./charts/todo-frontend-chart` renders valid YAML
- Deployment includes health probes, resource limits, env vars
- Service exposes port 3000
- NEXT_PUBLIC_API_URL defaults to backend service DNS

### Phase 3: Integration Testing

**Tasks**:
1. Create Kubernetes secret for OPENROUTER_API_KEY
2. Install backend chart with `helm install todo-backend`
3. Install frontend chart with `helm install todo-frontend`
4. Verify pods reach Running state
5. Test port-forward access to both services
6. Verify upgrade and rollback functionality

**Acceptance Criteria**:
- Both charts install successfully
- Pods reach Running state within 120 seconds
- Services accessible via port-forward
- helm upgrade and rollback work correctly

### Phase 4: Documentation

**Tasks**:
1. Update root README.md with Helm deployment instructions
2. Document prerequisite setup (Minikube, Docker env, secrets)
3. Include helm install/upgrade/uninstall commands
4. Add troubleshooting section

**Acceptance Criteria**:
- README includes complete Helm deployment workflow
- Commands are copy-paste ready
- Minikube setup documented

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Chart structure | Minimal (4 files each) | Spec requires minimal charts |
| Service type | ClusterIP (default) | Port-forward preferred for local dev |
| Secret handling | External K8s Secret reference | Never store secrets in chart values |
| Health probes | HTTP GET /health (backend), TCP/HTTP (frontend) | Match existing Docker health checks |
| Resource limits | 128Mi-512Mi memory, 100m-500m CPU | Suitable for Minikube resources |
| Chart version | 0.1.0 | Pre-release version for initial development |

---

## Risk Analysis

| Risk | Mitigation |
|------|------------|
| Image not found in Minikube | Document `eval $(minikube docker-env)` requirement |
| Secret missing causes pod crash | Document secret creation in README and quickstart |
| Port conflict during port-forward | Document alternative port options |
| Helm version incompatibility | Require Helm 3.x, use apiVersion: v2 |

---

## Next Steps

1. Run `/sp.tasks` to generate actionable task list
2. Implement using `helm-chart-builder` agent
3. Test on Minikube cluster
4. Update README with deployment instructions

---

## Related Artifacts

- [Specification](./spec.md)
- [Research](./research.md)
- [Data Model](./data-model.md)
- [Quickstart](./quickstart.md)
- [Backend Chart Contract](./contracts/backend-chart.yaml)
- [Frontend Chart Contract](./contracts/frontend-chart.yaml)
