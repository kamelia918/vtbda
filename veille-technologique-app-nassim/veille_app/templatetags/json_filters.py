import json
from django import template

register = template.Library()

@register.filter
def json_decode(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return []
