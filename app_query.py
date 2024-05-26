def query_user_when_login():
	return """
			SELECT 
				u.user_id,
				u.role_id, 
				u.username, 
				u.user_password, 
				u.status, 
				ur.role_name,
				u.first_name,
				u.last_name,
				COUNT(o.order_id) AS order_count
			FROM 
				users u
			JOIN 
			user_roles ur ON u.role_id = ur.role_id
			LEFT JOIN 
			orders o ON u.user_id = o.user_id
			WHERE 
			u.username = %s;
		"""


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

def register_new_user():
	return """
				INSERT INTO users (user_id, role_id, first_name, last_name, username, email, phone_number, loyalty_points, user_password, shipping_address, status)
				VALUES (UUID(), (SELECT role_id FROM user_roles WHERE role_name = 'customer'), %s, %s, %s, %s, %s, 0, %s, %s, TRUE)"""

def update_user_profile_query():
	return """
				UPDATE 
					users
				SET 
					first_name = %s,
					last_name = %s,
					email = %s,
					phone_number = %s,
					user_password = %s
				WHERE
					user_id = %s;
			"""

def update_user_profile_by_manager():
	return '''
				UPDATE 
					users
				SET 
					first_name = %s,
					last_name = %s,
					email = %s,
					phone_number = %s,
					user_password = %s
				WHERE
					user_id = %s;
'''


def get_user_profile_query():
	return """
			SELECT 
				first_name,
				last_name,
				email,
				phone_number
			FROM users
			WHERE user_id = %s;
		"""


def get_products_by_ids(product_ids):
    product_ids_string = ', '.join(map(str, product_ids))
    return f"""
        SELECT
            product_id, category_id, name, description, price, pd_image_path, is_active
        FROM products 
        WHERE product_id IN ({product_ids_string});
    """


