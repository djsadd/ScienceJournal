
from django.contrib import admin
from django.urls import path, include

# My Views
from .views import NewsListView, NewsDetailView


urlpatterns = [
    path("list/", NewsListView.as_view(), name="list-news"),
    path("detail/<int:pk>", NewsDetailView.as_view(), name="detail-news"),
]
