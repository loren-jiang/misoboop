# Generated by Django 2.2.12 on 2020-05-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_series_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='basictag',
            name='is_cuisine',
            field=models.BooleanField(default=False),
        ),
    ]