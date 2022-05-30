import requests
from datetime import datetime, timedelta
from pyowm import OWM

y_day = datetime.now() - timedelta(1)

today = datetime.today().strftime('%Y-%m-%d')
yesterday = datetime.strftime(y_day, '%Y-%m-%d')


def currency(code):
    curr_dict = {}
    curr_y_req = requests.get(f'https://cbu.uz/uz/arkhiv-kursov-valyut/json/{code}/{yesterday}/').json()
    curr_t_req = requests.get(f'https://cbu.uz/uz/arkhiv-kursov-valyut/json/{code}/{today}/').json()

    curr_yesterday = curr_y_req[0].get('Rate')
    curr_now = curr_t_req[0].get('Rate')

    if curr_yesterday > curr_now:
        curr_dict['status'] = 0
    else:
        curr_dict['status'] = 1
    curr_dict['price'] = round(float(curr_now), 2)
    return curr_dict


def get_weather():
    weather = {}

    owm = OWM('97989a5a3956ea1a0d3bd23253be1646')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Tashkent,UZ')
    w = observation.weather

    tashkent_celsius = w.temperature('celsius')['temp']
    weather_status = w.status

    weather['temp'] = tashkent_celsius
    weather['status'] = weather_status

    return weather
