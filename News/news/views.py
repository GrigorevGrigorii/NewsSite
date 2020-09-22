from django.shortcuts import render, redirect

from django.http import Http404
from django.views import View

from news.models import News

import requests


def get_weather():
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', {'q': 'Saint Petersburg', 'appid': '9f7ad1eebe97cba2c8ebb5dd08ab3a52'})
    data = r.json()
    weather = {}
    weather['name'] = data['name']
    weather['description'] = data['weather'][0]['description']
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
        ordered_data = News.objects.order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': get_weather()})


class SpecificNewsPage(View):
    def get(self, request, link, *args, **kwargs):
        specific_news = News.objects.filter(link=link).first()
        if not specific_news:
            raise Http404
        return render(request, "news/specific_news_page.html", context={'specific_news': specific_news})


class SearchPage(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').rstrip('/')
        ordered_data_with_q = News.objects.filter(title__contains=q).order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data_with_q, 'weather': get_weather()})
    
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
        text = request.POST.get('text')
        title = request.POST.get('title')
        
        all_links = list(News.objects.values_list('link', flat=True).order_by('link'))
        if all_links:
            for existing_link in all_links:
                if existing_link + 1 not in all_links:
                    link = existing_link + 1
                    break
        else:
            link = 1

        News.objects.create(text=text, title=title, link=link)
        
        return redirect('/news/')
