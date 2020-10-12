import requests
from datetime import datetime, timedelta


def get_weather(city="Saint Petersburg"):
    r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                     {'q': city, 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
    if r.status_code != 200:
        return None

    data = r.json()
    weather = dict()
    weather['name'] = data['name']
    weather['description'] = data['weather'][0]['description']
    weather['temp'] = round(data['main']['temp'] - 273.15, 2)
    weather['feels_like'] = round(data['main']['feels_like'] - 273.15, 2)
    weather['pressure'] = round(data['main']['pressure'] * 0.750062, 2)
    weather['humidity'] = data['main']['humidity']
    weather['wind_speed'] = round(data['wind']['speed'] * 3.6, 2)
    weather['timezone'] = timedelta(seconds=data['timezone'])

    return weather


if __name__ == "__main__":
    print(get_weather())
