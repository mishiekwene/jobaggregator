from django.urls import path
from . import views


app_name = 'main'
urlpatterns=[
    path('', views.HomeView.as_view(), name='home'),
    path('search', views.SearchView.as_view(), name='search'),
    path('search-index', views.suggest_api, name='search-index'),
    path('filter', views.FilterView.as_view(), name='filter')
]