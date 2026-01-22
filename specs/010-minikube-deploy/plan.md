# Implementation Plan: Minikube Deployment & AI-Assisted K8s Operations

**Branch**: `010-minikube-deploy` | **Date**: 2026-01-22 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/010-minikube-deploy/spec.md`

## Summary

Deploy the Todo AI Chatbot application (Phase III) to a local Minikube Kubernetes cluster using the existing Docker images (Spec 1) and Helm charts (Spec 2). The primary deliverables are documentation: README updates with complete deployment workflow, kubectl-ai/kagent usage examples, and troubleshooting guide. No new application code is required.

## Technical Context

**Language/Version**: Bash/Shell (documentation and commands), Minikube 1.30+, Helm 3.x, kubectl 1.28+
**Primary Dependencies**: Minikube (Docker driver), Helm charts (todo-backend-chart, todo-frontend-chart), kubectl-ai or kagent
**Storage**: N/A (applications use external Neon PostgreSQL)
**Testing**: Manual verification via kubectl commands, curl health checks, browser testing
**Target Platform**: Local Minikube cluster on Linux/macOS/Windows (Docker driver)
**Project Type**: Documentation-focused (no source code changes)
**Performance Goals**: Cluster ready in <180s, pods running in <120s, services accessible within 10s of port-forward
**Constraints**: Local only (no cloud), reuse existing artifacts (no Dockerfile/Helm chart modifications)
**Scale/Scope**: Single-node Minikube cluster, 2 deployments (frontend + backend), 1 secret

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Following /specify → /plan → /tasks → /implement workflow |
| II. Progressive Evolution | PASS | Phase IV builds on Phase III without breaking changes |
| III. Reusable Intelligence | PASS | Documentation patterns can be reused for Phase V cloud deployment |
| IV. Security First | PASS | Secrets managed via Kubernetes Secrets, no hardcoded credentials |
| V. Stateless & Resilient | PASS | Containers are stateless, external Neon DB for persistence |
| VI. Cloud-Native Mindset | PASS | Using Minikube, Helm, kubectl-ai per constitution Phase IV requirements |
| VII. AI-Native Focus | PASS | kubectl-ai/kagent demonstrates AI-assisted operations |
| VIII. Maintainability | PASS | Documentation includes Task ID references and spec links |

**Phase IV Specific Gates:**
| Requirement | Status | Notes |
|-------------|--------|-------|
| Docker Containerization | PASS | Using images from Spec 1 (008-docker-containerization) |
| Helm Charts | PASS | Using charts from Spec 2 (009-helm-charts) |
| Minikube Cluster | PASS | Docker driver, 4GB memory, 2 CPUs per constitution |
| AI Operations | PASS | kubectl-ai for manifest generation, kagent for health checks |

## Project Structure

### Documentation (this feature)

```text
specs/010-minikube-deploy/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: kubectl-ai/kagent research
├── data-model.md        # Phase 1 output: Kubernetes resource relationships
├── quickstart.md        # Phase 1 output: Quick deploy guide
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
# Documentation deliverables (new/updated files)
README.md                       # Updated with Minikube deployment section
docs/
└── troubleshooting/
    └── minikube.md             # Common issues and solutions

# Existing artifacts (referenced, not modified)
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

backend/
└── Dockerfile                  # From Spec 1

frontend/
└── Dockerfile                  # From Spec 1
```

**Structure Decision**: Documentation-only feature. Primary output is README update and troubleshooting guide. No application source code changes required.

## Complexity Tracking

No violations. This is a documentation-focused feature that reuses existing artifacts.

---

## Phase 0: Research Summary

### R1: Minikube Driver Selection

**Decision**: Docker driver (default)
**Rationale**: Most compatible across Linux/macOS/Windows, fastest startup, aligns with constitution recommendation
**Alternatives Considered**:
- VirtualBox: Slower startup, additional installation required
- Hyperkit (macOS): Platform-specific
- Hyper-V (Windows): Requires Pro/Enterprise edition

### R2: kubectl-ai Tool Selection

**Decision**: kubectl-ai as primary, kagent as alternative
**Rationale**: kubectl-ai has broader adoption and simpler installation (single binary). kagent provides more interactive experience but requires additional setup.
**Installation**:
```bash
# kubectl-ai (recommended)
brew install kubectl-ai  # macOS
# or download binary from https://github.com/sozercan/kubectl-ai/releases

# kagent (alternative)
pip install kagent
```

### R3: Image Loading Strategy

**Decision**: Use `eval $(minikube docker-env)` to build images directly in Minikube's Docker daemon
**Rationale**: Eliminates need for registry, fastest workflow, no network transfer
**Alternatives Considered**:
- `minikube image load`: Works but slower for large images
- Local registry addon: Additional complexity not needed for local dev

### R4: Secret Management

**Decision**: Manual secret creation via `kubectl create secret generic`
**Rationale**: Simple, explicit, and documented. No external secret management tools required.
**Secret Name**: `todo-backend-secrets` (matches Helm chart values.yaml)

### R5: Namespace Strategy

**Decision**: Default namespace
**Rationale**: Simplest for local development. Namespace isolation not required for single-developer Minikube clusters.
**Alternatives Considered**:
- Custom `todo-app` namespace: Additional kubectl context complexity

---

## Phase 1: Design Artifacts

### 1.1 Deployment Workflow

```
1. Prerequisites
   └── minikube, helm, kubectl, docker installed

2. Cluster Setup
   ├── minikube start --driver=docker --memory=4096 --cpus=2
   └── minikube status (verify)

3. Docker Environment
   ├── eval $(minikube docker-env)
   ├── docker build -t todo-backend:latest ./backend
   └── docker build -t todo-frontend:latest ./frontend

4. Secrets Creation
   └── kubectl create secret generic todo-backend-secrets \
       --from-literal=OPENROUTER_API_KEY=<key> \
       --from-literal=DATABASE_URL=<url> \
       --from-literal=BETTER_AUTH_SECRET=<secret>

5. Helm Deployment
   ├── helm install todo-backend ./charts/todo-backend-chart --dry-run (validate)
   ├── helm install todo-backend ./charts/todo-backend-chart
   ├── helm install todo-frontend ./charts/todo-frontend-chart --dry-run (validate)
   └── helm install todo-frontend ./charts/todo-frontend-chart

6. Verification
   ├── kubectl get pods (wait for Running)
   ├── kubectl get services
   └── kubectl port-forward svc/todo-backend 8000:8000 &

7. Access Application
   ├── kubectl port-forward svc/todo-frontend 3000:3000 &
   ├── curl http://localhost:8000/health → {"status":"ok"}
   └── Browser: http://localhost:3000

8. AI-Assisted Operations
   ├── kubectl-ai "show all pods" → kubectl get pods
   └── kubectl-ai "check why pod is failing" → diagnostic commands
```

### 1.2 Kubernetes Resource Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Minikube Cluster                         │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  default namespace                      │ │
│  │                                                         │ │
│  │  ┌─────────────────────┐    ┌─────────────────────┐   │ │
│  │  │   todo-backend      │    │   todo-frontend     │   │ │
│  │  │   Deployment        │    │   Deployment        │   │ │
│  │  │   ┌─────────────┐   │    │   ┌─────────────┐   │   │ │
│  │  │   │ Pod (1)     │   │    │   │ Pod (1)     │   │   │ │
│  │  │   │ :8000       │   │    │   │ :3000       │   │   │ │
│  │  │   └──────┬──────┘   │    │   └──────┬──────┘   │   │ │
│  │  └──────────┼──────────┘    └──────────┼──────────┘   │ │
│  │             │                          │               │ │
│  │  ┌──────────▼──────────┐    ┌──────────▼──────────┐   │ │
│  │  │  Service: ClusterIP │    │  Service: ClusterIP │   │ │
│  │  │  todo-backend:8000  │◄───│  todo-frontend:3000 │   │ │
│  │  └─────────────────────┘    └─────────────────────┘   │ │
│  │                                                         │ │
│  │  ┌─────────────────────┐                               │ │
│  │  │  Secret             │                               │ │
│  │  │  todo-backend-      │──► Referenced by backend pod  │ │
│  │  │  secrets            │                               │ │
│  │  └─────────────────────┘                               │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ▲                                   │
│                          │ port-forward                      │
│              ┌───────────┴───────────┐                      │
│              │ localhost:3000 (UI)   │                      │
│              │ localhost:8000 (API)  │                      │
│              └───────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
            ┌─────────────────────────┐
            │  External Neon DB       │
            │  (PostgreSQL)           │
            └─────────────────────────┘
```

### 1.3 kubectl-ai Usage Examples

**Example 1: Check Cluster Health**
```bash
$ kubectl-ai "show me all pods and their status"
# Translates to: kubectl get pods -o wide
NAME                             READY   STATUS    RESTARTS   AGE
todo-backend-6d4f5b8c9-x2k3j     1/1     Running   0          5m
todo-frontend-7c8d9e0f1-y4m5n    1/1     Running   0          4m
```

**Example 2: Diagnose Pod Issues**
```bash
$ kubectl-ai "why is my backend pod failing"
# Translates to: kubectl describe pod <pod-name> + kubectl logs <pod-name>
# Output: Shows events, container status, and recent logs
```

**Example 3: Scale Deployment**
```bash
$ kubectl-ai "scale backend to 2 replicas"
# Translates to: kubectl scale deployment todo-backend --replicas=2
deployment.apps/todo-backend scaled
```

### 1.4 Troubleshooting Matrix

| Issue | Symptom | Command to Diagnose | Solution |
|-------|---------|---------------------|----------|
| Minikube won't start | "Exiting due to DRV_AS_ROOT" | `minikube start --driver=docker` | Don't run as root, or use `--force` |
| Pods stuck in ImagePullBackOff | `kubectl get pods` shows ImagePullBackOff | `kubectl describe pod <name>` | Run `eval $(minikube docker-env)` before build |
| Pod CrashLoopBackOff | Pod keeps restarting | `kubectl logs <pod-name>` | Check secrets exist, DATABASE_URL valid |
| Port already in use | "bind: address already in use" | `lsof -i :3000` | Kill process or use different port |
| Service not accessible | curl timeout | `kubectl get svc` | Verify service exists, check port-forward |
| Missing secrets | CreateContainerConfigError | `kubectl get secrets` | Create secret with required keys |
| Insufficient resources | Pod pending | `kubectl describe pod <name>` | Increase Minikube memory: `minikube stop && minikube start --memory=6144` |

---

## Implementation Tasks Preview

The following tasks will be generated by `/sp.tasks`:

1. **T1**: Create Minikube quickstart section in README
2. **T2**: Document Docker image build commands (Minikube context)
3. **T3**: Document secret creation commands
4. **T4**: Document Helm install commands with dry-run examples
5. **T5**: Document port-forward and verification commands
6. **T6**: Document kubectl-ai/kagent examples with output
7. **T7**: Create troubleshooting guide (docs/troubleshooting/minikube.md)
8. **T8**: Update README with complete deployment flow
9. **T9**: Test and verify complete workflow on Minikube

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Minikube resource constraints | Medium | High | Document minimum requirements (4GB, 2 CPU) |
| Docker driver compatibility | Low | Medium | Provide alternative driver instructions |
| kubectl-ai not installed | Medium | Low | Document as optional, provide manual alternatives |
| External DB connectivity | Medium | High | Document DATABASE_URL format, test connection |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Execute tasks to create documentation deliverables
3. Test complete workflow on Minikube
4. Create PHR documenting the implementation
