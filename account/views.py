from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class LogInView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "account/login_page.html", context={'is_authenticated': request.user.is_authenticated})
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
            return render(request, "account/login_page.html",
                          context={'error': True, 'is_authenticated': request.user.is_authenticated})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/news/')


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "account/signup_page.html", context={'is_authenticated': request.user.is_authenticated})
        else:
            return redirect('/news/')

    def post(self, request, *args, **kwargs):
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        password_again = request.POST['password_again']

        if username == "":
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'username_error_empty': True})
        if email == "":
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'email_error_empty': True})
        if username in [item[0] for item in User.objects.values_list('username')]:
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'username_error_exists': True})
        if len(username) > 150:
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'username_error_too_long': True})
        if username in [item[0] for item in User.objects.values_list('email')]:
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'email_error_exists': True})
        if len(password) < 8 or password.isnumeric():
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'password_error': True})
        if password != password_again:
            return render(request, "account/signup_page.html",
                          context={'is_authenticated': request.user.is_authenticated, 'password_again_error': True})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('/login/')
