from flask import Flask
from flask import render_template
app = Flask(__name__)
from auth import hashPassword, getSalt, checkHashingValue
from cursor import getCursor
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from validation import is_valid_email, is_valid_phone_number

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
				u.user_id,
				u.role_id, 
				u.username, 
				u.password, 
				u.status, 
				ur.role_name,
				u.first_name,
				u.last_name,
				COUNT(o.order_id) AS order_count
			FROM 
				users u
			JOIN 
    		user_roles ur ON u.role_id = ur.role_id
			LEFT JOIN 
    		orders o ON u.user_id = o.user_id
			WHERE 
    		u.username = %s;
		"""
		cursor.execute(sql_query, (username,))
		user = cursor.fetchone()
		if username == '' or password == '':
			err_msg = "Please fill update the login form!"
		elif user is not None:
			user_password = user[3]
			user_status = user[4]
			# if checkHashingValue(user_password, user_password):
			if user_password == password:
				if user_status == 1:
					session["user_id"] = user[0]
					session["logged_in"] = True
					session["user_name"] = user[2]
					session["user_role"] = user[5]
					session["first_name"] = user[6]
					session["last_name"] = user[7]
					session["order_count"] = user[8]
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

@app.route('/manage-own-profile', methods=['GET', 'POST'])
def manage_own_profile():
	msg_obj = {
		"email": "",
		"phone_number": "",
		"success": ""
	}
	user_id = session.get("user_id")
	cursor = getCursor()

	if request.method == 'POST':
		first_name = request.form.get('first_name')
		last_name = request.form.get('last_name')
		email = request.form.get('email')
		phone_number = request.form.get('phone_number')
		user = (first_name, last_name, email, phone_number)
		check_status = True
		if email and is_valid_email(email) != True:
			check_status = False
			msg_obj["email"] = "Please enter a correct email address!"
		if phone_number and is_valid_phone_number(phone_number) != True:
			check_status = False
			msg_obj["phone_number"] = "Please enter a correct phone number!"
		if check_status:
			sql_query = """
				UPDATE 
					users
				SET 
					first_name = %s,
					last_name = %s,
					email = %s,
					phone_number = %s
				WHERE
					user_id = %s;
			"""
			cursor.execute(sql_query, (first_name, last_name, email, phone_number, user_id,))
			msg_obj["success"] = "Your profile has been updated successfully!"

	else:
		sql_query = """
			SELECT 
				first_name,
				last_name,
				email,
				phone_number
			FROM users
			WHERE user_id = %s;
		"""
		cursor.execute(sql_query, (user_id,))
		user = cursor.fetchone()

	return render_template('global/manage_own_profile.html',
		user=user, 
		msg_obj=msg_obj)
 
 

@app.route('/register', methods=['GET', 'POST'])
def register():
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

        try:
            cursor.execute("""
                INSERT INTO users (user_id, role_id, first_name, last_name, username, email, phone_number, loyalty_points, password, address, status)
                VALUES (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), %s, %s, %s, %s, %s, 0, %s, %s, TRUE)
            """, (first_name, last_name, username, email, phone_number, password, address))

            flash('Registration successful!')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('global/register.html', error=str(e))
        finally:
            cursor.close()  

    return render_template('global/register.html')