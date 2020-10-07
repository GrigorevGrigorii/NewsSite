import requests
from datetime import datetime, timedelta


class Weather:
    city_and_weather = dict()

    def __init__(self, number_of_minutes_for_update=1):
        self.number_of_minutes_for_update = number_of_minutes_for_update

    def get_weather(self, city="Saint Petersburg"):
        if city not in Weather.city_and_weather.keys() or datetime.now() - Weather.city_and_weather[city]['start_time'] > timedelta(minutes=self.number_of_minutes_for_update):
            r = requests.get('https://api.openweathermap.org/data/2.5/weather', {'q': city, 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
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

            Weather.city_and_weather[city] = dict()
            Weather.city_and_weather[city]['weather'] = weather
            Weather.city_and_weather[city]['start_time'] = datetime.now()

            return weather
        else:
            return Weather.city_and_weather[city]['weather']


if __name__ == "__main__":
    weather = Weather()
    print(weather.get_weather())
