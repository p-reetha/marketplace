from shop import app
from flask import request, render_template, redirect, url_for, flash, session
from shop.buyer_model import*
from shop.product_model import*
from shop.cart_model import*


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
        valid_name = validate_name(buyer_name)
        valid_mail_id = validate_mail_id(mail_id)
        valid_phone_no = validate_phone_no(phone_no)
        password_confirmed = confirm_password(password, confirm)
        if valid_name == 'true' and valid_mail_id == 'true' and valid_phone_no == 'true' and password_confirmed == 'true':
            sign_up = save_user(buyer_name, mail_id, phone_no, password)
            if sign_up == 'true':
                return redirect(url_for('login'))
        elif valid_name == 'false':
            flash("Invalid user name", "danger")
            return render_template('signup.html')
        elif valid_mail_id == 'false':
            flash("Invalid mail id", "danger")
            return render_template('signup.html')
        elif valid_phone_no == 'false':
            flash("Invalid phone number", "danger")
            return render_template('signup.html')
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
            return redirect(url_for('get_categories'))
        else:
            flash("Incorrect mail-id/password", "danger")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = get_categories_list()
    return render_template('categories.html', categories_list=categories)


@app.route('/products', methods=['GET'])
def get_products_of_selected_category():
    category = request.args.get('category').lower()
    list_of_products = get_products(category)
    return render_template('products.html', products_list=list_of_products)


@app.route('/addcart', methods=['GET', 'POST'])
def add_to_cart():
    if request.method == 'GET':
        prod_id = request.args.get('prod_id')
        desired_quantity = request.args.get('desired_quantity')
        if desired_quantity == '':
            desired_quantity = 1
        if 'buyer_id' not in session:
            flash('You must login first', 'danger')
            return redirect(url_for('login'))
        buyer_id = session['buyer_id']
        is_product_added = add_product_to_cart(prod_id, desired_quantity, buyer_id)
        session['product_add_status'] = is_product_added
        return '', 204


@app.route('/cart', methods=['GET'])
def view_cart():
    if request.method == 'GET':
        if 'buyer_id' not in session:
            flash('You must login first', 'danger')
            return redirect(url_for('login'))
        buyer_id = session['buyer_id']
        cart_products_list = get_products_in_cart(buyer_id)
        if cart_products_list:
            return render_template('cart.html', cart_prods_list=cart_products_list)
        else:
            flash('Cart is empty!', 'info')
            return render_template('cart.html')
    return render_template('cart.html')


@app.route('/removecart', methods=['GET', 'POST'])
def remove_from_cart():
    if request.method == 'GET':
        prod_id = request.args.get('prod_id')
        buyer_id = session['buyer_id']
        is_product_deleted = remove_product_from_cart(prod_id, buyer_id)
        if is_product_deleted == 'true':
            return redirect(url_for('view_cart'))
    return render_template('cart.html')


@app.route('/updatecart', methods=['GET', 'POST'])
def update_cart():
    if request.method == 'GET':
        buyer_id = session['buyer_id']
        prod_id = request.args.get('prod_id')
        desired_quantity = request.args.get('desired_quantity')
        is_quantity_updated = update_cart_product_quantity(prod_id, desired_quantity, buyer_id)
        session['quantity_update_status'] = is_quantity_updated
        return redirect(url_for('view_cart'))


@app.route('/buy', methods=['GET'])
def check_cart_products_availability():
    if request.method == 'GET':
        buyer_id = session['buyer_id']
        cart_products = get_products_in_cart(buyer_id)
        prods_availability_list = cart_products_availability(cart_products)
        session['availability_list'] = prods_availability_list
        return redirect(url_for('view_cart'))
    return render_template('cart.html')


@app.route('/buy', methods=['PUT'])
def buy_products():
    if request.method == 'PUT':
        buyer_id = session['buyer_id']
        cart_products = get_products_in_cart(buyer_id)
        purchased_products_list = get_products_to_buy(cart_products, buyer_id)
        if not purchased_products_list:
            return redirect(url_for('view_cart', message_to_display="No item is purchased"))
        else:
            return redirect(url_for('view_cart', purchased_prods_list=purchased_products_list))
    return render_template('cart.html')


