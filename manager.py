from flask import Blueprint, flash, redirect, url_for, jsonify, request
from cursor import getCursor
from flask import session
from flask import render_template
from manager_query import get_all_account_holders, update_customer_credit_apply


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
				credit_apply = user[5]
				if credit_apply is None or credit_apply == 0 or credit_apply == 0.00:
					credit_apply = 0
				users.append({
					"user_id": user[0],
					"first_name": user[1],
					"last_name": user[2],
					"credit_limit": user[3],
					"credit_remaining": user[4],
					"credit_apply": credit_apply
				})
		except Exception as e:
			print("@manager_page.route(/get_products): %s", e)
			return users
		return render_template("manager/credit_management.html", user=user, users=users)

@manager_page.route("/update_credit_apply", methods=["POST"])
def update_credit_apply():
	try:
		user_id = request.json.get("user_id")
		credit_limit = float(request.json.get("credit_limit", 0))
		credit_remaining = float(request.json.get("credit_remaining", 0))
		credit_apply = float(request.json.get("credit_apply", 0))

		new_credit_remaining = credit_remaining + (credit_apply - credit_limit)
		cursor = getCursor()
		sql_query = update_customer_credit_apply()
		cursor.execute(sql_query, (-1, new_credit_remaining, credit_apply, user_id))
		return jsonify({'message': 'Credit Limit Updated successfully'}), 200
	except Exception as e:
		print("@manager_page.route(/update_credit_apply): %s", e)
		return jsonify({'message': 'Credit Limit Updated Error'}), 400
	finally:
		cursor.close()

