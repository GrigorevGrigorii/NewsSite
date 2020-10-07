from django.shortcuts import render, redirect

from django.http import Http404
from django.views import View

from .models import News

from .weather import Weather


weather_class = Weather()
current_city = "Saint Petersburg"


class StartPage(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsPage(View):
    def get(self, request, *args, **kwargs):
        ordered_data = News.objects.order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': weather_class.get_weather(city=current_city)})
    
    def post(self, request, *args, **kwargs):
        city = request.POST.get('city')
        if weather_class.get_weather(city=city) is None:
            ordered_data = News.objects.order_by('-created')
            return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': None})
        else:
            global current_city
            current_city = city
            return redirect('/news/')


class SpecificNewsPage(View):
    def get(self, request, link, *args, **kwargs):
        specific_news = News.objects.filter(link=link).first()
        if not specific_news:
            raise Http404
        specific_news.created += weather_class.get_weather(city=current_city)['timezone']
        return render(request, "news/specific_news_page.html", context={'specific_news': specific_news})


class SearchPage(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').rstrip('/')
        ordered_data_with_q = News.objects.filter(title__contains=q).order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data_with_q, 'weather': weather_class.get_weather(current_city)})
    
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
