from factory import faker
import factory
import random
from recipe.models import Unit
from decimal import Decimal

LIST_SIZES = [1, 2, 3, 4, 5]

UNIT_TYPES_CHOICES = Unit.TYPE
UNIT_SYSTEM_CHOICES = Unit.SYSTEM

fake = faker.Faker('en_US')


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.Recipe'

    name = factory.Sequence(lambda n: f'recipe{n}')
    description = factory.LazyAttribute(
        lambda obj: f'description for ${obj.name}')
    # ingredient_amounts = factory.RelatedFactoryList('recipe.tests.factories.IngredientAmountFactory',
    #                                                 factory_related_name="recipe", size=lambda: random.randint(50, 100))
    # directions = factory.RelatedFactoryList(
    #     'recipe.tests.factories.DirectionFactory', factory_related_name="recipe", size=lambda: random.randint(5, 15))

    @factory.post_generation
    def post(obj, create, extracted, **kwargs):
        if not create:
            return
        if kwargs.get('randomize'):
            IngredientAmountFactory.create_batch(
                size=random.randint(50, 100), recipe_id=obj.id)
            DirectionFactory.create_batch(
                size=random.randint(5, 15), recipe_id=obj.id)

            ingredients_amounts = [
                ing_amt for ing_amt in obj.ingredient_amounts.all()]
            num_ing_amts = len(ingredients_amounts)
            for direction in obj.directions.all():
                start_idx = random.randint(0, num_ing_amts - 1)
                end_idx = random.randint(start_idx, num_ing_amts - 1)
                direction.ingredient_amounts.add(
                    *random.sample(ingredients_amounts, random.randint(0, num_ing_amts//2)))


class DirectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.Direction'
    name = factory.Sequence(lambda n: f'direction{n}')
    text = factory.Sequence(lambda n: f'direction_text{n}')


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.Ingredient'
    name = factory.Sequence(lambda n: f'ingredient{n}')
    name_abbrev = factory.Sequence(lambda n: f'ing{n}')
    plural_name = factory.Sequence(lambda n: f'ingredients{n}')


class IngredientAmountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.IngredientAmount'
    amount = Decimal(random.randint(0, 100))
    unit = factory.SubFactory('recipe.tests.factories.UnitFactory')
    ingredient = factory.SubFactory('recipe.tests.factories.IngredientFactory')


class UnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'recipe.Unit'
    name = factory.Sequence(lambda n: f'unit{n}')
    type = random.randint(0, 2)
    system = random.randint(0, 2)
