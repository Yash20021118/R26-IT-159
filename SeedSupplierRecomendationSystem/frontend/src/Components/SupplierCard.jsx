const SupplierCard = ({ supplier }) => {

  return (

    <div className="glass-card rounded-[28px] p-7 hover:-translate-y-2 transition duration-300 border border-white/10 flex flex-col justify-between min-h-[320px]">

      <div>

        <div className="flex items-start justify-between gap-4">

          <div>

            <h3 className="text-2xl font-bold text-white">
              {supplier.name}
            </h3>

            <p className="text-slate-400 mt-2">
              Smart Supplier Recommendation
            </p>

          </div>

          <div className="bg-green-500/15 border border-green-500/20 text-green-400 px-4 py-2 rounded-2xl text-lg font-bold">
            {supplier.match || supplier.score?.toFixed(0)}%
          </div>

        </div>

        <div className="mt-8 space-y-4">

          <div className="flex justify-between text-slate-300">
            <span>Price</span>
            <span className="font-semibold text-white">
              Rs. {supplier.price}
            </span>
          </div>

          <div className="flex justify-between text-slate-300">
            <span>Rating</span>
            <span className="font-semibold text-yellow-400">
              ⭐ {supplier.rating}
            </span>
          </div>

          <div className="flex justify-between text-slate-300">
            <span>Distance</span>
            <span className="font-semibold text-white">
              {supplier.distance} km
            </span>
          </div>

          <div className="flex justify-between text-slate-300">
            <span>Stock</span>
            <span className="font-semibold text-green-400">
              {supplier.stock}
            </span>
          </div>

        </div>

      </div>

      <button className="primary-btn w-full mt-8">
        View Supplier
      </button>

    </div>
  )
}

export default SupplierCard