import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || ''
})

export const fetchCustomers = (params) => api.get('/api/customers', { params }).then(r => r.data)
export const fetchProducts = (params) => api.get('/api/products', { params }).then(r => r.data)
export const fetchOrders = (params) => api.get('/api/orders', { params }).then(r => r.data)
export const fetchSummary = (params) => api.get('/api/stats/summary', { params }).then(r => r.data)
export const fetchPivot = (params) => api.get('/api/stats/pivot', { params }).then(r => r.data)
export const fetchChart = (params) => api.get('/api/stats/chart', { params }).then(r => r.data)
