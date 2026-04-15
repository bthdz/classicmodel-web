import { useEffect, useMemo, useState } from 'react'
import { BarChart, Bar, CartesianGrid, Legend, LineChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { fetchCustomers, fetchProducts, fetchOrders, fetchSummary, fetchPivot, fetchChart } from './api'
import StatCard from './components/StatCard'
import FilterBar from './components/FilterBar'
import PivotTable from './components/PivotTable'
import OrdersTable from './components/OrdersTable'

const defaultFilters = {
  q: '',
  customer_id: '',
  product_code: '',
  start_date: '',
  end_date: ''
}

function sanitizeFilters(filters) {
  return Object.fromEntries(Object.entries(filters).filter(([, v]) => v !== '' && v !== null && v !== undefined))
}

export default function App() {
  const [filters, setFilters] = useState(defaultFilters)
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [summary, setSummary] = useState(null)
  const [pivotRows, setPivotRows] = useState('customer')
  const [pivotCols, setPivotCols] = useState('month')
  const [pivotValue, setPivotValue] = useState('revenue')
  const [pivot, setPivot] = useState(null)
  const [chartGroupBy, setChartGroupBy] = useState('month')
  const [chartMetric, setChartMetric] = useState('revenue')
  const [chart, setChart] = useState(null)

  const queryParams = useMemo(() => sanitizeFilters(filters), [filters])

  const loadAll = async () => {
    const [customerData, productData, orderData, summaryData, pivotData, chartData] = await Promise.all([
      fetchCustomers({}),
      fetchProducts({}),
      fetchOrders(queryParams),
      fetchSummary(queryParams),
      fetchPivot({ ...queryParams, row_by: pivotRows, col_by: pivotCols, value: pivotValue }),
      fetchChart({ ...queryParams, group_by: chartGroupBy, metric: chartMetric })
    ])

    setCustomers(customerData)
    setProducts(productData)
    setOrders(orderData)
    setSummary(summaryData)
    setPivot(pivotData)
    setChart(chartData)
  }

  useEffect(() => {
    loadAll()
  }, [pivotRows, pivotCols, pivotValue, chartGroupBy, chartMetric])

  const chartData = useMemo(() => {
    if (!chart) return []
    return chart.categories.map((c, index) => ({
      name: c,
      value: Number(chart.series[0]?.data[index] || 0)
    }))
  }, [chart])

  return (
    <div className="app-shell">
      <header>
        <div>
          <h1>ClassicModels Analytics Dashboard</h1>
          <p>Tìm kiếm và thống kê theo khách hàng, thời gian, mặt hàng bằng ORM + RESTful API.</p>
        </div>
      </header>

      <FilterBar filters={filters} setFilters={setFilters} customers={customers} products={products} onRefresh={loadAll} />

      {summary && (
        <section className="stats-grid">
          <StatCard title="Doanh thu" value={Number(summary.revenue).toLocaleString()} />
          <StatCard title="Số lượng bán" value={summary.quantity} />
          <StatCard title="Đơn hàng" value={summary.orders} />
          <StatCard title="Khách hàng" value={summary.customers} />
          <StatCard title="Mặt hàng" value={summary.products} />
        </section>
      )}

      <section className="card chart-toolbar">
        <div>
          <label>Pivot Rows</label>
          <select value={pivotRows} onChange={(e) => setPivotRows(e.target.value)}>
            <option value="customer">customer</option>
            <option value="product">product</option>
            <option value="month">month</option>
            <option value="status">status</option>
          </select>
        </div>
        <div>
          <label>Pivot Columns</label>
          <select value={pivotCols} onChange={(e) => setPivotCols(e.target.value)}>
            <option value="month">month</option>
            <option value="customer">customer</option>
            <option value="product">product</option>
            <option value="status">status</option>
          </select>
        </div>
        <div>
          <label>Pivot Value</label>
          <select value={pivotValue} onChange={(e) => setPivotValue(e.target.value)}>
            <option value="revenue">revenue</option>
            <option value="quantity">quantity</option>
          </select>
        </div>
        <div>
          <label>Chart Group</label>
          <select value={chartGroupBy} onChange={(e) => setChartGroupBy(e.target.value)}>
            <option value="month">month</option>
            <option value="customer">customer</option>
            <option value="product">product</option>
          </select>
        </div>
        <div>
          <label>Chart Metric</label>
          <select value={chartMetric} onChange={(e) => setChartMetric(e.target.value)}>
            <option value="revenue">revenue</option>
            <option value="quantity">quantity</option>
          </select>
        </div>
      </section>

      <section className="chart-grid">
        <div className="card chart-card">
          <h3>Biểu đồ cột</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" name={chartMetric} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="card chart-card">
          <h3>Biểu đồ đường</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" name={chartMetric} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <PivotTable pivot={pivot} />
      <OrdersTable orders={orders} />
    </div>
  )
}
