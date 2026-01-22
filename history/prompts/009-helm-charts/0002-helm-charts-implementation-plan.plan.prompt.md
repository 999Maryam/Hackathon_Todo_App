---
id: "0002"
title: Helm Charts Implementation Plan
stage: plan
date: 2026-01-21
surface: agent
model: claude-opus-4-5-20251101
feature: 009-helm-charts
branch: 009-helm-charts
user: developer
command: /sp.plan
labels: ["helm", "kubernetes", "phase-iv", "minikube", "planning"]
links:
  spec: specs/009-helm-charts/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/009-helm-charts/plan.md
  - specs/009-helm-charts/research.md
  - specs/009-helm-charts/data-model.md
  - specs/009-helm-charts/quickstart.md
  - specs/009-helm-charts/contracts/backend-chart.yaml
  - specs/009-helm-charts/contracts/frontend-chart.yaml
tests:
  - null
---

## Prompt

/sp.plan Helm Charts for Todo AI Chatbot (Phase IV – Spec 2)

Create:
- charts/todo-backend-chart/ (Chart.yaml, values.yaml, templates/deployment.yaml, service.yaml)
- charts/todo-frontend-chart/ (same structure)
- values.yaml with defaults (image, port, replicas=1, env vars)
- README helm install instructions

Decisions:
- Chart version: 0.1.0
- Service type: ClusterIP (NodePort optional for local access)
- Secrets: Use Kubernetes Secret for OPENROUTER_API_KEY (not in values.yaml)
- Replicas: 1 (Minikube local)
- Ports: 8000 backend, 3000 frontend

Testing strategy:
- helm lint ./charts/todo-backend-chart
- helm template ./charts/todo-backend-chart > output.yaml
- kubectl apply -f output.yaml (dry-run)
- helm install todo-backend ./charts/todo-backend-chart --dry-run
- Verify rendered YAML has correct image, ports, env

Technical details & order:
1. Create folder structure: charts/todo-backend-chart/templates/
2. Chart.yaml: name, version, description
3. values.yaml: image.repository, image.tag, service.port, env vars
4. deployment.yaml: replicas, container image, ports, envFrom secret
5. service.yaml: type ClusterIP, port mapping
6. Repeat for frontend chart
7. Test: helm lint + template + dry-run install
8. Document in README: helm install commands + minikube port-forward

Why critical for Phase IV:
- Helm makes deployment reproducible & configurable for Minikube
- Prepares for Phase V cloud upgrade

## Response snapshot

Created implementation plan for Helm Charts feature (Phase IV - Spec 2):
- Phase 0 (Research): 10 research decisions documented covering chart structure, image references, service types, secret management, health probes, resource limits
- Phase 1 (Design): Data model for Helm chart entities, contracts for backend and frontend charts
- Plan.md: 4 implementation phases (backend chart, frontend chart, integration testing, documentation)
- Constitution check: All 8 principles verified, Phase IV specific checks passed
- Key decisions: Minimal chart structure, ClusterIP default, external K8s Secret for API keys, matching Docker health checks

## Outcome

- ✅ Impact: Complete implementation plan for Helm charts deployment infrastructure
- 🧪 Tests: Defined helm lint, helm template, helm install --dry-run validation
- 📁 Files: 6 created (plan.md, research.md, data-model.md, quickstart.md, 2 contracts)
- 🔁 Next prompts: /sp.tasks to generate actionable task list, then /sp.implement
- 🧠 Reflection: Research phase resolved all NEEDS CLARIFICATION; charts follow minimal structure as required

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (8/8 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
