from django.db import models

# My Models
from files.models import File
# Create your models here.


class Article(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    #PDF
    title = models.CharField(max_length=255, null=True, blank=True)
    annotation = models.TextField(null=True, blank=True)
    authors = models.TextField(null=True, blank=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)