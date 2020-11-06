from django.urls import path
from .views import StartView, SpecificNewsView, NewsView, CreateView, SearchView, LogInView, SignUpView, LogoutView

urlpatterns = [
    path('', NewsView.as_view()),
    path('create/', CreateView.as_view()),
    path('search', SearchView.as_view()),
    path('<int:link>/', SpecificNewsView.as_view()),
]
