from flask import Blueprint, flash, redirect, url_for, jsonify, session, render_template, request
from cursor import getCursor

from login_helper import getUserInfo
from staff_query import get_all_products_with_inventory, get_product_with_inventory

staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates/staff")

@staff_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = getUserInfo()
   if session.get('logged_in') != True or user["user_role"] != 'staff':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)

@staff_page.route("/inventory_management")
def inventory_management():
   user = getUserInfo()
   products = []
   try:
      cursor = getCursor()
      sql_query = get_all_products_with_inventory()
      cursor.execute(sql_query)
      results = cursor.fetchall()
      for item in results:
         products.append({
            "product_id": item[0],
            "product_name": item[1],
            "product_status": item[2],
            "product_inventory_id": item[3],
            "product_inventory": item[4]
         })
   except Exception as e:
      print("@staff_page.route(/inventory_management): %s", e)
      return products
   return render_template("staff/inventory_management.html", user=user, products=products)

@staff_page.route("/product_with_inventory", methods=["GET"])
def product_with_inventory():
   product = {
      "product_name": "",
      "product_description": "",
      "product_price": "",
      "product_image": "",
      "product_status": "",
      "product_inventory_id": "",
      "product_inventory": 0
   }
   try:
      product_id = request.args.get('product_id')
      cursor = getCursor()
      sql_query = get_product_with_inventory()
      cursor.execute(sql_query, (product_id, ))
      result = cursor.fetchone()
      product = {
         "product_name": result[0],
         "product_description": result[1],
         "product_price": result[2],
         "product_image": result[3],
         "product_status": result[4],
         "product_inventory_id": result[5],
         "product_inventory": result[6]
      }
      return product
   except Exception as e:
      print("staff_page/product_with_inventory : %e ",e)
      return product

# @staff_page.route("/update_product_inventory", methods=["POST"])
# def update_product_inventory():
#    try:
#       inventory_id = request.json.get('inventory_id')
#       new_inventory = request.json.get('new_inventory')