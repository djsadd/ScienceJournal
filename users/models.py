from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _


LANG_CHOICES = (
    ('ru', _('Русский')),
    ('en', _('Английский')),
    ('kz', _('Казахский')),
)


class CustomUser(AbstractUser):
    AUTHOR = "АВТОР"
    REDACTOR = "РЕДАКТОР"
    REVIEWER = "РЕЦЕНЗИСТ"

    choices = (
        (AUTHOR, _('Автор')),
        (REDACTOR, _('Редактор')),
        (REVIEWER, _('Рецензент')),
    )

    middle_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Отчество'),
        help_text=_('При наличии — отчество или второе имя')
    )
    department = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Кафедра/подразделение'),
        help_text=_('Краткое наименование кафедры или подразделения')
    )
    institution = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Учреждение'),
        help_text=_('Название университета или организации')
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Город, страна'),
        help_text=_('Город и страна проживания / работы')
    )
    academic_degree = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Академическая степень'),
        help_text=_('Например, д.ю.н., профессор')
    )
    orcid = models.CharField(
        max_length=19,
        blank=True,
        verbose_name=_('ORCID'),
        help_text=_('Идентификатор ORCID, например 0000-0001-2345-6789')
    )
    is_editorial_board = models.BooleanField(
        default=False,
        verbose_name=_('Редакционная коллегия'),
        help_text=_('Отметьте, чтобы пользователь отображался как член редакционной коллегии')
    )
    is_editorial_council = models.BooleanField(
        default=False,
        verbose_name=_('Редакционный совет'),
        help_text=_('Отметьте, чтобы пользователь отображался как член редакционного совета')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=choices, default=AUTHOR)
    languages = MultiSelectField(choices=LANG_CHOICES, default='ru')
    email_confirmed = models.BooleanField(default=False)

    @property
    def display_name(self):
        parts = [self.last_name or '', self.first_name or '', self.middle_name or '']
        return ' '.join(part for part in parts if part).strip()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.role}"
