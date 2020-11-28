from django.urls import path

from .views import *

urlpatterns = [
    path('', NewsView.as_view()),
    path('create/', CreateView.as_view()),
    path('search', SearchView.as_view()),
    path('<int:link>/', SpecificNewsView.as_view()),
]
