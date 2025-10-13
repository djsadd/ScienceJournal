from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
import os
# My Models


# Model for keywords of article
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# Model for categories of article
class Category(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


# Languages article
class LanguageChoicesArticle(models.TextChoices):
    RU = "Русский"
    KZ = "Казахский"
    ENG = "Английский"


def layout_upload_path(instance, filename):
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Формируем новое имя файла с датой и временем
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{timestamp}_{filename}"
    # Возвращаем путь внутри папки layouts
    return os.path.join('layouts', new_filename)


# Article model
class Article(models.Model):
    file = models.FileField(upload_to='articles/', null=True, blank=True)
    PDF = models.FileField(upload_to=layout_upload_path)
    language = models.CharField(choices=LanguageChoicesArticle.choices, default=LanguageChoicesArticle.RU)
    tags = models.ManyToManyField(Tag, related_name="articles")
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    annotation = RichTextField(null=True, blank=True)
    authors = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, null=True, blank=True)
    plagiarism = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"
