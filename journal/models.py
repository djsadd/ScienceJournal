from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Collection(models.Model):
    title = models.CharField(null=True, blank=True)
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)


