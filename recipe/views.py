from django.shortcuts import render
from core.models import BasicTag
from blog.models import Post
from recipe.models import Recipe, Unit
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django_json_ld.views import JsonLdDetailView
from django.db.models import F, Q, Sum, Count, Case, When
from django.http import JsonResponse
from .filters import filter_recipe_qs, RecipeFilterSet
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from core.models import Series, PublicImage
from django_filters.views import FilterView
from .serializers import IngredientAmountSerializer
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json


# Create your views here.

# Home page view which shows latest recipes 'latest_recipes' and latest blog posts 'latest_posts'
def home(request):
    context = {
        'latest_recipes': Recipe.objects.filter(is_published=True).prefetch_related('tags').order_by(
            '-created_at').select_related()[0:6],
        'latest_posts': Post.objects.prefetch_related('tags').order_by('-created_at').select_related()[0:6],
    }
    welcome_image = None
    try:
        welcome_image = PublicImage.objects.get(name='miso-rilakkuma')
    except PublicImage.DoesNotExist:
        pass
    context['welcome_image'] = welcome_image
    return render(request, 'home.html', context)


# About page view which details "Who, What, Where, and Why?"
def about(request):
    context = {}
    # about = None
    # try:
    #     about = Post.objects.get(headline='About')
    # except Post.DoesNotExist:
    #     pass
    # if about is not None:
    #     return HttpResponseRedirect(reverse('post-detail', kwargs={'slug':'about'}))
    human_image = None
    try:
        human_image = PublicImage.objects.get(name='loren')
    except PublicImage.DoesNotExist:
        pass
    context['human_image'] = human_image

    miso_image = None
    try:
        miso_image = PublicImage.objects.get(name='miso-rilakkuma')
    except PublicImage.DoesNotExist:
        pass
    context['miso_image'] = miso_image

    return render(request, 'about.html', context)


def like_recipe(request, *args, **kwargs):
    slug = kwargs.get('slug', None)
    Recipe.objects.filter(slug=slug).update(likes=F('likes') + 1)  # increment likes by 1
    num_likes = Recipe.objects.get(slug=slug).likes
    return JsonResponse({
        'numLikes': num_likes,
    })


class RecipeDetailView(JsonLdDetailView):
    queryset = Recipe.objects.select_related(
        'author',
        'image'
    ).prefetch_related(
        'directions__ingredient_amounts__ingredient',
        'directions__ingredient_amounts__unit',
        'ingredient_amounts__unit',
        'ingredient_amounts__ingredient').annotate(
        total_time=F('cook_time') + F('prep_time')).filter(
    )
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['ingredient_amounts'] =  serializers.serialize('json', (self.object.ingredient_amounts.values_list('unit__name', 'id')))
        #
        # a = {}
        # for ing_amt in self.object.ingredient_amounts.all():
        #     serializer = IngredientAmountSerializer(ing_amt)
        #     a[ing_amt.id] = serializer.data
        #
        # context['ingredient_amounts'] = a
        # context['ingredient_amounts'] = json.dumps(list(self.object.ingredient_amounts.values_list('unit__type  ', 'id')), cls=DjangoJSONEncoder)

        imperial_choice = Unit.SYSTEM.imperial

        context['imperial_ingredients'] = json.dumps([ing_amt.ingredient.name
                                                      for ing_amt in self.object.ingredient_amounts.filter(
                unit__system=imperial_choice).select_related('ingredient')])

        context['now'] = timezone.now()
        return context


class RecipeListView(FilterView):
    model = Recipe
    filterset_class = RecipeFilterSet
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related(
            'ratings', 'tags',
            'directions__ingredient_amounts__ingredient',
            'directions__ingredient_amounts__unit').annotate(
            total_time=F('cook_time') + F('prep_time')).filter(
            is_published=True
        )
        return qs


class RecipeSeriesDetailView(DetailView):
    model = Series
    template_name = 'recipe/series_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        posts = []
        for post in self.object.posts.all():
            post_img_url = post.placeholder_url
            if post.image:
                post_img_url = post.image.upload.url

            post_data = {
                'name': post.headline,
                'image_url': post_img_url,
                'description': post.short_description,
                'date': post.created_at,
                'is_post': True,
            }

            posts.append(post_data)

        recipes = []
        for recipe in self.object.recipes.all():
            recipe_img_url = recipe.placeholder_url
            if recipe.image:
                recipe_img_url = recipe.image.upload.url

            recipe_data = {
                'name': recipe.name,
                'image_url': recipe_img_url,
                'description': recipe.short_description,
                'date': recipe.created_at
            }
            recipes.append(recipe_data)

        sorted_recipes_and_posts = sorted(posts + recipes, key=lambda item: item['date'])
        context['recipes_and_posts'] = sorted_recipes_and_posts
        return context


class RecipeSeriesListView(ListView):
    model = Series
    template_name = 'recipe/series_list.html'

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('recipes', 'posts') \
            .annotate(num_recipes_and_posts=Count(Case(When(recipes__is_published=True, then=1))) +
                                            Count(Case(When(posts__is_published=True, then=1)))) \
            .filter(num_recipes_and_posts__gt=0).order_by()
        return qs


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
            total_time=F('cook_time') + F('prep_time')).annotate(avg_ratings=F('ratings__average'))
        return qs


def explore_recipes(request):
    context = {}
    tags = Recipe.tags.most_common().filter(filterable=True).order_by('-num_times')[0:10]
    recipes = Recipe.objects.filter(tags__in=tags).prefetch_related('ratings', 'tags').annotate(
        total_time=F('cook_time') + F('prep_time')).annotate(avg_ratings=F('ratings__average'))
    context['tags'] = tags
    tagged_recipes_dict = {}
    tag_slugs_dict = {}
    for tag in tags:
        tagged_recipes_dict[tag.name] = recipes.filter(tags__in=[tag]).distinct().order_by('-avg_ratings')
        tag_slugs_dict[tag.name] = tag.slug
    context['tagged_recipes'] = tagged_recipes_dict
    context['tag_slugs'] = tag_slugs_dict
    return render(request, 'recipe/explore_recipes.html', context)


def search_recipes(request):
    context = {
        'filter_tags': BasicTag.objects.filter(filterable=True, recipe__isnull=False).distinct()
    }
    return render(request, 'recipe/recipe_list_ajax.html', context)


def tagged_by_recipes(request, *args, **kwargs):
    context = {}
    tag_slug = kwargs.get('slug', None)
    context['recipes'] = Recipe.objects.filter(tags__slug__in=[tag_slug]).distinct()
    context['title'] = f'{tag_slug.capitalize()} recipes'
    return render(request, 'recipe/tagged_by_recipes.html', context)
