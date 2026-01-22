# Minikube Troubleshooting Guide

This guide covers common issues when deploying the Todo AI Chatbot to Minikube.

## Quick Reference Table

| Issue | Symptom | Solution |
|-------|---------|----------|
| Minikube won't start | "Exiting due to DRV_AS_ROOT" | Don't run as root, or use `--force` flag |
| ImagePullBackOff | Pod stuck pulling image | Run `eval $(minikube docker-env)` before building |
| CrashLoopBackOff | Pod keeps restarting | Check logs with `kubectl logs <pod>`, verify secrets |
| Port already in use | "bind: address already in use" | Kill existing process: `lsof -i :<port>` then `kill <pid>` |
| Service not accessible | curl timeout | Verify port-forward is active, check service exists |
| Missing secrets | CreateContainerConfigError | Create secret with `kubectl create secret generic` |
| Insufficient resources | Pod stuck in Pending | Increase Minikube memory: `--memory=6144` |
| Connection refused | Backend API errors | Verify DATABASE_URL is correct and Neon DB is accessible |

---

## Startup Issues

### Minikube Won't Start

**Symptom**: Error message "Exiting due to DRV_AS_ROOT: The "docker" driver should not be used with root privileges"

**Solution**:
```bash
# Option 1: Run as non-root user (recommended)
minikube start --driver=docker

# Option 2: Force run as root (not recommended)
minikube start --driver=docker --force
```

**Symptom**: "Exiting due to RSRC_INSUFFICIENT_MEMORY" or cluster starts but pods stay Pending

**Solution**:
```bash
# Stop and delete existing cluster
minikube stop
minikube delete

# Start with more resources
minikube start --driver=docker --memory=6144 --cpus=4
```

**Symptom**: "The docker driver is not supported on this host"

**Solution**:
```bash
# Ensure Docker is installed and running
docker --version
docker ps

# If Docker isn't running:
sudo systemctl start docker  # Linux
# Or start Docker Desktop on macOS/Windows
```

---

## Image Issues

### ImagePullBackOff

**Symptom**: `kubectl get pods` shows ImagePullBackOff status

**Cause**: Images were built on the host Docker daemon, not Minikube's daemon

**Solution**:
```bash
# 1. Configure terminal to use Minikube's Docker
eval $(minikube docker-env)

# 2. Verify you're using Minikube's Docker
docker images  # Should show Minikube's images, not local

# 3. Rebuild images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# 4. Verify images exist in Minikube
docker images | grep todo

# 5. Restart the pods
kubectl rollout restart deployment todo-backend
kubectl rollout restart deployment todo-frontend
```

**Alternative**: Use `minikube image load` (slower but works without docker-env)
```bash
# Build locally
docker build -t todo-backend:latest ./backend

# Load into Minikube
minikube image load todo-backend:latest
```

---

## Pod Issues

### CrashLoopBackOff

**Symptom**: Pod keeps restarting, status shows CrashLoopBackOff

**Diagnosis**:
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check container logs
kubectl logs <pod-name>

# Watch logs in real-time
kubectl logs -f <pod-name>
```

**Common Causes and Solutions**:

1. **Missing environment variables**:
   ```bash
   # Check if secret exists
   kubectl get secrets

   # Create if missing
   kubectl create secret generic todo-backend-secrets \
     --from-literal=OPENROUTER_API_KEY=<key> \
     --from-literal=DATABASE_URL=<url> \
     --from-literal=BETTER_AUTH_SECRET=<secret>
   ```

2. **Database connection failure**:
   ```bash
   # Check logs for connection errors
   kubectl logs <pod-name> | grep -i database

   # Verify DATABASE_URL format
   # postgresql://user:password@host:port/database
   ```

3. **Application startup error**:
   ```bash
   # Get full logs
   kubectl logs <pod-name> --previous
   ```

### Pod Stuck in Pending

**Symptom**: Pod status is Pending indefinitely

**Diagnosis**:
```bash
kubectl describe pod <pod-name>
# Look at Events section at bottom
```

**Common Causes**:

1. **Insufficient resources**:
   ```bash
   # Check node resources
   kubectl describe node minikube | grep -A 5 "Allocated resources"

   # Restart Minikube with more resources
   minikube stop
   minikube start --memory=6144 --cpus=4
   ```

2. **Image pull issues**: See ImagePullBackOff section above

---

## Secret Issues

### CreateContainerConfigError

**Symptom**: Pod status shows CreateContainerConfigError

**Cause**: Secret referenced by the deployment doesn't exist

**Solution**:
```bash
# Check existing secrets
kubectl get secrets

# Check which secrets the deployment expects
kubectl describe deployment todo-backend | grep -A 10 "Environment"

# Create the required secret
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=your-openrouter-key \
  --from-literal=DATABASE_URL=your-database-url \
  --from-literal=BETTER_AUTH_SECRET=your-auth-secret

# Restart deployment to pick up new secret
kubectl rollout restart deployment todo-backend
```

### Secret Values Wrong

**Symptom**: Application starts but authentication or API calls fail

**Solution**:
```bash
# Delete and recreate secret with correct values
kubectl delete secret todo-backend-secrets

kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENROUTER_API_KEY=correct-key \
  --from-literal=DATABASE_URL=correct-url \
  --from-literal=BETTER_AUTH_SECRET=correct-secret

kubectl rollout restart deployment todo-backend
```

---

## Network Issues

### Port Already in Use

**Symptom**: `kubectl port-forward` fails with "bind: address already in use"

**Solution**:
```bash
# Find what's using the port
lsof -i :3000  # or :8000

# Kill the process
kill <pid>

# Or use a different local port
kubectl port-forward svc/todo-frontend 3001:3000
# Access via localhost:3001 instead
```

### Service Not Accessible

**Symptom**: curl to localhost:3000 or localhost:8000 times out

**Diagnosis**:
```bash
# Check if port-forward is still running
ps aux | grep port-forward

# Check service exists
kubectl get svc

# Check service has endpoints
kubectl get endpoints

# Check pod is running
kubectl get pods
```

**Solution**:
```bash
# Restart port-forward
kubectl port-forward svc/todo-frontend 3000:3000

# If service has no endpoints, check pod labels match service selector
kubectl describe svc todo-frontend
kubectl get pods --show-labels
```

### Frontend Can't Reach Backend

**Symptom**: UI loads but API calls fail

**Cause**: Frontend is trying to reach backend via wrong URL

**Solution**:
```bash
# Check frontend environment variable
kubectl exec <frontend-pod> -- env | grep API_URL

# Should be: http://todo-backend:8000 (internal service name)
# NOT: http://localhost:8000 (won't work inside cluster)
```

---

## Helm Issues

### Helm Install Fails

**Symptom**: `helm install` returns an error

**Common Causes**:

1. **Chart syntax errors**:
   ```bash
   helm lint ./charts/todo-backend-chart
   ```

2. **Template rendering issues**:
   ```bash
   helm template todo-backend ./charts/todo-backend-chart --debug
   ```

3. **Release already exists**:
   ```bash
   # Uninstall first
   helm uninstall todo-backend

   # Then install again
   helm install todo-backend ./charts/todo-backend-chart
   ```

### Values Not Applied

**Symptom**: Configuration changes don't take effect

**Solution**:
```bash
# Use upgrade instead of install
helm upgrade todo-backend ./charts/todo-backend-chart \
  --set replicaCount=2

# Or force pod recreation
kubectl rollout restart deployment todo-backend
```

---

## Cleanup

### Full Reset

If nothing works, start fresh:

```bash
# Uninstall Helm releases
helm uninstall todo-frontend 2>/dev/null
helm uninstall todo-backend 2>/dev/null

# Delete secrets
kubectl delete secret todo-backend-secrets 2>/dev/null

# Delete Minikube cluster
minikube delete

# Start fresh
minikube start --driver=docker --memory=4096 --cpus=2
eval $(minikube docker-env)
```

---

## Useful Debug Commands

```bash
# Cluster health
kubectl cluster-info
kubectl get nodes
minikube status

# All resources
kubectl get all

# Pod details
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl logs <pod-name> --previous  # Previous container logs

# Service details
kubectl describe svc <service-name>
kubectl get endpoints

# Secret details (values are base64 encoded)
kubectl get secret <secret-name> -o yaml

# Events (good for debugging)
kubectl get events --sort-by='.lastTimestamp'

# Resource usage
kubectl top pods
kubectl top nodes
```

---

## Getting Help

If you're still stuck:

1. Check the [Minikube documentation](https://minikube.sigs.k8s.io/docs/)
2. Check the [Helm documentation](https://helm.sh/docs/)
3. Review pod logs: `kubectl logs <pod-name>`
4. Review events: `kubectl get events`
5. Open an issue in the project repository with:
   - Output of `minikube status`
   - Output of `kubectl get all`
   - Error messages from logs
