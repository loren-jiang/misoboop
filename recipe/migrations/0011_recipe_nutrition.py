# Generated by Django 2.2.12 on 2020-05-10 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_nutrition'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='nutrition',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipe.Nutrition'),
        ),
    ]
