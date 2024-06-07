import time
from flask import Blueprint, flash, redirect, url_for, jsonify, request,session,render_template
from cursor import getConection, getCursor
from customer_query import add_conversation, get_credit_fields, send_inquiry, update_credit_apply, get_customer_all_orders, get_order_all_data
from login_helper import getUserInfo
from customer_query import category_list_query, query_notifications

customer_page = Blueprint("customer", __name__, static_folder="static", template_folder="templates/customer")


@customer_page.route("/dashboard")
def dashboard():
  user = getUserInfo()
  if session.get('logged_in') != True or user["user_role"] != 'customer':
    return redirect(url_for('login_page.login'))
  
  connection = getCursor()  
  sql_query = "SELECT * FROM news WHERE is_published = true ORDER BY published_date DESC LIMIT 5"  # SQL query to get latest published news
  connection.execute(sql_query)
  news_list = []

  for news in connection:
    news_list.append({
        "news_id": news[0],
        "title": news[1],
        "content": news[2],
        "created_by": news[3],
        "is_published": news[4],
        "published_date": news[5]
    })
  connection.close()

  return render_template("global/account_dashboard.html", user=user, latest_news = news_list)


@customer_page.route("/categories")
def categories():
    connection = getCursor()
    sql_query = category_list_query()
    connection.execute(sql_query)
    categories_list = connection.fetchall()

    return render_template("global/categories.html", categories_list=categories_list)

@customer_page.route("/credit")
def credit():
  msg_obj = {
    "type": "",
    "msg": ""
  }
  user = getUserInfo()
  credit_obj = {
    "credit_limit": 0,
    "credit_remaining": 0,
    "credit_apply": 0,
    "limit_alert": False
  }
  if not user["user_id"]:
    return redirect(url_for('login_page.login'))
  
  cursor = getCursor()
  try:
    cursor.execute(get_credit_fields(), (user['user_id'],))
    result = cursor.fetchone()
    if result is not None and result[0] is not None and result[1] is not None and result[2] is not None:
      limit_alert = False
      if float(result[1]) < 50:
        limit_alert = True
      credit_obj = {
        "credit_limit": result[0],
        "credit_remaining": result[1],
        "credit_apply": result[2],
        "limit_alert": limit_alert
      }
      if result[2] == -1:
        msg_obj['type'] = 'success'
        msg_obj['msj'] = 'Congratulations!! Your credit limit has been increased!!'
        sql_query = update_credit_apply()
        cursor = getCursor()
        cursor.execute(sql_query, (0, user['user_id']))
      elif result[2] > 0:
        msg_obj['type'] = 'notification'
        msg_obj['msj'] = 'Your credit limit increasement application is currently pending on review, you should hear back within 3 business days.'
  except Exception as e:
    print(f"Database query failed: {e}")
    return "An error occurred", 500
  return render_template("credit.html", user=user, credit_obj=credit_obj, msg_obj=msg_obj)


@customer_page.route("/credit_apply", methods=["POST"])
def credit_apply():
  user = getUserInfo()
  try:
    new_limit = request.json.get("new_limit", 0)
    user_id = user["user_id"]
    sql_query = update_credit_apply()
    cursor = getCursor()
    cursor.execute(sql_query, (new_limit, user_id))
    return jsonify({'message': 'Application Submitted'}), 200
  except Exception as e:
    print("@customer_page.route(/credit_apply): %s", e)
    return jsonify({'message': 'Application Error'}), 400
  finally:
    cursor.close()

@customer_page.route("/notifications/", methods=['GET','POST'])
def notifications():
    user_id = session.get("user_id")
    print(user_id)
    try:
        connection = getCursor()
        connection.execute(query_notifications(), (user_id,0))
        notifications = connection.fetchall()

        return jsonify(notifications)
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return jsonify({"error": str(e)}), 500
    

@customer_page.route("/inquiry",methods = ["GET", "POST"])
def inquiry():
  msg = {
    "success" : "",
    "message" : ""
  }
  try:
    connc = getConection()
    cursor = connc.cursor()
    current_user = getUserInfo()
    if request.method == 'POST':
      content = request.form.get("inquiry")
      sender_id = current_user.get("user_id")
      cursor.execute("select user_id from users where username = 'staff' ")
      staff_id_result = cursor.fetchone()
      staff_id = staff_id_result[0]
      send_inquiry_sql = send_inquiry()
      add_conversation_sql = add_conversation()
      #  store message into database
      cursor.execute(send_inquiry_sql, (sender_id,staff_id,content))
      connc.commit()
      cursor.close()

      # insert data to conversations
      new_cursor = connc.cursor()
      last_message_id = cursor.lastrowid
      new_cursor.execute(add_conversation_sql,(staff_id,sender_id,last_message_id))
      connc.commit()
      msg = {
        "success" : True,
        "message" : "Your inquiry has been sent successfully"
      }
    return render_template("inquiry.html", msg = msg)
  except Exception as e:
    error_msg = "Error happens contact the admin : {0}".format(e)
    msg = {
      "success" : False,
      "message" : error_msg
    }
    return render_template("inquiry.html", msg = msg)



def process_notification(notifications):
    noti_list = []
    for noti in notifications:
       noti_obj = {
          "id" : noti[0],
          "message" : noti[1],
          "readed" : noti[2],
          "send_time" : noti[3]
	   }
       noti_list.append(noti_obj)
    return noti_list;
   

@customer_page.route("/orders")
def orders():
  user = getUserInfo()
  orders = []
  try:
    user_id = user["user_id"]
    sql_query = get_customer_all_orders()
    cursor = getCursor()
    cursor.execute(sql_query, (user_id,))
    orders = cursor.fetchall()
    return render_template("customer/orders.html", user=user, orders=orders)
  except Exception as e:
    print("@customer_page.route(/orders): %s", e)
    return render_template("customer/orders.html", user=user, orders=orders)
  
@customer_page.route("/order_details", methods=["POST"])
def order_details():
  order_items = []
  try:
    order_id = request.json.get("order_id")
    sql_query = get_order_all_data()
    cursor = getCursor()
    cursor.execute(sql_query, (order_id,))
    order_items = cursor.fetchall()
    return order_items, 200
  except Exception as e:
    print("@customer_page.route(/order_details): %s", e)
    return order_items, 400
  finally:
    cursor.close()

@customer_page.route("/faq")
def faq():
    return render_template('customer/faq.html')