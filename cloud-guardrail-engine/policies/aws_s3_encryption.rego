# METADATA
# title: AWS S3 Bucket Encryption Policy
# description: Ensures all S3 buckets have server-side encryption enabled
# scope: aws_s3_bucket
# severity: HIGH
# custom:
#   cci: CCI-001199
#   references:
#     - https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html

package aws.s3.encryption

import rego.v1

# Deny S3 buckets without server-side encryption
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "aws_s3_bucket"
    resource_change.change.actions[_] == "create"

    not has_encryption(resource_change)

    result := {
        "resource": resource_change.address,
        "msg": sprintf("S3 bucket '%s' does not have server-side encryption enabled. All S3 buckets must use SSE-S3, SSE-KMS, or SSE-C.", [resource_change.address]),
        "severity": "HIGH",
    }
}

# Deny S3 buckets with public access enabled
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "aws_s3_bucket"
    resource_change.change.actions[_] == "create"

    resource_change.change.after.public_access_block == null

    result := {
        "resource": resource_change.address,
        "msg": sprintf("S3 bucket '%s' does not have a public access block configured.", [resource_change.address]),
        "severity": "CRITICAL",
    }
}

# Deny S3 buckets without versioning enabled
violation contains result if {
    some resource_change in input.resource_changes
    resource_change.type == "aws_s3_bucket"
    resource_change.change.actions[_] == "create"

    resource_change.change.after.versioning[0].enabled != true

    result := {
        "resource": resource_change.address,
        "msg": sprintf("S3 bucket '%s' does not have versioning enabled.", [resource_change.address]),
        "severity": "MEDIUM",
    }
}

# Helper: Check if bucket has encryption configured
has_encryption(resource_change) if {
    resource_change.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default[_].sse_algorithm
}

has_encryption(resource_change) if {
    resource_change.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default[_].sse_algorithm == "AES256"
}

has_encryption(resource_change) if {
    resource_change.change.after.server_side_encryption_configuration[_].rule[_].apply_server_side_encryption_by_default[_].sse_algorithm == "aws:kms"
}
