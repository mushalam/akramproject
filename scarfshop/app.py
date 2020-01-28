from __future__ import print_function
import json
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, session
from jinja2 import Template
import SQLdb



app = Flask(__name__)
# app = Flask(__name__, template_folder='/scarfshop/templates', static_url_path='/scarfshop/static')
app.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343644'


# Decorators #
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
# End of decorators #


# Routes #
@app.route('/')
def shop_main():
    return render_template('shop-index.html')


@app.route('/item')
def shop_item():
    return render_template('shop-item.html')


@app.route('/product-list')
def shop_product_list():
    return render_template('shop-product-list.html')


@app.route('/contacts')
def shop_contacts():
    return render_template('shop-contacts.html')


@app.route('/account')
@login_required
def shop_account():
    return render_template('shop-account.html')


@app.route('/cart')
def shop_cart():
    return render_template('shop-shopping-cart.html')


@app.route('/faq')
def shop_faq():
    return render_template('shop-faq.html')


@app.route('/about')
def shop_about():
    return render_template('shop-about.html')


@app.route('/tc')
def shop_tc():
    return render_template('shop-contacts.html')


@app.route('/privp')
def shop_privp():
    return render_template('shop-privacy-policy.html')


@app.route('/prod-l-w')
def shop_prod_w():
    return render_template('shop-product-list-women.html')


@app.route('/prod-l-k')
def shop_prod_k():
    return render_template('shop-product-list-Kids.html')


@app.route('/pass-reset')
def shop_pass_reset():
    return render_template('forgot-password.html')

# End of routes #


# Login, logout, and registration #
@app.route('/checkout', methods=['GET', 'POST'])
# source: https://codeshack.io/login-system-python-flask-mysql/#creatingtheloginsystem
def shop_checkout():
    error = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_username = request.form['username']
        user_password = request.form['password']
        user_retrieved = SQLdb.get_users(user_username, user_password)
        cursor = SQLdb.get_users(user_username, user_password)

        if user_retrieved:
            print("line112:" + str(user_retrieved))
            # query: cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', ('as', 'as'))
            #is None for invalid password username

            # query: cursor.execute('SELECT * FROM tblCustomer WHERE email = %s AND password = %s', ('andrew.clarkson@yahoo.com', 'password2'))
            # is account is: ('andrew.clarkson@yahoo.com', 'password2', 'Andrew', 'Johnson', datetime.date(1984, 10, 3)) for retrieved
            print(session.keys())

            session['id'] = user_retrieved[5]
            session['username'] = user_retrieved[0]
            session['logged_in'] = True
            return redirect(url_for('shop_main'))
        else:
            error = 'Invalid credentials. Please, try again.'
    return render_template('shop-checkout.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('shop_main'))


@app.route('/registration')
def registration():
    return render_template('registration.html')



# End of login and registration #




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8089)

