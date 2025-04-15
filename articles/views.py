from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# My Models
from .models import Article
from bid.models import Bid, BidStatus
# Forms
from .forms import ArticleCreateForm
# Create your views here.


class MyArticles(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 10
    template_name = "articles/articles.html"
    login_url = '/users/login/'

    def post(self, request, *args, **kwargs):
        article_id = self.request.POST.get("article_id")
        article = Article.objects.get(pk=article_id)
        content = request.POST.get("content")
        bids = Bid(
            title=content,
            article=article
        )
        bids.status = BidStatus.SUBMITTED
        bids.save()
        return redirect('my_bids')


class Dashboard(LoginRequiredMixin, FormView):
    template_name = "dashboard.html"
    form_class = ArticleCreateForm
    success_url = "/articles/my/"
    login_url = '/users/login/'

    def form_valid(self, form):

        article = form.save()
        article.user = self.request.user

        return super().form_valid(form)
