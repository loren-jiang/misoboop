# Generated by Django 2.2.12 on 2020-04-30 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicimage',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
