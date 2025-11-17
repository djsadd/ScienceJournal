from celery import shared_task
from django.core.mail import send_mail

from .email import send_html_email


@shared_task
def send_mail_task(subject, message, from_email, recipient_list, html_message=None, fail_silently=False):
    """
    Proxy task for Django's :func:`send_mail` to run inside Celery worker.
    """
    return send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=fail_silently,
    )


@shared_task
def send_html_email_task(subject, to_email, template_name, context, from_email=None):
    """
    Wrapper task around the helper that prepares and sends HTML email.
    """
    send_html_email(subject, to_email, template_name, context, from_email=from_email)
