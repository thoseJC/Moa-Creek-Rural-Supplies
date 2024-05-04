from app import app
from flask_hashing import Hashing


hashing = Hashing(app)
app.secret_key = 'gemini'

def hashPassword(userInput):
        return hashing.hash_value(userInput, salt="kiwi")

def checkValue(hashedPassword, passwordToCheck):
        return hashing.check_value(hashedPassword,passwordToCheck, salt="kiwi")

def getSalt():
        return "kiwi"



