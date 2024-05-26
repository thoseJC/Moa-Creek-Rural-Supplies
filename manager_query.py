def get_user_account_info_sql():
    return '''select * from user_account_management where user_id != %s;'''