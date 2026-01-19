import enum
from datetime import datetime
from email.policy import default
from typing import Optional, Any

import sqlalchemy.orm as orm
from sqlalchemy.orm import DeclarativeBase, relationship, attribute_mapped_collection, backref, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Column, Numeric, Enum, DateTime, \
    func


class Base(DeclarativeBase):
    __abstract__ = True

class Catalog(Base):
    __tablename__ = 'catalogs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    parent_id = Column(Integer, ForeignKey('catalogs.id'), index=True, nullable=True)
    products = orm.relationship("Product", back_populates="catalog")

    sub_catalog = relationship(
        'Catalog',
        cascade='all',
        backref=backref("parent", remote_side='Catalog.id'),
        collection_class=attribute_mapped_collection('name')
    )

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.index = 0

    def append(self, catalog_name):
        self.sub_catalog[catalog_name] = Catalog(catalog_name, parent=self)
        self.index = len(self.sub_catalog)

    def get_sub_catalog(self, name):
        if name in self.sub_catalog:
            return self.sub_catalog[name]

    def __getitem__(self, item):
        return self.sub_catalog[item]

    def __setitem__(self, key, value):
        self.sub_catalog[key] = Catalog(value, parent=self)

    def __len__(self):
        return len(self.sub_catalog)

    def __next__(self):
        if self.index == 0:
            raise StopIteration  # Signal the end of iteration
        self.index -= 1
        return self.sub_catalog[self.index]

    def __iter__(self):
        return iter(self.sub_catalog)

    def __repr__(self):
        return f"Node(name={self.name!r}, id={self.id!r}, parent_id={self.parent_id!r})"


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True, unique=True)
    address = Column(String(100), nullable=False, index=True)
    orders = orm.relationship("Order", back_populates="client")

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELED = "canceled"


class OrderItem(Base):
    __tablename__ = "order_items"
    id : int = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = orm.relationship("Product", back_populates="order_items")
    quantity = Column(Numeric(precision=10, scale=2), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = orm.relationship("Order", back_populates="order_items")

class Order(Base):
    __tablename__ = "orders"

    id : int = Column(Integer, primary_key=True, index=True)

    total_price: orm.Mapped[float] = orm.mapped_column(Numeric(precision=10, scale=2), default=0)
    status: orm.Mapped[OrderStatus] = orm.mapped_column(Enum(OrderStatus))
    created_at: orm.Mapped[datetime] = orm.mapped_column(DateTime(timezone=True), server_default=func.now())
    client_id = Column(Integer, ForeignKey("clients.id"))
    client = orm.relationship("Client", back_populates="orders")
    order_items = orm.relationship("OrderItem", back_populates="order", collection_class=attribute_mapped_collection('id'))

    def append(self, order_item:OrderItem):
        self.order_items[order_item.id] = order_item

    def __getitem__(self, item):
        return self.order_items[item]

    def __setitem__(self, key, value: OrderItem):
        self.order_items[key] = value

    def set_total_price(self, quantity):
        self.total_price = sum(self.order_items[item].product.price * quantity for item in self.order_items)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    catalog_id = Column(Integer, ForeignKey("catalogs.id"))
    catalog = orm.relationship("Catalog", back_populates="products")
    order_items = orm.relationship("OrderItem", back_populates="product")
    count = Column(Integer)

# def get_tree(base_page, dest_dict):
#     dest_dict = { 'title': base_page.title, 'content': base_page.content }
#     children = base_page.children
#     if children:
#         dest_dict['children'] = {}
#         for child in children:
#             get_tree(child, dest_dict)
#     else:
#         return