import { Download, Wand2, Hash, CheckCircle, Server, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: Download,
    title: "Ingest",
    description: "Fetch latest multi-wavelength solar images from NASA/SDO",
    color: "text-ion",
    bgColor: "bg-ion/10",
  },
  {
    icon: Wand2,
    title: "Transform",
    description: "Apply noise extraction: Laplacian, gradients, FFT, sampling, RGB channels",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: Hash,
    title: "Distill",
    description: "Multi-round hashing (BLAKE3 + SHA-256) with timestamp chaining",
    color: "text-ion",
    bgColor: "bg-ion/10",
  },
  {
    icon: CheckCircle,
    title: "Validate",
    description: "Shannon entropy, chi-square, runs, autocorrelation, bit-entropy tests",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: Server,
    title: "Serve",
    description: "Store in Redis-backed pool with TTL; serve via REST with health/stats",
    color: "text-ion",
    bgColor: "bg-ion/10",
  },
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-24 bg-muted/20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            How It <span className="text-gradient-solar">Works</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            A five-stage pipeline that transforms solar chaos into cryptographic-quality entropy.
          </p>
        </div>

        {/* Pipeline visualization */}
        <div className="max-w-5xl mx-auto">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-4">
            {steps.map((step, index) => (
              <div key={index} className="flex items-center">
                <div className="group flex flex-col items-center text-center p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition-all duration-300 w-48">
                  <div className={`flex h-14 w-14 items-center justify-center rounded-xl ${step.bgColor} mb-4 group-hover:scale-110 transition-transform`}>
                    <step.icon className={`h-7 w-7 ${step.color}`} />
                  </div>
                  <h3 className="font-semibold mb-2">{step.title}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">
                    {step.description}
                  </p>
                </div>
                {index < steps.length - 1 && (
                  <ArrowRight className="hidden lg:block h-5 w-5 text-muted-foreground mx-2 flex-shrink-0" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Technical note */}
        <div className="mt-12 max-w-2xl mx-auto">
          <div className="p-4 rounded-lg bg-card border border-border text-center">
            <p className="text-sm text-muted-foreground">
              <span className="text-primary font-medium">Backed by</span>{' '}
              multi-stage image processing, modern hashing (BLAKE3 + SHA-256), and continuous statistical validation.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
