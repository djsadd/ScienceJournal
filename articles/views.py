from django.shortcuts import render
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views import View

# My Models
from .models import Article

# Forms
from .forms import ArticleCreateForm
# Create your views here.


class MyArticles(ListView):
    model = Article
    paginate_by = 10
    template_name = "articles/articles.html"

    def get_queryset(self):
        return self.model.objects.all()


class Dashboard(FormView):
    template_name = "dashboard.html"
    form_class = ArticleCreateForm
    success_url = "/articles/my/"

    def form_valid(self, form):

        article = form.save()
        article.user = self.request.user

        return super().form_valid(form)
