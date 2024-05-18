from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session
from cursor import getCursor


product_page = Blueprint("product_page", __name__, static_folder="static", template_folder="templates/product")


@product_page.route("/product-management")
def get_list_of_product():
	return render_template("product-management.html")