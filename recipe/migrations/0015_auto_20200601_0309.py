# Generated by Django 2.2.12 on 2020-06-01 03:09

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0014_recipe_lazy_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='lazy_description',
            field=tinymce.models.HTMLField(default='', editable=False, verbose_name='Lazy Text'),
        ),
    ]