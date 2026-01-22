---
name: k8s-deploy-skill
description: Deploy applications to local Kubernetes using Minikube and Helm charts following Phase IV workflow.
version: 1.0.0
---

# Kubernetes Deployment Skill

This skill executes the complete Phase IV local Kubernetes deployment workflow for the Todo Chatbot application.

## Input Requirements

- **Application**: Frontend (Next.js) and/or Backend (FastAPI)
- **Environment**: Local Minikube cluster
- **Deployment Method**: Helm charts or raw kubectl manifests

## Workflow Overview

```
1. Verify Prerequisites
   ↓
2. Start Minikube Cluster
   ↓
3. Configure Docker Environment
   ↓
4. Build Container Images
   ↓
5. Create/Update Helm Charts
   ↓
6. Deploy to Kubernetes
   ↓
7. Verify Deployment
   ↓
8. Expose Services
```

## Instructions

### Step 1: Verify Prerequisites

Check required tools are installed:

```bash
# Check Minikube
minikube version

# Check kubectl
kubectl version --client

# Check Helm
helm version

# Check Docker
docker version
```

**Required Tools:**
- Minikube v1.30+
- kubectl v1.27+
- Helm v3.12+
- Docker Desktop or Docker Engine

### Step 2: Start Minikube Cluster

```bash
# Start cluster with Docker driver and adequate resources
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=4096 \
  --addons=registry,ingress

# Verify cluster is running
minikube status

# Verify kubectl context
kubectl config current-context
```

### Step 3: Configure Docker Environment

```bash
# Set Docker to use Minikube's daemon (Linux/macOS)
eval $(minikube docker-env)

# Verify Docker is pointing to Minikube
docker info | grep -i name
```

### Step 4: Build Container Images

**Frontend (Next.js):**
```bash
cd frontend
docker build -t todo-frontend:latest .
```

**Backend (FastAPI):**
```bash
cd backend
docker build -t todo-backend:latest .
```

**Verify Images:**
```bash
minikube image ls | grep todo
```

### Step 5: Create Helm Charts

**Chart Structure:**
```
helm/
├── todo-frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       └── _helpers.tpl
└── todo-backend/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── deployment.yaml
        ├── service.yaml
        ├── secret.yaml
        └── _helpers.tpl
```

**Frontend values.yaml:**
```yaml
replicaCount: 2
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: Never  # Use local image
service:
  type: NodePort
  port: 3000
env:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

**Backend values.yaml:**
```yaml
replicaCount: 2
image:
  repository: todo-backend
  tag: latest
  pullPolicy: Never  # Use local image
service:
  type: ClusterIP
  port: 8000
env:
  DATABASE_URL: ""  # Set via --set or secrets
  JWT_SECRET: ""    # Set via --set or secrets
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

### Step 6: Deploy with Helm

```bash
# Create namespace
kubectl create namespace todo-app

# Deploy backend first
helm install todo-backend ./helm/todo-backend \
  -n todo-app \
  --set env.DATABASE_URL="$DATABASE_URL" \
  --set env.JWT_SECRET="$JWT_SECRET"

# Deploy frontend
helm install todo-frontend ./helm/todo-frontend \
  -n todo-app

# Verify releases
helm list -n todo-app
```

**Alternative: Deploy with kubectl**
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml -n todo-app
kubectl apply -f k8s/backend/ -n todo-app
kubectl apply -f k8s/frontend/ -n todo-app
```

### Step 7: Verify Deployment

```bash
# Check pods are running
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check pod logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app

# Describe pods if issues
kubectl describe pods -l app=todo-backend -n todo-app
```

### Step 8: Expose Services

```bash
# Get frontend URL via Minikube
minikube service todo-frontend -n todo-app --url

# Or use port-forward
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app

# For backend API testing
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app
```

## Troubleshooting

### Pods in ImagePullBackOff

```bash
# Verify image exists in Minikube
minikube image ls | grep todo

# Ensure imagePullPolicy is Never or IfNotPresent
kubectl get deployment todo-backend -o yaml | grep imagePullPolicy
```

### Pods in CrashLoopBackOff

```bash
# Check logs
kubectl logs <pod-name> -n todo-app --previous

# Check environment variables
kubectl exec <pod-name> -n todo-app -- env
```

### Service Not Accessible

```bash
# Check endpoints
kubectl get endpoints -n todo-app

# Verify selector matches pod labels
kubectl get pods --show-labels -n todo-app
```

## Cleanup

```bash
# Uninstall Helm releases
helm uninstall todo-frontend -n todo-app
helm uninstall todo-backend -n todo-app

# Delete namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Delete cluster (optional)
minikube delete
```

## Agent Coordination

This skill coordinates with:

| Task | Agent |
|------|-------|
| Cluster setup | `minikube-cluster-ops` |
| Docker builds | `docker-containerizer` |
| Helm charts | `helm-chart-builder` |
| kubectl operations | `kubectl-resource-manager` |

## Output

Upon completion, provide:
1. Deployment status summary
2. Service URLs/ports
3. Any warnings or issues encountered
4. Next steps for testing
