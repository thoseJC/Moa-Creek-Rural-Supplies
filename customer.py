from flask import Blueprint, flash, redirect, url_for, jsonify
from cursor import getCursor
from flask import session
from flask import render_template

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

