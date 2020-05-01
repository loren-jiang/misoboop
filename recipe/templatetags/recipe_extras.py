from django import template

register = template.Library()

"""
Template tags for recipe app
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
def render_ing_amt(ing_amt):
    unit_name = str(ing_amt.unit.name)
    # amount = ing_amt.amount
    return ing_amt.suffix()

