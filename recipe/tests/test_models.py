from django.test import TestCase, override_settings
from .factories import RecipeFactory
import tempfile
import shutil
from core.models import PublicImage
import json
import jsonschema

MEDIA_ROOT = tempfile.mkdtemp('_temp')
print(f'MEDIA_ROOT is now {MEDIA_ROOT}')

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

# TODO: there might be a better way to validate json-ld via online api, but for now use this


def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True


@override_settings(
    MEDIA_ROOT=MEDIA_ROOT,
    THUMBNAIL_STORAGE="inmemorystorage.InMemoryStorage",
    DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # make sure we're using in-memory test env.
        from django.conf import settings
        self.assertTrue(settings.THUMBNAIL_STORAGE ==
                        'inmemorystorage.InMemoryStorage')
        self.assertTrue(settings.DEFAULT_FILE_STORAGE ==
                        'inmemorystorage.InMemoryStorage')
        # todo: clearly something wrong with sorl.thumbnail not using correct storage...
        # new_image = PublicImage(
        #     name='temp_image',
        #   upload=tempfile.NamedTemporaryFile(suffix='.jpg'))
        # new_image.save()
        # self.test_recipe = RecipeFactory(
        #     name='Chinese smashed cucumbers',
        #     image=new_image
        # )

        self.test_recipe = RecipeFactory(name="Char siu pork")
        self.test_recipe.tags.add("Pork", "Chinese", "Comfort food")

    def tearDown(self):
        # shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        pass

    def test_str(self):
        self.assertEqual(str(self.test_recipe), "Char siu pork")

    def test_total_time(self):
        self.assertEqual(RecipeFactory(
            cook_time=30, prep_time=45).total_time(), 75)

    def test_slug_is_created_automatically(self):
        self.assertEqual(self.test_recipe.slug, "char-siu-pork")
        yogurt = RecipeFactory(name="yogurt")
        self.assertEqual(yogurt.slug, "yogurt")

    def test_get_absolute_url(self):
        self.assertEqual(self.test_recipe.get_absolute_url(),
                         "/recipes/recipe/char-siu-pork/")

    def test_tag_names_as_list(self):
        self.assertListEqual(self.test_recipe.tag_names_as_list(), [
                             "Chinese", "Comfort food", "Pork"])

    def test_adding_tags(self):
        self.test_recipe.tags.add("Takeout", "Cantonese")
        self.assertListEqual(self.test_recipe.tag_names_as_list(),
                             ["Cantonese", "Chinese", "Comfort food", "Pork", "Takeout"])

    def test_no_duplicate_tags(self):
        old_count = self.test_recipe.tags.count()
        self.test_recipe.tags.add("Pork", "Chinese", "Chinese")
        self.assertEqual(self.test_recipe.tags.count(), old_count)

    def test_validate_sd_schema(self):

        json_ld = self.test_recipe.sd
        print(json_ld)
        assert validate_json(json_ld, recipe_schema) == True

    def test_image_url(self):
        pass

    def test_ing_amts_as_list(self):
        pass
