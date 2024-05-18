from datetime import datetime

from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, session, request
from cursor import getCursor
from staff_query import order_list_query, order_list_without_date_query, update_order_status_query

order_page = Blueprint("order_page", __name__, static_folder="static", template_folder="templates/order")


@order_page.route("/orders_list", methods=['GET', 'POST'])
def orders_list():
    try:
        connection = getCursor()
        query_date = request.args.get('date', default=None)
        if query_date:
            try:
                # Assuming date is in YYYY-MM-DD format
                parsed_date = datetime.strptime(query_date, '%Y-%m-%d').date()
                sql_query = order_list_query()
                connection.execute(sql_query, (parsed_date,))
            except ValueError:
                return "Invalid date format", 400
        else:
            sql_query = order_list_without_date_query()
            connection.execute(sql_query)

        orders_list = connection.fetchall()
        return render_template("order/order_management.html", orders_list=orders_list)
    except Exception as e:
        print(f"Error fetching order list: {e}")
        return render_template("order/order_management.html", error=str(e))


@order_page.route("update_order_status", methods=['GET', 'POST'])
def update_order_status():
    try:
        order_id = request.form.get('order_id')
        order_status = request.form.get('order_status')
        connection = getCursor()

        if order_status not in ['pending''Prepared', 'Ready for Delivery', 'Delivered']:
            return "Invalid status"

        else:
            sql_query = update_order_status_query()
            connection.execute(sql_query, order_id)
            # return "Order status updated successfully"
            return render_template("order/order_management.html")
    except Exception as e:
        print(f"Error fetching order: {e}")
        return render_template("order/order_management.html", error=str(e))