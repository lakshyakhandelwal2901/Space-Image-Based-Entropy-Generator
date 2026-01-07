# Azure Deployment Guide

## Quick Setup with Azure Free Credits

This guide shows you how to deploy the Space Entropy Generator using your Azure free credits.

### Prerequisites
- Azure account with free credits
- Azure CLI installed (`az --version`)
- Logged in to Azure CLI (`az login`)

---

## Option 1: Local Redis + Azure Blob (Simplest)

Use local Docker Redis for development, Azure Blob for image storage backup.

```bash
# 1. Create resource group
az group create --name space-entropy-rg --location eastus

# 2. Create storage account
az storage account create \
  --name spaceentropy$(date +%s) \
  --resource-group space-entropy-rg \
  --location eastus \
  --sku Standard_LRS

# 3. Get connection string
STORAGE_CONNECTION=$(az storage account show-connection-string \
  --name spaceentropy* \
  --resource-group space-entropy-rg \
  --query connectionString -o tsv)

# 4. Create container
az storage container create \
  --name space-entropy-images \
  --connection-string "$STORAGE_CONNECTION"

# 5. Update .env
echo "USE_AZURE_BLOB=True" >> .env
echo "AZURE_STORAGE_CONNECTION_STRING=$STORAGE_CONNECTION" >> .env
echo "AZURE_STORAGE_CONTAINER=space-entropy-images" >> .env
```

---

## Option 2: Azure Cache for Redis + Blob (Production-ready)

Use managed Azure Redis (SSL-enabled) instead of local Docker.

```bash
# 1-4. Same as Option 1 (create RG + Storage + Container)

# 5. Create Azure Cache for Redis (Basic C0 - Free tier eligible)
az redis create \
  --name space-entropy-redis \
  --resource-group space-entropy-rg \
  --location eastus \
  --sku Basic \
  --vm-size c0 \
  --enable-non-ssl-port false

# 6. Get Redis credentials
REDIS_HOST=$(az redis show --name space-entropy-redis \
  --resource-group space-entropy-rg \
  --query hostName -o tsv)

REDIS_PASSWORD=$(az redis list-keys --name space-entropy-redis \
  --resource-group space-entropy-rg \
  --query primaryKey -o tsv)

# 7. Update .env for Azure Redis
cat >> .env << EOF
REDIS_HOST=$REDIS_HOST
REDIS_PORT=6380
REDIS_PASSWORD=$REDIS_PASSWORD
REDIS_USE_SSL=True
USE_AZURE_BLOB=True
AZURE_STORAGE_CONNECTION_STRING=$STORAGE_CONNECTION
EOF

# 8. Test locally
docker-compose down
python -m app.main
```

---

## Option 3: Full Azure Deployment (Container Apps)

Deploy the entire API to Azure Container Apps (serverless containers).

```bash
# 1-6. Same as Option 2 (RG + Storage + Redis)

# 7. Create container registry
az acr create \
  --resource-group space-entropy-rg \
  --name spaceentropyacr \
  --sku Basic \
  --admin-enabled true

# 8. Build and push image
az acr build \
  --registry spaceentropyacr \
  --image space-entropy-api:latest \
  --file docker/Dockerfile .

# 9. Create Container Apps environment
az containerapp env create \
  --name space-entropy-env \
  --resource-group space-entropy-rg \
  --location eastus

# 10. Deploy Container App
az containerapp create \
  --name space-entropy-api \
  --resource-group space-entropy-rg \
  --environment space-entropy-env \
  --image spaceentropyacr.azurecr.io/space-entropy-api:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server spaceentropyacr.azurecr.io \
  --env-vars \
    REDIS_HOST=$REDIS_HOST \
    REDIS_PORT=6380 \
    REDIS_PASSWORD=$REDIS_PASSWORD \
    REDIS_USE_SSL=True \
    USE_AZURE_BLOB=True \
    AZURE_STORAGE_CONNECTION_STRING="$STORAGE_CONNECTION"

# 11. Get app URL
az containerapp show \
  --name space-entropy-api \
  --resource-group space-entropy-rg \
  --query properties.configuration.ingress.fqdn -o tsv
```

---

## Cost Estimates (with Free Credits)

| Service | SKU | Monthly Cost | Free Tier |
|---------|-----|--------------|-----------|
| **Redis** | Basic C0 (250 MB) | ~$16 | ✅ 12 months free |
| **Storage** | LRS (5 GB) | <$1 | ✅ 12 months free |
| **Container Apps** | Consumption | Pay per use | ✅ Free quota (180k vCPU-s, 360k GiB-s) |
| **Container Registry** | Basic | $5 | First 10 GB free |

**Total with free credits**: ~$0-5/month for the first year

---

## Environment Variables Reference

### Local Development (.env)
```bash
# API
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Local Redis (Docker)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_USE_SSL=False

# No Azure
USE_AZURE_BLOB=False
```

### Azure Redis + Blob (.env)
```bash
# API
DEBUG=False
API_HOST=0.0.0.0
API_PORT=8000

# Azure Cache for Redis
REDIS_HOST=space-entropy-redis.redis.cache.windows.net
REDIS_PORT=6380
REDIS_PASSWORD=<your-primary-key>
REDIS_USE_SSL=True
REDIS_DB=0

# Azure Blob Storage
USE_AZURE_BLOB=True
AZURE_STORAGE_CONNECTION_STRING=<your-connection-string>
AZURE_STORAGE_CONTAINER=space-entropy-images
```

---

## Testing Your Azure Setup

```bash
# Health check
curl https://your-app.azurecontainerapps.io/api/v1/health

# Get random bytes
curl https://your-app.azurecontainerapps.io/api/v1/random/256

# View stats
curl https://your-app.azurecontainerapps.io/api/v1/stats

# Interactive docs
open https://your-app.azurecontainerapps.io/docs
```

---

## Cleanup (when done testing)

```bash
# Delete everything
az group delete --name space-entropy-rg --yes --no-wait
```

---

## Monitoring (Optional)

Add Application Insights for observability:

```bash
# Create App Insights
az monitor app-insights component create \
  --app space-entropy-insights \
  --location eastus \
  --resource-group space-entropy-rg

# Get instrumentation key
INSIGHTS_KEY=$(az monitor app-insights component show \
  --app space-entropy-insights \
  --resource-group space-entropy-rg \
  --query instrumentationKey -o tsv)

# Add to Container App
az containerapp update \
  --name space-entropy-api \
  --resource-group space-entropy-rg \
  --set-env-vars APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$INSIGHTS_KEY"
```

---

## Security Best Practices

1. **Use Key Vault** for secrets (instead of env vars):
   ```bash
   az keyvault create --name space-entropy-kv --resource-group space-entropy-rg
   az keyvault secret set --vault-name space-entropy-kv --name redis-password --value "$REDIS_PASSWORD"
   ```

2. **Enable Managed Identity** for Container App to access Storage without connection strings:
   ```bash
   az containerapp identity assign --name space-entropy-api --resource-group space-entropy-rg --system-assigned
   ```

3. **Restrict Redis access** to your Container App's IP/VNET only

4. **Enable API rate limiting** (add FastAPI rate limit middleware)

---

## Troubleshooting

### Redis Connection Issues
```bash
# Test Redis connectivity
az redis show --name space-entropy-redis --resource-group space-entropy-rg

# Check firewall rules
az redis firewall-rules list --name space-entropy-redis --resource-group space-entropy-rg
```

### Storage Issues
```bash
# Verify container exists
az storage container list --connection-string "$STORAGE_CONNECTION"

# Test upload
echo "test" > test.txt
az storage blob upload --container-name space-entropy-images --file test.txt --name test.txt --connection-string "$STORAGE_CONNECTION"
```

### Container App Logs
```bash
# View logs
az containerapp logs show --name space-entropy-api --resource-group space-entropy-rg --follow

# Check revisions
az containerapp revision list --name space-entropy-api --resource-group space-entropy-rg
```

---

## Next Steps

- Set up CI/CD with GitHub Actions
- Add custom domain + SSL certificate
- Enable autoscaling based on request load
- Implement API authentication
- Add rate limiting and DDoS protection (Azure Front Door)
