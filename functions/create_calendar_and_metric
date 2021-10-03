import pandas as pd
import random
from datetime import date, timedelta


def cal(len_days, int1=1, int2=20, last_date=date.today()):
    """Function returns len_days days and a random number assigned to it
    len_days: len of the df
    int1: minimum integer from which random int will be generated
    int2: maximum integer until which random int will be generated
    int1 and int2 define the range of integers from which random numbers will
    generated
    last_date: the date from which len_days days will be created. Defaults to current date
    """
    global df
    last_date = pd.to_datetime(last_date, format='%Y-%m-%d')
    dates = []
    counter = 0
    while counter <= len_days:
        d = last_date - timedelta(days=counter)
        dates.append(d)
        counter += 1
    dates = [d.strftime('%Y-%m-%d') for d in dates]
    metric = [random.randint(int1, int2) for x in range(len(dates))]
    df = pd.DataFrame({'date': dates, 'metric': metric})
    return df
