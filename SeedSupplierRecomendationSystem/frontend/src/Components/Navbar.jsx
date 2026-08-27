const Navbar = () => {
  return (
<nav className="fixed top-0 w-full z-50 px-14 py-7 flex justify-between items-center glass">
      <div>

        <h1 className="text-3xl font-bold text-green-400">
          SeedAI
        </h1>

        <p className="text-xs text-slate-400">
          Smart Supplier Matching
        </p>

      </div>

<div className="hidden md:flex gap-12 text-slate-300 items-center">
        <a href="#home" className="hover:text-green-400 transition">
          Home
        </a>

        <a href="#recommend" className="hover:text-green-400 transition">
          Recommendation
        </a>

        <a href="#suppliers" className="hover:text-green-400 transition">
          Suppliers
        </a>

        <a href="#analytics" className="hover:text-green-400 transition">
          Analytics
        </a>

      </div>

      <button className="primary-btn">
        Start
      </button>

    </nav>
  )
}

export default Navbar