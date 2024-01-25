from django import template

register = template.Library()

@register.filter
def split_string(value, delimiter):
    return value.split(delimiter)

@register.filter
def remove_quotes(value):
    return value.replace("'", "")