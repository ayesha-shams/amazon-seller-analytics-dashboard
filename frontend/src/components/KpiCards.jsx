export default function KpiCards({ kpi }) {
  if (!kpi) return null

  const cards = [
    { label: '30-Day Revenue', value: `$${kpi.total_revenue_30d.toLocaleString()}` },
    { label: 'Units Sold (30d)', value: kpi.total_units_30d.toLocaleString() },
    { label: 'Ad Spend (30d)', value: `$${kpi.total_ad_spend_30d.toLocaleString()}` },
    { label: 'Avg ROAS', value: `${kpi.average_roas_30d}x` },
    { label: 'Needs Reorder', value: kpi.products_needing_reorder, alert: kpi.products_needing_reorder > 0 },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
      {cards.map((c) => (
        <div key={c.label} className="bg-white rounded-xl shadow-sm p-4 border border-slate-100">
          <p className="text-xs text-slate-500 mb-1">{c.label}</p>
          <p className={`text-2xl font-semibold ${c.alert ? 'text-red-600' : 'text-slate-900'}`}>{c.value}</p>
        </div>
      ))}
    </div>
  )
}
