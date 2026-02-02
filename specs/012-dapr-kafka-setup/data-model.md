# Data Model: Dapr + Kafka Setup on Minikube

## Overview
This document defines the data structures and entities relevant to the Dapr + Kafka integration in the Minikube environment. While this feature is primarily infrastructure-focused, it includes data models for the event-driven architecture components.

## Key Entities

### 1. Dapr Configuration Entity
- **Name**: DaprConfiguration
- **Fields**:
  - id: String (unique identifier for Dapr app)
  - appId: String (application identifier used by Dapr)
  - appPort: Integer (port number of application)
  - enabled: Boolean (whether Dapr sidecar is enabled)
  - logLevel: String (logging level: debug, info, warn, error)
  - config: String (configuration name to use)
- **Relationships**: Associated with Kubernetes deployment

### 2. Kafka Topic Entity
- **Name**: KafkaTopic
- **Fields**:
  - name: String (topic name)
  - partitions: Integer (number of partitions)
  - replicationFactor: Integer (replication factor)
  - config: Object (topic configuration properties)
- **Validation**: Name must match one of: task-events, reminders, task-updates
- **Relationships**: Used by Dapr pubsub component

### 3. Dapr Component Entity
- **Name**: DaprComponent
- **Fields**:
  - name: String (component name)
  - type: String (component type: pubsub.kafka, state.postgresql, bindings.cron, secretstores.kubernetes)
  - version: String (component API version)
  - metadata: Array<Object> (configuration properties)
  - scopes: Array<String> (app IDs that can use this component)
- **Relationships**: Referenced by Dapr applications

### 4. Event Message Entity
- **Name**: EventMessage
- **Fields**:
  - eventId: String (unique event identifier)
  - eventType: String (event type: created, updated, completed, deleted, reminder)
  - topic: String (destination topic name)
  - data: Object (event payload)
  - metadata: Object (additional metadata)
  - timestamp: DateTime (when event was created)
- **Validation**: topic must be one of the predefined Kafka topics
- **Relationships**: Published to Kafka topics via Dapr pubsub

### 5. Reminder Configuration Entity
- **Name**: ReminderConfig
- **Fields**:
  - taskId: Integer (associated task ID)
  - remindAt: DateTime (when to trigger reminder)
  - userId: String (user identifier)
  - sent: Boolean (whether reminder has been sent)
- **Relationships**: Connected to task entity and Kafka reminders topic

## Event Schemas

### Task Event Schema
```json
{
  "event_type": "created|updated|completed|deleted",
  "task_id": 123,
  "task_data": {
    "title": "...",
    "priority": "high|medium|low",
    "due_date": "2026-01-26T12:00:00Z",
    "is_recurring": false,
    "tags": ["work", "urgent"]
  },
  "user_id": "user-uuid",
  "timestamp": "2026-01-26T12:00:00Z"
}
```

### Reminder Event Schema
```json
{
  "task_id": 123,
  "title": "Task title",
  "due_at": "2026-01-27T09:00:00Z",
  "remind_at": "2026-01-27T08:00:00Z",
  "user_id": "user-uuid"
}
```

## State Management Schema

### Dapr State Store Keys
- **Key Pattern**: `{userId}:{entityType}:{entityId}`
- **Example**: `user-123:conversation:456`
- **Value**: JSON serialized entity data

## Component Configuration Schemas

### PubSub Kafka Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
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
```

### PostgreSQL State Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgres-state
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "postgresql://user:password@host:port/db"
    - name: actorStateStore
      value: "true"
```

### Cron Binding Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "*/5 * * * *"
```

### Kubernetes Secret Store Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secret-store
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

## State Transitions

### Event Processing States
1. **Published** → Event sent to Kafka topic via Dapr pubsub
2. **Processing** → Consumer receives event from Dapr pubsub
3. **Completed** → Event processed successfully
4. **Failed** → Error occurred during processing

### Dapr Sidecar States
1. **Initializing** → Sidecar starting up
2. **Healthy** → Sidecar operational and connected
3. **Unhealthy** → Sidecar having issues
4. **Terminated** → Sidecar shut down

## Validation Rules

### Topic Name Validation
- Must be one of: `task-events`, `reminders`, `task-updates`
- Follow DNS-1123 label format (lowercase, alphanumeric, hyphens)
- Length: 1-63 characters

### Event Schema Validation
- Required fields must be present
- Timestamp format must be ISO 8601
- User ID must be valid UUID format
- Task ID must be positive integer

### Component Configuration Validation
- Required metadata fields must be present
- Connection strings must be valid format
- Port numbers must be in valid range (1-65535)

## Relationships

### Dapr Application to Components
- One application can use multiple Dapr components
- Components can be shared across multiple applications
- Scopes define which applications can access which components

### Events to Topics
- Each event is published to exactly one topic
- Topics can receive events from multiple sources
- Topic configuration affects event handling characteristics