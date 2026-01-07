import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "What makes this \"true\" randomness?",
    answer: "We derive entropy from non-deterministic natural phenomena — specifically, live solar imagery from NASA's SDO satellite. The chaotic dynamics of the sun's plasma, magnetic fields, and coronal activity are fundamentally unpredictable, then distilled via modern cryptographic hashing and validated statistically.",
  },
  {
    question: "Is this a TRNG or DRBG?",
    answer: "It's a hybrid pipeline: real-world entropy is harvested from space images and processed through cryptographic functions (BLAKE3 + SHA-256). The outputs are not deterministic repeats — each block is unique and derived from fresh solar observations.",
  },
  {
    question: "How often is entropy refreshed?",
    answer: "Configurable, but typically every 2 minutes. We fetch new solar imagery, extract noise, and distill fresh entropy blocks. A Redis-backed pool ensures low-latency reads even during refresh cycles.",
  },
  {
    question: "Can I verify quality?",
    answer: "Yes! Our /api/v1/stats endpoint exposes recent validation metrics including Shannon entropy, chi-square test results, runs analysis, and overall quality scores. Our methods are fully documented.",
  },
  {
    question: "Is it suitable for cryptographic keys?",
    answer: "Yes, with proper operational hygiene. Always fetch entropy via your backend over TLS — never expose API keys or secrets client-side. Combine with your system's entropy pool for defense in depth.",
  },
  {
    question: "What about NIST test suites?",
    answer: "Core statistical tests ship today. Full NIST SP 800-22 integration is on our roadmap — we're working to provide comprehensive validation for the most demanding compliance requirements.",
  },
];

const FAQ = () => {
  return (
    <section id="faq" className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Frequently Asked <span className="text-gradient-ion">Questions</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Everything you need to know about our entropy service.
          </p>
        </div>

        <div className="max-w-3xl mx-auto">
          <Accordion type="single" collapsible className="space-y-2">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`faq-${index}`}
                className="bg-card border border-border rounded-lg px-6"
              >
                <AccordionTrigger className="hover:no-underline text-left">
                  <span className="font-medium">{faq.question}</span>
                </AccordionTrigger>
                <AccordionContent className="text-muted-foreground leading-relaxed pb-4">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </div>
    </section>
  );
};

export default FAQ;
