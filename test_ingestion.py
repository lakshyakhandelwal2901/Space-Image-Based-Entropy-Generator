#!/usr/bin/env python3
"""
Development script to test image ingestion manually
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ingestion.fetch_images import ImageIngestionManager


async def main():
    print("=" * 60)
    print("Space Entropy Generator - Image Ingestion Test")
    print("=" * 60)
    print()
    
    manager = ImageIngestionManager()
    
    print(f"📁 Storage path: {manager.storage_path}")
    print(f"📊 Max stored images: {manager.max_stored_images}")
    print(f"🔧 Number of sources: {len(manager.sources)}")
    print()
    
    print("🚀 Fetching images from NASA SDO...")
    print()
    
    try:
        images = await manager.fetch_images()
        
        print()
        print(f"✅ Successfully fetched {len(images)} image(s)")
        print()
        
        if images:
            print("Image Details:")
            print("-" * 60)
            for i, img in enumerate(images, 1):
                print(f"{i}. {Path(img['path']).name}")
                print(f"   Source: {img['source']}")
                print(f"   Size: {img['size']:,} bytes")
                print(f"   Timestamp: {img['timestamp']}")
                print()
        
        # Show stored images
        stored = manager.get_stored_images()
        print(f"📦 Total stored images: {len(stored)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
