# Generated by Django 2.2.12 on 2020-04-28 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200422_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='series',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='core.Series'),
        ),
    ]
