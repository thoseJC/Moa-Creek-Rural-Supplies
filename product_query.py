def query_product_by_id():
	return """
		SELECT 
			p.product_id,
			p.name,
			p.description,
			p.price,
			p.pd_image_path,
			c.name,
			p.is_active
		FROM products p 
		JOIN categories c
		ON p.category_id = c.category_id
		WHERE p.product_id = %s;
	"""

def insert_product():
	return """
		INSERT INTO products (name, description, price, pd_image_path, category_id, is_active)
						VALUES (%s, %s, %s, %s, %s, %s)
	"""

def get_all_categories():
	return "SELECT category_id, name FROM categories;"

def sql_update_product():
	return """
			UPDATE products 
			SET name=%s, description=%s, price=%s, pd_image_path=%s, category_id=%s
			WHERE product_id=%s
	"""
