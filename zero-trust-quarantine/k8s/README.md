# Kubernetes Deployment Guide for Zero-Trust Quarantine Engine

This guide provides instructions for deploying the Zero-Trust Quarantine Engine to Kubernetes.

## Prerequisites

- Kubernetes cluster (v1.23+)
- `kubectl` configured with cluster access
- Container registry access (Docker Hub, ECR, GCR, etc.)
- AWS credentials (IAM role or access keys)
- Azure credentials (Service Principal or Managed Identity)

## File Structure

```
k8s/
├── deployment.yaml       # Complete Kubernetes manifests
└── README.md            # This file
```

## Components

The `deployment.yaml` contains the following Kubernetes resources:

1. **ConfigMap** (`zero-trust-quarantine-config`)
   - Non-sensitive configuration values
   - API host, port, log level
   - AWS region, Azure tenant/client IDs

2. **Secret** (`zero-trust-quarantine-secrets`)
   - Sensitive credentials
   - API secret token
   - AWS access keys
   - Azure client secret

3. **Deployment** (`zero-trust-quarantine`)
   - 2 replicas for high availability
   - Resource limits and requests
   - Health checks (readiness, liveness, startup probes)
   - Security context (non-root, read-only filesystem)

4. **Service** (`zero-trust-quarantine`)
   - ClusterIP service
   - Exposes port 80 → 8080

5. **HorizontalPodAutoscaler** (`zero-trust-quarantine-hpa`)
   - Auto-scales from 2 to 10 replicas
   - Based on CPU (70%) and memory (80%) utilization

6. **NetworkPolicy** (`zero-trust-quarantine-network-policy`)
   - Restricts ingress to specific namespaces
   - Allows egress for DNS and cloud APIs

7. **PodDisruptionBudget** (`zero-trust-quarantine-pdb`)
   - Ensures at least 1 pod available during disruptions

## Deployment Steps

### 1. Build and Push Docker Image

```bash
# Build the image
docker build -t your-registry/zero-trust-quarantine:1.0.0 .

# Push to registry
docker push your-registry/zero-trust-quarantine:1.0.0
```

### 2. Create Namespace

```bash
kubectl create namespace security
```

### 3. Update Configuration

Edit `deployment.yaml` and update:

- **ConfigMap**: Set your AWS region, Azure tenant ID, and client ID
- **Secret**: Set your actual credentials (or use external secrets management)
- **Deployment**: Update the image reference to your registry

### 4. Apply Manifests

```bash
# Apply all resources
kubectl apply -f k8s/deployment.yaml

# Verify deployment
kubectl get all -n security -l app=zero-trust-quarantine
```

### 5. Verify Deployment

```bash
# Check pod status
kubectl get pods -n security -l app=zero-trust-quarantine

# Check logs
kubectl logs -n security deployment/zero-trust-quarantine

# Test health endpoint
kubectl port-forward -n security svc/zero-trust-quarantine 8080:80
curl http://localhost:8080/healthz
```

## Configuration

### ConfigMap Values

| Key | Description | Default |
|-----|-------------|---------|
| `API_HOST` | API bind address | `0.0.0.0` |
| `API_PORT` | API port | `8080` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `AWS_REGION` | AWS region | `us-east-1` |
| `AZURE_TENANT_ID` | Azure AD tenant ID | - |
| `AZURE_CLIENT_ID` | Azure app client ID | - |

### Secret Values

| Key | Description |
|-----|-------------|
| `QUARANTINE_API_SECRET` | API authentication token |
| `AWS_ACCESS_KEY_ID` | AWS access key (optional if using IAM roles) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key (optional if using IAM roles) |
| `AZURE_CLIENT_SECRET` | Azure app client secret |

## Security Best Practices

### 1. Use External Secrets Management

Instead of storing secrets in Kubernetes, use:
- **AWS Secrets Manager** with External Secrets Operator
- **Azure Key Vault** with Secrets Store CSI Driver
- **HashiCorp Vault** with Vault Agent Injector

Example with External Secrets:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: zero-trust-quarantine-secrets
  namespace: security
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: zero-trust-quarantine-secrets
  data:
  - secretKey: QUARANTINE_API_SECRET
    remoteRef:
      key: zero-trust-quarantine/api-secret
```

### 2. Use IAM Roles for Service Accounts (IRSA)

For AWS EKS, use IAM roles instead of access keys:

```yaml
# Add annotation to service account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: zero-trust-quarantine
  namespace: security
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/QuarantineEngineRole
```

### 3. Use Workload Identity for GKE

For Google Kubernetes Engine:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: zero-trust-quarantine
  namespace: security
  annotations:
    iam.gke.io/gcp-service-account: quarantine-engine@project-id.iam.gserviceaccount.com
```

### 4. Enable Pod Security Standards

Apply restricted pod security standards:

```bash
kubectl label namespace security \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/audit=restricted \
  pod-security.kubernetes.io/warn=restricted
```

## Monitoring

### Prometheus Metrics

The application exposes metrics at `/metrics` (if implemented). Configure Prometheus:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: zero-trust-quarantine
  namespace: security
spec:
  selector:
    matchLabels:
      app: zero-trust-quarantine
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

### Logging

Configure log aggregation (ELK, Loki, CloudWatch):

```yaml
# Example Fluent Bit configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [INPUT]
        Name              tail
        Path              /var/log/containers/zero-trust-quarantine-*.log
    
    [OUTPUT]
        Name              es
        Match             *
        Host              elasticsearch
        Port              9200
        Index             zero-trust-quarantine
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment zero-trust-quarantine -n security --replicas=5
```

### Auto-Scaling

The HPA is configured to scale based on CPU and memory:

```bash
# View HPA status
kubectl get hpa -n security

# Describe HPA
kubectl describe hpa zero-trust-quarantine-hpa -n security
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod events
kubectl describe pod -n security -l app=zero-trust-quarantine

# Check pod logs
kubectl logs -n security -l app=zero-trust-quarantine --previous
```

### Health Check Failures

```bash
# Port forward and test manually
kubectl port-forward -n security svc/zero-trust-quarantine 8080:80
curl -v http://localhost:8080/healthz
```

### Network Policy Issues

```bash
# Test connectivity
kubectl run test --rm -it --image=busybox -n security -- wget -qO- http://zero-trust-quarantine:80/healthz
```

## Rollback

```bash
# View deployment history
kubectl rollout history deployment/zero-trust-quarantine -n security

# Rollback to previous version
kubectl rollout undo deployment/zero-trust-quarantine -n security

# Rollback to specific revision
kubectl rollout undo deployment/zero-trust-quarantine -n security --to-revision=2
```

## Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/deployment.yaml

# Delete namespace
kubectl delete namespace security
```

## Production Checklist

- [ ] Update image reference to production registry
- [ ] Configure external secrets management
- [ ] Set up IAM roles / Workload Identity
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Enable network policies
- [ ] Configure ingress with TLS
- [ ] Set up backup and disaster recovery
- [ ] Document runbooks for incident response
- [ ] Conduct security review and penetration testing
- [ ] Load test the deployment
- [ ] Configure CI/CD pipeline for automated deployments

## Support

For issues and questions:
- Check logs: `kubectl logs -n security deployment/zero-trust-quarantine`
- Review events: `kubectl get events -n security --sort-by='.metadata.creationTimestamp'`
- Contact: security-team@company.com
