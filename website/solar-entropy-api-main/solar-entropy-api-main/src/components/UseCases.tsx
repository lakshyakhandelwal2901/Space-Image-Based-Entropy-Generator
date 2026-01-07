import { Key, Dice6, Gamepad2, FlaskConical } from "lucide-react";

const useCases = [
  {
    icon: Key,
    title: "Cryptographic Key Material",
    description: "Bootstrap high-entropy keys for encryption, signing, and secure token generation.",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: Dice6,
    title: "Lotteries & Raffles",
    description: "Provably fair random selection for contests, giveaways, and unbiased decision-making.",
    color: "text-ion",
    bgColor: "bg-ion/10",
  },
  {
    icon: Gamepad2,
    title: "Gaming & Simulations",
    description: "Unpredictable outcomes for games, Monte Carlo simulations, and procedural generation.",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: FlaskConical,
    title: "Research & Reproducibility",
    description: "High-quality seeds for experiments. Store hashes for verification, not the secrets themselves.",
    color: "text-ion",
    bgColor: "bg-ion/10",
  },
];

const UseCases = () => {
  return (
    <section className="py-24 relative">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Use <span className="text-gradient-solar">Cases</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            True randomness powers critical systems across industries.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {useCases.map((useCase, index) => (
            <div
              key={index}
              className="group p-6 rounded-xl bg-card border border-border hover:border-primary/50 transition-all duration-300 text-center"
            >
              <div className={`inline-flex h-14 w-14 items-center justify-center rounded-xl ${useCase.bgColor} mb-4 group-hover:scale-110 transition-transform`}>
                <useCase.icon className={`h-7 w-7 ${useCase.color}`} />
              </div>
              <h3 className="font-semibold mb-2">{useCase.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">
                {useCase.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default UseCases;
