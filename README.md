# Todo AI Chatbot

A full-stack Todo application with AI-powered chatbot capabilities.

## Tech Stack

- **Frontend**: Next.js 16+ with React 19, TypeScript, Tailwind CSS, Better Auth
- **Backend**: Python 3.13+ with FastAPI, SQLModel, JWT authentication
- **Database**: Neon Serverless PostgreSQL
- **Containerization**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker 24+ installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose v2+ (included with Docker Desktop)
- Environment variables configured (see below)

### Environment Setup

Create `.env` files in both `backend/` and `frontend/` directories.

**backend/.env**:
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key
OPENROUTER_API_KEY=your-openrouter-key
```

**frontend/.env**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
```

---

## Docker Commands

### Build Images

```bash
# Build backend image (target size: <500MB)
docker build -t todo-backend -f backend/Dockerfile backend/

# Build frontend image (target size: <300MB)
docker build -t todo-frontend -f frontend/Dockerfile frontend/

# Verify image sizes
docker images | grep todo
```

### Docker Compose Usage

```bash
# Start all services (production mode)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# View service status and health
docker-compose ps
```

### Development Mode (Hot Reload)

```bash
# Start with dev profile (enables hot-reload)
docker-compose --profile dev up

# Backend: Changes to Python files trigger auto-reload
# Frontend: Changes to TypeScript files trigger HMR

# Stop dev mode
docker-compose --profile dev down
```

### Health Checks

```bash
# Check backend health
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Check frontend accessibility
curl -I http://localhost:3000
# Expected: HTTP 200
```

### Container Management

```bash
# Shell into backend container
docker exec -it todo-backend sh

# Shell into frontend container
docker exec -it todo-frontend sh

# View container logs
docker-compose logs backend
docker-compose logs frontend

# Check non-root user execution
docker exec todo-backend whoami   # Expected: appuser
docker exec todo-frontend whoami  # Expected: nextjs
```

---

## Minikube Deployment (Local Kubernetes)

Deploy the Todo AI Chatbot to a local Kubernetes cluster using Minikube and Helm charts.

> **Minimum Requirements**: 4GB RAM, 2 CPU cores available for Minikube
>
> **For detailed troubleshooting**, see [docs/troubleshooting/minikube.md](docs/troubleshooting/minikube.md)

---

### Step 1: Prerequisites

Ensure you have the following tools installed:

| Tool | Minimum Version | Installation |
|------|-----------------|--------------|
| **Minikube** | 1.30+ | [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/) |
| **Helm** | 3.x | [helm.sh/docs/intro/install](https://helm.sh/docs/intro/install/) |
| **kubectl** | 1.28+ | Bundled with Minikube |
| **Docker** | 24+ | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| **kubectl-ai** (optional) | Latest | [github.com/sozercan/kubectl-ai](https://github.com/sozercan/kubectl-ai) |

Verify installations:
```bash
minikube version   # v1.30.0 or higher
helm version       # v3.x
kubectl version    # v1.28+
docker --version   # Docker 24+
```

---

### Step 2: Start Minikube Cluster

```bash
# Start Minikube with Docker driver and recommended resources
minikube start --driver=docker --memory=4096 --cpus=2
```
# Recommended for Hackathon (Balanced & Fast)
minikube start --driver=docker --memory=2048 --cpus=2
**Verify cluster health:**
```bash
# Check Minikube status
minikube status
# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

#minikube dashboard url:
minikube dashboard --url

# Check node is ready
kubectl get nodes
# Expected output:
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   1m    v1.28.x

# Check cluster info
kubectl cluster-info
# Expected: Kubernetes control plane is running at https://...
```

---

### Step 3: Build Docker Images in Minikube

Configure your terminal to use Minikube's Docker daemon, then build images:

```bash
# IMPORTANT: Run this in every new terminal session
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest ./backend

# Build frontend image
docker build -t todo-frontend:latest ./frontend

# Verify images exist in Minikube
docker images | grep todo
# Expected:
# todo-backend    latest    ...    <SIZE>
# todo-frontend   latest    ...    <SIZE>
```

> **Note**: Images must be built AFTER running `eval $(minikube docker-env)` to be available in the cluster.

---

### Step 4: Create Kubernetes Secrets

Create the secret containing sensitive environment variables:

```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=<your-openrouter-api-key> \
  --from-literal=DATABASE_URL=<your-neon-database-url> \
  --from-literal=BETTER_AUTH_SECRET=<your-better-auth-secret>

# Verify secret was created
kubectl get secrets
# Expected: todo-backend-secrets listed
```

---

### Step 5: Validate Helm Charts (Dry-Run)

Before deploying, validate the charts render correctly:

```bash
# Dry-run backend chart
helm install todo-backend ./charts/todo-backend-chart --dry-run
# Expected: YAML output showing Deployment, Service, etc.

# Dry-run frontend chart
helm install todo-frontend ./charts/todo-frontend-chart --dry-run
# Expected: YAML output showing Deployment, Service, etc.

# Lint charts for errors
helm lint ./charts/todo-backend-chart
helm lint ./charts/todo-frontend-chart
# Expected: "0 chart(s) linted, 0 chart(s) failed"
```

---

### Step 6: Deploy with Helm

```bash
# Install backend chart
helm install todo-backend ./charts/todo-backend-chart

# Install frontend chart
helm install todo-frontend ./charts/todo-frontend-chart

# Verify Helm releases
helm list
# Expected:
# NAME            NAMESPACE   REVISION   STATUS     CHART
# todo-backend    default     1          deployed   todo-backend-chart-0.1.0
# todo-frontend   default     1          deployed   todo-frontend-chart-0.1.0
```

---

### Step 7: Verify Deployment

Wait for pods to reach Running state:

```bash
# Check pod status
kubectl get pods
# Expected (wait up to 120 seconds):
# NAME                             READY   STATUS    RESTARTS   AGE
# todo-backend-xxxxx-xxxxx         1/1     Running   0          1m
# todo-frontend-xxxxx-xxxxx        1/1     Running   0          1m

# Check services
kubectl get services
# Expected:
# NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
# todo-backend    ClusterIP   10.x.x.x         <none>        8000/TCP
# todo-frontend   ClusterIP   10.x.x.x         <none>        3000/TCP
```

---

### Step 8: Access the Application

Use port-forwarding to access services locally:

```bash
# Terminal 1: Forward backend
kubectl port-forward svc/todo-backend 8000:8000

# Terminal 2: Forward frontend
kubectl port-forward svc/todo-frontend 3000:3000
```

Or run both in background:
```bash
kubectl port-forward svc/todo-backend 8000:8000 &
kubectl port-forward svc/todo-frontend 3000:3000 &
```

**Verify access:**
```bash
# Check backend health
curl http://localhost:8000/health
# Expected: {"status":"ok"}

# Access frontend
# Open browser to: http://localhost:3000
```

---

### AI-Assisted Operations (Optional)

Use **kubectl-ai** for natural language Kubernetes operations:

**Installation:**
```bash
# macOS
brew tap sozercan/kubectl-ai
brew install kubectl-ai

# Linux/Windows: Download from
# https://github.com/sozercan/kubectl-ai/releases

# Set API key
export OPENAI_API_KEY=<your-openai-key>
```

**Example Commands:**

```bash
# Check cluster health
kubectl-ai "show me all pods and their status"
# Translates to: kubectl get pods -o wide

# Diagnose issues
kubectl-ai "why is my backend pod failing"
# Translates to: kubectl describe pod + kubectl logs

# Scale deployment
kubectl-ai "scale the backend to 2 replicas"
# Translates to: kubectl scale deployment todo-backend --replicas=2
```

> **Note**: kubectl-ai is optional. All operations can be done with standard kubectl commands.

---

### Helm Operations

```bash
# List releases
helm list

# Upgrade a release (e.g., scale replicas)
helm upgrade todo-backend ./charts/todo-backend-chart --set replicaCount=2

# Check release history
helm history todo-backend

# Rollback to previous version
helm rollback todo-backend 1
```

---

### Cleanup

```bash
# Uninstall Helm releases
helm uninstall todo-frontend
helm uninstall todo-backend

# Delete secret
kubectl delete secret todo-backend-secrets

# Stop Minikube (preserves cluster)
minikube stop

# Delete Minikube cluster (removes everything)
minikube delete
```

---

### Quick Troubleshooting

| Issue | Command | Solution |
|-------|---------|----------|
| Pods stuck in ImagePullBackOff | `kubectl describe pod <name>` | Run `eval $(minikube docker-env)` then rebuild images |
| Pods in CrashLoopBackOff | `kubectl logs <pod-name>` | Check secrets exist, verify DATABASE_URL |
| Port already in use | `lsof -i :3000` | Kill process or use different port |
| Cluster won't start | `minikube start --memory=6144` | Increase resources |

For detailed troubleshooting, see [docs/troubleshooting/minikube.md](docs/troubleshooting/minikube.md)

---

## Development (Without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
hackathon2-todo-app/
├── backend/
│   ├── app/              # FastAPI application
│   ├── Dockerfile        # Multi-stage Python container
│   ├── .dockerignore     # Build context exclusions
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/              # Next.js application
│   ├── Dockerfile        # Multi-stage Node container
│   ├── .dockerignore     # Build context exclusions
│   └── package.json      # Node dependencies
├── charts/               # Helm charts for Kubernetes deployment
│   ├── todo-backend-chart/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   └── templates/
│   └── todo-frontend-chart/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── docker-compose.yml    # Container orchestration
├── specs/                # Feature specifications
└── README.md             # This file
```

---

## API Documentation

When the backend is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Phase V: Advanced Features

### New Task Properties

| Property | Type | Description |
|----------|------|-------------|
| `priority` | `"low"` \| `"medium"` \| `"high"` | Task priority level |
| `due_date` | ISO 8601 datetime | Task due date/time |
| `tags` | Array of Tag objects | Associated tags |
| `is_recurring` | boolean | Whether task recurs |
| `recurring_config` | Object | Recurrence pattern (daily/weekly/monthly) |
| `reminder` | Object | Reminder settings |

### New API Endpoints

**Tags:**
```
GET    /api/{user_id}/tags           - List all user tags
POST   /api/{user_id}/tags           - Create a new tag
PUT    /api/{user_id}/tags/{tag_id}  - Update a tag
DELETE /api/{user_id}/tags/{tag_id}  - Delete a tag
```

**Reminders:**
```
GET    /api/{user_id}/tasks/{id}/reminder  - Get task reminder
POST   /api/{user_id}/tasks/{id}/reminder  - Set task reminder
DELETE /api/{user_id}/tasks/{id}/reminder  - Delete task reminder
```

### Task Query Parameters

Filter, search, and sort tasks using query parameters:

```bash
# Search tasks
GET /api/{user_id}/tasks?search=meeting

# Filter by priority
GET /api/{user_id}/tasks?priority=high&priority=medium

# Filter by completion status
GET /api/{user_id}/tasks?completed=false

# Filter by due date range
GET /api/{user_id}/tasks?due_from=2025-01-01&due_to=2025-01-31

# Filter by tags
GET /api/{user_id}/tasks?tag_ids=1&tag_ids=2

# Sort tasks
GET /api/{user_id}/tasks?sort_by=due_date&sort_order=asc
GET /api/{user_id}/tasks?sort_by=priority&sort_order=desc
```

### Testing Phase V Features

```bash
# Test priority setting
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "High priority task", "priority": "high"}'

# Test due date
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task with deadline", "due_date": "2025-01-20T10:00:00"}'

# Test tags - create tag
curl -X POST http://localhost:8000/api/{user_id}/tags \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work"}'

# Test reminder
curl -X POST http://localhost:8000/api/{user_id}/tasks/{task_id}/reminder \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"minutes_before": 60}'

# Test recurring task
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Daily standup", "is_recurring": true, "recurring_frequency": "daily", "due_date": "2025-01-20T09:00:00"}'

# Test search and filter
curl "http://localhost:8000/api/{user_id}/tasks?search=meeting&priority=high&sort_by=due_date" \
  -H "Authorization: Bearer {token}"
```

### MCP Tools (AI Agent)

Extended MCP tools for natural language task management:

| Tool | Description |
|------|-------------|
| `add_task` | Create task with priority, due_date, tag_ids |
| `list_tasks` | List tasks with search, filter, sort |
| `add_tag` | Create a new tag |
| `list_tags` | List all user tags with counts |
| `set_reminder` | Set reminder (minutes_before or exact time) |

**Example AI Commands:**
```
"Add a high priority task 'Finish report' due tomorrow at 5pm"
"Show me all tasks tagged with 'work' sorted by due date"
"Set a reminder 1 hour before my meeting task"
"Create a weekly recurring task for team standup"
```

### Kafka Events

Task events are published to Kafka for downstream processing:

| Event | Topic | Trigger |
|-------|-------|---------|
| `task_created` | task-events | New task created |
| `task_updated` | task-events | Task properties changed |
| `task_completed` | task-events | Task marked complete |
| `task_deleted` | task-events | Task deleted |
| `reminder_due` | reminders | Reminder time reached |

**Event Schema Example:**
```json
{
  "event_type": "task_created",
  "task_id": "uuid-here",
  "user_id": "user-123",
  "task_data": {
    "title": "Task title",
    "priority": "high",
    "due_date": "2025-01-20T10:00:00"
  },
  "timestamp": "2025-01-15T12:00:00"
}
```

---

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000 or 3000
lsof -i :8000
lsof -i :3000

# Kill the process or modify ports in docker-compose.yml
```

### Build Failures

```bash
# Clean rebuild (no cache)
docker-compose build --no-cache

# Check build context size
du -sh backend/ frontend/
```

### Container Won't Start

```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Common issues:
# - Missing environment variables
# - Database connection refused (check DATABASE_URL)
# - Port conflicts
```

### Image Size Issues

```bash
# Verify image sizes are within limits
docker images todo-backend  # Should be <500MB
docker images todo-frontend # Should be <300MB

# If too large, check .dockerignore files are correctly configured
```

---

## License

MIT
