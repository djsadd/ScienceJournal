from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from articles.models import Article
# Models
from users.models import CustomUser
from .models import Bid, BidStatus
# Create your views here.


class BidListView(LoginRequiredMixin, ListView):
    model = Bid
    template_name = "bid/requests.html"
    login_url = '/users/login/'

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
    fields = ["status"]
    # form_class =
