from flask import Blueprint, session, render_template, request, jsonify
from checkout_query import insert_payment_record, query_latest_id, insert_orders_record, insert_order_items_record, get_user_address_query, query_product_current_inventory, update_product_new_inventory
from cursor import getCursor
import uuid

checkout_page = Blueprint("checkout", __name__, static_folder="static", template_folder="templates/checkout")

@checkout_page.route("/proceed_payment", methods=["POST"])
def proceed_payment():
    try:
        user_id = request.json.get("userId")
        total = float(request.json.get('total', 0))
        payment_type = request.json.get('paymentType', "Credit Card")
        gst = request.json.get('gst', 0)
        freight = request.json.get('freight', 0)
        cart_items = request.json.get('cartItems', [])
        gift_card_id = request.json.get("giftCardId")
        cursor = getCursor()
        if payment_type == 'gift-card' and gift_card_id:
            # get gift card again : double validation 
            cursor.execute("select * from gift_card where gf_card_id = %s" ,(gift_card_id,))
            gf_card_info = cursor.fetchone()
            gf_card_amount = float(gf_card_info[1])
            update_gf_card_sql = "update gift_card set amount = %s where gf_card_id = %s"
            if gf_card_amount == 0:
                return jsonify({'message': 'Gift Card has 0 credit'}), 400
            if total >= gf_card_amount:
                # update the gift card value to 0
                cursor.execute(update_gf_card_sql, (0,gift_card_id ) )
            else:
                # update the remain of gift card value
                remain = gf_card_amount - total
                cursor.execute(update_gf_card_sql, (remain,gift_card_id ))
        if user_id != '':
            insert_payment_record_sql = insert_payment_record()
            cursor.execute(insert_payment_record_sql, (user_id, total, payment_type, gst, freight))
            cursor.execute(query_latest_id())
            result = cursor.fetchone()
            payment_id = result[0]
            sql_query = insert_orders_record()
            cursor.execute(sql_query, (user_id, payment_id, total, gst, freight))
            cursor.execute(query_latest_id())
            result = cursor.fetchone()
            order_id = result[0]
            
            for item in cart_items:
              print("item")
              product_id = item['id']
              qty = item['quantity']
              price = item.get('price', 0.00)
              sql_query = insert_order_items_record()
              cursor.execute(sql_query, (order_id, product_id, qty, price))

              sql_query = query_product_current_inventory()
              cursor.execute(sql_query, (product_id,))
              current_qty = cursor.fetchone()[0]

              new_qty = current_qty - qty
              sql_query = update_product_new_inventory()
              cursor.execute(sql_query, (new_qty, product_id))

                # if user buy gift card
              if product_id == '17' or product_id == '18' or product_id == '19':
                #   insert gift card record into gift card table for this user : 
                update_giftcard = "insert into gift_card (gf_card_id, amount, holder) values (%s, %s,%s)"
                amount = get_figt_card_amount(product_id)
                gift_card_uuid = str(uuid.uuid4())
                cursor.execute(update_giftcard, (gift_card_uuid, amount, user_id))
            return jsonify({'message': 'Payment Completed'}), 200
    except Exception as e:
        print("@checkout_page.route(/proceed_payment): %s", e)
        return jsonify({'message': 'Payment Error'}), 400
    finally:
        cursor.close()

@checkout_page.route("/get_user_address", methods=["GET"])
def get_user_address():
    address = {}
    try:
        user_id = request.args.get("user_id")
        cursor = getCursor()
        sql_query = get_user_address_query()
        cursor.execute(sql_query, (user_id, ))
        address = cursor.fetchone()
        return jsonify({
                'message': 'Success',
                'data': address
            }), 200
    except Exception as e:
        print("@checkout_page.route(/get_user_address): %s", e)
        return jsonify({
                'message': 'Fail',
                'data': address
            }), 400
    finally:
        cursor.close()


def get_figt_card_amount(gift_card_type_id):
    if gift_card_type_id == '17':
        return 100
    if gift_card_type_id == '18':
        return 50
    if gift_card_type_id == '19':
        return 20
    
