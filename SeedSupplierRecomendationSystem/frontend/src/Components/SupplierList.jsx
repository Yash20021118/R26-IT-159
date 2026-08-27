import SupplierCard from "./SupplierCard";

const suppliers = [
  {
    name: "Agro Lanka",
    price: 2500,
    rating: 4.8,
    distance: 5,
    stock: "Available",
    match: 96,
  },
  {
    name: "Green Harvest",
    price: 2700,
    rating: 4.5,
    distance: 7,
    stock: "Available",
    match: 91,
  },
  {
    name: "Seed Master",
    price: 2900,
    rating: 4.2,
    distance: 10,
    stock: "Low",
    match: 84,
  },
];

const SupplierList = () => {
  return (
    <section id="suppliers" className="section-padding">
      <div className="container-custom">
        <div className="text-center mb-20">
          <h2 className="text-5xl font-bold">Top Ranked Suppliers</h2>

          <p className="text-slate-400 mt-5">
            AI-powered supplier recommendation results
          </p>
        </div>

<div className="grid xl:grid-cols-3 md:grid-cols-2 gap-10">          {suppliers.map((supplier, index) => (
            <SupplierCard key={index} supplier={supplier} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default SupplierList;
