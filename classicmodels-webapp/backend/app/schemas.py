from datetime import date
from decimal import Decimal
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class CustomerOut(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    creditLimit: Optional[Decimal] = None

    class Config:
        from_attributes = True


class ProductOut(BaseModel):
    productCode: str
    productName: str
    productLine: Optional[str] = None
    productScale: Optional[str] = None
    productVendor: Optional[str] = None
    quantityInStock: Optional[int] = None
    buyPrice: Optional[Decimal] = None
    MSRP: Optional[Decimal] = None

    class Config:
        from_attributes = True


class OrderItemOut(BaseModel):
    productCode: str
    productName: str
    productLine: Optional[str] = None
    quantityOrdered: int
    priceEach: Decimal
    lineTotal: Decimal


class OrderOut(BaseModel):
    orderNumber: int
    orderDate: date
    status: Optional[str] = None
    customerNumber: int
    customerName: str
    totalAmount: Decimal
    items: List[OrderItemOut]


class SummaryStats(BaseModel):
    revenue: Decimal
    quantity: int
    orders: int
    customers: int
    products: int


class PivotResponse(BaseModel):
    row_field: str
    column_field: str
    value_field: str
    rows: List[Dict[str, Any]]
    columns: List[str]


class ChartSeries(BaseModel):
    name: str
    data: List[Decimal]


class ChartResponse(BaseModel):
    categories: List[str]
    series: List[ChartSeries]
