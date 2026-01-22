# Research: Minikube Deployment & AI-Assisted K8s Operations

**Feature**: 010-minikube-deploy
**Date**: 2026-01-22
**Purpose**: Resolve technical decisions for local Kubernetes deployment

---

## R1: Minikube Driver Selection

### Context
Minikube supports multiple drivers for virtualization. The choice affects startup time, compatibility, and available features.

### Decision
**Docker driver (default)**

### Rationale
- Most compatible across Linux/macOS/Windows
- Fastest startup time (~30-60 seconds)
- No additional hypervisor installation required
- Aligns with constitution Phase IV recommendation
- Works seamlessly with `eval $(minikube docker-env)`

### Alternatives Considered

| Driver | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| VirtualBox | Full VM isolation | Slower startup (2-3 min), additional install | Performance overhead |
| Hyperkit | Native macOS performance | macOS only | Platform-specific |
| Hyper-V | Native Windows | Windows Pro/Enterprise only | License restriction |
| Podman | Rootless containers | Less mature with Minikube | Complexity |

### Configuration
```bash
minikube start --driver=docker --memory=4096 --cpus=2
```

---

## R2: kubectl-ai Tool Selection

### Context
AI-assisted Kubernetes tools translate natural language to kubectl commands, improving developer experience.

### Decision
**kubectl-ai as primary, kagent as documented alternative**

### Rationale
- kubectl-ai: Single binary, broader adoption, simpler installation
- kagent: More interactive but requires Python environment
- Both meet the spec requirement for AI-assisted operations

### kubectl-ai Installation

**macOS (Homebrew)**:
```bash
brew tap sozercan/kubectl-ai
brew install kubectl-ai
```

**Linux/Windows (Binary)**:
```bash
# Download from https://github.com/sozercan/kubectl-ai/releases
# Add to PATH
chmod +x kubectl-ai
mv kubectl-ai /usr/local/bin/
```

**Configuration** (requires OpenAI API key):
```bash
export OPENAI_API_KEY=<your-key>
# or use local LLM with --backend flag
```

### kagent Installation (Alternative)

```bash
pip install kagent
kagent --help
```

### Comparison

| Feature | kubectl-ai | kagent |
|---------|------------|--------|
| Installation | Single binary | pip install |
| LLM Backend | OpenAI (configurable) | Multiple |
| Interactive | Yes | Yes |
| Offline | With local LLM | With local LLM |

---

## R3: Image Loading Strategy

### Context
Docker images built locally need to be accessible within the Minikube cluster.

### Decision
**Use `eval $(minikube docker-env)` to build directly in Minikube's Docker daemon**

### Rationale
- Eliminates need for image registry
- Fastest workflow (no network transfer)
- Images immediately available to Minikube pods
- Standard Minikube workflow

### Alternatives Considered

| Method | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| `minikube image load` | Works without env change | Slower, copies entire image | Performance |
| Local registry addon | Closer to production | Additional setup complexity | Overkill for local dev |
| External registry | Production-like | Requires network, auth | Out of scope |

### Usage
```bash
# Point Docker CLI to Minikube's daemon
eval $(minikube docker-env)

# Build images (now available inside Minikube)
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Verify images are in Minikube
minikube image ls | grep todo
```

### Important Notes
- Run `eval $(minikube docker-env)` in every new terminal session
- Images built in host Docker daemon are NOT automatically available
- Use `imagePullPolicy: IfNotPresent` or `Never` in Helm charts

---

## R4: Secret Management

### Context
The backend application requires sensitive environment variables (DATABASE_URL, OPENROUTER_API_KEY, BETTER_AUTH_SECRET).

### Decision
**Manual secret creation via `kubectl create secret generic`**

### Rationale
- Simple and explicit
- No external tools required
- Aligns with Helm chart configuration (secretName: "todo-backend-secrets")
- Secrets are not committed to Git

### Implementation
```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-openrouter-api-key> \
  --from-literal=DATABASE_URL=<your-neon-database-url> \
  --from-literal=BETTER_AUTH_SECRET=<your-auth-secret>
```

### Verification
```bash
kubectl get secret todo-backend-secrets -o yaml
# Verify keys exist (values are base64 encoded)
```

### Alternatives Considered

| Method | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Sealed Secrets | GitOps-friendly | Requires controller | Overkill for local dev |
| External Secrets | Cloud integration | Requires cloud provider | Out of scope |
| .env file with kubectl | Familiar pattern | Exposes secrets in command history | Security concern |

---

## R5: Namespace Strategy

### Context
Kubernetes namespaces provide isolation between workloads.

### Decision
**Default namespace**

### Rationale
- Simplest for single-developer local development
- No namespace switching in kubectl commands
- Aligns with Helm chart defaults
- Can be changed later for multi-team scenarios

### Alternatives Considered

| Strategy | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Custom `todo-app` | Isolation | Extra kubectl `-n` flags | Unnecessary complexity |
| Multiple namespaces | Environment separation | Overhead for local dev | Overkill |

### Future Consideration
For Phase V (production), consider namespace per environment:
- `todo-app-dev`
- `todo-app-staging`
- `todo-app-prod`

---

## R6: Port-Forward vs NodePort vs Ingress

### Context
Services need to be accessible from the developer's local machine.

### Decision
**kubectl port-forward for local access**

### Rationale
- Works with ClusterIP services (most secure)
- No external exposure
- Simple command, no additional configuration
- Spec explicitly requires port-forward

### Usage
```bash
# Terminal 1: Backend
kubectl port-forward svc/todo-backend 8000:8000

# Terminal 2: Frontend
kubectl port-forward svc/todo-frontend 3000:3000
```

### Alternatives Considered

| Method | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| NodePort | Direct access | Exposes ports, less secure | Security |
| Minikube service | Easy URL | Requires addon | Additional setup |
| Ingress | Production-like | Requires ingress controller | Out of scope (Phase V) |

---

## Summary of Decisions

| Topic | Decision | Spec Alignment |
|-------|----------|----------------|
| Minikube Driver | Docker | FR-001: Minikube start commands |
| AI Tools | kubectl-ai (primary) | FR-006: AI-assisted examples |
| Image Loading | docker-env | FR-011: Docker images from Spec 1 |
| Secrets | Manual kubectl | FR-008: Secret creation commands |
| Namespace | default | Simplicity for local dev |
| Access Method | port-forward | FR-005: Port-forward commands |

---

## Open Questions (None)

All technical decisions have been resolved. Ready for Phase 1 design artifacts.
