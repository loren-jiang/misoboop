from django.test import TestCase
from .factories import RecipeFactory

class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_str(self):
        self.assertEqual(RecipeFactory(name="cheddar doughnuts").name, "cheddar doughnuts")

    def test_total_time(self):
        self.assertEqual(RecipeFactory(cook_time=30, prep_time=45).total_time(), 75)

    def test_slug_is_created_automatically(self):
        banana_bread = RecipeFactory(name="banana bread")
        self.assertEqual(banana_bread.slug, "banana-bread")
        yogurt = RecipeFactory(name="yogurt")
        self.assertEqual(yogurt.slug, "yogurt")

    def test_get_absolute_url(self):
        char_siu_pork = RecipeFactory(name="char siu pork")
        self.assertEqual(char_siu_pork.get_absolute_url(), "/recipes/recipe/char-siu-pork/")

    def test_adding_tags(self):
        char_siu_pork = RecipeFactory(name="char siu pork")
        char_siu_pork.tags.add("Pork", "Chinese", "Comfort food")
        self.assertListEqual([tag.name for tag in char_siu_pork.tags.order_by('name')],
                             ["Chinese", "Comfort food", "Pork"])

    def test_no_duplicate_tags(self):
        char_siu_pork = RecipeFactory(name="char siu pork")
        char_siu_pork.tags.add("Pork", "Chinese", "Chinese")
        self.assertListEqual([tag.name for tag in char_siu_pork.tags.order_by('name')],
                             ["Chinese", "Pork"])



