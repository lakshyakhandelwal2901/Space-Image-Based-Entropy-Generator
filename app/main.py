"""FastAPI Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from app.config import settings
from app.api.routes import router
from app.ingestion import ingestion_manager
from app.preprocessing import preprocessor
from app.entropy import hasher, validator
from app.entropy.pool import entropy_pool

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def generate_entropy_continuously():
    """
    Background task: continuously generate and store entropy
    
    This task:
    1. Gets stored images from ingestion manager
    2. Extracts noise from each image
    3. Hashes noise into entropy blocks
    4. Validates and adds high-quality blocks to pool
    """
    while True:
        try:
            # Check if pool needs refilling
            stats = await entropy_pool.get_stats()
            available_bytes = stats.get('available_bytes', 0)
            
            # Refill if below threshold (1 MB)
            if available_bytes < 1024 * 1024:
                logger.info(f"Entropy pool low ({available_bytes:,} bytes). Generating more...")
                
                # Get available images
                images = ingestion_manager.get_stored_images()
                
                if images:
                    # Process each image
                    for image_path in images:
                        # Extract noise
                        raw_noise = preprocessor.extract_noise(image_path)
                        
                        # Hash into entropy blocks
                        entropy_blocks = hasher.process_image_noise(raw_noise, block_size=4096)
                        
                        # Validate and add to pool
                        added = 0
                        for block in entropy_blocks:
                            result = validator.validate(block)
                            if result['passed']:
                                await entropy_pool.add_entropy(
                                    block,
                                    result['quality_score'],
                                    {'source': 'space_image', 'image': image_path}
                                )
                                added += 1
                        
                        logger.info(f"Added {added} blocks from {image_path}")
                        
                        # Don't process all images at once
                        if added > 0:
                            break
                else:
                    logger.warning("No images available for entropy generation")
            
            # Wait before next check
            await asyncio.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            logger.error(f"Error in entropy generation: {e}", exc_info=True)
            await asyncio.sleep(60)  # Wait longer on error


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Space Entropy Generator...")
    
    # Start periodic image fetching in background
    fetch_task = asyncio.create_task(
        ingestion_manager.start_periodic_fetch()
    )
    
    # Start continuous entropy generation in background
    entropy_task = asyncio.create_task(
        generate_entropy_continuously()
    )
    
    logger.info("✓ Image ingestion started")
    logger.info("✓ Entropy generation started")
    logger.info(f"✓ Server running on http://{settings.api_host}:{settings.api_port}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Space Entropy Generator...")
    fetch_task.cancel()
    entropy_task.cancel()
    try:
        await fetch_task
    except asyncio.CancelledError:
        pass
    try:
        await entropy_task
    except asyncio.CancelledError:
        pass
    logger.info("✓ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Generate cryptographically secure random numbers from space imagery",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["entropy"])

# Root endpoint (not versioned)
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs",
        "api_base": "/api/v1"
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"ping": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
