from flask import Blueprint, flash, redirect, url_for, jsonify,request
from cursor import getConection, getCursor
from flask import session
from flask import render_template

from manager_query import get_user_account_info_sql





manager_page = Blueprint("manager", __name__, static_folder="static", template_folder="templates/manager")

@manager_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = {
      "user_id": session.get("user_id"),
      "user_role": session.get("user_role"),
      "first_name": session.get("first_name")
   }
   if session.get('logged_in') != True or user["user_role"] != 'manager':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)

@manager_page.route("/user-account", methods = ['GET', 'POST'])
def manage_user_account():
   valid_user = check_user_role()
   try:
      if not valid_user:
         return redirect(url_for('login_page.login'))
      user = get_current_user()
      users_data = get_account_user()
      users = process_user_data(users_data)
      if request.method == 'POST':
         print("request")
         print(request.json)
         data = request.json;
         account_status =  updateAccountStatus(data)
         status = True if account_status == 1 else False
         return jsonify({'success' : True, "new_status" : status})
         
      else:
         return render_template("manage-user-account.html", users = users)
   except Exception as e:
      users_data = get_account_user()
      users = process_user_data(users_data)
      users.paginate()
      return render_template("manage-user-account.html", users = users , error = e)

def get_current_user():
   user = {
      "user_id": session.get("user_id"),
      "user_role": session.get("user_role"),
      "first_name": session.get("first_name"),
      "logged_in" : session.get('logged_in')
   }
   return user;

def check_user_role():
   user = get_current_user();
   if user['logged_in'] != True or user["user_role"] != 'manager':
      return False;
   else:
      return True;

def get_account_user():
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
      print("manager/get_account_user : %e ",e)

def updateAccountStatus(data):
   connc = getConection()
   try:
      cursor = connc.cursor()
      user_id = data["user_id"]
      is_active = 1 if data["operation"] == 'Activate' else 0;
      cursor.execute("update users set status = %s where users.user_id = %s",( is_active,user_id))
      connc.commit()
      cursor.close()
      new_cursor = connc.cursor()
      new_cursor.execute("select status from users where user_id = %s",( user_id,))
      (account_status,) = new_cursor.fetchone();
      new_cursor.close()
      return account_status
   except Exception as err:
      print(f"Error: {err}")
      connc.rollback()
      return None
   finally:
      connc.close()


def process_user_data(users):
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



