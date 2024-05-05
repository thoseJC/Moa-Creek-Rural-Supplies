import re

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(pattern, email))

def is_valid_phone_number(phone_number):
    pattern = re.compile(r"(\+\d{1,3})?\s?\(?\d{1,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
    match = re.search(pattern, phone_number)
    return bool(match)


