# Generated by Django 2.2.12 on 2020-06-09 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0018_auto_20200601_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='cuisine',
            field=models.CharField(default='', max_length=500),
        ),
    ]