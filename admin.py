from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates/admin")

@admin_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = {
      "user_id": session.get("user_id"),
      "user_role": session.get("user_role"),
      "first_name": session.get("first_name")
   }
   if session.get('logged_in') != True or user["user_role"] != 'admin':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)