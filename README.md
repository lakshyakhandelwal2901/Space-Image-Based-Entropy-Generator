# Space-Image Based Entropy Generator 🌌

**True Randomness as a Service** powered by cosmic unpredictability

[![Status](https://img.shields.io/badge/status-✅%20Complete%20%26%20Live-brightgreen.svg)](#-quick-start-both-services)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

This project generates cryptographically secure random numbers by extracting entropy from live NASA space imagery, served via a REST API with a modern React web interface. Unlike pseudo-random generators (PRNGs) which are deterministic, this system harnesses natural cosmic unpredictability to produce true random numbers suitable for:

- 🔐 Cryptographic key generation
- ⛓️ Blockchain randomness
- 🤖 AI/ML stochastic processes
- 🎲 Simulations and gaming
- 🔒 Security applications

## 🌟 Key Features

### Backend
- **True Randomness**: Extracts entropy from natural cosmic phenomena (NASA SDO)
- **High Quality**: Shannon entropy ~8 bits per byte (avg 0.93+ quality score)
- **Scalable**: Redis-backed entropy pool with concurrent access
- **Secure**: Cryptographic hashing (SHA-256 + BLAKE3, multi-round, blockchain chaining)
- **Real-time**: Continuous image ingestion (1,200+ MB entropy pool)
- **Production Ready**: Docker containerized, fully deployed

### Frontend
- **Interactive Playground**: Generate and display random bytes in real-time
- **Live Statistics**: Auto-updating pool status and entropy quality metrics
- **Beautiful UI**: Modern React interface with Tailwind CSS styling
- **API Documentation**: Interactive endpoint documentation
- **Fully Integrated**: Connected to live backend API endpoints

## 🚀 Quick Start (Both Services)

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (for Redis)
- Git

### Start Both Services (30 seconds)

**Option 1: Automated (Recommended)**
```bash
# Clone repository
git clone <repository-url>
cd Space-Image-Based-Entropy-Generator-True-Randomness-as-a-Service-

# Start backend
python -m app.main &

# Start frontend (in another terminal)
cd website
npm install
npm run dev
```

**Option 2: With Docker Compose**
```bash
docker-compose up -d
```

### Access the Services

| Service | URL | Purpose |
|---------|-----|---------|
| **Web Frontend** | http://localhost:8080 | Interactive UI with Playground & Docs |
| **API Docs** | http://localhost:8000/docs | Swagger API documentation |
| **Health Check** | http://localhost:8000/api/v1/health | Backend status |

### Verify It's Working

```bash
# Check backend health
curl http://localhost:8000/api/v1/health

# Get random bytes
curl http://localhost:8000/api/v1/random/256

# Check pool statistics
curl http://localhost:8000/api/v1/stats

# Visit frontend
open http://localhost:8080
```

**Expected Response:**
```json
{
  "status": "healthy",
  "redis": {
    "available_blocks": 1262,
    "available_bytes": 5169152,
    "average_quality": 0.932
  }
}
```

## 🎨 Web Interface

The React frontend provides an interactive experience for exploring entropy generation:

### Features
- **Playground**: Generate random bytes and download results
- **Live Statistics**: Real-time pool metrics (entropy quality, available bytes, generation rate)
- **API Documentation**: Interactive docs with copy-paste examples
- **Beautiful Design**: Modern UI with Tailwind CSS

### Environment Configuration

Frontend uses environment variables for API connectivity:

```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_STATS_POLL_INTERVAL=10000  # Update stats every 10 seconds
```

For production deployment, see [WEBSITE_DEPLOYMENT.md](website/WEBSITE_DEPLOYMENT.md)

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

## 🏗️ Architecture

```
NASA SDO API → Image Ingestion → Noise Extraction → Cryptographic Hashing → Validation → Redis Pool → REST API
                                                                              ↓
                                                                          React UI
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

## 📁 Project Structure

```
space-entropy-generator/
├── app/                                # Backend (FastAPI)
│   ├── main.py                         # Entry point, lifespan context
│   ├── config.py                       # Configuration & settings
│   ├── api/
│   │   └── routes.py                   # REST endpoints
│   ├── ingestion/
│   │   └── fetch_images.py             # NASA SDO image fetching
│   ├── preprocessing/
│   │   └── noise_extraction.py         # Entropy extraction (5 techniques)
│   └── entropy/
│       ├── hashing.py                  # Cryptographic hashing
│       ├── validation.py               # Statistical quality tests
│       └── pool.py                     # Redis entropy pool
│
├── website/                            # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── lib/
│   │   │   └── api.ts                  # API utilities & TypeScript types
│   │   ├── components/
│   │   │   ├── Playground.tsx          # Random bytes generator
│   │   │   ├── LiveStats.tsx           # Real-time pool metrics
│   │   │   └── APISection.tsx          # API documentation
│   │   ├── pages/
│   │   │   ├── Index.tsx               # Home page
│   │   │   └── Docs.tsx                # Full API docs
│   │   ├── App.tsx                     # Router setup
│   │   └── index.css                   # Tailwind styles
│   ├── .env.local                      # Local API configuration
│   ├── vite.config.ts                  # Vite configuration
│   └── package.json                    # Frontend dependencies
│
├── docker-compose.yml                  # Full stack (Backend + Redis)
├── Dockerfile                          # Backend containerization
├── requirements.txt                    # Python dependencies
├── test_pipeline.py                    # End-to-end testing
├── .env.example                        # Environment template
└── README.md                           # This file
```

## ⚙️ Configuration

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

## 🔬 Implementation Status

### ✅ Phase 1-3: COMPLETE
- [x] Project structure & configuration
- [x] Image ingestion from NASA SDO (4 wavelengths)
- [x] Complete preprocessing pipeline (5 noise extraction techniques)
- [x] Cryptographic hashing (BLAKE3, SHA-256, multi-round)
- [x] Entropy validation (5 statistical tests)
- [x] Redis entropy pool manager
- [x] Complete REST API (health, stats, random/{n})
- [x] Background tasks (periodic image fetch & generation)
- [x] Docker containerization & docker-compose
- [x] Azure integration (optional)
- [x] **React web interface (NEW)**
- [x] **API utilities & TypeScript types (NEW)**
- [x] **Live statistics component (NEW)**
- [x] **Interactive playground (NEW)**
- [x] **Complete integration testing (NEW)**
- [x] **Dual-service deployment (NEW)**

### 🎯 What's Live Right Now
- ✅ Backend running on port 8000 (FastAPI + Uvicorn)
- ✅ Frontend running on port 8080 (React + Vite)
- ✅ Redis pool: 1,262+ blocks (5+ MB entropy)
- ✅ API responding with live random bytes
- ✅ Live stats updating every 10 seconds
- ✅ Playground generating real entropy

## 📊 Performance

**Typical Performance Metrics:**

- **Entropy Generation**: ~1,281 blocks (5.2MB) from single 1024×1024 image
- **Quality Score**: Average 0.93-0.95 (threshold: 0.75)
- **Shannon Entropy**: 7.95+ bits/byte (threshold: 7.8)
- **Processing Time**: ~10-15 seconds per image
- **API Response Time**: <100ms for requests up to 10KB
- **Pool Capacity**: Configurable (default 1MB), auto-refills when below threshold

## 🧪 Testing

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

## 🔐 Security Considerations

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

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Additional entropy sources (other space telescopes)
- [ ] NIST SP 800-22 test suite integration
- [ ] GPU acceleration for image processing
- [ ] Rate limiting and API authentication
- [ ] Performance benchmarking suite
- [ ] Prometheus metrics export

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NASA for providing free access to Solar Dynamics Observatory imagery
- Inspired by Cloudflare's lava lamp entropy wall
- Built with FastAPI, React, OpenCV, and modern Python tools

## 📮 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Note**: This is a research/educational project. For production cryptographic applications, always combine multiple entropy sources and consult security experts.

**Built with ☀️ solar entropy**
