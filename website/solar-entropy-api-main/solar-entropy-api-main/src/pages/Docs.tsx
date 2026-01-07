import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sparkles, ArrowLeft, Copy, Check, Terminal, Zap, Shield, AlertTriangle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { getApiBaseUrl } from "@/lib/api";

const API_BASE = getApiBaseUrl();

const codeExamples = {
  curl: `# Fetch 32 random bytes
curl -X GET "${API_BASE}/random/32" \\
  -H "Accept: application/json"`,
  python: `import requests

API_BASE = "${API_BASE}"

def get_random_bytes(n: int) -> dict:
    response = requests.get(f"{API_BASE}/random/{n}")
    return response.json()

# Get 32 random bytes
data = get_random_bytes(32)
print(f"Entropy: {data['bytes']}")
print(f"Length: {data['length']}")`,
  javascript: `const API_BASE = "${API_BASE}";

async function getRandomBytes(n) {
  const response = await fetch(\`\${API_BASE}/random/\${n}\`);
  return response.json();
}

// Get 32 random bytes
const data = await getRandomBytes(32);
console.log("Entropy:", data.bytes);
console.log("Length:", data.length);`,
};

const Docs = () => {
  const [copied, setCopied] = useState<string | null>(null);
  const { toast } = useToast();

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    toast({ title: "Copied to clipboard" });
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link to="/" className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
              <Sparkles className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="text-lg font-semibold">Entropy.Space</span>
          </Link>
          <Button variant="ghost" size="sm" asChild>
            <Link to="/">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Link>
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-4 pt-24 pb-16 max-w-4xl">
        {/* Title */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold mb-4">Documentation</h1>
          <p className="text-xl text-muted-foreground">
            Everything you need to integrate space-derived entropy into your applications.
          </p>
        </div>

        {/* Quickstart */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <Zap className="h-5 w-5 text-primary" />
            </div>
            <h2 className="text-2xl font-bold">Quickstart</h2>
          </div>

          <div className="space-y-4 text-muted-foreground mb-6">
            <p>Get started with the Entropy.Space API in under a minute:</p>
            <ol className="list-decimal list-inside space-y-2">
              <li><strong className="text-foreground">Get an API key</strong> from your dashboard</li>
              <li><strong className="text-foreground">Make a request</strong> to fetch random bytes</li>
              <li><strong className="text-foreground">Use the entropy</strong> in your application</li>
            </ol>
          </div>

          <Tabs defaultValue="curl" className="w-full">
            <TabsList className="bg-muted/50 border border-border">
              <TabsTrigger value="curl">cURL</TabsTrigger>
              <TabsTrigger value="python">Python</TabsTrigger>
              <TabsTrigger value="javascript">JavaScript</TabsTrigger>
            </TabsList>
            {Object.entries(codeExamples).map(([key, code]) => (
              <TabsContent key={key} value={key} className="mt-4">
                <div className="relative">
                  <pre className="code-block text-sm overflow-x-auto">
                    <code>{code}</code>
                  </pre>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-2 right-2 h-8 w-8"
                    onClick={() => copyToClipboard(code, key)}
                  >
                    {copied === key ? <Check className="h-4 w-4 text-primary" /> : <Copy className="h-4 w-4" />}
                  </Button>
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </section>

        {/* Environments */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-ion/10">
              <Terminal className="h-5 w-5 text-ion" />
            </div>
            <h2 className="text-2xl font-bold">Environments</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 pr-4 font-medium">Environment</th>
                  <th className="text-left py-3 font-medium">Base URL</th>
                </tr>
              </thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border">
                  <td className="py-3 pr-4">Production</td>
                  <td className="py-3 font-mono text-ion">https://api.entropy.space/v1</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-3 pr-4">Sandbox</td>
                  <td className="py-3 font-mono text-muted-foreground">https://sandbox.entropy.space/v1</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Endpoints */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-6">Endpoints</h2>

          <div className="space-y-6">
            {/* Health */}
            <div className="p-6 rounded-xl bg-card border border-border">
              <div className="flex items-center gap-3 mb-4">
                <span className="px-2 py-1 rounded text-xs font-mono bg-ion/20 text-ion">GET</span>
                <code className="font-mono">/health</code>
              </div>
              <p className="text-muted-foreground text-sm mb-4">Check service health and uptime status.</p>
              <div className="code-block text-xs">
                <code>{`{
  "status": "healthy",
  "service": "space-entropy-generator",
  "version": "0.1.0",
  "redis": { "connected": true, "uptime": 99.99 }
}`}</code>
              </div>
            </div>

            {/* Stats */}
            <div className="p-6 rounded-xl bg-card border border-border">
              <div className="flex items-center gap-3 mb-4">
                <span className="px-2 py-1 rounded text-xs font-mono bg-ion/20 text-ion">GET</span>
                <code className="font-mono">/stats</code>
              </div>
              <p className="text-muted-foreground text-sm mb-4">Get pool and validation statistics.</p>
              <div className="code-block text-xs">
                <code>{`{
  "pool_bytes": 1048576,
  "available_bytes": 1048576,
  "entropy_blocks": 256,
  "avg_shannon": 7.92,
  "avg_quality_score": 0.94,
  "last_validation": "2025-01-07T12:45:03Z"
}`}</code>
              </div>
            </div>

            {/* Random */}
            <div className="p-6 rounded-xl bg-card border border-border">
              <div className="flex items-center gap-3 mb-4">
                <span className="px-2 py-1 rounded text-xs font-mono bg-primary/20 text-primary">GET</span>
                <code className="font-mono">/random/{'{n}'}</code>
              </div>
              <p className="text-muted-foreground text-sm mb-4">Fetch n bytes of high-entropy randomness (max 10240 per request).</p>
              <div className="code-block text-xs">
                <code>{`{
  "bytes": "rF5wMvN2aK9pQw8xB1jL6c3d7tY4hZ5v...",
  "length": 32,
  "format": "base64"
}`}</code>
              </div>
            </div>
          </div>
        </section>

        {/* Rate Limits */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-6">Limits & Best Practices</h2>

          <div className="space-y-4">
            <div className="p-4 rounded-lg bg-card border border-border">
              <h3 className="font-semibold mb-2">Rate Limits</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• <strong>Free tier:</strong> Up to 100 requests/minute</li>
                <li>• <strong>Max bytes per request:</strong> 10,240 bytes</li>
                <li>• <strong>Rate limit window:</strong> 1 minute rolling</li>
              </ul>
            </div>

            <div className="p-4 rounded-lg bg-card border border-border">
              <h3 className="font-semibold mb-2">Best Practices</h3>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• Request only the bytes you need</li>
                <li>• Cache entropy locally when appropriate</li>
                <li>• Mix with system entropy for defense in depth</li>
                <li>• Never log or store raw entropy values</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Security */}
        <section className="mb-16">
          <div className="flex items-center gap-3 mb-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <Shield className="h-5 w-5 text-primary" />
            </div>
            <h2 className="text-2xl font-bold">Security Notes</h2>
          </div>

          <div className="p-4 rounded-lg bg-destructive/5 border border-destructive/20 flex items-start gap-3 mb-6">
            <AlertTriangle className="h-5 w-5 text-destructive flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium">No Authentication Required</p>
              <p className="text-sm text-muted-foreground">
                Current version operates without API key authentication. Use responsibly and monitor your request rates.
              </p>
            </div>
          </div>

          <ul className="space-y-2 text-muted-foreground text-sm">
            <li>• Service is served over HTTP (add TLS via reverse proxy in production)</li>
            <li>• All responses are JSON</li>
            <li>• Entropy is provided in base64 format (decode as needed)</li>
            <li>• Mix with system entropy for defense in depth when possible</li>
          </ul>
        </section>

        {/* Error Codes */}
        <section>
          <h2 className="text-2xl font-bold mb-6">Error Codes</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-3 pr-4 font-medium">Code</th>
                  <th className="text-left py-3 pr-4 font-medium">Status</th>
                  <th className="text-left py-3 font-medium">Description</th>
                </tr>
              </thead>
              <tbody className="text-muted-foreground">
                <tr className="border-b border-border">
                  <td className="py-3 pr-4 font-mono">400</td>
                  <td className="py-3 pr-4">Bad Request</td>
                  <td className="py-3">Invalid parameters (e.g., n out of range)</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-3 pr-4 font-mono">401</td>
                  <td className="py-3 pr-4">Unauthorized</td>
                  <td className="py-3">Missing or invalid API key</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-3 pr-4 font-mono">429</td>
                  <td className="py-3 pr-4">Rate Limited</td>
                  <td className="py-3">Too many requests, retry after delay</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-3 pr-4 font-mono">503</td>
                  <td className="py-3 pr-4">Service Unavailable</td>
                  <td className="py-3">Pool depleted or service maintenance</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} Entropy.Space. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

export default Docs;
