# Generated by Django 2.2.12 on 2020-05-01 17:10

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200430_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicimage',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
