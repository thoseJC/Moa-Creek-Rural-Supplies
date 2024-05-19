from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, session
from cursor import getCursor
from message_query_n_function import query_update_order_status, send_email

message_page = Blueprint("message_page", __name__, static_folder="static", template_folder="templates/message")


@message_page.route('/send_status_update_notifications/<user_id>', methods=['POST'])
def send_status_update_notifications(user_id):
    # Check if a valid customer ID is provided in the route parameter
    if not user_id:
        return 'No customer ID provided', 400

    try:
        con = getCursor()
        query = query_update_order_status()
        con.execute(query, (user_id,))
        user_info = con.fetchone()

        if not user_info:
            # Return a 404 response if no relevant member information is found
            return jsonify({'message': 'No member found'}), 404

        recipient = user_info[0]
        first_name = user_info[1]
        order_id = user_info[2]
        status = user_info[3]
         # Define the subject of the email
        subject = 'Order Status Update'
        # Compose the body of the email with personalized information
        body = f'Dear {first_name}, your order:{order_id} has moved to stage of:{status}'
        # Send the email 
        send_email(recipient, subject, body)
        return jsonify({'message': 'notification sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
