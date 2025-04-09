from django.shortcuts import render
from django.views.generic.list import ListView

# Models
from .models import Bid
# Create your views here.


class BidListView(ListView):
    model = Bid
    template_name = "bid/requests.html"
