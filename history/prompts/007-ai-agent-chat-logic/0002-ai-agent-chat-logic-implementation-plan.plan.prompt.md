---
id: "0002"
title: AI Agent Chat Logic Implementation Plan
stage: plan
date: 2026-01-14
surface: agent
model: claude-opus-4-5-20251101
feature: 007-ai-agent-chat-logic
branch: 007-ai-agent-chat-logic
user: developer
command: /sp.plan
labels: ["ai-agent", "openai-agents-sdk", "mcp-tools", "stateless", "phase-iii"]
links:
  spec: specs/007-ai-agent-chat-logic/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/007-ai-agent-chat-logic/plan.md
  - specs/007-ai-agent-chat-logic/research.md
  - specs/007-ai-agent-chat-logic/data-model.md
  - specs/007-ai-agent-chat-logic/quickstart.md
  - specs/007-ai-agent-chat-logic/contracts/agent-response.yaml
tests:
  - null
---

## Prompt

AI Agent & Chat Logic for Todo AI Chatbot (Phase III - Spec 3)

Create:
- System prompt file or inline definition (agent rules + tool selection examples)
- Agent configuration code (OpenAI Agents SDK runner + tool bindings)
- Stateless chat runner function (load -> run -> execute -> save -> return)
- Test file skeleton for agent behavior & persistence
- Updated /specs/features/agent-behavior.md with natural lang examples

Decisions:
- Agent model: gpt-4o-mini vs gpt-4o -> gpt-4o-mini (cost + speed for hackathon)
- Tool binding: MCP SDK tools directly vs wrapper -> direct binding
- Error handling: Agent catches & responds vs raise -> agent-friendly response
- History format: List of {"role": ..., "content": ...} -> yes, for OpenAI compatibility
- Confirmation style: Always friendly ("Got it! Task added.") -> yes, in prompt

Testing strategy:
- Behavior tests: Add/list/complete/delete/update intent detection
- Persistence tests: Message save/reload, user isolation
- Multi-turn: 3-4 message chain with correct tool sequence

Technical details & order:
1. Define system prompt (tool selection rules + examples)
2. Configure OpenAI agent + runner + bind 5 MCP tools
3. Implement chat runner with stateless cycle
4. Add current_user dependency (Phase II) for ownership
5. Write pytest tests for tool selection, persistence, errors
6. Document prompt & examples in spec

## Response snapshot

Created comprehensive implementation plan for AI Agent & Chat Logic:

**Phase 0 Research Decisions:**
1. OpenAI Agents SDK with `@function_tool` decorator for tool binding
2. Custom DB-backed session using Spec 1 helpers (not SQLiteSession)
3. gpt-4o-mini as default model (configurable via env)
4. Direct tool binding wrapping existing task_tools.py
5. Error handling via agent (tools return error dicts)
6. OpenAI-compatible history format from Spec 1

**Phase 1 Design Artifacts:**
- Architecture diagram showing Runner -> Agent -> Tools flow
- System prompt with 7 behavior rules
- Tool function signatures using `RunContextWrapper` for context injection
- AgentResponse/ToolCallRecord Pydantic schemas
- Runner function signature with full stateless cycle

**Deliverables defined:**
- `backend/app/agents/openai_agent.py` - Agent configuration
- `backend/app/agents/chat_runner.py` - Stateless runner function
- `backend/app/agents/prompts/system_prompt.txt` - Behavior rules
- `backend/tests/test_agent.py` - Test skeleton
- Contract: `specs/007-ai-agent-chat-logic/contracts/agent-response.yaml`

**Constitution Check:** All 8 principles pass or N/A

## Outcome

- Impact: Created complete implementation plan with architecture, research decisions, and design artifacts
- Tests: Test strategy defined - unit tests for intent detection, integration tests for persistence
- Files: 5 files created (plan.md, research.md, data-model.md, quickstart.md, agent-response.yaml)
- Next prompts: /sp.tasks to generate actionable implementation tasks
- Reflection: Research confirmed OpenAI Agents SDK is well-suited; Spec 1 helpers provide exact format needed

## Evaluation notes (flywheel)

- Failure modes observed: None - all research questions resolved cleanly
- Graders run and results (PASS/FAIL): Constitution check PASS (all applicable principles)
- Prompt variant (if applicable): Standard /sp.plan flow with user-provided decisions
- Next experiment (smallest change to try): N/A - proceed to /sp.tasks
