from django.db import models

# Models
from articles.models import Article
from users.models import CustomUser
from ckeditor.fields import RichTextField
from journal.models import Collection

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
    review = RichTextField(null=True, blank=True)
    reviewer = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
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


class ArticleVersion(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="versions")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_version")
