from sqlalchemy import Column, String, Integer, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(255), nullable=False, index=True)
    contactLastName = Column(String(50))
    contactFirstName = Column(String(50))
    phone = Column(String(50))
    city = Column(String(50))
    country = Column(String(50), index=True)
    salesRepEmployeeNumber = Column(Integer)
    creditLimit = Column(Numeric(10, 2))

    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    productCode = Column(String(15), primary_key=True, index=True)
    productName = Column(String(70), nullable=False, index=True)
    productLine = Column(String(50), index=True)
    productScale = Column(String(10))
    productVendor = Column(String(50))
    quantityInStock = Column(Integer)
    buyPrice = Column(Numeric(10, 2))
    MSRP = Column(Numeric(10, 2))

    order_details = relationship("OrderDetail", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True, index=True)
    orderDate = Column(Date, index=True)
    requiredDate = Column(Date)
    shippedDate = Column(Date)
    status = Column(String(15), index=True)
    comments = Column(String(500))
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), index=True)

    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "orderdetails"

    orderNumber = Column(Integer, ForeignKey("orders.orderNumber"), primary_key=True)
    productCode = Column(String(15), ForeignKey("products.productCode"), primary_key=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(Numeric(10, 2), nullable=False)
    orderLineNumber = Column(Integer)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")
