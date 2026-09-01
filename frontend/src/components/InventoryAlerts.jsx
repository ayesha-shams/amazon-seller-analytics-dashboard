export default function InventoryAlerts({ alerts }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-4 border border-slate-100 mb-8">
      <h2 className="text-sm font-medium text-slate-700 mb-4">Inventory Alerts</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-slate-500 border-b border-slate-100">
            <th className="pb-2">Product</th>
            <th className="pb-2">In Stock</th>
            <th className="pb-2">Daily Velocity</th>
            <th className="pb-2">Days Left</th>
            <th className="pb-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {alerts.map((a) => (
            <tr key={a.product_id} className="border-b border-slate-50">
              <td className="py-2">{a.product_name}</td>
              <td className="py-2">{a.units_in_stock}</td>
              <td className="py-2">{a.daily_velocity}</td>
              <td className="py-2">{a.days_of_stock_left >= 0 ? a.days_of_stock_left : '—'}</td>
              <td className="py-2">
                {a.needs_reorder ? (
                  <span className="text-red-600 font-medium">Reorder now</span>
                ) : (
                  <span className="text-emerald-600">OK</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
