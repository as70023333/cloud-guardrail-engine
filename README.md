# Awesome Security Engineer

<div align="center">

**Production-Ready Cloud Security Solutions for Multi-Cloud Environments**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Go](https://img.shields.io/badge/Go-1.22+-00ADD8?logo=go&logoColor=white)](https://golang.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)

</div>

---

## 🎯 The Problem We Solve

**Security breaches cost an average of $4.45M per incident.** In multi-cloud environments, the challenge is twofold:

1. **Prevention**: How do you catch security violations *before* infrastructure is deployed?
2. **Response**: How do you instantly revoke compromised sessions *across multiple clouds*?

This repository provides **production-ready, enterprise-grade solutions** for both challenges.

## 📚 Overview

This repository showcases two critical security engineering projects:

1. **[Cloud Guardrail Engine](#cloud-guardrail-engine)** - Prevent security violations before deployment with policy-as-code
2. **[Zero-Trust Quarantine Engine](#zero-trust-quarantine-engine)** - Instantly revoke compromised sessions across AWS and Azure

Both projects are **production-ready** with comprehensive testing, CI/CD pipelines, Kubernetes orchestration, and full documentation.

---

## 💼 Business Impact

### For Security Teams
- **Reduce MTTR**: Cut mean-time-to-remediation from hours to seconds
- **Shift-Left Security**: Catch violations before deployment, not after
- **Unified Posture**: Consistent security policies across AWS and Azure
- **Audit Ready**: Comprehensive logging and compliance reporting

### For Engineering Teams
- **Developer Velocity**: Fast feedback loops with CI/CD integration
- **Policy as Code**: Version-controlled, tested, and reviewed security policies
- **Self-Service**: Engineers can validate their own infrastructure changes
- **Clear Ownership**: Explicit policy violations with actionable remediation steps

### For Business Leaders
- **Risk Reduction**: Automated enforcement reduces human error
- **Cost Savings**: Prevent costly security breaches and compliance violations
- **Scalability**: Solutions that grow with your organization
- **Competitive Advantage**: Demonstrate mature security practices to customers

---

## 🛡️ Cloud Guardrail Engine

**Location:** [`cloud-guardrail-engine/`](https://github.com/as70023333/awesome-security-engineer/tree/main/cloud-guardrail-engine)

A Go-based CLI tool that evaluates Terraform plan JSON output against Open Policy Agent (OPA) Rego policies to enforce cloud security guardrails before infrastructure changes are applied.

### Key Features

- ✅ Multi-cloud policy support (AWS & Azure)
- ✅ OPA Rego policy evaluation with unit tests
- ✅ JSON-formatted compliance reports
- ✅ CI/CD integration with GitHub Actions
- ✅ Comprehensive test coverage

### Quick Start

```bash
# Navigate to the project directory
cd cloud-guardrail-engine

# Build the binary
make build

# Run against mock Terraform plan
make run-mock

# Run OPA policy unit tests
make test-policies
```

### Project Structure

```
cloud-guardrail-engine/
├── main.go                                    # CLI entrypoint
├── go.mod                                     # Go module definition
├── Makefile                                   # Build automation
├── policies/
│   ├── aws_s3_encryption.rego                # AWS S3 encryption policy
│   ├── aws_s3_encryption_test.rego           # AWS policy unit tests
│   ├── azure_storage_https.rego              # Azure HTTPS enforcement policy
│   └── azure_storage_https_test.rego         # Azure policy unit tests
└── tests/
    └── mock_tfplan.json                      # Test fixture
```

### Documentation

- **[Full Documentation](https://github.com/as70023333/awesome-security-engineer/tree/main/cloud-guardrail-engine)** - Complete project details
- **[CI/CD Pipeline](https://github.com/as70023333/awesome-security-engineer/blob/main/.github/workflows/ci.yml)** - GitHub Actions workflow
- **[Policy Examples](https://github.com/as70023333/awesome-security-engineer/tree/main/cloud-guardrail-engine/policies)** - OPA Rego policies

### Expected Output

```json
{
  "compliant": false,
  "violations": [
    "[aws] AWS S3 bucket 'unencrypted_bucket' must have server-side encryption enabled.",
    "[azure] Azure Storage Account 'insecure_storage' must enforce HTTPS traffic only."
  ]
}
```

---

## 🔐 Zero-Trust Quarantine Engine

**Location:** [`zero-trust-quarantine/`](https://github.com/as70023333/awesome-security-engineer/tree/main/zero-trust-quarantine)

A production-ready FastAPI-based event-driven API daemon that listens for high-risk identity alerts and immediately triggers cross-cloud identity quarantine by invalidating active sessions in AWS and Azure.

### Key Features

- ✅ Instant cross-cloud session revocation (AWS STS & Azure Entra ID)
- ✅ FastAPI webhook ingestion with token authentication
- ✅ AWS IAM token issue time-based session invalidation
- ✅ Azure Entra ID refresh token revocation
- ✅ Kubernetes-ready with comprehensive manifests
- ✅ Docker containerization with security hardening

### Quick Start

```bash
# Navigate to the project directory
cd zero-trust-quarantine

# Install dependencies
pip install -r requirements.txt

# Start the API server
QUARANTINE_API_SECRET="test-secret-123" uvicorn main:app --reload --port 8080

# Trigger a quarantine request
curl -X POST http://localhost:8080/api/v1/quarantine \
  -H "Content-Type: application/json" \
  -H "X-API-Token: test-secret-123" \
  -d '{
    "user_principal_name": "compromised.user@company.com",
    "aws_iam_role_name": "Developer-PowerUser-Role",
    "reason": "Anomalous login location & impossible travel detected",
    "risk_score": 0.95
  }'
```

### Project Structure

```
zero-trust-quarantine/
├── main.py                          # FastAPI webhook ingestion API
├── config.py                        # Environment configuration
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Production container image
├── providers/
│   ├── aws_quarantine.py           # AWS STS session revocation
│   └── azure_quarantine.py         # Azure Entra ID session revocation
├── tests/
│   └── test_payloads.py            # Webhook test fixtures
└── k8s/
    ├── deployment.yaml             # Kubernetes manifests
    └── README.md                   # K8s deployment guide
```

### Documentation

- **[Full Documentation](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/README.md)** - Complete project details
- **[Kubernetes Deployment Guide](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/k8s/README.md)** - K8s orchestration
- **[Docker Configuration](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/Dockerfile)** - Container setup
- **[API Documentation](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/main.py)** - FastAPI endpoints

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    External Threat Sources                   │
│  (SIEM, GuardDuty, Entra ID Risk, Custom Alerts)           │
└────────────────────┬────────────────────────────────────────┘
                     │ Webhook (HTTPS)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Zero-Trust Quarantine Engine                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI Webhook Ingestion (main.py)                 │  │
│  │  - Authentication (X-API-Token)                      │  │
│  │  - Request Validation (Pydantic)                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Provider Orchestration                              │  │
│  │  - AWS Quarantine Provider (STS token revocation)    │  │
│  │  - Azure Quarantine Provider (Entra ID revocation)   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌───────────────┐        ┌───────────────┐
│  AWS Cloud    │        │  Azure Cloud  │
│  - IAM        │        │  - Entra ID   │
│  - STS        │        │  - Graph API  │
└───────────────┘        └───────────────┘
```

---

## 🌐 Live Demo

**Interactive Portfolio**: [View the Live Demo](https://as70023333.github.io/awesome-security-engineer/)

Explore the architecture, features, and capabilities of both security engines through our interactive web interface.

---

## 🚀 Getting Started

### Prerequisites

**For Cloud Guardrail Engine:**
- Go 1.22+
- OPA CLI (for policy testing)
- Make

**For Zero-Trust Quarantine Engine:**
- Python 3.11+
- Docker (optional, for containerization)
- Kubernetes cluster (optional, for production deployment)
- AWS credentials (optional)
- Azure credentials (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/as70023333/awesome-security-engineer.git
cd awesome-security-engineer

# Choose your project
cd cloud-guardrail-engine    # For OPA policy engine
# OR
cd zero-trust-quarantine     # For identity quarantine engine
```

---

## 📖 Documentation

### Cloud Guardrail Engine

| Document | Description |
|----------|-------------|
| [Project README](https://github.com/as70023333/awesome-security-engineer/tree/main/cloud-guardrail-engine) | Main project documentation |
| [OPA Policies](https://github.com/as70023333/awesome-security-engineer/tree/main/cloud-guardrail-engine/policies) | Rego policy files |
| [AWS S3 Policy](https://github.com/as70023333/awesome-security-engineer/blob/main/cloud-guardrail-engine/policies/aws_s3_encryption.rego) | AWS S3 encryption enforcement |
| [Azure Storage Policy](https://github.com/as70023333/awesome-security-engineer/blob/main/cloud-guardrail-engine/policies/azure_storage_https.rego) | Azure HTTPS enforcement |
| [CI/CD Pipeline](https://github.com/as70023333/awesome-security-engineer/blob/main/.github/workflows/ci.yml) | GitHub Actions workflow |
| [Test Fixtures](https://github.com/as70023333/awesome-security-engineer/blob/main/cloud-guardrail-engine/tests/mock_tfplan.json) | Mock Terraform plan |

### Zero-Trust Quarantine Engine

| Document | Description |
|----------|-------------|
| [Project README](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/README.md) | Main project documentation |
| [Kubernetes Guide](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/k8s/README.md) | K8s deployment instructions |
| [K8s Manifests](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/k8s/deployment.yaml) | Complete K8s resources |
| [Dockerfile](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/Dockerfile) | Container configuration |
| [AWS Provider](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/providers/aws_quarantine.py) | AWS STS revocation |
| [Azure Provider](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/providers/azure_quarantine.py) | Azure Entra ID revocation |
| [API Implementation](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/main.py) | FastAPI endpoints |
| [Test Payloads](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/tests/test_payloads.py) | Webhook test fixtures |

---

## 🔧 Development

### Cloud Guardrail Engine

```bash
cd cloud-guardrail-engine

# Install dependencies
make deps

# Run all tests
make test

# Run linters
make lint

# Build binary
make build

# Run OPA policy tests
make test-policies

# Execute against mock data
make run-mock
```

### Zero-Trust Quarantine Engine

```bash
cd zero-trust-quarantine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
QUARANTINE_API_SECRET="dev-secret" uvicorn main:app --reload --port 8080

# Run test payloads
python tests/test_payloads.py

# Build Docker image
docker build -t zero-trust-quarantine:latest .

# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml
```

---

## 🧪 Testing

### Cloud Guardrail Engine

```bash
# Run OPA policy unit tests
cd cloud-guardrail-engine
make test-policies

# Expected output:
# cloud.guardrail.aws_test:
#   PASS: test_deny_unencrypted_s3_bucket
#   PASS: test_allow_encrypted_s3_bucket
# cloud.guardrail.azure_test:
#   PASS: test_deny_http_azure_storage
#   PASS: test_allow_https_azure_storage
# PASS: 4/4
```

### Zero-Trust Quarantine Engine

```bash
# Test health endpoint
curl http://localhost:8080/healthz

# Test quarantine endpoint
curl -X POST http://localhost:8080/api/v1/quarantine \
  -H "Content-Type: application/json" \
  -H "X-API-Token: test-secret-123" \
  -d '{
    "user_principal_name": "test.user@company.com",
    "aws_iam_role_name": "TestRole",
    "reason": "Test quarantine",
    "risk_score": 0.85
  }'
```

---

## 🏗️ Architecture

### Cloud Guardrail Engine

```
Terraform Plan JSON
       ↓
┌──────────────────┐
│  OPA Rego Engine │
│  (main.go)       │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Policy Loader   │
│  (rego.Load)     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  Evaluation      │
│  (data.cloud.    │
│   guardrail)     │
└────────┬─────────┘
         ↓
┌──────────────────┐
│  JSON Report     │
│  {compliant,     │
│   violations}    │
└──────────────────┘
```

### Zero-Trust Quarantine Engine

See [Architecture Diagram](#architecture-1) above.

---

## 🔒 Security

### Cloud Guardrail Engine

- **Policy as Code**: OPA Rego policies enforce security standards
- **Shift-Left Security**: Validates infrastructure before deployment
- **Compliance Automation**: Automated compliance checking for AWS and Azure
- **CI/CD Integration**: GitHub Actions pipeline with multi-stage security checks

### Zero-Trust Quarantine Engine

- **Zero-Trust Principles**: Assumes breach, responds instantly
- **Token-Based Authentication**: API secret token validation
- **Non-Root Containers**: Kubernetes security best practices
- **Network Policies**: Traffic isolation in Kubernetes
- **Read-Only Filesystem**: Container security hardening
- **Immediate Session Revocation**: AWS STS token issue time + Azure refresh token revocation

---

## 📊 Monitoring & Observability

### Cloud Guardrail Engine

- JSON-formatted compliance reports
- Exit code 1 on violations (CI/CD friendly)
- Detailed violation messages with resource names
- Severity levels (CRITICAL, HIGH, MEDIUM)

### Zero-Trust Quarantine Engine

- Health check endpoint (`/healthz`)
- Structured logging with timestamps
- Kubernetes health probes (readiness, liveness, startup)
- Prometheus metrics ready
- Audit logging for all quarantine actions

---

## 🚢 Deployment

### Cloud Guardrail Engine

```bash
# Build binary
cd cloud-guardrail-engine
make build

# Run in CI/CD
./bin/cloud-guardrail -plan terraform.json -policies ./policies
```

### Zero-Trust Quarantine Engine

**Docker:**
```bash
docker build -t zero-trust-quarantine:1.0.0 .
docker run -p 8080:8080 --env-file .env zero-trust-quarantine:1.0.0
```

**Kubernetes:**
```bash
kubectl create namespace security
kubectl apply -f k8s/deployment.yaml
kubectl get pods -n security -l app=zero-trust-quarantine
```

See [Kubernetes Deployment Guide](https://github.com/as70023333/awesome-security-engineer/blob/main/zero-trust-quarantine/k8s/README.md) for complete instructions.

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- **Go**: Follow standard Go conventions, run `gofmt`
- **Python**: Follow PEP 8, use type hints
- **Rego**: Follow OPA best practices, include unit tests
- **Kubernetes**: Follow security best practices (non-root, read-only, resource limits)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

For issues, questions, or contributions:

- **Issues**: [GitHub Issues](https://github.com/as70023333/awesome-security-engineer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/as70023333/awesome-security-engineer/discussions)
- **Email**: security-team@company.com

---

## 🙏 Acknowledgments

- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) - Policy engine
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [Microsoft Graph API](https://docs.microsoft.com/en-us/graph/api/overview) - Azure Entra ID integration
- [AWS SDK for Go](https://aws.amazon.com/sdk-for-go/) - AWS IAM integration
- [Azure SDK for Python](https://docs.microsoft.com/en-us/azure/developer/python/) - Azure integration

---

## 📚 Additional Resources

### Cloud Security

- [AWS Security Best Practices](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [Azure Security Center](https://azure.microsoft.com/en-us/services/security-center/)
- [Terraform Security](https://www.terraform.io/docs/cloud/sentinel/index.html)
- [OPA Documentation](https://www.openpolicyagent.org/docs/latest/)

### Zero Trust

- [NIST Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [AWS Zero Trust](https://aws.amazon.com/security/zero-trust/)
- [Microsoft Zero Trust](https://www.microsoft.com/en-us/security/business/zero-trust)
- [BeyondCorp](https://cloud.google.com/beyondcorp)

### Kubernetes Security

- [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

---

## 🗺️ Roadmap

### Cloud Guardrail Engine

- [ ] Support for additional cloud providers (GCP, Oracle Cloud)
- [ ] Custom policy templates library
- [ ] Web dashboard for policy management
- [ ] Integration with Terraform Cloud
- [ ] Policy versioning and rollback

### Zero-Trust Quarantine Engine

- [ ] Support for GCP Workload Identity
- [ ] Integration with SOAR platforms
- [ ] Automated incident response playbooks
- [ ] Multi-tenant support
- [ ] Advanced analytics and reporting

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/as70023333/awesome-security-engineer?style=social)
![GitHub forks](https://img.shields.io/github/forks/as70023333/awesome-security-engineer?style=social)
![GitHub issues](https://img.shields.io/github/issues/as70023333/awesome-security-engineer)
![GitHub pull requests](https://img.shields.io/github/issues-pr/as70023333/awesome-security-engineer)
![GitHub license](https://img.shields.io/github/license/as70023333/awesome-security-engineer)

---

**Built with ❤️ by security engineers, for security engineers.**
