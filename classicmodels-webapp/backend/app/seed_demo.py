from datetime import date
from .database import Base, engine, SessionLocal
from .models import Customer, Product, Order, OrderDetail


def seed_demo_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        customers = [
            Customer(customerNumber=103, customerName="Atelier graphique", contactLastName="Schmitt", contactFirstName="Carine", phone="40.32.2555", city="Nantes", country="France", creditLimit=21000),
            Customer(customerNumber=112, customerName="Signal Gift Stores", contactLastName="King", contactFirstName="Jean", phone="7025551838", city="Las Vegas", country="USA", creditLimit=71800),
            Customer(customerNumber=114, customerName="Australian Collectors, Co.", contactLastName="Ferguson", contactFirstName="Peter", phone="03 9520 4555", city="Melbourne", country="Australia", creditLimit=117300),
        ]
        products = [
            Product(productCode="S10_1678", productName="1969 Harley Davidson Ultimate Chopper", productLine="Motorcycles", productScale="1:10", productVendor="Min Lin Diecast", quantityInStock=7933, buyPrice=48.81, MSRP=95.70),
            Product(productCode="S10_1949", productName="1952 Alpine Renault 1300", productLine="Classic Cars", productScale="1:10", productVendor="Classic Metal Creations", quantityInStock=7305, buyPrice=98.58, MSRP=214.30),
            Product(productCode="S12_1099", productName="1968 Ford Mustang", productLine="Classic Cars", productScale="1:12", productVendor="Autoart Studio Design", quantityInStock=68, buyPrice=95.34, MSRP=194.57),
            Product(productCode="S18_1342", productName="1937 Lincoln Berline", productLine="Vintage Cars", productScale="1:18", productVendor="Motor City Art Classics", quantityInStock=8693, buyPrice=60.62, MSRP=102.74),
        ]
        orders = [
            Order(orderNumber=10100, orderDate=date(2024, 1, 15), requiredDate=date(2024, 1, 25), shippedDate=date(2024, 1, 22), status="Shipped", customerNumber=103),
            Order(orderNumber=10101, orderDate=date(2024, 2, 10), requiredDate=date(2024, 2, 20), shippedDate=date(2024, 2, 18), status="Shipped", customerNumber=112),
            Order(orderNumber=10102, orderDate=date(2024, 3, 5), requiredDate=date(2024, 3, 15), shippedDate=date(2024, 3, 11), status="Shipped", customerNumber=114),
            Order(orderNumber=10103, orderDate=date(2024, 3, 22), requiredDate=date(2024, 4, 1), shippedDate=date(2024, 3, 29), status="Shipped", customerNumber=112),
            Order(orderNumber=10104, orderDate=date(2024, 4, 12), requiredDate=date(2024, 4, 20), shippedDate=date(2024, 4, 18), status="Resolved", customerNumber=103),
        ]
        details = [
            OrderDetail(orderNumber=10100, productCode="S10_1678", quantityOrdered=30, priceEach=95.70, orderLineNumber=1),
            OrderDetail(orderNumber=10100, productCode="S10_1949", quantityOrdered=20, priceEach=214.30, orderLineNumber=2),
            OrderDetail(orderNumber=10101, productCode="S10_1949", quantityOrdered=15, priceEach=210.00, orderLineNumber=1),
            OrderDetail(orderNumber=10101, productCode="S12_1099", quantityOrdered=25, priceEach=194.57, orderLineNumber=2),
            OrderDetail(orderNumber=10102, productCode="S18_1342", quantityOrdered=40, priceEach=102.74, orderLineNumber=1),
            OrderDetail(orderNumber=10103, productCode="S10_1678", quantityOrdered=18, priceEach=92.00, orderLineNumber=1),
            OrderDetail(orderNumber=10103, productCode="S12_1099", quantityOrdered=12, priceEach=190.00, orderLineNumber=2),
            OrderDetail(orderNumber=10104, productCode="S18_1342", quantityOrdered=22, priceEach=101.50, orderLineNumber=1),
            OrderDetail(orderNumber=10104, productCode="S10_1949", quantityOrdered=10, priceEach=212.00, orderLineNumber=2),
        ]
        db.add_all(customers + products + orders + details)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
