# bid/templatetags/bid_filters.py
from django import template
from django.utils.html import strip_tags
import html

register = template.Library()

@register.filter
def clean_preview(value, length=50):
    try:
        text = strip_tags(value)
        text = html.unescape(text)  # ← удаляет &nbsp;, &laquo;, &raquo; и т.п.
        text = text.strip()
        return text[:length] + '…' if len(text) > length else text
    except:
        return ''
