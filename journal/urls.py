"""
URL configuration for ScienceJournal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# My Views
from .views import (SearchPublicationView, CollectionListView, CollectionDetailView, ContactsView, AboutView, ForAuthorsView,
                    BidDetailView, EditorialView, PublicationView, Editorial_boardView, Requirements_articlesView,statementView,
                    regulationsView, copyrightView, CollectionRedactorListView, CollectionCreateView, CollectionEditView)

urlpatterns = [
    path("", AboutView.as_view(), name="home"),
    path("search/", SearchPublicationView.as_view(), name="search_publications"),
    path("collection/", CollectionListView.as_view(), name="collection"),
    path("collection_redactor/", CollectionRedactorListView.as_view(), name="collection_redactor_list"),
    path("collection_redactor/create/", CollectionCreateView.as_view(), name="collection_create"),
    path("collection_redactor/<int:pk>/edit/", CollectionEditView.as_view(), name="collection_edit"),
    path("collection-detail/<int:pk>", CollectionDetailView.as_view(), name="collection_detail"),
    path("article-detail/<int:pk>", BidDetailView.as_view(), name="article_detail"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("about/", AboutView.as_view(), name="about"),
    path("editorial/", EditorialView.as_view(), name="editorial"),
    path("editorial_board/", Editorial_boardView.as_view(), name="editorial_board"),
    path("requirements_articles/", Requirements_articlesView.as_view(), name="requirements"),
    path("publication/", PublicationView.as_view(), name="publication"),
    path("statement/", statementView.as_view(), name="statement"),
    path("regulations/", regulationsView.as_view(), name="regulations"),
    path("copyright/", copyrightView.as_view(), name="copyright"),
    path("for-authors/", ForAuthorsView.as_view(), name="for_authors"),
]
