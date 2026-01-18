# Quickstart: Backend API Development Environment

**Feature**: Backend API | **Version**: 1.0.0 | **Date**: 2026-01-08

This guide walks through setting up, configuring, and running the Todo Backend API locally.

---

## Prerequisites

- Python 3.11 or later
- PostgreSQL 13+ (local installation OR use Neon PostgreSQL cloud)
- Git
- pip (Python package manager)
- Virtual environment tool (venv, built into Python)

---

## 1. Clone the Repository

```bash
git clone https://github.com/hackathon2-todo-app/repo.git
cd hackathon2-todo-app
git checkout 001-fastapi-backend
```

---

## 2. Create and Activate Virtual Environment

**macOS / Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

All Python dependencies are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlmodel` - ORM (SQLAlchemy + Pydantic)
- `pyjwt` - JWT token verification
- `psycopg2-binary` - PostgreSQL driver
- `pytest` - Testing framework
- `python-dotenv` - Environment variable management

---

## 4. Set Up Environment Variables

Create a `.env` file in the `backend/` directory (or repository root):

```bash
cp .env.example .env
```

Edit `.env` with your database and authentication details:

```dotenv
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db

# JWT Authentication
BETTER_AUTH_SECRET=your-shared-secret-key-from-better-auth

# Optional Configuration
JWT_EXPIRY_DAYS=7
LOG_LEVEL=INFO
```

**Environment Variables Explained**:

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://localhost/todo_db` | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | `super-secret-key-12345` | Shared secret for JWT verification (from Better Auth) |
| `JWT_EXPIRY_DAYS` | `7` | JWT token expiry in days (default: 7) |
| `LOG_LEVEL` | `INFO` | Logging level: DEBUG, INFO, WARNING, ERROR (default: INFO) |

**For Neon Cloud PostgreSQL**:
```dotenv
DATABASE_URL=postgresql://user:password@ep-xyz.region.neon.tech/todo_db
```

---

## 5. Initialize Database

The backend uses SQLModel to auto-generate database schema. On first run, tables are created automatically.

**Option A: Auto-create tables (simplest for development)**
```python
# This happens automatically when the app starts
# See app/database.py: create_db_and_tables()
```

**Option B: Use Alembic migrations (if implemented)**
```bash
cd backend/migrations
alembic upgrade head
```

Verify the database was created:
```bash
psql postgresql://user:password@localhost:5432/todo_db
\dt  # List tables - should see 'tasks' table
\q   # Exit
```

---

## 6. Run the Development Server

Start the FastAPI development server with auto-reload:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
INFO:     Started reloader process [67890]
```

---

## 7. Access the API

### Swagger UI (Interactive API Documentation)

Open in your browser:
```
http://localhost:8000/docs
```

This provides an interactive interface to:
- View all 6 endpoints
- Test endpoints with different parameters
- See request/response schemas
- Try authentication

### ReDoc (Alternative Documentation)

```
http://localhost:8000/redoc
```

### API Base URL

```
http://localhost:8000/api/{user_id}/tasks
```

---

## 8. Test Authentication with cURL

### Create a Valid JWT Token

First, you need a JWT token from Better Auth. For testing, create a token locally:

```bash
python
```

```python
import jwt
from datetime import datetime, timedelta

BETTER_AUTH_SECRET = "your-shared-secret-key-from-better-auth"
user_id = "user-123"

payload = {
    "user_id": user_id,
    "exp": datetime.utcnow() + timedelta(days=7)
}

token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")
print(f"Token: {token}")
```

### Test an Endpoint with cURL

**Get all tasks** (requires valid token):

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:8000/api/user-123/tasks
```

**Create a task**:

```bash
curl -X POST http://localhost:8000/api/user-123/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Update a task** (replace `{task_id}` with actual UUID):

```bash
curl -X PUT http://localhost:8000/api/user-123/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries and cook"
  }'
```

**Delete a task**:

```bash
curl -X DELETE http://localhost:8000/api/user-123/tasks/{task_id} \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Toggle completion**:

```bash
curl -X PATCH http://localhost:8000/api/user-123/tasks/{task_id}/complete \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 9. Run Tests

### Run All Tests

```bash
cd backend
pytest tests/ -v
```

### Run Specific Test Categories

**Unit tests only**:
```bash
pytest tests/unit/ -v
```

**Integration tests only**:
```bash
pytest tests/integration/ -v
```

**Authentication tests only**:
```bash
pytest tests/integration/test_auth.py -v
```

**With coverage report**:
```bash
pytest tests/ -v --cov=app --cov-report=html
# Opens coverage report in htmlcov/index.html
```

**Expected Output**:
```
tests/unit/test_models.py::test_task_creation PASSED
tests/integration/test_auth.py::test_missing_token_returns_401 PASSED
tests/integration/test_endpoints.py::test_create_task_returns_201 PASSED
...
======================== 50 passed in 2.34s ========================
```

---

## 10. Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app, route initialization
│   ├── config.py              # Environment configuration
│   ├── database.py            # SQLAlchemy engine, session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py            # Task SQLModel entity
│   │   └── schemas.py         # Pydantic request/response schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # JWT verification dependency
│   │   └── routes.py          # All 6 API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py    # Business logic
│   └── utils/
│       ├── __init__.py
│       └── errors.py          # Custom exception classes
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest fixtures
│   ├── unit/
│   │   ├── test_models.py
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_auth.py
│   │   ├── test_endpoints.py
│   │   ├── test_ownership.py
│   │   └── test_database.py
│   └── contract/
│       └── test_api_contract.py
│
├── .env                       # DO NOT COMMIT - Local env vars
├── .env.example               # Template for required env vars
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Modern Python project config
├── Makefile                   # Development shortcuts
└── README.md                  # Project overview
```

---

## 11. Development Workflow

### Make Code Changes

Edit files in `app/` and tests will auto-reload:

```bash
# Terminal 1: Running dev server
uvicorn app.main:app --reload

# Terminal 2: Making changes
# Edit app/api/routes.py
# Changes are automatically reloaded in Terminal 1
```

### Run Tests After Changes

```bash
# In a separate terminal
pytest tests/ -v --cov=app
```

### Format and Lint Code

```bash
# Install linting tools
pip install black flake8 isort

# Format code
black app/ tests/

# Check for issues
flake8 app/ tests/

# Sort imports
isort app/ tests/
```

---

## 12. Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

### Issue: `psycopg2 connection failed`

**Solution**: Check database is running and connection string is correct:
```bash
# Test PostgreSQL connection
psql postgresql://user:password@localhost:5432/todo_db

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Issue: `JWT token verification failed`

**Solution**: Ensure `BETTER_AUTH_SECRET` matches between frontend and backend:
```bash
# Check env var is set
echo $BETTER_AUTH_SECRET  # or print from .env

# Verify token was created with same secret
python
import jwt
jwt.decode(token, "your-secret", algorithms=["HS256"])
```

### Issue: `Tests fail with database connection error`

**Solution**: Use SQLite in-memory database for tests (see `conftest.py`):
```python
# conftest.py automatically sets up test database
# No need to configure anything
pytest tests/
```

---

## 13. Common Development Tasks

### Add a New Endpoint

1. Define the request/response schema in `app/models/schemas.py`
2. Add the route in `app/api/routes.py`
3. Add business logic in `app/services/task_service.py`
4. Add tests in `tests/integration/test_endpoints.py`
5. Tests will auto-run via pytest watch

### Update Database Schema

1. Modify the SQLModel in `app/models/task.py`
2. Create Alembic migration: `alembic revision --autogenerate -m "Add field"`
3. Apply migration: `alembic upgrade head`
4. Tests will use updated schema

### Debug an Endpoint

1. Add logging to `app/api/routes.py`:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"User {user_id} created task: {task}")
   ```

2. Set `LOG_LEVEL=DEBUG` in `.env`

3. Restart server and check console output

---

## 14. Performance Testing (Optional)

Test API response times under load:

```bash
# Install loadtest tool
pip install locust

# Create locustfile.py (see examples directory)
locust -f locustfile.py --host=http://localhost:8000

# Open browser to http://localhost:8089
# Configure number of users and spawn rate
# Run tests and monitor response times
```

---

## 15. Next Steps

1. ✅ **Environment Setup**: Complete (you are here)
2. ⏭ **Development**: Start implementing endpoints using `/sp.tasks` phase
3. ⏭ **Testing**: Run full test suite, verify 90%+ coverage
4. ⏭ **Frontend Integration**: Connect with Next.js frontend
5. ⏭ **Deployment**: Deploy to production (Vercel, AWS Lambda, etc.)

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **JWT Authentication**: https://tools.ietf.org/html/rfc7519
- **RESTful API Design**: https://restfulapi.net/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/

---

**Status**: ✅ Ready for development

**Last Updated**: 2026-01-08
