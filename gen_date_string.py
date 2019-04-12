import datetime


def gen_date_string():
    # Generate text
    now = datetime.datetime.now()

    day = now.strftime('%d')       # 05
    month = now.strftime('%B')[:5] # first 5 characters of month 'Novem'
    year = now.strftime('%Y')      # 2019
    return day + '\n' + month + '\n' + year