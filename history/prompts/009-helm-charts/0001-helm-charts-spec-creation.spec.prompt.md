---
id: "0001"
title: Helm Charts Spec Creation
stage: spec
date: 2026-01-21
surface: agent
model: claude-opus-4-5-20251101
feature: 009-helm-charts
branch: 009-helm-charts
user: developer
command: /sp.specify
labels: ["helm", "kubernetes", "phase-iv", "minikube", "deployment"]
links:
  spec: specs/009-helm-charts/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-helm-charts/spec.md
  - specs/009-helm-charts/checklists/requirements.md
tests:
  - null
---

## Prompt

/sp.specify Helm Charts for Todo AI Chatbot (Phase IV – Spec 2)

Target audience: Developers packaging Phase III apps for Kubernetes deployment

Focus:
- Create Helm charts for frontend (Next.js) and backend (FastAPI)
- Prepare charts for local Minikube deployment

Success criteria:
- Two separate Helm charts: todo-frontend-chart and todo-backend-chart
- Each chart includes: Chart.yaml, values.yaml, templates/deployment.yaml, service.yaml
- Configurable: image tag, replicas, ports (3000 frontend, 8000 backend), env vars
- Supports Minikube: no ingress (use port-forward), basic Service type ClusterIP/NodePort
- Helm install works: helm install todo-backend ./todo-backend-chart
- No cloud-specific settings (save for Phase V)

Constraints:
- Reuse Docker images from Spec 1 (todo-frontend, todo-backend)
- Charts must be minimal & valid (helm lint passes)
- Env vars from values.yaml (OPENROUTER_API_KEY as secret)
- No Helm hooks or CRDs needed

Deliverables:
- charts/todo-backend-chart/ (Chart.yaml, values.yaml, templates/)
- charts/todo-frontend-chart/ (same structure)
- README update with helm install/upgrade commands
- helm lint & template output verification

## Response snapshot

Created feature specification for Helm Charts (Phase IV - Spec 2):
- Branch: 009-helm-charts
- Spec: specs/009-helm-charts/spec.md
- 4 user stories covering backend deployment, frontend deployment, configuration, and upgrade/rollback
- 16 functional requirements defining chart structure and capabilities
- 6 measurable success criteria
- Quality checklist passed all validation items

## Outcome

- ✅ Impact: Defined specification for packaging Todo AI Chatbot apps as Helm charts for Kubernetes
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 2 created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: /sp.plan or /sp.clarify to proceed with implementation planning
- 🧠 Reflection: Spec captures all user requirements without implementation details; technology-agnostic success criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All quality checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
