import logging
import os
from azure.identity import DefaultAzureCredential
from msgraph import GraphServiceClient

logger = logging.getLogger("zero-trust-quarantine")

class AzureQuarantineProvider:
    def __init__(self):
        # Authenticates via Managed Identity, Azure CLI, or Service Principal environment variables
        self.credential = DefaultAzureCredential()
        self.graph_client = GraphServiceClient(credentials=self.credential)

    async def revoke_user_sessions(self, user_principal_name: str) -> bool:
        """
        Disables account sign-in and revokes all active refresh tokens in Entra ID.
        """
        try:
            # 1. Revoke active OAuth refresh tokens
            await self.graph_client.users.by_user_id(user_principal_name).revoke_sign_in_sessions.post()
            logger.info(f"✅ Successfully revoked Microsoft Entra ID sessions for: {user_principal_name}")

            # 2. Optionally disable account sign-in
            from msgraph.generated.models.user import User
            update_user = User(account_enabled=False)
            await self.graph_client.users.by_user_id(user_principal_name).patch(update_user)
            logger.info(f"🔒 Account sign-in disabled for: {user_principal_name}")

            return True

        except Exception as e:
            logger.error(f"❌ Azure Entra ID Quarantine failed for {user_principal_name}: {e}")
            return False
