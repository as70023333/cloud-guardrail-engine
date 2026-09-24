package cloud.guardrail.azure_test

import future.keywords.in
import data.cloud.guardrail.azure

# Test Case 1: Storage account with HTTPS disabled MUST trigger a deny violation
test_deny_insecure_storage_account {
    mock_plan := {
        "resource_changes": [{
            "name": "insecure_storage",
            "type": "azurerm_storage_account",
            "change": {
                "actions": ["create"],
                "after": {
                    "name": "stmulticloudprod01",
                    "enable_https_traffic_only": false
                }
            }
        }]
    }

    res := azure.deny with input as mock_plan
    count(res) == 1
}

# Test Case 2: Storage account with HTTPS enabled and TLS 1.2 MUST pass validation
test_allow_secure_storage_account {
    mock_plan := {
        "resource_changes": [{
            "name": "secure_storage",
            "type": "azurerm_storage_account",
            "change": {
                "actions": ["create"],
                "after": {
                    "name": "stsecureprod01",
                    "enable_https_traffic_only": true,
                    "min_tls_version": "TLS1_2"
                }
            }
        }]
    }

    res := azure.deny with input as mock_plan
    count(res) == 0
}
