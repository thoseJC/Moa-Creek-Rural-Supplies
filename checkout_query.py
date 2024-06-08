def insert_payment_record():
  return """
    INSERT INTO payment (user_id, total, payment_type, GST, freight) VALUES (%s, %s, %s, %s, %s);
  """

def insert_orders_record():
  return """
    INSERT INTO orders (user_id, payment_id, total, GST, freight, status) VALUES (%s, %s, %s, %s, %s, 'pending');
  """

def insert_order_items_record():
  return """
    INSERT INTO order_items (order_id, product_id, qty, price_per_unit) VALUES (%s, %s, %s, %s);
  """

def query_latest_id():
  return """
    SELECT LAST_INSERT_ID();
  """

def get_user_address_query():
	return """
    SELECT 
      street_address,
			city,
			state,
			postal_code,
			country
    FROM address 
    WHERE 
		  user_id = %s AND is_primary = TRUE;
  """
