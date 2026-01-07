import { Sparkles, Shield, Code2, Clock, Database, Cloud } from "lucide-react";

const features = [
  {
    icon: Sparkles,
    title: "High-Entropy Pipeline",
    description: "Multi-technique image noise extraction combined with modern cryptographic hashing for maximum unpredictability.",
  },
  {
    icon: Shield,
    title: "Continuous Validation",
    description: "Five statistical tests + quality scoring ensure every byte meets rigorous entropy thresholds.",
  },
  {
    icon: Code2,
    title: "Simple REST API",
    description: "Fetch random bytes in hex or base64 format. Query stats and health with a single request.",
  },
  {
    icon: Clock,
    title: "Freshness by Design",
    description: "New entropy harvested from images at configurable intervals — typically every 2 minutes.",
  },
  {
    icon: Database,
    title: "Scalable Pool",
    description: "Buffer and serve at low latency with configurable TTL for optimal performance.",
  },
  {
    icon: Cloud,
    title: "Flexible Backend",
    description: "Pluggable storage components including Redis and optional Azure Blob integration.",
  },
];

const Features = () => {
  return (
    <section id="features" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Key <span className="text-gradient-ion">Features</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Everything you need for production-grade true randomness.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <div
              key={index}
              className="group p-6 rounded-xl bg-card border border-border hover:border-ion/50 transition-all duration-300 card-glow"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-ion/10 mb-4 group-hover:bg-ion/20 transition-colors">
                <feature.icon className="h-6 w-6 text-ion" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
