"""API Routes for Space Entropy Generator"""

from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Optional
import base64
import logging
from pathlib import Path as FilePath

from app.entropy.pool import entropy_pool

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serve web interface"""
    html_file = FilePath(__file__).parent.parent / "templates" / "index.html"
    if html_file.exists():
        return html_file.read_text()
    else:
        # Fallback to JSON if HTML not found
        return JSONResponse({
            "name": "Space Entropy Generator",
            "version": "0.1.0",
            "description": "True Randomness as a Service using space imagery",
            "endpoints": {
                "/random/{n}": "Get n random bytes (Base64 encoded)",
                "/health": "Health check",
                "/stats": "Entropy pool statistics"
            }
        })


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns service health status
    """
    health = await entropy_pool.health_check()
    
    return {
        "status": "healthy" if health.get('healthy', False) else "degraded",
        "service": "space-entropy-generator",
        "version": "0.1.0",
        "redis": health
    }


@router.get("/stats")
async def get_stats():
    """
    Get entropy pool statistics
    
    Returns information about the entropy pool status
    """
    stats = await entropy_pool.get_stats()
    return stats


@router.get("/random/{n}")
async def get_random_bytes(
    n: int = Path(..., ge=1, le=10240, description="Number of random bytes to generate"),
):
    """
    Get n random bytes from the entropy pool
    
    Args:
        n: Number of bytes to return (1-10240)
        
    Returns:
        Base64 encoded random bytes
    """
    # Validate input
    if n < 1 or n > 10240:
        raise HTTPException(
            status_code=400,
            detail="Number of bytes must be between 1 and 10240"
        )
    
    # Get entropy from pool
    try:
        entropy = await entropy_pool.get_entropy(n)
        
        if entropy is None:
            raise HTTPException(
                status_code=503,
                detail="Entropy pool is empty. Please try again later."
            )
        
        # Encode as base64 for safe transport
        encoded = base64.b64encode(entropy).decode('utf-8')
        
        return {
            "bytes": encoded,
            "length": len(entropy),
            "format": "base64"
        }
    
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Entropy service unavailable: {str(e)}"
        )


@router.get("/random")
async def get_random_default():
    """
    Get default amount of random bytes (256 bytes)
    
    Returns:
        Base64 encoded random bytes
    """
    return await get_random_bytes(256)
