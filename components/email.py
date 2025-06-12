from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_html_email(subject, to_email, template_name, context, from_email=None):
    """
    Универсальная отправка HTML-письма на основе шаблона.

    :param subject: Тема письма
    :param to_email: Получатель (или список)
    :param template_name: Путь к шаблону
    :param context: Контекст для шаблона
    :param from_email: Отправитель (по умолчанию settings.DEFAULT_FROM_EMAIL)
    """
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string(template_name, context)
    text_content = render_to_string('email/request-add.txt', context) if template_name.endswith('.html') else ''

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email] if isinstance(to_email, str) else to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
