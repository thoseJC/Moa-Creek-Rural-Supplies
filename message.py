from datetime import datetime
from urllib import request

from flask import Blueprint, flash, redirect, url_for, jsonify, render_template, session, request
from cursor import getConection, getCursor
from login_helper import getUserInfo
from message_helper import get_receiver_id, process_conversation, process_message
from message_query import  query_inbox_with_customer_id, query_inbox_with_staff_id, query_update_order_status, send_email, query_conversation, query_insert_message, query_select_conversation, query_update_conversation, query_insert_conversation


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
    msg = {
        "success" : "",
        "message" : ""
    }
    user = getUserInfo()
    if 'user_id' not in session:
        return redirect(url_for('login_page.login'))
    try:
        user_id = session['user_id']
        user = getUserInfo()
        connection = getCursor()
        query_sql = query_inbox_with_customer_id() if user["user_role"] == "customer"  else query_inbox_with_staff_id()
        connection.execute(query_sql, (user_id,))
        conversations = connection.fetchall()
        if len(conversations) == 0:
            msg = {
                "success" : True,
                "message" : "No Conversation in Inbox"
            }
        else:
            processed_conversation = process_conversation(conversations)
            return render_template('inbox.html', conversations=processed_conversation, msg = msg,user =user,noMessage = False)
        return render_template('inbox.html', conversations=[], msg = msg,user =user ,noMessage = True)

    except Exception as e:
        return jsonify({'error': str(e)}), 400



@message_page.route('/conversation', methods=['GET', 'POST'])
def conversation():
    conversation_id = request.args.get('conversation_id')
    user = getUserInfo()
    current_user_id = user["user_id"]
    if 'user_id' not in session:
        return redirect(url_for('login_page.login'))
    
    try:
        connection = getCursor()
        connection.execute(query_conversation(), (conversation_id,))
        messages = connection.fetchall()
        processed_message = process_message(messages)
        msg_receiver_id_id = get_receiver_id(messages, current_user_id)
        return render_template('conversation.html', messages=processed_message, msg_receiver_id_id= msg_receiver_id_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@message_page.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login_page.login'))
    sender_id = session['user_id']
    
    sender_username = session["user_name"]
    receiver_id = request.form.get('receiver_id')
    content = request.form.get('content')

    try:
        connec =  getConection()
        connection = connec.cursor()
        connection.execute(query_insert_message(), (sender_id, receiver_id, content, datetime.utcnow(), 'sent'))
        new_message_id = connection.lastrowid
        # Update or create conversation  
        connection.execute(query_select_conversation(), (sender_id, receiver_id, receiver_id, sender_id))
        conversation = connection.fetchall()
        
        if conversation:
            connection.execute(query_update_conversation(), (new_message_id, datetime.utcnow(), conversation[0][0]))
        else:
            connection.execute(query_insert_conversation(), (sender_id, receiver_id, new_message_id, datetime.utcnow()))
        response = {                
                "sender_user_name":sender_username,
                'content': content,
                'send_time' : datetime.utcnow()
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


   
    