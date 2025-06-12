from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from articles.models import Article
# Models
from users.models import CustomUser
from .models import Bid, BidStatus, Review, ReviewStatus
from bid.forms import BidForm
from articles.forms import ArticleCreateForm, ArticleUpdateForm
from .forms import ReviewForm, CommentBid
from django.views.generic.edit import CreateView
from .models import ArticleVersion
# Create your views here.
from .components import send_to_recent
from django.db.models import Q
from permissions.redactor import RedactorRequiredMixin
from permissions.reviewer import ReviewRequiredMixin
from permissions.Author import BidAccessPermissionMixin
from django.core.exceptions import PermissionDenied
from components.email import send_html_email
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


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
            reviews = Review.objects.filter(reviewer=request.user)
            context["reviews"] = reviews
            return render(request, template_name="bid/reviewer/bid-list.html", context=context)

        return render(request, template_name=self.template_name, context=context)


class BidDetailViewRedactor(RedactorRequiredMixin, DetailView):
    model = Bid
    template_name = "bid/redactor/edit-request.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status == BidStatus.SUBMITTED:
            self.object.status = BidStatus.EDITOR_REVIEW
            self.object.save()

        reviews = Review.objects.filter(bid=self.object)
        reviewer = CustomUser.objects.filter(role=CustomUser.REVIEWER)
        context = self.get_context_data(object=self.object)
        comment_form = CommentBid()
        context["comment_form"] = comment_form
        context["reviews"] = reviews
        context["reviewer"] = reviewer

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        comment = request.POST.get("comment")

        bid_obj = self.get_object()
        if comment:
            bid_obj.comment = comment
        if not bid_obj.status == BidStatus.SENT_FOR_REVIEW and decision == "approve":
            bid_obj = send_to_recent(request, bid_obj)
        if decision == "reject":
            bid_obj.status = BidStatus.REJECTED
            bid_obj.save()
        if decision == "revision":
            bid_obj.status = BidStatus.NEEDS_REVISION
            bid_obj.save()
        if decision == "accept":
            bid_obj.status = BidStatus.ACCEPTED
            bid_obj.save()
        return redirect("my_bids")


class BidDetailViewReviewer(BidAccessPermissionMixin, UpdateView):
    model = Review
    template_name = "bid/reviewer/edit-request.html"
    form_class = ReviewForm
    success_url = reverse_lazy("my_bids")

    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        print(decision)
        if decision == 'save':
            self.object.status = ReviewStatus.SAVED
            self.object.save()
        if decision == 'submit':
            self.object.status = ReviewStatus.SUBMITTED
            self.object.save()
        return super().post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.responsible = self.request.user

        self.object.bid.status = BidStatus.EDITOR_REVIEW
        self.object.bid.save()
        return super().form_valid(form)


class UpdateBidView(BidAccessPermissionMixin, UpdateView):
    template_name = "bid/edit-request.html"
    model = Bid
    fields = ["manuscript", "authors_file", "cover_letter", "ai_usage_details"]

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().status not in [BidStatus.SUBMITTED, BidStatus.NEEDS_REVISION, BidStatus.REJECTED, BidStatus.PUBLISHED] and request.user.role == CustomUser.AUTHOR:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_form'] = kwargs.get('article_form') or ArticleUpdateForm(instance=self.object.article)
        context['bid_form'] = kwargs.get('bid_form') or self.get_form()
        print(context['article_form'].files)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        article_form = ArticleUpdateForm(request.POST, request.FILES)
        bid_form = self.get_form()

        if article_form.is_valid() and bid_form.is_valid():
            return self.forms_valid(article_form, bid_form)
        else:
            return self.form_invalid(article_form, bid_form)

    def forms_valid(self, article_form, bid_form):
        new_article = article_form.save(commit=False)

        if not article_form.cleaned_data.get('file'):
            new_article.file = self.object.article.file
            new_article.plagiarism = self.object.article.plagiarism

        new_article.user = self.request.user
        new_article.save()

        bid = bid_form.save(commit=False)
        ArticleVersion(article=new_article, bid=bid).save()

        bid.article = new_article
        bid.status = BidStatus.SUBMITTED
        bid.save()

        return redirect(self.get_success_url())

    def form_invalid(self, article_form, bid_form):
        return self.render_to_response(self.get_context_data(
            article_form=article_form,
            bid_form=bid_form
        ))

    def get_success_url(self):
        return reverse('my_bids')  # или "/dashboard/"


class ReviewDetailView(RedactorRequiredMixin, DetailView):
    model = Review
    template_name = "bid/reviewer/review-detail.html"


@csrf_exempt
def assign_reviewer(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Get ID from templates
        reviewer_id = data.get('reviewer_id')
        reviewer = CustomUser.objects.get(pk=reviewer_id)

        # Get objects in orm
        bid_id = data.get('bid_id')
        bid_obj = Bid.objects.get(id=bid_id)

        # Create obj review
        Review.objects.create(reviewer=reviewer, bid=bid_obj)

        return JsonResponse({'message': f'Рецензент с ID {reviewer_id} назначен.'})

    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)