from django.contrib import admin
from .models import Bid, ArticleVersion, Review
# Register your models here.


admin.site.register(Bid)
admin.site.register(ArticleVersion)
admin.site.register(Review)