# Quickstart: Helm Charts for Todo AI Chatbot

**Feature**: 009-helm-charts
**Date**: 2026-01-21

## Prerequisites

1. **Minikube** running with Docker driver
   ```bash
   minikube start --driver=docker --memory=4096 --cpus=2
   ```

2. **Helm 3.x** installed
   ```bash
   helm version  # Verify installation
   ```

3. **Docker images** built in Minikube environment
   ```bash
   # Configure shell to use Minikube's Docker daemon
   eval $(minikube docker-env)

   # Build images
   docker build -t todo-backend:latest ./backend
   docker build -t todo-frontend:latest ./frontend
   ```

4. **Kubernetes Secret** for API key
   ```bash
   kubectl create secret generic todo-backend-secrets \
     --from-literal=OPENROUTER_API_KEY=<your-api-key>
   ```

---

## Quick Deploy

### Step 1: Deploy Backend

```bash
# Lint chart first
helm lint ./charts/todo-backend-chart

# Install backend
helm install todo-backend ./charts/todo-backend-chart \
  --set env.DATABASE_URL="postgresql://user:pass@host:5432/db"

# Verify deployment
kubectl get pods -l app=todo-backend
kubectl get svc todo-backend
```

### Step 2: Deploy Frontend

```bash
# Lint chart first
helm lint ./charts/todo-frontend-chart

# Install frontend
helm install todo-frontend ./charts/todo-frontend-chart

# Verify deployment
kubectl get pods -l app=todo-frontend
kubectl get svc todo-frontend
```

### Step 3: Access Application

```bash
# Port-forward backend (in separate terminal)
kubectl port-forward svc/todo-backend 8000:8000

# Port-forward frontend (in separate terminal)
kubectl port-forward svc/todo-frontend 3000:3000

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Health check: http://localhost:8000/health
```

---

## Common Operations

### Upgrade Release

```bash
# Update image tag
helm upgrade todo-backend ./charts/todo-backend-chart \
  --set image.tag=v2.0.0

# Update replica count
helm upgrade todo-frontend ./charts/todo-frontend-chart \
  --set replicaCount=2
```

### Rollback Release

```bash
# Check history
helm history todo-backend

# Rollback to previous version
helm rollback todo-backend 1
```

### Uninstall

```bash
helm uninstall todo-backend
helm uninstall todo-frontend
kubectl delete secret todo-backend-secrets
```

---

## Verification Commands

```bash
# List releases
helm list

# Check pod status
kubectl get pods

# View pod logs
kubectl logs -l app=todo-backend

# Describe deployment
kubectl describe deployment todo-backend

# Render templates without installing
helm template test ./charts/todo-backend-chart
```

---

## Troubleshooting

### Pods not starting

```bash
# Check events
kubectl describe pod <pod-name>

# Check if secret exists
kubectl get secrets
```

### Image pull errors

```bash
# Verify Minikube Docker env
eval $(minikube docker-env)
docker images | grep todo

# Ensure image is built
docker build -t todo-backend:latest ./backend
```

### Service not accessible

```bash
# Check service endpoints
kubectl get endpoints todo-backend

# Verify selector matches pod labels
kubectl get pods --show-labels
```
