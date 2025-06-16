from django.contrib.auth.models import AbstractUser
from django.db import models

# MyModels
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

    KZ = "Казахский"
    RU = "Русский"
    ENG = "Английский"

    choices_lang = {
        KZ: "Казахский",
        RU: "Русский",
        ENG: "Английский",
    }

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # bids = models.ManyToManyField(Bid, null=True, blank=True)
    role = models.CharField(max_length=255, choices=choices, default=AUTHOR)
    language = models.CharField(max_length=255, choices=choices_lang, default=RU)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



