# METADATA
# title: Azure Storage Account HTTPS Enforcement Policy
# description: Ensures all Azure Storage accounts enforce HTTPS-only access
# scope: azurerm_storage_account
# severity: HIGH
# custom:
#   cci: CCI-000068
#   references:
#     - https://docs.microsoft.com/en-us/azure/storage/common/storage-require-secure-transfer
#     - https://learn.microsoft.com/en-us/azure/security/fundamentals/network-best-practices

package azure.storage.https

import rego.v1

# Deny storage accounts that don't enforce HTTPS
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "azurerm_storage_account"
    resource_change.change.actions[_] == "create"

    resource_change.change.after.enable_https_traffic_only != true

    result := {
        "resource": resource_change.address,
        "msg": sprintf("Storage account '%s' does not enforce HTTPS-only traffic. Set 'enable_https_traffic_only' to true.", [resource_change.address]),
        "severity": "HIGH",
    }
}

# Deny storage accounts with minimum TLS version below 1.2
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "azurerm_storage_account"
    resource_change.change.actions[_] == "create"

    tls_version := resource_change.change.after.min_tls_version
    tls_version != "TLS1_2"

    result := {
        "resource": resource_change.address,
        "msg": sprintf("Storage account '%s' has minimum TLS version '%s'. Must be 'TLS1_2' or higher.", [resource_change.address, tls_version]),
        "severity": "HIGH",
    }
}

# Deny storage accounts that allow blob public access
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "azurerm_storage_account"
    resource_change.change.actions[_] == "create"

    resource_change.change.after.allow_blob_public_access == true

    result := {
        "resource": resource_change.address,
        "msg": sprintf("Storage account '%s' allows public blob access. Set 'allow_blob_public_access' to false.", [resource_change.address]),
        "severity": "CRITICAL",
    }
}

# Deny storage accounts without network rules restricting access
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "azurerm_storage_account"
    resource_change.change.actions[_] == "create"

    not has_network_rules(resource_change)

    result := {
        "resource": resource_change.address,
        "msg": sprintf("Storage account '%s' does not have network rules configured. Restrict access using virtual network rules or IP rules.", [resource_change.address]),
        "severity": "MEDIUM",
    }
}

# Helper: Check if network rules are configured
has_network_rules(resource_change) if {
    resource_change.change.after.network_rules[_].default_action == "Deny"
}
