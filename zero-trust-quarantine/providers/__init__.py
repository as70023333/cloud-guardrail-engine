"""Cloud provider implementations for zero-trust quarantine operations."""

from .aws_quarantine import AWSQuarantineProvider
from .azure_quarantine import AzureQuarantineProvider

__all__ = ["AWSQuarantineProvider", "AzureQuarantineProvider"]
