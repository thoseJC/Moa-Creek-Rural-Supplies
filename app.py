from flask import Flask
from flask import render_template
app = Flask(__name__)
from auth import hashPassword, getSalt, checkHashingValue
from cursor import getCursor
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from manager import manager_page
from customer import customer_page
from admin import admin_page
from staff import staff_page

app.register_blueprint(manager_page, url_prefix="/manager")
app.register_blueprint(customer_page, url_prefix="/customer")
app.register_blueprint(admin_page, url_prefix="/admin")
app.register_blueprint(staff_page, url_prefix="/staff")


@app.route("/")
def home():
    return render_template('global/index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
	err_msg = ""
	if session.get("logged_in") == True:
		user_role = session.get("user_role")
		if user_role == 'manager':
			return redirect(url_for('manager.dashboard'))
		elif user_role == 'customer':
			return redirect(url_for('customer.dashboard'))
		elif user_role == 'admin':
			return redirect(url_for('admin.dashboard'))
		elif user_role == 'staff':
			return redirect(url_for('staff.dashboard'))
	
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		cursor = getCursor()
		sql_query = """
			SELECT 
				users.role_id, 
				users.username, 
				users.password, 
				users.status, 
				user_roles.role_name
			FROM users
			JOIN user_roles ON users.role_id = user_roles.role_id
			WHERE users.username = %s;
		"""
		cursor.execute(sql_query, (username,))
		user = cursor.fetchone()
		if user is not None:
			user_password = user[2]
			user_status = user[3]
			# if checkHashingValue(user_password, user_password):
			if user_password == password:
				if user_status == 1:
					session["user_id"] = user[0]
					session["logged_in"] = True
					session["user_name"] = user[1]
					session["user_role"] = user[4]
					user_role = session.get("user_role")
					if user_role == 'manager':
						return redirect(url_for('manager.dashboard'))
					elif user_role == 'customer':
						return redirect(url_for('customer.dashboard'))
					elif user_role == 'admin':
						return redirect(url_for('admin.dashboard'))
					elif user_role == 'staff':
						return redirect(url_for('staff.dashboard'))
				else:
					err_msg = "Your account is suspended, please contact the web administrator!"
			else:
				err_msg = "Incorrect password, please try again!"
		else:
			err_msg = "The account doesn't exist, please check!"
	return render_template('global/login.html', err_msg=err_msg)


@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('logged_in', None)
	session.pop('user_name', None)
	session.pop('user_role', None)
	return redirect(url_for('home'))
