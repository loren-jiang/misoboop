# Generated by Django 2.2.12 on 2020-06-01 03:18

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0017_auto_20200601_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direction',
            name='lazy_text',
            field=tinymce.models.HTMLField(default='', editable=False, verbose_name='Lazy Text'),
        ),
    ]
