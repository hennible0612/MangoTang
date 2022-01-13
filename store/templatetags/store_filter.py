from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def options(count=5):
    return range(1, count)