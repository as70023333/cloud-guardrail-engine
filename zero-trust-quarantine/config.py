import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for Zero-Trust Quarantine Engine"""
    
    # API Configuration
    API_SECRET_TOKEN: str = os.getenv("QUARANTINE_API_SECRET", "super-secret-token")
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # Azure Configuration
    AZURE_TENANT_ID: Optional[str] = os.getenv("AZURE_TENANT_ID")
    AZURE_CLIENT_ID: Optional[str] = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET: Optional[str] = os.getenv("AZURE_CLIENT_SECRET")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        if not cls.API_SECRET_TOKEN or cls.API_SECRET_TOKEN == "super-secret-token":
            raise ValueError("QUARANTINE_API_SECRET must be set to a secure value")
        
        # AWS credentials are optional (can use IAM roles)
        # Azure credentials are optional (can use managed identity)
        
    @classmethod
    def is_aws_configured(cls) -> bool:
        """Check if AWS credentials are configured"""
        return bool(cls.AWS_ACCESS_KEY_ID and cls.AWS_SECRET_ACCESS_KEY)
    
    @classmethod
    def is_azure_configured(cls) -> bool:
        """Check if Azure credentials are configured"""
        return bool(cls.AZURE_TENANT_ID and cls.AZURE_CLIENT_ID and cls.AZURE_CLIENT_SECRET)

# Global config instance
config = Config()
