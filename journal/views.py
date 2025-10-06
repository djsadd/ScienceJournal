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
                Q(article__title_en__iregex=query) |
                Q(article__title_kk__iregex=query) |
                Q(article__authors__iregex=query) |
                Q(article__authors_kk__iregex=query) |
                Q(article__authors_en__iregex=query) |
                Q(article__category__title_ru__iregex=query) |
                Q(article__category__title_kk__iregex=query) |
                Q(article__category__title_en__iregex=query)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bids"] = Bid.objects.filter(collection=self.get_object())
        return context


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

class EditorialView(View):
    template_name = "journal/editorial_policy.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Editorial"
        }
        return render(request, self.template_name, context)
    
class PublicationView(View):
    template_name = "journal/publication_ethics.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Publication"
        }
        return render(request, self.template_name, context)
    
class Editorial_boardView(View):
    template_name = "journal/editorial_board.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Editorial_board"
        }
        return render(request, self.template_name, context)
    
class Requirements_articlesView(View):
    template_name = "journal/Requirements.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Requitements"
        }
        return render(request, self.template_name, context)

class statementView(View):
    template_name = "journal/statement.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "statement"
        }
        return render(request, self.template_name, context)

class regulationsView(View):
    template_name = "journal/regulations.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "regulations"
        }
        return render(request, self.template_name, context)
    
class copyrightView(View):
    template_name = "journal/copyright_agreement.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "copyright"
        }
        return render(request, self.template_name, context)
    
class ForAuthorsView(View):
    template_name = "journal/authors.html"

    def get(self, request, *args, **kwargs):
        context = {
            "page_title": "Contacts"
        }
        return render(request, self.template_name, context)


