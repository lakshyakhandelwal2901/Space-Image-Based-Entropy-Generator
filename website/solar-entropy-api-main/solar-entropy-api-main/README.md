# Entropy.Space Marketing Website

Beautiful, responsive marketing site and API documentation for the Space-Image Based Entropy Generator (True Randomness as a Service).

## 🚀 Features

- **Modern React + TypeScript stack** with Vite
- **Interactive Playground** to generate and visualize random bytes
- **Live Statistics** from backend API (Shannon entropy, pool size, refresh time)
- **Comprehensive API Docs** with code examples (curl, Python, JavaScript)
- **Responsive Design** with Tailwind CSS and shadcn-ui components
- **Developer-Friendly** with proper error handling and loading states

## 📋 Prerequisites

- Node.js 16+ (install via [nvm](https://github.com/nvm-sh/nvm))
- npm or yarn
- Backend API running on `http://localhost:8000` (or configured via env vars)

## 🛠️ Setup

### 1. Clone and Install

```bash
cd website/solar-entropy-api-main/solar-entropy-api-main
npm install
```

### 2. Configure Environment

Create `.env.local` (copy from `.env.example`):

```bash
# Backend API base URL
VITE_API_BASE_URL=http://localhost:8000/api/v1

# Optional: stats refresh interval (ms)
VITE_STATS_POLL_INTERVAL=10000
```

### 3. Run Locally

```bash
npm run dev
```

Visit `http://localhost:8080` in your browser.

## 📦 Build for Production

```bash
npm run build
```

Output will be in `dist/`. Deploy to:
- **Vercel**: Push to GitHub and auto-deploy
- **Netlify**: Connect repo and build with `npm run build` / `dist`
- **Render**: Use static site hosting with same build settings

## 🌐 Production Deployment

When deploying to production, update `.env` with your actual backend URL:

```bash
VITE_API_BASE_URL=https://your-service.onrender.com/api/v1
```

Then rebuild and redeploy.

## 📁 Project Structure

```
src/
├── components/          # Reusable React components
│   ├── Hero.tsx        # Hero section with live stats
│   ├── Playground.tsx  # Interactive entropy generator
│   ├── APISection.tsx  # API overview & code examples
│   ├── LiveStats.tsx   # Live stats fetcher
│   └── ...
├── pages/              # Full page components
│   ├── Index.tsx       # Marketing homepage
│   └── Docs.tsx        # API documentation
├── lib/
│   └── api.ts          # API utilities & fetch wrappers
├── App.tsx             # Router setup
└── main.tsx            # Entry point
```

## 🔌 API Integration

The website connects to these backend endpoints:

- **`GET /health`** - Service health check
- **`GET /stats`** - Pool statistics (live entropy data)
- **`GET /random/{n}`** - Fetch n random bytes (1-10,240 bytes)

All requests are handled via the utility functions in `src/lib/api.ts` with proper error handling and TypeScript types.

## 🎨 Design System

- **Colors**: Space Black, Solar Yellow, Ion Blue, Quiet Grey
- **Components**: shadcn-ui (Button, Input, Tabs, Accordion, etc.)
- **Styling**: Tailwind CSS
- **Fonts**: Inter (body), JetBrains Mono (code)

## 🧪 Testing Playground Locally

1. Start the backend: `cd ../.. && python -m app.main`
2. Start the website: `npm run dev`
3. Navigate to http://localhost:8080 → Playground
4. Click "Generate" to fetch real entropy from your backend

## 📝 Customization

### Change API Endpoint

Edit `VITE_API_BASE_URL` in `.env.local`:

```bash
VITE_API_BASE_URL=https://custom-domain.com/api/v1
```

### Update Copy/Content

Edit components in `src/components/` and `src/pages/`

### Modify Colors/Styling

Tailwind config is in `tailwind.config.ts`. Use custom color names like `primary`, `ion`, `solar`, etc.

## 🚀 Next Steps

1. **Wire to your backend**: Update `.env.local` with backend URL
2. **Deploy static site**: Use Vercel, Netlify, or Render
3. **Add authentication** (optional): Add /dashboard, /login pages
4. **Add status page** (optional): Show uptime metrics from backend
5. **Analytics** (optional): Integrate Plausible, Fathom, or Vercel Analytics

## 📦 Dependencies

- **React 18** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn-ui** - Component library
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching (optional, for future use)
- **Recharts** - Charts/graphs (optional, for future analytics)

## 📄 License

Same as parent project (Space-Image Based Entropy Generator)
