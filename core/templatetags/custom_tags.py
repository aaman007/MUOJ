from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(obj: dict, key):
    return obj.get(key, '')


@register.filter(name='num_to_alpha')
def num_to_alpha(val: int):
    extras = int(val / 26)
    alpha = ''
    while extras:
        alpha += 'A'
        extras -= 1
    alpha += chr(65 + (val % 26))
    return alpha
