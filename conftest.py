import pytest
import os
import shutil
from django.conf import settings
from pytest_factoryboy import register

from core.tests.factories import SeriesFactory, TagFactory, PublicImageFactory
from blog.tests.factories import PostFactory
from recipe.tests.factories import DirectionFactory, RecipeFactory, IngredientAmountFactory, IngredientFactory, UnitFactory, NutritionFactory

register(TagFactory)
register(SeriesFactory)
register(PostFactory)
register(RecipeFactory)
register(IngredientAmountFactory)
register(IngredientFactory)
register(UnitFactory)
register(NutritionFactory)
register(DirectionFactory)
register(PublicImageFactory)


@pytest.fixture
def ten_posts(post_factory):
    return [post_factory() for _ in range(10)]


@pytest.fixture
def ten_seriess(series_factory):
    return [series_factory() for _ in range(10)]


@pytest.fixture
def ten_recipes(recipe_factory):
    return [recipe_factory() for _ in range(10)]


@pytest.fixture
def ten_ingredients(ingredient_factory):
    return [ingredient_factory() for _ in range(10)]


@pytest.fixture
def basic_units(unit_factory):
    units = {}
    units['gram'] = unit_factory(
        name='gram', name_abbrev='g', plural_abbrev='g', type=1, system=1)
    units['unit'] = unit_factory(name='unit', type=0, system=0)
    units['tbsp'] = unit_factory(
        name='tablesppon', name_abbrev='tbsp', plural_abbrev='tbsps', type=2, system=2)
    units['cup'] = unit_factory(
        name='cup', name_abbrev='cup', plural_abbrev='cups', type=2, system=2)
    units['package'] = unit_factory(
        name='package', type=0, system=0)
    units['pound'] = unit_factory(
        name='pound', name_abbrev='lb', plural_abbrev='lbs', type=2, system=2)

    return units

@pytest.fixture
def complete_post(post_factory, public_image_factory, admin_user):
    post = post_factory()
    post.image = public_image_factory()
    post.author = admin_user
    post.save()
    return post

@pytest.fixture
def complete_recipe(recipe_factory, admin_user, nutrition_factory, public_image_factory, direction_factory, ingredient_factory, ingredient_amount_factory, basic_units):
    # TODO: implement a complete recipe fixture
    recipe = recipe_factory()
    recipe.author = admin_user
    recipe.name = "Kimchi Fried Rice"
    recipe.nutrition = nutrition_factory()
    recipe.tags.add(*['Pork', 'Stir-fry'])

    recipe.total_time = 30
    recipe.prep_time = 5
    recipe.cook_time = 25
    recipe.short_description = "My take on a favorite college dinner of mine. Kimchi fried rice is quick-to-make, filling, and super tasty."
    recipe.description = "<h3>Secret ingredients?</h3>\r\n<p>This recipe is pretty straight forward and highly adaptable, but I do think the addition of two ingredients do elevate it. Butter and chicken apple sausage. I think butter gives a richness and nutty note that really compliments the stronger flavors of kimchi and sesame oil. Chicken apple sausage (from Trader Joe's) is something I usually have in the fridge and adds a really nice sweetness. I've used bacon before, but I've found the saltiness and fat from the bacon to be a bit overwhelming.</p>\r\n<p>In terms of specialty Korean ingredients, I have a few things to note.</p>\r\n<ul>\r\n<li>I'm not a kimchi expert, but I do find the fishier, more pungent ones to work really well for cooking. Ultimately, the choice is yours!&nbsp;</li>\r\n<li>Any garlic should be fine, but in most Asian markets they will sell minced garlic, which I find to be even more powerful.</li>\r\n<li>The strength and flavor of sesame oil vary a lot. I'm actually using a Korean perilla oil, which I find to have a stronger, deeper sesame flavor, but you may need to adjust the quantity to taste.</li>\r\n</ul>\r\n<p><img src=\"https://thumbnails-photos.amazon.com/v1/thumbnail/PPLbKpx6SMeFxPjbTJupQA?viewBox=1000%2C666&amp;ownerId=A2SSMUSNBKJMOU&amp;groupShareToken=0VNoLb-GRji2VP1Z5dbgoA.t7xBreg_5XRT9nsPv4Kga3\" alt=\"kimchi fried rice ingredients\" width=\"500\" height=\"333\" /><img src=\"https://thumbnails-photos.amazon.com/v1/thumbnail/cLmouPAdSmiRkQs6vVIozQ?viewBox=1000%2C666&amp;ownerId=A2SSMUSNBKJMOU&amp;groupShareToken=0VNoLb-GRji2VP1Z5dbgoA.t7xBreg_5XRT9nsPv4Kga3\" alt=\"\" width=\"500\" height=\"333\" /></p>\r\n<p>&nbsp;</p>\r\n<h3>Miso boop.</h3>\r\n<p><img src=\"https://thumbnails-photos.amazon.com/v1/thumbnail/saJiZQyTSbeJ9HRznSTkTg?viewBox=1000%2C666&amp;ownerId=A2SSMUSNBKJMOU&amp;groupShareToken=0VNoLb-GRji2VP1Z5dbgoA.t7xBreg_5XRT9nsPv4Kga3\" alt=\"blurry boop\" width=\"400\" height=\"266\" /></p>\r\n<p>&nbsp;</p>\r\n<h5>A couple of notes:</h5>\r\n<ul>\r\n<li>I didn't chop the kimchi because 1) I actually like large chunks of kimchi, 2) kimchi juice really does leave a lasting mark, and 3) I'm pretty lazy. Feel free to chop, though!</li>\r\n</ul>"
    recipe.servings = 2
    recipe.max_servings = 25
    recipe.image = public_image_factory()

    ingredients_list = [
        {"name": "Light soy sauce", "unit": basic_units['tbsp'], "amount": 2},
        {"name": "Egg", "unit": basic_units['unit'], "amount": 2},
        {"name": "Sesame oil", "unit": basic_units['tbsp'], "amount": 1},
        {"name": "Chicken apple sausage",
            "unit": basic_units['unit'], "amount": 1},
        {"name": "Butter", "unit": basic_units['tbsp'], "amount": 1.5},
        {"name": "Cooked white rice", "unit": basic_units['cup'], "amount": 3},
        {"name": "Roasted seaweed",
            "unit": basic_units['package'], "amount": 1},
        {"name": "Kimchi", "unit": basic_units['cup'], "amount": 0.5},
        {"name": "Diced onion", "unit": basic_units['cup'], "amount": 0.5},
        {"name": "Kimchi juice", "unit": basic_units['tbsp'], "amount": 2},
        {"name": "Green onion", "unit": basic_units['unit'], "amount": 1},
        {"name": "Minced garlic", "unit": basic_units['tbsp'], "amount": 1},

    ]

    ing_instances = []
    for ing in ingredients_list:
        ing_instance = ingredient_factory(name=ing['name'])
        ing_amt = ingredient_amount_factory(
            ingredient=ing_instance, unit=ing['unit'], amount=ing['amount'])
        ing_instances.append(ing_instance)

    recipe.ingredients.add(*ing_instances)

    directions = [
        {
            "name": "Sautee with butter",
            "text": """ 
            <p>In large non-stick pan or wok on medium heat, sautee sausage and onions with butter until translucent and slightly browned -- should take about 3 minutes. Then add minced garlic, kimchi, lower end of gree onion, and kimchi juice to pan and cook until liquid is about halfway reduced.</p>
            <p><img src="https://thumbnails-photos.amazon.com/v1/thumbnail/Bs6BjZjVSqGZnVZjatj0qg?viewBox=1000%2C666&amp;ownerId=A2SSMUSNBKJMOU&amp;groupShareToken=0VNoLb-GRji2VP1Z5dbgoA.t7xBreg_5XRT9nsPv4Kga3" alt="" width="600" height="400" /></p>
            """,
        },
        {
            "name": 'Add rice and "crispify"',
            "text": """ 
            <p>Add rice and break up large chunks until well incorporated. Add sesame oil and soy sauce and compress the ingredients in the pan. We want a nice, flat surface for the rice to start frying and get crispy! Optionally, you can make a well in the center for an egg.</p>
            <p>After about 5 minutes, you should start achieving a nice crust on the bottom, which in my opinion is the best part. Now, add half of the roasted seaweed and mix up the rice to break the crust into smaller pieces.</p>
            <p><img src="https://thumbnails-photos.amazon.com/v1/thumbnail/XMQEzLYgRYWaDCTBkZidKw?viewBox=1000%2C666&amp;ownerId=A2SSMUSNBKJMOU&amp;groupShareToken=0VNoLb-GRji2VP1Z5dbgoA.t7xBreg_5XRT9nsPv4Kga3" alt="" width="600" height="400" /></p>
            """,
        },
        {
            "name": "Fry an egg (optional)",
            "text": """ 
            <p>In a separate pan, fry up an egg sunny side up</p>
            """,
        },
        {
            "name": "Garnish and plate",
            "text": """ 
            <p>Put rice into bowl along with the fried egg. Garnish with sesame seeds, the remainder of the roasted seaweed, and the upper ends of the green onion. Add sriracha if ya want a little heat. Enjoy!</p>
            """,
        }
    ]
    dir_instances = []
    for direction in directions:
        direction['recipe_id'] = recipe.id
        dir_instances.append(direction_factory(**direction))
    recipe.directions.add(*dir_instances)

    recipe.save()
    return recipe




def pytest_sessionstart(session):
    print("\ntesting started")

    if (settings.MEDIA_ROOT == "_temp" and not os.path.exists('_temp')):
        print("\ncreating '_temp' folder")
        os.mkdir('_temp')


def pytest_sessionfinish(session, exitstatus):
    print("\ntesting concluded")
    # delete _temp directory after testing
    if (settings.MEDIA_ROOT == "_temp" and os.path.exists('_temp')):
        shutil.rmtree("_temp")

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('MB_DB_NAME'),
#         'USER': os.getenv('MB_DB_USER'),
#         'PASSWORD': os.getenv('MB_DB_PASSWORD'),
#         'HOST': os.getenv('MB_DB_HOST'),
#         'PORT': os.getenv('MB_DB_PORT'),
#     }
