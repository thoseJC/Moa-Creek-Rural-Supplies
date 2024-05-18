from flask import Blueprint, flash, redirect, url_for, jsonify,render_template,session
from app_query import query_product_by_id
from cursor import getCursor


product_page = Blueprint("product_page", __name__, static_folder="static", template_folder="templates/product")


@product_page.route("/product-management")
def get_list_of_product():
	return render_template("product-management.html")

@product_page.route('/<int:product_id>')
def show_product(product_id):
	cursor = getCursor()
	sql_query = query_product_by_id()
	cursor.execute(sql_query, (product_id,))
	fetched_product = cursor.fetchone()
	product = {
		"id":fetched_product[0],
		"name": fetched_product[1],
		"description": fetched_product[2],
		"price": fetched_product[3],
		"image": fetched_product[4],
		"category": fetched_product[5],
		"active": fetched_product[6]

	}

	return render_template('product_info.html',product = product)