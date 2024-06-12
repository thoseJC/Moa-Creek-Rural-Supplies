import os
from flask import Blueprint, flash,request, redirect, url_for, jsonify,render_template,session
from app_query import get_products_by_categories, query_product_by_id, get_products_by_ids
from cursor import getCursor
from product_query import query_product_by_id, insert_product, get_all_categories, sql_update_product,query_product_list

product_page = Blueprint("product_page", __name__, static_folder="static", template_folder="templates/product")
UPLOAD_FOLDER = 'static/images/products'

@product_page.route("/product-management")
def get_list_of_product():
	try:
		products = []
		cursor = getCursor()
		sql_query = query_product_list()
		cursor.execute(sql_query)
		for product in cursor:
			products.append({
                "id": product[0],
                "name": product[1],
                "description": product[2],
                "price": product[3],
                "pd_image_path": product[4],
                "category_name": product[5],
                "is_active": product[6]
            })
		cursor.close()
        
		return render_template('product_management.html', products=products)	
	except Exception as e:
		print("Error in product_management:", e)
        # Handle error appropriately, like rendering an error template
		return render_template('product_management.html', error_msg="An error occurred while fetching products.")

@product_page.route('/<int:product_id>')
def show_product(product_id):
	try:
		cursor = getCursor()
		sql_query = query_product_by_id()
		cursor.execute(sql_query, (product_id,))
		fetched_product = cursor.fetchone()
		cursor.execute("select * from categories")
		categories = cursor.fetchall()
		product = {
			"id":fetched_product[0],
			"name": fetched_product[1],
			"description": fetched_product[2],
			"price": fetched_product[3],
			"discount": fetched_product[4],
			"discounted_price": fetched_product[5],
			"image": fetched_product[6],
			"category": fetched_product[7],
			"active": fetched_product[8],
			"quantity": fetched_product[9],
			"categoryId" : fetched_product[10]
		}
		categoryId = product["categoryId"]
		cursor.execute("select * from products where category_id = %s",(categoryId,))
		products = cursor.fetchall();
		return render_template('product_info.html',product = product, products= products, categories =categories, error_msg = None)
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
			file = request.files['product_image']
			category_id = request.form['category_id']

			if file.filename == "":
				flash("No select file")
				return redirect(url_for('product_page.get_list_of_product'))
			filename = file.filename
			print(os.path.join(UPLOAD_FOLDER))
			file.save(os.path.join(UPLOAD_FOLDER, filename))

			# Insert the new product into the database
			cursor = getCursor()
			sql_query = insert_product()
			cursor.execute(sql_query, (name, description, price, filename, category_id, 1))

			# Redirect to the product info page of the newly added product
			return redirect(url_for('product_page.get_list_of_product'))
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
            price = float(request.form['price'])
            discount = float(request.form['discount'])
            discounted_price = price - (price * discount / 100)
            image_path = request.form['image_path']
            category_id = request.form['category_id']

            # Update the product in the database
            cursor = getCursor()
            sql_query = sql_update_product()
            cursor.execute(sql_query, (name, description, price, image_path, category_id,discount, discounted_price, product_id))

            # Redirect to the product info page of the updated product
            return redirect(url_for('product_page.get_list_of_product'))
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
                "discount": fetched_product[4],
                "discounted_price": fetched_product[5],
                "image": fetched_product[6],
                "category_id": fetched_product[7],
                "active": fetched_product[8]
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
		return redirect(url_for('product_page.get_list_of_product'))
	except Exception as e:
		print("@app.route('/product/delete'): %s",e)
		#return render_template('product_management.html', error_msg = e)
		return redirect(url_for('product_page.get_list_of_product', error_msg = e) )


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
				"discounted_price": product[5],
                "pd_image_path": product[6],
                "is_active": product[7]
            })
        cursor.close()
        return products
    except Exception as e:
        print("@app.route(/get_products): %s", e)
        return products

@product_page.route('/<string:categries>', methods=['GET'])
def list_product(categries):
	try:
		# get a list of product from same categories
		get_products_by_categories_sql = get_products_by_categories()
		cursor = getCursor()
		cursor.execute(get_products_by_categories_sql,(categries,) )
		products_data = cursor.fetchall()
		products = process_product(products_data)
		cursor.close()
		return render_template("product_list.html", products = products)
	except Exception as e:
		print(e)	
		return render_template("product_list.html" ,products= [] )
	

def process_product(products_data):
	new_list = []
	if len(products_data) > 0:
		for product in products_data:
			product_obj = {
				"id" : product[0],
				"categories_id" : product[1],
				"name" : product[2],
				"product_description" : product[3],
				"price" : product[4],
				"image_path" : product[5],
				"shipping_type" : product[6],
			}
			new_list.append(product_obj)
		return new_list
	else:
		return []


