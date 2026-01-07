# Website Deployment Guide

This document explains how to deploy the Entropy.Space marketing website alongside the backend API.

## Architecture Overview

The website is a static React SPA that connects to your backend API via HTTP requests:

```
┌──────────────┐         HTTP          ┌──────────────┐
│   Website    │ ────────────────────> │   Backend    │
│  (Static)    │  /api/v1/health       │  (FastAPI)   │
│  React SPA   │  /api/v1/stats        │  Python      │
│              │  /api/v1/random/{n}   │              │
└──────────────┘                       └──────────────┘
```

## Option 1: Deploy on Vercel (Recommended for Website)

### Prerequisites
- GitHub account
- Vercel account (free tier is fine)
- Backend API already deployed (e.g., on Render)

### Steps

1. **Push Website to GitHub**
   ```bash
   cd website/solar-entropy-api-main/solar-entropy-api-main
   git add .
   git commit -m "Prepare website for deployment"
   git push
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Click "Import Project"
   - Select your GitHub repository
   - Set root directory: `website/solar-entropy-api-main/solar-entropy-api-main`

3. **Configure Build Settings**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Add Environment Variables**
   In Vercel dashboard → Settings → Environment Variables:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api/v1
   VITE_STATS_POLL_INTERVAL=10000
   ```

5. **Deploy**
   - Click "Deploy"
   - Your site will be live at `https://<project-name>.vercel.app`

6. **Optional: Custom Domain**
   - Vercel dashboard → Domains
   - Add your domain (e.g., `entropy.space`)
   - Update DNS records as instructed

## Option 2: Deploy on Netlify

### Steps

1. **Build the Website**
   ```bash
   cd website/solar-entropy-api-main/solar-entropy-api-main
   npm install
   npm run build
   ```

2. **Connect to Netlify**
   - Go to https://netlify.com
   - Drag and drop the `dist/` folder
   - Or connect via GitHub for auto-deploy

3. **Configure Environment**
   - Site settings → Environment variables
   - Add `VITE_API_BASE_URL`

4. **Configure Build**
   ```toml
   # netlify.toml
   [build]
     command = "npm run build"
     publish = "dist"
     base = "website/solar-entropy-api-main/solar-entropy-api-main"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200
   ```

## Option 3: Deploy on Render (Static Site)

### Steps

1. **Create New Static Site**
   - Go to Render dashboard
   - New → Static Site
   - Connect your GitHub repo

2. **Configure**
   - Root Directory: `website/solar-entropy-api-main/solar-entropy-api-main`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. **Environment Variables**
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api/v1
   ```

4. **Deploy**
   - Render will auto-build and deploy
   - Live at `https://<site-name>.onrender.com`

## Option 4: Same Server as Backend (Not Recommended)

You can serve the website from the FastAPI backend, but this couples your frontend and backend.

### Steps

1. **Build Website**
   ```bash
   cd website/solar-entropy-api-main/solar-entropy-api-main
   npm run build
   ```

2. **Copy Build to Backend**
   ```bash
   cp -r dist/* ../../app/static/
   ```

3. **Update FastAPI to Serve Static Files**
   ```python
   # app/main.py
   from fastapi.staticfiles import StaticFiles
   
   app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
   ```

4. **Deploy Backend with Website Included**

## CORS Configuration

If your website and backend are on different domains, configure CORS in the backend:

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-website.vercel.app",
        "https://entropy.space",  # Your custom domain
        "http://localhost:8080",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables Reference

### Website

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | `https://api.entropy.space/api/v1` |
| `VITE_STATS_POLL_INTERVAL` | Stats refresh interval (ms) | `10000` |

### Backend

See main `DEPLOYMENT.md` for backend env vars.

## Testing After Deployment

1. **Check Health Endpoint**
   ```bash
   curl https://your-website.com/api/v1/health
   ```

2. **Test Playground**
   - Visit https://your-website.com
   - Scroll to Playground
   - Click "Generate"
   - Verify random bytes are fetched

3. **Verify Stats**
   - Check Hero section stats
   - Confirm they update every 10 seconds
   - Open browser console to check for errors

## Troubleshooting

### CORS Errors

**Problem**: Browser console shows CORS errors  
**Solution**: Add your website domain to backend CORS origins

### API Connection Failed

**Problem**: "Failed to fetch" errors  
**Solution**: 
- Verify `VITE_API_BASE_URL` is correct
- Check backend is running and accessible
- Ensure backend has HTTPS (or both are HTTP)

### Build Fails on Deployment

**Problem**: npm install or build fails  
**Solution**:
- Verify Node.js version (should be 16+)
- Check for TypeScript errors locally first
- Review deployment logs for specific error

### Stats Not Updating

**Problem**: Hero stats show default values  
**Solution**:
- Check `/stats` endpoint is working
- Verify CORS allows cross-origin requests
- Inspect browser Network tab for failed requests

## Performance Optimization

### 1. Enable Compression
Most hosting platforms (Vercel, Netlify) handle this automatically.

### 2. Configure Caching
Add cache headers for static assets:
```nginx
# Example Nginx config
location /assets/ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}
```

### 3. Use CDN
Vercel and Netlify include CDN by default. For custom hosting, use Cloudflare.

### 4. Optimize Images
If you add images:
```bash
npm install --save-dev vite-plugin-imagemin
```

## Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **Environment Variables**: Never commit `.env.local` to git
3. **API Rate Limiting**: Backend should enforce rate limits
4. **CORS Restrictive**: Only allow your website domains
5. **No Secrets Client-Side**: Never expose API keys or secrets in frontend code

## Monitoring

### Analytics
Add to `index.html`:
```html
<!-- Plausible Analytics -->
<script defer data-domain="entropy.space" src="https://plausible.io/js/script.js"></script>
```

### Error Tracking
Add Sentry:
```bash
npm install @sentry/react
```

```typescript
// src/main.tsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: import.meta.env.MODE,
});
```

## Cost Estimate

### Vercel
- **Free Tier**: 100 GB bandwidth/month, unlimited projects
- **Pro**: $20/month (commercial projects)

### Netlify
- **Free Tier**: 100 GB bandwidth/month
- **Pro**: $19/month

### Render
- **Static Site**: Free with 100 GB bandwidth/month

All tiers are sufficient for small to medium traffic.

## Next Steps

1. Deploy backend first (see main `DEPLOYMENT.md`)
2. Deploy website with backend URL configured
3. Test all API integrations
4. Add custom domain (optional)
5. Enable analytics (optional)
6. Add error tracking (optional)
