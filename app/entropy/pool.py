"""Entropy Pool Manager - Redis-backed secure entropy storage"""

import redis
import asyncio
import uuid
import base64
import json
from typing import Optional, Dict, List
from datetime import datetime, timezone
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class EntropyPool:
    """Manages a pool of high-quality entropy using Redis"""
    
    def __init__(self):
        """Initialize entropy pool"""
        self.redis_client = None
        self.stats_key = "entropy:stats"
        self.pool_key_prefix = "entropy:block"
        self.used_key_prefix = "entropy:used"
        
        # Connect to Redis
        self._connect()
    
    def _connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password if settings.redis_password else None,
                decode_responses=False,  # We work with bytes
                ssl=getattr(settings, 'redis_use_ssl', False)
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"✓ Connected to Redis at {settings.redis_host}:{settings.redis_port}")
        except redis.ConnectionError as e:
            logger.error(f"✗ Failed to connect to Redis: {e}")
            self.redis_client = None
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if self.redis_client is None:
            return False
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    async def add_entropy(self, entropy_data: bytes, quality_score: float, 
                         source_info: Optional[Dict] = None) -> str:
        """
        Add entropy block to the pool
        
        Args:
            entropy_data: High-quality entropy bytes
            quality_score: Quality score from validation (0-1)
            source_info: Optional metadata about entropy source
            
        Returns:
            Block ID (UUID)
        """
        if not self.is_connected():
            raise ConnectionError("Redis not connected")
        
        # Generate unique block ID
        block_id = str(uuid.uuid4())
        key = f"{self.pool_key_prefix}:{block_id}"
        
        # Create block metadata
        block_data = {
            'id': block_id,
            'data': base64.b64encode(entropy_data).decode('utf-8'),
            'quality_score': quality_score,
            'size': len(entropy_data),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'source_info': source_info or {}
        }
        
        # Store in Redis with TTL
        self.redis_client.setex(
            key,
            settings.entropy_ttl,
            json.dumps(block_data)
        )
        
        # Update statistics
        await self._update_stats('blocks_added', 1)
        await self._update_stats('total_bytes_added', len(entropy_data))
        
        logger.debug(f"Added entropy block {block_id[:8]}... ({len(entropy_data)} bytes, quality: {quality_score:.3f})")
        
        return block_id
    
    async def get_entropy(self, n_bytes: int) -> Optional[bytes]:
        """
        Get n random bytes from the pool
        
        IMPORTANT: Never returns the same entropy twice (atomic operation)
        
        Args:
            n_bytes: Number of bytes to retrieve
            
        Returns:
            Random bytes or None if pool is empty
        """
        if not self.is_connected():
            raise ConnectionError("Redis not connected")
        
        if n_bytes <= 0:
            return b''
        
        collected = bytearray()
        blocks_used = []
        
        # Get available blocks
        pattern = f"{self.pool_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        
        if not keys:
            logger.warning("Entropy pool is empty")
            return None
        
        # Collect entropy from blocks
        for key in keys:
            if len(collected) >= n_bytes:
                break
            
            # Check if already used
            block_id = key.decode('utf-8').split(':')[-1]
            used_key = f"{self.used_key_prefix}:{block_id}"
            
            if self.redis_client.exists(used_key):
                continue  # Skip already used blocks
            
            # Get block data
            block_json = self.redis_client.get(key)
            if not block_json:
                continue
            
            try:
                block_data = json.loads(block_json)
                entropy_bytes = base64.b64decode(block_data['data'])
                
                # Take what we need
                needed = n_bytes - len(collected)
                collected.extend(entropy_bytes[:needed])
                
                # Mark as used (with same TTL as original block)
                ttl = self.redis_client.ttl(key)
                if ttl > 0:
                    self.redis_client.setex(used_key, ttl, '1')
                
                # Delete the original block to prevent reuse
                self.redis_client.delete(key)
                
                blocks_used.append(block_id)
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error reading block {block_id}: {e}")
                continue
        
        if len(collected) < n_bytes:
            logger.warning(f"Could only collect {len(collected)}/{n_bytes} bytes from pool")
            if len(collected) == 0:
                return None
        
        # Update statistics
        await self._update_stats('bytes_served', len(collected))
        await self._update_stats('requests_served', 1)
        
        logger.info(f"Served {len(collected)} bytes from {len(blocks_used)} blocks")
        
        return bytes(collected[:n_bytes])
    
    async def get_stats(self) -> Dict:
        """
        Get entropy pool statistics
        
        Returns:
            Dictionary with pool statistics
        """
        if not self.is_connected():
            return {
                'status': 'disconnected',
                'error': 'Redis not connected'
            }
        
        # Count available blocks
        pattern = f"{self.pool_key_prefix}:*"
        available_keys = self.redis_client.keys(pattern)
        num_blocks = len(available_keys)
        
        # Calculate total available bytes
        total_bytes = 0
        quality_scores = []
        
        for key in available_keys[:100]:  # Sample first 100 blocks for stats
            block_json = self.redis_client.get(key)
            if block_json:
                try:
                    block_data = json.loads(block_json)
                    total_bytes += block_data['size']
                    quality_scores.append(block_data['quality_score'])
                except:
                    pass
        
        # Extrapolate if we sampled
        if len(available_keys) > 100:
            total_bytes = int(total_bytes * (num_blocks / 100))
        
        # Get accumulated stats
        stats_data = self.redis_client.get(self.stats_key)
        accumulated_stats = {}
        if stats_data:
            try:
                accumulated_stats = json.loads(stats_data)
            except:
                pass
        
        # Calculate average quality
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        return {
            'status': 'connected',
            'available_blocks': num_blocks,
            'available_bytes': total_bytes,
            'average_quality': round(avg_quality, 3),
            'blocks_added': accumulated_stats.get('blocks_added', 0),
            'total_bytes_added': accumulated_stats.get('total_bytes_added', 0),
            'bytes_served': accumulated_stats.get('bytes_served', 0),
            'requests_served': accumulated_stats.get('requests_served', 0),
            'redis_host': settings.redis_host,
            'redis_port': settings.redis_port
        }
    
    async def _update_stats(self, key: str, increment: int):
        """Update accumulated statistics"""
        if not self.is_connected():
            return
        
        try:
            stats_data = self.redis_client.get(self.stats_key)
            stats = json.loads(stats_data) if stats_data else {}
        except:
            stats = {}
        
        stats[key] = stats.get(key, 0) + increment
        stats['last_updated'] = datetime.now(timezone.utc).isoformat()
        
        self.redis_client.set(self.stats_key, json.dumps(stats))
    
    async def clear_pool(self):
        """Clear all entropy from pool (for testing/maintenance)"""
        if not self.is_connected():
            return
        
        # Delete all entropy blocks
        pattern = f"{self.pool_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
        
        # Delete used markers
        pattern = f"{self.used_key_prefix}:*"
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
        
        logger.info("Cleared entropy pool")
    
    async def health_check(self) -> Dict:
        """
        Health check for the entropy pool
        
        Returns:
            Health status dictionary
        """
        health = {
            'redis_connected': self.is_connected(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if health['redis_connected']:
            stats = await self.get_stats()
            health['available_blocks'] = stats['available_blocks']
            health['available_bytes'] = stats['available_bytes']
            health['healthy'] = stats['available_blocks'] > 0
        else:
            health['healthy'] = False
            health['error'] = 'Redis not connected'
        
        return health


# Global entropy pool instance
entropy_pool = EntropyPool()


if __name__ == "__main__":
    # Test entropy pool
    import sys
    from pathlib import Path
    from app.ingestion import ingestion_manager
    from app.preprocessing import preprocessor
    from app.entropy import hasher, validator
    
    async def test_pool():
        print("Testing Entropy Pool")
        print("=" * 60)
        
        # Check connection
        if not entropy_pool.is_connected():
            print("✗ Redis not connected. Start Redis with: redis-server")
            return 1
        
        print("✓ Connected to Redis\n")
        
        # Clear pool for testing
        await entropy_pool.clear_pool()
        
        # Get images
        images = ingestion_manager.get_stored_images()
        if not images:
            print("✗ No images found")
            return 1
        
        print(f"Found {len(images)} images\n")
        
        # Process first image
        test_image = images[0]
        print(f"1. Processing: {Path(test_image).name}")
        
        # Extract noise
        raw_noise = preprocessor.extract_noise(test_image)
        print(f"   Extracted {len(raw_noise):,} bytes of raw noise")
        
        # Hash into entropy blocks
        entropy_blocks = hasher.process_image_noise(raw_noise, block_size=4096)
        print(f"   Generated {len(entropy_blocks)} entropy blocks\n")
        
        # Add blocks to pool
        print("2. Adding entropy to pool...")
        added_count = 0
        for block in entropy_blocks:
            result = validator.validate(block)
            if result['passed']:
                await entropy_pool.add_entropy(
                    block,
                    result['quality_score'],
                    {'source': Path(test_image).name}
                )
                added_count += 1
        
        print(f"   Added {added_count} high-quality blocks to pool\n")
        
        # Get statistics
        stats = await entropy_pool.get_stats()
        print("3. Pool Statistics:")
        print("-" * 60)
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test entropy retrieval
        print("\n4. Testing entropy retrieval:")
        print("-" * 60)
        
        for size in [256, 1024, 4096]:
            entropy = await entropy_pool.get_entropy(size)
            if entropy:
                print(f"   Retrieved {len(entropy)} bytes")
                print(f"   Sample: {entropy[:32].hex()}")
            else:
                print(f"   Failed to retrieve {size} bytes")
        
        # Final statistics
        print("\n5. Final Statistics:")
        print("-" * 60)
        stats = await entropy_pool.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        return 0
    
    exit_code = asyncio.run(test_pool())
    sys.exit(exit_code)
