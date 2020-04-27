# Generated by Django 2.2.12 on 2020-04-27 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0053_recipe_max_servings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.OneToOneField(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PublicImage'),
        ),
    ]
