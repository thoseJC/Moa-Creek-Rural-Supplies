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

@app.route('/manage-own-profile', methods=['GET', 'POST'])
def manage_own_profile():
	msg_obj = {
		"email": "",
		"phone_number": "",
		"success": ""
	}
	try:
		user_id = session.get("user_id")
		cursor = getCursor()

		if request.method == 'POST':
			first_name = request.form.get('first_name')
			last_name = request.form.get('last_name')
			email = request.form.get('email')
			phone_number = request.form.get('phone_number')
			user_password = request.form.get("first_password")
			print("password : %s", user_password)
			user = (first_name, last_name, email, phone_number)
			check_status = True
			if email and is_valid_email(email) != True:
				check_status = False
				msg_obj["email"] = "Please enter a correct email address!"
			if phone_number and is_valid_phone_number(phone_number) != True:
				check_status = False
				msg_obj["phone_number"] = "Please enter a correct phone number!"
			if check_status:
				sql_query = update_user_profile_query()
				cursor.execute(sql_query, (first_name, last_name, email, phone_number, user_id,))
				msg_obj["success"] = "Your profile has been updated successfully!"

		else:
			sql_query = get_user_profile_query()
			cursor.execute(sql_query, (user_id,))
			user = cursor.fetchone()

		return render_template('global/manage_own_profile.html',
			user=user, 
			msg_obj=msg_obj)
	except Exception as e:
		print("def manage_own_profile(): %s", e)
		return render_template('global/manage_own_profile.html',user=user, msg_obj=msg_obj, error_msg = e)
 

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