import Navbar from "./Components/Navbar";
import Hero from "./Components/Hero";
import RecommendationForm from "./Components/RecommendationForm";
import Footer from "./Components/Footer";

function App() {
  return (
    <div className="min-h-screen bg-[#07131f] text-white overflow-x-hidden">
      {/* BACKGROUND GLOW */}

      <div className="fixed top-[-250px] left-[-250px] w-[600px] h-[600px] bg-green-500/10 blur-[140px] rounded-full"></div>

      <div className="fixed bottom-[-250px] right-[-250px] w-[600px] h-[600px] bg-cyan-500/10 blur-[140px] rounded-full"></div>

      {/* MAIN */}

      <div className="relative">
        <br />
        <br />

        {/* NAVBAR */}

        <Navbar />
        <br />
        <br />

        {/* HERO */}

        <Hero />
        <br />
        <br />
        <br />
        {/* MAIN CONTENT */}

        <main className="max-w-7xl mx-auto px-6 lg:px-10 pb-24">
          <section id="recommend" className="mt-10">
            <br />
            <br />
            <br />

            <RecommendationForm />
            <br />
            <br />
            <br />
            <br />
          </section>
          <br />
<br />

        </main>

        {/* FOOTER */}
        <br />

        <Footer />
      </div>
    </div>
  );
}

export default App;
