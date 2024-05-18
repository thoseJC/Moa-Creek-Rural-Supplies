from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session
from cursor import getCursor


order_page = Blueprint("order_page", __name__, static_folder="static", template_folder="templates/order")


@order_page.route("/order-management")
def get_all_customer_order():
	return render_template("order-management.html")