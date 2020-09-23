import requests
from datetime import datetime, timedelta


class Weather:
    current_weather = None
    start_time = None

    def __init__(self, number_of_minutes_for_update=2):
        self.number_of_minutes_for_update = number_of_minutes_for_update

    def get_weather(self, city='Saint Petersburg'):
        if Weather.current_weather is None or datetime.now() - Weather.start_time > timedelta(
                minutes=self.number_of_minutes_for_update):
            r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                             {'q': city, 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
            data = r.json()
            weather = dict()
            weather['name'] = data['name']
            weather['description'] = data['weather'][0]['description']
            weather['temp'] = round(data['main']['temp'] - 273.15, 2)
            weather['feels_like'] = round(data['main']['feels_like'] - 273.15, 2)
            weather['pressure'] = round(data['main']['pressure'] * 0.750062, 2)
            weather['humidity'] = data['main']['humidity']
            weather['wind_speed'] = round(data['wind']['speed'] * 3.6, 2)

            Weather.start_time = datetime.now()
            Weather.current_weather = weather

            return weather
        else:
            return Weather.current_weather


if __name__ == "__main__":
    weather = Weather()
    print(weather.get_weather())
