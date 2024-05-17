from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session,request
from app_query import register_new_user
from auth import hashPassword
from cursor import getCursor
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
				cursor.execute(register_query
				, (first_name, last_name, username, email, phone_number, password, address))

				flash('Registration successful!')
				return redirect(url_for('login'))
			except Exception as e:
				flash(f'Registration failed: {str(e)}', 'error')
				return render_template('register.html', error=str(e))
			finally:
				cursor.close()  

		return render_template('register.html')
	except Exception as e:
		print("@app.route('/register'): %s",e)
		return render_template('register.html', error_msg = e)