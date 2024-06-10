import uuid
from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session,request
from app_query import query_user_when_login, register_new_user, add_address_to_new_user
from auth import hashPassword
from cursor import getCursor
from login_helper import redirect_by_role, setUp_session
from validation import is_valid_email, is_valid_phone_number

register_page = Blueprint("register_page", __name__, static_folder="static", template_folder="templates/global")

@register_page.route('/', methods=['GET', 'POST'])
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
				return render_template('register.html', error="Invalid email format.")
			if phone_number and not is_valid_phone_number(phone_number):
				return render_template('register.html', error="Invalid phone number format.")

			hashed_password = hashPassword(password)
			cursor = getCursor()
			register_query = register_new_user()

			try:
				new_user_id = str(uuid.uuid4())
				cursor.execute(
					register_query, 
					(
						new_user_id, 
						first_name, 
						last_name, 
						username, 
						email, 
						phone_number, 
						password
					)
				)

				add_address_to_new_user_query = add_address_to_new_user()
				cursor.execute(
					add_address_to_new_user_query, 
					(
						new_user_id, 
						address, 
						'', 
						'', 
						'', 
						''
					)
				)
				
				# get user info from db
				sql_query = query_user_when_login()
				cursor.execute(sql_query, (username,))
				new_user = cursor.fetchone()
				if new_user:
					setUp_session(new_user)
					flash('Registration successful!')
					user_role = session.get("user_role")
					return redirect_by_role(user_role)
				else:
					return redirect(url_for('login_page.login'))
			except Exception as e:
				flash(f'Registration failed: {str(e)}', 'error')
				return render_template('register.html', error=str(e))
			finally:
				cursor.close()  

		return render_template('register.html')
	except Exception as e:
		print("@app.route('/register'): %s",e)
		return render_template('register.html', error_msg = e)