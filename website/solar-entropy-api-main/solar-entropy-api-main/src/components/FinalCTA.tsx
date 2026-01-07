import { Button } from "@/components/ui/button";
import { ArrowRight, BookOpen } from "lucide-react";
import { Link } from "react-router-dom";

const FinalCTA = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-3xl" />
      
      <div className="container mx-auto px-4 relative">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Ready to harness{' '}
            <span className="text-gradient-solar">true entropy</span>?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Join developers and security teams who trust space-derived randomness for their most critical systems.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button variant="hero" size="xl">
              Get API Key
              <ArrowRight className="h-5 w-5" />
            </Button>
            <Button variant="heroOutline" size="xl" asChild>
              <Link to="/docs">
                <BookOpen className="h-5 w-5" />
                Explore Docs
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FinalCTA;
