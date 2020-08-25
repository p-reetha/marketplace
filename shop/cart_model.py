from shop.db_connection import connect_db
from shop.buyer_model import Buyer
from shop.product_model import Product
from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
products_in_cart = []
products_availability_list = []
purchased_products = []

db = connect_db()


class Cart(Base):
    __tablename__ = 'carts'
    cart_item_id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey(Buyer.buyer_id))
    prod_id = Column(Integer, ForeignKey(Product.prod_id)) # 'products.prod_id'
    desired_quantity = Column(Integer, unique=False, nullable=False)


def add_product_to_cart(prod_id, desired_quantity, buyer_id):
    obj = Cart(buyer_id=buyer_id, prod_id=prod_id, desired_quantity=desired_quantity)
    product = db.query(Product).filter_by(prod_id=prod_id).one()
    if product.prod_quantity < int(desired_quantity):
        return str(product.prod_quantity) + ' items only available'
    db.add(obj)
    db.commit()
    return 'true'


def get_products_in_cart(buyer_id):
    cart_products_list = db.query(Cart).add_columns(Product.category, Product.prod_name, Product.price, Product.seller).filter(Product.prod_id == Cart.prod_id).filter(Cart.buyer_id == buyer_id).all()
    for product in cart_products_list:
        product_dict = {
            "prod_id": product[0].prod_id,
            "category": product[1],
            "prod_name": product[2],
            "prod_price": product[3],
            "prod_seller": product[4],
            "desired_quantity": product[0].desired_quantity}
        products_in_cart.append(product_dict)
    return products_in_cart


def remove_product_from_cart(prod_id, buyer_id):
    product = db.query(Cart).filter_by(buyer_id=buyer_id, prod_id=prod_id).one()
    db.delete(product)
    db.commit()
    return 'true'


def update_cart_product_quantity(prod_id, desired_quantity, buyer_id):
    cart = db.query(Cart).filter_by(buyer_id=buyer_id, prod_id=prod_id).one()
    product = db.query(Product).filter_by(prod_id=prod_id).one()
    if product.prod_quantity < int(desired_quantity):
        return str(product.prod_quantity) + ' items only available'
    cart.desired_quantity = desired_quantity
    db.add(cart)
    db.commit()
    return 'true'


def cart_products_availability(cart_products):
    for cart_product in cart_products:
        product = db.query(Product).filter_by(prod_id=cart_product['prod_id']).one()
        if product.prod_quantity == 0:
            product_availability_dict = {
                "product_name": product.prod_name,
                "availability": "Not available"
            }
        elif product.prod_quantity < cart_product['desired_quantity']:
            product_availability_dict = {
                "product_name": product.prod_name,
                "availability": str(product.prod_quantity) + ' items only available'
            }
        else:
            product_availability_dict = {
                "product_name": product.prod_name,
                "availability": "Available"
            }
        products_availability_list.append(product_availability_dict)
    return products_availability_list


def get_products_to_buy(cart_products, buyer_id):
    for cart_product in cart_products:
        product = db.query(Product).filter_by(prod_id=cart_product['prod_id']).one()
        if product.prod_quantity > cart_product['desired_quantity']:
            product.prod_quantity -= cart_product['desired_quantity']
            remove_product_from_cart(cart_product['prod_id'], buyer_id)
            if product.prod_quantity == 0:
                product.prod_availability = 'no'
            db.add(product)
            db.commit()
            purchased_products.append(cart_product['prod_name'] + ' - ' + cart_product['category'])
    return purchased_products
