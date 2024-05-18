from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

from customer_query import category_list_query

customer_page = Blueprint("customer", __name__, static_folder="static", template_folder="templates/customer")

@customer_page.route("/dashboard")
def dashboard():
  user = {
    "user_id": session.get("user_id"),
    "user_role": session.get("user_role"),
    "first_name": session.get("first_name"),
    "last_name": session.get("last_name"),
    "order_count": session.get("order_count")
  }
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
