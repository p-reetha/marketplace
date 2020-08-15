from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Buyer(Base):
    __tablename__ = 'buyers'
    buyer_id = Column(Integer, primary_key=True)
    buyer_name = Column(String(30), unique=False, nullable=False)
    mail_id = Column(String(120), unique=True, nullable=False)
    phone_no = Column(String(15), unique=True, nullable=False)
    password = Column(String(20), unique=True, nullable=False)


class Product(Base):
    __tablename__ = 'products'
    prod_id = Column(Integer, primary_key=True)
    category = Column(String(20), unique=False, nullable=False)
    prod_name = Column(String(30), unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False)
    seller = Column(String(50), unique=False, nullable=False)
    prod_quantity = Column(Integer, unique=False)
    prod_availability = Column(String(10), unique=False, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'
    cart_item_id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('buyers.buyer_id'))
    prod_id = Column(Integer, ForeignKey('products.prod_id'))
    desired_quantity = Column(Integer, unique=False, nullable=False)
