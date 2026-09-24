import logging
import asyncio
from typing import Optional
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.revoke_sign_in_sessions.revoke_sign_in_sessions_post_request_body import RevokeSignInSessionsPostRequestBody
from kiota_authentication_azure.azure_identity_authentication_provider import AzureIdentityAuthenticationProvider
from kiota_serialization_json.json_parse_node_factory import JsonParseNodeFactory
from kiota_serialization_text.text_parse_node_factory import TextParseNodeFactory
from kiota_serialization_json.json_serialization_writer_factory import JsonSerializationWriterFactory
from kiota_serialization_text.text_serialization_writer_factory import TextSerializationWriterFactory
from kiota_serialization_form_url_encoded.form_url_encoded_serialization_writer_factory import FormUrlEncodedSerializationWriterFactory

logger = logging.getLogger("zero-trust-quarantine.azure")

class AzureQuarantineProvider:
    """Azure Entra ID Session Revocation Provider"""
    
    def __init__(self, tenant_id: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize Azure Entra ID client
        
        Args:
            tenant_id: Azure AD tenant ID
            client_id: Application (client) ID
            client_secret: Client secret for the application
        """
        import os
        self.tenant_id = tenant_id or os.getenv("AZURE_TENANT_ID")
        self.client_id = client_id or os.getenv("AZURE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("AZURE_CLIENT_SECRET")
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            logger.warning("Azure credentials not fully configured. Session revocation will be simulated.")
            self.graph_client = None
        else:
            self.graph_client = self._initialize_graph_client()
        
        logger.info(f"Azure Quarantine Provider initialized for tenant: {self.tenant_id}")
    
    def _initialize_graph_client(self) -> GraphServiceClient:
        """Initialize Microsoft Graph client with proper authentication"""
        try:
            # Create credential
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            
            # Create authentication provider
            auth_provider = AzureIdentityAuthenticationProvider(
                credential,
                scopes=["https://graph.microsoft.com/.default"]
            )
            
            # Create request adapter
            from kiota_http.httpx_request_adapter import HttpxRequestAdapter
            request_adapter = HttpxRequestAdapter(
                auth_provider,
                JsonParseNodeFactory(),
                JsonSerializationWriterFactory()
            )
            
            # Create Graph client
            graph_client = GraphServiceClient(request_adapter)
            
            logger.info("Microsoft Graph client initialized successfully")
            return graph_client
            
        except Exception as e:
            logger.error(f"Failed to initialize Microsoft Graph client: {e}")
            return None
    
    async def revoke_user_sessions(self, user_principal_name: str) -> bool:
        """
        Revoke all active sessions for a user in Azure Entra ID
        
        Args:
            user_principal_name: User's principal name (e.g., user@company.com)
            
        Returns:
            bool: True if revocation successful, False otherwise
        """
        if not self.graph_client:
            logger.warning(f"⚠️  Graph client not configured. Simulating session revocation for: {user_principal_name}")
            return self._simulate_revocation(user_principal_name)
        
        try:
            logger.warning(f"🔒 Revoking all sessions for user: {user_principal_name}")
            
            # Create request body
            request_body = RevokeSignInSessionsPostRequestBody()
            
            # Call Graph API to revoke sign-in sessions
            await self.graph_client.users.by_user_id(user_principal_name).revoke_sign_in_sessions.post(request_body)
            
            logger.warning(f"✅ All sessions revoked for user: {user_principal_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to revoke sessions for user {user_principal_name}: {e}")
            return False
    
    def _simulate_revocation(self, user_principal_name: str) -> bool:
        """
        Simulate session revocation when Graph client is not configured
        
        Args:
            user_principal_name: User's principal name
            
        Returns:
            bool: Always returns True in simulation mode
        """
        logger.info(f"[SIMULATION] Would revoke all sessions for: {user_principal_name}")
        logger.info(f"[SIMULATION] Actions that would be taken:")
        logger.info(f"  - Invalidate all refresh tokens")
        logger.info(f"  - Revoke all active sessions")
        logger.info(f"  - Force re-authentication on next access")
        return True
    
    async def get_user_details(self, user_principal_name: str) -> Optional[dict]:
        """
        Get user details from Azure Entra ID
        
        Args:
            user_principal_name: User's principal name
            
        Returns:
            dict: User details or None if not found
        """
        if not self.graph_client:
            logger.warning("Graph client not configured. Cannot retrieve user details.")
            return None
        
        try:
            user = await self.graph_client.users.by_user_id(user_principal_name).get()
            
            return {
                "id": user.id,
                "display_name": user.display_name,
                "user_principal_name": user.user_principal_name,
                "account_enabled": user.account_enabled
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve user details for {user_principal_name}: {e}")
            return None
    
    async def disable_user_account(self, user_principal_name: str) -> bool:
        """
        Disable a user account in Azure Entra ID
        
        Args:
            user_principal_name: User's principal name
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.graph_client:
            logger.warning(f"⚠️  Graph client not configured. Simulating account disable for: {user_principal_name}")
            return True
        
        try:
            logger.warning(f"🔒 Disabling user account: {user_principal_name}")
            
            from msgraph.generated.models.user import User
            user = User()
            user.account_enabled = False
            
            await self.graph_client.users.by_user_id(user_principal_name).patch(user)
            
            logger.warning(f"✅ User account disabled: {user_principal_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to disable user account {user_principal_name}: {e}")
            return False
