from shop.db_connection import connect_db
from shop.models import Buyer, Product, Cart
dictionaries_list = []

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
        return 'true', buyer.buyer_id, buyer.buyer_name
    else:
        return 'false', None, None


def get_categories_list():
    cat_list = db.query(Product.category).group_by(Product.category).all()
    return cat_list


def get_products(category):
    global product_dict
    prod_list = db.query(Product).filter_by(category=category, prod_availability='yes').all()
    for product in prod_list:
        product_dict = {
            "prod_id": product.prod_id,
            "category": product.category,
            "prod_name": product.prod_name,
            "prod_price": product.price,
            "prod_seller": product.seller,
            "prod_quantity": product.prod_quantity,
            "prod_availability": product.prod_availability}
        dictionaries_list.append(product_dict)
    return dictionaries_list


def add_product_to_cart(prod_id, desired_quantity, buyer_id):
    obj = Cart(buyer_id=buyer_id, prod_id=prod_id, desired_quantity=desired_quantity)
    product = db.query(Product).filter_by(prod_id=prod_id).one()
    if product.prod_quantity < int(desired_quantity):
        return str(product.prod_quantity) + ' items only available'
    db.add(obj)
    db.commit()
    return 'true'


def products_in_cart(buyer_id):
    cart_prod_list = db.query(Cart).add_columns(Cart.desired_quantity, Product.category, Product.prod_name, Product.price).filter(Product.prod_id == Cart.prod_id).filter(Cart.buyer_id == buyer_id).all()
    return cart_prod_list


def remove_product_from_cart(cart_item_id, buyer_id):
    product = db.query(Cart).filter_by(buyer_id=buyer_id, cart_item_id=cart_item_id).one()
    db.delete(product)
    db.commit()
    return 'true'


def update_cart_product_quantity(cart_item_id, desired_quantity, buyer_id):
    cart = db.query(Cart).filter_by(cart_item_id=cart_item_id, buyer_id=buyer_id).one()
    prod_id = cart.prod_id
    product = db.query(Product).filter_by(prod_id=prod_id).one()
    if product.prod_quantity < int(desired_quantity):
        return str(product.prod_quantity) + ' items only available'
    cart.desired_quantity = desired_quantity
    db.add(cart)
    db.commit()
    return 'true'


def product_to_buy(cart_item_id, desired_quantity, buyer_id):
    cart = db.query(Cart).filter_by(cart_item_id=cart_item_id, buyer_id=buyer_id).one()
    prod_id = cart.prod_id
    product = db.query(Product).filter_by(prod_id=prod_id).one()
    if product.prod_quantity == 0:
        product.prod_availability = 'no'
        db.add(product)
        db.commit()
        return 'stock is not available'
    elif product.prod_quantity < desired_quantity:
        return str(product.prod_quantity) + ' items only available'
    else:
        product.prod_quantity -= int(desired_quantity)
        if product.prod_quantity == 0:
            product.prod_quantity = 'no'
        db.add(product)
        db.commit()
        return 'true'
