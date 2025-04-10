from django.db import models

# My Models
from files.models import File
# Create your models here.


class Article(models.Model):
    file = models.FileField(upload_to='articles/', null=True, blank=True)  # <-- сюда будет загружаться файл
    #PDF
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    annotation = models.TextField(null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)