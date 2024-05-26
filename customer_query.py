def category_list_query():
    return """
    		SELECT 
    			*
    		FROM 
    			categories
    	"""

def query_notifications():
    return """
    		SELECT notification_id, message, is_read, created_at FROM notifications WHERE user_id = %s and is_read = %s ORDER BY created_at DESC
    	"""