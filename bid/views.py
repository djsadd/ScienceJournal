from journal.models import Collection
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from articles.models import Article
# Models
from .mixins import BidAccessMixin
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from users.models import CustomUser
from .models import Bid, BidStatus, Review, ReviewStatus
from bid.forms import BidForm
from articles.forms import ArticleCreateForm, ArticleUpdateForm
from .forms import ReviewForm, CommentBid, UploadLayoutFile
from django.views.generic.edit import CreateView
from .models import ArticleVersion, BidVersion
# Create your views here.
from .components import send_to_recent
from django.db.models import Q
from permissions.redactor import RedactorRequiredMixin
from permissions.reviewer import ReviewRequiredMixin
from permissions.Author import BidAccessPermissionMixin
from django.core.exceptions import PermissionDenied
from components.tasks import send_html_email_task
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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
            reviews = Review.objects.filter(reviewer=request.user, is_active=True)
            context["reviews"] = reviews
            return render(request, template_name="bid/reviewer/bid-list.html", context=context)

        return render(request, template_name=self.template_name, context=context)


class BidDetailViewRedactor(RedactorRequiredMixin, DetailView):
    model = Bid
    template_name = "bid/redactor/edit-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Пример: добавляем ещё одну форму
        context['extra_form'] = UploadLayoutFile()
        return context

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
        bid_obj = self.get_object()

        if "save_layout" in request.POST:
            layout_form = UploadLayoutFile(request.POST, request.FILES, instance=bid_obj.article)
            print(request.FILES)
            if layout_form.is_valid():
                layout_form.save()
                return redirect("edit-request-redactor", bid_obj.pk)

        decision = request.POST.get('decision')
        comment = request.POST.get("comment")

        bid_obj = self.get_object()

        if comment:
            bid_obj.comment = comment
            messages.success(self.request, 'Комментарии успешно оставлен!')
        if not bid_obj.status == BidStatus.SENT_FOR_REVIEW and decision == "approve":
            bid_obj = send_to_recent(request, bid_obj)
        if decision == "reject":
            bid_obj.status = BidStatus.REJECTED
            bid_obj.save()
            messages.success(self.request, 'Статья успешно отклонена!')
        if decision == "revision":
            bid_obj.status = BidStatus.NEEDS_REVISION
            bid_obj.save()
            messages.success(self.request, 'Статья успешно отправлена на доработку!')
            if bid_obj.responsible and bid_obj.responsible.email:
                article_title = getattr(bid_obj.article, "title_ru", None) or bid_obj.article.title
                send_html_email_task.delay(
                    f"Ваша статья «{article_title}» отправлена на доработку",
                    bid_obj.responsible.email,
                    "email/request-revision.html",
                    context={
                        "user": {"first_name": bid_obj.responsible.first_name},
                        "article": {"title": article_title},
                    },
                )
        if decision == "accept":
            return redirect("collection-redactor", bid_pk=bid_obj.pk)
            # bid_obj.status = BidStatus.ACCEPTED
            # bid_obj.save()
        return redirect(request.path)


class BidDetailViewReviewer(BidAccessPermissionMixin, UpdateView):
    model = Review
    template_name = "bid/reviewer/edit-request.html"
    form_class = ReviewForm
    success_url = reverse_lazy("my_bids")

    def post(self, request, *args, **kwargs):
        decision = request.POST.get('decision')
        if decision == 'save':
            self.object.status = ReviewStatus.SAVED
            self.object.save()
        if decision == 'submit':
            self.object.set_submit()
            return redirect("my_bids")
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
        allowed_statuses = [
            BidStatus.DRAFT,
            BidStatus.SUBMITTED,
            BidStatus.NEEDS_REVISION,
            BidStatus.REJECTED,
            BidStatus.PUBLISHED,
        ]
        if (
            request.user.role == CustomUser.AUTHOR
            and self.get_object().status not in allowed_statuses
        ):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_form'] = kwargs.get('article_form') or ArticleUpdateForm(instance=self.object.article)
        context['bid_form'] = kwargs.get('bid_form') or self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        article_form = ArticleUpdateForm(request.POST, request.FILES)
        obj = self.object
        old_bid = BidVersion.objects.create(
            bid=obj,
            comment=obj.comment,
            exclusive_submission=obj.exclusive_submission,
            ai_usage_details=obj.ai_usage_details,
            manuscript=obj.manuscript,
            authors_file=obj.authors_file,
            cover_letter=obj.cover_letter,
        )
        old_bid.save()
        bid_form = self.get_form()

        if article_form.is_valid() and bid_form.is_valid():
            return self.forms_valid(article_form, bid_form, old_bid)
        else:
            return self.form_invalid(article_form, bid_form)

    def forms_valid(self, article_form, bid_form, old_bid):
        new_article = article_form.save(commit=False)
        if not article_form.cleaned_data.get('file'):
            new_article.file = self.object.article.file
            new_article.plagiarism = self.object.article.plagiarism

        new_article.user = self.request.user
        new_article.save()

        bid = bid_form.save(commit=False)
        ArticleVersion(article=new_article, bid_version=old_bid).save()

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


@login_required(login_url='/users/login/')
def withdraw_bid(request, pk):
    """
    Allow the responsible author to withdraw a submitted bid back to draft.
    """
    if request.method != "POST":
        return HttpResponseForbidden()

    bid_obj = get_object_or_404(Bid, pk=pk)

    if bid_obj.responsible != request.user:
        raise PermissionDenied()

    if bid_obj.status == BidStatus.SUBMITTED:
        bid_obj.status = BidStatus.DRAFT
        bid_obj.save()
        messages.success(request, "Заявка отозвана и переведена в черновик.")
    else:
        messages.error(request, "Эту заявку нельзя отозвать.")

    return redirect("my_bids")


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
        old_reviews = Review.objects.filter(bid_id=bid_id, reviewer_id=reviewer_id)

        if bid_obj.status == BidStatus.PUBLISHED:
            return JsonResponse({'message': f'Рецензент с ID {reviewer_id} не может быть назначен так как статья уже находится в публикации.'})

        for row in old_reviews:
            if row.status != ReviewStatus.SUBMITTED:
                return JsonResponse({'message': f'Рецензент с ID {reviewer_id} не назначен, так как он еще не опубликовал рецензию на эту статью.'})

        # Create obj review
        review = Review.objects.create(reviewer=reviewer, bid=bid_obj)

        review_url = reverse('edit-request-reviewer', args=[review.id])
        review_link = request.build_absolute_uri(review_url)

        send_html_email_task.delay(
            f"?'???? ?????????????>?? ????O???????: {bid_obj.article.title_ru}",
            reviewer.email,
            "email/review-add.html",
            context={
                "user": {"first_name": reviewer.first_name},
                "article": {"title": bid_obj.article.title},
                "review_link": review_link
            },
        )

        return JsonResponse({'message': f'Рецензент с ID {reviewer_id} назначен.'})

    return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


class BidDetailView(BidAccessPermissionMixin, DetailView):
    model = Bid
    template_name = "bid/view-request.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.request.user.role == CustomUser.REDACTOR:
            context['reviews'] = Review.objects.filter(bid=self.object)
        return context


class BidVersionList(DetailView):
    model = Bid
    template_name = "bid/redactor/version-list.html"


class BidVersionDetailView(DetailView):
    model = BidVersion
    template_name = "bid/redactor/version_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        bid_version = self.get_object()
        article_version = ArticleVersion.objects.get(bid_version=bid_version)
        context["article_version"] = article_version
        return context


class CollectionRedactorListView(BidAccessMixin, ListView):
    model = Collection
    template_name = "bid/redactor/collection-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bid_pk = self.kwargs['bid_pk']
        context['bid'] = Bid.objects.get(pk=bid_pk)  # Чтобы в шаблоне отобразить данные заявки
        return context


def select_collection_bid(request, bid_pk, collection_pk):
    if request.user.role == CustomUser.REDACTOR:
        bid_obj = Bid.objects.get(pk=bid_pk)
        collection_obj = Collection.objects.get(pk=collection_pk)
        bid_obj.collection = collection_obj
        bid_obj.status = BidStatus.PUBLISHED
        bid_obj.published_at = now().date()
        bid_obj.save()
        send_html_email_task.delay(
            f"?'?????? ???'???'???? {bid_obj.article.title_ru} ????????????? ???????+?>????????????! ?'?<????????: {collection_obj.title}",
            request.user.email,
            "email/request-add.html",
            context={
                "user": {"first_name": request.user.first_name},
                "article": {"title": bid_obj.article.title},
                "collection": {"title": collection_obj.title},
            },
        )

        return redirect("my_bids")


def inactive_review(request, review_pk):

    if request.user.role == CustomUser.REDACTOR:
        obj = get_object_or_404(Review, id=review_pk)
        if obj.bid.status == BidStatus.PUBLISHED:
            messages.error(request, "Данная статья уже опубликована")
            return redirect("edit-request-redactor", obj.bid.pk)
        obj.is_active = False
        obj.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

