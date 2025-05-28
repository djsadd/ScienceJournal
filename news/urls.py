
from django.contrib import admin
from django.urls import path, include

# My Views
from .views import NewsListView


urlpatterns = [
    path("list/", NewsListView.as_view(), name="list-news"),
]
