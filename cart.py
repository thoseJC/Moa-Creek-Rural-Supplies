from flask import Blueprint, session, render_template

cart_page = Blueprint("cart", __name__, static_folder="static", template_folder="templates/cart")

@cart_page.route("/")
def cart():
    user_id = 0
    if session.get("user_id"):
        user_id = session.get("user_id")
    return render_template('global/cart.html', user_id = user_id)
