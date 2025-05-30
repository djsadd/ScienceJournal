from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# My Models
from .models import Article
from bid.models import Bid, BidStatus, ArticleVersion
# Forms
from .forms import ArticleCreateForm
from bid.forms import BidForm
# Create your views here.


class MyArticles(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 10
    template_name = "articles/articles.html"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BidForm()  # Передаём форму в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = BidForm(request.POST, request.FILES)
        if form.is_valid():
            bid = form.save(commit=False)
            print(form, "VALID")
            article_id = request.POST.get("article_id")
            article = Article.objects.get(pk=article_id)
            bid.article = article

            bid.status = BidStatus.SUBMITTED
            bid.responsible = request.user
            bid.save()

            return redirect("my_bids")
        else:
            print("Форма недействительна:", form.errors)
            return self.get(request, *args, **kwargs)  # Или верни с ошибкой


class Dashboard(LoginRequiredMixin, FormView):
    template_name = "dashboard.html"
    form_class = ArticleCreateForm
    success_url = "/articles/my/"
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bid_form'] = BidForm(self.request.POST or None, self.request.FILES or None)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        article_form = self.get_form()
        bid_form = BidForm(request.POST, request.FILES)

        if article_form.is_valid() and bid_form.is_valid():
            return self.forms_valid(article_form, bid_form)
        else:
            return self.form_invalid(article_form)

    def forms_valid(self, article_form, bid_form):
        article = article_form.save(commit=False)
        article.user = self.request.user
        article.save()

        bid = bid_form.save(commit=False)
        bid.article = article
        bid.status = BidStatus.SUBMITTED
        bid.responsible = self.request.user
        bid.save()
        ArticleVersion(article=article, bid=bid).save()

        return super().form_valid(article_form)