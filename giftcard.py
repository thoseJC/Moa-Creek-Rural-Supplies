from decimal import Decimal
import time
from flask import Blueprint, flash, redirect, url_for, jsonify, request,session,render_template
from cursor import getConection, getCursor
from customer_query import add_conversation, get_credit_fields, send_inquiry, update_credit_apply, get_customer_all_orders, get_order_all_data
from login_helper import getUserInfo
from customer_query import category_list_query, query_notifications

giftcard_page = Blueprint("giftcard_page", __name__, static_folder="static", template_folder="templates/giftcard")


@giftcard_page.route("/validate" ,methods = ["POST", "GET"])
def getGiftCard():
	if request.method == "POST":
		try:
			reqBody = request.get_json()
			gf_card_id = reqBody.get("gf_card_id")
			cardHolder = session["user_id"]
			cursor = getCursor()
			cursor.execute("select * from gift_card where gf_card_id = %s and holder = %s ", (gf_card_id, cardHolder) )
			result = cursor.fetchone()
			if result and result[0]:
				gf_card = {
					"id" : result[0],
					"amount" : Decimal(result[1]),
					"holder" : result[2],
					"exprired_date" : result[3]
				}
				return jsonify(gf_card),200
			else:
				return jsonify({"message":"gift card not exist"}),404
		except Exception as e:
			return jsonify({"message":"gift card not {e}"}),400


