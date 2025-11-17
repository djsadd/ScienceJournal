from django.shortcuts import redirect
from django.views.generic import FormView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from components.tasks import send_html_email_task
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# My Models
from bid.models import BidStatus, ArticleVersion, BidVersion
from django.contrib import messages
# Forms
from .forms import ArticleCreateForm
from bid.forms import BidForm
from users.models import CustomUser
from articles.models import Tag
# Views


class Dashboard(LoginRequiredMixin, FormView):
    template_name = "articles/dashboard.html"
    form_class = ArticleCreateForm
    success_url = "/articles/dashboard/"
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_active:
            messages.error(request, 'Произошла ошибка.')
            return redirect("home")
        if request.user.is_authenticated and (
                request.user.role == CustomUser.REDACTOR or request.user.role == CustomUser.REVIEWER
        ):
            return redirect("my_bids")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bid_form'] = BidForm(self.request.POST or None, self.request.FILES or None)
        context['tag_list'] = Tag.objects.all()
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
