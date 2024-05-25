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