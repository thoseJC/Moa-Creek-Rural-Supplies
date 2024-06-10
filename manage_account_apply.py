from flask import Blueprint, render_template, redirect, url_for, flash, session, request
import mysql.connector
import connect

manage_account_apply_page = Blueprint('manage_account_apply', __name__)

def getDictCursor():
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=False
    )
    return connection, connection.cursor(dictionary=True)

@manage_account_apply_page.route("/dashboard", methods=['GET'])
def dashboard():
    if not session.get('logged_in') or session.get("user_role") != 'manager':
        flash('You must be logged in as a manager to access this page.', 'error')
        return redirect(url_for('login_page.login'))

    connection, cursor = getDictCursor()
    try:
        cursor.execute("""
            SELECT user_id, username, first_name, last_name, business_name, account_holder, credit_limit
            FROM users WHERE account_holder != 'init'
        """)
        applications = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template("manager/manage_account_apply.html", applications=applications)

@manage_account_apply_page.route("/approve/<user_id>", methods=['POST'])
def approve_application(user_id):
    if session.get("user_role") != 'manager':
        flash('Unauthorized', 'error')
        return redirect(url_for('manage_account_apply.dashboard'))

    credit_limit = request.form.get('credit_limit')  
    
    if update_application_status(user_id, 'approved', credit_limit):
        flash('Application approved successfully.', 'success')
    else:
        flash('Failed to approve application.', 'error')
    return redirect(url_for('manage_account_apply.dashboard'))

@manage_account_apply_page.route("/reject/<user_id>", methods=['POST'])
def reject_application(user_id):
    if session.get("user_role") != 'manager':
        flash('Unauthorized', 'error')
        return redirect(url_for('manage_account_apply.dashboard'))

    if update_application_status(user_id, 'declined'):
        flash('Application rejected successfully.', 'success')
    else:
        flash('Failed to reject application.', 'error')
    return redirect(url_for('manage_account_apply.dashboard'))

def update_application_status(user_id, status, credit_limit=None):
    connection, cursor = getDictCursor()
    try:
        if status == 'approved' and credit_limit is not None:
            cursor.execute("""
                UPDATE users
                SET account_holder = %s, credit_limit = %s
                WHERE user_id = %s
            """, (status, credit_limit, user_id))
        else:
            cursor.execute("""
                UPDATE users
                SET account_holder = %s
                WHERE user_id = %s
            """, (status, user_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error updating application status: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()
