from flask import redirect,url_for,session

def redirect_by_role(user_role):
	if user_role == 'manager':
		return redirect(url_for('manager.dashboard'))
	if user_role == 'customer':
		return redirect(url_for('customer.dashboard'))
	if user_role == 'admin':
		return redirect(url_for('admin.dashboard'))
	if user_role == 'staff':
		return redirect(url_for('staff.dashboard'))
	
def setUp_session(user):
	session["user_id"] = user[0]
	session["logged_in"] = True
	session["user_name"] = user[2]
	session["user_role"] = user[5]
	session["first_name"] = user[6]
	session["last_name"] = user[7]
	session["order_count"] = user[8]
	session["password"] = user[3]