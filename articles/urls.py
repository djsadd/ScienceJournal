from django.urls import path

# My Views
from .views import Dashboard


urlpatterns = [
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
