# Website Prompt — Space-Image Based Entropy Generator (True Randomness as a Service)

This document is a turnkey prompt and content brief for generating a polished marketing website and lightweight docs for the Space-Image Based Entropy Generator (aka “True Randomness as a Service”). It is written for a designer, frontend engineer, or a website-generating AI. Use it to create a fast, accessible, credible site that converts developers and security teams.

## Who This Site Is For
- Developers, SREs, and security engineers who need high-quality random bytes
- Researchers and data scientists evaluating non-deterministic RNG sources
- Web3, cryptography, gaming, and simulation teams

## Core Positioning
- Headline: “True Randomness. From Space.”
- Subheading: “We transform live solar observations into high-entropy randomness — validated, pooled, and delivered via a simple API you can trust.”
- One-line proof: “Backed by multi-stage image processing, modern hashing (BLAKE3 + SHA-256), and continuous statistical validation.”

## Visual Direction
- Hero: Dynamic solar imagery (e.g., SDO wavelengths) with a subtle noise/glow overlay.
- Motif: Space-grade, scientific, clean. Avoid gimmicks. Convey precision and reliability.
- Motion: Very light, physics-informed micro-animations. Prefer performance and restraint.

## Brand Voice & Tone
- Confident, transparent, technically precise.
- Factual over flashy; briefly explain trade-offs; link to methods when claims are made.
- Friendly to newcomers; inspires trust for experts.

## Page Structure
Build a single-page site with clear anchors, plus a minimal “Docs” page variant using the same components. Sections below include suggested copy and UI elements.

### 1) Hero
- H1: “True Randomness. From Space.”
- Subtext: “We extract unpredictability from live solar imagery to produce high-entropy random bytes. Delivered via HTTPS. Validated continuously.”
- Primary CTA: “Get API Key”
- Secondary CTA: “Try the Playground” (opens an in-page panel to fetch bytes live)
- Trust badges: “Developer-first API”, “Continuously Validated”, “Open Methods”
- Quick stat strip (live if possible): Shannon entropy (avg), pool size (bytes), last refresh (time)

### 2) Why It Matters
- Headline: “PRNGs Are Fast. Entropy Is Hard.”
- Copy (short): Many workloads are fine with PRNGs — until they’re not. True entropy matters for cryptographic keys, lotteries, secure tokens, and unpredictability-critical systems. We harvest non-deterministic structure from real-world space images to bootstrap robust randomness.

### 3) How It Works (High-Level)
- 1. Ingest: Fetch latest multi-wavelength solar images (e.g., NASA/SDO).
- 2. Transform: Apply noise extraction (Laplacian, gradients, FFT domains, sampling/patching, RGB channels).
- 3. Distill: Mix and compress through multi-round hashing (BLAKE3 + SHA-256) with timestamp/chaining and XOF expansion.
- 4. Validate: Run Shannon entropy, chi-square, runs, autocorrelation, and bit-entropy tests; score quality.
- 5. Pool & Serve: Store blocks in a Redis-backed pool with TTL; serve via REST with health/stats.

Add a schematic diagram: five boxes with arrows. Keep labels concise.

### 4) Key Features
- High-entropy pipeline: Multi-technique image noise extraction + modern hashing.
- Continuous validation: Five statistical tests + quality scoring; thresholds configurable.
- Simple API: Fetch random bytes in hex/base64; query stats and health.
- Freshness by design: New entropy from images at a configurable cadence (e.g., every 2 minutes).
- Scalable pool: Buffer and serve at low latency; configurable TTL.
- Optional cloud storage: Pluggable backend components (e.g., Azure Blob) as needed.

### 5) API at a Glance
Show a compact code panel with tabs for curl, Python, and JavaScript.

Example endpoints:
- GET /api/v1/health — service health
- GET /api/v1/stats — pool and validation stats
- GET /api/v1/random/{n} — n bytes of randomness (n up to a reasonable limit)

Example curl:
```bash
curl -s https://{{SERVICE_URL}}/api/v1/random/32 | jq
```

Example response (JSON):
```json
{
	"format": "hex",
	"bytes": "f1c93e…a7",
	"length": 32,
	"entropy_score": 0.94,
	"timestamp": "2025-01-13T12:45:03Z"
}
```

### 6) Validation & Quality
- Summary card: “Avg Shannon ≥ 7.8”, “Quality Score ≥ 0.75 (configurable)”
- Accordion detail: briefly describe each test and its role.
- Note: We aim to integrate more test batteries (e.g., NIST SP 800-22) — roadmap callout.

Where useful, you may include the entropy equation with KaTeX: $H(X) = -\sum p(x) \log_2 p(x)$.

### 7) Playground
- Small panel with: desired length (bytes), format (hex/base64), and a “Generate” button.
- Results area: monospace output, copy-to-clipboard, and a tiny histogram visualization of byte distribution for the sample.
- Disclaimer: Playground responses are rate-limited and not suitable for key generation by themselves; always fetch via your own backend for secrets.

### 8) Use Cases
- Cryptographic key material bootstrapping
- Lotteries, raffles, unbiased selections
- Gaming, simulations, Monte Carlo
- Research and reproducibility (store hashes, not secrets)

### 9) Pricing (Placeholder — editable)
- Free: 100K bytes/day, community support
- Pro: 5 GB/month, priority support, custom intervals
- Enterprise: Custom pool sizing, regional deployments, compliance

### 10) FAQ
- What makes this “true” randomness? We derive entropy from non-deterministic natural phenomena (space imagery), then distill via modern hashing and validate statistically.
- Is this a TRNG or DRBG? It’s a hybrid pipeline: real-world entropy harvested and processed through cryptographic functions; outputs are not deterministic repeats.
- How often is entropy refreshed? Configurable (e.g., every 2 minutes). Pooling ensures low-latency reads.
- Can I verify quality? Yes — stats endpoint exposes recent validation metrics; methods are documented.
- Is it suitable for cryptographic keys? Yes, with proper operational hygiene. Fetch via backend over TLS; never expose secrets client-side.
- What about NIST test suites? Core tests ship today; NIST 800-22 is on the roadmap.

### 11) Final CTA
- Primary: “Get API Key”
- Secondary: “Explore Docs”

## Docs Page (Lightweight Variant)
Use same header/footer and system. Include:
- Quickstart (curl, Python, JS)
- Environments and base URLs
- Endpoints: health, stats, random/{n}
- Limits and best practices
- Security notes and validation methods
- Error codes and troubleshooting

## Design System
- Colors:
	- Space Black: #0B0F14
	- Solar Yellow: #F2C14E
	- Ion Blue: #3A86FF
	- Quiet Grey: #8C99A6
	- Off-White: #F6F7F9
- Type:
	- Headlines: Inter or Sora, semi-bold; body: Inter regular.
	- Numbers and code: JetBrains Mono or Fira Code.
- Components: CTA Button, Stat Pill, Code Block, Accordion, Card, Tabs, Toast
- Icons: Shield (security), Waveform (signal), Diagram (pipeline), Rocket (deploy)
- Spacing: 4/8/12/16/24/32 scale; touch targets ≥ 44px.

## Interactions & Motion
- On hero load: subtle solar flare shimmer (GPU-accelerated, low CPU usage).
- On fetch: show a brief “distill” animation — dots converge into a block.
- On copy: toast “Copied to clipboard”.
- Respect `prefers-reduced-motion`.

## Accessibility
- Contrast AA+; keyboard focus visible; skip-to-content link; semantic landmarks.
- All imagery needs descriptive alt text; do not rely on color alone.
- Validate with automated checks and manual keyboard-only pass.

## Performance Budget
- LCP ≤ 2.5s on 4G; TTI ≤ 3s; CLS ≤ 0.1.
- Avoid large JS frameworks unless necessary; prioritize server-rendered HTML or lightweight hydration.
- Lazy-load non-critical images; compress hero media; prefetch key routes.

## SEO & Metadata
- Title: “True Randomness from Space — Entropy as a Service”
- Description: “High-entropy randomness distilled from live solar imagery. Validated continuously. Simple API for developers and security teams.”
- Open Graph image: Solar hero with tagline; 1200×630.
- Structured Data (JSON-LD, Organization + Product):
```html
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "SoftwareApplication",
	"name": "Space-Image Based Entropy Generator",
	"applicationCategory": "DeveloperApplication",
	"operatingSystem": "Any",
	"offers": {"@type": "Offer", "price": "0"},
	"url": "https://{{SERVICE_URL}}/",
	"description": "High-entropy randomness distilled from live solar imagery; delivered via API.",
	"softwareHelp": {"@type": "CreativeWork", "url": "https://{{SERVICE_URL}}/docs"}
}
</script>
```

## Analytics & Consent
- Use privacy-friendly analytics by default; request consent for any additional trackers.
- Provide a cookie banner and a privacy page; no dark patterns.

## Legal
- Links in footer: Privacy, Terms, Security, Status
- Security page: responsible disclosure policy and contact.

## Deployment Notes
- Target: static hosting + API backend (separate). Use a CDN.
- Base URL placeholder: `{{SERVICE_URL}}`.
- Provide a 404 page mirroring the brand style.

## Content Checklist (Copy-Ready)
- Hero H1: True Randomness. From Space.
- Hero Sub: We transform live solar observations into high-entropy randomness — validated and delivered by API.
- CTA Primary: Get API Key
- CTA Secondary: Try the Playground
- Feature bullets (5):
	- Space-derived entropy
	- Rigorous validation
	- Simple REST API
	- Low-latency pool
	- Configurable cadence
- “How it works” steps (5): Ingest → Transform → Distill → Validate → Serve
- API endpoints: /api/v1/health, /api/v1/stats, /api/v1/random/{n}
- Footnote: “Do not expose sensitive randomness directly to client apps.”

## Optional Components
- Status page widget: uptime and incidents feed.
- Changelog: highlight pipeline updates, validation changes, and performance improvements.
- Customer logos or testimonials (if/when available).

---

Implementation tip: Start with semantic HTML and minimal CSS variables; ship progressively enhanced JS for the Playground. Keep it fast, accessible, and honest.

