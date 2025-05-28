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

    def form_valid(self, form):

        article = form.save()
        article.user = self.request.user

        return super().form_valid(form)
