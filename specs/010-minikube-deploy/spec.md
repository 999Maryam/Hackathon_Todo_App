# Feature Specification: Minikube Deployment & AI-Assisted K8s Operations

**Feature Branch**: `010-minikube-deploy`
**Created**: 2026-01-22
**Status**: Draft
**Input**: User description: "Minikube Deployment & AI-Assisted K8s Operations (Phase IV – Spec 3)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start and Verify Minikube Cluster (Priority: P1)

A developer wants to start a local Kubernetes cluster using Minikube so they can deploy and test the Todo AI Chatbot application locally before any cloud deployment. The cluster must be healthy and ready to accept workloads.

**Why this priority**: This is the foundation for all subsequent deployment activities. Without a running, healthy cluster, no Helm charts can be deployed and no application can be tested.

**Independent Test**: Can be fully tested by running `minikube start` and verifying cluster health with `kubectl get nodes`. The node should show `Ready` status.

**Acceptance Scenarios**:

1. **Given** Minikube is installed on the developer's machine, **When** they run `minikube start`, **Then** a local Kubernetes cluster starts within 180 seconds.

2. **Given** Minikube is running, **When** they run `kubectl get nodes`, **Then** at least one node is listed with status `Ready`.

3. **Given** Minikube is running, **When** they run `minikube status`, **Then** the output shows host, kubelet, and apiserver as `Running`.

4. **Given** Minikube is running, **When** they run `kubectl cluster-info`, **Then** the Kubernetes control plane endpoint is displayed.

---

### User Story 2 - Deploy Backend and Frontend via Helm Charts (Priority: P1)

A developer wants to deploy both the FastAPI backend and Next.js frontend applications to their Minikube cluster using the Helm charts created in Spec 2. Both applications should run as Kubernetes pods and be accessible via their services.

**Why this priority**: Deploying the actual applications is the core objective of this spec. Without successful Helm deployments, the developer cannot test the chatbot in a Kubernetes environment.

**Independent Test**: Can be fully tested by running `helm install` for both charts and verifying pods are Running with `kubectl get pods`.

**Acceptance Scenarios**:

1. **Given** Minikube is running and Helm charts exist in `charts/` directory, **When** a developer runs `helm install todo-backend ./charts/todo-backend-chart`, **Then** the backend deployment is created and pods reach `Running` state within 120 seconds.

2. **Given** the backend is deployed, **When** a developer runs `helm install todo-frontend ./charts/todo-frontend-chart`, **Then** the frontend deployment is created and pods reach `Running` state within 120 seconds.

3. **Given** both charts are installed, **When** a developer runs `kubectl get pods`, **Then** both backend and frontend pods show status `Running` with 1/1 containers ready.

4. **Given** secrets are pre-created in the cluster, **When** charts are installed with secret references, **Then** pods have access to required environment variables from secrets.

---

### User Story 3 - Access Chatbot via Port Forwarding (Priority: P1)

A developer wants to access the deployed chatbot application from their local browser using port forwarding. The frontend should be accessible at localhost:3000 and successfully communicate with the backend at localhost:8000.

**Why this priority**: Port forwarding is the standard method for accessing ClusterIP services in Minikube. This validates the full application stack works end-to-end in Kubernetes.

**Independent Test**: Can be fully tested by running port-forward commands and accessing the application URLs in a browser or via curl.

**Acceptance Scenarios**:

1. **Given** the frontend service is deployed, **When** a developer runs `kubectl port-forward svc/todo-frontend 3000:3000`, **Then** the frontend UI is accessible at `http://localhost:3000`.

2. **Given** the backend service is deployed, **When** a developer runs `kubectl port-forward svc/todo-backend 8000:8000`, **Then** `curl http://localhost:8000/health` returns HTTP 200 with `{"status":"ok"}` response.

3. **Given** both port-forwards are active, **When** a developer interacts with the chatbot UI, **Then** the frontend successfully communicates with the backend API.

---

### User Story 4 - Use AI-Assisted Operations with kubectl-ai/kagent (Priority: P2)

A developer wants to use AI-assisted Kubernetes tools (kubectl-ai or kagent) to perform common operations and troubleshooting tasks using natural language commands. This improves developer experience and reduces the learning curve for Kubernetes operations.

**Why this priority**: While not essential for deployment, AI-assisted tools significantly improve developer experience and align with the project's AI-focused nature. Demonstrating at least one AI-assisted operation fulfills the spec requirement.

**Independent Test**: Can be fully tested by executing at least one natural language command with kubectl-ai or kagent and verifying it produces the expected output or action.

**Acceptance Scenarios**:

1. **Given** kubectl-ai or kagent is installed and configured, **When** a developer uses natural language like "show me all pods in default namespace", **Then** the tool translates this to the appropriate kubectl command and displays pod information.

2. **Given** AI-assisted tools are available, **When** a developer asks "what's wrong with my deployment", **Then** the tool analyzes deployment status and provides diagnostic information.

3. **Given** the chatbot is deployed, **When** a developer uses AI-assisted tools to "scale the backend to 2 replicas", **Then** the tool executes the scaling operation or shows the command to do so.

---

### User Story 5 - Perform Dry-Run Helm Install (Priority: P2)

A developer wants to validate Helm chart deployment without actually installing resources. This allows verification of generated Kubernetes manifests before deployment.

**Why this priority**: Dry-run capability is essential for validating changes before applying them, reducing risk of deployment errors.

**Independent Test**: Can be fully tested by running `helm install --dry-run` and verifying YAML output is valid.

**Acceptance Scenarios**:

1. **Given** Helm charts exist in `charts/` directory, **When** a developer runs `helm install todo-backend ./charts/todo-backend-chart --dry-run`, **Then** the command outputs rendered Kubernetes YAML without creating resources.

2. **Given** a dry-run is executed, **When** reviewing the output, **Then** the deployment, service, and any referenced secrets/configmaps are correctly templated.

---

### Edge Cases

- What happens when Minikube is not installed? The `minikube start` command fails with "command not found" error; README provides installation instructions.
- What happens when Minikube fails to start due to resource constraints? Minikube outputs memory/CPU requirement errors; troubleshooting notes address minimum requirements.
- How does the system handle missing Docker images? Pods fail with `ImagePullBackOff`; troubleshooting notes explain building images locally.
- What happens if `todo-secrets` secret is not created? Pods fail with `CreateContainerConfigError`; README provides secret creation commands.
- What happens if port 3000 or 8000 is already in use? Port-forward fails with "address already in use"; troubleshooting notes suggest using alternate ports.
- How does the system handle kubectl-ai/kagent not being installed? The tool returns "command not found"; README provides installation instructions as optional.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Documentation MUST provide commands to start Minikube with appropriate configuration for local development
- **FR-002**: Documentation MUST include cluster verification commands (`kubectl get nodes`, `minikube status`)
- **FR-003**: Documentation MUST provide Helm install commands for both backend and frontend charts
- **FR-004**: Documentation MUST include dry-run examples for Helm chart validation
- **FR-005**: Documentation MUST provide port-forward commands for accessing services at localhost:3000 (frontend) and localhost:8000 (backend)
- **FR-006**: Documentation MUST include at least one kubectl-ai or kagent usage example with expected command and output
- **FR-007**: Documentation MUST include verification command `curl localhost:8000/health` with expected response
- **FR-008**: Documentation MUST include commands to create required Kubernetes secrets (todo-secrets)
- **FR-009**: Documentation MUST provide troubleshooting notes for common Minikube issues (startup failures, image pull errors, port conflicts)
- **FR-010**: README MUST be updated with a Minikube deployment section containing all commands in sequence
- **FR-011**: Documentation MUST reference Docker images from Spec 1 and Helm charts from Spec 2
- **FR-012**: Documentation MUST NOT include any cloud-specific configurations (no AWS, GCP, Azure references)

### Key Entities

- **Minikube Cluster**: Local single-node Kubernetes cluster for development. Provides Docker driver integration, DNS, and networking.
- **Helm Release**: Named installation of a Helm chart. Tracks revision history for upgrade/rollback operations.
- **Port Forward**: Kubectl mechanism to expose cluster services to localhost. Maps local ports to service ports.
- **Kubernetes Secret (todo-secrets)**: Pre-created secret containing sensitive environment variables (DATABASE_URL, OPENROUTER_API_KEY, etc.).
- **kubectl-ai/kagent**: AI-powered CLI tools that translate natural language into kubectl commands for improved developer experience.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can start Minikube and see `Ready` node status within 180 seconds of running `minikube start`
- **SC-002**: Both Helm charts install without errors, with pods reaching `Running` state within 120 seconds of installation
- **SC-003**: The chatbot frontend is accessible at localhost:3000 and loads the UI within 10 seconds of port-forward initiation
- **SC-004**: The backend health check at localhost:8000/health returns HTTP 200 with `{"status":"ok"}` response
- **SC-005**: At least one kubectl-ai or kagent command is demonstrated with documented output
- **SC-006**: A developer with Minikube and Helm experience can deploy the full application following the README in under 10 minutes
- **SC-007**: All troubleshooting scenarios have documented solutions or workarounds

## Assumptions

- Minikube 1.30+ is installed with Docker driver configured
- Helm 3.x is installed and accessible in PATH
- kubectl is configured to communicate with Minikube cluster (handled automatically by Minikube)
- Docker images (todo-frontend, todo-backend) will be built locally using Minikube's Docker environment or loaded via `minikube image load`
- Helm charts from Spec 2 (009-helm-charts) are complete and tested
- Dockerfiles from Spec 1 (008-docker-containerization) are complete and tested
- External Neon PostgreSQL database is accessible from local network
- Developer has minimum 4GB RAM and 2 CPU cores available for Minikube
- kubectl-ai or kagent installation is optional (one of them sufficient to meet AI-assisted requirement)

## Constraints

- Local Minikube deployment only; no cloud providers
- Reuse existing Docker images from Spec 1; no new Dockerfiles
- Reuse existing Helm charts from Spec 2; no chart modifications
- No persistent storage configuration (applications are stateless or use external database)
- Secrets (todo-secrets) are pre-created manually; no automated secret management
- No Ingress configuration (covered in future Phase V)
- No LoadBalancer service type (ClusterIP and NodePort only)

## Deliverables

1. **Minikube Commands Documentation**: Start, verify, and configure Minikube cluster
2. **Helm Deployment Commands**: Install commands with dry-run examples for both charts
3. **kubectl-ai/kagent Examples**: At least one AI-assisted operation with output
4. **README Update**: Minikube deployment section with complete step-by-step instructions
5. **Troubleshooting Guide**: Common Minikube issues and solutions

## Out of Scope

- Multi-node cluster configuration
- Cloud Kubernetes deployments (EKS, GKE, AKS)
- Ingress controller setup and configuration
- TLS/SSL certificate management
- Continuous deployment pipelines
- Helm chart modifications or enhancements
- Prometheus/Grafana monitoring setup
- Production hardening or security scanning
