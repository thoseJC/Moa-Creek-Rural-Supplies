from flask import Blueprint, flash, redirect, url_for, jsonify, request
from cursor import getCursor
from flask import session
from flask import render_template
from customer_query import get_credit_fields, update_credit_apply

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

@customer_page.route("/notifications/", methods=['GET'])
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