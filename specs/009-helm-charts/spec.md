# Feature Specification: Helm Charts for Todo AI Chatbot

**Feature Branch**: `009-helm-charts`
**Created**: 2026-01-21
**Status**: Draft
**Input**: User description: "Helm Charts for Todo AI Chatbot (Phase IV – Spec 2)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Backend to Local Kubernetes (Priority: P1)

A developer wants to package and deploy the FastAPI backend application to their local Minikube cluster using Helm. They need a standardized, repeatable deployment process that configures the application with appropriate settings for local development.

**Why this priority**: The backend is the core service that handles API requests and AI chat logic. Without a working backend deployment, the frontend cannot function. This is the foundation for the entire Kubernetes deployment workflow.

**Independent Test**: Can be fully tested by running `helm install todo-backend ./charts/todo-backend-chart` on Minikube and verifying the backend pods are running and accessible via port-forward.

**Acceptance Scenarios**:

1. **Given** Minikube is running and Helm is installed, **When** a developer runs `helm install todo-backend ./charts/todo-backend-chart`, **Then** the backend deployment is created with 1 replica and a ClusterIP service on port 8000.

2. **Given** the backend chart is installed, **When** a developer runs `kubectl port-forward svc/todo-backend 8000:8000`, **Then** the backend API is accessible at `localhost:8000`.

3. **Given** the backend chart is installed, **When** a developer runs `helm lint ./charts/todo-backend-chart`, **Then** no errors are reported and the chart is valid.

---

### User Story 2 - Deploy Frontend to Local Kubernetes (Priority: P1)

A developer wants to package and deploy the Next.js frontend application to their local Minikube cluster using Helm. The frontend must be configured to communicate with the backend service within the cluster.

**Why this priority**: The frontend is essential for user interaction. Having both backend and frontend deployable via Helm enables a complete local development environment that mirrors production patterns.

**Independent Test**: Can be fully tested by running `helm install todo-frontend ./charts/todo-frontend-chart` on Minikube and verifying the frontend pods are running and the UI is accessible via port-forward.

**Acceptance Scenarios**:

1. **Given** Minikube is running and Helm is installed, **When** a developer runs `helm install todo-frontend ./charts/todo-frontend-chart`, **Then** the frontend deployment is created with 1 replica and a ClusterIP service on port 3000.

2. **Given** the frontend chart is installed, **When** a developer runs `kubectl port-forward svc/todo-frontend 3000:3000`, **Then** the frontend UI is accessible at `localhost:3000`.

3. **Given** the frontend chart is installed, **When** a developer runs `helm lint ./charts/todo-frontend-chart`, **Then** no errors are reported and the chart is valid.

---

### User Story 3 - Configure Application via Helm Values (Priority: P2)

A developer wants to customize deployment settings (replicas, image tags, environment variables) without modifying chart templates. Configuration should be externalized to values.yaml for flexibility.

**Why this priority**: Configuration flexibility is essential for adapting deployments to different environments (dev, staging) without chart modifications. This enables reusability.

**Independent Test**: Can be tested by modifying values.yaml and running `helm upgrade` to verify configuration changes are applied correctly.

**Acceptance Scenarios**:

1. **Given** the backend chart is installed with default values, **When** a developer updates `replicaCount` in values.yaml to 2 and runs `helm upgrade`, **Then** the deployment scales to 2 replicas.

2. **Given** a developer needs a specific image version, **When** they set `image.tag: "v1.2.0"` in values.yaml, **Then** the deployment uses the specified image tag.

3. **Given** the backend requires an API key, **When** the developer creates a Kubernetes secret and references it via values.yaml, **Then** the pod has access to the secret as an environment variable.

---

### User Story 4 - Upgrade and Rollback Deployments (Priority: P3)

A developer wants to upgrade an existing Helm release with new configuration or image versions and be able to rollback if issues occur.

**Why this priority**: Deployment lifecycle management is important for maintaining application stability and enabling safe updates.

**Independent Test**: Can be tested by running `helm upgrade` with new values and then `helm rollback` to verify version management works.

**Acceptance Scenarios**:

1. **Given** the backend chart is installed at revision 1, **When** a developer runs `helm upgrade todo-backend ./charts/todo-backend-chart --set image.tag=v2.0.0`, **Then** the release is upgraded to revision 2.

2. **Given** the backend is at revision 2 with issues, **When** a developer runs `helm rollback todo-backend 1`, **Then** the deployment reverts to revision 1 configuration.

---

### Edge Cases

- What happens when Minikube is not running? The helm install command will fail with a clear kubectl connection error.
- How does the system handle missing required secrets? Pods will fail to start with CrashLoopBackOff; events will show the missing secret reference.
- What happens if port 3000 or 8000 is already in use during port-forward? kubectl port-forward will error with "address already in use" message.
- How does the system handle invalid values.yaml syntax? `helm lint` and `helm install` will fail with YAML parsing errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Helm chart for the backend (FastAPI) application under `charts/todo-backend-chart/`
- **FR-002**: System MUST provide a Helm chart for the frontend (Next.js) application under `charts/todo-frontend-chart/`
- **FR-003**: Each chart MUST include Chart.yaml with valid metadata (name, version, appVersion, description)
- **FR-004**: Each chart MUST include values.yaml with configurable parameters (image repository, tag, replicas, ports, environment variables)
- **FR-005**: Each chart MUST include templates/deployment.yaml with Kubernetes Deployment resource definition
- **FR-006**: Each chart MUST include templates/service.yaml with Kubernetes Service resource definition
- **FR-007**: Backend chart MUST expose port 8000 by default
- **FR-008**: Frontend chart MUST expose port 3000 by default
- **FR-009**: Charts MUST support Service type configuration (ClusterIP or NodePort) for Minikube compatibility
- **FR-010**: Backend chart MUST support environment variable injection from values.yaml
- **FR-011**: Backend chart MUST support referencing Kubernetes Secrets for sensitive values (OPENROUTER_API_KEY)
- **FR-012**: Charts MUST pass `helm lint` validation without errors
- **FR-013**: Charts MUST work with `helm template` to render valid Kubernetes manifests
- **FR-014**: Charts MUST use Docker images from Spec 1 (todo-frontend, todo-backend) as default image references
- **FR-015**: Charts MUST NOT include cloud-specific configurations (Ingress, LoadBalancer, PersistentVolumeClaims)
- **FR-016**: Charts MUST NOT require Helm hooks or Custom Resource Definitions (CRDs)

### Key Entities

- **Helm Chart**: A package containing Kubernetes resource templates and configuration values. Contains Chart.yaml (metadata), values.yaml (defaults), and templates/ directory.
- **Deployment**: Kubernetes workload resource managing pod replicas. Defines container image, ports, environment variables, and resource limits.
- **Service**: Kubernetes networking resource providing stable endpoint for pods. Defines port mappings and service type (ClusterIP/NodePort).
- **Secret**: Kubernetes resource for storing sensitive data. Referenced by deployments to inject credentials as environment variables.
- **ConfigMap**: Kubernetes resource for non-sensitive configuration data. Can be used for application settings.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Both charts can be installed on a fresh Minikube cluster in under 60 seconds combined
- **SC-002**: 100% of `helm lint` checks pass for both charts without errors or warnings
- **SC-003**: Deployed pods reach Running state within 120 seconds of helm install
- **SC-004**: Port-forwarded services respond to health checks within 10 seconds of port-forward initiation
- **SC-005**: Configuration changes via values.yaml are reflected in deployed resources after `helm upgrade`
- **SC-006**: A developer with Helm and Minikube experience can deploy both applications following the README in under 5 minutes

## Assumptions

- Minikube is installed and running with Docker driver
- Helm 3.x is installed and configured
- kubectl is configured to communicate with Minikube cluster
- Docker images (todo-frontend, todo-backend) are available locally or will be built using Minikube's Docker environment
- Neon PostgreSQL database connection is handled via environment variables (external to cluster)
- No persistent storage is required for the applications (stateless containers)

## Out of Scope

- Ingress configuration (Ingress controller setup is Phase V)
- Cloud-specific configurations (AWS EKS, GCP GKE, Azure AKS)
- Helm chart repository publishing
- TLS/SSL certificate management
- Horizontal Pod Autoscaling (HPA)
- Network Policies
- Pod Disruption Budgets
- Multi-environment value file management (dev/staging/prod)
