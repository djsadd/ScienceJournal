from django.db import models

# Create your models here.
from ckeditor.fields import RichTextField


class Category(models.Model):
    title_eng = models.CharField(max_length=255)
    title_kk = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)


class News(models.Model):
    title_eng = models.CharField(max_length=255)
    title_kk = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    description_eng = RichTextField(null=True, blank=True)
    description_kk = RichTextField(null=True, blank=True)
    description_ru = RichTextField(null=True, blank=True)
    image = models.ImageField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    date = models.DateField()



