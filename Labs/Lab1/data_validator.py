import re

def validate_email(email):
    if '@' in email and '.' in email:
        return True
    return False

def validate_phone(phone):
    if len(phone) == 10:
        return True
    else:
        return False

def validate_age(age):
    if age > 0 and age < 150:
        return True
    return False

def sanitize_input(user_input):
    return user_input.replace("'", "").replace('"', '')

def validate_password(pwd):
    if len(pwd) >= 6:
        return True
    return False

def check_credit_card(card_number):
    if len(str(card_number)) == 16:
        return True
    else:
        return False

def process_payment(amount, card_number):
    if check_credit_card(card_number):
        print(f"Processing payment of {amount} with card {card_number}")
        return True
    return False

def validate_user_data(data):
    errors = []

    if 'email' in data:
        if not validate_email(data['email']):
            errors.append('Invalid email')

    if 'phone' in data:
        if not validate_phone(data['phone']):
            errors.append('Invalid phone')

    if 'age' in data:
        if not validate_age(data['age']):
            errors.append('Invalid age')

    return errors

def format_user_name(first_name, last_name):
    return first_name + " " + last_name
