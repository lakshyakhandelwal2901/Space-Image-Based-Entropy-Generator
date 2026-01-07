# Space-Image Based Entropy Generator 🌌

**True Randomness as a Service** powered by cosmic unpredictability

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

This project generates cryptographically secure random numbers by extracting entropy from live space imagery (solar images, starfields, satellite images). Unlike traditional pseudo-random number generators (PRNGs) which are deterministic, this system harnesses natural cosmic unpredictability to produce true random numbers suitable for:

- 🔐 Cryptographic key generation
- ⛓️ Blockchain randomness
- 🤖 AI/ML stochastic processes
- 🎲 Simulations and gaming
- 🔒 Security applications

## 🌟 Key Features

- **True Randomness**: Extracts entropy from natural cosmic phenomena
- **High Quality**: Shannon entropy ~8 bits per byte
- **Scalable**: Redis-backed entropy pool with concurrent access
- **Secure**: Cryptographic hashing (SHA-256 + BLAKE3)
- **Real-time**: Continuous image ingestion from NASA sources
- **Production Ready**: Docker-ready with comprehensive API

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Space Image Sources                       │
│  (NASA SDO, Satellites, Starfield Cameras, Cosmic Rays)     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Image Ingestion Module                          │
│  • Periodic fetching from multiple sources                   │
│  • Timestamping & storage management                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Preprocessing & Noise Extraction                   │
│  • Grayscale conversion                                      │
│  • Random region sampling                                    │
│  • High-frequency noise (Laplacian/FFT)                      │
│  • RGB channel separation                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Entropy Extraction                              │
│  • Cryptographic hashing (SHA-256, BLAKE3)                   │
│  • Multi-source mixing                                       │
│  • Quality validation (Shannon entropy)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Redis Entropy Pool                              │
│  • Continuously refreshed                                    │
│  • Thread-safe concurrent access                             │
│  • Automatic expiration                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Service                                 │
│  GET /api/v1/random/{n}  - Get random bytes                  │
│  GET /api/v1/health      - Health check                      │
│  GET /api/v1/stats       - Pool statistics                   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
space-entropy-generator/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Configuration management
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── fetch_images.py      # Image fetching from NASA/sources
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── noise_extraction.py  # [TODO] Image preprocessing
│   ├── entropy/
│   │   ├── __init__.py
│   │   ├── hashing.py           # [TODO] Cryptographic hashing
│   │   ├── validation.py        # [TODO] Entropy quality checks
│   │   └── pool.py              # [TODO] Redis entropy pool
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py            # API endpoints
│   └── security/
│       ├── __init__.py
│       └── rate_limit.py        # [TODO] Rate limiting
├── tests/                       # Test suite
├── docker/
│   └── Dockerfile
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── # Space-Image Based Entropy Generator 🌌

**True Randomness as a Service** - Generate cryptographically secure random numbers from NASA space imagery.

## Overview

This service generates high-quality cryptographic entropy by extracting noise patterns from live NASA Solar Dynamics Observatory (SDO) images. The entropy is validated using comprehensive statistical tests, stored in a Redis pool, and served via a REST API.

### Key Features

- **Live Space Imagery**: Fetches real-time solar images from NASA SDO in multiple wavelengths (193Å, 304Å, 171Å, 211Å)
- **Multi-Stage Processing**: Combines multiple noise extraction techniques (Laplacian, FFT, gradients, random sampling)
- **Cryptographic Hardening**: Multi-round hashing with BLAKE3 and SHA-256, timestamp chaining, blockchain-like linking
- **Quality Validation**: 5 statistical tests ensure entropy meets cryptographic standards (Shannon entropy ≥7.8 bits/byte)
- **High-Performance Pool**: Redis-backed entropy pool with atomic operations, TTL management, and continuous generation
- **REST API**: Simple HTTP endpoints for retrieving random bytes in base64 format
- **Azure Ready**: Optional Azure Blob Storage and Azure Cache for Redis integration
- **Docker Support**: Complete docker-compose setup for local development

## Architecture

```
NASA SDO API → Image Ingestion → Noise Extraction → Cryptographic Hashing → Validation → Redis Pool → REST API
```

### Pipeline Components

1. **Image Ingestion** ([app/ingestion/](app/ingestion/))
   - Fetches 4 wavelengths concurrently from NASA SDO
   - Automatic cleanup of old images (keeps 10 most recent)
   - Optional Azure Blob Storage backup

2. **Noise Extraction** ([app/preprocessing/](app/preprocessing/))
   - Laplacian edge detection with image mixing
   - High-frequency FFT filtering
   - Sobel gradient calculation
   - Non-deterministic random region sampling
   - RGB channel separation

3. **Cryptographic Hashing** ([app/entropy/hashing.py](app/entropy/hashing.py))
   - 3-round alternating BLAKE3/SHA-256 hashing
   - Microsecond timestamp integration
   - Blockchain-like chaining between blocks
   - BLAKE3 XOF extension to target block size

4. **Quality Validation** ([app/entropy/validation.py](app/entropy/validation.py))
   - Shannon entropy calculation (target: ≥7.8 bits/byte)
   - Chi-square test for uniform distribution
   - Runs test for consecutive patterns
   - Autocorrelation test for self-similarity
   - Bit entropy test for bit-level randomness

5. **Entropy Pool** ([app/entropy/pool.py](app/entropy/pool.py))
   - Redis-backed storage with 1-hour TTL
   - Atomic retrieval with automatic block deletion
   - Statistics tracking (blocks added/served, average quality)
   - Health monitoring

6. **REST API** ([app/api/routes.py](app/api/routes.py))
   - `/health` - Service health and pool status
   - `/stats` - Pool statistics
   - `/random/{n}` - Retrieve 1-10240 random bytes
   - Base64-encoded responses

## Quick Start

### Prerequisites

- Docker and docker-compose
- Python 3.11+ (for local development)
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Space-Image-Based-Entropy-Generator-True-Randomness-as-a-Service-

# Install system dependencies (for OpenCV)
sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Start Redis

```bash
docker-compose up -d redis
```

### 3. Run the Service

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### 4. Test the Pipeline

```bash
# Run comprehensive end-to-end test
python test_pipeline.py

# Quick API test
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/random/256
```

## API Usage

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status": "healthy",
  "redis": {
    "redis_connected": true,
    "available_blocks": 1278,
    "available_bytes": 5234688,
    "healthy": true
  }
}
```

### Get Statistics

```bash
curl http://localhost:8000/api/v1/stats
```

Response:
```json
{
  "status": "connected",
  "available_blocks": 1278,
  "available_bytes": 5234688,
  "average_quality": 0.937,
  "blocks_added": 1281,
  "bytes_served": 5376,
  "requests_served": 3
}
```

### Get Random Bytes

```bash
# Get 256 random bytes (default)
curl http://localhost:8000/api/v1/random

# Get specific amount (1-10240 bytes)
curl http://localhost:8000/api/v1/random/1024
```

Response:
```json
{
  "bytes": "afd861741c33468547f05ef4da5cfd61...",
  "length": 256,
  "format": "base64"
}
```

### Python Client Example

```python
import requests
import base64

# Get 1024 random bytes
response = requests.get('http://localhost:8000/api/v1/random/1024')
data = response.json()

# Decode from base64
random_bytes = base64.b64decode(data['bytes'])
print(f"Retrieved {len(random_bytes)} random bytes")
print(f"First 32 bytes (hex): {random_bytes[:32].hex()}")
```

## Configuration

Environment variables (see [.env.example](.env.example)):

```bash
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_USE_SSL=False

# Entropy Pool Settings
ENTROPY_POOL_SIZE=1048576          # 1MB pool size
ENTROPY_BLOCK_SIZE=4096            # 4KB blocks
MIN_SHANNON_ENTROPY=7.8            # Quality threshold

# Image Ingestion
IMAGE_FETCH_INTERVAL=300           # Fetch every 5 minutes
IMAGES_DIR=data/images             # Local image storage
MAX_IMAGES=10                      # Keep 10 most recent

# Azure Integration (Optional)
USE_AZURE_BLOB=False
AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_CONTAINER=space-entropy
AZURE_STORAGE_SAS_TOKEN=
AZURE_USE_MANAGED_IDENTITY=False

# API Settings
API_V1_PREFIX=/api/v1
MAX_RANDOM_BYTES=10240             # Max bytes per request
```

## Performance

**Typical Performance Metrics:**

- **Entropy Generation**: ~1,281 blocks (5.2MB) from single 1024×1024 image
- **Quality Score**: Average 0.93-0.95 (threshold: 0.75)
- **Shannon Entropy**: 7.95+ bits/byte (threshold: 7.8)
- **Processing Time**: ~10-15 seconds per image
- **API Response Time**: <100ms for requests up to 10KB
- **Pool Capacity**: Configurable (default 1MB), auto-refills when below threshold

## Testing

### Run Comprehensive Test

```bash
python test_pipeline.py
```

This tests:
- Redis connection
- Image ingestion from NASA
- Noise extraction
- Cryptographic hashing
- Quality validation
- Pool storage and retrieval
- End-to-end pipeline

### Manual Testing

```bash
# Test individual modules
python -m app.ingestion.fetch_images
python -m app.preprocessing.noise_extraction
python -m app.entropy.validation
python -m app.entropy.pool
```

## Azure Deployment

For production deployment with Azure services, see [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for:

- Azure Blob Storage integration
- Azure Cache for Redis setup
- Container Apps deployment
- Cost estimates and scaling options

## Project Structure

```
├── app/
│   ├── api/                  # REST API routes
│   ├── ingestion/            # Image fetching from NASA
│   ├── preprocessing/        # Noise extraction
│   ├── entropy/              # Hashing, validation, pool
│   ├── storage/              # Azure Blob Storage (optional)
│   ├── config.py             # Configuration management
│   └── main.py               # FastAPI application
├── data/
│   └── images/               # Local image storage
├── tests/                    # Unit tests (TBD)
├── docker/                   # Docker configuration
├── docker-compose.yml        # Docker Compose setup
├── Dockerfile                # Multi-stage build
├── requirements.txt          # Python dependencies
├── test_pipeline.py          # End-to-end test script
└── README.md                 # This file
```

## How It Works

### 1. Image Acquisition
The service fetches live solar images from NASA's Solar Dynamics Observatory in 4 different wavelengths. These images capture real solar activity with inherent quantum noise.

### 2. Noise Extraction
Multiple techniques extract unpredictable noise:
- **Laplacian**: Edge detection highlights high-frequency variations
- **FFT**: Frequency domain filtering isolates random components
- **Gradients**: Sobel filters capture pixel-level variations
- **Random Sampling**: Non-deterministic region selection with time-based seeds

### 3. Cryptographic Hardening
Raw noise undergoes multiple transformations:
- **Multi-round Hashing**: 3 rounds alternating BLAKE3 and SHA-256
- **Timestamp Integration**: Microsecond UTC timestamps mixed into each block
- **Chaining**: Each block includes hash of previous block (blockchain-style)
- **Extension**: BLAKE3 XOF extends blocks to target size

### 4. Quality Assurance
Every block passes 5 statistical tests:
- **Shannon Entropy**: ≥7.8 bits/byte (near-perfect randomness)
- **Chi-Square**: Tests uniform distribution
- **Runs Test**: Detects consecutive patterns
- **Autocorrelation**: Ensures no self-similarity
- **Bit Entropy**: Validates bit-level randomness

### 5. Serving
Validated entropy is stored in Redis with:
- 1-hour TTL to ensure freshness
- Atomic retrieval prevents double-serving
- Automatic deletion after use
- Continuous background generation

## Security Considerations

### Strengths
- **Physical Entropy Source**: Real solar activity provides true randomness
- **Multiple Extraction Methods**: Reduces vulnerability to single-method weaknesses
- **Cryptographic Hardening**: Multi-round hashing whitens any residual patterns
- **Quality Validation**: Statistical tests ensure cryptographic standards
- **No Reuse**: Entropy blocks deleted after serving

### Limitations
- **Network Dependency**: Requires internet access to NASA SDO
- **Processing Overhead**: ~10-15 seconds per image generation
- **Pool Depletion**: High-volume requests may temporarily exhaust pool
- **Trust Model**: Assumes NASA image stream integrity

### Best Practices
- Use for **non-critical applications** or as **entropy mixing source**
- Combine with system entropy (`/dev/urandom`) for defense in depth
- Monitor pool statistics to avoid depletion
- Implement rate limiting for production deployments
- Rotate entropy frequently (1-hour TTL default)

## Monitoring

### Health Checks
```bash
# Check service health
curl http://localhost:8000/api/v1/health

# Monitor pool statistics
watch -n 5 'curl -s http://localhost:8000/api/v1/stats | jq'
```

### Logs
```bash
# View service logs
docker-compose logs -f app

# View Redis logs
docker-compose logs -f redis
```

### Metrics to Monitor
- `available_blocks`: Should stay above 100 for healthy operation
- `average_quality`: Should be >0.9 (warning if <0.85)
- `bytes_served` vs `blocks_added`: Track consumption rate

## Troubleshooting

### Redis Connection Failed
```bash
# Check Redis is running
docker ps | grep redis

# Restart Redis
docker-compose restart redis

# Check logs
docker-compose logs redis
```

### Low Entropy Pool
```bash
# Check current statistics
curl http://localhost:8000/api/v1/stats

# Manually trigger image fetch
python -m app.ingestion.fetch_images

# Restart background tasks
docker-compose restart app
```

### Image Fetch Failed
```bash
# Test NASA API connectivity
curl -I https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg

# Check logs for errors
docker-compose logs app | grep ERROR
```

### OpenCV Import Error
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y libgl1 libglib2.0-0
```

## Contributing

Contributions welcome! Areas for improvement:

- [ ] Comprehensive unit tests
- [ ] NIST SP 800-22 test suite integration
- [ ] GPU acceleration for image processing
- [ ] Rate limiting and API authentication
- [ ] Additional entropy sources (other space telescopes)
- [ ] Performance benchmarking suite
- [ ] Prometheus metrics export

## License

[MIT License](LICENSE)

## Acknowledgments

- **NASA SDO**: Solar Dynamics Observatory provides the space imagery
- **BLAKE3**: High-performance cryptographic hashing
- **FastAPI**: Modern Python web framework
- **Redis**: High-performance key-value store

## References

- [NASA Solar Dynamics Observatory](https://sdo.gsfc.nasa.gov/)
- [BLAKE3 Specification](https://github.com/BLAKE3-team/BLAKE3-specs)
- [NIST SP 800-22](https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final) - Statistical Test Suite for Random and Pseudorandom Number Generators
- [RFC 4086](https://www.rfc-editor.org/rfc/rfc4086) - Randomness Requirements for Security

---

**Built with ☀️ solar entropy**
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional, for containerized deployment)
- Redis (included in docker-compose)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/space-entropy-generator.git
cd space-entropy-generator
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run with Docker Compose (recommended)**
```bash
docker-compose up -d
```

5. **Or run locally**
```bash
# Start Redis
redis-server

# Run the application
python -m app.main
```

The API will be available at `http://localhost:8000`

## 📡 API Usage

### Get Random Bytes

```bash
# Get 256 random bytes (Base64 encoded)
curl http://localhost:8000/api/v1/random/256

# Get 1024 random bytes
curl http://localhost:8000/api/v1/random/1024
```

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Statistics

```bash
curl http://localhost:8000/api/v1/stats
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation.

## ⚙️ Configuration

Key configuration options in `.env`:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Entropy Pool
ENTROPY_POOL_SIZE=1048576      # 1 MB
ENTROPY_BLOCK_SIZE=4096        # 4 KB blocks
MIN_SHANNON_ENTROPY=7.8        # Quality threshold

# Image Ingestion
IMAGE_FETCH_INTERVAL=300       # Fetch every 5 minutes
MAX_STORED_IMAGES=10           # Keep last 10 images
```

## 🔬 Implementation Status

### ✅ Phase 1: Completed
- [x] Project structure
- [x] Configuration management
- [x] Image ingestion from NASA SDO
- [x] FastAPI application setup
- [x] Basic API endpoints
- [x] Docker configuration

### 🚧 Phase 2: Next Steps (In Progress)
- [ ] Image preprocessing & noise extraction
- [ ] Cryptographic hashing implementation
- [ ] Entropy validation (Shannon entropy)
- [ ] Redis entropy pool manager
- [ ] Complete API implementation

### 📋 Phase 3: Planned
- [ ] Security hardening
- [ ] Rate limiting
- [ ] NIST randomness testing integration
- [ ] Comprehensive test suite
- [ ] Performance optimization

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🔐 Security Considerations

- **Multi-source**: Uses multiple image types to prevent single-source manipulation
- **Timestamping**: Each entropy block includes timestamps to prevent replay attacks
- **Hash chaining**: Entropy blocks are cryptographically linked
- **Quality validation**: Automatic rejection of low-quality entropy
- **Rate limiting**: API access controls (to be implemented)
- **No logging**: Raw entropy is never logged

## 🌐 Data Sources

Currently supported:
- **NASA Solar Dynamics Observatory (SDO)**: Multiple wavelength solar images
  - 193 Å (1.6 million K)
  - 304 Å (50,000 K)
  - 171 Å (600,000 K)
  - 211 Å (2 million K)

Future sources:
- Hubble Space Telescope images
- Weather satellite imagery
- Ground-based telescope starfields
- Cosmic ray detectors

## 📊 Entropy Quality

Expected quality metrics:
- **Shannon Entropy**: ~7.8-8.0 bits/byte
- **NIST SP 800-22**: Pass all 15 statistical tests
- **Dieharder**: Pass comprehensive randomness battery

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NASA for providing free access to Solar Dynamics Observatory imagery
- Inspired by Cloudflare's lava lamp entropy wall
- Built with FastAPI, OpenCV, and modern Python tools

## 📮 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Note**: This is a research/educational project. For production cryptographic applications, always combine multiple entropy sources and consult security experts.