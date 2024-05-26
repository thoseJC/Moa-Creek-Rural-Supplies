from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template
from manager_query import get_all_account_holders


manager_page = Blueprint("manager", __name__, static_folder="static", template_folder="templates/manager")

def get_user_info():
  return {
    "user_id": session.get("user_id"),
   "user_role": session.get("user_role"),
   "first_name": session.get("first_name")
  }

@manager_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = get_user_info()
   if session.get('logged_in') != True or user["user_role"] != 'manager':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)

@manager_page.route("/credit_management")
def credit_management():
		user = get_user_info()
		users = []
		try:
			cursor = getCursor()
			sql_query = get_all_account_holders()
			cursor.execute(sql_query)
			results = cursor.fetchall()
			for user in results:
				users.append({
					"user_id": user[0],
					"first_name": user[1],
					"last_name": user[2],
					"credit_apply": user[3]
				})
		except Exception as e:
			print("@app.route(/get_products): %s", e)
			return users
		return render_template("manager/credit_management.html", user=user, users=users)