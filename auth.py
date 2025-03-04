from app import app
from flask_hashing import Hashing
from flask import render_template, session


hashing = Hashing(app)
app.secret_key = 'gemini'

def hashPassword(userInput):
        return hashing.hash_value(userInput, salt="kiwi")

def checkHashingValue(hashedPassword, passwordToCheck):
        return hashing.check_value(hashedPassword,passwordToCheck, salt="kiwi")

def getSalt():
        return "kiwi"

def checkLogin():
        if session.get("loggedin") != True:
                return render_template("/login.html")


