"""Configuration management for the Space Entropy Generator"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Space Entropy Generator"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_rate_limit: int = 100  # requests per minute
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_use_ssl: bool = False  # Set True for Azure Cache for Redis (port 6380)
    
    # Entropy Pool Settings
    entropy_pool_size: int = 1024 * 1024  # 1 MB default pool size
    entropy_block_size: int = 4096  # bytes
    entropy_ttl: int = 3600  # seconds (1 hour)
    min_shannon_entropy: float = 7.8  # bits per byte (out of 8.0)
    
    # Image Ingestion Settings
    nasa_sdo_base_url: str = "https://sdo.gsfc.nasa.gov/assets/img/latest"
    image_fetch_interval: int = 300  # seconds (5 minutes)
    image_storage_path: str = "/tmp/space_entropy_images"
    max_stored_images: int = 10
    
    # Supported NASA SDO image types
    sdo_image_types: list = [
        "latest_1024_0193.jpg",  # 193 Angstrom
        "latest_1024_0304.jpg",  # 304 Angstrom
        "latest_1024_0171.jpg",  # 171 Angstrom
        "latest_1024_0211.jpg",  # 211 Angstrom
    ]
    
    # Security
    require_api_key: bool = False
    api_key: Optional[str] = None

    # Azure (optional)
    use_azure_blob: bool = False
    azure_storage_connection_string: Optional[str] = None
    azure_storage_account: Optional[str] = None
    azure_storage_container: str = "space-entropy-images"
    azure_storage_sas_token: Optional[str] = None
    azure_use_managed_identity: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
