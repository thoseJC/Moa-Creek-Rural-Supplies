from email.mime.text import MIMEText
import smtplib


def query_update_order_status():
    return """
        SELECT u.email, u.first_name, o.order_id, o.status 
        FROM users u 
        JOIN orders o ON u.user_id = o.user_id 
        WHERE u.user_id = %s
        """


def send_email(recipient, subject, body):
    sender = "hchw311@gmail.com"
    password = "ohsg dntm wnrs ybbp"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()

def query_inbox_with_staff_id():
    return """
    SELECT c.*, u.first_name, u.last_name, u.username FROM conversations c left join users u on u.user_id = c.customer_id
    WHERE c.staff_id = %s;
    """

def query_inbox_with_customer_id():
    return """
    SELECT c.*, u.first_name, u.last_name, u.username FROM conversations c left join users u on u.user_id = c.staff_id
    WHERE c.customer_id = %s;
    """

def query_conversation():
    return """
SELECT messages.*, 
       sender.username AS sender_username, 
       receiver.username AS receiver_username, 
       sender_role.role_name AS sender_role_name,
       receiver_role.role_name AS receiver_role_name
FROM messages
LEFT JOIN users AS sender ON messages.sender_id = sender.user_id
LEFT JOIN users AS receiver ON messages.receiver_id = receiver.user_id
LEFT JOIN user_roles AS sender_role ON sender.role_id = sender_role.role_id
LEFT JOIN user_roles AS receiver_role ON receiver.role_id = receiver_role.role_id
WHERE messages.message_id IN (
    SELECT message_id 
    FROM conversations 
    WHERE conversation_id = %s
)
ORDER BY messages.created_at;

    """


def query_check_receiver():
    return """
    SELECT * FROM users WHERE user_id = %s
    """

def query_insert_message():
    return """
        INSERT INTO messages (sender_id, receiver_id, content, created_at, status) 
        VALUES (%s, %s, %s, %s, %s)
    """

def query_select_conversation():
    return """
        SELECT * FROM conversations 
        WHERE (customer_id = %s AND staff_id = %s) 
           OR (customer_id = %s AND staff_id = %s)
    """

def query_update_conversation():
    return """
            UPDATE conversations 
            SET last_message_id = %s, updated_at = %s 
            WHERE conversation_id = %s
    """

def query_insert_conversation():
    return """
            INSERT INTO conversations (customer_id, staff_id, last_message_id, updated_at) 
            VALUES (%s, %s, %s, %s)
    """
def query_fetch_sender_username():
    return """
            SELECT username FROM users WHERE users.user_id = %s
    """

 