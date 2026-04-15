export default function PivotTable({ pivot }) {
  if (!pivot || !pivot.rows?.length) {
    return <div className="card">Không có dữ liệu pivot.</div>
  }

  return (
    <div className="card table-wrap">
      <h3>Pivot: {pivot.row_field} × {pivot.column_field} ({pivot.value_field})</h3>
      <table>
        <thead>
          <tr>
            <th>{pivot.row_field}</th>
            {pivot.columns.map((col) => <th key={col}>{col}</th>)}
          </tr>
        </thead>
        <tbody>
          {pivot.rows.map((row) => (
            <tr key={row.row}>
              <td>{row.row}</td>
              {pivot.columns.map((col) => <td key={col}>{row[col] ?? 0}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
