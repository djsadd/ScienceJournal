from django.db import models

# Models
from articles.models import Article
# Create your models here.


class Bid(models.Model):
    DRAFT = "Черновик"
    SUBMITTED = "Отправлено"
    UNDER_EDITORIAL_REVIEW = "На проверке у редактора"
    UNDER_PEER_REVIEW = "Отправлено на рецензию"
    REVISION_REQUIRED = "Требуется доработка"
    RESUBMITTED_FOR_REVIEW = "Повторная рецензия"
    ACCEPTED = "Принято к публикации"
    REJECTED = "Отклонено"
    PUBLISHED = "Опубликовано"

    STATUS_CHOICE = {DRAFT: "Черновик",
                     SUBMITTED: "Отправлено",
                     UNDER_EDITORIAL_REVIEW: "На проверке у редактора",
                     UNDER_PEER_REVIEW: "Отправлено на рецензию",
                     REVISION_REQUIRED: "Требуется доработка",
                     RESUBMITTED_FOR_REVIEW: "Повторная рецензия",
                     ACCEPTED: "Принято к публикации",
                     REJECTED: "Отклонено",
                     PUBLISHED: "Опубликовано"}

    status = models.CharField(max_length=255, choices=STATUS_CHOICE, default=STATUS_CHOICE)
    title = models.TextField(null=True, blank=True)
    #messages =
    date_created = models.DateTimeField(auto_created=True)
    review = models.TextField(null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

