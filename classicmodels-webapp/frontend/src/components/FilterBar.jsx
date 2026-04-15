export default function FilterBar({ filters, setFilters, customers, products, onRefresh }) {
  const update = (key, value) => setFilters((prev) => ({ ...prev, [key]: value }))

  return (
    <div className="card filter-grid">
      <div>
        <label>Từ khóa</label>
        <input value={filters.q} onChange={(e) => update('q', e.target.value)} placeholder="Tên khách hàng / đơn hàng" />
      </div>
      <div>
        <label>Khách hàng</label>
        <select value={filters.customer_id} onChange={(e) => update('customer_id', e.target.value)}>
          <option value="">Tất cả</option>
          {customers.map((c) => (
            <option key={c.customerNumber} value={c.customerNumber}>{c.customerName}</option>
          ))}
        </select>
      </div>
      <div>
        <label>Mặt hàng</label>
        <select value={filters.product_code} onChange={(e) => update('product_code', e.target.value)}>
          <option value="">Tất cả</option>
          {products.map((p) => (
            <option key={p.productCode} value={p.productCode}>{p.productName}</option>
          ))}
        </select>
      </div>
      <div>
        <label>Từ ngày</label>
        <input type="date" value={filters.start_date} onChange={(e) => update('start_date', e.target.value)} />
      </div>
      <div>
        <label>Đến ngày</label>
        <input type="date" value={filters.end_date} onChange={(e) => update('end_date', e.target.value)} />
      </div>
      <div className="filter-actions">
        <button onClick={onRefresh}>Làm mới dữ liệu</button>
      </div>
    </div>
  )
}
