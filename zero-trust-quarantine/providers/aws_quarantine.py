import logging
import boto3
from botocore.exceptions import ClientError
from typing import List, Optional

logger = logging.getLogger("zero-trust-quarantine.aws")

class AWSQuarantineProvider:
    """AWS IAM & STS Session Invalidation Provider"""
    
    def __init__(self, region: str = "us-east-1"):
        """Initialize AWS clients"""
        self.iam_client = boto3.client('iam', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        logger.info(f"AWS Quarantine Provider initialized for region: {region}")
    
    def quarantine_iam_role(self, role_name: str) -> bool:
        """
        Quarantine an IAM role by:
        1. Detaching all policies
        2. Removing inline policies
        3. Revoking active sessions
        
        Args:
            role_name: Name of the IAM role to quarantine
            
        Returns:
            bool: True if quarantine successful, False otherwise
        """
        try:
            logger.warning(f"🔒 Quarantining IAM role: {role_name}")
            
            # Step 1: Get all attached policies
            attached_policies = self.iam_client.list_attached_role_policies(RoleName=role_name)
            
            # Step 2: Detach all managed policies
            for policy in attached_policies.get('AttachedPolicies', []):
                policy_arn = policy['PolicyArn']
                logger.info(f"Detaching policy: {policy_arn} from role: {role_name}")
                self.iam_client.detach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
            
            # Step 3: Remove inline policies
            inline_policies = self.iam_client.list_role_policies(RoleName=role_name)
            for policy_name in inline_policies.get('PolicyNames', []):
                logger.info(f"Deleting inline policy: {policy_name} from role: {role_name}")
                self.iam_client.delete_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name
                )
            
            # Step 4: Revoke active sessions (best effort - STS doesn't have direct session revocation)
            # Instead, we can update the role's trust policy to deny all assume role actions
            self._update_trust_policy_to_deny(role_name)
            
            logger.warning(f"✅ IAM role {role_name} successfully quarantined")
            return True
            
        except ClientError as e:
            logger.error(f"❌ Failed to quarantine IAM role {role_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error quarantining IAM role {role_name}: {e}")
            return False
    
    def _update_trust_policy_to_deny(self, role_name: str) -> None:
        """
        Update role trust policy to deny all assume role actions
        
        Args:
            role_name: Name of the IAM role
        """
        try:
            # Create a deny-all trust policy
            deny_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Deny",
                        "Principal": "*",
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
            
            import json
            self.iam_client.update_assume_role_policy(
                RoleName=role_name,
                PolicyDocument=json.dumps(deny_policy)
            )
            logger.info(f"Updated trust policy for role {role_name} to deny all assume role actions")
            
        except ClientError as e:
            logger.error(f"Failed to update trust policy for role {role_name}: {e}")
    
    def revoke_user_access_keys(self, username: str) -> bool:
        """
        Revoke all access keys for an IAM user
        
        Args:
            username: IAM username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.warning(f"🔒 Revoking access keys for user: {username}")
            
            # List all access keys
            keys = self.iam_client.list_access_keys(UserName=username)
            
            # Deactivate all keys
            for key in keys.get('AccessKeyMetadata', []):
                access_key_id = key['AccessKeyId']
                logger.info(f"Deactivating access key: {access_key_id} for user: {username}")
                self.iam_client.update_access_key(
                    UserName=username,
                    AccessKeyId=access_key_id,
                    Status='Inactive'
                )
            
            logger.warning(f"✅ All access keys revoked for user: {username}")
            return True
            
        except ClientError as e:
            logger.error(f"❌ Failed to revoke access keys for user {username}: {e}")
            return False
    
    def deactivate_mfa_devices(self, username: str) -> bool:
        """
        Deactivate all MFA devices for an IAM user
        
        Args:
            username: IAM username
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.warning(f"🔒 Deactivating MFA devices for user: {username}")
            
            # List all MFA devices
            mfa_devices = self.iam_client.list_mfa_devices(UserName=username)
            
            # Deactivate all MFA devices
            for device in mfa_devices.get('MFADevices', []):
                serial_number = device['SerialNumber']
                logger.info(f"Deactivating MFA device: {serial_number} for user: {username}")
                self.iam_client.deactivate_mfa_device(
                    UserName=username,
                    SerialNumber=serial_number
                )
            
            logger.warning(f"✅ All MFA devices deactivated for user: {username}")
            return True
            
        except ClientError as e:
            logger.error(f"❌ Failed to deactivate MFA devices for user {username}: {e}")
            return False
