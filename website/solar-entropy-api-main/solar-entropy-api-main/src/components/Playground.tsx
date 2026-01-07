import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Copy, Check, Loader2, Sparkles, AlertCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { fetchRandomBytes, ApiError } from "@/lib/api";

// Convert base64 to hex
const base64ToHex = (base64: string): string => {
  const binaryString = atob(base64);
  return Array.from(binaryString)
    .map(char => char.charCodeAt(0).toString(16).padStart(2, '0'))
    .join('');
};

const Playground = () => {
  const [length, setLength] = useState(32);
  const [format, setFormat] = useState<'hex' | 'base64'>('hex');
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const { toast } = useToast();

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetchRandomBytes(length);
      // Convert from base64 to hex if needed
      const entropy = format === 'hex' ? base64ToHex(response.bytes) : response.bytes;
      setResult(entropy);
    } catch (error) {
      const message = error instanceof ApiError 
        ? error.detail 
        : error instanceof Error 
        ? error.message 
        : 'Failed to generate entropy';
      toast({
        title: "Error",
        description: message,
        variant: "destructive",
      });
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (result) {
      navigator.clipboard.writeText(result);
      setCopied(true);
      toast({
        title: "Copied!",
        description: "Entropy copied to clipboard.",
      });
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Calculate byte distribution for visualization
  const getByteDistribution = () => {
    if (!result || format !== 'hex') return [];
    const bytes: number[] = [];
    for (let i = 0; i < result.length; i += 2) {
      bytes.push(parseInt(result.slice(i, i + 2), 16));
    }
    const distribution = new Array(16).fill(0);
    bytes.forEach(b => {
      const bucket = Math.floor(b / 16);
      distribution[bucket]++;
    });
    const max = Math.max(...distribution);
    return distribution.map(v => (v / max) * 100);
  };

  const distribution = getByteDistribution();

  return (
    <section id="playground" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Try the <span className="text-gradient-solar">Playground</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Generate random bytes instantly. See entropy in action.
          </p>
        </div>

        <div className="max-w-2xl mx-auto">
          <div className="p-6 rounded-xl bg-card border border-border card-glow">
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="flex-1">
                <label className="text-sm text-muted-foreground mb-2 block">Length (bytes)</label>
                <Input
                  type="number"
                  value={length}
                  onChange={(e) => setLength(Math.min(128, Math.max(1, parseInt(e.target.value) || 1)))}
                  min={1}
                  max={128}
                  className="bg-muted/50"
                />
              </div>
              <div>
                <label className="text-sm text-muted-foreground mb-2 block">Format</label>
                <Tabs value={format} onValueChange={(v) => setFormat(v as 'hex' | 'base64')}>
                  <TabsList className="bg-muted/50 border border-border">
                    <TabsTrigger value="hex">Hex</TabsTrigger>
                    <TabsTrigger value="base64">Base64</TabsTrigger>
                  </TabsList>
                </Tabs>
              </div>
              <div className="flex items-end">
                <Button onClick={handleGenerate} disabled={loading} variant="hero" className="w-full sm:w-auto">
                  {loading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Sparkles className="h-4 w-4" />
                  )}
                  Generate
                </Button>
              </div>
            </div>

            {/* Result */}
            {result && (
              <div className="space-y-4 animate-fade-in">
                <div className="relative">
                  <div className="p-4 rounded-lg bg-muted/50 border border-border font-mono text-xs break-all max-h-32 overflow-y-auto">
                    {result}
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="absolute top-2 right-2 h-8 w-8"
                    onClick={copyToClipboard}
                  >
                    {copied ? (
                      <Check className="h-4 w-4 text-primary" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}
                  </Button>
                </div>

                {/* Byte distribution histogram */}
                {distribution.length > 0 && (
                  <div>
                    <p className="text-xs text-muted-foreground mb-2">Byte Distribution</p>
                    <div className="flex items-end gap-1 h-12">
                      {distribution.map((height, i) => (
                        <div
                          key={i}
                          className="flex-1 bg-ion/60 rounded-t transition-all duration-300"
                          style={{ height: `${Math.max(4, height)}%` }}
                        />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Disclaimer */}
            <p className="text-xs text-muted-foreground mt-6 text-center">
              ⚠️ Playground responses are rate-limited and simulated for demo purposes. 
              Always fetch via your own backend for production secrets.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Playground;
