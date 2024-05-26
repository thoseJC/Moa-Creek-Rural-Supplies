def get_all_account_holders():
	return """
		SELECT
      user_id,
			first_name,
			last_name,
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
#       credit_apply
# 		FROM
# 			users
# 		WHERE
# 			account_holder=true;
# 	"""