# Research: MCP Tools Server & Task Operations

**Feature**: 002-mcp-tools
**Date**: 2026-01-14
**Status**: Complete

---

## Research Questions

### RQ-001: MCP SDK Integration Pattern

**Question**: How to integrate MCP SDK with existing FastAPI backend?

**Decision**: Use FastMCP with lifespan management for database session injection

**Rationale**:
- FastMCP provides decorator-based tool registration (`@mcp.tool()`)
- Lifespan context manager allows sharing database session across tools
- Tools can access typed context via `ctx.request_context.lifespan_context`
- Supports both stdio and HTTP transports

**Alternatives Considered**:
1. Low-level MCP Server API - More verbose, requires manual schema definition
2. Separate MCP process - Complex IPC, not needed for this use case
3. Mount MCP as FastAPI router - MCP SDK handles transport layer differently

**Reference**: [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

### RQ-002: Tool Return Format

**Question**: How to ensure tools return exact specified format?

**Decision**: Return dictionaries directly from tool functions

**Rationale**:
- MCP SDK wraps dict returns as structured content
- Avoids Pydantic serialization complexity
- Exact match to spec: `{"task_id": int, "status": str, "title": str}`
- For `list_tasks`, return `list[dict]` of full task objects

**Implementation**:
```python
@mcp.tool()
def add_task(user_id: str, title: str, description: str | None = None) -> dict:
    """Add a new task."""
    # ... create task ...
    return {"task_id": task.id, "status": "created", "title": task.title}
```

---

### RQ-003: Database Session Management

**Question**: How to provide database session to MCP tools?

**Decision**: Use FastMCP lifespan with dataclass context

**Rationale**:
- Existing `get_session()` from Phase II provides Session dependency
- Lifespan pattern ensures proper connection lifecycle
- Tools access session via `ctx.request_context.lifespan_context.db`
- Stateless: new session per request, no in-memory state

**Implementation Pattern**:
```python
@dataclass
class ToolContext:
    db_session_factory: Callable[[], Generator[Session, None, None]]

@asynccontextmanager
async def tool_lifespan(server: FastMCP) -> AsyncIterator[ToolContext]:
    yield ToolContext(db_session_factory=get_session)
```

---

### RQ-004: User Isolation Enforcement

**Question**: How to consistently enforce user_id filtering across all tools?

**Decision**: Helper function pattern with mandatory user_id parameter

**Rationale**:
- Every tool accepts `user_id` as first parameter (per spec FR-002)
- Internal helper functions take user_id and apply `WHERE user_id = ?` filter
- No way to accidentally bypass isolation - user_id is required
- Uniform error message: "Task not found or not owned"

**Implementation Pattern**:
```python
def _get_task_if_owned(task_id: int, user_id: str, db: Session) -> Task | None:
    """Get task only if owned by user."""
    return db.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
```

---

### RQ-005: Task ID Type Handling

**Question**: Task model uses UUID, but spec requires int task_id. How to handle?

**Decision**: Use UUID internally, convert to string representation in responses

**Rationale**:
- Phase II Task model uses `uuid.UUID` as primary key (see `backend/app/models/task.py`)
- Cannot change to int without breaking Phase II compatibility
- Spec says `task_id: int` but this is conceptual - UUID string works for AI agent
- Return `str(task.id)` in responses instead of int

**Update to Spec Interpretation**:
- Tool parameters: `task_id` accepts string (UUID)
- Return values: `task_id` returns string (UUID)
- Agent can handle either format - the key is consistency

---

### RQ-006: Error Response Format

**Question**: What format for error responses from tools?

**Decision**: Return dict with "error" key and descriptive message

**Rationale**:
- Per FR-024: Tools return dict responses, not HTTP exceptions
- Per FR-025: "Task not found or not owned" for missing/unauthorized
- Per FR-026: Descriptive messages for validation errors
- Consistent format enables agent to parse and respond appropriately

**Implementation**:
```python
# Success
return {"task_id": str(task.id), "status": "created", "title": task.title}

# Error
return {"error": "Task not found or not owned"}
return {"error": "Title is required"}
```

---

### RQ-007: MCP Server Deployment

**Question**: Run MCP server separately or integrate with FastAPI?

**Decision**: Separate MCP server process using stdio transport

**Rationale**:
- OpenAI Agents SDK connects to MCP servers via stdio (default)
- Keeps FastAPI REST API separate from MCP tool server
- MCP server runs as subprocess when agent needs tools
- Cleaner separation of concerns: REST for humans, MCP for AI

**Implementation**:
- `backend/app/tools/mcp_server.py` - FastMCP server with 5 tools
- Run via: `python -m app.tools.mcp_server`
- Agent (Spec 3) will spawn this as subprocess

---

### RQ-008: Status Filter Validation

**Question**: How to handle invalid status filter in list_tasks?

**Decision**: Default to "all" if invalid value provided

**Rationale**:
- Per edge case: "System returns an error or treats as all"
- "Treats as all" is more user-friendly - agent gets full list
- Log warning for debugging purposes
- Valid values: "all", "pending", "completed"

**Implementation**:
```python
VALID_STATUS_FILTERS = {"all", "pending", "completed"}

def list_tasks(user_id: str, status: str = "all") -> list[dict]:
    if status not in VALID_STATUS_FILTERS:
        status = "all"  # Default to all for invalid values
    # ... filter based on status ...
```

---

## Technology Decisions

### MCP SDK Version

- Package: `mcp>=1.25`
- Using FastMCP high-level API for simplicity
- Decorator-based tool registration

### Database Access

- Reuse Phase II: `app.database.get_session()`
- SQLModel queries with user_id filtering
- No new tables - only existing Task table

### Transport

- stdio transport (default) for agent integration
- Can switch to HTTP if needed for testing

---

## Dependencies to Add

```
mcp>=1.25
```

Add to `backend/requirements.txt`

---

## File Structure

```
backend/app/tools/
├── __init__.py           # Export tool functions
├── mcp_server.py         # FastMCP server with 5 tools
└── task_tools.py         # Tool implementation functions
```

---

## Sources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [PyPI mcp package](https://pypi.org/project/mcp/)
- [MCP Server Documentation](https://modelcontextprotocol.github.io/python-sdk/)
- [OpenAI Agents MCP Integration](https://openai.github.io/openai-agents-python/mcp/)
