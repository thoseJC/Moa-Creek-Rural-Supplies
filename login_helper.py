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
	session["password"] = user[3]
	session["user_role"] = user[5]
	session["first_name"] = user[6]
	session["last_name"] = user[7]
	session["business_account_status"] = user[8]
	session["order_count"] = user[9]

def getUserInfo():
	user = {
    	"user_id": session.get("user_id"),
    	"user_role": session.get("user_role"),
    	"first_name": session.get("first_name"),
    	"last_name": session.get("last_name"),
    	"order_count": session.get("order_count"),
		"business_account_status" : session.get("business_account_status")
	}
	return user;
	
