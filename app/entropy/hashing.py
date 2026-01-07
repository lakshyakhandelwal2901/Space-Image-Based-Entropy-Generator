"""Cryptographic Hashing Module - Converts raw noise into high-quality entropy"""

import hashlib
import blake3
from typing import List, Optional
from datetime import datetime
import struct
import logging

logger = logging.getLogger(__name__)


class EntropyHasher:
    """Applies cryptographic hashing to raw entropy data"""
    
    def __init__(self):
        """Initialize hasher"""
        self.previous_hash = None
    
    def sha256_hash(self, data: bytes) -> bytes:
        """
        Apply SHA-256 hash
        
        Args:
            data: Input bytes
            
        Returns:
            32-byte SHA-256 hash
        """
        return hashlib.sha256(data).digest()
    
    def blake3_hash(self, data: bytes) -> bytes:
        """
        Apply BLAKE3 hash
        
        BLAKE3 is faster and more secure than SHA-256
        
        Args:
            data: Input bytes
            
        Returns:
            32-byte BLAKE3 hash
        """
        return blake3.blake3(data).digest()
    
    def hash_with_timestamp(self, data: bytes, timestamp: Optional[datetime] = None) -> bytes:
        """
        Hash data with timestamp for anti-replay protection
        
        Args:
            data: Input bytes
            timestamp: Timestamp to include (uses current time if None)
            
        Returns:
            Hashed bytes including timestamp
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        # Convert timestamp to bytes (microseconds since epoch)
        timestamp_int = int(timestamp.timestamp() * 1000000)
        timestamp_bytes = struct.pack('>Q', timestamp_int)
        
        # Combine data with timestamp
        combined = data + timestamp_bytes
        
        # Hash with BLAKE3 (faster)
        return self.blake3_hash(combined)
    
    def hash_chain(self, data: bytes, previous_hash: Optional[bytes] = None) -> bytes:
        """
        Hash with chaining to previous block
        
        This creates a blockchain-like structure preventing replay
        
        Args:
            data: Input bytes
            previous_hash: Previous block's hash (or None for first block)
            
        Returns:
            Chained hash
        """
        if previous_hash is None:
            previous_hash = self.previous_hash or b'\x00' * 32
        
        # Combine current data with previous hash
        combined = previous_hash + data
        
        # Hash the combination
        new_hash = self.blake3_hash(combined)
        
        # Store for next chain
        self.previous_hash = new_hash
        
        return new_hash
    
    def extract_entropy_blocks(self, raw_data: bytes, block_size: int = 4096) -> List[bytes]:
        """
        Extract entropy blocks from raw data using cryptographic hashing
        
        Applies multiple hash rounds to whiten the data
        
        Args:
            raw_data: Raw noise bytes from image processing
            block_size: Desired size of each entropy block
            
        Returns:
            List of high-quality entropy blocks
        """
        if not raw_data:
            return []
        
        blocks = []
        
        # Split raw data into chunks
        chunk_size = max(block_size, 1024)  # Ensure minimum chunk size
        num_chunks = len(raw_data) // chunk_size
        
        if num_chunks == 0:
            # If data is smaller than chunk_size, hash it directly
            hashed = self.multi_round_hash(raw_data, rounds=3)
            # Extend to block_size by repeated hashing
            extended = self._extend_to_size(hashed, block_size)
            blocks.append(extended)
        else:
            for i in range(num_chunks):
                chunk = raw_data[i * chunk_size:(i + 1) * chunk_size]
                
                # Apply multiple hash rounds for whitening
                hashed = self.multi_round_hash(chunk, rounds=3)
                
                # Add timestamp and chain with previous block
                timestamped = self.hash_with_timestamp(hashed)
                chained = self.hash_chain(timestamped)
                
                # Extend to desired block size
                extended = self._extend_to_size(chained, block_size)
                
                blocks.append(extended)
        
        logger.info(f"✓ Extracted {len(blocks)} entropy blocks ({block_size} bytes each)")
        
        return blocks
    
    def multi_round_hash(self, data: bytes, rounds: int = 3) -> bytes:
        """
        Apply multiple rounds of hashing for better whitening
        
        Args:
            data: Input bytes
            rounds: Number of hash rounds
            
        Returns:
            Multi-hashed bytes
        """
        result = data
        
        for i in range(rounds):
            # Alternate between SHA-256 and BLAKE3
            if i % 2 == 0:
                result = self.blake3_hash(result)
            else:
                result = self.sha256_hash(result)
        
        return result
    
    def _extend_to_size(self, data: bytes, target_size: int) -> bytes:
        """
        Extend hash output to target size using key derivation
        
        Args:
            data: Input hash (32 bytes)
            target_size: Desired output size
            
        Returns:
            Extended bytes of target_size
        """
        if len(data) >= target_size:
            return data[:target_size]
        
        # Use BLAKE3 in extended output mode
        hasher = blake3.blake3(data)
        
        # BLAKE3 can produce arbitrary-length output
        return hasher.digest(length=target_size)
    
    def mix_sources(self, data_sources: List[bytes]) -> bytes:
        """
        Mix entropy from multiple sources
        
        Combines data from different images/sources for better security
        
        Args:
            data_sources: List of byte arrays from different sources
            
        Returns:
            Mixed entropy bytes
        """
        if not data_sources:
            return b''
        
        if len(data_sources) == 1:
            return self.blake3_hash(data_sources[0])
        
        # XOR all sources together
        max_len = max(len(d) for d in data_sources)
        
        # Pad all sources to same length
        padded = []
        for data in data_sources:
            if len(data) < max_len:
                # Extend using hashing
                extended = self._extend_to_size(data, max_len)
                padded.append(extended)
            else:
                padded.append(data[:max_len])
        
        # XOR combine all sources
        result = bytearray(padded[0])
        for data in padded[1:]:
            for i in range(len(result)):
                result[i] ^= data[i]
        
        # Final hash for whitening
        mixed = self.blake3_hash(bytes(result))
        
        logger.debug(f"Mixed {len(data_sources)} entropy sources")
        
        return mixed
    
    def process_image_noise(self, raw_noise: bytes, block_size: int = 4096) -> List[bytes]:
        """
        Complete processing pipeline for image noise
        
        Main entry point for converting raw image noise to entropy blocks
        
        Args:
            raw_noise: Raw noise extracted from image
            block_size: Size of each output block
            
        Returns:
            List of processed entropy blocks
        """
        logger.info(f"Processing {len(raw_noise):,} bytes of raw noise")
        
        # Extract entropy blocks with chaining and timestamps
        blocks = self.extract_entropy_blocks(raw_noise, block_size)
        
        return blocks


# Global hasher instance
hasher = EntropyHasher()


if __name__ == "__main__":
    # Test with raw noise from preprocessing
    import sys
    from pathlib import Path
    from app.ingestion import ingestion_manager
    from app.preprocessing import preprocessor
    from app.entropy.validation import validator
    
    print("Testing Entropy Hasher")
    print("=" * 60)
    
    # Get stored images
    images = ingestion_manager.get_stored_images()
    
    if not images:
        print("No images found. Run test_ingestion.py first.")
        sys.exit(1)
    
    print(f"Found {len(images)} images\n")
    
    # Extract noise from first image
    test_image = images[0]
    print(f"1. Extracting noise from: {Path(test_image).name}")
    raw_noise = preprocessor.extract_noise(test_image)
    print(f"   Raw noise: {len(raw_noise):,} bytes\n")
    
    # Process into entropy blocks
    print("2. Hashing into entropy blocks...")
    entropy_blocks = hasher.process_image_noise(raw_noise, block_size=4096)
    print(f"   Generated {len(entropy_blocks)} blocks\n")
    
    # Validate quality
    print("3. Validating entropy quality:")
    print("-" * 60)
    
    passed_count = 0
    for i, block in enumerate(entropy_blocks[:5]):  # Test first 5 blocks
        result = validator.validate(block)
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"Block {i+1}: {status} | Shannon: {result['shannon_entropy']:.3f} | Quality: {result['quality_score']:.3f}")
        if result['passed']:
            passed_count += 1
    
    print(f"\nPassed: {passed_count}/{min(5, len(entropy_blocks))} blocks")
    
    # Show sample bytes
    if entropy_blocks:
        print(f"\nSample from first block (32 bytes):")
        print(f"  {entropy_blocks[0][:32].hex()}")
