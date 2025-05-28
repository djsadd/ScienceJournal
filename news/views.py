from django.shortcuts import render
from .models import News
from django.views.generic.list import ListView

# Create your views here.


class NewsListView(ListView):
    model = News
    template_name = "news/news-list.html"
