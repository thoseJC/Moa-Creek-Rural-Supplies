from flask import Blueprint, session, render_template, request, jsonify
from checkout_query import insert_payment_record, query_latest_id, insert_orders_record, insert_order_items_record
from cursor import getCursor

checkout_page = Blueprint("checkout", __name__, static_folder="static", template_folder="templates/checkout")

@checkout_page.route("/proceed_payment", methods=["POST"])
def proceed_payment():
    try:
        print("request.json", request.json)
        user_id = request.json.get("userId")
        total = request.json.get('total', 0)
        payment_type = request.json.get('paymentType', "Credit Card")
        gst = request.json.get('gst', 0)
        freight = request.json.get('freight', 0)
        cart_items = request.json.get('cartItems', [])

        if user_id != '':
            cursor = getCursor()
            sql_query = insert_payment_record()
            cursor.execute(sql_query, (user_id, total, payment_type, gst, freight))
            cursor.execute(query_latest_id())
            result = cursor.fetchone()
            payment_id = result[0]
            sql_query = insert_orders_record()
            cursor.execute(sql_query, (user_id, payment_id, total, gst, freight))
            cursor.execute(query_latest_id())
            result = cursor.fetchone()
            order_id = result[0]
            for item in cart_items:
              product_id = item['id']
              qty = item['quantity']
              price = item.get('price', 0.00)
              sql_query = insert_order_items_record()
              cursor.execute(sql_query, (order_id, product_id, qty, price))
            return jsonify({'message': 'Payment Completed'}), 200
    except Exception as e:
        print("@checkout_page.route(/proceed_payment): %s", e)
        return jsonify({'message': 'Payment Error'}), 400
    finally:
        cursor.close()

