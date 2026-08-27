const ComparisonTable = ({ suppliers = [] }) => {
  if (!suppliers.length) {
    return (
      <div className="mt-16 overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-sm">
        <div className="px-8 py-8 md:px-10 md:py-10">
          <div className="flex items-center gap-5">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-100 text-2xl">
              📋
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-800 md:text-3xl">
                Supplier Comparison
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Compare supplier performance metrics and recommendation scores
              </p>
            </div>
          </div>

          <div className="mt-10 flex min-h-[220px] flex-col items-center justify-center rounded-3xl bg-slate-50 px-6 py-10 text-center">
            <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-white text-3xl shadow-sm">
              📊
            </div>

            <p className="font-semibold text-slate-600">
              No supplier data available
            </p>

            <p className="mt-2 max-w-md text-sm leading-6 text-slate-400">
              Supplier comparison details will appear here once supplier data
              is available.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-16 overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-sm transition-shadow duration-300 hover:shadow-md">

      {/* ================= HEADER ================= */}
      <div className="border-b border-slate-100 bg-gradient-to-r from-emerald-50 via-white to-white px-8 py-8 md:px-10 md:py-10">

        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

          <div className="flex items-center gap-5">

            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-emerald-100 text-2xl">
              📋
            </div>

            <div>
              <h2 className="text-2xl font-bold tracking-tight text-slate-800 md:text-3xl">
                Supplier Comparison
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Compare supplier performance metrics and recommendation scores
              </p>
            </div>

          </div>

          {/* Supplier count */}
          <div className="flex w-fit items-center gap-3 rounded-full border border-emerald-100 bg-white px-5 py-3 shadow-sm">

            <span className="h-3 w-3 rounded-full bg-emerald-500" />

            <span className="text-sm font-semibold text-slate-600">
              {suppliers.length} Suppliers
            </span>

          </div>

        </div>

      </div>

      {/* ================= TABLE AREA ================= */}
      <div className="p-6 md:p-8">

        <div className="overflow-x-auto rounded-3xl border border-slate-100">

          <table className="w-full min-w-[950px] text-left">

            {/* ================= TABLE HEADER ================= */}
            <thead className="bg-slate-50">

              <tr className="border-b border-slate-200">

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Supplier
                </th>

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Price
                </th>

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Rating
                </th>

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Distance
                </th>

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Stock
                </th>

                <th className="px-6 py-5 text-sm font-semibold text-slate-500">
                  Score
                </th>

              </tr>

            </thead>

            {/* ================= TABLE BODY ================= */}
            <tbody>

              {suppliers.map((supplier, index) => (

                <tr
                  key={supplier._id}
                  className="border-b border-slate-100 transition-all duration-200 last:border-b-0 hover:bg-emerald-50/40"
                >

                  {/* SUPPLIER */}
                  <td className="px-6 py-6">

                    <div className="flex items-center gap-4">

                      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-emerald-50 font-bold text-emerald-600">
                        {index + 1}
                      </div>

                      <div>

                        <h3 className="text-base font-bold text-slate-800">
                          {supplier.name}
                        </h3>

                        <p className="mt-1 text-sm text-slate-400">
                          Smart Supplier Match
                        </p>

                      </div>

                    </div>

                  </td>

                  {/* PRICE */}
                  <td className="px-6 py-6">

                    <div className="font-semibold text-slate-700">
                      Rs. {supplier.price}
                    </div>

                  </td>

                  {/* RATING */}
                  <td className="px-6 py-6">

                    <div className="inline-flex items-center gap-2 rounded-xl bg-amber-50 px-3 py-2">

                      <span className="text-sm">
                        ⭐
                      </span>

                      <span className="font-semibold text-amber-700">
                        {supplier.rating}
                      </span>

                    </div>

                  </td>

                  {/* DISTANCE */}
                  <td className="px-6 py-6">

                    <div className="inline-flex items-center gap-2 text-slate-600">

                      <span className="text-sm">
                        📍
                      </span>

                      <span className="font-medium">
                        {supplier.distance} km
                      </span>

                    </div>

                  </td>

                  {/* STOCK */}
                  <td className="px-6 py-6">

                    <div className="inline-flex items-center gap-2 rounded-xl bg-emerald-50 px-3 py-2">

                      <span className="h-2 w-2 rounded-full bg-emerald-500" />

                      <span className="font-semibold text-emerald-700">
                        {supplier.stock}
                      </span>

                    </div>

                  </td>

                  {/* SCORE */}
                  <td className="px-6 py-6">

                    <div className="inline-flex min-w-[70px] items-center justify-center rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-2.5 font-bold text-emerald-700">

                      {supplier.score.toFixed(0)}

                    </div>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

        {/* TABLE FOOTER */}
        <div className="mt-6 flex flex-col gap-3 rounded-2xl bg-slate-50 px-5 py-4 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between">

          <span>
            Showing {suppliers.length} supplier
            {suppliers.length !== 1 ? "s" : ""}
          </span>

          <span className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Recommendation scores are based on the current ranking
          </span>

        </div>

      </div>

    </div>
  );
};

export default ComparisonTable;