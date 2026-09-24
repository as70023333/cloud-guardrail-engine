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

### AWS STS Session Revocation

When an IAM role is quarantined, the AWS provider attaches an inline boundary policy that invalidates all existing temporary STS credentials:

1. **Token Issue Time Check**: Creates a timestamp-based deny policy using `aws:TokenIssueTime` condition
2. **Dynamic Policy Naming**: Each quarantine creates a uniquely-named policy with timestamp (e.g., `Quarantine-RevokeOlderSessions-1705312800`)
3. **Immediate Effect**: All STS sessions issued before the quarantine timestamp are instantly denied
4. **No Session Tracking Required**: Leverages AWS IAM's built-in token validation without needing to track individual sessions

**Policy Structure:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "RevokeOlderSessions",
    "Effect": "Deny",
    "Action": "*",
    "Resource": "*",
    "Condition": {
      "DateLessThan": {
        "aws:TokenIssueTime": "2024-01-15T10:30:00Z"
      }
    }
  }]
}
```

### Azure Entra ID Session Revocation

When a user is quarantined, the Azure provider performs two critical actions:

1. **Refresh Token Revocation**: Calls Microsoft Graph API's `revokeSignInSessions` endpoint to invalidate all active OAuth refresh tokens
2. **Account Disable**: Sets `accountEnabled = false` to prevent any new sign-ins
3. **Immediate Effect**: Existing sessions lose their ability to refresh tokens, forcing re-authentication
4. **Comprehensive Coverage**: Revokes tokens across all Microsoft 365 services (Teams, SharePoint, Exchange, etc.)

**Authentication Methods:**
- Managed Identity (recommended for Azure-hosted deployments)
- Azure CLI credentials (for local development)
- Service Principal via environment variables (for CI/CD)

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

### Test Execution & Usage

Start the server locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
QUARANTINE_API_SECRET="test-secret-123" uvicorn main:app --reload --port 8080
```

Trigger a sample identity quarantine request via curl:

```bash
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
