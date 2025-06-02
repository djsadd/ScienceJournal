from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
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
from .forms import BidReviewForm
from .models import ArticleVersion
# Create your views here.
from .components import send_to_recent
from django.db.models import Q


class BidListView(LoginRequiredMixin, ListView):
    model = Bid
    template_name = "bid/requests.html"
    login_url = '/users/login/'
    paginate_by = 3

    def get_paginate_by(self, queryset):
        if self.request.user.role == CustomUser.REDACTOR:
            return 10
        return 3

    def get_queryset(self):
        if self.request.user.role == CustomUser.REDACTOR:
            return super().get_queryset()

        if self.request.user.role == CustomUser.REVIEWER:
            return super().get_queryset().filter(
                Q(status=BidStatus.SENT_FOR_REVIEW) | Q(status=BidStatus.RE_REVIEW)
            )

        queryset = super().get_queryset()
        return queryset.filter(responsible=self.request.user)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        if self.request.user.role == CustomUser.REDACTOR:
            return render(request, template_name="bid/redactor/bid-list.html", context=context)

        if self.request.user.role == CustomUser.REVIEWER:
            return render(request, template_name="bid/reviewer/bid-list.html", context=context)

        return render(request, template_name=self.template_name, context=context)


class BidDetailViewRedactor(DetailView):
    model = Bid
    template_name = "bid/redactor/edit-request.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status == BidStatus.SUBMITTED:
            self.object.status = BidStatus.EDITOR_REVIEW
            self.object.save()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        bid_obj = self.get_object()
        if not bid_obj.status == BidStatus.SENT_FOR_REVIEW and decision == "approve":
            bid_obj = send_to_recent(request, bid_obj)
        if decision == "reject":
            bid_obj.status = BidStatus.REJECTED
            bid_obj.save()
        if decision == "accept":
            bid_obj.status = BidStatus.ACCEPTED
            bid_obj.save()
        return redirect("my_bids")


class BidDetailViewReviewer(UpdateView):
    model = Bid
    template_name = "bid/reviewer/edit-request.html"
    form_class = BidReviewForm
    success_url = reverse_lazy("my_bids")  # замените на нужный URL


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
