from datetime import date
from decimal import Decimal
from sqlalchemy import func, cast, Float
from sqlalchemy.orm import Session, joinedload
from .models import Customer, Product, Order, OrderDetail


def apply_filters(query, customer_id=None, product_code=None, start_date=None, end_date=None):
    if customer_id:
        query = query.filter(Order.customerNumber == customer_id)
    if product_code:
        query = query.filter(OrderDetail.productCode == product_code)
    if start_date:
        query = query.filter(Order.orderDate >= start_date)
    if end_date:
        query = query.filter(Order.orderDate <= end_date)
    return query


def search_customers(db: Session, q: str | None = None, country: str | None = None):
    query = db.query(Customer)
    if q:
        term = f"%{q}%"
        query = query.filter(Customer.customerName.ilike(term))
    if country:
        query = query.filter(Customer.country == country)
    return query.order_by(Customer.customerName.asc()).all()


def search_products(db: Session, q: str | None = None, product_line: str | None = None):
    query = db.query(Product)
    if q:
        term = f"%{q}%"
        query = query.filter(Product.productName.ilike(term))
    if product_line:
        query = query.filter(Product.productLine == product_line)
    return query.order_by(Product.productName.asc()).all()


def search_orders(db: Session, q: str | None = None, customer_id=None, product_code=None, start_date: date | None = None, end_date: date | None = None):
    query = db.query(Order).options(
        joinedload(Order.customer),
        joinedload(Order.order_details).joinedload(OrderDetail.product)
    ).join(Customer).join(OrderDetail)
    if q:
        term = f"%{q}%"
        query = query.filter(Customer.customerName.ilike(term))
    query = apply_filters(query, customer_id, product_code, start_date, end_date)
    return query.distinct().order_by(Order.orderDate.desc()).limit(100).all()


def summary_stats(db: Session, customer_id=None, product_code=None, start_date=None, end_date=None):
    line_total = OrderDetail.quantityOrdered * cast(OrderDetail.priceEach, Float)
    base = db.query(Order, OrderDetail).join(OrderDetail, Order.orderNumber == OrderDetail.orderNumber)
    base = apply_filters(base, customer_id, product_code, start_date, end_date)

    revenue = db.query(func.coalesce(func.sum(line_total), 0.0)).select_from(Order).join(OrderDetail)
    revenue = apply_filters(revenue, customer_id, product_code, start_date, end_date).scalar() or 0

    quantity = db.query(func.coalesce(func.sum(OrderDetail.quantityOrdered), 0)).select_from(Order).join(OrderDetail)
    quantity = apply_filters(quantity, customer_id, product_code, start_date, end_date).scalar() or 0

    orders = db.query(func.count(func.distinct(Order.orderNumber))).select_from(Order).join(OrderDetail)
    orders = apply_filters(orders, customer_id, product_code, start_date, end_date).scalar() or 0

    customers = db.query(func.count(func.distinct(Order.customerNumber))).select_from(Order).join(OrderDetail)
    customers = apply_filters(customers, customer_id, product_code, start_date, end_date).scalar() or 0

    products = db.query(func.count(func.distinct(OrderDetail.productCode))).select_from(Order).join(OrderDetail)
    products = apply_filters(products, customer_id, product_code, start_date, end_date).scalar() or 0

    return {
        "revenue": Decimal(str(round(float(revenue), 2))),
        "quantity": int(quantity),
        "orders": int(orders),
        "customers": int(customers),
        "products": int(products),
    }


def _month_expr(db: Session):
    dialect = db.bind.dialect.name
    if dialect == "sqlite":
        return func.strftime("%Y-%m", Order.orderDate)
    return func.date_format(Order.orderDate, "%Y-%m")


def pivot_data(db: Session, row_by="customer", col_by="month", value="revenue", customer_id=None, product_code=None, start_date=None, end_date=None):
    row_expr_map = {
        "customer": Customer.customerName,
        "product": Product.productName,
        "month": _month_expr(db),
        "status": Order.status,
    }
    col_expr_map = {
        "customer": Customer.customerName,
        "product": Product.productName,
        "month": _month_expr(db),
        "status": Order.status,
    }
    metric_expr = {
        "revenue": func.sum(OrderDetail.quantityOrdered * cast(OrderDetail.priceEach, Float)),
        "quantity": func.sum(OrderDetail.quantityOrdered),
    }

    row_expr = row_expr_map[row_by]
    col_expr = col_expr_map[col_by]
    val_expr = metric_expr[value]

    query = db.query(row_expr.label("row_key"), col_expr.label("col_key"), val_expr.label("metric")) \
        .select_from(Order) \
        .join(Customer, Customer.customerNumber == Order.customerNumber) \
        .join(OrderDetail, OrderDetail.orderNumber == Order.orderNumber) \
        .join(Product, Product.productCode == OrderDetail.productCode)
    query = apply_filters(query, customer_id, product_code, start_date, end_date)
    query = query.group_by(row_expr, col_expr).order_by(row_expr, col_expr)

    records = query.all()
    columns = sorted({str(r.col_key) for r in records if r.col_key is not None})
    table = {}
    for r in records:
        row_key = str(r.row_key)
        if row_key not in table:
            table[row_key] = {"row": row_key}
        table[row_key][str(r.col_key)] = round(float(r.metric or 0), 2)

    return {
        "row_field": row_by,
        "column_field": col_by,
        "value_field": value,
        "columns": columns,
        "rows": list(table.values()),
    }


def chart_data(db: Session, group_by="month", metric="revenue", customer_id=None, product_code=None, start_date=None, end_date=None, limit=10):
    group_expr_map = {
        "month": _month_expr(db),
        "customer": Customer.customerName,
        "product": Product.productName,
    }
    metric_expr = {
        "revenue": func.sum(OrderDetail.quantityOrdered * cast(OrderDetail.priceEach, Float)),
        "quantity": func.sum(OrderDetail.quantityOrdered),
    }
    gexpr = group_expr_map[group_by]
    mexpr = metric_expr[metric]

    query = db.query(gexpr.label("group_key"), mexpr.label("metric")) \
        .select_from(Order) \
        .join(Customer, Customer.customerNumber == Order.customerNumber) \
        .join(OrderDetail, OrderDetail.orderNumber == Order.orderNumber) \
        .join(Product, Product.productCode == OrderDetail.productCode)
    query = apply_filters(query, customer_id, product_code, start_date, end_date)
    query = query.group_by(gexpr).order_by(mexpr.desc() if group_by != "month" else gexpr.asc())
    if group_by != "month":
        query = query.limit(limit)

    rows = query.all()
    return {
        "categories": [str(r.group_key) for r in rows],
        "series": [{"name": metric, "data": [Decimal(str(round(float(r.metric or 0), 2))) for r in rows]}],
    }
