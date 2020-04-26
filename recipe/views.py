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
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers

import json


# Create your views here.

# Home page view which shows latest recipes 'latest_recipes' and latest blog posts 'latest_posts'
def home(request):
    context = {
        'latest_recipes': Recipe.objects.prefetch_related('tags', ).order_by('-created_at').select_related()[0:6],
        'latest_posts': Post.objects.prefetch_related('tags').order_by('-created_at').select_related()[0:6]
    }
    return render(request, 'home.html', context)

# About page view which details "Who, What, Where, and Why?"
def about(request):
    context = {}
    about = None
    try:
        about = Post.objects.get(name='About')
    except Post.DoesNotExist:
        pass
    if about is not None:
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug':'about'}))
    return render(request, 'about.html', context)

def like_recipe(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    Recipe.objects.filter(slug=slug).update(likes=F('likes') + 1)  # increment likes by 1
    num_likes = Recipe.objects.get(slug=slug).likes
    return JsonResponse({
        'numLikes': num_likes,
    })


class RecipeDetailView(JsonLdDetailView):
    queryset = Recipe.objects.prefetch_related(
        'author',
        'directions__ingredient_amounts__ingredient',
        'directions__ingredient_amounts__unit',
        'ingredient_amounts__unit',
        'ingredient_amounts__ingredient').annotate(
            total_time=F('cook_time') + F('prep_time'))
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        print(serializers.serialize('json', self.object.ingredient_amounts.all()))
        # context['ingredient_amounts_json'] = serializers.serialize('json', )
        return context


class RecipeListView(ListView):
    model = Recipe
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        context['filter_tags'] = BasicTag.objects.filter(filterable=True)

        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related(
            'ratings', 'tags',
            'directions__ingredient_amounts__ingredient',
            'directions__ingredient_amounts__unit').annotate(
            total_time=F('cook_time') + F('prep_time'))
        return filter_recipe_qs(self.request, qs)


class ExploreRecipesListView(ListView):
    model = Recipe
    template_name = 'recipe/explore_recipes.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        tags = Recipe.tags.most_common().filter(filterable=True).order_by('-num_times')[0:10]
        recipes = Recipe.objects.filter(tags__in=tags)
        context['filter_tags'] = tags
        for tag in tags:
            context[tag.name] = recipes.filter(tags__in=[tag])
        return context

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('ratings', 'tags').annotate(
            total_time=F('cook_time') + F('prep_time'))
        return qs


def explore_recipes(request):
    context = {}
    tags = Recipe.tags.most_common().filter(filterable=True).order_by('-num_times')[0:10]
    recipes = Recipe.objects.filter(tags__in=tags).prefetch_related('ratings', 'tags').annotate(
            total_time=F('cook_time') + F('prep_time')).annotate(avg_ratings=F('ratings__average'))
    context['tags'] = tags
    tagged_recipes_dict = {}
    for tag in tags:
        tagged_recipes_dict[tag.name] = recipes.filter(tags__in=[tag]).distinct().order_by('-avg_ratings')

    context['tagged_recipes'] = tagged_recipes_dict

    return render(request, 'recipe/explore_recipes.html', context)


def search_recipes(request):
    context = {
        'filter_tags': BasicTag.objects.filter(filterable=True)
    }
    return render(request, 'recipe/recipe_list_ajax.html', context)
