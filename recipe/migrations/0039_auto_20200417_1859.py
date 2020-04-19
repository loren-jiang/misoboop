# Generated by Django 3.0.5 on 2020-04-17 18:59

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0038_auto_20200416_2035'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredientamount',
            name='amount_gt_0',
        ),
        migrations.AlterField(
            model_name='ingredientamount',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('1'), max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Amount'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamount',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=Decimal('0')), name='amount_gte_0'),
        ),
    ]
