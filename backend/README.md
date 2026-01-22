---
title: MyTodo App Backend
emoji: ✅
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Todo Backend API

Secure, RESTful API for multi-user task management with JWT authentication, built with FastAPI and SQLModel.

## Quick Start

See the complete setup guide: [../specs/001-fastapi-backend/quickstart.md](../specs/001-fastapi-backend/quickstart.md)

## Development Commands

```bash
# Install dependencies
make install

# Run development server with auto-reload
make run

# Run full test suite with coverage
make test

# Format code
make format

# Lint code
make lint

# Clean cache files
make clean
```

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000/api/{user_id}/tasks

## Architecture

- **Framework**: FastAPI (async-capable, modern Python web framework)
- **ORM**: SQLModel (combining SQLAlchemy + Pydantic for type-safe queries)
- **Database**: PostgreSQL (via Neon or local installation)
- **Authentication**: JWT tokens from Better Auth
- **Testing**: pytest with unit, integration, and contract tests

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app & routes
│   ├── config.py               # Environment configuration
│   ├── database.py             # Database engine & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py             # Task SQLModel entity
│   │   └── schemas.py          # Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # JWT verification
│   │   └── routes.py           # All endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py     # Business logic
│   └── utils/
│       ├── __init__.py
│       └── errors.py           # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── unit/
│   ├── integration/
│   └── contract/
├── .env.example                # Template for env vars
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/test_endpoints.py -v
```

## Deployment

For production deployment information, see the main project documentation.
