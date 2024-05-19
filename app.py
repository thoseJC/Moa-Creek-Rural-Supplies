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

from cursor import getCursor
from app_query import get_products_by_ids


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


@app.route("/")
def home():
    return render_template('global/index.html')

@app.route("/cart")
def cart():
    user_id = 0
    if session.get("user_id"):
        user_id = session.get("user_id")
    return render_template('global/cart.html', user_id = user_id)


@app.route("/get_products", methods=["POST"])
def get_products():
    products = []
    try:
        product_ids = request.json.get("product_ids", [])
        cursor = getCursor()
        sql_query = get_products_by_ids(product_ids)
        cursor.execute(sql_query)
        for product in cursor:
            products.append({
                "product_id": product[0],
                "category_id": product[1],
                "name": product[2],
                "description": product[3],
                "price": product[4],
                "pd_image_path": product[5],
                "is_active": product[6]
            })
        cursor.close()
        return products
    except Exception as e:
        print("@app.route(/get_products): %s", e)
        return products


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    session.pop('user_name', None)
    session.pop('user_role', None)
    return redirect(url_for('home'))
