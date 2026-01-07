# Production Deployment Guide

This guide covers deploying the Space Entropy Generator to production environments.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Security Hardening](#security-hardening)
- [Monitoring and Observability](#monitoring-and-observability)
- [Performance Tuning](#performance-tuning)
- [High Availability](#high-availability)

## Docker Deployment

### Build and Run with Docker Compose

```bash
# Build the image
docker-compose build

# Start all services
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Production Docker Compose

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --maxmemory 1gb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  app:
    build:
      context: .
      dockerfile: Dockerfile
    restart: always
    ports:
      - "8000:8000"
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ENTROPY_POOL_SIZE=2097152  # 2MB
      - LOG_LEVEL=INFO
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app

volumes:
  redis_data:
```

### NGINX Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=random_limit:10m rate=5r/s;

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000" always;

        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /api/v1/health {
            proxy_pass http://app;
            limit_req zone=api_limit burst=20;
        }

        location /api/v1/random/ {
            proxy_pass http://app;
            limit_req zone=random_limit burst=10;
        }
    }
}
```

## Kubernetes Deployment

### Namespace and ConfigMap

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: space-entropy

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: entropy-config
  namespace: space-entropy
data:
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  ENTROPY_POOL_SIZE: "2097152"
  IMAGE_FETCH_INTERVAL: "300"
  LOG_LEVEL: "INFO"
```

### Redis Deployment

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: redis-pvc
  namespace: space-entropy
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: space-entropy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        volumeMounts:
        - name: redis-storage
          mountPath: /data
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
      volumes:
      - name: redis-storage
        persistentVolumeClaim:
          claimName: redis-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: space-entropy
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

### Application Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: entropy-app
  namespace: space-entropy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: entropy-app
  template:
    metadata:
      labels:
        app: entropy-app
    spec:
      containers:
      - name: app
        image: your-registry/space-entropy:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: entropy-config
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"

---
apiVersion: v1
kind: Service
metadata:
  name: entropy-service
  namespace: space-entropy
spec:
  selector:
    app: entropy-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: entropy-ingress
  namespace: space-entropy
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - entropy.your-domain.com
    secretName: entropy-tls
  rules:
  - host: entropy.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: entropy-service
            port:
              number: 80
```

## Security Hardening

### 1. API Key Authentication

Update [app/api/routes.py](app/api/routes.py):

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    valid_keys = settings.api_keys.split(',')
    if x_api_key not in valid_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return x_api_key

@router.get("/random/{n}", dependencies=[Depends(verify_api_key)])
async def get_random_bytes(n: int = Path(..., ge=1, le=10240)):
    # ... rest of the code
```

### 2. Rate Limiting

Install FastAPI rate limiter:

```bash
pip install slowapi
```

Update [app/main.py](app/main.py):

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/random/{n}")
@limiter.limit("10/minute")
async def get_random(request: Request, n: int):
    # ... rest of the code
```

### 3. HTTPS/TLS

Generate SSL certificates:

```bash
# Using Let's Encrypt
certbot certonly --standalone -d your-domain.com

# Or self-signed for testing
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem
```

### 4. Redis Authentication

Update docker-compose:

```yaml
redis:
  command: redis-server --requirepass YOUR_STRONG_PASSWORD
```

Update environment:

```bash
REDIS_PASSWORD=YOUR_STRONG_PASSWORD
```

## Monitoring and Observability

### Prometheus Metrics

Install prometheus-fastapi-instrumentator:

```bash
pip install prometheus-fastapi-instrumentator
```

Update [app/main.py](app/main.py):

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)
```

### Prometheus Configuration

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'space-entropy'
    static_configs:
      - targets: ['app:8000']
```

### Grafana Dashboard

Key metrics to monitor:

- Request rate (requests/second)
- Response times (p50, p95, p99)
- Error rate (5xx responses)
- Entropy pool size (bytes available)
- Entropy quality score (average)
- Redis connection status

### Logging

Configure structured logging in [app/config.py](app/config.py):

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        return json.dumps(log_data)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

## Performance Tuning

### 1. Redis Optimization

```bash
# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Connection pooling
maxclients 10000
```

### 2. FastAPI Workers

Use Gunicorn with Uvicorn workers:

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive 5
```

### 3. Image Processing Optimization

Enable OpenCV optimizations in [app/preprocessing/noise_extraction.py](app/preprocessing/noise_extraction.py):

```python
import cv2

# Use multiple threads
cv2.setNumThreads(4)

# Enable hardware acceleration
cv2.setUseOptimized(True)
```

### 4. Connection Pooling

Update Redis connection in [app/entropy/pool.py](app/entropy/pool.py):

```python
pool = redis.ConnectionPool(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    max_connections=50,
    socket_keepalive=True,
    socket_connect_timeout=5
)
redis_client = redis.Redis(connection_pool=pool)
```

## High Availability

### Redis Sentinel

For Redis high availability, use Sentinel:

```yaml
services:
  redis-master:
    image: redis:7-alpine
    command: redis-server --appendonly yes

  redis-replica:
    image: redis:7-alpine
    command: redis-server --replicaof redis-master 6379

  sentinel:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
```

### Load Balancing

Use multiple app instances behind a load balancer:

```yaml
app:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '2'
        memory: 2G
```

### Health Checks

Implement comprehensive health checks:

```python
@router.get("/health/detailed")
async def detailed_health():
    checks = {
        "redis": await entropy_pool.health_check(),
        "pool_size": await entropy_pool.get_stats(),
        "disk_space": check_disk_space(),
        "memory": check_memory_usage(),
        "image_source": await check_nasa_api()
    }
    
    all_healthy = all(c.get("healthy", False) for c in checks.values())
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }
```

## Backup and Disaster Recovery

### Redis Backup

```bash
# Manual backup
docker exec redis redis-cli BGSAVE

# Automated backup script
#!/bin/bash
docker exec redis redis-cli BGSAVE
sleep 10
docker cp redis:/data/dump.rdb /backups/redis-$(date +%Y%m%d-%H%M%S).rdb
```

### Configuration Backup

```bash
# Backup environment and config
tar czf config-backup-$(date +%Y%m%d).tar.gz \
  .env \
  docker-compose.yml \
  nginx.conf
```

## Troubleshooting

### High Memory Usage

```bash
# Check Redis memory
redis-cli INFO memory

# Monitor app memory
docker stats

# Reduce pool size
ENTROPY_POOL_SIZE=524288  # 512KB
```

### Slow Response Times

```bash
# Check Redis latency
redis-cli --latency

# Profile Python code
pip install py-spy
py-spy top --pid $(pgrep -f "python -m app.main")
```

### Connection Timeouts

```bash
# Increase timeouts
REDIS_SOCKET_TIMEOUT=10
REDIS_SOCKET_CONNECT_TIMEOUT=5

# Check network
docker exec app ping redis
```

## Maintenance

### Update Dependencies

```bash
# Update Python packages
pip list --outdated
pip install --upgrade -r requirements.txt

# Update Docker images
docker-compose pull
docker-compose up -d
```

### Log Rotation

Configure logrotate:

```
/var/log/space-entropy/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
    sharedscripts
    postrotate
        docker-compose restart app
    endscript
}
```

---

**Need help?** File an issue on GitHub or check the [README](README.md) for more details.
