package cloud.guardrail.azure_test

import future.keywords.in
import data.cloud.guardrail.azure

# Test Case 1: Storage account without HTTPS enforced MUST trigger a violation
test_deny_http_azure_storage {
    mock_plan := {
        "resource_changes": [{
            "name": "insecure_storage",
            "type": "azurerm_storage_account",
            "change": {
                "actions": ["create"],
                "after": {
                    "name": "sttest01",
                    "enable_https_traffic_only": false
                }
            }
        }]
    }

    res := azure.deny with input as mock_plan
    count(res) == 1
}

# Test Case 2: Storage account enforcing HTTPS MUST pass
test_allow_https_azure_storage {
    mock_plan := {
        "resource_changes": [{
            "name": "secure_storage",
            "type": "azurerm_storage_account",
            "change": {
                "actions": ["create"],
                "after": {
                    "name": "sttest01",
                    "enable_https_traffic_only": true
                }
            }
        }]
    }

    res := azure.deny with input as mock_plan
    count(res) == 0
}
