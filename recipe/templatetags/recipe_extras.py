from django import template

register = template.Library()

"""
Template tags for recipe app
"""

@register.filter
def render_ing_amt(ing_amt):
    unit_name = str(ing_amt.unit.name)
    return ing_amt.suffix()

