# Generated by Django 2.2.12 on 2020-05-02 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_auto_20200501_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='system',
            field=models.IntegerField(choices=[(0, 'Other'), (1, 'Metric'), (2, 'Imperial')], null=True),
        ),
    ]
