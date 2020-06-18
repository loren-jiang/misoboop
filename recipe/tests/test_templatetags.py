import pytest
from recipe.templatetags import recipe_extras

pytestmark = pytest.mark.django_db

class TestTemplateTags:
    def test_render_ing_amt(self, ingredient_amount_factory):
        ing_amt = ingredient_amount_factory()
        assert recipe_extras.render_ing_amt(ing_amt) == ing_amt.suffix()