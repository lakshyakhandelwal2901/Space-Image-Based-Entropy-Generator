"""Image Ingestion Module - Fetches space images from NASA and other sources"""

import asyncio
import httpx
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import hashlib
import logging

from app.config import settings
from typing import Any
try:
    from app.storage import AzureBlobStorage
except Exception:
    AzureBlobStorage = None  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageSource:
    """Base class for image sources"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def fetch_image(self, url: str, save_path: str) -> Optional[str]:
        """Fetch an image from URL and save it"""
        raise NotImplementedError


class NASASDOSource(ImageSource):
    """NASA Solar Dynamics Observatory image source"""
    
    def __init__(self):
        super().__init__("NASA_SDO")
        self.base_url = settings.nasa_sdo_base_url
        self.image_types = settings.sdo_image_types
    
    async def fetch_image(self, url: str, save_path: str) -> Optional[str]:
        """
        Fetch a single image from NASA SDO
        
        Args:
            url: Full URL to the image
            save_path: Local path to save the image
            
        Returns:
            Path to saved image or None if failed
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Save image
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                # Calculate hash for verification
                image_hash = hashlib.sha256(response.content).hexdigest()[:16]
                
                logger.info(f"✓ Fetched image from {url} (hash: {image_hash})")
                return save_path
                
        except Exception as e:
            logger.error(f"✗ Failed to fetch image from {url}: {e}")
            return None
    
    async def fetch_latest_images(self, storage_path: str) -> List[str]:
        """
        Fetch all configured latest images from NASA SDO
        
        Args:
            storage_path: Directory to store images
            
        Returns:
            List of paths to successfully downloaded images
        """
        # Create storage directory if it doesn't exist
        Path(storage_path).mkdir(parents=True, exist_ok=True)
        
        downloaded_images = []
        tasks = []
        
        # Create timestamp for this batch
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        for image_type in self.image_types:
            url = f"{self.base_url}/{image_type}"
            
            # Create unique filename with timestamp
            filename = f"sdo_{timestamp}_{image_type}"
            save_path = os.path.join(storage_path, filename)
            
            # Create async task for each image
            tasks.append(self.fetch_image(url, save_path))
        
        # Fetch all images concurrently
        results = await asyncio.gather(*tasks)
        
        # Filter out failed downloads
        downloaded_images = [path for path in results if path is not None]
        
        logger.info(f"✓ Downloaded {len(downloaded_images)}/{len(self.image_types)} images")
        
        return downloaded_images


class ImageIngestionManager:
    """Manages image ingestion from multiple sources"""
    
    def __init__(self):
        self.storage_path = settings.image_storage_path
        self.max_stored_images = settings.max_stored_images
        self.sources: List[ImageSource] = []
        self.azure_blob = None
        
        # Initialize sources
        self._initialize_sources()
        
        # Ensure storage directory exists
        Path(self.storage_path).mkdir(parents=True, exist_ok=True)

        # Optional Azure Blob uploader
        if getattr(settings, 'use_azure_blob', False) and AzureBlobStorage is not None:
            try:
                self.azure_blob = AzureBlobStorage(container_name=settings.azure_storage_container)
                logger.info("✓ Azure Blob uploader initialized")
            except Exception as e:
                logger.error(f"Azure Blob initialization failed: {e}")
                self.azure_blob = None
    
    def _initialize_sources(self):
        """Initialize all configured image sources"""
        # Add NASA SDO as primary source
        self.sources.append(NASASDOSource())
        logger.info(f"✓ Initialized {len(self.sources)} image source(s)")
    
    async def fetch_images(self) -> List[Dict[str, any]]:
        """
        Fetch images from all sources
        
        Returns:
            List of dictionaries with image metadata
        """
        all_images = []
        
        for source in self.sources:
            if isinstance(source, NASASDOSource):
                images = await source.fetch_latest_images(self.storage_path)
                
                for image_path in images:
                    all_images.append({
                        'path': image_path,
                        'source': source.name,
                        'timestamp': datetime.utcnow(),
                        'size': os.path.getsize(image_path)
                    })

                    # Optionally upload to Azure Blob
                    if self.azure_blob:
                        blob_name = Path(image_path).name
                        url = self.azure_blob.upload_file(image_path, blob_name=blob_name)
                        if url:
                            all_images[-1]['blob_url'] = url  # type: ignore[index]
        
        # Clean up old images if we exceed max storage
        self._cleanup_old_images()
        
        return all_images
    
    def _cleanup_old_images(self):
        """Remove oldest images if we exceed max_stored_images"""
        try:
            # Get all image files in storage
            image_files = sorted(
                Path(self.storage_path).glob("*.jpg"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Remove excess images (keep newest ones)
            if len(image_files) > self.max_stored_images:
                for old_file in image_files[self.max_stored_images:]:
                    old_file.unlink()
                    logger.info(f"✓ Cleaned up old image: {old_file.name}")
                    
        except Exception as e:
            logger.error(f"✗ Error during cleanup: {e}")
    
    def get_stored_images(self) -> List[str]:
        """Get list of currently stored images"""
        return [str(f) for f in Path(self.storage_path).glob("*.jpg")]
    
    async def start_periodic_fetch(self, interval: int = None):
        """
        Start periodic image fetching
        
        Args:
            interval: Fetch interval in seconds (uses config default if None)
        """
        if interval is None:
            interval = settings.image_fetch_interval
        
        logger.info(f"✓ Starting periodic image fetch (interval: {interval}s)")
        
        while True:
            try:
                images = await self.fetch_images()
                logger.info(f"✓ Fetched {len(images)} image(s)")
            except Exception as e:
                logger.error(f"✗ Error in periodic fetch: {e}")
            
            await asyncio.sleep(interval)


# Global instance
ingestion_manager = ImageIngestionManager()


# Utility function for manual testing
async def test_fetch():
    """Test function to manually fetch images"""
    manager = ImageIngestionManager()
    images = await manager.fetch_images()
    
    print(f"\nFetched {len(images)} images:")
    for img in images:
        print(f"  - {img['path']} ({img['size']} bytes) from {img['source']}")
    
    return images


if __name__ == "__main__":
    # Run test fetch
    asyncio.run(test_fetch())
