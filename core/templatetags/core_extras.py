from django import template

register = template.Library()

"""
Template tags for core app
"""

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def min_to_hr(value):
    value = int(value)
    hrs = str(value // 60) + 'hr' if value // 60 else ''
    mins = str(value % 60) + 'min' if value % 60 else ''
    return f'{hrs} {mins}'

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_obj_item(obj, key):
    return obj.__dict__.get(key)

@register.simple_tag
def create_list(*args):
    return args

@register.filter
def split(value, arg):
    return value.split(arg)