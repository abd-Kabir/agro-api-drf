from datetime import datetime

import pandas as pd


def check_days_year(date):
    p = pd.Period(date.strftime("%Y %m %d"))
    if p.is_leap_year:
        days = 366
    else:
        days = 365
    return days


def date_transform(response_list, data, model_date):
    date_type = datetime.strptime(response_list[data][model_date], '%Y-%m-%d')
    formatted = date_type.strftime('%d.%m.%Y')
    return formatted
