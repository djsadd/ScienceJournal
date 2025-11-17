from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
from .models import Collection
from bid.models import Bid, BidStatus
from articles.models import Article
from permissions.redactor import RedactorRequiredMixin
from users.models import CustomUser

from django.db.models import Q


class CollectionRedactorListView(RedactorRequiredMixin, ListView):
    model = Collection
    template_name = "journal/redactor/collection_list.html"


class CollectionCreateView(RedactorRequiredMixin, CreateView):
    model = Collection
    template_name = "journal/redactor/collection_form.html"
    fields = ["title", "description", "layout"]
    success_url = reverse_lazy("collection_redactor_list")


class SearchPublicationView(ListView):
    template_name = 'journal/main.html'
    model = Bid
    paginate_by = 6

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
        context['query'] = self.request.GET.get("q", "")
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


class CollectionEditView(RedactorRequiredMixin, DetailView):
    model = Collection
    template_name = "journal/redactor/collection_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        collection = self.get_object()
        context["bids_in_collection"] = Bid.objects.filter(collection=collection)
        context["available_bids"] = Bid.objects.filter(collection__isnull=True, status=BidStatus.PUBLISHED)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = request.POST.get("action")
        # Сохранение вёрстки тома
        if action == "save_layout":
            layout_file = request.FILES.get("layout")
            if layout_file:
                self.object.layout = layout_file
                self.object.save()
                messages.success(request, "Вёрстка тома сохранена.")
            else:
                messages.error(request, "Файл вёрстки не выбран.")
            return redirect("collection_edit", pk=self.object.pk)

        bid_id = request.POST.get("bid_id")

        if not bid_id:
            messages.error(request, "Не выбрана статья.")
            return redirect("collection_edit", pk=self.object.pk)

        bid = get_object_or_404(Bid, pk=bid_id)

        if action == "add":
            bid.collection = self.object
            bid.save()
            messages.success(request, "Статья добавлена в том.")
        elif action == "remove":
            if bid.collection_id == self.object.pk:
                bid.collection = None
                bid.save()
                messages.success(request, "Статья убрана из тома.")
        else:
            messages.error(request, "Неизвестное действие.")

        return redirect("collection_edit", pk=self.object.pk)


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
        board_members = CustomUser.objects.filter(is_editorial_board=True, is_active=True).order_by('last_name', 'first_name')
        council_members = CustomUser.objects.filter(is_editorial_council=True, is_active=True).order_by('last_name', 'first_name')
        context = {
            "page_title": "Editorial_board",
            "board_members": board_members,
            "council_members": council_members,
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


