from django.urls import path

# My Views
from .views import Dashboard, RedactorArticleCreateView, create_tag_api


urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("redactor/create/", RedactorArticleCreateView.as_view(), name="redactor_article_create"),
    path("redactor/api/tag/create/", create_tag_api, name="redactor_tag_create"),
]
