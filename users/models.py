from django.contrib.auth.models import AbstractUser
from django.db import models

# MyModels
from bid.models import Bid
# Create your models here.


class CustomUser(AbstractUser):
    AUTHOR = "АВТОР"
    REDACTOR = "РЕДАКТОР"
    REVIEWER = "РЕЦЕНЗИСТ"

    choices = {
        AUTHOR: "АВТОР",
        REDACTOR: "РЕДАКТОР",
        REVIEWER: "РЕЦЕНЗИСТ",
    }

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bids = models.ManyToManyField(Bid, null=True, blank=True)
    role = models.CharField(max_length=255, choices=choices, default=AUTHOR)

