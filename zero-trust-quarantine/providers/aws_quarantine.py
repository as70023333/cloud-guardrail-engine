import logging
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("zero-trust-quarantine")

class AWSQuarantineProvider:
    def __init__(self):
        self.iam_client = boto3.client("iam")

    def quarantine_iam_role(self, role_name: str) -> bool:
        """
        Revokes all active STS sessions issued before the current timestamp for a given IAM Role.
        """
        try:
            current_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            policy_name = f"Quarantine-RevokeOlderSessions-{int(datetime.now().timestamp())}"

            # Inline policy denying all actions if credentials were issued before now
            revoke_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "RevokeOlderSessions",
                        "Effect": "Deny",
                        "Action": "*",
                        "Resource": "*",
                        "Condition": {
                            "DateLessThan": {
                                "aws:TokenIssueTime": current_utc
                            }
                        }
                    }
                ]
            }

            import json
            self.iam_client.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(revoke_policy)
            )

            logger.info(f"✅ Successfully invalidated AWS STS sessions for role: {role_name} (Cutoff: {current_utc})")
            return True

        except ClientError as e:
            logger.error(f"❌ AWS IAM Quarantine failed for role {role_name}: {e}")
            return False
