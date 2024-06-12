from flask import Blueprint, request, render_template, flash, redirect, session, url_for
import mysql.connector
import connect

shipping_address = Blueprint('shipping_address', __name__)

def getDictCursor():
    connection = mysql.connector.connect(
        user=connect.dbuser,
        password=connect.dbpass,
        host=connect.dbhost,
        database=connect.dbname,
        autocommit=False
    )
    return connection, connection.cursor(dictionary=True)

@shipping_address.route("/shipping_info")
def shipping_info():
    return render_template('shipping/shipping_information.html')

@shipping_address.route('/add_address', methods=['GET', 'POST'])
def add_address():
    if not session.get('user_id'):
        flash('You need to login to add an address.', 'warning')
        return redirect(url_for('login_page.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        connection, cursor = getDictCursor()
        try:
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state = request.form.get('state')
            postal_code = request.form.get('postal_code')
            country = request.form.get('country')
            is_primary = request.form.get('is_primary') == 'on'

            if is_primary:
                cursor.execute("""
                    UPDATE address SET is_primary = %s
                    WHERE user_id = %s AND is_primary = %s
                """, (False, user_id, True))

            cursor.execute("""
                INSERT INTO address (user_id, street_address, city, state, postal_code, country, is_primary)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, street_address, city, state, postal_code, country, is_primary))
            connection.commit()
            flash('Address added successfully!')
            return redirect(url_for('shipping_address.manage_addresses', user_id=user_id))
        except Exception as e:
            flash(f'Failed to add address: {str(e)}')
            return render_template('shipping/add_address.html', error=str(e))
    return render_template('shipping/add_address.html')

@shipping_address.route('/manage_addresses/<user_id>', methods=['GET'])
def manage_addresses(user_id):
    connection, cursor = getDictCursor()
    try:
        cursor.execute("SELECT * FROM address WHERE user_id = %s", (user_id,))
        addresses = cursor.fetchall()
        return render_template('shipping/manage_addresses.html', addresses=addresses, user_id=user_id)
    except Exception as e:
        connection.rollback()
        flash(f'Failed to delete address: {str(e)}')


@shipping_address.route('/update_address/<int:address_id>', methods=['GET', 'POST'])
def update_address(address_id):
    connection, cursor = getDictCursor()
    try:
        if request.method == 'POST':
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state = request.form.get('state')
            postal_code = request.form.get('postal_code')
            country = request.form.get('country')
            is_primary_value = request.form.get('is_primary')
            is_primary = 1 if is_primary_value == 'true' else 0


            cursor.execute("""
                UPDATE address SET
                street_address = %s,
                city = %s,
                state = %s,
                postal_code = %s,
                country = %s,
                is_primary = %s
                WHERE address_id = %s
            """, (street_address, city, state, postal_code, country, is_primary, address_id))
            connection.commit()
            flash('Address updated successfully!')
            return redirect(url_for('shipping_address.manage_addresses', user_id=session.get('user_id')))
        else:
            cursor.execute("SELECT * FROM address WHERE address_id = %s", (address_id,))
            address = cursor.fetchone()
            if address:
                return render_template('shipping/update_address.html', address=address)
            else:
                flash('No address found.')
                return redirect(url_for('shipping_address.manage_addresses', user_id=session.get('user_id')))
    except Exception as e:
        connection.rollback()
        flash(f'Failed to update address: {str(e)}')
        return render_template('shipping/update_address.html', error=str(e), address_id=address_id)


@shipping_address.route('/delete_address/<int:address_id>', methods=['POST'])
def delete_address(address_id):
    connection, cursor = getDictCursor()
    try:
        cursor.execute("DELETE FROM address WHERE address_id = %s", (address_id,))
        connection.commit()
        flash('Address deleted successfully!')
    except Exception as e:
        connection.rollback()
        flash(f'Failed to delete address: {str(e)}')
    return redirect(url_for('shipping_address.manage_addresses', user_id=session.get('user_id')))

@shipping_address.route('/customer/dashboard', methods=['GET'])
def customer_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view this page.", "warning")
        return redirect(url_for('login'))

    connection, cursor = getDictCursor()
    try:
        cursor.execute("SELECT first_name, last_name, user_role, (SELECT COUNT(*) FROM orders WHERE user_id = %s) as order_count FROM users WHERE user_id = %s", (user_id, user_id))
        user = cursor.fetchone()

        cursor.execute("SELECT street_address, city, state, postal_code, country FROM address WHERE user_id = %s AND is_primary = '1'", (user_id,))
        primary_address = cursor.fetchone()

        return render_template('customer/dashboard.html', user=user, primary_address=primary_address)
    except Exception as e:
        flash(f"Error fetching data: {str(e)}", "error")
        return redirect(url_for('home'))
