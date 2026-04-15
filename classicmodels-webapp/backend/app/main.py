from datetime import date
from decimal import Decimal
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import crud, schemas
from .seed_demo import seed_demo_data
from .models import OrderDetail

app = FastAPI(title="ClassicModels Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        has_data = db.query(OrderDetail).first() is not None
    finally:
        db.close()
    if not has_data and engine.url.get_backend_name().startswith("sqlite"):
        seed_demo_data()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/customers", response_model=list[schemas.CustomerOut])
def get_customers(
    q: str | None = None,
    country: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.search_customers(db, q=q, country=country)


@app.get("/api/products", response_model=list[schemas.ProductOut])
def get_products(
    q: str | None = None,
    product_line: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.search_products(db, q=q, product_line=product_line)


@app.get("/api/orders", response_model=list[schemas.OrderOut])
def get_orders(
    q: str | None = None,
    customer_id: int | None = None,
    product_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    orders = crud.search_orders(db, q=q, customer_id=customer_id, product_code=product_code, start_date=start_date, end_date=end_date)
    response = []
    for order in orders:
        items = []
        total = Decimal("0")
        for item in order.order_details:
            line_total = Decimal(str(item.quantityOrdered)) * item.priceEach
            total += line_total
            items.append({
                "productCode": item.productCode,
                "productName": item.product.productName,
                "productLine": item.product.productLine,
                "quantityOrdered": item.quantityOrdered,
                "priceEach": item.priceEach,
                "lineTotal": line_total,
            })
        response.append({
            "orderNumber": order.orderNumber,
            "orderDate": order.orderDate,
            "status": order.status,
            "customerNumber": order.customerNumber,
            "customerName": order.customer.customerName,
            "totalAmount": total,
            "items": items,
        })
    return response


@app.get("/api/stats/summary", response_model=schemas.SummaryStats)
def get_summary(
    customer_id: int | None = None,
    product_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return crud.summary_stats(db, customer_id, product_code, start_date, end_date)


@app.get("/api/stats/pivot", response_model=schemas.PivotResponse)
def get_pivot(
    row_by: str = Query("customer", pattern="^(customer|product|month|status)$"),
    col_by: str = Query("month", pattern="^(customer|product|month|status)$"),
    value: str = Query("revenue", pattern="^(revenue|quantity)$"),
    customer_id: int | None = None,
    product_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return crud.pivot_data(db, row_by, col_by, value, customer_id, product_code, start_date, end_date)


@app.get("/api/stats/chart", response_model=schemas.ChartResponse)
def get_chart(
    group_by: str = Query("month", pattern="^(month|customer|product)$"),
    metric: str = Query("revenue", pattern="^(revenue|quantity)$"),
    customer_id: int | None = None,
    product_code: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return crud.chart_data(db, group_by, metric, customer_id, product_code, start_date, end_date, limit)
