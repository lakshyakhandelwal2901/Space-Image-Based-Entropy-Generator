import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Copy, Check } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { getApiBaseUrl } from "@/lib/api";

const API_BASE = getApiBaseUrl();

const codeExamples = {
  curl: `curl -s "${API_BASE}/random/32" | jq`,
  python: `import requests
import json

API_BASE = "${API_BASE}"

response = requests.get(f"{API_BASE}/random/32")
data = response.json()
print(f"Random bytes: {data['bytes']}")
print(f"Length: {data['length']}")`,
  javascript: `const API_BASE = "${API_BASE}";

async function getRandomBytes(n) {
  const response = await fetch(\`\${API_BASE}/random/\${n}\`);
  return response.json();
}

// Get 32 random bytes
const data = await getRandomBytes(32);
console.log("Random bytes:", data.bytes);
console.log("Length:", data.length);`,
};

const responseExample = `{
  "bytes": "rF5wMvN2aK9pQw8xB1jL6c3d7tY4hZ5v",
  "length": 32,
  "format": "base64"
}`;

const APISection = () => {
  const [copied, setCopied] = useState<string | null>(null);
  const { toast } = useToast();

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    toast({
      title: "Copied to clipboard",
      description: "Code snippet copied successfully.",
    });
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <section id="api" className="py-24 bg-muted/20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            API at a <span className="text-gradient-solar">Glance</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Three simple endpoints. Get randomness in seconds.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          {/* Endpoints */}
          <div className="grid md:grid-cols-3 gap-4 mb-8">
            <div className="p-4 rounded-lg bg-card border border-border">
              <code className="text-sm text-ion font-mono">GET</code>
              <p className="font-mono text-sm mt-1">/health</p>
              <p className="text-xs text-muted-foreground mt-2">Service health status</p>
            </div>
            <div className="p-4 rounded-lg bg-card border border-border">
              <code className="text-sm text-ion font-mono">GET</code>
              <p className="font-mono text-sm mt-1">/stats</p>
              <p className="text-xs text-muted-foreground mt-2">Pool & validation stats</p>
            </div>
            <div className="p-4 rounded-lg bg-card border border-border">
              <code className="text-sm text-primary font-mono">GET</code>
              <p className="font-mono text-sm mt-1">/random/{'{n}'}</p>
              <p className="text-xs text-muted-foreground mt-2">n bytes of entropy</p>
            </div>
          </div>

          {/* Code examples */}
          <div className="grid lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Request</h3>
              <Tabs defaultValue="curl" className="w-full">
                <TabsList className="bg-muted/50 border border-border">
                  <TabsTrigger value="curl" className="text-xs">cURL</TabsTrigger>
                  <TabsTrigger value="python" className="text-xs">Python</TabsTrigger>
                  <TabsTrigger value="javascript" className="text-xs">JavaScript</TabsTrigger>
                </TabsList>
                {Object.entries(codeExamples).map(([key, code]) => (
                  <TabsContent key={key} value={key} className="mt-4">
                    <div className="relative">
                      <pre className="code-block text-xs overflow-x-auto">
                        <code>{code}</code>
                      </pre>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="absolute top-2 right-2 h-8 w-8"
                        onClick={() => copyToClipboard(code, key)}
                      >
                        {copied === key ? (
                          <Check className="h-4 w-4 text-primary" />
                        ) : (
                          <Copy className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </TabsContent>
                ))}
              </Tabs>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Response</h3>
              <div className="relative">
                <pre className="code-block text-xs overflow-x-auto h-full">
                  <code className="text-primary/80">{responseExample}</code>
                </pre>
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute top-2 right-2 h-8 w-8"
                  onClick={() => copyToClipboard(responseExample, 'response')}
                >
                  {copied === 'response' ? (
                    <Check className="h-4 w-4 text-primary" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default APISection;
