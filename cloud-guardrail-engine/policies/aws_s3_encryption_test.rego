package cloud.guardrail.aws_test

import future.keywords.if
import future.keywords.in
import data.cloud.guardrail.aws

# Test Case 1: Unencrypted bucket MUST trigger a deny violation
test_deny_unencrypted_s3_bucket if {
    mock_plan := {
        "resource_changes": [{
            "name": "unencrypted_bucket",
            "type": "aws_s3_bucket",
            "change": {
                "actions": ["create"],
                "after": {"bucket": "test-bucket"}
            }
        }]
    }

    res := aws.deny with input as mock_plan
    count(res) == 1
}

# Test Case 2: Encrypted bucket MUST pass validation (no deny violations)
test_allow_encrypted_s3_bucket if {
    mock_plan := {
        "resource_changes": [{
            "name": "encrypted_bucket",
            "type": "aws_s3_bucket",
            "change": {
                "actions": ["create"],
                "after": {
                    "bucket": "test-bucket",
                    "server_side_encryption_configuration": [{}]
                }
            }
        }]
    }

    res := aws.deny with input as mock_plan
    count(res) == 0
}
