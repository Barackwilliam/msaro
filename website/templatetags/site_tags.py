import json

from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

register = template.Library()

_JSON_ESCAPES = {ord(">"): "\\u003E", ord("<"): "\\u003C", ord("&"): "\\u0026"}


@register.simple_tag(takes_context=True)
def t(context, key):
    """Text from Admin → Page texts. Usage: {% t 'about.s1.h1' %}"""
    block = context.get("blocks", {}).get(key)
    if block is None:
        return ""
    return mark_safe(block.text) if block.is_html else conditional_escape(block.text)


@register.simple_tag(takes_context=True)
def img(context, key):
    """URL of a picture from Admin → Page pictures. Usage: {% img 'home.about_photo' %}"""
    block = context.get("image_blocks", {}).get(key)
    return block.src if block else ""


@register.simple_tag(takes_context=True)
def img_alt(context, key):
    block = context.get("image_blocks", {}).get(key)
    return block.alt if block else ""


@register.filter
def json_script_safe(value):
    """JSON that is safe to place inside a <script> tag."""
    return mark_safe(json.dumps(value, ensure_ascii=False).translate(_JSON_ESCAPES))


@register.filter
def aos_delay(value):
    """Renders the data-aos-delay attribute only when a delay is set."""
    if value is None or value == "":
        return ""
    return mark_safe(f' data-aos-delay="{escape(value)}"')


@register.filter
def ask_url(package, site):
    return package.ask_url(site)


@register.filter
def booking_number(package, site):
    return package.booking_number(site)
