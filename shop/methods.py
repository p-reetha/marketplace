from flask import session
from shop.db_connection import connect_db
from shop.models import Buyer, Product, Cart

db = connect_db()


def validate_user(buyer_name, mail_id, phone_no, password, confirm):
    if password == confirm:
        obj = Buyer(buyer_name=buyer_name, mail_id=mail_id, phone_no=phone_no, password=password)
        db.add(obj)
        db.commit()
        return 'true'
    else:
        return 'false'


def is_user_exists(mail_id, password):
    buyer = db.query(Buyer).filter_by(mail_id=mail_id, password=password).first()
    if buyer:
        session['buyer_id'] = buyer.buyer_id
        session['buyer_name'] = buyer.buyer_name
        return 'true'
    else:
        return 'false'


def get_categories_list():
    cat_list = db.query(Product.category).group_by(Product.category).all()
    return cat_list


def get_products(category):
    prod_list = db.query(Product).filter_by(category=category, prod_availabity='yes').all()
    return prod_list


def add_product_to_cart(prod_id, quantity):
    buyer_id = session['buyer_id']
    obj = Cart(buyer_id=buyer_id, prod_id=prod_id, quantity=quantity)
    session.add(obj)
    session.commit()
    return 'true'


def products_in_cart():
    buyer_id = session['buyer_id']
    cart_prod_list = db.query(Cart).add_columns(Cart.quantity, Product.category, Product.prod_name, Product.price).filter(Product.prod_id == Cart.prod_id).filter(Cart.buyer_id == buyer_id).all()
    return cart_prod_list


def remove_product_from_cart(cart_item_id):
    buyer_id = session['buyer_id']
    product = db.query(Cart).filter_by(buyer_id=buyer_id, cart_item_id=cart_item_id).one()
    db.delete(product)
    db.commit()
    return 'true'


def update_cart_product_quantity(cart_item_id, quantity):
    buyer_id = session['buyer_id']
    product = db.query(Cart).filter_by(cart_item_id=cart_item_id, buyer_id=buyer_id).one()
    product.quantity = quantity
    db.add(product)
    db.commit()
    return 'true'


def product_to_buy(cart_item_id):
    buyer_id = session['buyer_id']
    product = db.query(Product).filter_by(cart_item_id=cart_item_id, buyer_id=buyer_id).one()
    product.prod_availability = 'no'
    db.add(product)
    db.commit()
    return 'true'
