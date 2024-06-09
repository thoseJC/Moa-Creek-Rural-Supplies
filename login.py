from flask import Blueprint, request,flash, redirect, url_for, jsonify,render_template,session
from cursor import getCursor
from app_query import query_user_when_login, query_product_by_id,register_new_user,update_user_profile_query, get_user_profile_query
from login_helper import redirect_by_role, setUp_session
from auth import hashPassword, getSalt, checkHashingValue

login_page = Blueprint("login_page", __name__, static_folder="static", template_folder="templates/global")


@login_page.route("/", methods=['GET', 'POST'])
def login():
	try:
		err_msg = ""
		if session.get("logged_in") == True:
			user_role = session.get("user_role")
			return redirect_by_role(user_role)
		if request.method == 'POST':
			username = request.form.get('username')
			password = request.form.get('password')
			cursor = getCursor()
			sql_query = query_user_when_login()
			cursor.execute(sql_query, (username,))
			user = cursor.fetchone()
			if user == None:
				return render_template('login.html', err_msg="User Not Exist")
			user_password = user[3]
			user_status = user[4]
				# if checkHashingValue(user_password, user_password):
			if user_password != password:
				return render_template('login.html', err_msg="Password Not Correct")
			if user_status != 1:
					return render_template('login.html', err_msg="Account Suspended")
			setUp_session(user)
			user_role = session.get("user_role")
			return redirect_by_role(user_role)
		else:
			return render_template('login.html', err_msg=err_msg)
	except Exception as e:
		print("@app.route(/login) : %s",e)
		return render_template('login.html', err_msg=e)