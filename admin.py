from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

from login_helper import getUserInfo

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates/admin")

@admin_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user = getUserInfo()
   if session.get('logged_in') != True or user["user_role"] != 'admin':
      return redirect(url_for('login_page.login'))
   return render_template("global/account_dashboard.html", user=user)