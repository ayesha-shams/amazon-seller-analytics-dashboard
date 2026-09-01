export default function AdPerformance({ data }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-4 border border-slate-100">
      <h2 className="text-sm font-medium text-slate-700 mb-4">Ad Performance by Product (ROAS)</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-slate-500 border-b border-slate-100">
            <th className="pb-2">Product</th>
            <th className="pb-2">Spend</th>
            <th className="pb-2">Attributed Sales</th>
            <th className="pb-2">ROAS</th>
          </tr>
        </thead>
        <tbody>
          {data.map((d) => (
            <tr key={d.product_id} className="border-b border-slate-50">
              <td className="py-2">{d.product_name}</td>
              <td className="py-2">${d.total_spend.toLocaleString()}</td>
              <td className="py-2">${d.total_attributed_sales.toLocaleString()}</td>
              <td className={`py-2 font-medium ${d.roas < 2 ? 'text-red-600' : 'text-emerald-600'}`}>
                {d.roas}x
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
