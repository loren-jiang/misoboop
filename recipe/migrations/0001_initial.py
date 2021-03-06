# Generated by Django 2.2.12 on 2020-04-30 02:00

import adminsortable.fields
from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, null=True, unique=True)),
                ('use_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('1'), max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount')),
                ('ingredient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingredient_amounts', to='recipe.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Name')),
                ('name_abbrev', models.CharField(blank=True, max_length=60, verbose_name='Abbreviation')),
                ('plural_abbrev', models.CharField(blank=True, max_length=60, verbose_name='Plural Abbreviation')),
                ('type', models.IntegerField(choices=[(0, 'Other'), (1, 'Mass'), (2, 'Volume')])),
                ('system', models.IntegerField(choices=[(0, 'Metric'), (1, 'Imperial')], null=True)),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=500, unique=True)),
                ('short_description', models.TextField(default='')),
                ('description', tinymce.models.HTMLField(default='', verbose_name='Text')),
                ('prep_time', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('cook_time', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('large_image_url', models.URLField(default='https://via.placeholder.com/1000', max_length=300)),
                ('med_image_url', models.URLField(default='https://via.placeholder.com/400', max_length=300)),
                ('sm_image_url', models.URLField(default='https://via.placeholder.com/150', max_length=300)),
                ('servings', models.PositiveSmallIntegerField(default=1)),
                ('max_servings', models.PositiveSmallIntegerField(default=25)),
                ('is_published', models.BooleanField(default=False)),
                ('slug', models.SlugField(max_length=100)),
                ('likes', models.PositiveSmallIntegerField(default=1)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('image', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PublicImage')),
                ('ingredients', models.ManyToManyField(blank=True, through='recipe.IngredientAmount', to='recipe.Ingredient')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='core.Series')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='core.TaggedWhatever', to='core.BasicTag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_amounts', to='recipe.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ingredient_amounts', to='recipe.Unit'),
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('text', tinymce.models.HTMLField(default='', verbose_name='Text')),
                ('direction_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('ingredient_amounts', models.ManyToManyField(blank=True, to='recipe.IngredientAmount')),
                ('recipe', adminsortable.fields.SortableForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directions', to='recipe.Recipe')),
            ],
            options={
                'verbose_name': 'Direction',
                'verbose_name_plural': 'Directions',
                'ordering': ['direction_order'],
            },
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=Decimal('0')), name='amount_gte_0'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='no_duplicate_ingredients_in_recipe'),
        ),
        migrations.AddConstraint(
            model_name='direction',
            constraint=models.UniqueConstraint(fields=('recipe', 'text'), name='no duplicate direction per recipe'),
        ),
    ]
