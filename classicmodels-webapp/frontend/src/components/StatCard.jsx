export default function StatCard({ title, value }) {
  return (
    <div className="card stat-card">
      <div className="muted">{title}</div>
      <div className="stat-value">{value}</div>
    </div>
  )
}
