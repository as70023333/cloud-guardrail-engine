package cloud.guardrail.azure

import future.keywords.in

default allow = false

# Find all azurerm_storage_account resource changes in terraform plan
deny[reason] {
    resource := input.resource_changes[_]
    resource.type == "azurerm_storage_account"
    
    # Check if create or update action
    actions := resource.change.actions
    "create" in actions
    
    # Validation logic: Ensure HTTPS-only traffic is enforced
    resource.change.after.enable_https_traffic_only != true
    
    reason := sprintf("Azure Storage Account '%v' must enforce HTTPS traffic only.", [resource.name])
}

deny[reason] {
    resource := input.resource_changes[_]
    resource.type == "azurerm_storage_account"
    
    actions := resource.change.actions
    "create" in actions
    
    # Validation logic: Ensure minimum TLS version is 1.2
    resource.change.after.min_tls_version != "TLS1_2"
    
    reason := sprintf("Azure Storage account '%v' must use minimum TLS version TLS1_2.", [resource.name])
}

allow {
    count(deny) == 0
}
