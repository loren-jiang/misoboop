import django_filters
from .models import Recipe, Ingredient
from core.models import BasicTag
from django.db.models import Q, F
from core.filters import IcontainsInFilter, NullsAlwaysLastOrderingFilter

class RecipeFilterSet(django_filters.FilterSet):
    ingredients = IcontainsInFilter(query_param='ingredients', lookup_expr='ingredients__name__icontains')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=BasicTag.objects.filter(filterable=True),
        to_field_name='name',
        field_name='tags__name'
    )

    class Meta:
        model = Recipe
        fields = {
            'name': ['icontains'],
        }


def filter_recipe_qs(request, qs):
    ingredients = request.GET.getlist('ingredients', [])
    name__icontains = request.GET.get('name__icontains')
    tags = request.GET.getlist('tags', [])
    ordering = request.GET.getlist('ordering', [])

    if name__icontains != '' and name__icontains is not None:
        qs = qs.filter(Q(name__icontains=name__icontains))
    if ingredients:
        qs = qs.filter(Q(ingredients__name__in=ingredients))
    if tags:
        qs = qs.filter(Q(tags__name__in=tags))
    if ordering:
        qs = qs.order_by(*ordering)

    return qs.distinct()
