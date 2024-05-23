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


 