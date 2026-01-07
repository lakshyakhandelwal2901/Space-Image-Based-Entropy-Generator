import Header from "@/components/Header";
import Hero from "@/components/Hero";
import WhyItMatters from "@/components/WhyItMatters";
import HowItWorks from "@/components/HowItWorks";
import Features from "@/components/Features";
import APISection from "@/components/APISection";
import Playground from "@/components/Playground";
import Validation from "@/components/Validation";
import UseCases from "@/components/UseCases";
import Pricing from "@/components/Pricing";
import FAQ from "@/components/FAQ";
import FinalCTA from "@/components/FinalCTA";
import Footer from "@/components/Footer";

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        <Hero />
        <WhyItMatters />
        <HowItWorks />
        <Features />
        <APISection />
        <Playground />
        <Validation />
        <UseCases />
        <Pricing />
        <FAQ />
        <FinalCTA />
      </main>
      <Footer />
    </div>
  );
};

export default Index;
