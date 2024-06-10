def process_conversation(conversations):
	cons_list = []
	for conv in conversations:
		conv_obj = {
			"conversation_id" : conv[0],
			"customer_id" : conv[1],
			"last_message_id" : conv[3],
			"last_update_at" : conv[4],
			"cust_full_name" : conv[5]+ " " + conv[6],
			"cust_login_name" : conv[7]
		}
		cons_list.append(conv_obj)
	return cons_list

def process_message(messages):
	message_list = []
	for msg in messages:
		msg_obj = {
			"message_id" : msg[0],
			"content" : msg[3],
			"send_time" : msg[4],
			"sender_username" : msg[6],
			"receiver_username" : msg[7],
			"sender_role_name" : msg[8]
		}
		message_list.append(msg_obj)
	return message_list

def get_receiver_id(messages, current_user_id):
	first_msg = messages[0]
	if first_msg[1] != current_user_id:
		return first_msg[1]
	else:
		return first_msg[2]



