from django.urls import resolve, reverse
from django.test import TestCase
import pytest
from bs4 import BeautifulSoup
from recipe.views import home, about
from core.utils import strip_leading_trailing_spaces
from recipe.views import explore_recipes, like_recipe
from recipe.models import Recipe
import json

pytestmark = pytest.mark.django_db

class TestHomeView:
    def test_home_url_resolves_to_home_page(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert response.resolver_match.func == home, "view should be a function view called home"

    def test_home_has_correct_view_name(self, client):
        response = client.get('/')
        assert 'home' == response.resolver_match.view_name, "view_name should be 'home'"

    def test_home_has_correct_template(self, client):
        response = client.get('/')
        assert 'home.html' in (
            t.name for t in response.templates), "home view uses correct html template home.html"

    def test_home_url_accessible_by_name(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200, "home url accessible by reverse('home')"

    def test_home_has_correct_title(self, client):
        response = client.get('/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert 'MisoBoop' == strip_leading_trailing_spaces(
            title[0].text), "title is MisoBoop"

    def test_home_url_contains_correct_context(self, client):
        response = client.get(reverse('home'))
        assert 'latest_recipes' in response.context, "context has 'latest_recipes'"
        assert 'latest_posts' in response.context, "context has 'latest_posts'"
        assert 'welcome_image' in response.context, "context has 'welcome_image'"


class TestAboutView:
    def test_about_url_resolves_to_home_page(self, client):
        response = client.get('/about/')
        assert response.status_code == 200
        assert response.resolver_match.func == about, "view should be a function view called about"

    def test_about_has_correct_view_name(self, client):
        response = client.get('/about/')
        assert 'about' == response.resolver_match.view_name, "view_name should be 'about'"

    def test_about_has_correct_template(self, client):
        response = client.get('/about/')
        assert 'about.html' in (
            t.name for t in response.templates), "about view uses correct html template about.html"

    def test_about_url_accessible_by_name(self, client):
        response = client.get(reverse('about'))
        assert response.status_code == 200, "about url accessible by reverse('about')"

    def test_about_has_correct_title(self, client):
        response = client.get('/about/')
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert 'MisoBoop | About' == strip_leading_trailing_spaces(
            title[0].text), "title is MisoBoop | About"


class TestRecipesView:
    def test_recipe_has_view_on_add(self, client, recipe_factory):
        recipe = recipe_factory(name="Pigs in a blanket")
        response = client.get(recipe.get_absolute_url())
        assert response.status_code == 200

    def test_recipe_slug(self, client, recipe_factory, tag_factory):
        recipe = recipe_factory(name="Fried rice")
        response = client.get(f'/recipes/recipe/{recipe.slug}/')
        assert response.status_code == 200

    def test_recipe_tag_view(self, client, recipe_factory, tag_factory):
        recipe = recipe_factory(name="Pigs in a blanket")
        tag1 = tag_factory(name="comfort food")

        recipe.tags.add(tag1)

        response = client.get(f'/recipes/tag/{tag1.slug}/')
        assert response.status_code == 200

        assert response.context['title'] == f'{tag1.name.capitalize()} recipes'
        assert recipe in response.context['recipes']

        tag2 = tag_factory(name="pork")
        more_pork_recipes = []

        # add some pork recipes
        for _ in range(5):
            r = recipe_factory()
            r.tags.add(tag2)
            more_pork_recipes.append(r)

        response = client.get(f'/recipes/tag/{tag2.slug}/')
        assert response.context['title'] == f'{tag2.name.capitalize()} recipes'
        for recipe in more_pork_recipes:
            assert recipe in response.context['recipes']

    def test_bad_recipe_tag(self, client):
        response = client.get('/recipes/tag/bad-tag/')
        assert response.status_code == 200
        assert response.context['title'] == 'No such tag found...'

    def test_recipe_explore_title(self, client):
        response = client.get('/recipes/explore/')
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find_all('title')
        assert len(title) == 1, "only one title"
        assert strip_leading_trailing_spaces(
            title[0].text) == 'MisoBoop | Explore recipes', "title is correct"

    def test_recipe_explore_context(self, client, recipe_factory, tag_factory):
        # create lots of tags
        tags = []
        for _ in range(50):
            tag = tag_factory()
            tags.append(tag)

        # create lots of recipes
        recipes = []
        for _ in range(50):
            recipe = recipe_factory()
            recipes.append(recipe)
        for i in range(50):
            recipes[i].tags.set(*tags[i:50])

        response = client.get(
            '/recipes/explore/', {'num_tags_to_show': 5, 'num_recipes_to_show': 50})
        context_keys = ['tags', 'tagged_recipes', 'tag_slugs']
        for key in context_keys:
            assert key in response.context
        assert len(response.context['tagged_recipes'].keys()) == 5
        for k in range(5):
            assert len(response.context['tagged_recipes']
                       [tags[49 - k].name]) == 50 - k

    def test_recipe_explore_num_recipes_shown(self, client, recipe_factory, tag_factory):
        recipes = []
        for _ in range(11):
            recipe = recipe_factory()
            recipes.append(recipe)
        tag = tag_factory(name='ex_tag')

        for i in range(11):
            recipes[i].tags.set(tag)
        response = client.get(
            '/recipes/explore/', {'num_tags_to_show': 10, 'num_recipes_to_show': 5})
        assert response.status_code == 200
        assert len(response.context['tagged_recipes'].keys()) == 1
        assert len(response.context['tagged_recipes']['ex_tag']) == 5

    def test_recipe_series_detail_view(self, client, recipe_factory, post_factory, series_factory):
        series = series_factory(name="ex_series")
        recipes = []
        for _ in range(6):
            recipe = recipe_factory()
            recipes.append(recipe)

        posts = []
        for _ in range(5):
            post = post_factory()
            posts.append(post)

        series.recipes.add(*recipes)
        series.posts.add(*posts)

        response = client.get(series.get_absolute_url())
        assert response.status_code == 200
        assert 'recipes_and_posts' in response.context

        assert len(response.context['recipes_and_posts']) == len(recipes) + len(posts)
    
    def test_recipes_series_list_view(self, client, ten_seriess, ten_posts):
        seriess = ten_seriess
        posts = ten_posts

        response = client.get('/recipes/series/')
        assert response.status_code == 200
        
        assert 'series_list' in response.context
        assert len(response.context['series_list']) == 0
        

        for i in range(len(seriess)):
            seriess[i].posts.add(posts[i])
        response = client.get('/recipes/series/')
        assert response.context['series_list'].count() == len(seriess)

    def test_like_recipe(self, rf, recipe_factory):
        recipe = recipe_factory()
        request = rf.get(reverse('like-recipe', kwargs={'slug':recipe.slug}))
        assert recipe.likes == 1
        response = like_recipe(request, slug=recipe.slug)
        assert response.status_code == 200
        json_dict = json.loads(response.content)
        assert json_dict['numLikes'] == 2
      
        for i in range(50):
            like_recipe(request, slug=recipe.slug)
        assert Recipe.objects.get(id=recipe.id).likes == 52

    def test_recipe_search(self, client):
        response = client.get(reverse('search-recipes'))
        assert response.status_code == 200

        # TODO: complete this test

    def test_recipe_print(self, client, recipe_factory):
        recipe = recipe_factory()
        response = client.get(reverse('recipe-print', kwargs={'slug': recipe.slug}))
        assert response.status_code == 200

        # TODO: complete this test
        
