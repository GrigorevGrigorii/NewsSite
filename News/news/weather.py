import requests
import datetime


class Weather:
    current_weather = None
    start_time = datetime.datetime.now()

    def __init__(self, number_of_minutes_for_update=1):
        self.number_of_minutes_for_update = number_of_minutes_for_update

    @staticmethod
    def get_weather():
        if datetime.datetime.now() - Weather.start_time > datetime.timedelta(minutes=3) or Weather.current_weather is None:
            r = requests.get('https://api.openweathermap.org/data/2.5/weather', {'q': 'Saint Petersburg', 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
            data = r.json()
            weather = dict()
            weather['name'] = data['name']
            weather['description'] = data['weather'][0]['description']
            weather['temp'] = round(data['main']['temp'] - 273.15, 2)
            weather['feels_like'] = round(data['main']['feels_like'] - 273.15, 2)
            weather['pressure'] = round(data['main']['pressure'] * 0.750062, 2)
            weather['humidity'] = data['main']['humidity']
            weather['wind_speed'] = round(data['wind']['speed'] * 3.6, 2)

            Weather.current_weather = weather

            return weather
        else:
            return Weather.current_weather


if __name__ == "__main__":
    weather = Weather()
    print(weather.get_weather())

