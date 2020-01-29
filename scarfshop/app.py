from __future__ import print_function
import json
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, url_for, redirect, session, flash
from jinja2 import Template
import SQLdb
from forms import ContactForm
from flask_mail import Message, Mail

mail = Mail()


app = Flask(__name__)
# app = Flask(__name__, template_folder='/scarfshop/templates', static_url_path='/scarfshop/static')
app.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343644'
app.jinja_env.filters['zip']=zip
shipping_cost=6.00

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'akramscarfsup@gmail.com'
app.config["MAIL_PASSWORD"] = 'Brunel123'

def pull_data():
    cart_items = SQLdb.get_cart_details()
    print(cart_items)
    temp_list = []
    total = 0.00
    for item in cart_items:
        total = round(total + float(item[2]),2)
    entries = len(cart_items)
    for cart_item in cart_items:
        temp_list.append(SQLdb.get_product_by_id(int(cart_item[0])))
    print(temp_list[0])

    return cart_items,temp_list,total,entries

mail.init_app(app)

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
@app.route('/', methods=['GET', 'POST'])
def shop_main():
    cart_items, temp_list, total, entries = pull_data()
    return render_template('shop-index.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/item')
def shop_item():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-item.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/product-list', methods=['POST','GET'])
def shop_product_list():
    cart_items, temp_list, total, entries=pull_data()
    product_list=SQLdb.get_all_products()
    if request.method=='POST':
        temp_id=request.form['prodID']
        prod=SQLdb.get_product_by_id(int(temp_id))
        SQLdb.add_product_to_cart(prod)

    return render_template('shop-product-list.html', items=cart_items,t_items=temp_list,total=total,entries=entries, products=product_list)


@app.route('/contacts', methods=['GET', 'POST'])
def shop_contacts():
    cart_items, temp_list, total, entries=pull_data()

    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('shop-contacts.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
            msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('shop-contacts.html', success=True,items=cart_items, t_items=temp_list, total=total, entries=entries)

    elif request.method == 'GET':
        return render_template('shop-contacts.html', form=form,items=cart_items, t_items=temp_list, total=total, entries=entries)
    return render_template('shop-contacts.html', items=cart_items, t_items=temp_list, total=total, entries=entries)

@app.route('/account')
@login_required
def shop_account():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-account.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/cart', methods=['GET', 'POST'])
def shop_cart():
    cart_items, temp_list, total, entries=pull_data()
    total_cost=total+shipping_cost
    if request.method =='POST':
        a=request.form['quantity']
        b=request.form['prodID']
        #print(str(a))
        SQLdb.update_cart(int(b),int(a))
        if request.form['del']=='true':
            SQLdb.delete_cart_entry(int(b))
            redirect(url_for('shop_cart'))


    return render_template('shop-shopping-cart.html',items=cart_items,t_items=temp_list,total=total,entries=entries,t_cost=total_cost,ship=shipping_cost)


@app.route('/faq')
def shop_faq():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-faq.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/about')
def shop_about():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-about.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/tc')
def shop_tc():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-contacts.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/privp')
def shop_privp():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-privacy-policy.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/prod-l-w')
def shop_prod_w():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-product-list-women.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/prod-l-k')
def shop_prod_k():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('shop-product-list-Kids.html', items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/pass-reset')
def shop_pass_reset():
    cart_items, temp_list, total, entries=pull_data()
    return render_template('forgot-password.html',items=cart_items,t_items=temp_list,total=total,entries=entries)

# End of routes #


# Login, logout, and registration #
@app.route('/checkout', methods=['GET', 'POST'])
# source: https://codeshack.io/login-system-python-flask-mysql/#creatingtheloginsystem
def shop_checkout():
    cart_items, temp_list, total, entries = pull_data()
    error = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        user_username = request.form['username']
        user_password = request.form['password']
        user_retrieved = SQLdb.get_users(user_username, user_password)

        if user_retrieved:

            session['id'] = user_retrieved[5]
            session['username'] = user_retrieved[0]
            session['logged_in'] = True

            return redirect(url_for('shop_main'))
        else:
            error = 'Invalid credentials. Please, try again.'
    return render_template('shop-checkout.html', error=error,items=cart_items,t_items=temp_list,total=total,entries=entries)


@app.route('/logout')
@login_required
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('shop_main'))


@app.route('/registration')
def registration():
    return render_template('registration.html')


# End of login and registration #




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8089)

