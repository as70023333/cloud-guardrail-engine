package cloud.guardrail.aws

import future.keywords.if
import future.keywords.in
import future.keywords.contains

default allow = false

# Find all aws_s3_bucket resource changes in terraform plan
deny contains reason if {
    resource := input.resource_changes[_]
    resource.type == "aws_s3_bucket"
    
    # Check if create or update action
    actions := resource.change.actions
    "create" in actions
    
    # Validation logic: Ensure server-side encryption is defined
    not resource.change.after.server_side_encryption_configuration
    
    reason := sprintf("AWS S3 bucket '%v' must have server-side encryption enabled.", [resource.name])
}

allow if {
    count(deny) == 0
}
