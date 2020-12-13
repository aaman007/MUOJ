from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(obj: dict, key):
    return obj.get(key, '')
