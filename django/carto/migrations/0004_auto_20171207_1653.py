# Generated by Django 2.0rc1 on 2017-12-07 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carto', '0003_auto_20171207_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='alpha',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
        migrations.AddField(
            model_name='layer',
            name='colormap',
            field=models.CharField(default='hot', max_length=20),
        ),
    ]
