from django.shortcuts import render
from recipe.models import Recipe
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone
from django_json_ld.views import JsonLdDetailView
from django.db.models import F, Q
from django.http import JsonResponse
import json

# Create your views here.

def home(request):
    data = {
        'latest_3_recipes': Recipe.objects.order_by('-modified_at').select_related()[0:3],
    }
    return render(request, 'recipe/home.html', data)

def like_recipe(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    Recipe.objects.filter(slug=slug).update(likes=F('likes') + 1) # increment likes by 1
    num_likes = Recipe.objects.get(slug=slug).likes
    return JsonResponse({
        'numLikes': num_likes,
    })

class RecipeDetailView(JsonLdDetailView):
    queryset = Recipe.objects.prefetch_related('directions',
                                               'ingredient_amounts',
                                               'ingredient_amounts__unit',
                                               'ingredient_amounts__ingredient', )
    model = Recipe
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class RecipeListView(ListView):
    model = Recipe

    def get_queryset(self):
        kwargs = self.kwargs
        ingredients = self.request.GET.getlist('ingredient', [])
        name_icontains = self.request.GET.get('name_icontains')
        tags = self.request.GET.getlist('tag', [])
        qs = super().get_queryset()

        if name_icontains != '' and name_icontains is not None:
            qs = qs.filter(Q(name__icontains=name_icontains))
        if ingredients:
            qs = qs.filter(Q(ingredients__name__in=ingredients))
        if tags:
            qs = qs.filter(Q(tags__name__in=tags))
        return qs


