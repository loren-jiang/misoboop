# Generated by Django 2.2.12 on 2020-05-06 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_publicimage_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='image',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.PublicImage'),
        ),
    ]
