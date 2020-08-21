import re


def validate_name(name):
    if re.match(r'^[a-zA-Z]+$', name):
        return 'true'
    else:
        return 'false'


def validate_mail_id(mail_id):
    if re.match(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', mail_id):
        return 'true'
    else:
        return 'false'


def validate_phone_no(phone_no):
    if re.match(r'^\d{10}$', phone_no):
        return 'true'
    else:
        return 'false'


def confirm_password(password, confirm):
    if password == confirm:
        return 'true'
    else:
        return 'false'
