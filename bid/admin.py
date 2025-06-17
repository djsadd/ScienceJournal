from django.contrib import admin
from .models import Bid, ArticleVersion, Review, BidVersion
# Register your models here.


admin.site.register(Bid)
admin.site.register(ArticleVersion)
admin.site.register(Review)
admin.site.register(BidVersion)