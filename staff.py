from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates/staff")

@staff_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = {
      "user_id": session.get("user_id"),
      "user_role": session.get("user_role"),
      "first_name": session.get("first_name")
   }
   if session.get('logged_in') != True or user["user_role"] != 'staff':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)