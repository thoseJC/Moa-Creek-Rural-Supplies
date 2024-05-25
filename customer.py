from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template
from customer_query import get_credit_fields

from customer_query import category_list_query

customer_page = Blueprint("customer", __name__, static_folder="static", template_folder="templates/customer")

def get_user_info():
  return {
    "user_id": session.get("user_id"),
    "user_role": session.get("user_role"),
    "first_name": session.get("first_name"),
    "last_name": session.get("last_name"),
    "order_count": session.get("order_count")
  }

@customer_page.route("/dashboard")
def dashboard():
  user = get_user_info()
  if session.get('logged_in') != True or user["user_role"] != 'customer':
    return redirect(url_for('login_page.login'))
  return render_template("global/account_dashboard.html", user=user)

@customer_page.route("/categories")
def categories():
    connection = getCursor()
    sql_query = category_list_query()
    connection.execute(sql_query)
    categories_list = connection.fetchall()

    return render_template("global/categories.html", categories_list=categories_list)

@customer_page.route("/credit")
def credit():
  user = get_user_info()
  credit_obj = {
    "credit_limit": 0,
    "credit_remaining": 0,
    "credit_apply": 0,
    "limit_alert": False
  }
  if not user["user_id"]:
    return redirect(url_for('login_page.login'))
  
  cursor = getCursor()
  try:
    cursor.execute(get_credit_fields(), (user['user_id'],))
    result = cursor.fetchone()
    if result:
      limit_alert = False
      if float(result[1]) <= 50:
        limit_alert = True
      credit_obj = {
        "credit_limit": result[0],
        "credit_remaining": result[1],
        "credit_apply": result[2],
        "limit_alert": limit_alert
      }
  except Exception as e:
    print(f"Database query failed: {e}")
    return "An error occurred", 500
  return render_template("credit.html", user=user, credit_obj=credit_obj)