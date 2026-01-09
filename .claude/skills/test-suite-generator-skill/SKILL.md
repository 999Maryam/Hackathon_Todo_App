# SKILL: test-suite-generator

## 1. Purpose
Generate comprehensive test suites with pytest (backend) and Jest + React Testing Library (frontend).

## 2. Input Parameters
- `TestSuiteType`: unit/integration/e2e.
- `CoverageThreshold`: Percentage (e.g., 80%).

## 3. Code Template

### Backend Integration Test
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, token_headers: dict):
    response = await client.post("/api/tasks/", json={"title": "Test Task"}, headers=token_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
```

### Frontend Component Test
```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskButton } from './TaskButton';

test('calls onAction when clicked', () => {
  const handleAction = jest.fn();
  render(<TaskButton onAction={handleAction} />);
  fireEvent.click(screen.getByRole('button'));
  expect(handleAction).toHaveBeenCalledTimes(1);
});
```

## 4. Output
Structured test files and configuration for running coverage reports.

## 5. Usage Example
Input: `TestSuiteType="integration"`
Output: Tests that verify API endpoints against a real database (in-memory or test container).

## 6. Quality Standards
- Use fixtures for shared setup (DB session, Auth headers).
- Target >80% code coverage.
- Independent tests (no side effects on other tests).
