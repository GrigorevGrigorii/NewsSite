from django.urls import path, include

from .views import *


urlpatterns = [
    path('login/', LogInView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('', include('social_django.urls', namespace='social')),
]
