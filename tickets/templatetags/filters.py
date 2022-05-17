from django import template
register = template.Library()

@register.filter(name='times') 
def times(number):
    return range(int(number))


@register.filter(name='to_int')
def to_int(value):
    return int(value)


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# @register.filter
# def update_variable(value):
#     data = value
#     return data

@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


@register.filter
def index(indexable, i):
    return indexable[i]
