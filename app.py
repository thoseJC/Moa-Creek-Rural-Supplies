from flask import Flask
app = Flask(__name__)
from auth import hashPassword, getSalt
from cursor import getCursor


@app.route("/")
def home():
    return "Hello, Flask!"