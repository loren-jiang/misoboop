import django_filters
from .models import Recipe, Ingredient
from core.models import BasicTag
from django.db.models import Q, F
from django_filters.fields import Lookup
from functools import reduce
import operator
from rest_framework.filters import OrderingFilter


class NullsAlwaysLastOrderingFilter(OrderingFilter):
    """ Use Django nulls_last feature to force nulls to bottom in all orderings. """

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            f_ordering = []
            for o in ordering:
                if not o:
                    continue
                if o[0] == '-':
                    f_ordering.append(F(o[1:]).desc(nulls_last=True))
                else:
                    f_ordering.append(F(o).asc(nulls_last=True))

            return queryset.order_by(*f_ordering)

        return queryset


class IcontainsInFilter(django_filters.Filter):
    def __init__(self, *args, **kwargs):
        self.query_param = kwargs.pop('query_param', None)
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        params = list(filter(
            lambda x: x,  # filters empty strings
            self.parent.request.GET.getlist(self.query_param, [])))
        if params:
            clauses = (Q(**{self.lookup_expr: ing}) for ing in params)
            query = reduce(operator.or_, clauses)
            qs = qs.filter(query).distinct()
        return qs


class RecipeFilterSet(django_filters.FilterSet):
    ingredients = IcontainsInFilter(query_param='ingredients', lookup_expr='ingredients__name__icontains')
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=BasicTag.objects.filter(filterable=True),
        to_field_name='name',
        field_name='tags__name'
    )
    #
    # ingredients = django_filters.Filter(method='filter_ingredients')
    #
    # def filter_ingredients(self, queryset, name, value):
    #     """
    #     Filter using icontains and in; for m2m fields that you don't necessarily need in db (vs. MultipleModelChoiceField)
    #     """
    #     ingredient_names = self.request.GET.getlist(name, [])
    #     qs = queryset
    #     if ingredient_names:
    #         clauses = (Q(ingredients__name__icontains=ing) for ing in ingredient_names)
    #         query = reduce(operator.or_, clauses)
    #         qs = qs.filter(query).distinct()
    #     return qs

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
