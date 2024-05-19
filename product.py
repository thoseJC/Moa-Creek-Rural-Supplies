from flask import Blueprint, flash,request, redirect, url_for, jsonify,render_template,session
from app_query import query_product_by_id, get_products_by_ids
from cursor import getCursor
from product_query import query_product_by_id, insert_product, get_all_categories, sql_update_product

product_page = Blueprint("product_page", __name__, static_folder="static", template_folder="templates/product")


@product_page.route("/product-management")
def get_list_of_product():
	return render_template("product-management.html")

@product_page.route('/<int:product_id>')
def show_product(product_id):
	try:
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
	except Exception as e:
		print("@app.route('/product'): %s",e)
		return render_template('product_info.html', error_msg = e)


@product_page.route('/add', methods=['GET', 'POST'])
def add_product():
	try:
		category_id = request.args.get('category_id')
		if category_id is not None:
			category_id = int(category_id)  # Convert to integer if it's not None
		if request.method == 'POST':
			# Retrieve form data
			name = request.form['name']
			description = request.form['description']
			price = request.form['price']
			image_path = request.form['image_path']
			category_id = request.form['category_id']

			# Insert the new product into the database
			cursor = getCursor()
			sql_query = insert_product()
			cursor.execute(sql_query, (name, description, price, image_path, category_id, 1))

			# Redirect to the product info page of the newly added product
			return redirect(url_for('product_page.show_product', product_id=cursor.lastrowid))
		else:
			# If it's a GET request, render the form to add a new product
			# Retrieve category options from the database
			cursor = getCursor()
			sql_query = get_all_categories()
			cursor.execute(sql_query)
			categories = cursor.fetchall()
			print(category_id)
			return render_template('add_product.html', selected_category_id=category_id, categories=categories)
	except Exception as e:
		print("@app.route('/product/add'): %s",e)
		return render_template('add_product.html', error_msg = e)


@product_page.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
	try:
		if request.method == 'POST':
			# Retrieve form data
			name = request.form['name']
			description = request.form['description']
			price = request.form['price']
			image_path = request.form['image_path']
			category_id = request.form['category_id']

			# Update the product in the database
			cursor = getCursor()
			sql_query = sql_update_product()
			cursor.execute(sql_query, (name, description, price, image_path, category_id, product_id))

			# Redirect to the product info page of the updated product
			return redirect(url_for('show_product', product_id=product_id))
		else:
			# Fetch the product details from the database
			cursor = getCursor()
			sql_query1 = query_product_by_id()
			cursor.execute(sql_query1, (product_id,))
			fetched_product = cursor.fetchone()
			product = {
				"id": fetched_product[0],
				"name": fetched_product[1],
				"description": fetched_product[2],
				"price": fetched_product[3],
				"image": fetched_product[4],
				"category_id": fetched_product[5],
				"active": fetched_product[6]
			}

			# Retrieve category options from the database
			sql_query = get_all_categories()
			cursor.execute(sql_query)
			categories = cursor.fetchall()

			return render_template('edit_product.html', product=product, categories=categories)
	except Exception as e:
		print("@app.route('/product/edit'): %s",e)
		return render_template('edit_product.html', error_msg = e)
		
@product_page.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
	try:
		# Delete the product from the database
		cursor = getCursor()
		sql_query = "DELETE FROM products WHERE product_id = %s"
		cursor.execute(sql_query, (product_id,))

		# Redirect to a page after deletion (e.g., product listing page)
		return redirect(url_for('show_product', product_id=1))
	except Exception as e:
		print("@app.route('/product/delete'): %s",e)
		return render_template('edit_product.html', error_msg = e)


@product_page.route("/get_products", methods=["POST"])
def get_products():
    products = []
    try:
        product_ids = request.json.get("product_ids", [])
        if len(product_ids) == 0:
            return products
        cursor = getCursor()
        sql_query = get_products_by_ids(product_ids)
        cursor.execute(sql_query)
        for product in cursor:
            products.append({
                "product_id": product[0],
                "category_id": product[1],
                "name": product[2],
                "description": product[3],
                "price": product[4],
                "pd_image_path": product[5],
                "is_active": product[6]
            })
        cursor.close()
        return products
    except Exception as e:
        print("@app.route(/get_products): %s", e)
        return products

