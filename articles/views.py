from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
# My Models
from .models import Article
# Create your views here.


class MyArticles(ListView):
    model = Article
    paginate_by = 10
    template_name = "articles/articles.html"


class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard.html', {
            'user': request.user
        })