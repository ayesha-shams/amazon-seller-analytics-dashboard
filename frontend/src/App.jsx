import { useEffect, useState } from 'react'
import { getKpiSummary, getRevenueTrend, getInventoryAlerts, getAdPerformance } from './api/client'
import KpiCards from './components/KpiCards'
import RevenueTrendChart from './components/RevenueTrendChart'
import InventoryAlerts from './components/InventoryAlerts'
import AdPerformance from './components/AdPerformance'

export default function App() {
  const [kpi, setKpi] = useState(null)
  const [revenueTrend, setRevenueTrend] = useState([])
  const [inventoryAlerts, setInventoryAlerts] = useState([])
  const [adPerformance, setAdPerformance] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    Promise.all([getKpiSummary(), getRevenueTrend(30), getInventoryAlerts(), getAdPerformance(30)])
      .then(([kpiData, revenueData, alertsData, adData]) => {
        setKpi(kpiData)
        setRevenueTrend(revenueData)
        setInventoryAlerts(alertsData)
        setAdPerformance(adData)
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-8 text-slate-500">Loading dashboard…</div>
  if (error) return <div className="p-8 text-red-600">Failed to load data: {error}. Is the backend running on port 8000?</div>

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-xl font-semibold text-slate-900 mb-6">Amazon Seller Analytics Dashboard</h1>
      <KpiCards kpi={kpi} />
      <RevenueTrendChart data={revenueTrend} />
      <InventoryAlerts alerts={inventoryAlerts} />
      <AdPerformance data={adPerformance} />
    </div>
  )
}
