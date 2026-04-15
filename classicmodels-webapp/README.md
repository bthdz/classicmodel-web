# ClassicModels Web App

Website full-stack để **tìm kiếm** và **thống kê** trên CSDL **ClassicModels** theo:
- **Khách hàng**
- **Thời gian**
- **Mặt hàng**

Công nghệ sử dụng:
- **Backend:** FastAPI + SQLAlchemy ORM + RESTful API
- **Frontend:** React + Vite + Recharts
- **Database:** MySQL ClassicModels hoặc SQLite demo

## Chức năng chính

### 1) Tìm kiếm
- Tra cứu khách hàng
- Tra cứu mặt hàng
- Tra cứu đơn hàng theo:
  - khách hàng
  - mặt hàng
  - khoảng thời gian
  - từ khóa

### 2) Thống kê tổng quan
- Tổng doanh thu
- Tổng số lượng bán
- Số đơn hàng
- Số khách hàng phát sinh giao dịch
- Số mặt hàng bán ra

### 3) Pivot / Dashboard
- Pivot theo `customer`, `product`, `month`, `status`
- Giá trị thống kê:
  - `revenue`
  - `quantity`
- Biểu đồ:
  - Bar chart
  - Line chart
- Phân tích theo:
  - khách hàng
  - thời gian
  - mặt hàng

## Cấu trúc thư mục

```text
classicmodels-webapp/
├── backend/
│   ├── app/
│   │   ├── crud.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── seed_demo.py
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Thiết kế dữ liệu ORM

Dùng các bảng cốt lõi của ClassicModels:
- `customers`
- `orders`
- `orderdetails`
- `products`

Các quan hệ ORM chính:
- `Customer 1 - n Order`
- `Order 1 - n OrderDetail`
- `Product 1 - n OrderDetail`

## RESTful API

### Search APIs
- `GET /api/customers?q=&country=`
- `GET /api/products?q=&product_line=`
- `GET /api/orders?q=&customer_id=&product_code=&start_date=&end_date=`

### Analytics APIs
- `GET /api/stats/summary?customer_id=&product_code=&start_date=&end_date=`
- `GET /api/stats/pivot?row_by=customer&col_by=month&value=revenue`
- `GET /api/stats/chart?group_by=month&metric=revenue`

## Cách chạy backend

### 1. Tạo môi trường ảo
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Cấu hình CSDL
Sao chép file môi trường:
```bash
cp .env.example .env
```

Để dùng **ClassicModels MySQL thật**, sửa:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/classicmodels
```

Hoặc dùng **SQLite demo**:
```env
DATABASE_URL=sqlite+pysqlite:///./classicmodels_demo.db
```

### 3. Chạy API
```bash
uvicorn app.main:app --reload --port 8000
```

API docs:
- `http://localhost:8000/docs`

## Cách chạy frontend

```bash
cd frontend
npm install
npm run dev
```

Mở trình duyệt:
- `http://localhost:5173`

## Gợi ý mở rộng
- Thêm xác thực JWT
- Export Excel/PDF
- Phân trang API
- Tối ưu truy vấn bằng materialized view / cache
- Thêm drill-down từ chart sang đơn hàng chi tiết
- Bổ sung bộ lọc theo `productLine`, `country`, `status`

## Lưu ý
- Khi dùng SQLite demo, ứng dụng tự seed dữ liệu mẫu để demo dashboard.
- Khi dùng CSDL ClassicModels thật, hệ thống sẽ làm việc trực tiếp trên schema sẵn có.
