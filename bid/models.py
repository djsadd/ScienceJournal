from django.db import models

# Models
from articles.models import Article
# Create your models here.


class BidStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    SUBMITTED = 'submitted', 'Отправлено'
    EDITOR_REVIEW = 'editor_review', 'На проверке у редактора'
    SENT_FOR_REVIEW = 'sent_for_review', 'Отправлено на рецензию'
    NEEDS_REVISION = 'needs_revision', 'Требуется доработка'
    RE_REVIEW = 're_review', 'Повторная рецензия'
    ACCEPTED = 'accepted', 'Принято к публикации'
    REJECTED = 'rejected', 'Отклонено'
    PUBLISHED = 'published', 'Опубликовано'


class Bid(models.Model):
    status = models.CharField(max_length=255, choices=BidStatus.choices, default=BidStatus.DRAFT)
    title = models.TextField(null=True, blank=True)
    #messages =
    date_created = models.DateTimeField(auto_now_add=True)
    review = models.TextField(null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

