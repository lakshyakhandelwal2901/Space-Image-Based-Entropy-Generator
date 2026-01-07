"""Storage helpers (optional Azure Blob)."""

from typing import Optional

try:
    from .azure_blob import AzureBlobStorage  # type: ignore
except Exception:
    AzureBlobStorage = None  # type: ignore

__all__ = [
    'AzureBlobStorage',
]
