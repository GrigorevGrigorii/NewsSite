from django.shortcuts import render, redirect

from django.http import Http404
from django.views import View

from .models import News, Comments

from .weather import get_weather


current_city = "Saint Petersburg"


class StartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        ordered_data = News.objects.order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': get_weather(city=current_city), 'is_authenticated': request.user.is_authenticated})
    
    def post(self, request, *args, **kwargs):
        city = request.POST.get('city')
        if city == "":
            return redirect('/news/')
        if get_weather(city=city) is None:
            ordered_data = News.objects.order_by('-created')
            return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': None})
        else:
            global current_city
            current_city = city
            return redirect('/news/')


class SpecificNewsView(View):
    def get(self, request, link, *args, **kwargs):
        specific_news = News.objects.filter(link=link).first()
        if not specific_news:
            raise Http404
        tz = get_weather(city=current_city)['timezone']
        specific_news.created += tz
        comments = Comments.objects.filter(news=specific_news).order_by('-created')
        for comment in comments:
            comment.created += tz
        return render(request, "news/specific_news_page.html", context={'specific_news': specific_news, 'is_authenticated': request.user.is_authenticated, 'comments': comments})

    def post(self, request, link, *args, **kwargs):
        specific_news = News.objects.filter(link=link).first()
        if not specific_news:
            raise Http404
        text = request.POST.get('text_of_comment').strip()
        if text == "":
            comments = Comments.objects.filter(news=specific_news).order_by('-created')
            return render(request, "news/specific_news_page.html", context={'specific_news': specific_news, 'is_authenticated': request.user.is_authenticated, 'comments': comments, 'error_empty': True})
        if len(text) > 256:
            comments = Comments.objects.filter(news=specific_news).order_by('-created')
            return render(request, "news/specific_news_page.html", context={'specific_news': specific_news, 'is_authenticated': request.user.is_authenticated, 'comments': comments, 'error_too_long': True})

        if request.user.is_authenticated:
            Comments.objects.create(text=text, user=request.user, news=specific_news)
        else:
            Comments.objects.create(text=text, news=specific_news)

        return redirect(f'/news/{link}/')


class SearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q').rstrip('/')
        ordered_data_with_q = News.objects.filter(title__contains=q).order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data_with_q, 'weather': get_weather(current_city), 'is_authenticated': request.user.is_authenticated})
    
    def post(self, request, *args, **kwargs):
        q = request.POST.get('q')
        if q:
            return redirect('/news/search?q={}/'.format(q))
        else:
            return redirect('/news/')


class CreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_page.html", context={'is_authenticated': request.user.is_authenticated})
    
    def post(self, request, *args, **kwargs):
        text = request.POST.get('text').strip()
        title = request.POST.get('title').strip()
        if text == "" and title == "":
            return render(request, "news/create_page.html", context={'is_authenticated': request.user.is_authenticated, 'error_empty_text': True, 'error_empty_title': True})
        if text == "":
            return render(request, "news/create_page.html", context={'is_authenticated': request.user.is_authenticated, 'error_empty_text': True})
        if title == "":
            return render(request, "news/create_page.html", context={'is_authenticated': request.user.is_authenticated, 'error_empty_title': True})
        
        all_links = list(News.objects.values_list('link', flat=True).order_by('link'))
        if all_links:
            for existing_link in all_links:
                if existing_link + 1 not in all_links:
                    link = existing_link + 1
                    break
        else:
            link = 1
        
        if request.user.is_authenticated:
            News.objects.create(text=text, title=title, link=link, user=request.user)
        else:
            News.objects.create(text=text, title=title, link=link)
        
        return redirect('/news/')
