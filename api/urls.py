from django.urls import path
from .views import NewsAPI, CommentsAPI

urlpatterns = [
    path('news/', NewsAPI.as_view()),
    path('comments/', CommentsAPI.as_view()),
]
