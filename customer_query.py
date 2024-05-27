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
    		SELECT notification_id, message, is_read, created_at FROM notifications WHERE user_id = %s and is_read = %s ORDER BY created_at DESC
    	"""
