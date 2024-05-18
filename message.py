from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session
from cursor import getCursor


message_page = Blueprint("message_page", __name__, static_folder="static", template_folder="templates/message")


@message_page.route("/message-management")
def get_all_customer_order():
	return render_template("order-management.html")