from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

# from app import app
manager_page = Blueprint("manager", __name__, static_folder="static", template_folder="templates/manager")

@manager_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
   user_role = session.get("user_role")
   if session.get('logged_in') != True or user_role != 'manager':
      return redirect(url_for('login'))
   return render_template("global/account_dashboard.html", user_role = user_role)