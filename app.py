from flask import Flask
from flask import render_template
app = Flask(__name__)
from auth import hashPassword, getSalt
from cursor import getCursor


@app.route("/")
def home():
    return render_template('global/index.html')