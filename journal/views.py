from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from .models import Collection
from bid.models import Bid
from articles.models import Article
from django.db.models import Q


class JournalView(ListView):
    template_name = 'journal/main.html'
    model = Bid
    paginate_by = 3

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Bid.objects.published().filter(
                Q(article__title_ru__iregex=query) |
                Q(article__authors__iregex=query) |
                Q(article__category__title_ru__iregex=query)
                # Q(article__title_kz__icontains=query)
            )
        return Bid.objects.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class CollectionListView(ListView):
    model = Collection
    template_name = "journal/archives.html"
    paginate_by = 3


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "journal/collection_detail.html"


class BidDetailView(DetailView):
    model = Bid
    template_name = "journal/article_detail.html"


class ContactsView(View):
    template_name = "journal/contacts.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Contacts"
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "journal/about.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Contacts"
        }
        return render(request, self.template_name, context)


class ForAuthorsView(View):
    template_name = "journal/authors.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Contacts"
        }
        return render(request, self.template_name, context)


