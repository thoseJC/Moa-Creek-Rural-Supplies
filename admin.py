from flask import Blueprint, flash, redirect, url_for, jsonify, request, session, render_template
from cursor import getConection, getCursor
from flask import current_app as app
from login_helper import getUserInfo

admin_page = Blueprint("admin", __name__, static_folder="static", template_folder="templates/admin")

@admin_page.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    user = getUserInfo()
    if session.get('logged_in') != True or user["user_role"] != 'admin':
        return redirect(url_for('login_page.login'))
    return render_template("global/account_dashboard.html", user=user)

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