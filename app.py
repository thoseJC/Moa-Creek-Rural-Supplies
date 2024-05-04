from flask import Flask
from flask import render_template
<<<<<<< Updated upstream
app = Flask(__name__)
=======

from cursor import getCursor
>>>>>>> Stashed changes

from customer import customer_page

app = Flask(__name__)

# blueprint registration:
app.register_blueprint(customer_page, url_prefix="/customer")


@app.route("/")
def home():
    return render_template('global/index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
