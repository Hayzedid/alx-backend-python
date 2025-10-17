# Kubernetes Implementation for Django Messaging App

This document provides comprehensive instructions for deploying and managing the Django messaging application using Kubernetes with advanced deployment strategies.

## 🚀 Overview

This implementation includes:
- **Local Kubernetes cluster setup** with Minikube
- **Basic deployment** with scaling capabilities
- **Ingress configuration** for external access
- **Blue-Green deployment** strategy for zero-downtime deployments
- **Rolling updates** with continuous availability testing

## 📋 Prerequisites

### Required Software
- **Docker** - For container management
- **Minikube** - Local Kubernetes cluster
- **kubectl** - Kubernetes command-line tool
- **curl** - For testing (optional but recommended)
- **wrk** - For load testing (optional)

### Installation Links
- **Minikube**: https://minikube.sigs.k8s.io/docs/start/
- **kubectl**: https://kubernetes.io/docs/tasks/tools/
- **Docker**: https://docs.docker.com/get-docker/

## 🏗️ Project Structure

```
messaging_app/
├── 🐳 Docker Configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── ☸️ Kubernetes Manifests
│   ├── deployment.yaml           # Basic deployment
│   ├── blue_deployment.yaml      # Blue version for blue-green
│   ├── green_deployment.yaml     # Green version for blue-green
│   ├── kubeservice.yaml          # Services for blue-green
│   └── ingress.yaml              # Ingress configuration
│
├── 📜 Kubernetes Scripts
│   ├── kurbeScript               # Cluster setup script
│   ├── kubctl-0x01              # Scaling script
│   ├── kubctl-0x02              # Blue-green deployment script
│   └── kubctl-0x03              # Rolling update script
│
└── 📚 Documentation
    ├── commands.txt              # Ingress setup commands
    ├── KUBERNETES_README.md      # This file
    └── DOCKER_README.md          # Docker documentation
```

## 🎯 Task Implementation

### Task 0: Kubernetes Cluster Setup ✅

**Script**: `kurbeScript`

**Features**:
- Checks for Minikube and kubectl installation
- Starts Minikube cluster with Docker driver
- Verifies cluster connectivity
- Retrieves available pods and cluster information
- Provides useful commands for cluster management

**Usage**:
```bash
chmod +x kurbeScript
./kurbeScript
```

### Task 1: Django App Deployment ✅

**File**: `deployment.yaml`

**Features**:
- Complete Kubernetes deployment manifest
- Django app containerization with resource limits
- ClusterIP service for internal access
- ConfigMap for environment configuration
- Health checks (liveness and readiness probes)
- Persistent volume mounting

**Deployment**:
```bash
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs <pod-name>
```

### Task 2: Application Scaling ✅

**Script**: `kubctl-0x01`

**Features**:
- Scales Django app to 3 replicas using `kubectl scale`
- Verifies multiple pods are running
- Performs load testing with `wrk`
- Monitors resource usage with `kubectl top`
- Provides comprehensive pod and deployment status

**Usage**:
```bash
chmod +x kubctl-0x01
./kubctl-0x01
```

### Task 3: Ingress Configuration ✅

**Files**: `ingress.yaml`, `commands.txt`

**Features**:
- Nginx Ingress controller setup
- Multiple domain routing (messaging-app.local, api.messaging-app.local)
- Path-based routing (/api/, /admin/)
- NodePort service for external access
- SSL redirect configuration

**Setup**:
```bash
# Enable Ingress addon
minikube addons enable ingress

# Apply Ingress configuration
kubectl apply -f ingress.yaml

# Add to hosts file
echo "$(minikube ip) messaging-app.local api.messaging-app.local" >> /etc/hosts
```

### Task 4: Blue-Green Deployment ✅

**Files**: `blue_deployment.yaml`, `green_deployment.yaml`, `kubeservice.yaml`, `kubctl-0x02`

**Features**:
- Separate blue and green deployments
- Traffic switching services
- Health check validation
- Automated deployment and verification
- ConfigMap for deployment state management

**Usage**:
```bash
chmod +x kubctl-0x02
./kubctl-0x02
```

### Task 5: Rolling Updates ✅

**Files**: `blue_deployment.yaml` (updated to v2.0), `kubctl-0x03`

**Features**:
- Updates Docker image to version 2.0
- Monitors rollout progress with `kubectl rollout status`
- Continuous availability testing during update
- Zero-downtime verification
- Rollback capabilities

**Usage**:
```bash
chmod +x kubctl-0x03
./kubctl-0x03
```

## 🔧 Detailed Configuration

### Deployment Specifications

#### Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### Health Checks
```yaml
livenessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Service Configuration

#### ClusterIP Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: django-messaging-service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: django-messaging-app
```

#### NodePort Service
```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8000
    nodePort: 30080
```

### Ingress Configuration

#### Domain-based Routing
```yaml
spec:
  rules:
  - host: messaging-app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: django-messaging-service
            port:
              number: 80
```

## 🚀 Deployment Strategies

### 1. Basic Deployment
- Single deployment with multiple replicas
- Simple scaling and updates
- Suitable for development and testing

### 2. Blue-Green Deployment
- Two identical production environments
- Instant traffic switching
- Zero downtime deployments
- Easy rollback capabilities

### 3. Rolling Updates
- Gradual replacement of old pods
- Configurable update strategy
- Continuous availability monitoring
- Automatic rollback on failure

## 📊 Monitoring and Testing

### Health Monitoring
```bash
# Check pod status
kubectl get pods -l app=django-messaging-app

# Check deployment status
kubectl get deployments

# View pod logs
kubectl logs -f deployment/django-messaging-app

# Monitor resource usage
kubectl top pods
kubectl top nodes
```

### Load Testing
```bash
# Install wrk (if not available)
sudo apt-get install wrk  # Ubuntu/Debian
brew install wrk          # macOS

# Run load test
wrk -t2 -c10 -d30s http://messaging-app.local/
```

### Availability Testing
```bash
# Continuous availability test
while true; do
  curl -s http://messaging-app.local/ > /dev/null && echo "✅ UP" || echo "❌ DOWN"
  sleep 1
done
```

## 🔄 Common Operations

### Scaling Operations
```bash
# Scale up
kubectl scale deployment django-messaging-app --replicas=5

# Scale down
kubectl scale deployment django-messaging-app --replicas=1

# Auto-scaling (HPA)
kubectl autoscale deployment django-messaging-app --cpu-percent=50 --min=1 --max=10
```

### Update Operations
```bash
# Update image
kubectl set image deployment/django-messaging-app django-app=messaging-app:2.0

# Check rollout status
kubectl rollout status deployment/django-messaging-app

# View rollout history
kubectl rollout history deployment/django-messaging-app

# Rollback to previous version
kubectl rollout undo deployment/django-messaging-app
```

### Traffic Management
```bash
# Switch to blue
kubectl patch service django-messaging-service-blue-green -p '{"spec":{"selector":{"version":"blue"}}}'

# Switch to green
kubectl patch service django-messaging-service-blue-green -p '{"spec":{"selector":{"version":"green"}}}'

# Canary deployment (split traffic)
kubectl patch service django-messaging-service-blue-green -p '{"spec":{"selector":{"app":"django-messaging-app"}}}'
```

## 🐛 Troubleshooting

### Common Issues

#### Pod Not Starting
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check resource constraints
kubectl top pods
kubectl describe nodes
```

#### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints

# Check service configuration
kubectl describe service <service-name>

# Test service connectivity
kubectl run test-pod --image=busybox --rm -it -- wget -qO- http://service-name
```

#### Ingress Issues
```bash
# Check ingress status
kubectl get ingress

# Check ingress controller logs
kubectl logs -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx

# Verify DNS resolution
nslookup messaging-app.local
```

### Performance Issues
```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Check cluster capacity
kubectl describe nodes

# Monitor metrics
kubectl get --raw /metrics
```

## 🔒 Security Considerations

### Production Deployment
1. **Resource Limits**: Always set resource requests and limits
2. **Security Context**: Run containers as non-root user
3. **Network Policies**: Implement network segmentation
4. **RBAC**: Configure role-based access control
5. **Secrets Management**: Use Kubernetes secrets for sensitive data
6. **Image Security**: Scan images for vulnerabilities

### Example Security Configuration
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  capabilities:
    drop:
    - ALL
```

## 📈 Performance Optimization

### Resource Optimization
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### Horizontal Pod Autoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: django-messaging-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: django-messaging-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 🎯 Best Practices

### Deployment Best Practices
1. **Use specific image tags** (avoid `latest`)
2. **Implement health checks** for all containers
3. **Set resource limits** to prevent resource starvation
4. **Use ConfigMaps and Secrets** for configuration
5. **Implement proper logging** and monitoring
6. **Test deployments** in staging environment first

### Operational Best Practices
1. **Monitor resource usage** regularly
2. **Implement backup strategies** for persistent data
3. **Use namespaces** for environment separation
4. **Implement CI/CD pipelines** for automated deployments
5. **Regular security updates** and vulnerability scanning
6. **Document all procedures** and runbooks

## 📚 Additional Resources

- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Minikube Documentation**: https://minikube.sigs.k8s.io/docs/
- **kubectl Cheat Sheet**: https://kubernetes.io/docs/reference/kubectl/cheatsheet/
- **Kubernetes Best Practices**: https://kubernetes.io/docs/concepts/configuration/overview/
- **Ingress Controllers**: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/

## ✅ Verification Checklist

### Task 0: Cluster Setup
- [ ] Minikube installed and running
- [ ] kubectl configured and working
- [ ] Cluster info accessible
- [ ] Pods listing working

### Task 1: Basic Deployment
- [ ] Deployment manifest applied
- [ ] Pods running successfully
- [ ] Service accessible internally
- [ ] Logs showing no errors

### Task 2: Scaling
- [ ] Deployment scaled to 3 replicas
- [ ] All pods running and ready
- [ ] Load testing completed
- [ ] Resource monitoring working

### Task 3: Ingress
- [ ] Ingress controller enabled
- [ ] Ingress resource created
- [ ] Domain names configured
- [ ] External access working

### Task 4: Blue-Green Deployment
- [ ] Blue deployment running
- [ ] Green deployment running
- [ ] Traffic switching working
- [ ] Health checks passing

### Task 5: Rolling Updates
- [ ] Image updated to version 2.0
- [ ] Rolling update completed
- [ ] Zero downtime achieved
- [ ] All pods updated successfully

---

**Status**: ✅ All Kubernetes tasks completed successfully!

The Django messaging app is now fully deployed on Kubernetes with advanced deployment strategies, monitoring, and management capabilities.
