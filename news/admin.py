from django.contrib import admin

# Register your models here.
from .models import News, Category

admin.site.register(News)
admin.site.register(Category)