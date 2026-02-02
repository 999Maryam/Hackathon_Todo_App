# Quickstart: Dapr + Kafka Setup on Minikube

## Overview
This guide walks through setting up Dapr (Distributed Application Runtime) with Redpanda (Kafka-compatible) on Minikube for event-driven architecture. This enables your applications to use Dapr building blocks like pub/sub, state management, and cron bindings.

## Prerequisites
- Minikube installed and running
- kubectl configured to connect to Minikube
- Dapr CLI installed
- Helm 3+ installed
- Existing Phase IV Helm charts from the todo app

## Step 1: Start Minikube (if not running)
```bash
minikube start
```

## Step 2: Install Dapr on Minikube
```bash
dapr init -k
```

Verify installation:
```bash
dapr status -k
```
Expected: All Dapr control plane components showing as HEALTHY.

## Step 3: Deploy Redpanda
Create the Redpanda deployment:

```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redpanda
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redpanda
  template:
    metadata:
      labels:
        app: redpanda
    spec:
      containers:
      - name: redpanda
        image: docker.redpanda.com/redpandadata/redpanda:v23.2.15
        ports:
        - containerPort: 9092
        - containerPort: 8081
        - containerPort: 8082
        command:
        - rpk
        args:
        - redpanda
        - start
        - --mode=dev-container
        - --kafka-addr=0.0.0.0:9092
        - --advertise-kafka-addr=redpanda:9092
---
apiVersion: v1
kind: Service
metadata:
  name: redpanda
  namespace: default
spec:
  selector:
    app: redpanda
  ports:
    - protocol: TCP
      port: 9092
      targetPort: 9092
  type: ClusterIP
EOF
```

Wait for Redpanda to be ready:
```bash
kubectl wait --for=condition=ready pod -l app=redpanda --timeout=180s
```

## Step 4: Create Dapr Components

### 4.1 Create Kafka Pub/Sub Component
```bash
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub-kafka
  namespace: default
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "redpanda:9092"
  - name: consumerGroup
    value: "todo-app-consumer-group"
  - name: authRequired
    value: "false"
  - name: initialOffset
    value: "newest"
EOF
```

### 4.2 Create PostgreSQL State Component
```bash
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore-postgresql
  namespace: default
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "host=neon-db.example.com port=5432 user=username password=password dbname=todoapp sslmode=require"
  - name: actorStateStore
    value: "true"
  - name: concurrency
    value: "first-write"
EOF
```

### 4.3 Create Cron Binding Component
```bash
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: cron-binding
  namespace: default
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/5 * * * *"
EOF
```

### 4.4 Create Kubernetes Secret Store Component
```bash
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore-kubernetes
  namespace: default
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
EOF
```

## Step 5: Update Helm Chart with Dapr Annotations

Update your existing Helm chart's deployment.yaml to include Dapr annotations:

```bash
# Assuming you're updating the todo-backend deployment
kubectl patch deployment todo-backend -p '{"spec":{"template":{"metadata":{"annotations":{"dapr.io/enabled":"true","dapr.io/app-id":"todo-backend","dapr.io/app-port":"8000","dapr.io/config":""}}}}}'
```

Or if updating the Helm chart template directly, add these annotations to the deployment template:

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

## Step 6: Verify Setup

Check Dapr components:
```bash
dapr components -k
```
Expected: All four components (pubsub-kafka, statestore-postgresql, cron-binding, secretstore-kubernetes) showing as ACTIVE.

Check pods with Dapr sidecar:
```bash
kubectl get pods
```
Expected: Your application pods should show 2/2 Ready status (app container + Dapr sidecar).

## Step 7: Test Event Flow

Publish a test event to Kafka topic:
```bash
dapr publish --pubsub pubsub-kafka -t task-events -d '{"eventId": "123", "eventType": "test", "data": {"message": "Hello Dapr + Kafka!"}}'
```

Check that the event was published by examining Dapr logs:
```bash
dapr logs todo-backend --follow
```

## Step 8: Verify All Components Healthy

Final check of all components:
```bash
dapr status -k
kubectl get pods
dapr components -k
```

## Troubleshooting

### Common Issues:

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