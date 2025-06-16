from django.db import models

# Models
from articles.models import Article
from users.models import CustomUser
from ckeditor.fields import RichTextField
from journal.models import Collection
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
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
    # collection = models.ForeignKey(to=Collection, on_delete=models.PROTECT, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='bids_responsible')
    comment = RichTextField(null=True, blank=True)
    exclusive_submission = models.BooleanField(null=True, blank=True, default=True, help_text="Подтвердите, что статья не публиковалась ранее и не рассматривается другим журналом")
    no_plagiarism = models.BooleanField(null=True, blank=True,
        default=True,
        help_text="Подтвердите, что в статье отсутствуют неправомерные заимствования текста (плагиат)"
    )
    authors_confirmed = models.BooleanField(null=True, blank=True,
        default=False,
        help_text="Все авторы подтвердили прочтение и согласие с рукописью"
    )

    ai_usage_details = models.TextField(null=False, blank=False,
        help_text="Если применялся ИИ, опишите, на каких этапах (поиск источников, анализ данных, визуализация и т.п.)"
    )
    manuscript = models.FileField(null=True, blank=True,
        upload_to='manuscripts/',
        help_text=(
            'Файл рукописи статьи в формате *.DOC или *.DOCX. '
            'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
            '<a href="URL_на_требования" target="_blank">требованиями для авторов</a> и не содержит никаких упоминаний об авторах, '
            'их местах работы, должностях, ученых степенях и ученых званиях, а также об источниках финансирования и иной информации, '
            'которая может использоваться для идентификации авторов.'
        )
    )
    authors_file = models.FileField(null=True, blank=True,
        upload_to='authors_files/',
        help_text=(
            'Файл со сведениями об авторах в формате *.DOC или *.DOCX. Перед загрузкой убедитесь, что файл оформлен в соответствии с '
            '<a href="URL_на_требования" target="_blank">требованиями для авторов</a> и включает:<br>'
            '– Ф. И. О. авторов, их аффилиации (название подразделения, организация, город, страна), ученые степени, звания, ORCID;<br>'
            '– информацию для корреспонденции: Ф. И. О., email, номер телефона;<br>'
            '– информацию об источниках финансирования;<br>'
            '– информацию о вкладе авторов (с указанием инициалов и видов вклада);<br>'
            '– иные авторские комментарии и примечания (конфликты интересов, благодарности и т.п.).'
        )
    )
    cover_letter = models.FileField(null=True, blank=True,
        upload_to='cover_letters/',
        help_text=(
            'Файл с заполненным и подписанным всеми авторами письмом в формате *.PDF. '
            'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
            '<a href="URL_на_требования" target="_blank">требованиями</a>.'
        )
    )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.status == BidStatus.REJECTED:
            return PermissionDenied()
        return super().save(
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,)


class ArticleVersion(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="versions")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_version")


class ReviewStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    SAVED = 'saved', 'Сохранено'
    SUBMITTED = 'submitted', 'Отправлено'


class Review(models.Model):
    plagiarism = RichTextField()
    novelty = RichTextField()
    originality = RichTextField()
    innovation = RichTextField()
    significance = RichTextField()
    structuredness = RichTextField()
    literary_level = RichTextField()
    design_quality = RichTextField()
    conclusion = RichTextField()
    reviewer = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.PROTECT,null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_submitted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT)

    def is_not_draft(self):
        return self.status == ReviewStatus.DRAFT

    def set_submit(self):
        self.save(set_submit=True)

    def save(self, *args, set_submit=False, **kwargs):
        if self.status == ReviewStatus.SAVED and set_submit == True:
            self.status = ReviewStatus.SUBMITTED
        elif self.pk:
            if self.status == ReviewStatus.SUBMITTED:
                raise ValidationError("Нельзя изменять объект со статусом 'Submitted'.")
        super().save(*args, **kwargs)
