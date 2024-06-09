from flask import Blueprint, session, render_template
from cursor import getCursor, getConection

cart_page = Blueprint("cart", __name__, static_folder="static", template_folder="templates/cart")

@cart_page.route("/")
def cart():
    user_id = 0
    if session.get("user_id"):
        user_id = session.get("user_id")

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
    finally:
        if cursor:
            cursor.close()
        if db_conn:
            db_conn.close()

    return render_template(
        'global/cart.html',
        user_id=user_id,
        standard_price=prices.get('standard', 0),
        oversized_price=prices.get('oversized', 0),
        pickup_price=prices.get('pickup', 0)
    )