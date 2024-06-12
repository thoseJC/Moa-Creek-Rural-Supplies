from flask import Blueprint, flash, redirect, url_for, jsonify,request,render_template,session
from app_query import query_user_when_login, update_user_profile_by_manager
from auth import hashPassword
from cursor import getConection, getCursor
from login_helper import getUserInfo, setUp_session
from flask import render_template
from manager_query import get_all_account_holders, update_customer_credit_apply

from manager_query import get_user_account_info_sql

manager_page = Blueprint("manager", __name__, static_folder="static", template_folder="templates/manager")

def get_user_info():
  return {
    "user_id": session.get("user_id"),
   "user_role": session.get("user_role"),
   "first_name": session.get("first_name")
  }

@manager_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = getUserInfo()
   try:
      if session.get('logged_in') != True or user["user_role"] != 'manager':
         return redirect(url_for('login_page.login'))
      cursor = getCursor()
      cursor.execute("select * from users where user_id = %s", (user["user_id"],))
      user_data = cursor.fetchone()
      return render_template("global/account_dashboard.html", user=user, user_data= user_data)
   except Exception as e:
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
			for result in results:
				credit_apply = result[5]
				if credit_apply is None or credit_apply == 0 or credit_apply == 0.00:
					credit_apply = 0
				users.append({
					"user_id": result[0],
					"first_name": result[1],
					"last_name": result[2],
					"credit_limit": result[3],
					"credit_remaining": result[4],
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


@manager_page.route("/user-account", methods = ['GET', 'POST'])
def manage_user_account():
   valid_user = check_user_role()
   try:
      if not valid_user:
         return redirect(url_for('login_page.login'))
      users_data = get_users_data()
      users = process_users_data(users_data)
      if request.method == 'POST':
         data = request.json
         account_status =  updateAccountStatus(data)
         status = True if account_status == 1 else False
         return jsonify({'success' : True, "new_status" : status})
         
      else:
         return render_template("manage-user-account.html", users = users)
   except Exception as e:
      users_data = get_users_data()
      users = process_users_data(users_data)
      flash('Failed to update user account status.', 'error')  # Flash an error message
      return render_template("manage-user-account.html", users = users , error = e)
   
@manager_page.route("/user-account/<string:user_id>", methods = ['GET', 'POST'])
def manage_user_account_by_id(user_id):
   valid_user = check_user_role()
   msg_obj = {
		"email": "",
		"phone_number": "",
		"success": ""
	}
   try:
      if not valid_user:
         return redirect(url_for('login_page.login'))
      connc = getConection()
      cursor = connc.cursor()
      if request.method == 'POST':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            user_password = hashPassword(request.form.get("first_password")) if request.form.get("first_password") else session.get("password")
            update_user_info = update_user_profile_by_manager()
            cursor.execute(update_user_info, (first_name,last_name,email,phone_number,user_password, user_id))
            connc.commit()
            msg_obj["success"] = "Your profile has been updated successfully!"
      cursor.execute(query_user_when_login(), (user_id,))
      dbUser = cursor.fetchone()
      setUp_session(dbUser)
      user_data = process_user_data(dbUser)
      # update session data : 
      return render_template("manage_user_by_id.html", user = user_data, msg_obj= msg_obj)
   except Exception as e:
      cursor.execute("select * from users where user_id = %s", (user_id,))
      dbUser = cursor.fetchone()
      user_data = process_user_data(dbUser)
      flash('Failed to update user profile.', 'error')  # Flash an error message
      print("def manage_user_account_by_id(user_id): %s",e)
      return render_template("manage_user_by_id.html", user = user_data , error = e,msg_obj= msg_obj)

def get_current_user():
   user = {
      "user_id": session.get("user_id"),
      "user_role": session.get("user_role"),
      "first_name": session.get("first_name"),
      "logged_in" : session.get('logged_in')
   }
   return user

def check_user_role():
   user = get_current_user()
   if user['logged_in'] != True or user["user_role"] != 'manager':
      return False
   else:
      return True

def get_users_data():
   user = get_current_user()
   user_id = user["user_id"]
   try:
      cursor = getCursor()
      if cursor:
         sql = get_user_account_info_sql()
         cursor.execute(sql,(user_id,))
         users = cursor.fetchall()
         cursor.close()
         return users
      else:
           raise Exception("Database connection faild")
   except Exception as e:
      print("manager/get_users_data : %e ",e)

def updateAccountStatus(data):
   connc = getConection()
   try:
      cursor = connc.cursor()
      user_id = data["user_id"]
      is_active = 1 if data["operation"] == 'Activate' else 0
      cursor.execute("update users set status = %s where users.user_id = %s",( is_active,user_id))
      connc.commit()
      cursor.close()
      new_cursor = connc.cursor()
      new_cursor.execute("select status from users where user_id = %s",( user_id,))
      (account_status,) = new_cursor.fetchone()
      new_cursor.close()
      return account_status
   except Exception as err:
      print(f"Error: {err}")
      connc.rollback()
      return None
   finally:
      connc.close()


def process_users_data(users):
   if len(users) > 0:
      processed_user = []
      for user in users:
         new_user = {
            "user_id" : user[0],
            "full_name" : user[1]+" "+user[2],
            "username" : user[3],
            "email": user[4],
            "role" : user[5],
            "is_active": user[6]
         }
         processed_user.append(new_user)
      return processed_user
   else:
      return []
   

def process_user_data(user):
      if user:
         user_obj = {
            "user_id" : user[0],
            "user_role_id" : user[1],
            "first_name" : user[2],
            "last_name" : user[3],
            "login_name" : user[4],
            "email" : user[5],
            "password" : user[8],
            "phone": user[6],
            "acccount_status":user[7],
            "join_date" : user[10]
         }
         return user_obj
      else:
         return None


@manager_page.route('/report_panel')
def report_panel():
    connection = getCursor()
  
    # inventory data
    connection.execute("SELECT * FROM inventory")
    inventory_data = connection.fetchall()
    x_invt_qty= [row[1] for row in inventory_data]
    y_invt_id = [row[0] for row in inventory_data]
    invt_data = {
        'x_invt_qty': x_invt_qty,
        'y_invt_id': y_invt_id
    }
    
    # orders data
    connection.execute("SELECT status, COUNT(order_id) as order_count FROM orders GROUP BY status;")
    orders_data = connection.fetchall()
    x_odrs_status = [row[0] for row in orders_data]
    y_odrs_qty = [row[1] for row in orders_data]
    odrs_data = {
        'x_odrs_status': x_odrs_status,
        'y_odrs_qty': y_odrs_qty
    }
    
    # payment data
    connection.execute("SELECT DATE_FORMAT(paid_date, '%Y-%m-%d') as month, SUM(total) as total FROM payment GROUP BY month;")
    payment_data = connection.fetchall()
    x_pyt_date = [row[0] for row in payment_data]
    y_pyt_total = [row[1] for row in payment_data]
    pyt_data = {
        'x_pyt_date': x_pyt_date,
        'y_pyt_total': y_pyt_total
    }
    
    # shipments data
    connection.execute("SELECT status, COUNT(shipment_id) as shipment_count FROM shipments GROUP BY status;")
    shipments_data = connection.fetchall()
    x_spm_status = [row[0] for row in shipments_data]
    y_spm_qty = [row[1] for row in shipments_data]
    spm_data = {
        'x_spm_status': x_spm_status,
        'y_spm_qty': y_spm_qty
    }

    return jsonify({
        'inventory': invt_data,
        'orders': odrs_data,
        'payment': pyt_data,
        'shipments': spm_data
    })


@manager_page.route('/web_report')
def web_report():
    return render_template("/report_panel.html")


