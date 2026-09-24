"""
Webhook Test Fixtures for Zero-Trust Quarantine Engine

This module contains sample webhook payloads from various SIEM and cloud
security services that can trigger the quarantine engine.
"""

# Sample GuardDuty Finding - IAM Credential Compromise
GUARDDUTY_IAM_COMPROMISE = {
    "schemaVersion": "2.0",
    "id": "1234567890abcdef1234567890abcdef",
    "partition": "aws",
    "region": "us-east-1",
    "account": "123456789012",
    "type": "UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration",
    "resource": {
        "resourceType": "AccessKey",
        "accessKeyDetails": {
            "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "principalId": "AIDAJKLMNOPQRSTUVWXYZ",
            "userType": "IAMUser",
            "userName": "compromised-user"
        }
    },
    "service": {
        "serviceName": "guardduty",
        "count": 5,
        "archived": False,
        "action": {
            "actionType": "AWS_API_CALL",
            "awsApiCallAction": {
                "api": "AssumeRole",
                "serviceName": "sts.amazonaws.com"
            }
        },
        "eventFirstSeen": "2024-01-15T10:30:00Z",
        "eventLastSeen": "2024-01-15T10:45:00Z",
        "severity": 8.5
    },
    "severity": 8.5,
    "title": "EC2 instance credentials were used to call AWS APIs from an external IP address"
}

# Sample Entra ID Risk Detection - Impossible Travel
ENTRA_ID_IMPOSSIBLE_TRAVEL = {
    "id": "risk-detection-12345",
    "createdDateTime": "2024-01-15T10:30:00Z",
    "riskEventType": "impossibleTravel",
    "riskState": "atRisk",
    "riskLevel": "high",
    "riskDetail": "none",
    "source": "IdentityProtection",
    "detectionTimingType": "realtime",
    "userPrincipalName": "alex.salazar@company.com",
    "userDisplayName": "Alex Salazar",
    "userId": "12345678-1234-1234-1234-123456789012",
    "ipAddress": "203.0.113.42",
    "location": {
        "city": "Moscow",
        "state": "Moscow",
        "countryOrRegion": "RU",
        "geoCoordinates": {
            "latitude": 55.7558,
            "longitude": 37.6173
        }
    },
    "activity": {
        "riskEventType": "impossibleTravel",
        "eventTypes": ["signin"],
        "tokenIssuerType": "AzureAD"
    }
}

# Sample SIEM Alert - Multiple Failed Login Attempts
SIEM_BRUTE_FORCE_ALERT = {
    "alert_id": "ALERT-2024-001234",
    "timestamp": "2024-01-15T10:30:00Z",
    "severity": "high",
    "category": "Authentication",
    "subcategory": "Brute Force",
    "source": "corporate-siem",
    "user": {
        "username": "alex.salazar@company.com",
        "email": "alex.salazar@company.com",
        "department": "Engineering"
    },
    "details": {
        "failed_attempts": 47,
        "time_window_minutes": 5,
        "source_ips": [
            "198.51.100.23",
            "198.51.100.24",
            "198.51.100.25"
        ],
        "target_services": [
            "Azure Portal",
            "AWS Console",
            "Corporate VPN"
        ]
    },
    "risk_score": 9.2,
    "recommended_actions": [
        "QUARANTINE_USER",
        "RESET_CREDENTIALS",
        "INVESTIGATE_SOURCE_IPS"
    ]
}

# Sample Quarantine Request - Standard Format
QUARANTINE_REQUEST_STANDARD = {
    "user_principal_name": "alex.salazar@company.com",
    "aws_iam_role_name": "DeveloperRole",
    "reason": "Impossible travel detected: User signed in from New York 2 hours ago, now signing in from Moscow",
    "risk_score": 9.5
}

# Sample Quarantine Request - AWS Only
QUARANTINE_REQUEST_AWS_ONLY = {
    "user_principal_name": "service-account@company.com",
    "aws_iam_role_name": "ServiceAccountRole",
    "reason": "IAM access key exfiltration detected from EC2 instance",
    "risk_score": 8.5
}

# Sample Quarantine Request - Azure Only
QUARANTINE_REQUEST_AZURE_ONLY = {
    "user_principal_name": "alex.salazar@company.com",
    "aws_iam_role_name": None,
    "reason": "Multiple failed authentication attempts from suspicious IP range",
    "risk_score": 7.8
}

# Sample Health Check Response
HEALTH_CHECK_RESPONSE = {
    "status": "healthy",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
}

# Sample Quarantine Response
QUARANTINE_RESPONSE_SUCCESS = {
    "status": "completed",
    "user_principal_name": "alex.salazar@company.com",
    "actions_taken": {
        "azure_entra": True,
        "aws_sts": True
    },
    "timestamp": "2024-01-15T10:30:05Z"
}

QUARANTINE_RESPONSE_PARTIAL = {
    "status": "completed",
    "user_principal_name": "alex.salazar@company.com",
    "actions_taken": {
        "azure_entra": True,
        "aws_sts": False
    },
    "timestamp": "2024-01-15T10:30:05Z",
    "errors": [
        "AWS IAM role quarantine failed: AccessDenied"
    ]
}

def get_test_payloads():
    """Return all test payloads as a dictionary"""
    return {
        "guardduty_iam_compromise": GUARDDUTY_IAM_COMPROMISE,
        "entra_id_impossible_travel": ENTRA_ID_IMPOSSIBLE_TRAVEL,
        "siem_brute_force_alert": SIEM_BRUTE_FORCE_ALERT,
        "quarantine_request_standard": QUARANTINE_REQUEST_STANDARD,
        "quarantine_request_aws_only": QUARANTINE_REQUEST_AWS_ONLY,
        "quarantine_request_azure_only": QUARANTINE_REQUEST_AZURE_ONLY,
        "health_check_response": HEALTH_CHECK_RESPONSE,
        "quarantine_response_success": QUARANTINE_RESPONSE_SUCCESS,
        "quarantine_response_partial": QUARANTINE_RESPONSE_PARTIAL
    }

if __name__ == "__main__":
    import json
    payloads = get_test_payloads()
    print("Available test payloads:")
    for name, payload in payloads.items():
        print(f"\n{name}:")
        print(json.dumps(payload, indent=2))
