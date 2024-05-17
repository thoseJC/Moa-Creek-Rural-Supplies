# @app.route('/manage-own-profile', methods=['GET', 'POST'])
# def manage_own_profile():
# 	msg_obj = {
# 		"email": "",
# 		"phone_number": "",
# 		"success": ""
# 	}
# 	try:
# 		user_id = session.get("user_id")
# 		cursor = getCursor()

# 		if request.method == 'POST':
# 			first_name = request.form.get('first_name')
# 			last_name = request.form.get('last_name')
# 			email = request.form.get('email')
# 			phone_number = request.form.get('phone_number')
# 			user_password = request.form.get("first_password")
# 			print("password : %s", user_password)
# 			user = (first_name, last_name, email, phone_number)
# 			check_status = True
# 			if email and is_valid_email(email) != True:
# 				check_status = False
# 				msg_obj["email"] = "Please enter a correct email address!"
# 			if phone_number and is_valid_phone_number(phone_number) != True:
# 				check_status = False
# 				msg_obj["phone_number"] = "Please enter a correct phone number!"
# 			if check_status:
# 				sql_query = update_user_profile_query()
# 				cursor.execute(sql_query, (first_name, last_name, email, phone_number, user_id,))
# 				msg_obj["success"] = "Your profile has been updated successfully!"

# 		else:
# 			sql_query = get_user_profile_query()
# 			cursor.execute(sql_query, (user_id,))
# 			user = cursor.fetchone()

# 		return render_template('global/manage_own_profile.html',
# 			user=user, 
# 			msg_obj=msg_obj)
# 	except Exception as e:
# 		print("def manage_own_profile(): %s", e)
# 		return render_template('global/manage_own_profile.html',user=user, msg_obj=msg_obj, error_msg = e)