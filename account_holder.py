from flask import Blueprint, request, render_template, flash, redirect, session, url_for
import mysql.connector
import connect

account_holder = Blueprint('account_holder', __name__)

def getDictCursor():
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=False
    )
    return connection, connection.cursor(dictionary=True)

@account_holder.route("/apply_account_holder", methods=['GET', 'POST'])
def apply_account_holder():
    if not session.get('user_id'):
        flash('You need to login to apply.', 'warning')
        return redirect(url_for('login_page.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        connection, cursor = getDictCursor()
        try:
            business_name = request.form['business_name']
            tax_number = request.form['tax_number']
            credit_check = request.form.get('credit_check', 'off') == 'on'
            print(f"Applying with: {business_name}, {tax_number}, {credit_check}")

            cursor.execute("""
                UPDATE users
                SET business_name = %s, tax_employer_number = %s, credit_check = %s, account_holder = 'applied'
                WHERE user_id = %s
            """, (business_name, tax_number, bool(credit_check), user_id))
            connection.commit()
            print("Update committed")
            flash('Your account holder application has been submitted successfully!')
            return redirect(url_for('account_holder.apply_account_holder')) 
        except Exception as e:
            connection.rollback()
            print(f"Failed to submit application: {str(e)}")
            flash(f'Failed to submit application: {str(e)}', 'error')
            return redirect(url_for('account_holder.apply_account_holder'))  


    connection, cursor = getDictCursor()
    try:
        cursor.execute("""
            SELECT account_holder
            FROM users
            WHERE user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        account_holder_status = result["account_holder"] if result else None
    except Exception as e:
        print(e)
        

    user = {
        "user_id": user_id,
        "account_holder_status": account_holder_status
    }

    return render_template('customer/apply_account_holder.html', user=user)