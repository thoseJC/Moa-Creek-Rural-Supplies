from flask import Flask,session,request,redirect,url_for,flash,render_template
app = Flask(__name__)
from auth import hashPassword, getSalt, checkHashingValue
from cursor import getCursor
from validation import is_valid_email, is_valid_phone_number
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

# import query function 
from app_query import register_new_user,update_user_profile_query, get_user_profile_query


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

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', None)
    session.pop('user_name', None)
    session.pop('user_role', None)
    return redirect(url_for('home'))




 
