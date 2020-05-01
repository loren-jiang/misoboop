# Generated by Django 2.2.12 on 2020-05-01 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20200501_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='name_abbrev',
            field=models.CharField(blank=True, max_length=60, verbose_name='Abbreviation'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='plural_abbrev',
            field=models.CharField(blank=True, max_length=60, verbose_name='Plural Abbreviation'),
        ),
    ]
