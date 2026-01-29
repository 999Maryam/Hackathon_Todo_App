# Quickstart: Phase V Part A - Advanced Features

**Feature**: 011-advanced-features
**Date**: 2026-01-26

---

## Prerequisites

1. **Phase IV Complete**: Docker containers and Helm charts working
2. **Neon PostgreSQL**: Database accessible
3. **Redpanda Cloud Account**: Sign up at https://redpanda.com/cloud (FREE tier)

---

## Step 1: Environment Setup

### Add new environment variables to `.env`:

```bash
# Kafka/Redpanda Configuration
KAFKA_BOOTSTRAP_SERVERS=<your-cluster>.cloud.redpanda.com:9092
REDPANDA_USERNAME=<your-username>
REDPANDA_PASSWORD=<your-password>

# Optional: Local Redpanda (for development)
# KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

---

## Step 2: Install New Dependencies

### Backend (Python):

```bash
cd backend
pip install aiokafka>=0.8.0 python-dateutil>=2.8
# Update requirements.txt
echo "aiokafka>=0.8.0" >> requirements.txt
echo "python-dateutil>=2.8" >> requirements.txt
```

### Frontend (Node.js):

```bash
cd frontend
npm install date-fns @radix-ui/react-select
```

---

## Step 3: Database Migration

Run the Alembic migration to add new tables and columns:

```bash
cd backend
alembic revision --autogenerate -m "Add Phase V advanced features"
alembic upgrade head
```

This creates:
- Extended `tasks` table (priority, due_date, is_recurring, recurring_config_id)
- New `tags` table
- New `task_tags` table
- New `recurring_configs` table
- New `reminders` table

---

## Step 4: Redpanda Cloud Setup

1. **Create Topics** in Redpanda Console:
   - `task-events` (task lifecycle events)
   - `reminders` (reminder notifications)
   - `task-updates` (real-time sync)

2. **Get Credentials**:
   - Bootstrap servers URL
   - SASL username and password

3. **Test Connection**:
   ```bash
   # Install rpk CLI (optional)
   rpk topic list --brokers <your-cluster>.cloud.redpanda.com:9092 \
     --tls-enabled --sasl-mechanism SCRAM-SHA-256 \
     --user <username> --password <password>
   ```

---

## Step 5: Local Development (Optional)

For local Kafka/Redpanda development:

```bash
# Start local Redpanda with Docker
docker run -d --name redpanda \
  -p 9092:9092 \
  -p 8081:8081 \
  -p 8082:8082 \
  redpandadata/redpanda:latest \
  redpanda start \
  --smp 1 \
  --memory 512M \
  --overprovisioned \
  --kafka-addr PLAINTEXT://0.0.0.0:9092 \
  --advertise-kafka-addr PLAINTEXT://localhost:9092

# Create topics
docker exec -it redpanda rpk topic create task-events reminders task-updates
```

---

## Step 6: Run the Application

### Backend:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend:

```bash
cd frontend
npm run dev
```

---

## Step 7: Test the Features

### Create a task with priority and due date:

```bash
curl -X POST "http://localhost:8000/api/{user_id}/tasks" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Review PR",
    "priority": "high",
    "due_date": "2026-01-27T17:00:00Z",
    "tag_ids": [1, 2]
  }'
```

### Create a tag:

```bash
curl -X POST "http://localhost:8000/api/{user_id}/tags" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Work"}'
```

### List tasks with filters:

```bash
curl "http://localhost:8000/api/{user_id}/tasks?priority=high&sort_by=due_date&sort_order=asc" \
  -H "Authorization: Bearer <token>"
```

### Search tasks:

```bash
curl "http://localhost:8000/api/{user_id}/tasks?search=review" \
  -H "Authorization: Bearer <token>"
```

---

## Step 8: Verify Kafka Events

Check that events are being published:

```bash
# Using rpk CLI
rpk topic consume task-events --brokers <your-cluster>.cloud.redpanda.com:9092 \
  --tls-enabled --sasl-mechanism SCRAM-SHA-256 \
  --user <username> --password <password>
```

Expected output:
```json
{
  "event_type": "created",
  "task_id": 1,
  "task_data": {"title": "Review PR", "priority": "high", ...},
  "user_id": "user-uuid",
  "timestamp": "2026-01-26T10:30:00Z"
}
```

---

## Troubleshooting

### Kafka Connection Issues

1. **SSL/TLS Errors**: Ensure `security_protocol="SASL_SSL"` is set
2. **Authentication Errors**: Check username/password in environment variables
3. **Timeout Errors**: Verify network access to Redpanda Cloud

### Database Migration Errors

1. **Column Already Exists**: Migration already applied, skip with `alembic stamp head`
2. **Foreign Key Errors**: Ensure `users` table exists

### Frontend Build Errors

1. **date-fns Import Errors**: Ensure package is installed: `npm install date-fns`
2. **TypeScript Errors**: Update `lib/types.ts` with new Task interface

---

## Next Steps

After completing Part A setup:

1. **Part B**: Deploy Dapr on Minikube with Kafka pub/sub
2. **Part C**: Deploy to cloud (DigitalOcean/GKE/Azure)

Run `/sp.tasks` to generate implementation tasks.
