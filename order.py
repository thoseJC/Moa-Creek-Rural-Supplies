from datetime import datetime
import smtplib

from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, session, request
from cursor import getCursor
from message import send_email, send_status_update_notifications
from staff_query import order_list_query, order_list_without_date_query, update_order_status_query
from message import send_status_update_notifications

order_page = Blueprint("order_page", __name__, static_folder="static", template_folder="templates/order")


def create_notification(user_id, message):
    connection = getCursor()
    sql_query = "INSERT INTO notifications (user_id, message) VALUES (%s, %s)"
    connection.execute(sql_query, (user_id, message))
    connection.commit()


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
        return render_template("/order_management.html", orders_list=orders_list)
    except Exception as e:
        print(f"Error fetching order list: {e}")
        return render_template("/order_management.html", error=str(e))


@order_page.route("/update_order_status", methods=['GET', 'POST'])
def update_order_status():
    try:
        order_id = request.form.get('order_id')
        status = request.form.get('order_status')
        connection = getCursor()

        sql_query = update_order_status_query()
        connection.execute(sql_query, (status, order_id))

        flash('Order status updated successfully')
        return redirect(url_for('order_page.orders_list'))
    except Exception as e:
        print(f"Error fetching order: {e}")
        flash('Failed to update order status.', 'error')  # Flash an error message
        return redirect(url_for('order_page.orders_list'))


@order_page.route("/send_message_order_status", methods=['POST'])
def send_message_order_status():
    user_id = request.form.get('user_id')

    try:
        send_status_update_notifications(user_id)
        flash('Notification sent successfully!', 'success')
        return redirect(url_for('order_page.orders_list'))

    except Exception as e:
        flash(f'Failed to send notification: {str(e)}', 'error')
        return redirect(url_for('order_page.orders_list'))
