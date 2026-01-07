import { AlertTriangle, Zap, Lock } from "lucide-react";

const WhyItMatters = () => {
  return (
    <section className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3 mb-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
              <AlertTriangle className="h-5 w-5 text-primary" />
            </div>
            <h2 className="text-3xl md:text-4xl font-bold">
              PRNGs Are Fast. <span className="text-muted-foreground">Entropy Is Hard.</span>
            </h2>
          </div>
          
          <p className="text-lg text-muted-foreground mb-12 leading-relaxed">
            Many workloads are fine with PRNGs — until they're not. True entropy matters for 
            cryptographic keys, lotteries, secure tokens, and unpredictability-critical systems. 
            We harvest non-deterministic structure from real-world space images to bootstrap robust randomness.
          </p>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="group p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition-all duration-300 card-glow">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-destructive/10 mb-4">
                <Zap className="h-6 w-6 text-destructive" />
              </div>
              <h3 className="text-lg font-semibold mb-2">The Problem with PRNGs</h3>
              <p className="text-muted-foreground text-sm">
                Pseudo-random number generators are deterministic — if you know the seed and algorithm, 
                you can predict every output. For security-critical applications, this is a fatal flaw.
              </p>
            </div>

            <div className="group p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition-all duration-300 card-glow">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 mb-4">
                <Lock className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">True Physical Entropy</h3>
              <p className="text-muted-foreground text-sm">
                We tap into the chaotic, non-deterministic nature of solar phenomena — plasma dynamics, 
                magnetic field fluctuations, and coronal activity that no algorithm can predict.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default WhyItMatters;
