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

# def get_all_account_holders():
# 	return """
# 		SELECT
#       user_id,
# 			first_name,
# 			last_name,
#       credit_limit,
#       credit_remaining,
#       credit_apply
# 		FROM
# 			users
# 		WHERE
# 			account_holder=true;
# 	"""

def update_customer_credit_apply():
	return """
    UPDATE users
    SET credit_apply=%s, credit_remaining=%s, credit_limit=%s
    WHERE user_id=%s;
  """