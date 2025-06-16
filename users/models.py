from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
# MyModels
# Create your models here.

LANG_CHOICES = (
    ('ru', 'Русский'),
    ('en', 'Английский'),
    ('kz', 'Казахский'),
)


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
    # bids = models.ManyToManyField(Bid, null=True, blank=True)
    role = models.CharField(max_length=255, choices=choices, default=AUTHOR)
    languages = MultiSelectField(choices=LANG_CHOICES, default='ru')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.languages}"



