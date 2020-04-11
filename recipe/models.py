from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from core.models import CreatedModified
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import User, Group
from taggit.managers import TaggableManager

# Create your models here.
class Recipe(CreatedModified):
    """

    """
    author = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True, unique=True)
    prep_time = models.PositiveSmallIntegerField(blank=True, null=True)
    cook_time = models.PositiveSmallIntegerField(blank=True, null=True)
    image_url = models.URLField(max_length=300, blank=True, null=True)
    ingredients = models.ManyToManyField('Ingredient', through='IngredientAmount', blank=True)
    servings = models.PositiveSmallIntegerField(default=1)
    tags = TaggableManager()

    class Meta:
        ordering = ['name']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def __str__(self):
        return self.name

    def get_ingredient_amounts_as_list(self):
        """
        Get ingredient amounts as list for given recipe with optimized select_related
        :return: list of ingredient amounts
        """
        ingredients = self.ingredient_amounts.select_related('ingredient', 'unit')
        return list(ingredients)

    def get_directions_as_text(self):
        """
        Get directions as single string
        :return: stirng of directions concatenated
        """
        directions_text = ''
        for i, direction in enumerate(self.directions.all()):
            directions_text += f"{str(i + 1)}) {direction.text} \n"
        return directions_text


class Direction(SortableMixin):
    name = models.CharField(max_length=100, default='')
    text = models.TextField(blank=True, verbose_name=_('Text'))
    recipe = SortableForeignKey('Recipe', related_name='directions', on_delete=models.CASCADE)
    order_with_respect_to = 'recipe'
    ingredient_amounts = models.ManyToManyField('IngredientAmount', blank=True)
    direction_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Direction')
        verbose_name_plural = _('Directions')
        ordering=['direction_order']


class Ingredient(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, unique=True)
    use_count = models.PositiveIntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        return self.name

class IngredientAmount(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=12,  validators=[MinValueValidator(Decimal('0.01'))],
                                 verbose_name=_('Amount'), default=Decimal('1'))
    unit = models.ForeignKey('Unit', related_name='ingredient_amounts', on_delete=models.SET_NULL, null=True, blank=True)
    # quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('quantity'))
    recipe = models.ForeignKey('Recipe', related_name='ingredient_amounts', on_delete=models.CASCADE, null=True, blank=True)
    ingredient = models.ForeignKey('Ingredient', related_name='ingredient_amounts', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return ' | '.join(list(map(lambda s: str(s), [self.ingredient, self.amount, self.unit] )))

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=Decimal('0')), name='amount_gt_0'),
            models.UniqueConstraint(fields=('recipe', 'ingredient'), name='no_duplicate_ingredients_in_recipe')
        ]


class Unit(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('Name'))
    name_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Abbreviation'))
    plural_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Plural Abbreviation'))
    TYPE = Choices((0, 'other', 'Other'), (1, 'mass', 'Mass'), (2, 'volume', 'Volume'))
    type = models.IntegerField(choices=TYPE)
    SYSTEM = Choices((0, 'metric', 'Metric'), (1, 'imperial', 'Imperial'))
    system = models.IntegerField(choices=SYSTEM, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ["name"]
