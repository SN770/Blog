def is_valid_name(name):
    if len(name) == 0:
        return False

    for i in name:
        if not (i.lower() >= 'a' and i.lower() <= 'z'):
            return False
    return True

def is_valid_surname(surname):
    if len(surname) == 0:
        return False

    for i in surname:
        if not (i.lower() >= 'a' and i.lower() <= 'z'):
            return False
    return True

def is_valid_age(age):
    digits = '1234567890'
    for age in digits:
        if age not in digits and len(age) > 2:
            return False
        else:
            return True

def is_valid_username(username):
    digits = '1234567890'
    
    if len(username) == 0:
        return False

    if username[0] in digits:
        return False

    for i in username:
        if not (i.lower() >= 'a' and i.lower() <= 'z' or i in digits or i == '_'):
            return False

    return True
    
def is_valid_password(password):
    digits = '1234567890'

    if len(password) < 8:
        return -1
    
    for i in password:
        if not (i.lower() >= 'a' and i.lower() <= 'z' or i in digits or i == '_'):
            return 0

    return 1

def is_exist (users, username):
    for user in users:
        if user.username == username:
            return True
    return False

def is_valid_email(email):
    if '@' in email:
        return True
    return False