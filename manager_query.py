def get_all_account_holders():
	return """
		SELECT
      user_id,
			first_name,
			last_name,
			credit_limit,
			credit_remaining,
			credit_apply
		FROM
			users;
	"""

def update_customer_credit_apply():
	return """
    UPDATE users
    SET credit_apply=%s, credit_remaining=%s, credit_limit=%s
    WHERE user_id=%s;
  """
def get_user_account_info_sql():
    return '''select * from user_account_management where user_id != %s;'''
