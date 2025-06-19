from django.db import models
from django.core.validators import RegexValidator
# Models
from articles.models import Article
from journal.models import Collection
from users.models import CustomUser
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
import re
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


class BidManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status=BidStatus.PUBLISHED)


def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text).lower()


class Bid(models.Model):
    status = models.CharField(max_length=255, choices=BidStatus.choices, default=BidStatus.DRAFT)
    collection = models.ForeignKey(to=Collection, on_delete=models.PROTECT, null=True, blank=True)
    published_at = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='bids_responsible')
    comment = RichTextField(null=True, blank=True)
    exclusive_submission = models.BooleanField(null=True,
                                               blank=True,
                                               default=True,
                                               help_text="Подтвердите, что статья не публиковалась ранее и не рассматривается другим журналом"
                                               ) # To BidVersion
    no_plagiarism = models.BooleanField(null=True, blank=True,
        default=True,
        help_text="Подтвердите, что в статье отсутствуют неправомерные заимствования текста (плагиат)"
    ) # To BidVersion
    authors_confirmed = models.BooleanField(null=True, blank=True,
        default=False,
        help_text="Все авторы подтвердили прочтение и согласие с рукописью"
    ) # To BidVersion

    ai_usage_details = models.TextField(null=False, blank=False,
        help_text="Если применялся ИИ, опишите, на каких этапах (поиск источников, анализ данных, визуализация и т.п.)"
    ) # To BidVersion
    manuscript = models.FileField(null=True, blank=True,
        upload_to='manuscripts/',
        help_text=(
            'Файл рукописи статьи в формате *.DOC или *.DOCX. '
            'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
            '<a href="URL_на_требования" target="_blank">требованиями для авторов</a> и не содержит никаких упоминаний об авторах, '
            'их местах работы, должностях, ученых степенях и ученых званиях, а также об источниках финансирования и иной информации, '
            'которая может использоваться для идентификации авторов.'
        )
    ) # To BidVersion
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
    ) # To BidVersion
    cover_letter = models.FileField(null=True, blank=True,
        upload_to='cover_letters/',
        help_text=(
            'Файл с заполненным и подписанным всеми авторами письмом в формате *.PDF. '
            'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
            '<a href="URL_на_требования" target="_blank">требованиями</a>.'
        )
    )
    doi = models.CharField(
        max_length=100, null=True, blank=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$',
                message='Введите корректный DOI. Пример: 10.1000/xyz123',
                flags=re.IGNORECASE
            )
        ],
        help_text="Укажите DOI, например: 10.1000/xyz123"
    )

    objects = BidManager()

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

        if self.pk:
            old = self.__class__.objects.get(pk=self.pk)
            if old.status == BidStatus.PUBLISHED and self.status != old.status:
                raise PermissionDenied("Нельзя изменить статус после публикации")
            if old.status == BidStatus.REJECTED and self.status != old.status:
                raise PermissionDenied("Нельзя изменить отклонённую заявку")
        return super().save(
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,)

    def __str__(self):
        return f"{self.article.title}"


class BidVersion(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.PROTECT)
    comment = RichTextField(null=True, blank=True)
    exclusive_submission = models.BooleanField(null=True,
                                               blank=True,
                                               default=True,
                                               help_text="Подтвердите, что статья не публиковалась ранее и не рассматривается другим журналом"
                                               )  # To BidVersion
    no_plagiarism = models.BooleanField(null=True, blank=True,
                                        default=True,
                                        help_text="Подтвердите, что в статье отсутствуют неправомерные заимствования текста (плагиат)"
                                        )  # To BidVersion
    authors_confirmed = models.BooleanField(null=True, blank=True,
                                            default=False,
                                            help_text="Все авторы подтвердили прочтение и согласие с рукописью"
                                            )  # To BidVersion

    ai_usage_details = models.TextField(null=False, blank=False,
                                        help_text="Если применялся ИИ, опишите, на каких этапах (поиск источников, анализ данных, визуализация и т.п.)"
                                        )  # To BidVersion
    manuscript = models.FileField(null=True, blank=True,
                                  upload_to='manuscripts/',
                                  help_text=(
                                      'Файл рукописи статьи в формате *.DOC или *.DOCX. '
                                      'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
                                      '<a href="URL_на_требования" target="_blank">требованиями для авторов</a> и не содержит никаких упоминаний об авторах, '
                                      'их местах работы, должностях, ученых степенях и ученых званиях, а также об источниках финансирования и иной информации, '
                                      'которая может использоваться для идентификации авторов.'
                                  )
                                  )  # To BidVersion
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
                                    )  # To BidVersion
    cover_letter = models.FileField(null=True, blank=True,
                                    upload_to='cover_letters/',
                                    help_text=(
                                        'Файл с заполненным и подписанным всеми авторами письмом в формате *.PDF. '
                                        'Перед загрузкой убедитесь, что файл оформлен в соответствии с '
                                        '<a href="URL_на_требования" target="_blank">требованиями</a>.'
                                    )
                                    )  # To BidVersion


class ArticleVersion(models.Model):
    bid_version = models.ForeignKey(BidVersion, on_delete=models.CASCADE, related_name="versions",default=1)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_version")


class ReviewStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    SAVED = 'saved', 'Сохранено'
    SUBMITTED = 'submitted', 'Отправлено'


class ActiveReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


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
    is_active = models.BooleanField(default=True)
    reviewer = models.ForeignKey(to=CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    bid = models.ForeignKey(Bid, on_delete=models.PROTECT,null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_submitted = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=ReviewStatus.choices, default=ReviewStatus.DRAFT)

    objects = ActiveReviewManager()
    all_objects = models.Manager()

    def is_not_draft(self):
        return self.status == ReviewStatus.DRAFT

    def set_submit(self):
        self.save(set_submit=True)

    def save(self, *args, set_submit=False, **kwargs):
        if self.status == ReviewStatus.SAVED and set_submit==True:
            self.status = ReviewStatus.SUBMITTED
        elif self.pk:
            if self.status == ReviewStatus.SUBMITTED:
                raise ValidationError("Нельзя изменять объект со статусом 'Submitted'.")
        super().save(*args, **kwargs)
