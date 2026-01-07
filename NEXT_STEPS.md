# 🚀 Next Steps - Phase 2 Implementation Guide

## Overview
Phase 1 is complete with a working image ingestion system. Now we'll implement the core entropy generation functionality.

## Phase 2: Preprocessing & Entropy Extraction

### 1. Image Preprocessing Module (`app/preprocessing/noise_extraction.py`)

**Goal**: Extract high-entropy noise from space images

**Implementation checklist**:
- [ ] Create `ImagePreprocessor` class
- [ ] Implement grayscale conversion
- [ ] Implement random region sampling (avoid deterministic patterns)
- [ ] Implement noise extraction methods:
  - [ ] Laplacian filter (edge detection)
  - [ ] FFT high-frequency components
  - [ ] Pixel difference analysis
- [ ] RGB channel separation and individual processing
- [ ] Normalize extracted data to byte sequences
- [ ] Add unit tests

**Key considerations**:
- Use non-deterministic sampling (seed from system time + image hash)
- Extract from multiple regions per image
- Combine multiple noise extraction methods
- Ensure output has high Shannon entropy

**Example API**:
```python
preprocessor = ImagePreprocessor()
noise_bytes = preprocessor.extract_noise(image_path)
# Returns: bytes with high entropy content
```

---

### 2. Cryptographic Hashing Module (`app/entropy/hashing.py`)

**Goal**: Apply cryptographic functions to raw entropy

**Implementation checklist**:
- [ ] Create `EntropyHasher` class
- [ ] Implement SHA-256 hashing
- [ ] Implement BLAKE3 hashing
- [ ] Implement entropy mixing from multiple sources
- [ ] Add timestamp chaining to prevent replay attacks
- [ ] Create hash verification functions
- [ ] Add unit tests

**Key features**:
- Multiple hash rounds for whitening
- Mix entropy from different images/sources
- Include timestamps in hash chain
- Support both deterministic and non-deterministic modes (for testing)

**Example API**:
```python
hasher = EntropyHasher()
random_bytes = hasher.hash_entropy(
    noise_data=extracted_noise,
    previous_hash=last_block_hash,
    timestamp=datetime.utcnow()
)
```

---

### 3. Entropy Validation Module (`app/entropy/validation.py`)

**Goal**: Ensure generated entropy meets quality standards

**Implementation checklist**:
- [ ] Create `EntropyValidator` class
- [ ] Implement Shannon entropy calculation
- [ ] Implement basic statistical tests:
  - [ ] Chi-square test
  - [ ] Runs test
  - [ ] Autocorrelation test
- [ ] Add quality scoring (0-10 scale)
- [ ] Create rejection logic for low-quality entropy
- [ ] Prepare hooks for NIST SP 800-22 integration
- [ ] Add comprehensive tests

**Shannon entropy formula**:
```
H = -Σ(P(xi) * log2(P(xi)))
where P(xi) is the probability of byte value xi
```

**Target**: > 7.8 bits per byte (out of 8.0 maximum)

**Example API**:
```python
validator = EntropyValidator()
quality = validator.validate(entropy_bytes)
# Returns: {'shannon_entropy': 7.95, 'chi_square': 0.98, 'passed': True}
```

---

### 4. Redis Entropy Pool Manager (`app/entropy/pool.py`)

**Goal**: Maintain a continuously refreshed pool of high-quality entropy

**Implementation checklist**:
- [ ] Create `EntropyPool` class
- [ ] Implement Redis connection management
- [ ] Create entropy block storage structure
- [ ] Implement concurrent-safe entropy extraction
- [ ] Add automatic TTL (Time To Live) management
- [ ] Implement pool refill logic
- [ ] Add pool statistics tracking
- [ ] Handle Redis connection failures gracefully
- [ ] Add comprehensive tests

**Redis data structure**:
```
Key: entropy:block:{uuid}
Value: {
    'data': base64_encoded_bytes,
    'hash': sha256_hash,
    'quality': shannon_entropy_score,
    'timestamp': utc_timestamp,
    'source_images': [image_hashes]
}
TTL: 3600 seconds (configurable)
```

**Key features**:
- Atomic operations for thread safety
- Never return the same entropy twice
- Automatic background refill
- Quality-based prioritization
- Monitoring and alerts

**Example API**:
```python
pool = EntropyPool()
await pool.add_entropy(entropy_bytes, quality_score)
random_data = await pool.get_entropy(n_bytes=256)
stats = await pool.get_stats()
```

---

### 5. Integrate Everything

**Update `app/main.py`**:
- [ ] Add background task for entropy generation
- [ ] Connect image ingestion → preprocessing → entropy extraction → pool
- [ ] Add error handling and retry logic
- [ ] Implement graceful degradation

**Update `app/api/routes.py`**:
- [ ] Implement `/random/{n}` endpoint with actual entropy
- [ ] Implement `/stats` with real pool statistics
- [ ] Add `/health` checks for all components
- [ ] Add proper error responses

**Create integration pipeline**:
```python
async def entropy_generation_pipeline():
    while True:
        # 1. Get images from ingestion manager
        images = ingestion_manager.get_stored_images()
        
        # 2. Process each image
        for image_path in images:
            # Extract noise
            noise = preprocessor.extract_noise(image_path)
            
            # Hash and mix
            entropy = hasher.hash_entropy(noise)
            
            # Validate quality
            quality = validator.validate(entropy)
            
            # Add to pool if quality is good
            if quality['passed']:
                await pool.add_entropy(entropy, quality)
        
        await asyncio.sleep(60)  # Run every minute
```

---

## Implementation Order

1. **Start with validation** (easiest to test independently)
   - Implement Shannon entropy calculation
   - Create test cases with known entropy values
   
2. **Implement preprocessing** (can test with real images)
   - Start with simple methods (grayscale, Laplacian)
   - Add more complex methods incrementally
   - Validate entropy quality after each method
   
3. **Add hashing** (straightforward)
   - Implement basic SHA-256 first
   - Add BLAKE3
   - Implement mixing strategies
   
4. **Build entropy pool** (requires Redis)
   - Start with in-memory dict for testing
   - Add Redis integration
   - Implement concurrent access patterns
   
5. **Integrate and test end-to-end**
   - Connect all modules
   - Test full pipeline
   - Measure performance

---

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies (Redis, file I/O)
- Use known test vectors for validation

### Integration Tests
- Test full pipeline with real images
- Verify entropy quality meets standards
- Test concurrent access patterns
- Measure throughput

### Performance Tests
- Measure entropy generation rate (bytes/second)
- Test pool refill under load
- Verify response times under concurrent requests

---

## Development Commands

```bash
# Run tests
pytest -v

# Run specific test file
pytest tests/test_preprocessing.py -v

# Run with coverage
pytest --cov=app tests/

# Run the application
python -m app.main

# Test image ingestion
python test_ingestion.py

# Monitor Redis
redis-cli MONITOR

# Check entropy pool
redis-cli KEYS "entropy:*"
```

---

## Success Criteria for Phase 2

- [ ] Shannon entropy consistently > 7.8 bits/byte
- [ ] Entropy generation rate > 1 KB/second
- [ ] Pool maintains at least 100 KB of validated entropy
- [ ] API responds in < 100ms for 1 KB requests
- [ ] All tests pass with > 90% code coverage
- [ ] No entropy block is ever served twice

---

## Estimated Time

- Preprocessing module: 2-3 hours
- Hashing module: 1-2 hours
- Validation module: 2-3 hours
- Pool manager: 3-4 hours
- Integration & testing: 2-3 hours

**Total: ~10-15 hours of development**

---

## Phase 3 Preview

After Phase 2 is complete:
- [ ] Security hardening (rate limiting, API keys)
- [ ] NIST SP 800-22 statistical test suite integration
- [ ] Performance optimization (GPU acceleration for preprocessing)
- [ ] WebSocket streaming API
- [ ] Comprehensive monitoring and alerting
- [ ] Production deployment guide

---

## Quick Start for Phase 2

```bash
# Create the first file
touch app/preprocessing/noise_extraction.py

# Start with the ImagePreprocessor class
# Implement grayscale conversion first
# Test with real NASA images we already downloaded
```

Ready to start Phase 2? Let's build the preprocessing module first! 🚀
