from django import template

register = template.Library()

@register.filter
def youtube_embed(value):
    if not value:
        return ''
    return value.replace('watch?v=', 'embed/')

@register.filter
def times(number):
    return range(int(number))
