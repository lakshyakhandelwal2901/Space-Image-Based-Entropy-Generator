"""Azure Blob Storage helper (optional).

This module is only used if settings.use_azure_blob is True. All imports are
wrapped so the app still works without Azure SDK installed.
"""
from __future__ import annotations

import logging
from typing import Optional
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

try:
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except Exception:  # pragma: no cover - keep optional
    AZURE_AVAILABLE = False
    BlobServiceClient = None  # type: ignore
    DefaultAzureCredential = None  # type: ignore


class AzureBlobStorage:
    def __init__(self,
                 container_name: Optional[str] = None):
        if not AZURE_AVAILABLE:
            raise RuntimeError("Azure SDK not available. Install azure-storage-blob & azure-identity.")

        self.container_name = container_name or settings.azure_storage_container
        self.client = self._build_client()
        self._ensure_container()

    def _build_client(self) -> BlobServiceClient:
        # Prefer connection string if provided
        if settings.azure_storage_connection_string:
            return BlobServiceClient.from_connection_string(settings.azure_storage_connection_string)

        # Otherwise use account + SAS token
        if settings.azure_storage_account and settings.azure_storage_sas_token:
            account_url = f"https://{settings.azure_storage_account}.blob.core.windows.net{settings.azure_storage_sas_token}"
            return BlobServiceClient(account_url=account_url)

        # Or DefaultAzureCredential (Managed Identity / dev login)
        if settings.azure_storage_account and settings.azure_use_managed_identity:
            credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
            account_url = f"https://{settings.azure_storage_account}.blob.core.windows.net"
            return BlobServiceClient(account_url=account_url, credential=credential)

        raise RuntimeError("Azure Blob credentials not configured.")

    def _ensure_container(self) -> None:
        try:
            container_client = self.client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
                logger.info(f"✓ Created Azure Blob container '{self.container_name}'")
        except Exception as e:
            logger.error(f"Azure container check/create failed: {e}")
            raise

    def upload_file(self, local_path: str, blob_name: Optional[str] = None) -> Optional[str]:
        try:
            blob_client = self.client.get_blob_client(
                container=self.container_name,
                blob=blob_name or Path(local_path).name,
            )
            with open(local_path, 'rb') as f:
                blob_client.upload_blob(f, overwrite=True)
            url = blob_client.url
            logger.info(f"✓ Uploaded to Azure Blob: {url}")
            return url
        except Exception as e:
            logger.error(f"Azure upload failed for {local_path}: {e}")
            return None
