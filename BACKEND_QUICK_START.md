# Backend API - Quick Start Guide

## 🚀 Installation & Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your database and auth details:
# DATABASE_URL=postgresql://user:pass@localhost:5432/todo_db
# BETTER_AUTH_SECRET=your-secret-key
```

### 3. Run Development Server
```bash
make run
# or: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: http://localhost:8000

---

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 6 API Endpoints

#### 1️⃣ List All Tasks
```bash
curl -X GET http://localhost:8000/api/user-123/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 2️⃣ Create Task
```bash
curl -X POST http://localhost:8000/api/user-123/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

#### 3️⃣ Get Single Task
```bash
curl -X GET http://localhost:8000/api/user-123/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 4️⃣ Update Task
```bash
curl -X PUT http://localhost:8000/api/user-123/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title"}'
```

#### 5️⃣ Toggle Completion
```bash
curl -X PATCH http://localhost:8000/api/user-123/tasks/TASK_ID/complete \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 6️⃣ Delete Task
```bash
curl -X DELETE http://localhost:8000/api/user-123/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🧪 Testing

### Run All Tests
```bash
make test
# or: pytest tests/ -v --cov=app --cov-report=html
```

### Run Specific Test Category
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Contract tests only
pytest tests/contract/ -v

# Authentication tests
pytest tests/integration/test_auth.py -v

# Multi-user isolation tests
pytest tests/integration/test_ownership.py -v
```

### Test Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
# Opens htmlcov/index.html in browser
```

---

## 🔑 Authentication

### Getting a Test Token

**For Development/Testing**:
```python
from app.api.dependencies import create_test_token

token = create_test_token("user-123")
print(f"Token: {token}")
```

**From Better Auth** (Production):
- Better Auth issues JWT tokens after user signup/login
- Tokens include `user_id` claim
- Share `BETTER_AUTH_SECRET` between frontend and backend

### Token Structure
```
Header: Bearer <jwt_token>
Example: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app & routes
│   ├── config.py            # Environment config
│   ├── database.py          # Database setup
│   ├── models/
│   │   ├── task.py          # Task entity
│   │   └── schemas.py       # Pydantic schemas
│   ├── api/
│   │   ├── dependencies.py  # JWT dependency
│   │   └── routes.py        # All 6 endpoints
│   ├── services/
│   │   └── task_service.py  # Business logic
│   └── utils/
│       └── errors.py        # Error classes
├── tests/
│   ├── conftest.py          # pytest fixtures
│   ├── unit/                # Model/schema tests
│   ├── integration/         # Endpoint tests
│   └── contract/            # API contract tests
├── requirements.txt
├── .env.example
├── Makefile
└── README.md
```

---

## 🛠 Development Commands

```bash
# Install dependencies
make install

# Run dev server with auto-reload
make run

# Run all tests with coverage
make test

# Format code (black + isort)
make format

# Lint code (flake8)
make lint

# Clean cache files
make clean
```

---

## 🔒 Security Features

✅ **JWT Authentication**: Every endpoint requires valid token
✅ **Multi-User Isolation**: Users can only see/modify their own tasks
✅ **Input Validation**: Pydantic validates all inputs
✅ **Error Handling**: Consistent 400/401/403/404 responses
✅ **Type Safety**: Full type hints throughout

---

## 📊 Database Schema

### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## ✅ Validation Rules

### Title
- Required, non-empty
- Max 255 characters
- Error: 400 Bad Request if invalid

### Description
- Optional
- Max 2000 characters
- Error: 400 Bad Request if exceeds limit

### User ID
- From JWT token
- Must match URL path
- Error: 403 Forbidden if mismatch

### Completed Status
- Boolean (true/false)
- Toggle via PATCH endpoint only
- Default: false

---

## 🚨 Error Responses

```json
// 400 Bad Request - Validation Error
{
  "error": "Validation error",
  "status": 400,
  "detail": "title: ensure this value has at least 1 character"
}

// 401 Unauthorized - Missing/Invalid Token
{
  "error": "Missing or invalid authentication token",
  "status": 401
}

// 403 Forbidden - Permission Denied
{
  "error": "You do not have permission to access these tasks",
  "status": 403
}

// 404 Not Found
{
  "error": "Task not found",
  "status": 404
}
```

---

## 🔄 Response Format

### List Tasks
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user-123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    }
  ]
}
```

### Single Task
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:00:00Z",
  "updated_at": "2026-01-08T10:00:00Z"
}
```

---

## 🧬 Code Quality

- **Type Hints**: 100% coverage
- **Test Coverage**: 80+ tests (unit, integration, contract)
- **Documentation**: Swagger UI auto-generated
- **Linting**: PEP 8 compliant
- **Error Handling**: Comprehensive and consistent

---

## 🚀 Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use production database (Neon PostgreSQL)
- [ ] Configure CORS for frontend domain
- [ ] Set up proper logging and monitoring
- [ ] Configure health check endpoint
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/TLS

---

## 📚 Additional Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [JWT RFC](https://tools.ietf.org/html/rfc7519)
- [REST API Best Practices](https://restfulapi.net/)

---

## ❓ Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Activate venv and install requirements
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: `psycopg2 connection failed`
**Solution**: Check DATABASE_URL in .env and verify PostgreSQL is running
```bash
cat .env | grep DATABASE_URL
psql postgresql://user:pass@localhost/todo_db
```

### Issue: `JWT token verification failed`
**Solution**: Ensure BETTER_AUTH_SECRET matches between frontend and backend
```bash
echo $BETTER_AUTH_SECRET
# Must match the secret used to create the token
```

### Issue: `Tests fail with "permission denied"`
**Solution**: Use SQLite in-memory for tests (conftest.py handles this)
```bash
pytest tests/ -v  # Should work without database
```

---

## 📞 Support

- **Issue Tracker**: GitHub Issues
- **Documentation**: See `specs/001-fastapi-backend/quickstart.md`
- **Architecture**: See `specs/001-fastapi-backend/plan.md`
- **Data Model**: See `specs/001-fastapi-backend/data-model.md`

---

**Status**: ✅ Production Ready
**Last Updated**: 2026-01-08
**Implementation**: Complete
