from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from articles.models import Article
# Models
from users.models import CustomUser
from .models import Bid, BidStatus
from bid.forms import BidForm
from articles.forms import ArticleCreateForm, ArticleUpdateForm
from .models import ArticleVersion
# Create your views here.


class BidListView(LoginRequiredMixin, ListView):
    model = Bid
    template_name = "bid/requests.html"
    login_url = '/users/login/'
    paginate_by = 3

    def get_paginate_by(self, queryset):
        if self.request.user.role == CustomUser.REDACTOR:
            return 10  # например, для редактора показывать по 10 заявок
        return 3  # для остальных — по 3

    def get_queryset(self):
        if self.request.user.role == CustomUser.REDACTOR:
            return super().get_queryset()

        queryset = super().get_queryset()
        return queryset.filter(responsible=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if self.request.user.role == CustomUser.REDACTOR:
            return render(request, template_name="bid/redactor/bid-list.html", context=context)

        return render(request, template_name=self.template_name, context=context)


class BidDetailView(DetailView):
    model = Bid
    template_name = "bid/redactor/edit-request.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status == BidStatus.SUBMITTED:
            self.object.status = BidStatus.EDITOR_REVIEW
            self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UpdateBidView(UpdateView):
    template_name = "bid/edit-request.html"
    model = Bid
    fields = ["manuscript", "authors_file", "cover_letter", "ai_usage_details"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_form'] = kwargs.get('article_form') or ArticleUpdateForm(instance=self.object.article)
        context['bid_form'] = kwargs.get('bid_form') or self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # текущий Bid

        # не передаём instance — создаём новую статью
        article_form = ArticleUpdateForm(request.POST, request.FILES)
        bid_form = self.get_form()

        if article_form.is_valid() and bid_form.is_valid():
            return self.forms_valid(article_form, bid_form)
        else:
            return self.form_invalid(article_form, bid_form)

    def forms_valid(self, article_form, bid_form):
        new_article = article_form.save(commit=False)
        new_article.user = self.request.user
        new_article.save()

        bid = bid_form.save(commit=False)
        ArticleVersion(article=new_article, bid=bid).save()

        bid.article = new_article
        bid.save()

        return redirect(self.get_success_url())

    def form_invalid(self, article_form, bid_form):
        return self.render_to_response(self.get_context_data(
            article_form=article_form,
            bid_form=bid_form
        ))

    def get_success_url(self):
        return reverse('my_bids')  # или "/dashboard/"
