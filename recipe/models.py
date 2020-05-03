import datetime
from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from core.models import CreatedModified
from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.urls import reverse
from tinymce import HTMLField
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from core.models import BasicTag, TaggedWhatever
import math
# Create your models here.


# todo: add hitCount? https://django-hitcount.readthedocs.io/en/latest/installation.html
class Recipe(CreatedModified):
    """
    Model representing a recipe, which roughly follows https://jsonld.com/recipe/
    """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=500, unique=True)
    short_description = models.TextField(default='')
    description = HTMLField(default='', verbose_name=_('Text'))
    prep_time = models.PositiveSmallIntegerField(default=0)
    cook_time = models.PositiveSmallIntegerField(default=0)
    image = models.OneToOneField('core.PublicImage', on_delete=models.SET_NULL, blank=True, null=True)
    placeholder_url = models.URLField(max_length=300, default="https://via.placeholder.com/400")
    ingredients = models.ManyToManyField('Ingredient', through='IngredientAmount', blank=True)
    servings = models.PositiveSmallIntegerField(default=1)
    max_servings = models.PositiveSmallIntegerField(default=25)
    tags = TaggableManager(through=TaggedWhatever, blank=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, editable=False)
    likes = models.PositiveSmallIntegerField(default=1)
    ratings = GenericRelation(Rating, related_query_name='recipes')
    series = models.ForeignKey('core.Series', on_delete=models.SET_NULL, blank=True, null=True, related_name='recipes')

    class Meta:
        ordering = ['name',]
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_time(self):
        return self.cook_time + self.prep_time

    def tag_names_as_list(self):
        return [tag.name for tag in self.tags.order_by('name')]


    def ing_amts_as_list(self):
        """
        Get ingredient amounts as list for given recipe with optimized select_related
        :return: list of ingredient amounts
        """
        ingredients = self.ingredient_amounts.select_related('ingredient', 'unit')
        return [f'{str(ing.amount)} {str(ing.unit)} {str(ing.ingredient)}' for ing in ingredients]

    def get_directions_as_text(self):
        """
        Get directions as single string
        :return: stirng of directions concatenated
        """
        directions_text = ''
        for i, direction in enumerate(self.directions.all()):
            directions_text += f"{str(i + 1)}) {direction.text} \n"
        return directions_text

    def get_directions_as_list(self):
        directions_list = [''] * self.directions.count()
        for i, direction in enumerate(self.directions.all()):
            directions_list[i] = (f"{str(i + 1)}) {direction.text}")
        return directions_list

    def get_pdf_printout(self):
        pass

    def image_url(self):
        if self.image:
            return self.image.upload.url
        return ''

    @property
    def sd(self):
        return {
            "@context": "https://schema.org",
            "@type": "Recipe",
            "author": str(self.author),
            "cookTime": self.cook_time,
            "datePublished": self.created_at.date().isoformat(),
            "description": self.description,
            "image": self.image_url(),
            "recipeIngredient": self.ing_amts_as_list(),
            "interactionStatistic": {
                "@type": "InteractionCounter",
                "interactionType": "http://schema.org/Comment",
                "userInteractionCount": self.likes
            },
            "name": self.name,
            "nutrition": {
                # todo: need to implement Nutrition model
                "@type": "NutritionInformation",
                "calories": "1200 calories",
                "carbohydrateContent": "12 carbs",
                "proteinContent": "9 grams of protein",
                "fatContent": "9 grams fat"
            },
            "prepTime": self.prep_time,
            "recipeInstructions": self.get_directions_as_list(),
            "recipeYield": self.servings
        }


class Direction(SortableMixin):
    name = models.CharField(max_length=100, default='')
    text = HTMLField(default='', verbose_name=_('Text'))
    # rich_text = HTMLField(default='')
    recipe = SortableForeignKey('Recipe', related_name='directions', on_delete=models.CASCADE)
    order_with_respect_to = 'recipe'
    ingredient_amounts = models.ManyToManyField('IngredientAmount', blank=True)
    direction_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Direction')
        verbose_name_plural = _('Directions')
        ordering = ['direction_order']
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'text'], name='no duplicate direction per recipe')
        ]


class Ingredient(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True, unique=True)
    name_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Abbreviation'))
    plural_name = models.CharField(max_length=60, blank=True, verbose_name=_('Plural name'))
    use_count = models.PositiveIntegerField(default=0)
    # tags = TaggableManager()

    class Meta:
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(Decimal('0.00'))],
                                 verbose_name=_('Amount'), default=Decimal('1'))
    unit = models.ForeignKey('Unit', related_name='ingredient_amounts', on_delete=models.SET_NULL, null=True,
                             blank=True)
    # quantity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_('quantity'))
    recipe = models.ForeignKey('Recipe', related_name='ingredient_amounts', on_delete=models.CASCADE, null=True,
                               blank=True)
    ingredient = models.ForeignKey('Ingredient', related_name='ingredient_amounts', on_delete=models.SET_NULL,
                                   null=True, blank=True)

    def __str__(self):
        return ' | '.join(list(map(lambda s: str(s), [self.ingredient, self.amount, self.unit])))

    def prefix(self):
        """
        Outputs nicely formatted number ('prefix') depending on system of measurement; limits to one decimal place
        :return: str
        """
        # todo: not sure if this should just be handled server side since the whole point is scaling and convert
        # from metric to imperial

        # if imperial, we want to represent as fraction


        # first, round to nearest 0.25 since that's really the precision achievable from cooking measurements
        rounded_amt = round(self.amount * 100 // 25 + self.amount * 100 % 25) / 100
        pass


    def suffix(self):
        """
        Outputs nicely formatted descriptor of ingredient amount ('suffix') depending on plurality and units
        :return: str
        """
        is_plural = self.amount > 1
        has_real_unit = self.unit.name != "Unit"
        ret = ''
        if not has_real_unit:
            ret = f"{self.ingredient.plural_name if (is_plural and self.ingredient.plural_name) else self.ingredient.name}"
        else:
            ret = f"{self.unit.plural_abbrev  + ' of'} " \
               f"{self.ingredient.plural_name if (is_plural and self.ingredient.plural_name) else self.ingredient}"
        return ret.lower()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gte=Decimal('0')), name='amount_gte_0'),
            models.UniqueConstraint(fields=('recipe', 'ingredient'), name='no_duplicate_ingredients_in_recipe')
        ]

class Unit(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('Name'))
    name_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Abbreviation'))
    plural_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Plural Abbreviation'))
    TYPE = Choices((0, 'other', 'Other'), (1, 'mass', 'Mass'), (2, 'volume', 'Volume'))
    type = models.IntegerField(choices=TYPE)
    SYSTEM = Choices((0, 'other', 'Other'), (1, 'metric', 'Metric'), (2, 'imperial', 'Imperial'))
    system = models.IntegerField(choices=SYSTEM, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ["name"]


