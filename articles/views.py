from django.shortcuts import redirect
from django.views.generic import FormView

# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# My Models
from bid.models import BidStatus, ArticleVersion

# Forms
from .forms import ArticleCreateForm
from bid.forms import BidForm
from users.models import CustomUser
# Views


class Dashboard(LoginRequiredMixin, FormView):
    template_name = "articles/dashboard.html"
    form_class = ArticleCreateForm
    success_url = "/articles/my/"
    login_url = '/users/login/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (
                request.user.role == CustomUser.REDACTOR or request.user.role == CustomUser.REVIEWER
        ):
            return redirect("my_bids")

        return super().dispatch(request, *args, **kwargs)

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