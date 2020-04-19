import django_filters
from .models import Recipe, Ingredient

class RecipeFilterSet(django_filters.FilterSet):
    ingredients = django_filters.ModelMultipleChoiceFilter(
        queryset=Ingredient.objects.all(),
        to_field_name='name',
    )

    class Meta:
        model = Recipe
        fields = {
            'name': ['icontains'],
        }