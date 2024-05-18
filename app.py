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
from app_query import query_product_by_id,register_new_user,update_user_profile_query, get_user_profile_query


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


@app.route('/product/<int:product_id>')
def show_product(product_id):
	cursor = getCursor()
	sql_query = query_product_by_id()
	cursor.execute(sql_query, (product_id,))
	fetched_product = cursor.fetchone()
	product = {
		"id":fetched_product[0],
		"name": fetched_product[1],
		"description": fetched_product[2],
		"price": fetched_product[3],
		"image": fetched_product[4],
		"category": fetched_product[5],
		"active": fetched_product[6]

	}

	return render_template('product/product_info.html',product = product)
 
 

@app.route('/register', methods=['GET', 'POST'])
def register():
	try:
		if request.method == 'POST':
			username = request.form.get('username')
			first_name = request.form.get('firstName')
			last_name = request.form.get('lastName')
			email = request.form.get('email')
			password = request.form.get('password')
			phone_number = request.form.get('phoneNumber') or None
			address = request.form.get('address') or None

			if not is_valid_email(email):
				return render_template('global/register.html', error="Invalid email format.")
			if phone_number and not is_valid_phone_number(phone_number):
				return render_template('global/register.html', error="Invalid phone number format.")

			hashed_password = hashPassword(password)
			cursor = getCursor()
			register_query = register_new_user()

			try:
				cursor.execute(register_query
				, (first_name, last_name, username, email, phone_number, password, address))

				flash('Registration successful!')
				return redirect(url_for('login'))
			except Exception as e:
				flash(f'Registration failed: {str(e)}', 'error')
				return render_template('global/register.html', error=str(e))
			finally:
				cursor.close()  

		return render_template('global/register.html')
	except Exception as e:
		print("@app.route('/register'): %s",e)
		return render_template('global/register.html', error_msg = e)