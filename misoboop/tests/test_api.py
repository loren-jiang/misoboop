import pytest
import json
from recipe.models import Ingredient, Recipe, BasicTag

pytestmark = pytest.mark.django_db


def test_api_root(client):
    response = client.get('/api/')
    assert response.status_code == 200
    sub_urls_map = json.loads(response.content)
    assert sorted([key for key in sub_urls_map]) == sorted(
        ["recipes", "ingredients", "tags"]), "api router has correct urls"

def test_api_recipes(client):
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
    assert recipe_count == recipes_qs.count(), "all recipes shown on api"
    assert sorted([recipe['id'] for recipe in results]) == sorted([recipe.id for recipe in recipes_qs])

def test_api_ingredients(client):
    response = client.get('/api/ingredients/')
    assert response.status_code == 200
    ingredients = json.loads(response.content)
    ingredients_qs = Ingredient.objects.all()
    assert len(ingredients) == ingredients_qs.count(), "all ingredients shown on api"
    assert sorted([i['id'] for i in ingredients]) == sorted([i.id for i in ingredients_qs])

def test_api_tags(client):
    response = client.get('/api/tags/')
    assert response.status_code == 200
    tags = json.loads(response.content)
    tags_qs = BasicTag.objects.all()
    assert len(tags) == tags_qs.count(), "all ingredients shown on api"
    assert sorted([i['id'] for i in tags]) == sorted([i.id for i in tags_qs])

    