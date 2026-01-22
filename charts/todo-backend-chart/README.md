# Todo Backend Helm Chart

This Helm chart deploys the Todo AI Chatbot FastAPI backend application to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- A Kubernetes Secret named `todo-backend-secrets` containing the `OPENROUTER_API_KEY`

## Installing the Chart

```bash
# Install with default values
helm install my-todo-backend ./charts/todo-backend-chart

# Install with custom values file
helm install my-todo-backend ./charts/todo-backend-chart -f custom-values.yaml

# Install with inline value overrides
helm install my-todo-backend ./charts/todo-backend-chart \
  --set env.DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --set env.BETTER_AUTH_SECRET="your-secret-here"
```

## Configuration

The following table lists the configurable parameters and their default values.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Container image repository | `todo-backend` |
| `image.tag` | Container image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `8000` |
| `service.nodePort` | NodePort (if service.type is NodePort) | `null` |
| `resources.limits.cpu` | CPU limit | `500m` |
| `resources.limits.memory` | Memory limit | `512Mi` |
| `resources.requests.cpu` | CPU request | `100m` |
| `resources.requests.memory` | Memory request | `128Mi` |
| `env.DATABASE_URL` | PostgreSQL connection string | `""` |
| `env.ENVIRONMENT` | Application environment | `production` |
| `env.BETTER_AUTH_SECRET` | Better Auth secret key | `""` |
| `secrets.openRouterApiKey.secretName` | Secret name for OpenRouter API key | `todo-backend-secrets` |
| `secrets.openRouterApiKey.secretKey` | Secret key name | `OPENROUTER_API_KEY` |
| `probes.liveness.path` | Liveness probe HTTP path | `/health` |
| `probes.liveness.port` | Liveness probe port | `8000` |
| `probes.liveness.initialDelaySeconds` | Liveness probe initial delay | `5` |
| `probes.liveness.periodSeconds` | Liveness probe period | `30` |
| `probes.liveness.timeoutSeconds` | Liveness probe timeout | `10` |
| `probes.liveness.failureThreshold` | Liveness probe failure threshold | `3` |
| `probes.readiness.path` | Readiness probe HTTP path | `/health` |
| `probes.readiness.port` | Readiness probe port | `8000` |
| `probes.readiness.initialDelaySeconds` | Readiness probe initial delay | `5` |
| `probes.readiness.periodSeconds` | Readiness probe period | `10` |
| `probes.readiness.timeoutSeconds` | Readiness probe timeout | `5` |
| `probes.readiness.failureThreshold` | Readiness probe failure threshold | `3` |

## Required Secrets

Before deploying, create a Kubernetes Secret with the OpenRouter API key:

```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY="your-api-key-here"
```

## Health Checks

The chart configures both liveness and readiness probes using the `/health` endpoint:

- **Liveness Probe**: Checks if the container is alive (restarts if unhealthy)
- **Readiness Probe**: Checks if the container is ready to receive traffic

## Upgrading the Chart

```bash
helm upgrade my-todo-backend ./charts/todo-backend-chart -f custom-values.yaml
```

## Uninstalling the Chart

```bash
helm uninstall my-todo-backend
```

## Example Custom Values

Create a `custom-values.yaml` file:

```yaml
replicaCount: 2

image:
  tag: "v1.0.0"

service:
  type: NodePort
  nodePort: 30800

env:
  DATABASE_URL: "postgresql://user:password@postgres.default.svc.cluster.local:5432/tododb"
  ENVIRONMENT: "staging"
  BETTER_AUTH_SECRET: "my-secret-key-here"

resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 256Mi
```

## Troubleshooting

### Check Pod Status
```bash
kubectl get pods -l app=my-todo-backend-todo-backend
```

### View Pod Logs
```bash
kubectl logs -l app=my-todo-backend-todo-backend
```

### Check Service
```bash
kubectl get svc my-todo-backend-todo-backend
```

### Describe Deployment
```bash
kubectl describe deployment my-todo-backend-todo-backend
```

## Chart Structure

```
todo-backend-chart/
├── Chart.yaml           # Chart metadata
├── values.yaml          # Default configuration values
├── .helmignore          # Files to ignore when packaging
├── README.md            # This file
└── templates/
    ├── deployment.yaml  # Kubernetes Deployment
    └── service.yaml     # Kubernetes Service
```
