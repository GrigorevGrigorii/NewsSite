from django.urls import path
from .views import NewsAPI, CommentsAPI, UserAPI

urlpatterns = [
    path('news/', NewsAPI.as_view()),
    path('comments/', CommentsAPI.as_view()),
    path('user/', UserAPI.as_view()),
]
