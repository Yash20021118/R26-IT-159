import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const Analytics = ({ suppliers }) => {
  // SAFETY CHECK
  if (!suppliers || suppliers.length === 0) {
    return (
      <div className="mt-10 overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-sm">
        <div className="px-8 py-8 md:px-10 md:py-10">
          <div className="flex items-center gap-5">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-100 text-2xl">
              📊
            </div>

            <div>
              <h2 className="text-2xl font-bold text-slate-800 md:text-3xl">
                Supplier Analytics
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Performance overview of available suppliers
              </p>
            </div>
          </div>

          <div className="mt-10 flex min-h-[220px] flex-col items-center justify-center rounded-3xl bg-slate-50 px-6 py-10 text-center">
            <div className="mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-white text-3xl shadow-sm">
              📈
            </div>

            <p className="font-semibold text-slate-600">
              No supplier data available.
            </p>

            <p className="mt-2 max-w-md text-sm leading-6 text-slate-400">
              Supplier analytics will appear here once supplier information is
              available.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // CHART DATA
  // Existing supplier data and fields remain unchanged.
  const chartData = suppliers.map((supplier) => ({
    name: supplier.supplierName,
    score: supplier.score || 0,
    rating: supplier.rating,
    stock: supplier.stock,
  }));

  // DISPLAY-ONLY STATISTICS
  const bestScore = Math.max(
    ...suppliers.map((supplier) => supplier.score || 0)
  );

  const averageScore =
    suppliers.reduce(
      (total, supplier) => total + (supplier.score || 0),
      0
    ) / suppliers.length;

  return (
    <div className="mt-10 overflow-hidden rounded-[32px] border border-slate-200 bg-white shadow-sm transition-shadow duration-300 hover:shadow-md">

      {/* ================= HEADER ================= */}
      <div className="border-b border-slate-100 bg-gradient-to-r from-emerald-50 via-white to-white px-8 py-8 md:px-10 md:py-10">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">

          <div className="flex items-center gap-5">
            <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-emerald-100 text-2xl">
              📊
            </div>

            <div>
              <h2 className="text-2xl font-bold tracking-tight text-slate-800 md:text-3xl">
                Supplier Analytics
              </h2>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                Visual comparison of supplier recommendation scores
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

      {/* ================= MAIN CONTENT ================= */}
      <div className="p-8 md:p-10">

        {/* ================= SUMMARY CARDS ================= */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">

          {/* Suppliers */}
          <div className="rounded-3xl border border-slate-100 bg-slate-50 p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-md md:p-7">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">
                  Total Suppliers
                </p>

                <p className="mt-4 text-3xl font-bold text-slate-800">
                  {suppliers.length}
                </p>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-50 text-xl">
                👥
              </div>
            </div>

            <p className="mt-5 text-sm text-slate-400">
              Available for comparison
            </p>
          </div>

          {/* Best Score */}
          <div className="rounded-3xl border border-emerald-100 bg-emerald-50/60 p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-md md:p-7">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">
                  Best Score
                </p>

                <p className="mt-4 text-3xl font-bold text-emerald-700">
                  {bestScore.toFixed(2)}
                </p>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-xl">
                🏆
              </div>
            </div>

            <p className="mt-5 text-sm text-slate-400">
              Highest recommendation score
            </p>
          </div>

          {/* Average Score */}
          <div className="rounded-3xl border border-amber-100 bg-amber-50/60 p-6 transition-all duration-300 hover:-translate-y-1 hover:shadow-md md:p-7">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium text-slate-500">
                  Average Score
                </p>

                <p className="mt-4 text-3xl font-bold text-slate-800">
                  {averageScore.toFixed(2)}
                </p>
              </div>

              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100 text-xl">
                📈
              </div>
            </div>

            <p className="mt-5 text-sm text-slate-400">
              Across all suppliers
            </p>
          </div>
        </div>

        {/* ================= CHART SECTION ================= */}
        <div className="mt-10 rounded-3xl border border-slate-100 bg-slate-50/60 p-6 md:p-8">

          {/* Chart heading */}
          <div className="mb-8">
            <div className="flex items-center gap-3">
              <div className="h-2 w-2 rounded-full bg-emerald-500" />

              <h3 className="text-lg font-bold text-slate-800 md:text-xl">
                Recommendation Score
              </h3>
            </div>

            <p className="mt-3 text-sm leading-6 text-slate-500">
              Compare the recommendation scores of available suppliers.
            </p>
          </div>

          {/* Chart */}
          <div className="h-[360px] w-full md:h-[430px]">

            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{
                  top: 10,
                  right: 20,
                  left: 5,
                  bottom: 65,
                }}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#e2e8f0"
                />

                <XAxis
                  dataKey="name"
                  tick={{
                    fill: "#64748b",
                    fontSize: 12,
                  }}
                  axisLine={false}
                  tickLine={false}
                  angle={-25}
                  textAnchor="end"
                  interval={0}
                />

                <YAxis
                  tick={{
                    fill: "#64748b",
                    fontSize: 12,
                  }}
                  axisLine={false}
                  tickLine={false}
                />

                <Tooltip
                  cursor={{
                    fill: "rgba(16, 185, 129, 0.06)",
                  }}
                  contentStyle={{
                    borderRadius: "16px",
                    border: "1px solid #e2e8f0",
                    backgroundColor: "#ffffff",
                    boxShadow:
                      "0 10px 30px rgba(15, 23, 42, 0.10)",
                    padding: "14px 16px",
                  }}
                  labelStyle={{
                    fontWeight: "700",
                    color: "#1e293b",
                    marginBottom: "6px",
                  }}
                  itemStyle={{
                    color: "#059669",
                    fontWeight: "600",
                  }}
                />

                <Bar
                  dataKey="score"
                  name="Recommendation Score"
                  fill="#10b981"
                  radius={[8, 8, 0, 0]}
                  maxBarSize={55}
                />

              </BarChart>
            </ResponsiveContainer>

          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;