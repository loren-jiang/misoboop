from django.test import TestCase, override_settings
from .factories import RecipeFactory
import tempfile
import shutil
from core.models import PublicImage
import json
import jsonschema
from recipe.models import Recipe
import pytest
from django.conf import settings
from bs4 import BeautifulSoup

pytestmark = pytest.mark.django_db

# TODO: there might be a better way to validate json-ld via online api, but for now use this
recipe_schema = {
    "type": "object",
    "properties": {
        # "@context": {"type": "string"},
        # "@type": {"type": "string"},
        "author":  {"type": "string"},
        "cookTime":  {"type": "string"},
        "datePublished":  {"type": "string"},
        "description":  {"type": "string"},
        "image": {"type": "string"},
        "recipeIngredient": {"type": "array"},
        "interactionStatistic": {"type": "object"},
        "name": {"type": "string"},
        "nutrition": {"type": "object"},
        "prepTime": {"type": "string"},
        "recipeInstructions": {"type": "array"},
        "recipeYield": {"type": ["integer", "string"]},
        "suitableForDiet": {"type": "string"},
        "recipeCuisine": {"type": "string"},
    }

}


def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True


# @override_settings(
#     MEDIA_ROOT=MEDIA_ROOT,
#     THUMBNAIL_STORAGE="inmemorystorage.InMemoryStorage",
#     DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
# class RecipeModelTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         pass

#     def setUp(self):
#         # make sure we're using in-memory test env.
#         from django.conf import settings
#         self.assertTrue(settings.THUMBNAIL_STORAGE ==
#                         'inmemorystorage.InMemoryStorage')
#         self.assertTrue(settings.DEFAULT_FILE_STORAGE ==
#                         'inmemorystorage.InMemoryStorage')
#         # todo: clearly something wrong with sorl.thumbnail not using correct storage...
#         # new_image = PublicImage(
#         #     name='temp_image',
#         #   upload=tempfile.NamedTemporaryFile(suffix='.jpg'))
#         # new_image.save()
#         # self.test_recipe = RecipeFactory(
#         #     name='Chinese smashed cucumbers',
#         #     image=new_image
#         # )

#         self.test_recipe = RecipeFactory(name="Char siu pork")
#         self.test_recipe.tags.add("Pork", "Chinese", "Comfort food")

#     def tearDown(self):
#         # shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
#         pass


#     def test_image_url(self):
#         pass

#     def test_ing_amts_as_list(self):
#         pass


@pytest.fixture
def basic_recipe(recipe_factory):
    recipe = recipe_factory(
        name="Char siu pork",
        cook_time=30,
        prep_time=45,
    )
    recipe.tags.add("Pork", "Chinese", "Comfort food")
    return recipe


class TestRecipeModel:
    def test_recipe_image(self, recipe_factory, public_image_factory):
        recipe = recipe_factory()
        image = public_image_factory()
        recipe.image = image
        recipe.save()
        assert bool(recipe.image.upload)
        assert bool(recipe.image.thumbnail)

    def test_recipe_directions(self, recipe_factory):
        recipe = recipe_factory(post__randomize=True)
        pass

    def test_str(self, basic_recipe):
        assert str(basic_recipe) == "Char siu pork"

    def test_total_time(self, basic_recipe):
        assert basic_recipe.total_time() == 75

    def test_slug_is_created_automatically(self, basic_recipe, recipe_factory):
        assert basic_recipe.slug == "char-siu-pork"
        yogurt = recipe_factory(name="Yogurt")
        assert yogurt.slug == "yogurt"

    def test_get_absolute_url(self, basic_recipe):
        assert basic_recipe.get_absolute_url() == "/recipes/recipe/char-siu-pork/"

    def test_tag_names_as_list(self, basic_recipe):
        assert basic_recipe.tag_names_as_list(
        ) == ["Chinese", "Comfort food", "Pork"]

    def test_adding_tags(self, basic_recipe):
        basic_recipe.tags.add("Takeout", "Cantonese")
        assert basic_recipe.tag_names_as_list(
        ) == ["Cantonese", "Chinese", "Comfort food", "Pork", "Takeout"]

    def test_no_duplicate_tags(self, basic_recipe):
        old_count = basic_recipe.tags.count()
        basic_recipe.tags.add("Pork", "Chinese", "Chinese")
        assert basic_recipe.tags.count() == old_count

    def test_validate_sd_schema(self, basic_recipe):
        json_ld = basic_recipe.sd
        assert validate_json(json_ld, recipe_schema) == True

    def test_lazify_desc(self, complete_recipe):
        if settings.LAZIFY_IMAGES:
            assert bool(complete_recipe.lazy_description)

            soup = BeautifulSoup(complete_recipe.lazy_description, "html.parser")
            images = soup.findAll('img')
            for img in images:
                assert img.has_attr('data-src')
                assert img.has_attr('class')
                assert settings.LAZIFY_IMAGE_CLASS in img['class']
    
    def test_lazify_direction(self, complete_recipe):
        if settings.LAZIFY_IMAGES:

            for direction in complete_recipe.directions.all():
                assert bool(direction.lazy_text)
                soup = BeautifulSoup(direction.lazy_text, "html.parser")
                images = soup.findAll('img')
                for img in images:
                    assert img.has_attr('data-src')
                    assert img.has_attr('class')
                    assert settings.LAZIFY_IMAGE_CLASS in img['class']
        
    def test_thumbnail(self, complete_recipe):
        assert bool(complete_recipe.image)
        assert bool(complete_recipe.image.thumbnail)



class TestIngredientAmountModel:
    def test_str(self, ingredient_amount_factory, unit_factory, ingredient_factory):
        ing = ingredient_factory(name="salt", plural_name="salt")
        unit = unit_factory(name="gram", name_abbrev="g",
                            plural_abbrev="g", system=1, type=1)
        ing_amt = ingredient_amount_factory(
            amount=5.0, unit=unit, ingredient=ing)
        assert str(ing_amt) == f'{str(ing_amt.amount)} g of salt'


class TestIngredientModel:
    def test_str(self, ingredient_factory):
        ing = ingredient_factory(name="Pork")
        assert "Pork" == str(ing)


class TestUnitModel:
    def test_str(self, unit_factory):
        unit = unit_factory(name="gram", name_abbrev="g")
        assert str(unit) == "g"
        unit.name_abbrev = ""
        unit.save()
        assert str(unit) == "gram"
