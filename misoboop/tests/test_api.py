import pytest
import math
import json
from recipe.models import Ingredient, Recipe, BasicTag
from recipe.views_api import RecipeViewSet, CustomPageNumberPagination, CustomLimitOffsetPagination

pytestmark = pytest.mark.django_db


def test_api_root(client):
    response = client.get('/api/')
    assert response.status_code == 200
    sub_urls_map = json.loads(response.content)
    assert sorted([key for key in sub_urls_map]) == sorted(
        ["recipes", "ingredients", "tags"]), "api router has correct urls"

def test_api_recipes(client, ten_recipes):
    response = client.get('/api/recipes/')
    assert response.status_code == 200
    recipes_content = json.loads(response.content)
    num_pages = recipes_content['num_pages']
    recipe_count = 0
    results = []
    for k in range(num_pages):
        page_response_content =  json.loads(client.get(f'/api/recipes/?page={k+1}').content)
        recipe_count += page_response_content['count']
        results += page_response_content['results']
    recipes_qs = Recipe.objects.all()
    assert recipe_count == recipes_qs.count() == 10, "all recipes shown on api"
    assert sorted([recipe['id'] for recipe in results]) == sorted([recipe.id for recipe in recipes_qs])

def test_api_recipes_search(client, recipe_factory):
    recipes = [recipe_factory() for _ in range(100)]
    response_search_pork = client.get('/api/recipes/?search=pork')
    response_search_pork_json = json.loads(response_search_pork.content)
    assert response_search_pork.status_code == 200
    assert response_search_pork_json['results'] == []

    pork_recipe = recipe_factory(name="pork roast")
    response_search_pork = client.get('/api/recipes/?search=pork')
    response_search_pork_json = json.loads(response_search_pork.content)
    assert response_search_pork.status_code == 200
    assert response_search_pork_json['results'][0]['id'] == pork_recipe.id

def test_api_recipes_pagination(client, recipe_factory):
    N = 25
    recipes = [recipe_factory() for _ in range(N)]
    response = client.get('/api/recipes/')
    response_json = json.loads(response.content)
    assert CustomPageNumberPagination == RecipeViewSet.pagination_class
    page_size = CustomPageNumberPagination.page_size
    if N > page_size:
        assert response_json['num_pages'] == math.ceil(N / page_size)

def test_api_ingredients(client, ten_ingredients):
    response = client.get('/api/ingredients/')
    assert response.status_code == 200
    ingredients = json.loads(response.content)
    ingredients_qs = Ingredient.objects.all()
    assert len(ingredients) == ingredients_qs.count() == 10, "all ingredients shown on api"
    assert sorted([i['id'] for i in ingredients]) == sorted([i.id for i in ingredients_qs])

def test_api_tags(client):
    response = client.get('/api/tags/')
    assert response.status_code == 200
    tags = json.loads(response.content)
    tags_qs = BasicTag.objects.all()
    assert len(tags) == tags_qs.count(), "all ingredients shown on api"
    assert sorted([i['id'] for i in tags]) == sorted([i.id for i in tags_qs])

def test_api_recipes_list(client, ten_recipes):
    response = client.get('/api/recipes_list/')
    assert response.status_code == 200
    # response_json = json.loads(response.content)

def test_api_ingredients_list(client, ten_ingredients):
    response = client.get('/api/ingredients_list/')
    assert response.status_code == 200
