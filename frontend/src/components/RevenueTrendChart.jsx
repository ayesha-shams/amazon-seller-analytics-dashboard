import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function RevenueTrendChart({ data }) {
  return (
    <div className="bg-white rounded-xl shadow-sm p-4 border border-slate-100 mb-8">
      <h2 className="text-sm font-medium text-slate-700 mb-4">Revenue Trend (30 days)</h2>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis dataKey="date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#4f46e5" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
