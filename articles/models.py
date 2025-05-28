from django.db import models
from ckeditor.fields import RichTextField

# My Models
from files.models import File
# Create your models here.


class Category(models.Model):
    title_en = models.CharField(max_length=255, null=True, blank=True)
    title_kk = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title_ru}"


class Article(models.Model):
    file = models.FileField(upload_to='articles/', null=True, blank=True)  # <-- сюда будет загружаться файл
    #PDF
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    title_kk = models.CharField(max_length=255, null=True, blank=True)
    title_ru = models.CharField(max_length=255, null=True, blank=True)
    annotation = RichTextField(null=True, blank=True)
    annotation_kk = RichTextField(null=True, blank=True)
    annotation_ru = RichTextField(null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True, blank=True)
