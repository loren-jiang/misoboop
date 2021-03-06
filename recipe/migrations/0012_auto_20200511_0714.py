# Generated by Django 2.2.12 on 2020-05-11 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_basictag_is_cuisine'),
        ('recipe', '0011_recipe_nutrition'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='image',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PublicImage'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='is_specialty',
            field=models.BooleanField(default=False),
        ),
    ]
