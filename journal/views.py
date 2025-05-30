from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.
from .models import Collection


class JournalView(View):
    template_name = 'journal/main.html'

    def get(self, request):
        return render(request, self.template_name, {
            'user': request.user
        })


class CollectionListView(ListView):
    model = Collection
    template_name = "journal/archives.html"
    paginate_by = 3


class CollectionDetailView(DetailView):
    model = Collection
    template_name = "journal/collection_detail.html"


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