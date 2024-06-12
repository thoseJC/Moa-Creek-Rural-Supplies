from flask import Blueprint, flash, redirect, session, render_template, url_for
from cursor import getCursor, getConection

cart_page = Blueprint("cart", __name__, static_folder="static", template_folder="templates/cart")

@cart_page.route("/")
def cart():
    if not session.get('user_id'):
        flash('You need to login to check Cart.', 'warning')
        return redirect(url_for('login_page.login'))

    user_id = session['user_id']

    query = "SELECT shipping_type, price FROM shipping_fee"
    prices = {}

    db_conn = None
    cursor = None
    try:
        db_conn = getConection()  
        cursor = db_conn.cursor() 
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            prices[row[0]] = row[1]
    except Exception as e:
        print("Error fetching shipping prices: %s" % e)


    return render_template(
        'global/cart.html',
        user_id=user_id,
        standard_price=prices.get('standard', 0),
        oversized_price=prices.get('oversized', 0),
        pickup_price=prices.get('pickup', 0)
    )