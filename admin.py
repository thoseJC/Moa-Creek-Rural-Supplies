from flask import Blueprint, flash, redirect, url_for, jsonify, request

from admin_query import query_add, query_edit, query_delete_prm, query_delete_p, query_delete_c
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


@admin_page.route('/categories_management')
def categories_management():
    connection = getCursor()
    sql_query = "SELECT * FROM categories"
    connection.execute(sql_query,)
    categories = connection.fetchall()
    return render_template('/categories_management.html', categories=categories)


@admin_page.route('/add', methods=('POST',))
def add():
    name = request.form.get('name')
    description = request.form.get('description')

    connection = getCursor()
    sql_query = query_add
    connection.execute(sql_query, (name, description))

    return redirect(url_for('admin.categories_management'))


@admin_page.route('/edit', methods=['POST', 'GET'])
def edit():
    id = request.form.get('id')
    print(id)
    name = request.form.get('name')
    description = request.form.get('description')

    connection = getCursor()
    sql_query = query_edit
    connection.execute(sql_query, (name, description, id))
    return redirect(url_for('admin.categories_management'))


@admin_page.route('/delete', methods=('POST', 'GET'))
def delete():
    id = request.args.get('id')
    connection = getCursor()

    prm_sql_query = query_delete_prm
    connection.execute(prm_sql_query, (id,))

    p_sql_query = query_delete_p
    connection.execute(p_sql_query, (id,))

    c_sql_query = query_delete_c
    connection.execute(c_sql_query, (id,))

    return redirect(url_for('admin.categories_management'))