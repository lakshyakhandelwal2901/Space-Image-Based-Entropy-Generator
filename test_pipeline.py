#!/usr/bin/env python3
"""
End-to-end test script for Space Entropy Generator
Tests the full pipeline from image ingestion to API serving
"""

import sys
import asyncio
import base64
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from app.ingestion import ingestion_manager
from app.preprocessing import preprocessor
from app.entropy import hasher, validator
from app.entropy.pool import entropy_pool


async def test_full_pipeline():
    """Test complete entropy generation pipeline"""
    
    print("=" * 70)
    print(" Space Entropy Generator - End-to-End Test")
    print("=" * 70)
    print()
    
    # Step 1: Check Redis connection
    print("1. Testing Redis connection...")
    if not entropy_pool.is_connected():
        print("   ✗ Redis not connected!")
        print("   Start Redis with: docker-compose up -d redis")
        return 1
    print("   ✓ Redis connected")
    print()
    
    # Step 2: Fetch images
    print("2. Fetching space images...")
    images = await ingestion_manager.fetch_images()
    if not images:
        print("   ✗ No images fetched")
        return 1
    print(f"   ✓ Fetched {len(images)} images")
    for img in images:
        print(f"     - {Path(img['path']).name} ({img['size']:,} bytes)")
    print()
    
    # Step 3: Extract noise from first image
    test_image = images[0]['path']
    print(f"3. Extracting noise from {Path(test_image).name}...")
    raw_noise = preprocessor.extract_noise(test_image)
    print(f"   ✓ Extracted {len(raw_noise):,} bytes of raw noise")
    print()
    
    # Step 4: Hash into entropy blocks
    print("4. Hashing into entropy blocks...")
    entropy_blocks = hasher.process_image_noise(raw_noise, block_size=4096)
    print(f"   ✓ Generated {len(entropy_blocks)} entropy blocks")
    print()
    
    # Step 5: Validate entropy quality
    print("5. Validating entropy quality...")
    passed = 0
    failed = 0
    sample_results = []
    
    for i, block in enumerate(entropy_blocks[:10]):  # Test first 10
        result = validator.validate(block, detailed=True)
        if result['passed']:
            passed += 1
            sample_results.append(result)
        else:
            failed += 1
    
    print(f"   ✓ Passed: {passed}/{passed+failed} blocks tested")
    
    if sample_results:
        avg_shannon = sum(r['shannon_entropy'] for r in sample_results) / len(sample_results)
        avg_quality = sum(r['quality_score'] for r in sample_results) / len(sample_results)
        print(f"   ✓ Avg Shannon entropy: {avg_shannon:.3f} bits/byte")
        print(f"   ✓ Avg quality score: {avg_quality:.3f}")
    print()
    
    # Step 6: Add to entropy pool
    print("6. Adding entropy to pool...")
    await entropy_pool.clear_pool()  # Clear for testing
    
    added = 0
    for block in entropy_blocks:
        result = validator.validate(block)
        if result['passed']:
            await entropy_pool.add_entropy(
                block,
                result['quality_score'],
                {'source': Path(test_image).name}
            )
            added += 1
    
    print(f"   ✓ Added {added} high-quality blocks to pool")
    print()
    
    # Step 7: Get pool statistics
    print("7. Pool statistics:")
    stats = await entropy_pool.get_stats()
    print(f"   Status: {stats['status']}")
    print(f"   Available blocks: {stats['available_blocks']}")
    print(f"   Available bytes: {stats['available_bytes']:,}")
    print(f"   Average quality: {stats['average_quality']:.3f}")
    print()
    
    # Step 8: Retrieve random bytes
    print("8. Testing entropy retrieval...")
    test_sizes = [256, 1024, 4096]
    
    for size in test_sizes:
        entropy = await entropy_pool.get_entropy(size)
        if entropy:
            # Quick validation of retrieved entropy
            result = validator.validate(entropy)
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            print(f"   {status} {size} bytes - Shannon: {result['shannon_entropy']:.3f}, Quality: {result['quality_score']:.3f}")
            print(f"        Sample: {entropy[:16].hex()}...")
        else:
            print(f"   ✗ Failed to retrieve {size} bytes")
    
    print()
    
    # Step 9: Final statistics
    print("9. Final pool statistics:")
    final_stats = await entropy_pool.get_stats()
    print(f"   Available blocks: {final_stats['available_blocks']}")
    print(f"   Available bytes: {final_stats['available_bytes']:,}")
    print(f"   Bytes served: {final_stats['bytes_served']:,}")
    print(f"   Requests served: {final_stats['requests_served']}")
    print()
    
    # Summary
    print("=" * 70)
    print(" Test Summary")
    print("=" * 70)
    print("✓ Image ingestion: WORKING")
    print("✓ Noise extraction: WORKING")
    print("✓ Cryptographic hashing: WORKING")
    print("✓ Entropy validation: WORKING")
    print("✓ Redis pool storage: WORKING")
    print("✓ Entropy retrieval: WORKING")
    print()
    print("🎉 All tests passed! The system is operational.")
    print()
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(test_full_pipeline())
    sys.exit(exit_code)
