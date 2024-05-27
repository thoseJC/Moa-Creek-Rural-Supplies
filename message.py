from datetime import datetime
from urllib import request

from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, session, request
from cursor import getCursor
from message_query import query_fetch_sender_username, query_update_order_status, send_email, query_inbox, query_conversation, query_check_receiver, query_insert_message, query_select_conversation, query_update_conversation, query_insert_conversation


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

        subject = 'Order Status Update'
        # Compose the body of the email with personalized information
        body = (f'Dear {first_name},\n\nWe are pleased to inform you that your order (Order ID: {order_id}) has '
                f'advanced to the following status: {status}.\n\nThank you for choosing our service. If you have any '
                f'questions or require further assistance, please do not hesitate to contact us.\n\nBest regards,'
                f'\n[Moe Creek Rural Supplies][(https://haoboli.pythonanywhere.com/]')

        # Send the email
        send_email(recipient, subject, body)

        return jsonify({'message': 'notification sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@message_page.route('/inbox')
def inbox():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        connection = getCursor()
        connection.execute(query_inbox(), (user_id, user_id))
        conversations = connection.fetchall()
        return render_template('inbox.html', conversations=conversations)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()



@message_page.route('/conversation', methods=['GET', 'POST'])
def conversation():
    conversation_id = request.args.get('conversation_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        connection = getCursor()
        connection.execute(query_conversation(), (conversation_id,))
        messages = connection.fetchall()
        print(messages)
        return render_template('conversation.html', messages=messages)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@message_page.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    sender_id = session['user_id']
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('content')

    try:
        connection = getCursor()

        # Check if receiver exists
        connection.execute(query_check_receiver(), (receiver_id,))
        receiver = connection.fetchone(buffered=True)
        
        if not receiver:
            return jsonify({"error": "Receiver does not exist"}), 400
        else:
            connection.execute(query_insert_message(), (sender_id, receiver_id, content, datetime.utcnow(), 'sent'))
            new_message_id = connection.lastrowid

            # Update or create conversation
            connection.execute(query_select_conversation(), (sender_id, receiver_id, receiver_id, sender_id))
            conversation = connection.fetchone(buffered=True)
            if conversation:
                connection.execute(query_update_conversation(), (new_message_id, datetime.utcnow(), conversation[0]))
                print(conversation[0])
            else:
                connection.execute(query_insert_conversation(), (sender_id, receiver_id, new_message_id, datetime.utcnow()))

            connection.execute(query_fetch_sender_username(), (sender_id,))
            sender_result = connection.fetchone(buffered=True)
            sender_username = sender_result[0] if sender_result else 'Unknown'

            response = {
                'sender_username': sender_username,
                'content': content
            }
            return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()
   
    