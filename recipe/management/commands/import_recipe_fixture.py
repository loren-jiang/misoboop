import json
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from recipe.models import Recipe, IngredientAmount, Ingredient, Direction, Unit
from django.utils import timezone
import re
from decimal import Decimal
from fractions import Fraction
from functools import reduce

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

class Command(BaseCommand):
    help = ''
    def handle(self, *args, **options):
        with open('fixtures/recipe_fixture.json') as file:
            recipe_fixture = json.load(file)
            directions = defaultdict(list)
            ingredients = defaultdict(list)
            recipes = []
            for key in recipe_fixture.keys():

                recipe = recipe_fixture[key]
                ingredients[recipe['name']] = recipe['ingredients']
                for d in recipe['instructions'].split('.'):
                    directions[recipe['name']].append(d)

                recipes.append(Recipe(
                    name=recipe['name'],
                    servings=recipe['servings'],
                    cook_time=recipe['cook_time'],
                    prep_time=recipe['prep_time'],
                ))

            recipes_created = Recipe.objects.bulk_create(recipes, ignore_conflicts=True)
            recipes_qs = Recipe.objects.filter(name__in=[recipe.name for recipe in recipes_created])

            ingredient_amts_to_create = []

            directions_to_create = []

            for r in recipes_qs:
                r_dirs = directions[r.name]
                for d in r_dirs:
                    directions_to_create.append(Direction(recipe=r, text=d, name=d))

                r_ings = ingredients[r.name]
                for i in r_ings:
                    if i:
                        i_split = i.split(' ')
                        nums = list(filter(lambda x: hasNumbers(x), i_split))
                        amt = Fraction('0/1')
                        if nums:
                            try:
                                amt = reduce(lambda x,y: Fraction(x) + Fraction(y), nums, Fraction('0/1'))
                            except ValueError:
                                pass
                        i_unit = i_split[len(nums)] if amt else None
                        b = int(bool(amt))
                        i_name = ' '.join(i_split[len(nums)+b:])
                        # print(amt, i_unit, i_name)
                        if i_unit:
                            unit, created = Unit.objects.get_or_create(name=i_unit, type=2, system=1)
                        else:
                            unit = None
                        ing, created = Ingredient.objects.get_or_create(name=i_name)
                        ingredient_amts_to_create.append(IngredientAmount(unit=unit, recipe=r, ingredient=ing, amount=Decimal(float(amt))))
            # IngredientAmount.objects.bulk_create(ingredient_amts_to_create, ignore_conflicts=True)

            # for el in ingredient_amts_to_create:
            #     i_a = IngredientAmount.objects.get(recipe=el.recipe,
            #           ingredient=el.ingredient)
            #     i_a.unit = el.unit
            #     i_a.save()

            directions_created = Direction.objects.bulk_create(directions_to_create, ignore_conflicts=True)


            file.close()




