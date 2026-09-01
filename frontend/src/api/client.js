import axios from 'axios'

// Point this at your deployed backend URL when you go live (e.g. Render/Railway URL)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: API_BASE_URL })

export const getKpiSummary = () => api.get('/analytics/kpi-summary').then(r => r.data)
export const getRevenueTrend = (days = 30) => api.get(`/analytics/revenue-trend?days=${days}`).then(r => r.data)
export const getInventoryAlerts = () => api.get('/analytics/inventory-alerts').then(r => r.data)
export const getAdPerformance = (days = 30) => api.get(`/analytics/ad-performance?days=${days}`).then(r => r.data)
