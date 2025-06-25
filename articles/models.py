from django.db import models
from ckeditor.fields import RichTextField

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


# Article model
class Article(models.Model):
    file = models.FileField(upload_to='articles/')
    # PDF
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
