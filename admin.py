from flask import Blueprint, flash, redirect, url_for, jsonify, request, session, render_template
from cursor import getConection, getCursor
from flask import current_app as app
from login_helper import getUserInfo
from admin_query import query_add, query_edit,query_ctgr_list, query_deactivate_prm, query_deactivate_p, query_deactivate_c

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates/admin")


@admin_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    user = getUserInfo()
    if session.get('logged_in') != True or user["user_role"] != 'admin':
        return redirect(url_for('login_page.login'))
    return render_template("global/account_dashboard.html", user=user)


@admin_page.route('/categories_management')
def categories_management():
    try:
        connection = getCursor()
        sql_query = query_ctgr_list()
        connection.execute(sql_query,)
        categories = connection.fetchall()
        return render_template('/categories_management.html', categories=categories)
    except Exception as e:
        flash(f"An error occurred while fetching categories: {e}", "error")
        return redirect(url_for('admin.categories_management'))


@admin_page.route('/add', methods=['POST', 'GET'])
def add():
    try:
        name = request.form.get('name')
        description = request.form.get('description')

        connection = getCursor()
        sql_query = query_add()
        connection.execute(sql_query, (name, description))

        return redirect(url_for('admin.categories_management'))
    except Exception as e:
        flash(f"An error occurred while adding the category: {e}", "error")
        return redirect(url_for('admin.categories_management'))


@admin_page.route('/edit', methods=['POST', 'GET'])
def edit():
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')

        connection = getCursor()
        sql_query = query_edit()
        connection.execute(sql_query, (name, description, id))

        return redirect(url_for('admin.categories_management'))
    except Exception as e:
        flash(f"An error occurred while editing the category: {e}", "error")
        return redirect(url_for('admin.categories_management'))


@admin_page.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    try:
        connection = getCursor()

        prm_sql_query = query_deactivate_prm()
        connection.execute(prm_sql_query, (id,))

        p_sql_query = query_deactivate_p()
        connection.execute(p_sql_query, (id,))

        c_sql_query = query_deactivate_c()
        connection.execute(c_sql_query, (id,id))

        return redirect('/admin/categories_management')
    except Exception as e:
        flash(f"An error occurred while deleting the category: {e}", "error")
        return redirect('/admin/categories_management')


@admin_page.route('/manage_shipping_prices', methods=['GET', 'POST'])
def manage_shipping_prices():
    if request.method == 'POST':
        standard_price = request.form['standard']
        oversized_price = request.form['oversized']
        pickup_price = request.form['pickup']

        update_query = """
        UPDATE shipping_fee
        SET price = CASE 
            WHEN shipping_type = 'standard' THEN %s
            WHEN shipping_type = 'oversized' THEN %s
            WHEN shipping_type = 'pickup' THEN %s
        END
        WHERE shipping_type IN ('standard', 'oversized', 'pickup')
        """

        db_conn = getConection()
        cursor = db_conn.cursor()
        cursor.execute(update_query, (standard_price, oversized_price, pickup_price))
        db_conn.commit()
        cursor.close()
        db_conn.close()

        # Clear previous flash messages
        session.pop('_flashes', None)
        
        flash('Shipping prices updated successfully.', 'success')
        return redirect(url_for('admin.manage_shipping_prices'))

    query = "SELECT shipping_type, price FROM shipping_fee"
    prices = {}

    db_conn = getConection()
    cursor = db_conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        prices[row[0]] = row[1]
    cursor.close()
    db_conn.close()

    return render_template(
        'manage_shipping_prices.html',
        standard_price=prices.get('standard', 0),
        oversized_price=prices.get('oversized', 0),
        pickup_price=prices.get('pickup', 0)
    ) 