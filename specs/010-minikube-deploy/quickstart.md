# Quickstart: Minikube Deployment

**Feature**: 010-minikube-deploy
**Time**: ~10 minutes
**Prerequisites**: Docker, Minikube, Helm, kubectl installed

---

## TL;DR - Complete Deployment in 8 Commands

```bash
# 1. Start Minikube
minikube start --driver=docker --memory=4096 --cpus=2

# 2. Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# 3. Build images (inside Minikube's Docker)
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# 4. Create secrets
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-key> \
  --from-literal=DATABASE_URL=<your-neon-url> \
  --from-literal=BETTER_AUTH_SECRET=<your-secret>

# 5. Deploy with Helm
helm install todo-backend ./charts/todo-backend-chart
helm install todo-frontend ./charts/todo-frontend-chart

# 6. Wait for pods to be ready
kubectl wait --for=condition=Ready pods --all --timeout=120s

# 7. Port forward (run in separate terminals)
kubectl port-forward svc/todo-backend 8000:8000 &
kubectl port-forward svc/todo-frontend 3000:3000 &

# 8. Verify
curl http://localhost:8000/health
# Open http://localhost:3000 in browser
```

---

## Step-by-Step Guide

### Step 1: Start Minikube Cluster

```bash
# Start with recommended resources
minikube start --driver=docker --memory=4096 --cpus=2

# Verify cluster is running
minikube status
kubectl get nodes
```

**Expected Output**:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   30s   v1.28.x
```

### Step 2: Configure Docker Environment

```bash
# Point Docker CLI to Minikube's daemon
eval $(minikube docker-env)

# Verify (should show Minikube's containers)
docker ps | head -5
```

**Important**: Run this in every new terminal session!

### Step 3: Build Docker Images

```bash
# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Verify images exist
docker images | grep todo
```

**Expected Output**:
```
todo-backend    latest    abc123...    10 seconds ago    450MB
todo-frontend   latest    def456...    5 seconds ago     200MB
```

### Step 4: Create Kubernetes Secret

```bash
# Replace placeholders with actual values
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=sk-or-v1-xxxxx \
  --from-literal=DATABASE_URL=postgresql://user:pass@host/db \
  --from-literal=BETTER_AUTH_SECRET=your-jwt-secret

# Verify secret exists
kubectl get secret todo-backend-secrets
```

### Step 5: Deploy with Helm (Dry-Run First)

```bash
# Validate backend chart (dry-run)
helm install todo-backend ./charts/todo-backend-chart --dry-run

# If no errors, install
helm install todo-backend ./charts/todo-backend-chart

# Validate frontend chart (dry-run)
helm install todo-frontend ./charts/todo-frontend-chart --dry-run

# If no errors, install
helm install todo-frontend ./charts/todo-frontend-chart

# Verify Helm releases
helm list
```

**Expected Output**:
```
NAME            NAMESPACE   REVISION    STATUS      CHART
todo-backend    default     1           deployed    todo-backend-chart-0.1.0
todo-frontend   default     1           deployed    todo-frontend-chart-0.1.0
```

### Step 6: Wait for Pods to be Ready

```bash
# Watch pods until Running
kubectl get pods -w

# Or wait with timeout
kubectl wait --for=condition=Ready pods --all --timeout=120s
```

**Expected Output**:
```
NAME                             READY   STATUS    RESTARTS   AGE
todo-backend-6d4f5b8c9-x2k3j     1/1     Running   0          45s
todo-frontend-7c8d9e0f1-y4m5n    1/1     Running   0          40s
```

### Step 7: Access Services via Port-Forward

```bash
# Terminal 1: Backend API
kubectl port-forward svc/todo-backend 8000:8000

# Terminal 2: Frontend UI
kubectl port-forward svc/todo-frontend 3000:3000
```

Or run both in background:
```bash
kubectl port-forward svc/todo-backend 8000:8000 &
kubectl port-forward svc/todo-frontend 3000:3000 &
```

### Step 8: Verify Application

```bash
# Check backend health
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Open frontend in browser
open http://localhost:3000  # macOS
xdg-open http://localhost:3000  # Linux
start http://localhost:3000  # Windows
```

---

## AI-Assisted Operations (Optional)

### Using kubectl-ai

```bash
# Install kubectl-ai (if not installed)
brew install kubectl-ai  # macOS

# Set OpenAI API key
export OPENAI_API_KEY=<your-key>

# Example commands
kubectl-ai "show all pods"
kubectl-ai "describe the backend deployment"
kubectl-ai "check why pod is failing"
kubectl-ai "scale backend to 2 replicas"
```

---

## Cleanup

```bash
# Uninstall Helm releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Delete secret
kubectl delete secret todo-backend-secrets

# Stop Minikube (preserves state)
minikube stop

# Delete Minikube cluster (removes everything)
minikube delete
```

---

## Troubleshooting Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| `ImagePullBackOff` | Run `eval $(minikube docker-env)` then rebuild images |
| `CrashLoopBackOff` | Check `kubectl logs <pod>` for errors |
| `CreateContainerConfigError` | Verify secret exists with correct keys |
| Port already in use | Kill existing process: `lsof -i :3000` then `kill <pid>` |
| Minikube won't start | Check resources: `minikube start --memory=6144` |

See [full troubleshooting guide](../../docs/troubleshooting/minikube.md) for detailed solutions.
