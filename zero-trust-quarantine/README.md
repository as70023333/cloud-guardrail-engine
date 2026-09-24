# Zero-Trust Quarantine Engine

Production-ready prototype for instant cross-cloud identity quarantine. This event-driven API daemon listens for high-risk identity alerts (via webhooks from SIEM, GuardDuty, or Entra ID Risk Detections) and immediately triggers cross-cloud identity quarantine by invalidating active sessions.

## 🎯 Overview

The Zero-Trust Quarantine Engine provides:
- **Instant Session Revocation**: Invalidate all active sessions across AWS and Azure within seconds
- **Cross-Cloud Coordination**: Simultaneously quarantine identities in multiple cloud providers
- **Event-Driven Architecture**: FastAPI webhook ingestion for real-time threat response
- **Zero-Trust Enforcement**: Follows zero-trust principles by assuming breach and responding instantly

## 📁 Repository Structure

```
zero-trust-quarantine/
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── main.py                         # FastAPI webhook ingestion API
├── config.py                       # Environment & API configurations
├── providers/
│   ├── __init__.py
│   ├── aws_quarantine.py          # AWS IAM & STS session invalidation
│   └── azure_quarantine.py        # Azure Entra ID session revocation
├── tests/
│   └── test_payloads.py           # Webhook test fixtures
└── Dockerfile                      # Container definition
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- AWS credentials (optional - can use IAM roles)
- Azure AD application credentials (optional - can use managed identity)

### Local Development

1. **Clone and setup environment**:
```bash
cd zero-trust-quarantine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Run the API server**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Test health endpoint**:
```bash
curl http://localhost:8000/healthz
```

### Docker Deployment

```bash
# Build the image
docker build -t zero-trust-quarantine:latest .

# Run the container
docker run -d \
  --name quarantine-engine \
  -p 8000:8000 \
  --env-file .env \
  zero-trust-quarantine:latest
```

## 🔐 API Endpoints

### POST /api/v1/quarantine

Trigger identity quarantine across cloud providers.

**Headers:**
```
X-API-Token: your-secret-token
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_principal_name": "alex.salazar@company.com",
  "aws_iam_role_name": "DeveloperRole",
  "reason": "Impossible travel detected",
  "risk_score": 9.5
}
```

**Response:**
```json
{
  "status": "completed",
  "user_principal_name": "alex.salazar@company.com",
  "actions_taken": {
    "azure_entra": true,
    "aws_sts": true
  }
}
```

### GET /healthz

Health check endpoint for monitoring and load balancers.

**Response:**
```json
{
  "status": "healthy"
}
```

## 🛡️ Security Features

### AWS Quarantine Actions

When an IAM role is quarantined:
1. **Policy Detachment**: All managed policies are detached from the role
2. **Inline Policy Removal**: All inline policies are deleted
3. **Trust Policy Update**: Role trust policy is updated to deny all `sts:AssumeRole` actions
4. **Session Invalidation**: Active sessions are effectively invalidated

### Azure Entra ID Quarantine Actions

When a user is quarantined:
1. **Session Revocation**: All active sessions are revoked via Microsoft Graph API
2. **Token Invalidation**: All refresh tokens are invalidated
3. **Forced Re-authentication**: User must re-authenticate on next access

## 📊 Integration Examples

### AWS GuardDuty Integration

```python
import requests
import json

# GuardDuty CloudWatch Event -> Lambda -> Quarantine API
def handle_guardduty_finding(event):
    finding = event['detail']
    
    if finding['severity'] >= 8.0:
        payload = {
            "user_principal_name": f"{finding['resource']['accessKeyDetails']['userName']}@company.com",
            "aws_iam_role_name": finding['resource']['accessKeyDetails'].get('principalId'),
            "reason": f"GuardDuty Finding: {finding['title']}",
            "risk_score": finding['severity']
        }
        
        response = requests.post(
            "http://quarantine-engine:8000/api/v1/quarantine",
            headers={"X-API-Token": "your-secret-token"},
            json=payload
        )
        
        return response.json()
```

### Azure Entra ID Risk Detection Integration

```python
from azure.identity import DefaultAzureCredential
from azure.eventgrid import EventGridSubscriber

def handle_risk_detection(event):
    risk_detection = event.data
    
    if risk_detection['riskLevel'] in ['high', 'medium']:
        payload = {
            "user_principal_name": risk_detection['userPrincipalName'],
            "reason": f"Entra ID Risk: {risk_detection['riskEventType']}",
            "risk_score": map_risk_level(risk_detection['riskLevel'])
        }
        
        response = requests.post(
            "http://quarantine-engine:8000/api/v1/quarantine",
            headers={"X-API-Token": "your-secret-token"},
            json=payload
        )
```

### SIEM Webhook Integration

```python
# Generic SIEM webhook handler
@app.post("/webhook/siem")
async def siem_webhook(alert: dict):
    # Transform SIEM alert to quarantine request
    if alert.get('severity') == 'high':
        payload = {
            "user_principal_name": alert['user']['email'],
            "reason": f"SIEM Alert: {alert['category']} - {alert['subcategory']}",
            "risk_score": alert.get('risk_score', 8.0)
        }
        
        # Forward to quarantine engine
        await trigger_quarantine(payload)
```

## 🧪 Testing

### Run Test Payloads

```bash
python tests/test_payloads.py
```

### Manual API Testing

```bash
# Test quarantine request
curl -X POST http://localhost:8000/api/v1/quarantine \
  -H "X-API-Token: your-secret-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_principal_name": "test.user@company.com",
    "aws_iam_role_name": "TestRole",
    "reason": "Manual test",
    "risk_score": 7.5
  }'
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `QUARANTINE_API_SECRET` | API authentication token | Yes |
| `AWS_REGION` | AWS region for IAM operations | No (defaults to us-east-1) |
| `AWS_ACCESS_KEY_ID` | AWS access key | No (can use IAM roles) |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | No (can use IAM roles) |
| `AZURE_TENANT_ID` | Azure AD tenant ID | No (can use managed identity) |
| `AZURE_CLIENT_ID` | Azure application client ID | No (can use managed identity) |
| `AZURE_CLIENT_SECRET` | Azure application client secret | No (can use managed identity) |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No (defaults to INFO) |

## 🏗️ Architecture

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
│  │  - Event Dispatching                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Provider Orchestration                              │  │
│  │  - AWS Quarantine Provider                           │  │
│  │  - Azure Quarantine Provider                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌───────────────┐        ┌───────────────┐
│  AWS Cloud    │        │  Azure Cloud  │
│  - IAM        │        │  - Entra ID   │
│  - STS        │        │  - Graph API  │
│  - Sessions   │        │  - Sessions   │
└───────────────┘        └───────────────┘
```

## 🚨 Production Considerations

### Security
- **Never commit .env files** - Use secrets management (AWS Secrets Manager, Azure Key Vault)
- **Rotate API tokens regularly** - Implement token rotation policy
- **Use IAM roles** - Prefer IAM roles over access keys where possible
- **Enable audit logging** - Log all quarantine actions for compliance
- **Implement rate limiting** - Prevent abuse of quarantine API

### Reliability
- **Deploy with high availability** - Use multiple replicas behind load balancer
- **Implement circuit breakers** - Handle cloud provider outages gracefully
- **Add retry logic** - Retry failed operations with exponential backoff
- **Monitor health endpoints** - Integrate with monitoring systems

### Compliance
- **Document quarantine procedures** - Maintain runbooks for incident response
- **Implement approval workflows** - Consider human-in-the-loop for critical actions
- **Audit trail** - Maintain detailed logs of all quarantine actions
- **Data retention** - Define log retention policies per compliance requirements

## 📝 License

This is a prototype implementation for demonstration purposes.

## 🤝 Contributing

This is a production-ready prototype. For production deployments:
1. Implement proper secrets management
2. Add comprehensive logging and monitoring
3. Set up automated testing and CI/CD
4. Implement proper error handling and retry logic
5. Add metrics and alerting
6. Conduct security review and penetration testing

## 📞 Support

For issues and questions, please open an issue in the repository.
