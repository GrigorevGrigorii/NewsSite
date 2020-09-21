from django.shortcuts import render, redirect
from django.conf import settings

from django.http import Http404
from django.views import View

import json
from datetime import datetime
import requests


with open(settings.NEWS_JSON_PATH, 'r') as data_file:
    data = json.load(data_file)

def get_weather():
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', {'q': 'Saint Petersburg', 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
    data = r.json()
    weather = {}
    weather['name'] = data['name']
    weather['description'] = data['weather'][0]['description'][0].upper() + data['weather'][0]['description'][1:]
    weather['temp'] = round(data['main']['temp'] - 273.15, 2)
    weather['feels_like'] = round(data['main']['feels_like'] - 273.15, 2)
    weather['pressure'] = round(data['main']['pressure'] * 0.750062, 2)
    weather['humidity'] = data['main']['humidity']
    weather['wind_speed'] = round(data['wind']['speed'] * 3.6, 2)
    
    return weather


class StartPage(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/news_page.html", context={'data': data, 'weather': get_weather()})


class SpecificNewsPage(View):
    def get(self, request, link, *args, **kwargs):
        context = {}
        for item in data:
            if item['link'] == link:
                context = item
                break
        if not context:
            raise Http404
        return render(request, "news/specific_news_page.html", context=context)


class SearchPage(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').rstrip('/')
        data_with_q = list(filter(lambda news: q in news['title'], data))
        return render(request, "news/news_page.html", context={'data': data_with_q, 'weather': get_weather()})
    
    def post(self, request, *args, **kwargs):
        q = request.POST.get('q')
        if q:
            return redirect('/news/search?q={}/'.format(q))
        else:
            return redirect('/news/')


class CreatePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_page.html")
    
    def post(self, request, *args, **kwargs):
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = request.POST.get('text')
        title = request.POST.get('title')
        
        all_links = sorted([news['link'] for news in data])
        for existing_link in all_links:
            if existing_link + 1 not in all_links:
                link = existing_link + 1
                break
        
        new_news = {"created": created, "text": text, "title": title, "link": link}
        data.append(new_news)
        
        with open(settings.NEWS_JSON_PATH, 'w') as data_file:
            json.dump(data, data_file)
        
        return redirect('/news/')
