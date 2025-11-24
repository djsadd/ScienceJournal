from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.translation import gettext as _

from components.tasks import send_html_email_task
from permissions.redactor import RedactorRequiredMixin

from bid.forms import BidForm
from bid.models import BidStatus, ArticleVersion, BidVersion
from users.models import CustomUser
from articles.models import Tag
from .forms import ArticleCreateForm


class BaseArticleBidCreateView(LoginRequiredMixin, FormView):
    """
    Общий обработчик для создания статьи и связанной заявки.
    Используется автором и редактором.
    """

    form_class = ArticleCreateForm
    login_url = '/users/login/'

    def get_bid_form(self):
        return BidForm(self.request.POST or None, self.request.FILES or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bid_form'] = kwargs.get('bid_form') or self.get_bid_form()
        context['tag_list'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        article_form = self.get_form()
        bid_form = self.get_bid_form()
        if article_form.is_valid() and bid_form.is_valid():
            return self.forms_valid(article_form, bid_form)
        return self.form_invalid(article_form, bid_form)

    def form_invalid(self, article_form, bid_form):
        return self.render_to_response(self.get_context_data(
            form=article_form,
            bid_form=bid_form
        ))

    def forms_valid(self, article_form, bid_form):
        article = article_form.save(commit=False)
        article.user = self.request.user
        article.save()
        article_form.save_m2m()
        article_form.attach_new_tags(article)

        bid = bid_form.save(commit=False)
        bid.article = article
        bid.status = BidStatus.SUBMITTED
        bid.responsible = self.request.user
        bid.save()
        bid_version = BidVersion.objects.create(
            bid=bid,
            comment=bid.comment,
            exclusive_submission=bid.exclusive_submission,
            ai_usage_details=bid.ai_usage_details,
            manuscript=bid.manuscript,
            authors_file=bid.authors_file,
            cover_letter=bid.cover_letter,
        )
        ArticleVersion(article=article, bid_version=bid_version).save()

        send_html_email_task.delay(
            "?'?????? ??????????? ????????????? ???'?????????>?????!",
            self.request.user.email,
            "email/request-add.html",
            context={
                "user": {"first_name": self.request.user.first_name},
                "article": {"title": article.title},
            },
        )

        return super().form_valid(article_form)


class Dashboard(BaseArticleBidCreateView):
    template_name = "articles/dashboard.html"
    success_url = "/articles/dashboard/"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_active:
            messages.error(request, '�?�?�?����?�?�>�� �?�?��+���.')
            return redirect("home")
        if request.user.is_authenticated and request.user.role == CustomUser.REDACTOR:
            return redirect("redactor_article_create")
        if request.user.is_authenticated and request.user.role == CustomUser.REVIEWER:
            return redirect("my_bids")

        return super().dispatch(request, *args, **kwargs)


class RedactorArticleCreateView(RedactorRequiredMixin, BaseArticleBidCreateView):
    template_name = "articles/redactor/create.html"
    success_url = reverse_lazy("redactor_article_create")


@require_POST
def create_tag_api(request):
    """
    Create a new tag with translations for editors.
    """
    if not request.user.is_authenticated or request.user.role != CustomUser.REDACTOR:
        return JsonResponse({"error": _("Недостаточно прав")}, status=403)

    name_ru = (request.POST.get("name_ru") or "").strip()
    name_en = (request.POST.get("name_en") or "").strip()
    name_kk = (request.POST.get("name_kk") or "").strip()

    if not name_ru:
        return JsonResponse({"error": _("Укажите ключевое слово на русском")}, status=400)

    tag, created = Tag.objects.get_or_create(name=name_ru)
    # Populate translation fields if provided
    if name_en:
        setattr(tag, "name_en", name_en)
    if name_kk:
        setattr(tag, "name_kk", name_kk)
    tag.save()

    return JsonResponse({
        "id": tag.id,
        "name": tag.name,
        "name_ru": getattr(tag, "name_ru", tag.name),
        "name_en": getattr(tag, "name_en", ""),
        "name_kk": getattr(tag, "name_kk", ""),
        "created": created,
    })
