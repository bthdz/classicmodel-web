export default function OrdersTable({ orders }) {
  return (
    <div className="card table-wrap">
      <h3>Danh sách đơn hàng</h3>
      <table>
        <thead>
          <tr>
            <th>Mã đơn</th>
            <th>Ngày đặt</th>
            <th>Khách hàng</th>
            <th>Trạng thái</th>
            <th>Tổng tiền</th>
            <th>Mặt hàng</th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr key={order.orderNumber}>
              <td>{order.orderNumber}</td>
              <td>{order.orderDate}</td>
              <td>{order.customerName}</td>
              <td>{order.status}</td>
              <td>{Number(order.totalAmount).toLocaleString()}</td>
              <td>{order.items.map((i) => i.productName).join(', ')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
