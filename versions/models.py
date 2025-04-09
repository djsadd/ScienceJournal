from django.db import models

# Create your models here.


class Version(models.Model):
    version = models.CharField(max_length=255)