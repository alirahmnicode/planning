import datetime


def calculate_term(term):
    now = datetime.datetime.now()
    if term == 'year':
        expiration = now + datetime.timedelta(days=365)
    elif term == 'month':
        expiration = now + datetime.timedelta(days=30)
    else:
        expiration = now + datetime.timedelta(days=7)
    return expiration