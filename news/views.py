from django.shortcuts import render, redirect

from django.http import Http404
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import News

from .weather import get_weather


current_city = "Saint Petersburg"


class StartView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class LogInView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "news/login_page.html", context={'is_authenticated': request.user.is_authenticated})
        else:
            return redirect('/news/')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/news/')
        else:
            return render(request, "news/login_page.html", context={'error': True, 'is_authenticated': request.user.is_authenticated})


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "news/signup_page.html", context={'is_authenticated': request.user.is_authenticated})
        else:
            return redirect('/news/')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_again = request.POST['password_again']

        if username in [item[0] for item in User.objects.values_list('username')]:
            return render(request, "news/signup_page.html", context={'is_authenticated': request.user.is_authenticated, 'username_error_exists': True})
        if username in [item[0] for item in User.objects.values_list('email')]:
            return render(request, "news/signup_page.html", context={'is_authenticated': request.user.is_authenticated, 'email_error_exists': True})
        if len(password) < 8 or password.isnumeric():
            return render(request, "news/signup_page.html", context={'is_authenticated': request.user.is_authenticated, 'password_error': True})
        if password != password_again:
            return render(request, "news/signup_page.html", context={'is_authenticated': request.user.is_authenticated, 'password_again_error': True})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('/login/')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        ordered_data = News.objects.order_by('-created')
        return render(request, "news/news_page.html", context={'data': ordered_data, 'weather': get_weather(city=current_city), 'is_authenticated': request.user.is_authenticated})
    
    def post(self, request, *args, **kwargs):
        city = request.POST.get('city')
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
        specific_news.created += get_weather(city=current_city)['timezone']
        return render(request, "news/specific_news_page.html", context={'specific_news': specific_news, 'is_authenticated': request.user.is_authenticated})


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
