from flask import Flask,session,redirect,url_for,render_template,request
app = Flask(__name__)
from manager import manager_page
from customer import customer_page
from admin import admin_page
from staff import staff_page
from product import product_page
from order import order_page
from message import message_page
from login import login_page
from register import register_page
from user_profile import profile_page
# from inventory import inventory_page
from cart import cart_page
from promotion import promotion_page
from news import news_page, get_news_list
from checkout import checkout_page
from account_holder import account_holder
from shippingaddress import shipping_address
from manage_account_apply import manage_account_apply_page

app.register_blueprint(manager_page, url_prefix="/manager")
app.register_blueprint(customer_page, url_prefix="/customer")
app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(staff_page, url_prefix="/staff")
app.register_blueprint(product_page, url_prefix="/product")
app.register_blueprint(order_page, url_prefix="/order")
app.register_blueprint(message_page, url_prefix="/message")
app.register_blueprint(login_page, url_prefix="/login")
app.register_blueprint(register_page, url_prefix="/register")
app.register_blueprint(profile_page, url_prefix="/profile")
# app.register_blueprint(inventory_page, url_prefix="/inventory")
app.register_blueprint(cart_page, url_prefix="/cart")
app.register_blueprint(checkout_page, url_prefix="/checkout")
app.register_blueprint(shipping_address, url_prefix="/shipping")
app.register_blueprint(promotion_page, url_prefix="/promotion")
app.register_blueprint(news_page, url_prefix="/news")
app.register_blueprint(account_holder, url_prefix='/account_holder')
app.register_blueprint(manage_account_apply_page, url_prefix="/manage_account_apply")

@app.route("/")
def home():
    news_list = get_news_list()
    return render_template('global/index.html', latest_news=news_list)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    session.pop('user_name', None)
    session.pop('user_role', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)