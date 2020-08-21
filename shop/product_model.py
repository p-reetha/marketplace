from shop.db_connection import connect_db
from sqlalchemy import Integer, String, Column
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
products_list = []

db = connect_db()


class Product(Base):
    __tablename__ = 'products'
    prod_id = Column(Integer, primary_key=True)
    category = Column(String(20), unique=False, nullable=False)
    prod_name = Column(String(30), unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False)
    seller = Column(String(50), unique=False, nullable=False)
    prod_quantity = Column(Integer, unique=False)
    prod_availability = Column(String(10), unique=False, nullable=False)


def get_categories_list():
    cat_list = db.query(Product.category).group_by(Product.category).all()
    return cat_list


def get_products(category):
    prod_list = db.query(Product).filter_by(category=category, prod_availability='yes').all()
    for product in prod_list:
        product_dict = {
            "prod_id": product.prod_id,
            "category": product.category,
            "prod_name": product.prod_name,
            "prod_price": product.price,
            "prod_seller": product.seller,
            "prod_quantity": product.prod_quantity}
        products_list.append(product_dict)
    return products_list
