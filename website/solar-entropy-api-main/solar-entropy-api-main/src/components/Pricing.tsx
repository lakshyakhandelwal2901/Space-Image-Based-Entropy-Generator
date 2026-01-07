import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    description: "Perfect for getting started and experimentation.",
    features: [
      "100K bytes/day",
      "Standard validation",
      "Community support",
      "Public rate limits",
    ],
    cta: "Get Started",
    variant: "outline" as const,
    popular: false,
  },
  {
    name: "Pro",
    price: "$29",
    period: "/month",
    description: "For production workloads that need reliable entropy.",
    features: [
      "5 GB/month",
      "Priority validation",
      "Priority support",
      "Custom refresh intervals",
      "99.9% uptime SLA",
    ],
    cta: "Start Pro Trial",
    variant: "hero" as const,
    popular: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "For organizations with advanced compliance needs.",
    features: [
      "Unlimited volume",
      "Custom pool sizing",
      "Regional deployments",
      "Dedicated support",
      "Compliance reports",
      "Custom SLA",
    ],
    cta: "Contact Sales",
    variant: "outline" as const,
    popular: false,
  },
];

const Pricing = () => {
  return (
    <section id="pricing" className="py-24 bg-muted/20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Simple, Transparent <span className="text-gradient-solar">Pricing</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Start free. Scale as you grow. No hidden fees.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative p-6 rounded-xl bg-card border ${
                plan.popular ? 'border-primary' : 'border-border'
              } ${plan.popular ? 'shadow-lg shadow-primary/10' : ''}`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-primary text-primary-foreground text-xs font-medium">
                  Most Popular
                </div>
              )}
              
              <div className="text-center mb-6">
                <h3 className="text-xl font-semibold mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  {plan.period && <span className="text-muted-foreground">{plan.period}</span>}
                </div>
                <p className="text-sm text-muted-foreground mt-2">{plan.description}</p>
              </div>

              <ul className="space-y-3 mb-6">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center gap-2 text-sm">
                    <Check className={`h-4 w-4 ${plan.popular ? 'text-primary' : 'text-ion'}`} />
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <Button variant={plan.variant} className="w-full">
                {plan.cta}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Pricing;
