from django.test import TestCase, override_settings
from .factories import RecipeFactory
import tempfile
import shutil
from core.models import PublicImage

MEDIA_ROOT = tempfile.mkdtemp('_temp')
print(f'MEDIA_ROOT is now {MEDIA_ROOT}')

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
        self.assertTrue(settings.THUMBNAIL_STORAGE == 'inmemorystorage.InMemoryStorage')
        self.assertTrue(settings.DEFAULT_FILE_STORAGE == 'inmemorystorage.InMemoryStorage')
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
        self.assertEqual(RecipeFactory(cook_time=30, prep_time=45).total_time(), 75)

    def test_slug_is_created_automatically(self):
        self.assertEqual(self.test_recipe.slug, "char-siu-pork")
        yogurt = RecipeFactory(name="yogurt")
        self.assertEqual(yogurt.slug, "yogurt")

    def test_get_absolute_url(self):
        self.assertEqual(self.test_recipe.get_absolute_url(), "/recipes/recipe/char-siu-pork/")

    def test_tag_names_as_list(self):
        self.assertListEqual(self.test_recipe.tag_names_as_list(), ["Chinese", "Comfort food", "Pork"])

    def test_adding_tags(self):
        self.test_recipe.tags.add("Takeout", "Cantonese")
        self.assertListEqual(self.test_recipe.tag_names_as_list(),
                             ["Cantonese", "Chinese", "Comfort food", "Pork", "Takeout"])

    def test_no_duplicate_tags(self):
        old_count = self.test_recipe.tags.count()
        self.test_recipe.tags.add("Pork", "Chinese", "Chinese")
        self.assertEqual(self.test_recipe.tags.count(), old_count)

    def test_sd(self):
        pass

    def test_image_url(self):
        pass

    def test_ing_amts_as_list(self):
        pass

