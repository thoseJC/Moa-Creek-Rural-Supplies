def category_list_query():
    return """
    		SELECT 
    			*
    		FROM 
    			categories
    	"""


def get_credit_fields():
	return """
		SELECT
			credit_limit,
			credit_remaining,
			credit_apply
		FROM
			users
		WHERE
			user_id=%s;
	"""

def update_credit_apply():
	return """
		UPDATE users
    SET credit_apply = %s
    WHERE user_id = %s
	"""
def query_notifications():
    return """
    		SELECT notification_id, message, is_read, created_at FROM notifications WHERE user_id = %s and is_read = %s ORDER BY created_at DESC;
    	"""


def send_inquiry():
      return """
		INSERT INTO messages (sender_id, receiver_id, content) VALUES(%s, %s,%s);
      """

def add_conversation():
	return """
	INSERT INTO conversations (staff_id, customer_id, last_message_id) VALUES (%s, %s,%s);
"""

def get_customer_all_orders():
	return """
		SELECT
			order_id,
			order_date,
			total,
			status
		FROM
			orders
		WHERE
			user_id=%s;
	"""

def get_order_all_data():
	return """
		SELECT 
			o.order_id,
			o.order_date,
			o.total,
			o.status,
			u.first_name,
			u.last_name,
			a.street_address,
			a.city,
			a.state,
			a.postal_code,
			a.country,
			p.name AS product_name,
			p.pd_image_path,
			oi.price_per_unit,
			oi.qty,
			o.gst,
			o.freight
		FROM 
			orders o
		INNER JOIN 
			order_items oi ON oi.order_id = o.order_id
		INNER JOIN 
			products p ON oi.product_id = p.product_id
		INNER JOIN 
			users u ON o.user_id = u.user_id
		INNER JOIN 
			address a ON u.user_id = a.user_id AND a.is_primary = TRUE
		WHERE 
			o.order_id=%s;
	"""
