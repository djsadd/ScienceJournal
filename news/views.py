from django.shortcuts import render
from .models import News
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

# Create your views here.


class NewsListView(ListView):
    model = News
    template_name = "news/news-list.html"
    paginate_by = 3


class NewsDetailView(DetailView):
    model = News
    template_name = "news/news-detail.html"
