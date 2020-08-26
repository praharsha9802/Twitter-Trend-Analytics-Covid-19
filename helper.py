from datetime import timedelta, date, datetime

def daterange(start_date, end_date, flag):
    start_date = formatDate(start_date, flag)
    end_date = formatDate(end_date, flag)
    days = int((end_date - start_date).days)
    for n in range(days):
        if not flag:
            yield (start_date + timedelta(n)).strftime('%Y-%m-%d'), (start_date + timedelta(n+1)).strftime('%Y-%m-%d')
        else:
            yield (start_date + timedelta(n)).strftime('%d-%m-%Y'), (start_date + timedelta(n + 1)).strftime('%d-%m-%Y')


def formatDate(date, flag):
    if not flag:
        tDate = datetime.strptime(date, '%Y-%m-%d')
    else:
        tDate = datetime.strptime(date, '%d-%m-%Y')
    return tDate.date()