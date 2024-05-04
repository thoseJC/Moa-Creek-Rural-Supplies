from flask import Blueprint, render_template
from cursor import getCursor

customer_page = Blueprint('customer', __name__, static_folder="static", template_folder="templates/customer")


@customer_page.route('/categories')
def categories():
  return render_template('categories.html')

