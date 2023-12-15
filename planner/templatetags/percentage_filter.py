from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    return int((value / total) * 100)