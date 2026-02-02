# Dapr + Kafka Infrastructure Setup

This directory contains the infrastructure configuration for the Dapr + Kafka event-driven architecture on Minikube.

## Overview

This setup includes:
- Dapr (Distributed Application Runtime) control plane
- Redpanda (Kafka-compatible) event streaming platform
- Dapr component configurations for pubsub, state management, cron bindings, and secret stores
- Helm chart updates for Dapr sidecar injection

## Prerequisites

- Minikube (v1.30+)
- kubectl
- Dapr CLI (v1.13+)
- Helm 3+
- Docker

## Setup Instructions

### 1. Start Minikube

```bash
minikube start --memory=2048 --cpus=2
```

### 2. Install Dapr on Minikube

```bash
dapr init -k
```

### 3. Verify Dapr Installation

```bash
dapr status -k
```

All Dapr control plane components should show as HEALTHY.

### 4. Deploy Local PostgreSQL Database

```bash
kubectl apply -f .infrastructure/postgres/postgres-deployment.yaml
```

Wait for PostgreSQL to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=postgres --timeout=180s
```

### 5. Create Application Secrets (SECURE WAY)

Create secrets using kubectl (do NOT store secrets in plain text files):

```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres:5432/todoapp" \
  --from-literal=BETTER_AUTH_SECRET="your-secure-secret-here" \
  --from-literal=OPENROUTER_API_KEY="your-api-key-here"
```

### 6. Deploy Redpanda

```bash
kubectl apply -f .infrastructure/redpanda/deployment.yaml
kubectl apply -f .infrastructure/redpanda/service.yaml
```

Wait for Redpanda to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=redpanda --timeout=180s
```

### 7. Deploy Dapr Components

Apply all Dapr component configurations:

```bash
kubectl apply -f .infrastructure/dapr/components/
```

Verify components are active:

```bash
dapr components -k
```

### 8. Deploy Application with Dapr Sidecar

Deploy your application using the modified Helm charts that include Dapr annotations:

```bash
helm upgrade --install todo-backend charts/todo-backend-chart/ --namespace default
```

## Dapr Components

### 1. Kafka Pub/Sub Component

Located at: `.infrastructure/dapr/components/pubsub-kafka.yaml`

Enables event publishing and subscribing through Redpanda (Kafka-compatible).

### 2. PostgreSQL State Component

Located at: `.infrastructure/dapr/components/state-postgresql.yaml`

Provides state management backed by PostgreSQL database.

### 3. Cron Binding Component

Located at: `.infrastructure/dapr/components/bindings-cron.yaml`

Enables scheduled task execution based on cron expressions.

### 4. Kubernetes Secret Store Component

Located at: `.infrastructure/dapr/components/secretstores-kubernetes.yaml`

Provides secure access to Kubernetes secrets.

## Helm Chart Updates

The backend Helm chart has been updated to include Dapr annotations:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
spec:
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "todo-backend"
        dapr.io/app-port: "8000"
        dapr.io/config: ""
```

These annotations enable automatic Dapr sidecar injection.

## Verification Commands

Check Dapr control plane status:
```bash
dapr status -k
```

Check Dapr components:
```bash
dapr components -k
```

Check running pods (should show 2/2 Ready for apps with Dapr):
```bash
kubectl get pods
```

Test event publishing:
```bash
dapr publish --pubsub pubsub-kafka -t task-events -d '{"eventId": "123", "eventType": "test", "data": {"message": "Hello Dapr + Kafka!"}}'
```

View Dapr logs:
```bash
dapr logs --follow
```

## Expected Timeframes

- Dapr installation: ~5 minutes
- Redpanda startup: ~3 minutes
- Topic creation: ~1 minute
- Component configuration: ~2 minutes
- Total setup time: ~15 minutes (well under 30-minute requirement)

## Troubleshooting

### Common Issues

1. **Dapr components show INACTIVE status**
   - Check if the referenced services are running (e.g., Redpanda)
   - Verify component configuration YAMLs

2. **Pods stuck in Init:0/1 status**
   - Check if Dapr sidecar injector is running: `kubectl get pods -n dapr-system`
   - Verify Dapr is properly installed: `dapr status -k`

3. **Unable to connect to Redpanda**
   - Verify Redpanda pod is Running: `kubectl get pods -l app=redpanda`
   - Check Redpanda logs: `kubectl logs -l app=redpanda`

4. **Event publishing fails**
   - Ensure the pubsub component is ACTIVE
   - Verify the topic name is correct
   - Check that Redpanda is accessible from the pubsub component

## Security Considerations

- Uses Dapr's built-in mTLS for service-to-service communication
- Stores secrets in Kubernetes and accesses them via Dapr secret store
- Maintains JWT-based authentication for user requests
- Proper namespace isolation in Minikube

## Cleanup

To remove the setup:

```bash
# Remove Dapr components
kubectl delete components.dapr.io pubsub-kafka,statestore-postgresql,cron-binding,secretstore-kubernetes

# Remove Redpanda
kubectl delete deployment,service redpanda

# Optionally uninstall Dapr from cluster
# dapr uninstall -k
```

## Next Steps

- Integrate Dapr pub/sub into your application code using Dapr HTTP API
- Implement state management using Dapr state API
- Use Dapr secret store to access secrets securely
- Configure cron bindings for scheduled tasks