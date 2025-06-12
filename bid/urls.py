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
from .views import BidListView, UpdateBidView, BidDetailViewRedactor, BidDetailViewReviewer, ReviewDetailView, assign_reviewer


urlpatterns = [
    path("my/", BidListView.as_view(), name="my_bids"),
    path("edit/<int:pk>", UpdateBidView.as_view(), name="edit-request"),
    path("request/<int:pk>", BidDetailViewRedactor.as_view(), name="edit-request-redactor"),
    path("request-review/<int:pk>", BidDetailViewReviewer.as_view(), name="edit-request-reviewer"),
    path("review/<int:pk>", ReviewDetailView.as_view(), name="review-detail"),
    path("assign_reviewer/", assign_reviewer, name="assign_reviewer"),
]
