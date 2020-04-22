from django.shortcuts import render
from core.models import BasicTag
from blog.models import Post
from recipe.models import Recipe
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django_json_ld.views import JsonLdDetailView
from django.db.models import F, Q
from django.http import JsonResponse
from .filters import filter_recipe_qs
import json

# Create your views here.

def home(request):
    data = {
        'latest_recipes': Recipe.objects.prefetch_related('tags',).order_by('-created_at').select_related()[0:6],
        'latest_posts': Post.objects.prefetch_related('tags').order_by('-created_at').select_related()[0:6]
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
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['filter_tags'] = BasicTag.objects.filter(filterable=True)

        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('ratings', 'tags').annotate(total_time=F('cook_time')+F('prep_time'))
        return filter_recipe_qs(self.request, qs)


def ajax_recipes(request):
    context = {
        'filter_tags': BasicTag.objects.filter(filterable=True)
    }
    return render(request, 'recipe/recipe_list_ajax.html', context)


