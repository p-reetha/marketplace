from shop import app
from flask import request, render_template, redirect, url_for, flash, session
from shop.methods import*


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        buyer_name = request.form.get('buyer_name')
        mail_id = request.form.get('mail_id')
        phone_no = request.form.get('phone_no')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        sign_up = validate_user(buyer_name, mail_id, phone_no, password, confirm)
        if sign_up == 'true':
            return redirect(url_for('login'))
        else:
            flash("password does not match", "danger")
            return render_template('signup.html')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail_id = request.form.get('mail_id')
        password = request.form.get('password')
        log_in, user_id, user_name = is_user_exists(mail_id, password)
        if log_in == 'true':
            session['buyer_id'] = user_id
            session['buyer_name'] = user_name
            return redirect(url_for('categories'))
        else:
            flash("Incorrect mail-id/password", "danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('home.html')


@app.route('/categories', methods=['GET'])
def categories():
    categories_list = get_categories_list()
    return str(categories_list)


@app.route('/products', methods=['GET'])
def products():
    category = request.form['category']
    list_of_products = get_products(category)
    return str(list_of_products)


@app.route('/cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        prod_id = request.form['prod_id'] # need to pass hidden value of prod_id in UI
        desired_quantity = request.form['desired_quantity']
        buyer_id = session['buyer_id']
        is_product_added = add_product_to_cart(prod_id, desired_quantity, buyer_id)
        if is_product_added == 'true':
            return redirect(url_for('categories'))
        else:
            return is_product_added


@app.route('/cart', methods=['GET'])
def view_cart():
    if request.method == 'GET':
        buyer_id = session['buyer_id']
        products_list = products_in_cart(buyer_id)
        if products_list != 0:
            return products_list
        else:
            return 'cart is empty'


@app.route('/cart', methods=['DELETE'])
def remove_from_cart():
    if request.method == 'DELETE':
        cart_item_id = request.form['cart_item_id']
        buyer_id = session['buyer_id']
        is_product_deleted = remove_product_from_cart(cart_item_id, buyer_id)
        if is_product_deleted == 'true':
            return render_template('cart.html')


@app.route('/cart', methods=['PUT'])
def update_cart():
    if request.method == 'PUT':
        cart_item_id = request.form['cart_item_id']
        desired_quantity = request.form['desired_quantity']
        buyer_id = session['buyer_id']
        is_quantity_updated = update_cart_product_quantity(cart_item_id, desired_quantity, buyer_id)
        if is_quantity_updated == 'true':
            return render_template('cart.html')
        else:
            return is_quantity_updated


@app.route('/buy', methods=['PUT'])
def buy_product():
    if request.method == 'PUT':
        cart_item_id = request.form['cart_item_id']
        desired_quantity = request.form['desired_quantity']
        buyer_id = session['buyer_id']
        is_product_purchased = product_to_buy(cart_item_id, desired_quantity, buyer_id)
        if is_product_purchased == 'true':
            return redirect(url_for('categories'))
        else:
            return is_product_purchased


