import { useState } from "react";
import axios from "axios";

import ComparisonTable from "./ComparisonTable";
import Analytics from "./Analytics";

const RecommendationForm = () => {
  const [seedType, setSeedType] = useState("Rice Seed");
  const [region, setRegion] = useState("Colombo");

  const [suppliers, setSuppliers] = useState([]);

  const [searchTerm, setSearchTerm] = useState("");
  const [minimumRating, setMinimumRating] = useState(0);
  const [maximumDistance, setMaximumDistance] = useState(100);

  // Filter suppliers
  const filteredSuppliers = suppliers.filter((supplier) => {
    return (
      supplier.supplierName
        ?.toLowerCase()
        .includes(searchTerm.toLowerCase()) &&
      supplier.rating >= minimumRating &&
      supplier.distance_km <= maximumDistance
    );
  });

  const topSupplier = filteredSuppliers[0];

  // Get recommendations
  const getRecommendations = async () => {
    try {
      const response = await axios.post(
        "http://localhost:5001/api/suppliers/rank",
        {
          seedType,
          region,
          minimumRating,
          maximumDistance,
        }
      );

      setSuppliers(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <section className="px-6 py-10">
      <div className="max-w-7xl mx-auto glass-card p-10 rounded-[35px]">

        <h2 className="text-5xl font-black mb-12">
          Supplier Recommendation Engine
        </h2>

        {/* FORM */}
        <div className="grid md:grid-cols-2 gap-8">

          <div>
            <label className="block mb-3 text-lg font-semibold">
              Seed Type
            </label>

            <select
              value={seedType}
              onChange={(e) => setSeedType(e.target.value)}
              className="input-field"
            >
              <option>Rice Seed</option>
              <option>Corn Seed</option>
              <option>Tomato Seed</option>
              <option>Onion Seed</option>
              <option>Carrot Seed</option>
              <option>Potato Seed</option>
              <option>Cabbage Seed</option>
              <option>Chili Seed</option>
              <option>Brinjal Seed</option>
              <option>Pumpkin Seed</option>
            </select>
          </div>

          <div>
            <label className="block mb-3 text-lg font-semibold">
              Region
            </label>

            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="input-field"
            >
              <option>Colombo</option>
              <option>Kandy</option>
              <option>Galle</option>
              <option>Kurunegala</option>
              <option>Jaffna</option>
              <option>Anuradhapura</option>
              <option>Badulla</option>
              <option>Matara</option>
              <option>Ratnapura</option>
              <option>Nuwara Eliya</option>
              <option>Trincomalee</option>
              <option>Batticaloa</option>
              <option>Hambantota</option>
              <option>Polonnaruwa</option>
              <option>Ampara</option>
              <option>Monaragala</option>
              <option>Kalutara</option>
              <option>Puttalam</option>
              <option>Vavuniya</option>
              <option>Kilinochchi</option>
            </select>
          </div>
        </div>

        {/* AHP + TOPSIS */}
        <div className="mt-14">
          <h3 className="text-3xl font-bold mb-8">
            Recommendation Method
          </h3>

          <div className="glass-card p-8 rounded-3xl border border-green-500/20">

            <div className="flex items-center gap-3 mb-4">
              <div className="w-4 h-4 rounded-full bg-green-400"></div>

              <h4 className="text-2xl font-bold text-green-400">
                AHP + TOPSIS
              </h4>
            </div>

            <p className="text-slate-300 leading-7">
              This supplier recommendation system uses the Analytic Hierarchy
              Process (AHP) to determine expert-based criteria weights and
              TOPSIS to rank eligible suppliers based on Price, Rating,
              Distance and Stock Availability.
            </p>

            <div className="grid md:grid-cols-4 gap-4 mt-8">

              <div className="bg-white/5 p-4 rounded-2xl text-center">
                <p className="text-slate-400 text-sm">Price</p>
                <p className="font-bold mt-2">Cost</p>
              </div>

              <div className="bg-white/5 p-4 rounded-2xl text-center">
                <p className="text-slate-400 text-sm">Rating</p>
                <p className="font-bold mt-2">Benefit</p>
              </div>

              <div className="bg-white/5 p-4 rounded-2xl text-center">
                <p className="text-slate-400 text-sm">Distance</p>
                <p className="font-bold mt-2">Cost</p>
              </div>

              <div className="bg-white/5 p-4 rounded-2xl text-center">
                <p className="text-slate-400 text-sm">Stock</p>
                <p className="font-bold mt-2">Benefit</p>
              </div>

            </div>

            <p className="text-green-400 mt-6 text-sm">
              Criteria weights are determined using expert evaluation (AHP)
              and are not manually adjusted by users.
            </p>

          </div>
        </div>

        {/* FILTERS */}
        <div className="mt-14">

          <h3 className="text-3xl font-bold mb-8">
            Search & Filter Suppliers
          </h3>

          <div className="grid md:grid-cols-3 gap-8">

            <div>
              <label className="block mb-3">
                Search Supplier
              </label>

              <input
                type="text"
                placeholder="Search supplier..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field"
              />
            </div>

            <div>
              <label className="block mb-3">
                Minimum Rating
              </label>

              <input
                type="number"
                min="0"
                max="5"
                step="0.1"
                value={minimumRating}
                onChange={(e) => setMinimumRating(Number(e.target.value))}
                className="input-field"
              />
            </div>

            <div>
              <label className="block mb-3">
                Maximum Distance (km)
              </label>

              <input
                type="number"
                min="1"
                value={maximumDistance}
                onChange={(e) => setMaximumDistance(Number(e.target.value))}
                className="input-field"
              />
            </div>

          </div>
        </div>

        {/* BUTTON */}
        <button
          onClick={getRecommendations}
          className="primary-btn mt-14"
        >
          Generate Recommendation
        </button>

        {/* TOP SUPPLIER */}
        {topSupplier && (
          <div className="glass-card p-10 rounded-[35px] mt-16 border border-green-500/20">

            <p className="text-green-400 font-bold tracking-widest">
              TOP RECOMMENDED SUPPLIER
            </p>

            <div className="flex flex-col lg:flex-row justify-between gap-10 mt-6">

              <div>

                <h1 className="text-5xl font-black">
                  {topSupplier.supplierName}
                </h1>

                <p className="text-slate-400 mt-6 leading-8 max-w-2xl">
                  Supplier ranking generated using the AHP–TOPSIS
                  multi-criteria decision-making method based on
                  Price, Supplier Rating, Distance and Stock Availability.
                </p>

                <div className="grid grid-cols-2 gap-6 mt-10">

                  <div className="glass-card p-5 rounded-2xl">
                    <p className="text-slate-400">Price</p>
                    <h3 className="text-2xl font-bold mt-2">
                      Rs. {topSupplier.price}
                    </h3>
                  </div>

                  <div className="glass-card p-5 rounded-2xl">
                    <p className="text-slate-400">Rating</p>
                    <h3 className="text-2xl font-bold mt-2 text-yellow-400">
                      ⭐ {topSupplier.rating}
                    </h3>
                  </div>

                  <div className="glass-card p-5 rounded-2xl">
                    <p className="text-slate-400">Distance</p>
                    <h3 className="text-2xl font-bold mt-2">
                      {topSupplier.distance_km} km
                    </h3>
                  </div>

                  <div className="glass-card p-5 rounded-2xl">
                    <p className="text-slate-400">Stock</p>
                    <h3 className="text-2xl font-bold mt-2 text-green-400">
                      {topSupplier.stock}
                    </h3>
                  </div>

                </div>

              </div>

              <div className="glass-card p-10 rounded-[35px] min-w-[260px] flex flex-col justify-center items-center border border-green-500/20">

                <p className="text-slate-400">
                  TOPSIS Score
                </p>

                <h1 className="text-6xl font-black text-green-400 mt-4">
                  {topSupplier.score
                    ? `${(topSupplier.score * 100).toFixed(2)}%`
                    : "0%"}
                </h1>

                <p className="text-sm text-slate-500 mt-3">
                  Closeness Coefficient
                </p>

              </div>

            </div>

          </div>
        )}

        {/* SUPPLIER CARDS */}
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8 mt-16">

          {filteredSuppliers.map((supplier) => (

            <div
              key={supplier._id}
              className="glass-card p-8 rounded-[30px] border border-white/10 hover:-translate-y-2 transition duration-300"
            >

              <div className="flex justify-between items-start">

                <div>
                  <h3 className="text-2xl font-bold">
                    {supplier.supplierName}
                  </h3>

                  <p className="text-slate-400 mt-2">
                    Smart Supplier Match
                  </p>
                </div>

                <div className="bg-green-500/20 text-green-400 px-4 py-2 rounded-2xl font-bold">
                  {supplier.rank ? `#${supplier.rank}` : "-"}
                </div>

              </div>

              <div className="mt-8 space-y-5">

                <div className="flex justify-between">
                  <span className="text-slate-400">Price</span>
                  <span>Rs. {supplier.price}</span>
                </div>

                <div className="flex justify-between">
                  <span className="text-slate-400">Rating</span>
                  <span className="text-yellow-400">
                    ⭐ {supplier.rating}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-slate-400">Distance</span>
                  <span>{supplier.distance_km} km</span>
                </div>

                <div className="flex justify-between">
                  <span className="text-slate-400">Stock</span>
                  <span className="text-green-400">
                    {supplier.stock}
                  </span>
                </div>

              </div>

              <div className="mt-6 pt-4 border-t border-white/10 flex justify-between items-center">

                <span className="text-slate-400 text-sm">
                  TOPSIS Score
                </span>

                <span className="text-xl font-bold text-green-400">
                  {supplier.score
                    ? `${(supplier.score * 100).toFixed(2)}%`
                    : "0%"}
                </span>

              </div>

            </div>

          ))}

        </div>

        {/* TABLE */}
        <ComparisonTable suppliers={filteredSuppliers} />

        {/* ANALYTICS */}
        <div className="mt-16">
          <Analytics suppliers={filteredSuppliers} />
        </div>

      </div>
    </section>
  );
};

export default RecommendationForm;