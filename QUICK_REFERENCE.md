# Quick Reference Guide

## One-Liners

### Start the Service
```bash
docker-compose up -d redis && python -m app.main
```

### Test Everything
```bash
python test_pipeline.py
```

### Get Random Bytes
```bash
curl http://localhost:8000/api/v1/random/256
```

### Check Health
```bash
curl http://localhost:8000/api/v1/health | jq
```

### Monitor Pool
```bash
watch -n 5 'curl -s http://localhost:8000/api/v1/stats | jq'
```

---

## API Endpoints

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Service info | `curl http://localhost:8000/` |
| `/api/v1/health` | GET | Health check | `curl http://localhost:8000/api/v1/health` |
| `/api/v1/stats` | GET | Pool statistics | `curl http://localhost:8000/api/v1/stats` |
| `/api/v1/random` | GET | 256 random bytes | `curl http://localhost:8000/api/v1/random` |
| `/api/v1/random/{n}` | GET | N random bytes (1-10240) | `curl http://localhost:8000/api/v1/random/1024` |

---

## Configuration Quick Reference

### Key Environment Variables

```bash
# Redis
REDIS_HOST=localhost           # Redis server address
REDIS_PORT=6379                # Redis port
REDIS_USE_SSL=False            # Enable SSL for Azure Redis

# Pool Settings
ENTROPY_POOL_SIZE=1048576      # 1MB pool size
ENTROPY_BLOCK_SIZE=4096        # 4KB blocks
MIN_SHANNON_ENTROPY=7.8        # Quality threshold

# Image Fetching
IMAGE_FETCH_INTERVAL=300       # Fetch every 5 minutes
MAX_IMAGES=10                  # Keep 10 images

# Azure (Optional)
USE_AZURE_BLOB=False           # Enable Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=  # Connection string
```

---

## Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart specific service
docker-compose restart app

# Check status
docker-compose ps

# Clean everything
docker-compose down -v
```

---

## Maintenance Commands

### Redis Operations
```bash
# Connect to Redis CLI
docker exec -it redis redis-cli

# Check memory usage
docker exec redis redis-cli INFO memory

# Monitor commands
docker exec redis redis-cli MONITOR

# Flush database (DANGER)
docker exec redis redis-cli FLUSHALL
```

### System Monitoring
```bash
# Check container resources
docker stats

# Check logs in real-time
docker-compose logs -f app | grep ERROR

# Monitor API requests
docker-compose logs -f app | grep "GET /api"
```

---

## Python API Client

### Basic Usage
```python
import requests
import base64

# Get random bytes
response = requests.get('http://localhost:8000/api/v1/random/1024')
data = response.json()

# Decode from base64
random_bytes = base64.b64decode(data['bytes'])
print(f"Got {len(random_bytes)} random bytes")
```

### Advanced Usage
```python
import requests
import base64
import time

class EntropyClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_random(self, n_bytes=256):
        """Get n random bytes"""
        response = self.session.get(f'{self.base_url}/api/v1/random/{n_bytes}')
        response.raise_for_status()
        data = response.json()
        return base64.b64decode(data['bytes'])
    
    def get_health(self):
        """Check service health"""
        response = self.session.get(f'{self.base_url}/api/v1/health')
        return response.json()
    
    def get_stats(self):
        """Get pool statistics"""
        response = self.session.get(f'{self.base_url}/api/v1/stats')
        return response.json()
    
    def wait_for_entropy(self, min_bytes=4096, timeout=60):
        """Wait until enough entropy is available"""
        start = time.time()
        while time.time() - start < timeout:
            stats = self.get_stats()
            if stats['available_bytes'] >= min_bytes:
                return True
            time.sleep(1)
        return False

# Example usage
client = EntropyClient()

# Check health
health = client.get_health()
print(f"Status: {health['status']}")

# Get random data
random_data = client.get_random(1024)
print(f"Got {len(random_data)} bytes")

# Monitor pool
stats = client.get_stats()
print(f"Available: {stats['available_blocks']} blocks ({stats['available_bytes']} bytes)")
print(f"Quality: {stats['average_quality']:.3f}")
```

---

## Troubleshooting Quick Fixes

### Redis Not Connected
```bash
# Check if Redis is running
docker ps | grep redis

# Restart Redis
docker-compose restart redis

# Check Redis logs
docker-compose logs redis
```

### Low Entropy Pool
```bash
# Check current status
curl http://localhost:8000/api/v1/stats

# Manually fetch images
docker exec -it app python -m app.ingestion.fetch_images

# Restart background tasks
docker-compose restart app
```

### Image Fetch Failed
```bash
# Test NASA API connectivity
curl -I https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg

# Check proxy settings
echo $http_proxy

# Check DNS
nslookup sdo.gsfc.nasa.gov
```

### High Memory Usage
```bash
# Check memory usage
docker stats

# Reduce pool size in .env
ENTROPY_POOL_SIZE=524288  # 512KB

# Restart with new settings
docker-compose restart app
```

### OpenCV Import Error
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y libgl1 libglib2.0-0

# Reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python
```

---

## Performance Tips

### Increase Throughput
```bash
# Increase pool size
ENTROPY_POOL_SIZE=2097152  # 2MB

# Reduce fetch interval
IMAGE_FETCH_INTERVAL=180   # 3 minutes

# Use more Redis connections
# Edit app/entropy/pool.py - increase max_connections
```

### Reduce Latency
```bash
# Use smaller blocks
ENTROPY_BLOCK_SIZE=2048    # 2KB

# Enable Redis pipelining (already enabled)

# Use connection pooling (already enabled)
```

### Scale Horizontally
```bash
# Run multiple app instances
docker-compose up -d --scale app=3

# Use load balancer
# See DEPLOYMENT.md for NGINX config
```

---

## Quality Metrics

### What to Monitor

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Shannon Entropy | ≥7.9 | 7.8-7.9 | <7.8 |
| Quality Score | ≥0.9 | 0.75-0.9 | <0.75 |
| Available Blocks | >100 | 10-100 | <10 |
| Response Time | <100ms | 100-500ms | >500ms |
| Error Rate | 0% | <1% | ≥1% |

### Sample Quality Check
```bash
# Get multiple samples and check quality
for i in {1..10}; do
  curl -s http://localhost:8000/api/v1/random/1024 | jq -r '.bytes' | base64 -d | xxd | head -n 5
done
```

---

## Development Workflow

### Make Changes
```bash
# 1. Edit code
vim app/api/routes.py

# 2. Restart app
docker-compose restart app

# 3. Check logs
docker-compose logs -f app

# 4. Test
curl http://localhost:8000/api/v1/health
```

### Add New Feature
```bash
# 1. Create feature branch
git checkout -b feature/new-endpoint

# 2. Implement changes
# ... edit files ...

# 3. Test locally
python test_pipeline.py

# 4. Commit and push
git add .
git commit -m "Add new feature"
git push origin feature/new-endpoint
```

---

## Useful Queries

### Redis Inspection
```bash
# List all entropy blocks
docker exec redis redis-cli KEYS "entropy:block:*"

# Count blocks
docker exec redis redis-cli KEYS "entropy:block:*" | wc -l

# Check block details
docker exec redis redis-cli GET "entropy:block:123e4567-e89b-12d3-a456-426614174000"

# Check TTL
docker exec redis redis-cli TTL "entropy:block:123e4567-e89b-12d3-a456-426614174000"
```

### Log Analysis
```bash
# Count requests
docker-compose logs app | grep "GET /api/v1/random" | wc -l

# Find errors
docker-compose logs app | grep ERROR

# Monitor image fetching
docker-compose logs app | grep "Fetched image"

# Track entropy generation
docker-compose logs app | grep "Added.*blocks to pool"
```

---

## Testing Snippets

### Load Test
```bash
# Simple load test with Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/v1/random/256

# With curl and parallel
seq 1 100 | parallel -j10 "curl -s http://localhost:8000/api/v1/random/256 > /dev/null"
```

### Validate Randomness
```python
import requests
import base64
from collections import Counter

# Get sample
response = requests.get('http://localhost:8000/api/v1/random/10240')
data = base64.b64decode(response.json()['bytes'])

# Check byte distribution
counts = Counter(data)
print(f"Unique bytes: {len(counts)}/256")
print(f"Most common: {counts.most_common(5)}")
print(f"Least common: {counts.most_common()[-5:]}")

# Expected: roughly 40 occurrences each for 10KB
```

---

## Resource Limits

### Recommended Resources

**Development:**
- CPU: 1 core
- Memory: 1GB
- Disk: 10GB

**Production:**
- CPU: 2-4 cores
- Memory: 2-4GB
- Disk: 50GB
- Network: 10 Mbps

### Docker Resource Limits
```yaml
# In docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M
```

---

## Security Checklist

- [ ] Change default Redis password
- [ ] Enable TLS/SSL for production
- [ ] Add API key authentication
- [ ] Configure rate limiting
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Monitor for anomalies
- [ ] Backup configuration
- [ ] Document incident response

---

## Quick Links

- [Full Documentation](README.md)
- [Azure Deployment](AZURE_DEPLOYMENT.md)
- [Production Deployment](DEPLOYMENT.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

**Need more help?** Check the detailed documentation or open an issue on GitHub.
