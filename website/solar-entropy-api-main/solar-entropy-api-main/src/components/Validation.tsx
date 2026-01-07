import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { CheckCircle, Info } from "lucide-react";

const tests = [
  {
    name: "Shannon Entropy",
    description: "Measures the average information content per byte. Higher values (max 8.0 for bytes) indicate more randomness.",
    threshold: "≥ 7.8 bits/byte",
  },
  {
    name: "Chi-Square Test",
    description: "Compares observed byte frequencies against expected uniform distribution. Low chi-square suggests good uniformity.",
    threshold: "p-value > 0.01",
  },
  {
    name: "Runs Test",
    description: "Analyzes sequences of consecutive identical bits. Too few or too many runs indicate patterns.",
    threshold: "Within expected range",
  },
  {
    name: "Autocorrelation",
    description: "Checks for correlations between bits at different positions. No correlation indicates independence.",
    threshold: "Near zero",
  },
  {
    name: "Bit-Level Entropy",
    description: "Evaluates entropy at the individual bit level for fine-grained quality assessment.",
    threshold: "≥ 0.95",
  },
];

const Validation = () => {
  return (
    <section id="validation" className="py-24 bg-muted/20 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Validation & <span className="text-gradient-ion">Quality</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Every entropy block is validated before serving. No compromises on quality.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          {/* Summary cards */}
          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            <div className="p-6 rounded-xl bg-card border border-border card-glow text-center">
              <div className="text-3xl font-bold text-primary font-mono mb-2">≥ 7.8</div>
              <p className="text-sm text-muted-foreground">Avg Shannon Entropy (bits/byte)</p>
            </div>
            <div className="p-6 rounded-xl bg-card border border-border card-glow text-center">
              <div className="text-3xl font-bold text-ion font-mono mb-2">≥ 0.75</div>
              <p className="text-sm text-muted-foreground">Quality Score (configurable)</p>
            </div>
          </div>

          {/* Test accordion */}
          <Accordion type="single" collapsible className="space-y-2">
            {tests.map((test, index) => (
              <AccordionItem
                key={index}
                value={`test-${index}`}
                className="bg-card border border-border rounded-lg px-4"
              >
                <AccordionTrigger className="hover:no-underline">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="h-4 w-4 text-primary" />
                    <span className="font-medium">{test.name}</span>
                    <span className="text-xs text-muted-foreground font-mono bg-muted px-2 py-1 rounded">
                      {test.threshold}
                    </span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground text-sm pb-4">
                  {test.description}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>

          {/* Roadmap note */}
          <div className="mt-8 p-4 rounded-lg bg-ion/5 border border-ion/20 flex items-start gap-3">
            <Info className="h-5 w-5 text-ion flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium">Roadmap: NIST SP 800-22</p>
              <p className="text-sm text-muted-foreground">
                We're working on integrating the full NIST SP 800-22 statistical test suite for comprehensive validation.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Validation;
