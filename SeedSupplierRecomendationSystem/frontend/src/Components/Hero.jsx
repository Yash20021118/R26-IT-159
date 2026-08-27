import { motion } from "framer-motion";

const Hero = () => {
  return (
    <section
      id="home"
      className="relative min-h-[90vh] flex items-center justify-center overflow-hidden pt-36 pb-24 px-6"
    >
      {/* BACKGROUND EFFECTS */}

      <div className="absolute top-[-150px] left-[-150px] w-[500px] h-[500px] bg-green-500/10 rounded-full blur-[120px]"></div>

      <div className="absolute bottom-[-150px] right-[-150px] w-[500px] h-[500px] bg-cyan-500/10 rounded-full blur-[120px]"></div>

      {/* GRID */}

      <div className="absolute inset-0 opacity-[0.03]">
        <div className="h-full w-full bg-[linear-gradient(to_right,#ffffff10_1px,transparent_1px),linear-gradient(to_bottom,#ffffff10_1px,transparent_1px)] bg-[size:80px_80px]"></div>
      </div>

      {/* CONTENT */}

      <motion.div
        initial={{ opacity: 0, y: 70 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="relative z-10 text-center max-w-7xl"
      >
        {/* BADGE */}

<div className="inline-flex items-center gap-5 mb-10 px-8 py-4  border-lime-400/30 bg-gradient-to-r from-lime-400/20 via-green-400/15 to-emerald-400/10 backdrop-blur-2xl shadow-[0_0_50px_rgba(132,255,0,0.25)]">

  <div className="relative flex items-center justify-center">

    <div className="w-3 h-3 rounded-full bg-lime-300 animate-pulse shadow-[0_0_20px_rgba(190,242,100,1)]"></div>

    <div className="absolute w-6 h-6 rounded-full border border-lime-300/40 animate-ping"></div>

  </div>

  <span className="text-lime-200 text-sm md:text-base font-bold tracking-[0.30em] uppercase drop-shadow-[0_0_10px_rgba(190,242,100,0.6)]">

    AI Recommendation Powered Marketplace

  </span>

</div>

        {/* TITLE */}

        <h1 className="text-5xl md:text-8xl font-black leading-[1.05] tracking-tight max-w-6xl mx-auto">
          Smart Seed
          <span className="text-green-400"> Supplier </span>
          Matching System
        </h1>

        {/* DESCRIPTION */}

        <p className="mt-10 text-slate-400 text-xl md:text-2xl leading-10 max-w-4xl mx-auto">
          Intelligent supplier recommendation platform using weighted ranking
          algorithms based on supplier pricing, ratings, distance analysis, and
          stock availability for smarter agricultural decision making.
        </p>

        {/* BUTTONS */}

        <div className="mt-14 flex justify-center items-center gap-6 flex-wrap">
          <button className="primary-btn text-lg px-10 py-5">
            Generate Recommendation
          </button>

          <button className="secondary-btn text-lg px-10 py-5">
            Explore Marketplace
          </button>
        </div>
        <br />
        {/* STATS */}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20">
          <div className="glass-card rounded-[28px] p-8 border border-white/10">
            <h2 className="text-4xl font-black text-green-400">25+</h2>

            <p className="text-slate-400 mt-3">Verified Suppliers</p>
          </div>

          <div className="glass-card rounded-[28px] p-8 border border-white/10">
            <h2 className="text-4xl font-black text-cyan-400">AI</h2>

            <p className="text-slate-400 mt-3">Smart Ranking</p>
          </div>

          <div className="glass-card rounded-[28px] p-8 border border-white/10">
            <h2 className="text-4xl font-black text-yellow-400">98%</h2>

            <p className="text-slate-400 mt-3">Recommendation Accuracy</p>
          </div>

          <div className="glass-card rounded-[28px] p-8 border border-white/10">
            <h2 className="text-4xl font-black text-pink-400">Live</h2>

            <p className="text-slate-400 mt-3">Marketplace Analytics</p>
          </div>
        </div>
      </motion.div>
    </section>
    
  );
};

export default Hero;
